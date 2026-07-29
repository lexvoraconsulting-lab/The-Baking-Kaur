#!/usr/bin/env python3
"""
Self-check for the Enterprise Master Taxonomy (Build-005) BL-0 skeleton.

WHY
  Regenerates ai/taxonomy/schemas/*.schema.json from the Pydantic models,
  then validates the structural example catalog, checks whole-catalog
  invariants (duplicate IDs, unresolved references), ID format/allocation,
  and import/export round-tripping. No network calls. No real taxonomy
  content is validated here - that ships in BL-1+.

USAGE
  python -m ai.taxonomy.test_taxonomy
"""
import json
from pathlib import Path

from pydantic import ValidationError

from ai.taxonomy.catalog import TaxonomyCatalog
from ai.taxonomy.exporter import export_catalog, regenerate_schemas
from ai.taxonomy.ids import (
    allocate_category_id,
    allocate_term_id,
    is_valid_category_id,
    is_valid_term_id,
)
from ai.taxonomy.loader import load_catalog
from ai.taxonomy.models_pydantic import (
    CategoryModel,
    RelationshipModel,
    TaxonomyAttributeModel,
    TermModel,
)

TAXONOMY_DIR = Path(__file__).parent
EXAMPLES_DIR = TAXONOMY_DIR / "examples"
CONTENT_DIR = TAXONOMY_DIR / "content"


def _example_raw() -> dict:
    return json.loads((EXAMPLES_DIR / "catalog.json").read_text())


def test_example_catalog_loads():
    catalog = load_catalog(EXAMPLES_DIR / "catalog.json")
    assert len(catalog.categories) == 2
    assert len(catalog.attribute_groups) == 1
    assert len(catalog.vocabularies) == 1
    assert len(catalog.terms) == 2


def test_children_of_resolves_parent_child():
    catalog = load_catalog(EXAMPLES_DIR / "catalog.json")
    children = catalog.children_of("TAX-CAT-000001")
    assert len(children) == 1
    assert children[0].category_id == "TAX-CAT-000002"


def test_terms_in_vocabulary():
    catalog = load_catalog(EXAMPLES_DIR / "catalog.json")
    terms = catalog.terms_in_vocabulary("TAX-VOC-000001")
    assert len(terms) == 2


def test_deprecated_term_external_ids_reuse_eal_model():
    catalog = load_catalog(EXAMPLES_DIR / "catalog.json")
    active_term = catalog.get_term("TAX-TERM-000001")
    assert active_term.external_ids[0].system == "shopify"
    assert active_term.external_ids[0].value == "colour-red"


def test_unresolved_category_parent_id_rejected():
    raw = _example_raw()
    categories = [CategoryModel(**c) for c in raw["categories"]]
    categories[1] = CategoryModel(**{**raw["categories"][1], "parent_id": "TAX-CAT-999999"})
    try:
        TaxonomyCatalog(categories, [], [], [])
        assert False, "expected ValueError for unresolved parent_id"
    except ValueError as e:
        assert "does not resolve" in str(e)


def test_unresolved_term_vocabulary_id_rejected():
    raw = _example_raw()
    terms = [TermModel(**t) for t in raw["terms"]]
    bad = dict(raw["terms"][0])
    bad["vocabulary_id"] = "TAX-VOC-999999"
    terms[0] = TermModel(**bad)
    try:
        TaxonomyCatalog([], [], [], terms)
        assert False, "expected ValueError for unresolved vocabulary_id"
    except ValueError as e:
        assert "does not resolve" in str(e)


def test_duplicate_category_id_rejected():
    raw = _example_raw()
    categories = [CategoryModel(**c) for c in raw["categories"]]
    dup = CategoryModel(**{**raw["categories"][0], "category_id": categories[1].category_id})
    try:
        TaxonomyCatalog([categories[1], dup], [], [], [])
        assert False, "expected ValueError for duplicate category_id"
    except ValueError as e:
        assert "duplicate category_id" in str(e)


def test_active_status_with_superseded_by_rejected():
    raw = dict(_example_raw()["terms"][0])  # status=active, superseded_by=None
    raw["superseded_by"] = "TAX-TERM-000002"
    try:
        TermModel(**raw)
        assert False, "expected ValidationError: active status with superseded_by set"
    except ValidationError:
        pass


