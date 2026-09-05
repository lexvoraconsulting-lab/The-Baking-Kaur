#!/usr/bin/env python3
"""
Self-check for ai.attribute_intelligence's core: ids, models, normalizer,
validator, confidence engine, conflict resolution, rule-based inference,
history log, search, exporter, observability, and the end-to-end
AttributeIntelligenceService flow - no network calls.

USAGE
  python -m ai.attribute_intelligence.test_attribute_intelligence
"""
import tempfile
from pathlib import Path

from ai.ead.loader import load_definitions
from ai.ear.loader import load_registry
from ai.taxonomy.catalog import TaxonomyCatalog
from ai.taxonomy.loader import load_catalog
from ai.taxonomy.models_pydantic import RelationshipModel, TermModel, VocabularyModel

from ai.attribute_intelligence.confidence import AttributeConfidenceEngine
from ai.attribute_intelligence.conflicts import AttributeConflictResolver
from ai.attribute_intelligence.exporter import export_profile
from ai.attribute_intelligence.history import AttributeHistoryLog
from ai.attribute_intelligence.inference import AttributeInferenceEngine, TaxonomyRelationshipInferenceRule
from ai.attribute_intelligence.models import AttributeObservation, ResolvedAttribute, SubjectAttributeProfile
from ai.attribute_intelligence.normalizer import AttributeNormalizer
from ai.attribute_intelligence.observability import compute_coverage_report, compute_drift
from ai.attribute_intelligence.search import AttributeSearchService
from ai.attribute_intelligence.service import AttributeIntelligenceService
from ai.attribute_intelligence.validator import AttributeValidator


def _obs(registry_reference="EAR-000001", subject_id="gid://shopify/Product/1", source="vision",
         value="Red", confidence=0.9, observed_at="2026-08-02T00:00:00Z") -> AttributeObservation:
    return AttributeObservation(registry_reference, subject_id, source, value, confidence, observed_at)


def test_observation_id_is_deterministic():
    a = _obs()
    b = _obs()
    assert a.observation_id == b.observation_id


def test_normalizer_matches_real_taxonomy_term_and_synonym():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    normalizer = AttributeNormalizer(catalog)
    term = normalizer.normalize("Red", vocabulary_id_or_name="TAX-VOC-000001")
    assert term is not None and term.label == "Red"

    by_synonym = normalizer.normalize("Crimson", vocabulary_id_or_name="Colour Name")
    assert by_synonym is not None and by_synonym.term_id == "TAX-TERM-000002"

    unmatched = normalizer.normalize("Chartreuse")
    assert unmatched is None


def test_validator_flags_missing_confidence_and_unknown_definition():
    validator = AttributeValidator()
    issues = validator.validate(_obs(confidence=None), definition=None)
    codes = {i.code for i in issues}
    assert "missing_confidence" in codes and "no_definition" in codes


def test_validator_enforces_allowed_values_and_minimum_confidence():
    definitions = load_definitions("ai/ead/examples/definitions.json")
    definition = definitions.get("EAR-000001")
    validator = AttributeValidator()

    if definition.allowed_values:
        bad_value = validator.validate(_obs(value="not-a-real-colour"), definition)
        assert any(i.code == "value_not_allowed" for i in bad_value)

    low_conf = validator.validate(_obs(confidence=0.01), definition)
    assert any(i.code == "below_minimum_confidence" for i in low_conf)


def test_confidence_engine_ranks_manual_over_vision_regardless_of_raw_confidence():
    engine = AttributeConfidenceEngine()
    vision_obs = _obs(source="vision", value="Red", confidence=0.99)
    manual_obs = _obs(source="manual", value="Blue", confidence=0.5)
    winner, method = engine.resolve_best([vision_obs, manual_obs])
    assert winner.source == "manual" and method == "highest_trust"


def test_confidence_engine_single_source_when_all_agree():
    engine = AttributeConfidenceEngine()
    a = _obs(source="vision", value="Red", confidence=0.9)
    b = _obs(source="shopify", value="Red", confidence=1.0)
    winner, method = engine.resolve_best([a, b])
    assert method == "single_source"


