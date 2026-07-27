#!/usr/bin/env python3
"""
Self-check for Enterprise Attribute Definitions (EAD) v1.

WHY
  Regenerates ai/ead/schemas/ead.schema.json from the Pydantic model, then
  validates both example definition sets, checks the whole-set uniqueness
  invariant, ID determinism/format, confidence-range consistency,
  import/export round-tripping, AND a real cross-reference check against
  ai/ear/examples/registry.json (via ai.ear.loader) - concretely proving
  Build-002/Build-003 integrate without modifying either. No network calls.

USAGE
  python -m ai.ead.test_ead
"""
import json
from pathlib import Path

from pydantic import ValidationError

from ai.ead.api import cross_reference_against_registry
from ai.ead.definitions import DefinitionSet
from ai.ead.exporter import export_definitions, regenerate_schema
from ai.ead.ids import compute_definition_id
from ai.ead.loader import load_definitions
from ai.ead.models_pydantic import EADDefinitionModel
from ai.ear.loader import load_registry

EAD_DIR = Path(__file__).parent
EXAMPLES_DIR = EAD_DIR / "examples"
EAR_EXAMPLES_DIR = EAD_DIR.parent / "ear" / "examples"


def _example_definitions_raw() -> list[dict]:
    return json.loads((EXAMPLES_DIR / "definitions.json").read_text())["definitions"]


def test_definitions_json_example():
    definition_set = load_definitions(EXAMPLES_DIR / "definitions.json")
    assert len(definition_set) == 5


def test_definitions_yaml_example():
    definition_set = load_definitions(EXAMPLES_DIR / "definitions.yaml")
    assert len(definition_set) == 5


def test_json_and_yaml_examples_are_equal():
    json_set = load_definitions(EXAMPLES_DIR / "definitions.json")
    yaml_set = load_definitions(EXAMPLES_DIR / "definitions.yaml")
    assert json_set.all_registry_references() == yaml_set.all_registry_references()
    for ref in json_set.all_registry_references():
        assert json_set.get(ref) == yaml_set.get(ref)


def test_example_definition_ids_match_computed():
    for raw in _example_definitions_raw():
        expected = compute_definition_id(raw["registry_reference"])
        assert raw["definition_id"] == expected, (
            f"{raw['registry_reference']!r} has definition_id {raw['definition_id']!r}, "
            f"expected {expected!r} - example is stale"
        )


def test_cross_reference_against_real_ear_registry():
    definition_set = load_definitions(EXAMPLES_DIR / "definitions.json")
    ear_registry = load_registry(EAR_EXAMPLES_DIR / "registry.json")
    unresolved = cross_reference_against_registry(definition_set, ear_registry)
    assert unresolved == [], f"Definitions with no matching EAR entry: {unresolved}"


def test_duplicate_registry_reference_rejected():
    raws = _example_definitions_raw()
    definitions = [EADDefinitionModel(**raw) for raw in raws]
    raw_dup = dict(raws[1])
    raw_dup["registry_reference"] = definitions[0].registry_reference
    raw_dup["definition_id"] = compute_definition_id(raw_dup["registry_reference"])
    dup = EADDefinitionModel(**raw_dup)
    try:
        DefinitionSet([definitions[0], dup])
        assert False, "expected ValueError for duplicate registry_reference"
    except ValueError as e:
        assert "duplicate registry_reference" in str(e)


def test_invalid_registry_reference_format_rejected():
    raw = dict(_example_definitions_raw()[0])
    raw["registry_reference"] = "NOT-A-VALID-ID"
    try:
        EADDefinitionModel(**raw)
        assert False, "expected ValidationError for invalid registry_reference format"
    except ValidationError:
        pass


def test_missing_required_field_rejected():
    raw = dict(_example_definitions_raw()[0])
    del raw["business_definition"]
    try:
        EADDefinitionModel(**raw)
        assert False, "expected ValidationError for missing business_definition"
    except ValidationError:
        pass


def test_confidence_out_of_range_rejected():
    raw = dict(_example_definitions_raw()[0])
    raw["confidence_expectations"] = {**raw["confidence_expectations"], "minimum_confidence": 1.5}
    try:
        EADDefinitionModel(**raw)
        assert False, "expected ValidationError for confidence out of [0,1] range"
    except ValidationError:
        pass


def test_typical_confidence_below_minimum_rejected():
    raw = dict(_example_definitions_raw()[0])
    raw["confidence_expectations"] = {
        **raw["confidence_expectations"],
        "minimum_confidence": 0.8,
        "typical_confidence": 0.3,
    }
    try:
        EADDefinitionModel(**raw)
        assert False, "expected ValidationError for typical_confidence below minimum_confidence"
    except ValidationError:
        pass


def test_definition_id_is_deterministic():
    a = compute_definition_id("EAR-000001")
    b = compute_definition_id("EAR-000001")
    c = compute_definition_id("EAR-000002")
    assert a == b
    assert a != c


def test_examples_require_at_least_one_example_value():
    raw = dict(_example_definitions_raw()[0])
    raw["examples"] = []
    try:
        EADDefinitionModel(**raw)
        assert False, "expected ValidationError for empty examples list"
    except ValidationError:
        pass


def test_export_then_reload_round_trips():
    definition_set = load_definitions(EXAMPLES_DIR / "definitions.json")
    json_path = EAD_DIR / "_tmp_export.json"
    yaml_path = EAD_DIR / "_tmp_export.yaml"
    try:
        export_definitions(definition_set, json_path)
        export_definitions(definition_set, yaml_path)
        reloaded_json = load_definitions(json_path)
        reloaded_yaml = load_definitions(yaml_path)
        assert reloaded_json.all_registry_references() == definition_set.all_registry_references()
        assert reloaded_yaml.all_registry_references() == definition_set.all_registry_references()
        for ref in definition_set.all_registry_references():
            assert reloaded_json.get(ref) == definition_set.get(ref)
            assert reloaded_yaml.get(ref) == definition_set.get(ref)
    finally:
        json_path.unlink(missing_ok=True)
        yaml_path.unlink(missing_ok=True)


if __name__ == "__main__":
    regenerate_schema()
    test_definitions_json_example()
    test_definitions_yaml_example()
    test_json_and_yaml_examples_are_equal()
    test_example_definition_ids_match_computed()
    test_cross_reference_against_real_ear_registry()
    test_duplicate_registry_reference_rejected()
    test_invalid_registry_reference_format_rejected()
    test_missing_required_field_rejected()
    test_confidence_out_of_range_rejected()
    test_typical_confidence_below_minimum_rejected()
    test_definition_id_is_deterministic()
    test_examples_require_at_least_one_example_value()
    test_export_then_reload_round_trips()
    print("OK")