def test_deprecated_status_without_superseded_by_rejected():
    raw = dict(_example_raw()["terms"][1])  # status=deprecated, superseded_by set
    raw["superseded_by"] = None
    try:
        TermModel(**raw)
        assert False, "expected ValidationError: deprecated status with no superseded_by"
    except ValidationError:
        pass


def test_vocabulary_domain_scope_requires_domain():
    from ai.taxonomy.models_pydantic import VocabularyModel

    try:
        VocabularyModel(
            vocabulary_id="TAX-VOC-000002", name="Flower Type", scope="domain", domain=None
        )
        assert False, "expected ValidationError: scope=domain requires domain"
    except ValidationError:
        pass


def test_id_formats_valid():
    for raw in _example_raw()["categories"]:
        assert is_valid_category_id(raw["category_id"])
    for raw in _example_raw()["terms"]:
        assert is_valid_term_id(raw["term_id"])


def test_id_allocation_is_sequential_and_gapless_from_existing():
    assert allocate_category_id(["TAX-CAT-000001", "TAX-CAT-000002"]) == "TAX-CAT-000003"
    assert allocate_term_id([]) == "TAX-TERM-000001"


def test_enum_datatype_requires_vocabulary_id():
    try:
        TaxonomyAttributeModel(
            attribute_id="TAX-ATTR-000001", group_id="TAX-GRP-000001",
            name="primary_colour", data_type="enum", vocabulary_id=None,
        )
        assert False, "expected ValidationError: enum data_type with no vocabulary_id"
    except ValidationError:
        pass


def test_attribute_unresolved_group_id_rejected():
    from ai.taxonomy.catalog import TaxonomyCatalog

    attr = TaxonomyAttributeModel(
        attribute_id="TAX-ATTR-000001", group_id="TAX-GRP-999999",
        name="primary_colour", data_type="string",
    )
    try:
        TaxonomyCatalog([], [], [], [], [attr])
        assert False, "expected ValueError for unresolved group_id"
    except ValueError as e:
        assert "does not resolve" in str(e)


def test_real_bakery_content_loads_and_resolves():
    catalog = load_catalog(CONTENT_DIR / "bakery_v1.json")
    assert len(catalog.categories) == 6
    assert len(catalog.attribute_groups) == 30
    assert len(catalog.vocabularies) == 17
    assert len(catalog.terms) == 96
    assert len(catalog.attributes) == 26
    # Cakes -> Birthday Cakes -> Character Cakes, and additive-only inheritance per Inheritance.md
    birthday_children = catalog.children_of("TAX-CAT-000001")
    assert any(c.name == "Birthday Cakes" for c in birthday_children)
    primary_colour = catalog.get_attribute("TAX-ATTR-000001")
    assert primary_colour.vocabulary_id == "TAX-VOC-000001"
    colour_terms = catalog.terms_in_vocabulary("TAX-VOC-000001")
    assert any(t.label == "Red" for t in colour_terms)


def test_bl2_no_term_hardcodes_a_category_or_single_group():
    """Hierarchy.md: a Controlled Vocabulary Term never hardcodes which Category it's valid for.
    TermModel/VocabularyModel must never grow a category_id or single group_id field."""
    assert "category_id" not in TermModel.model_fields
    assert "group_id" not in TermModel.model_fields
    from ai.taxonomy.models_pydantic import VocabularyModel
    assert "category_id" not in VocabularyModel.model_fields
    assert "group_id" not in VocabularyModel.model_fields


def test_bl2_shape_vocabulary_reused_across_two_groups():
    catalog = load_catalog(CONTENT_DIR / "bakery_v1.json")
    shape_attrs = [a for a in catalog.attributes if a.vocabulary_id == "TAX-VOC-000002"]
    groups_using_shape = {a.group_id for a in shape_attrs}
    assert len(groups_using_shape) == 2, "Shape must stay reusable across multiple Attribute Groups"


def test_bl2_flagship_term_richness():
    catalog = load_catalog(CONTENT_DIR / "bakery_v1.json")
    rose_gold = next(t for t in catalog.terms if t.label == "Rose Gold")
    assert len(rose_gold.synonyms) == 3
    systems = {e.system for e in rose_gold.external_ids}
    assert systems == {"ai_vision", "search", "erp", "shopify", "seo"}