def test_conflict_resolver_produces_a_conflict_record_and_keeps_every_observation():
    resolver = AttributeConflictResolver()
    a = _obs(source="vision", value="Red", confidence=0.9)
    b = _obs(source="manual", value="Blue", confidence=0.6)
    winner, conflict = resolver.resolve([a, b])
    assert winner.value == "Blue"
    assert conflict is not None
    assert conflict.competing_observations == (a, b)
    assert conflict.resolved_observation_id == winner.observation_id


def test_conflict_resolver_returns_none_when_values_agree():
    resolver = AttributeConflictResolver()
    a = _obs(source="vision", value="Red")
    b = _obs(source="shopify", value="Red")
    _, conflict = resolver.resolve([a, b])
    assert conflict is None


def _catalog_with_pairs_with_relationship() -> TaxonomyCatalog:
    base = load_catalog("ai/taxonomy/examples/catalog.json")
    style_vocab = VocabularyModel(vocabulary_id="TAX-VOC-000099", name="Style", scope="global")
    style_term = TermModel(term_id="TAX-TERM-000099", vocabulary_id="TAX-VOC-000099", label="Bold")
    relationship = RelationshipModel(
        relationship_id="TAX-REL-000001", subject_type="term", subject_id="TAX-TERM-000001",
        relationship_type="PAIRS_WITH", object_type="term", object_id="TAX-TERM-000099",
    )
    return TaxonomyCatalog(
        categories=base.categories, attribute_groups=base.attribute_groups,
        vocabularies=base.vocabularies + [style_vocab], terms=base.terms + [style_term],
        attributes=base.attributes, relationships=[relationship],
    )


def test_inference_rule_proposes_a_reduced_confidence_observation_via_real_relationship():
    catalog = _catalog_with_pairs_with_relationship()
    rule = TaxonomyRelationshipInferenceRule(
        catalog, vocabulary_to_registry_reference={"TAX-VOC-000099": "EAR-000099"},
        observed_at="2026-08-02T00:00:00Z",
    )
    engine = AttributeInferenceEngine(rules=[rule])
    inferred = engine.infer([_obs(value="Red", confidence=0.8)])
    assert len(inferred) == 1
    assert inferred[0].registry_reference == "EAR-000099"
    assert inferred[0].value == "Bold"
    assert inferred[0].source == "inference"
    assert inferred[0].confidence == 0.4  # 0.8 * default 0.5 penalty


def test_inference_rule_produces_nothing_when_no_relationship_or_mapping_exists():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")  # no relationships in the real fixture
    rule = TaxonomyRelationshipInferenceRule(catalog, vocabulary_to_registry_reference={})
    engine = AttributeInferenceEngine(rules=[rule])
    assert engine.infer([_obs(value="Red")]) == []


def test_history_log_appends_a_transition_and_is_readable():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "attribute_history.jsonl"
        log = AttributeHistoryLog(log_path=log_path)
        previous = ResolvedAttribute(
            registry_reference="EAR-000001", subject_id="gid://shopify/Product/1",
            value="Red", confidence=0.9, source="vision", resolved_at="2026-08-01T00:00:00Z",
        )
        new = ResolvedAttribute(
            registry_reference="EAR-000001", subject_id="gid://shopify/Product/1",
            value="Blue", confidence=0.6, source="manual", resolved_at="2026-08-02T00:00:00Z",
        )
        log.record_transition(previous, new)
        content = log_path.read_text(encoding="utf-8").strip()
        assert '"previous_value": "Red"' in content
        assert '"new_value": "Blue"' in content


def test_search_service_composes_ear_and_taxonomy_lookups():
    registry = load_registry("ai/ear/examples/registry.json")
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    search = AttributeSearchService(ear_registry=registry, taxonomy_catalog=catalog)
    assert len(search.find_attributes_by_namespace("domain.bakery")) >= 2
    assert len(search.find_attributes_by_owner("vision_engine")) >= 2
    assert any(t.label == "Red" for t in search.find_terms_by_label_substring("red"))


