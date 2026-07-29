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
from ai.taxonomy.models_pydantic import CategoryModel, TermModel

TAXONOMY_DIR = Path(__file__).parent
EXAMPLES_DIR = TAXONOMY_DIR / "examples"


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
    test_export_then_reload_round_trips()
    print("OK")