def test_bl2_delivery_vocabulary_is_product_attribute_scoped_not_logistics():
    catalog = load_catalog(CONTENT_DIR / "bakery_v1.json")
    delivery_vocab = next(v for v in catalog.vocabularies if v.name == "Delivery Attribute")
    terms = catalog.terms_in_vocabulary(delivery_vocab.vocabulary_id)
    labels = {t.label for t in terms}
    assert "Requires Refrigeration" in labels
    assert not any("₹" in label or "fee" in label.lower() for label in labels)


def test_real_content_cross_system_labels_present():
    catalog = load_catalog(CONTENT_DIR / "bakery_v1.json")
    wedding = next(t for t in catalog.terms if t.label == "Wedding")
    systems = {e.system for e in wedding.external_ids}
    assert "shopify" in systems
    assert "search" in systems


def test_relationship_self_loop_rejected():
    try:
        RelationshipModel(
            relationship_id="TAX-REL-000001", subject_type="term", subject_id="TAX-TERM-000001",
            relationship_type="RELATED_TO", object_type="term", object_id="TAX-TERM-000001",
        )
        assert False, "expected ValidationError for a self-loop relationship"
    except ValidationError:
        pass


def test_relationship_subject_id_must_match_subject_type_format():
    try:
        RelationshipModel(
            relationship_id="TAX-REL-000001", subject_type="term", subject_id="TAX-CAT-000001",
            relationship_type="RELATED_TO", object_type="term", object_id="TAX-TERM-000001",
        )
        assert False, "expected ValidationError: subject_type='term' with a category-shaped ID"
    except ValidationError:
        pass


def test_relationship_unresolved_reference_rejected():
    from ai.taxonomy.catalog import TaxonomyCatalog

    vocabularies, terms = _example_vocabularies_and_terms()
    rel = RelationshipModel(
        relationship_id="TAX-REL-000001", subject_type="term", subject_id=terms[0].term_id,
        relationship_type="RELATED_TO", object_type="term", object_id="TAX-TERM-999999",
    )
    try:
        TaxonomyCatalog([], [], vocabularies, terms, [], [rel])
        assert False, "expected ValueError for unresolved object_id"
    except ValueError as e:
        assert "does not resolve" in str(e)


def _example_vocabularies_and_terms():
    from ai.taxonomy.models_pydantic import VocabularyModel

    raw = _example_raw()
    vocabularies = [VocabularyModel(**v) for v in raw["vocabularies"]]
    terms = [TermModel(**t) for t in raw["terms"]]
    return vocabularies, terms


def test_relationship_duplicate_triple_rejected():
    from ai.taxonomy.catalog import TaxonomyCatalog

    vocabularies, terms = _example_vocabularies_and_terms()
    rel1 = RelationshipModel(
        relationship_id="TAX-REL-000001", subject_type="term", subject_id=terms[0].term_id,
        relationship_type="RELATED_TO", object_type="term", object_id=terms[1].term_id,
    )
    rel2 = RelationshipModel(
        relationship_id="TAX-REL-000002", subject_type="term", subject_id=terms[0].term_id,
        relationship_type="RELATED_TO", object_type="term", object_id=terms[1].term_id,
    )
    try:
        TaxonomyCatalog([], [], vocabularies, terms, [], [rel1, rel2])
        assert False, "expected ValueError for duplicate relationship triple"
    except ValueError as e:
        assert "duplicate relationship triple" in str(e)


def test_relationship_circular_is_a_rejected():
    from ai.taxonomy.catalog import TaxonomyCatalog

    vocabularies, terms = _example_vocabularies_and_terms()
    a, b = terms[0].term_id, terms[1].term_id
    rel1 = RelationshipModel(
        relationship_id="TAX-REL-000001", subject_type="term", subject_id=a,
        relationship_type="IS_A", object_type="term", object_id=b,
    )
    rel2 = RelationshipModel(
        relationship_id="TAX-REL-000002", subject_type="term", subject_id=b,
        relationship_type="IS_A", object_type="term", object_id=a,
    )
    try:
        TaxonomyCatalog([], [], vocabularies, terms, [], [rel1, rel2])
        assert False, "expected ValueError for circular IS_A relationship"
    except ValueError as e:
        assert "circular relationship" in str(e)


