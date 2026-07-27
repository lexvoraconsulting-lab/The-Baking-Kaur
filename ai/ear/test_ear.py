#!/usr/bin/env python3
"""
Self-check for the Enterprise Attribute Registry (EAR) v1.

WHY
  Regenerates ai/ear/schemas/ear.schema.json from the Pydantic model, then
  validates both example registries, checks whole-registry invariants
  (duplicate IDs, duplicate names, deprecated/status consistency), ID
  determinism/format, and import/export round-tripping. No network calls.

USAGE
  python -m ai.ear.test_ear
"""
import json
from pathlib import Path

from pydantic import ValidationError

from ai.ear.exporter import export_registry, regenerate_schema
from ai.ear.ids import compute_registry_uuid, is_valid_attribute_id
from ai.ear.loader import load_registry
from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.ear.registry import Registry

EAR_DIR = Path(__file__).parent
EXAMPLES_DIR = EAR_DIR / "examples"


def _example_entries_raw() -> list[dict]:
    return json.loads((EXAMPLES_DIR / "registry.json").read_text())["attributes"]


def test_registry_json_example():
    registry = load_registry(EXAMPLES_DIR / "registry.json")
    assert len(registry) == 5


def test_registry_yaml_example():
    registry = load_registry(EXAMPLES_DIR / "registry.yaml")
    assert len(registry) == 5


def test_json_and_yaml_examples_are_equal():
    json_registry = load_registry(EXAMPLES_DIR / "registry.json")
    yaml_registry = load_registry(EXAMPLES_DIR / "registry.yaml")
    assert json_registry.all_attribute_ids() == yaml_registry.all_attribute_ids()
    for aid in json_registry.all_attribute_ids():
        assert json_registry.get(attribute_id=aid) == yaml_registry.get(attribute_id=aid)


def test_example_registry_uuids_match_computed():
    for raw in _example_entries_raw():
        expected = compute_registry_uuid(raw["eal_reference"])
        assert raw["registry_uuid"] == expected, (
            f"{raw['eal_reference']!r} has registry_uuid {raw['registry_uuid']!r}, "
            f"expected {expected!r} - example is stale"
        )


def test_example_attribute_ids_are_valid_format():
    for raw in _example_entries_raw():
        assert is_valid_attribute_id(raw["attribute_id"])


def test_duplicate_attribute_id_rejected():
    entries = [EARAttributeEntryModel(**raw) for raw in _example_entries_raw()]
    raw_dup = dict(_example_entries_raw()[1])
    raw_dup["attribute_id"] = entries[0].attribute_id  # collide on ID only
    dup = EARAttributeEntryModel(**raw_dup)
    try:
        Registry([entries[0], dup])
        assert False, "expected ValueError for duplicate attribute_id"
    except ValueError as e:
        assert "duplicate attribute_id" in str(e)


def test_duplicate_namespace_name_rejected():
    entries = [EARAttributeEntryModel(**raw) for raw in _example_entries_raw()]
    raw_dup = _example_entries_raw()[1]
    raw_dup = {**raw_dup, "attribute_id": "EAR-000099", "canonical_name": entries[0].canonical_name,
               "namespace": entries[0].namespace}
    dup = EARAttributeEntryModel(**raw_dup)
    try:
        Registry([entries[0], dup])
        assert False, "expected ValueError for duplicate (namespace, canonical_name)"
    except ValueError as e:
        assert "duplicate (namespace, canonical_name)" in str(e)


def test_invalid_datatype_rejected():
    raw = dict(_example_entries_raw()[0])
    raw["datatype"] = "not_a_real_datatype"
    try:
        EARAttributeEntryModel(**raw)
        assert False, "expected ValidationError for invalid datatype"
    except ValidationError:
        pass


def test_missing_required_field_rejected():
    raw = dict(_example_entries_raw()[0])
    del raw["eal_reference"]
    try:
        EARAttributeEntryModel(**raw)
        assert False, "expected ValidationError for missing eal_reference"
    except ValidationError:
        pass


def test_registry_uuid_is_deterministic():
    a = compute_registry_uuid("eal.domain.bakery.colour.primary")
    b = compute_registry_uuid("eal.domain.bakery.colour.primary")
    c = compute_registry_uuid("eal.domain.bakery.colour.secondary")
    assert a == b
    assert a != c


def test_deprecated_status_requires_deprecated_in():
    raw = dict(_example_entries_raw()[0])  # status=active, deprecated_in=None
    raw["status"] = "deprecated"
    try:
        EARAttributeEntryModel(**raw)
        assert False, "expected ValueError: deprecated status with no deprecated_in"
    except ValidationError:
        pass

    raw2 = dict(_example_entries_raw()[3])  # status=deprecated, deprecated_in="v1"
    raw2["status"] = "active"
    try:
        EARAttributeEntryModel(**raw2)
        assert False, "expected ValueError: active status with deprecated_in set"
    except ValidationError:
        pass


def test_namespace_must_match_eal_reference():
    raw = dict(_example_entries_raw()[0])
    raw["namespace"] = "domain.flowers"
    try:
        EARAttributeEntryModel(**raw)
        assert False, "expected ValueError for namespace/eal_reference mismatch"
    except ValidationError:
        pass


def test_export_then_reload_round_trips(tmp_path_json="_tmp_export.json", tmp_path_yaml="_tmp_export.yaml"):
    registry = load_registry(EXAMPLES_DIR / "registry.json")
    json_path = EAR_DIR / tmp_path_json
    yaml_path = EAR_DIR / tmp_path_yaml
    try:
        export_registry(registry, json_path)
        export_registry(registry, yaml_path)
        reloaded_json = load_registry(json_path)
        reloaded_yaml = load_registry(yaml_path)
        assert reloaded_json.all_attribute_ids() == registry.all_attribute_ids()
        assert reloaded_yaml.all_attribute_ids() == registry.all_attribute_ids()
        for aid in registry.all_attribute_ids():
            assert reloaded_json.get(attribute_id=aid) == registry.get(attribute_id=aid)
            assert reloaded_yaml.get(attribute_id=aid) == registry.get(attribute_id=aid)
    finally:
        json_path.unlink(missing_ok=True)
        yaml_path.unlink(missing_ok=True)


if __name__ == "__main__":
    regenerate_schema()
    test_registry_json_example()
    test_registry_yaml_example()
    test_json_and_yaml_examples_are_equal()
    test_example_registry_uuids_match_computed()
    test_example_attribute_ids_are_valid_format()
    test_duplicate_attribute_id_rejected()
    test_duplicate_namespace_name_rejected()
    test_invalid_datatype_rejected()
    test_missing_required_field_rejected()
    test_registry_uuid_is_deterministic()
    test_deprecated_status_requires_deprecated_in()
    test_namespace_must_match_eal_reference()
    test_export_then_reload_round_trips()
    print("OK")