def test_export_profile_is_json_safe_and_flags_conflicts():
    resolved = ResolvedAttribute(
        registry_reference="EAR-000001", subject_id="gid://shopify/Product/1",
        value="Blue", confidence=0.6, source="manual", resolved_at="2026-08-02T00:00:00Z",
        resolution_method="highest_trust",
    )
    profile = SubjectAttributeProfile(
        subject_id="gid://shopify/Product/1", resolved_at="2026-08-02T00:00:00Z",
        attributes={"EAR-000001": resolved},
    )
    exported = export_profile(profile)
    assert exported["attributes"]["EAR-000001"]["value"] == "Blue"
    assert exported["attributes"]["EAR-000001"]["has_conflict"] is False


def test_coverage_report_flags_missing_and_low_confidence():
    resolved = ResolvedAttribute(
        registry_reference="EAR-000001", subject_id="s1", value="Red", confidence=0.2,
        source="vision", resolved_at="2026-08-02T00:00:00Z",
    )
    profile = SubjectAttributeProfile(subject_id="s1", resolved_at="2026-08-02T00:00:00Z", attributes={"EAR-000001": resolved})
    report = compute_coverage_report(profile, expected_registry_references=["EAR-000001", "EAR-000002"])
    assert report.missing_registry_references == ("EAR-000002",)
    assert report.low_confidence_registry_references == ("EAR-000001",)
    assert report.completeness == 0.5


def test_compute_drift_detects_value_change():
    old = ResolvedAttribute(registry_reference="EAR-000001", subject_id="s1", value="Red", confidence=0.9, source="vision", resolved_at="t1")
    new = ResolvedAttribute(registry_reference="EAR-000001", subject_id="s1", value="Blue", confidence=0.6, source="manual", resolved_at="t2")
    previous_profile = SubjectAttributeProfile(subject_id="s1", resolved_at="t1", attributes={"EAR-000001": old})
    current_profile = SubjectAttributeProfile(subject_id="s1", resolved_at="t2", attributes={"EAR-000001": new})
    drift = compute_drift(previous_profile, current_profile)
    assert drift == {"EAR-000001": ("Red", "Blue")}


def test_service_end_to_end_resolves_validates_and_logs_history():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    definitions = load_definitions("ai/ead/examples/definitions.json")
    with tempfile.TemporaryDirectory() as tmp:
        history_log = AttributeHistoryLog(log_path=Path(tmp) / "history.jsonl")
        service = AttributeIntelligenceService(
            taxonomy_catalog=catalog, ead_definitions=definitions, history_log=history_log,
        )
        vision_obs = _obs(source="vision", value="Red", confidence=0.9)
        manual_obs = _obs(source="manual", value="Blue", confidence=0.6)

        profile = service.resolve("gid://shopify/Product/1", [vision_obs, manual_obs], resolved_at="2026-08-02T00:00:00Z")
        resolved = profile.attributes["EAR-000001"]
        assert resolved.value == "Blue"  # manual outranks vision
        assert len(profile.conflicts) == 1

        # a second resolve with the SAME winning value must not log a new transition
        profile2 = service.resolve("gid://shopify/Product/1", [manual_obs], resolved_at="2026-08-02T00:05:00Z")
        assert profile2.attributes["EAR-000001"].value == "Blue"
        lines = (Path(tmp) / "history.jsonl").read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1  # only the first resolve produced a real transition


if __name__ == "__main__":
    test_observation_id_is_deterministic()
    test_normalizer_matches_real_taxonomy_term_and_synonym()
    test_validator_flags_missing_confidence_and_unknown_definition()
    test_validator_enforces_allowed_values_and_minimum_confidence()
    test_confidence_engine_ranks_manual_over_vision_regardless_of_raw_confidence()
    test_confidence_engine_single_source_when_all_agree()
    test_conflict_resolver_produces_a_conflict_record_and_keeps_every_observation()
    test_conflict_resolver_returns_none_when_values_agree()
    test_inference_rule_proposes_a_reduced_confidence_observation_via_real_relationship()
    test_inference_rule_produces_nothing_when_no_relationship_or_mapping_exists()
    test_history_log_appends_a_transition_and_is_readable()
    test_search_service_composes_ear_and_taxonomy_lookups()
    test_export_profile_is_json_safe_and_flags_conflicts()
    test_coverage_report_flags_missing_and_low_confidence()
    test_compute_drift_detects_value_change()
    test_service_end_to_end_resolves_validates_and_logs_history()
    print("OK")