def test_relationship_associative_type_allows_both_directions():
    """PAIRS_WITH (associative, not hierarchical) must NOT trigger the cycle check."""
    from ai.taxonomy.catalog import TaxonomyCatalog

    vocabularies, terms = _example_vocabularies_and_terms()
    a, b = terms[0].term_id, terms[1].term_id
    rel1 = RelationshipModel(
        relationship_id="TAX-REL-000001", subject_type="term", subject_id=a,
        relationship_type="PAIRS_WITH", object_type="term", object_id=b,
    )
    rel2 = RelationshipModel(
        relationship_id="TAX-REL-000002", subject_type="term", subject_id=b,
        relationship_type="PAIRS_WITH", object_type="term", object_id=a,
    )
    catalog = TaxonomyCatalog([], [], vocabularies, terms, [], [rel1, rel2])
    assert len(catalog.relationships) == 2


def test_real_content_relationships_load_and_resolve():
    catalog = load_catalog(CONTENT_DIR / "bakery_v1.json")
    assert len(catalog.relationships) == 24
    dark_ganache_rels = catalog.relationships_for("term", "TAX-TERM-000091")
    assert any(r.relationship_type == "PAIRS_WITH" for r in dark_ganache_rels)
    assert any(r.relationship_type == "IS_A" for r in dark_ganache_rels)


def test_real_content_excludes_external_id_covered_relationship_types():
    """SEARCH_ALIAS/SHOPIFY_TAG/etc. must never appear as relationship_type - they belong in
    Term.external_ids only (see RelationshipType's docstring)."""
    catalog = load_catalog(CONTENT_DIR / "bakery_v1.json")
    used_types = {r.relationship_type for r in catalog.relationships}
    excluded = {
        "SEARCH_ALIAS", "SHOPIFY_TAG", "ERP_REFERENCE",
        "VISION_LABEL", "SEO_KEYWORD", "GOOGLE_MERCHANT_LABEL",
    }
    assert used_types.isdisjoint(excluded)


def test_export_then_reload_round_trips(tmp_json="_tmp_catalog.json", tmp_yaml="_tmp_catalog.yaml"):
    catalog = load_catalog(EXAMPLES_DIR / "catalog.json")
    json_path = TAXONOMY_DIR / tmp_json
    yaml_path = TAXONOMY_DIR / tmp_yaml
    try:
        export_catalog(catalog, json_path)
        export_catalog(catalog, yaml_path)
        reloaded_json = load_catalog(json_path)
        reloaded_yaml = load_catalog(yaml_path)
        assert len(reloaded_json) == len(catalog)
        assert len(reloaded_yaml) == len(catalog)
        for term_id in [t.term_id for t in catalog.terms]:
            assert reloaded_json.get_term(term_id) == catalog.get_term(term_id)
            assert reloaded_yaml.get_term(term_id) == catalog.get_term(term_id)
    finally:
        json_path.unlink(missing_ok=True)
        yaml_path.unlink(missing_ok=True)


if __name__ == "__main__":
    regenerate_schemas()
    test_example_catalog_loads()
    test_children_of_resolves_parent_child()
    test_terms_in_vocabulary()
    test_deprecated_term_external_ids_reuse_eal_model()
    test_unresolved_category_parent_id_rejected()
    test_unresolved_term_vocabulary_id_rejected()
    test_duplicate_category_id_rejected()
    test_active_status_with_superseded_by_rejected()
    test_deprecated_status_without_superseded_by_rejected()
    test_vocabulary_domain_scope_requires_domain()
    test_id_formats_valid()
    test_id_allocation_is_sequential_and_gapless_from_existing()
    test_enum_datatype_requires_vocabulary_id()
    test_attribute_unresolved_group_id_rejected()
    test_real_bakery_content_loads_and_resolves()
    test_real_content_cross_system_labels_present()
    test_bl2_no_term_hardcodes_a_category_or_single_group()
    test_bl2_shape_vocabulary_reused_across_two_groups()
    test_bl2_flagship_term_richness()
    test_bl2_delivery_vocabulary_is_product_attribute_scoped_not_logistics()
    test_relationship_self_loop_rejected()
    test_relationship_subject_id_must_match_subject_type_format()
    test_relationship_unresolved_reference_rejected()
    test_relationship_duplicate_triple_rejected()
    test_relationship_circular_is_a_rejected()
    test_relationship_associative_type_allows_both_directions()
    test_real_content_relationships_load_and_resolve()
    test_real_content_excludes_external_id_covered_relationship_types()
    test_export_then_reload_round_trips()
    print("OK")
