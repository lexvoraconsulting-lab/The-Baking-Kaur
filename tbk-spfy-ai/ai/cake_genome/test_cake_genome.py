"""
Self-check: python -m ai.cake_genome.test_cake_genome

Pins the two silent-data-loss defects the first live run surfaced, plus the
Phase 1 safety invariants. Framework-free, matching every other ai/ module.
"""
from ai.cake_genome.builder import build_cake_genome, find_value_conflicts
from ai.cake_genome.validation import validate_genome
from ai.structure_discovery import ObservationMatcher, build_discovery_result
from ai.vision.python.extraction import parse_extraction
from ai.vision.python.taxonomy_digest import load_canonical_catalog

CATALOG = load_canonical_catalog()
MATCHER = ObservationMatcher(CATALOG)


def _pipeline(payload: str):
    extraction = parse_extraction(
        payload, image_id="TBK-000000000000000a", taxonomy_version="1.0",
        schema_version="v1", prompt_version="test", provider="test", model="test",
        extracted_at="2026-08-20T00:00:00Z",
    )
    discovery = build_discovery_result(extraction, MATCHER)
    return discovery, build_cake_genome(discovery, extraction)


def test_duplicate_attribute_values_are_not_silently_overwritten():
    """Regression: qwen2.5vl:3b reported visible_text twice with different
    values; a dict keyed on attribute name kept only the last."""
    discovery, genome = _pipeline(
        '{"observations":['
        '{"group":"Writing","attribute":"visible_text","value":"HAPPY BIRTHDAY","value_state":"present","confidence":0.98},'
        '{"group":"Writing","attribute":"visible_text","value":"We love you, Dad","value_state":"present","confidence":0.95}],'
        '"unmatched":[]}'
    )
    conflicts = find_value_conflicts(discovery)
    assert "visible_text" in conflicts, conflicts
    lock = genome.design_identity_lock
    assert "visible_text" not in lock.locked_attributes, (
        "a contradicted attribute must not enter the fingerprint")
    assert any("conflicting" in u for u in lock.unresolved), lock.unresolved
    assert any(u["attribute"] == "visible_text" for u in genome.uncertain_attributes)
    assert any("contradictory" in c for c in lock.caveats), lock.caveats


def test_matched_group_with_no_section_alias_is_not_dropped():
    """Regression: Writing resolved correctly but no SECTION_ALIASES entry
    mapped it, so it vanished from the genome entirely."""
    _, genome = _pipeline(
        '{"observations":[{"group":"Writing","attribute":"visible_text",'
        '"value":"HAPPY BIRTHDAY","value_state":"present","confidence":0.9}],"unmatched":[]}'
    )
    everywhere = [
        a["attribute"] for s in genome.sections.values() for a in s["attributes"]
    ]
    assert "visible_text" in everywhere, genome.sections


def test_lock_excludes_unresolved_features_but_records_them():
    _, genome = _pipeline(
        '{"observations":[{"group":"Colour","attribute":"primary_colour","value":"White",'
        '"value_state":"present","confidence":0.9}],'
        '"unmatched":[{"observed":"balloon arch","why_unmatched":"nothing fits",'
        '"suggested_kind":"term","suggested_label":"Balloon Arch","confidence":0.8}]}'
    )
    lock = genome.design_identity_lock
    assert lock.locked_attributes == {"primary_colour": "White"}
    assert "Balloon Arch" in lock.unresolved
    assert [d["feature"] for d in genome.distinctive_features] == ["Balloon Arch"]


def test_lock_is_deterministic_and_order_independent():
    a = '{"observations":[{"group":"Colour","attribute":"primary_colour","value":"White","value_state":"present","confidence":0.9},{"group":"Geometry","attribute":"shape","value":"Round","value_state":"present","confidence":0.9}],"unmatched":[]}'
    b = '{"observations":[{"group":"Geometry","attribute":"shape","value":"Round","value_state":"present","confidence":0.9},{"group":"Colour","attribute":"primary_colour","value":"White","value_state":"present","confidence":0.9}],"unmatched":[]}'
    assert _pipeline(a)[1].design_identity_lock.lock_id == _pipeline(b)[1].design_identity_lock.lock_id


def test_genome_is_never_self_verified():
    """EPR section 04 / VIG-007: no automated path may assert verification."""
    _, genome = _pipeline(
        '{"observations":[{"group":"Colour","attribute":"primary_colour","value":"White",'
        '"value_state":"present","confidence":1.0}],"unmatched":[]}'
    )
    assert genome.verification_status == "unverified"
    assert all(a["verification_status"] == "unverified"
               for s in genome.sections.values() for a in s["attributes"])
    assert validate_genome(genome).passed


def test_validation_flags_a_self_verified_genome():
    from dataclasses import replace
    _, genome = _pipeline(
        '{"observations":[{"group":"Colour","attribute":"primary_colour","value":"White",'
        '"value_state":"present","confidence":1.0}],"unmatched":[]}'
    )
    tampered = replace(genome, verification_status="verified")
    report = validate_genome(tampered)
    assert not report.passed
    assert any(f.code == "SAFETY_SELF_VERIFIED" for f in report.findings)


def test_parse_failure_still_produces_a_validated_report():
    _, genome = _pipeline("the model refused")
    report = validate_genome(genome)
    assert not report.passed, "an empty genome must not silently pass"
    assert any(f.code == "COMPLETENESS_NO_SECTIONS" for f in report.findings)


def demo():
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {name}")
    print("ai.cake_genome self-check passed")


if __name__ == "__main__":
    demo()
