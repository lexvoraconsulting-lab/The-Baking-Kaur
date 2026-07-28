#!/usr/bin/env python3
"""
Self-check for Enterprise Attribute Distribution v1 (Build-004), BL-1 scope.

WHY
  BL-1 introduces the DistributionRecord model only (no resolution engine,
  adapters, loader/exporter, or examples yet - those are later backlog
  items). This self-check constructs records directly rather than loading
  example files, since no real examples exist until a later item produces
  them from real EAL/EAR/EAD data.

USAGE
  python -m ai.attribute_distribution.test_attribute_distribution
"""
from pydantic import ValidationError

from ai.attribute_distribution.ids import compute_distribution_id
from ai.attribute_distribution.models_pydantic import DistributionRecordModel

_VALID = {
    "registry_reference": "EAR-000001",
    "target_system": "shopify",
    "value": "white",
    "external_id": {"system": "shopify", "id_type": "metafield", "value": "custom.primary_colour"},
    "human_verification_status": "verified",
    "distribution_id": compute_distribution_id("EAR-000001", "shopify"),
    "confidence": 0.85,
    "status": "pending",
}


def test_valid_record_constructs():
    record = DistributionRecordModel(**_VALID)
    assert record.registry_reference == "EAR-000001"
    assert record.target_system == "shopify"
    assert record.distribution_version == "1.0"


def test_distribution_id_is_deterministic():
    a = compute_distribution_id("EAR-000001", "shopify")
    b = compute_distribution_id("EAR-000001", "shopify")
    c = compute_distribution_id("EAR-000001", "erp")
    d = compute_distribution_id("EAR-000002", "shopify")
    assert a == b
    assert a != c
    assert a != d


def test_invalid_registry_reference_format_rejected():
    raw = dict(_VALID)
    raw["registry_reference"] = "NOT-A-VALID-ID"
    try:
        DistributionRecordModel(**raw)
        assert False, "expected ValidationError for invalid registry_reference format"
    except ValidationError:
        pass


def test_missing_required_field_rejected():
    raw = dict(_VALID)
    del raw["external_id"]
    try:
        DistributionRecordModel(**raw)
        assert False, "expected ValidationError for missing external_id"
    except ValidationError:
        pass


def test_confidence_out_of_range_rejected():
    raw = dict(_VALID)
    raw["confidence"] = 1.5
    try:
        DistributionRecordModel(**raw)
        assert False, "expected ValidationError for confidence out of [0,1] range"
    except ValidationError:
        pass


def test_conflict_notes_required_when_status_conflict():
    raw = dict(_VALID)
    raw["status"] = "conflict"
    try:
        DistributionRecordModel(**raw)
        assert False, "expected ValidationError: status='conflict' with no conflict_notes"
    except ValidationError:
        pass

    raw2 = dict(_VALID)
    raw2["conflict_notes"] = "downstream value diverges"
    try:
        DistributionRecordModel(**raw2)
        assert False, "expected ValidationError: conflict_notes set but status != 'conflict'"
    except ValidationError:
        pass

    raw3 = dict(_VALID)
    raw3["status"] = "conflict"
    raw3["conflict_notes"] = "downstream value diverges"
    DistributionRecordModel(**raw3)  # should not raise


def test_erp_target_system_accepted():
    raw = dict(_VALID)
    raw["target_system"] = "erp"
    raw["external_id"] = {"system": "erp", "id_type": "sku_attribute_code", "value": "COLOUR_PRIMARY"}
    raw["distribution_id"] = compute_distribution_id("EAR-000001", "erp")
    DistributionRecordModel(**raw)  # should not raise


if __name__ == "__main__":
    test_valid_record_constructs()
    test_distribution_id_is_deterministic()
    test_invalid_registry_reference_format_rejected()
    test_missing_required_field_rejected()
    test_confidence_out_of_range_rejected()
    test_conflict_notes_required_when_status_conflict()
    test_erp_target_system_accepted()
    print("OK")
