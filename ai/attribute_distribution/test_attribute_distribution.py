#!/usr/bin/env python3
"""
Self-check for Enterprise Attribute Distribution v1 (Build-004), BL-1 through BL-5 scope.

WHY
  BL-1 introduced the DistributionRecord model (constructed directly here, no
  example files of its own yet). BL-2 adds resolve_distribution() and tests
  it against real EAL/EAR/EAD example fixtures already in the repo - the same
  "real cross-reference, not synthetic" convention ai/ead/test_ead.py already
  established. BL-3 adds detect_conflict(), tested with synthetic
  CurrentDownstreamValue inputs (pure unit tests - no real downstream data
  exists yet, per Risk R-2). BL-4 adds ShopifyAdapter.write_review_artifact(),
  tested against a temp file, cleaned up after - no stray files left in the
  repo, matching ai/ear/test_ear.py's round-trip temp-file pattern. BL-5 adds
  ERPAdapter.stub_submit() - fully stubbed, no I/O to test against, so its
  test only asserts the count and the absence of any side effect.

USAGE
  python -m ai.attribute_distribution.test_attribute_distribution
"""
import json
from pathlib import Path

import yaml
from pydantic import ValidationError

from ai.eal.models_pydantic import EALAttributeRecordModel
from ai.ear.loader import load_registry
from ai.ead.loader import load_definitions

from ai.attribute_distribution.conflicts import CurrentDownstreamValue, detect_conflict
from ai.attribute_distribution.ids import compute_distribution_id
from ai.attribute_distribution.models_pydantic import DistributionRecordModel
from ai.attribute_distribution.resolver import resolve_distribution
from ai.attribute_distribution.shopify_adapter import ShopifyAdapter
from ai.attribute_distribution.erp_adapter import ERPAdapter

_EAL_EXAMPLES = Path(__file__).parent.parent / "eal" / "examples"
_EAR_EXAMPLES = Path(__file__).parent.parent / "ear" / "examples"
_EAD_EXAMPLES = Path(__file__).parent.parent / "ead" / "examples"


def _load_eal_record(path: Path) -> EALAttributeRecordModel:
    text = path.read_text(encoding="utf-8")
    raw = yaml.safe_load(text) if path.suffix in (".yaml", ".yml") else json.loads(text)
    return EALAttributeRecordModel(**raw)

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
    del raw["value"]
    try:
        DistributionRecordModel(**raw)
        assert False, "expected ValidationError for missing value"
    except ValidationError:
        pass


def test_external_id_required_when_dry_run_or_success():
    raw = dict(_VALID)
    raw["status"] = "dry_run"
    raw["external_id"] = None
    try:
        DistributionRecordModel(**raw)
        assert False, "expected ValidationError: status='dry_run' requires external_id"
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


def test_notes_required_when_status_failed_or_conflict():
    raw = dict(_VALID)
    raw["status"] = "conflict"
    try:
        DistributionRecordModel(**raw)
        assert False, "expected ValidationError: status='conflict' with no notes"
    except ValidationError:
        pass

    raw2 = dict(_VALID)
    raw2["notes"] = "downstream value diverges"
    try:
        DistributionRecordModel(**raw2)
        assert False, "expected ValidationError: notes set but status doesn't require it"
    except ValidationError:
        pass

    raw3 = dict(_VALID)
    raw3["status"] = "conflict"
    raw3["notes"] = "downstream value diverges"
    DistributionRecordModel(**raw3)  # should not raise

    raw4 = dict(_VALID)
    raw4["status"] = "failed"
    raw4["notes"] = "no mapping defined for this attribute"
    DistributionRecordModel(**raw4)  # should not raise


def test_erp_target_system_accepted():
    raw = dict(_VALID)
    raw["target_system"] = "erp"
    raw["external_id"] = {"system": "erp", "id_type": "sku_attribute_code", "value": "COLOUR_PRIMARY"}
    raw["distribution_id"] = compute_distribution_id("EAR-000001", "erp")
    DistributionRecordModel(**raw)  # should not raise


def test_resolve_shopify_success_verified_real_fixtures():
    eal_record = _load_eal_record(_EAL_EXAMPLES / "shopify_mapping_example.yaml")  # verified
    ear_registry = load_registry(_EAR_EXAMPLES / "registry.json")
    ead_definitions = load_definitions(_EAD_EXAMPLES / "definitions.json")
    ear_entry = ear_registry.get(eal_reference=eal_record.canonical_path)
    ead_definition = ead_definitions.get(ear_entry.attribute_id)

    result = resolve_distribution(eal_record, ear_entry, ead_definition, "shopify")
    assert result.status == "dry_run"
    assert result.external_id.value == "custom.primary_colour"
    assert result.value == "white"


def test_resolve_shopify_blocked_unverified():
    eal_record = _load_eal_record(_EAL_EXAMPLES / "vision_output_example.json")  # unverified
    ear_registry = load_registry(_EAR_EXAMPLES / "registry.json")
    ead_definitions = load_definitions(_EAD_EXAMPLES / "definitions.json")
    ear_entry = ear_registry.get(eal_reference=eal_record.canonical_path)
    ead_definition = ead_definitions.get(ear_entry.attribute_id)

    result = resolve_distribution(eal_record, ear_entry, ead_definition, "shopify")
    assert result.status == "failed"
    assert "blocked" in result.notes
    assert result.external_id is None


def test_resolve_erp_allowed_unverified():
    eal_record = _load_eal_record(_EAL_EXAMPLES / "vision_output_example.json")  # unverified
    ear_registry = load_registry(_EAR_EXAMPLES / "registry.json")
    ead_definitions = load_definitions(_EAD_EXAMPLES / "definitions.json")
    ear_entry = ear_registry.get(eal_reference=eal_record.canonical_path)
    ead_definition = ead_definitions.get(ear_entry.attribute_id)

    result = resolve_distribution(eal_record, ear_entry, ead_definition, "erp")
    assert result.status == "dry_run"
    assert result.external_id.value == "COLOUR_PRIMARY"


def test_resolve_missing_mapping_fails():
    payload = json.loads((_EAL_EXAMPLES / "api_payload_example.json").read_text())
    decoration_raw = payload["attributes"][1]  # decoration.type - draft, no mapping
    eal_record = EALAttributeRecordModel(**decoration_raw)
    ear_registry = load_registry(_EAR_EXAMPLES / "registry.json")
    ead_definitions = load_definitions(_EAD_EXAMPLES / "definitions.json")
    ear_entry = ear_registry.get(eal_reference=eal_record.canonical_path)
    ead_definition = ead_definitions.get(ear_entry.attribute_id)

    result = resolve_distribution(eal_record, ear_entry, ead_definition, "shopify")
    assert result.status == "failed"
    assert "no shopify mapping" in result.notes


def test_resolve_join_mismatch_raises():
    eal_record = _load_eal_record(_EAL_EXAMPLES / "shopify_mapping_example.yaml")
    ear_registry = load_registry(_EAR_EXAMPLES / "registry.json")
    ead_definitions = load_definitions(_EAD_EXAMPLES / "definitions.json")
    wrong_ear_entry = ear_registry.get(attribute_id="EAR-000003")  # image_vector, not colour
    ead_definition = ead_definitions.get("EAR-000001")
    try:
        resolve_distribution(eal_record, wrong_ear_entry, ead_definition, "shopify")
        assert False, "expected ValueError for eal_reference/ear_entry mismatch"
    except ValueError:
        pass


def _dry_run_record():
    raw = dict(_VALID)
    raw["status"] = "dry_run"
    return DistributionRecordModel(**raw)


def test_detect_conflict_unknown_current_leaves_unchanged():
    record = _dry_run_record()
    result = detect_conflict(record, CurrentDownstreamValue(known=False))
    assert result.status == "dry_run"
    assert result.notes is None


def test_detect_conflict_matching_current_leaves_unchanged():
    record = _dry_run_record()
    result = detect_conflict(record, CurrentDownstreamValue(known=True, value="white"))
    assert result.status == "dry_run"
    assert result.notes is None


def test_detect_conflict_divergent_current_flags_conflict():
    record = _dry_run_record()
    result = detect_conflict(record, CurrentDownstreamValue(known=True, value="chocolate brown"))
    assert result.status == "conflict"
    assert "white" in result.notes
    assert "chocolate brown" in result.notes


def test_detect_conflict_requires_dry_run_status():
    raw = dict(_VALID)
    raw["status"] = "failed"
    raw["external_id"] = None
    raw["notes"] = "no mapping"
    record = DistributionRecordModel(**raw)
    try:
        detect_conflict(record, CurrentDownstreamValue(known=True, value="anything"))
        assert False, "expected ValueError for non-dry_run status"
    except ValueError:
        pass


def test_shopify_adapter_writes_only_eligible_records():
    shopify_dry_run = _dry_run_record()  # target_system="shopify", status="dry_run"

    erp_raw = dict(_VALID)
    erp_raw["target_system"] = "erp"
    erp_raw["status"] = "dry_run"
    erp_raw["external_id"] = {"system": "erp", "id_type": "sku_attribute_code", "value": "COLOUR_PRIMARY"}
    erp_raw["distribution_id"] = compute_distribution_id("EAR-000001", "erp")
    erp_dry_run = DistributionRecordModel(**erp_raw)  # wrong target_system - must be skipped

    failed_raw = dict(_VALID)
    failed_raw["status"] = "failed"
    failed_raw["external_id"] = None
    failed_raw["notes"] = "no mapping"
    failed_record = DistributionRecordModel(**failed_raw)  # wrong status - must be skipped

    tmp_path = Path(__file__).parent / "_tmp_shopify_review.jsonl"
    try:
        adapter = ShopifyAdapter()
        written = adapter.write_review_artifact(
            [shopify_dry_run, erp_dry_run, failed_record], tmp_path
        )
        assert written == 1, f"expected exactly 1 eligible record, wrote {written}"

        lines = tmp_path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1
        payload = json.loads(lines[0])
        assert payload["target_system"] == "shopify"
        assert payload["status"] == "dry_run"
        assert payload["value"] == "white"
    finally:
        tmp_path.unlink(missing_ok=True)


def test_erp_adapter_counts_only_eligible_records():
    erp_raw = dict(_VALID)
    erp_raw["target_system"] = "erp"
    erp_raw["status"] = "dry_run"
    erp_raw["external_id"] = {"system": "erp", "id_type": "sku_attribute_code", "value": "COLOUR_PRIMARY"}
    erp_raw["distribution_id"] = compute_distribution_id("EAR-000001", "erp")
    erp_dry_run = DistributionRecordModel(**erp_raw)

    shopify_dry_run = _dry_run_record()  # target_system="shopify" - must be skipped

    failed_raw = dict(_VALID)
    failed_raw["target_system"] = "erp"
    failed_raw["status"] = "failed"
    failed_raw["external_id"] = None
    failed_raw["notes"] = "no mapping"
    failed_record = DistributionRecordModel(**failed_raw)  # wrong status - must be skipped

    adapter = ERPAdapter()
    count = adapter.stub_submit([erp_dry_run, shopify_dry_run, failed_record])
    assert count == 1, f"expected exactly 1 eligible ERP record, got {count}"


def test_erp_adapter_performs_no_io():
    # No file created, no directory touched - stub_submit takes no path argument
    # at all, which is itself the proof it cannot perform file I/O.
    import inspect
    sig = inspect.signature(ERPAdapter.stub_submit)
    assert "path" not in sig.parameters
    assert "url" not in sig.parameters


def test_package_reexports_all_public_symbols():
    import ai.attribute_distribution as pkg

    for name in (
        "DistributionRecord",
        "DistributionRecordModel",
        "compute_distribution_id",
        "resolve_distribution",
        "CurrentDownstreamValue",
        "detect_conflict",
        "ShopifyAdapter",
        "ERPAdapter",
    ):
        assert hasattr(pkg, name), f"ai.attribute_distribution does not re-export {name!r}"


if __name__ == "__main__":
    test_valid_record_constructs()
    test_distribution_id_is_deterministic()
    test_invalid_registry_reference_format_rejected()
    test_missing_required_field_rejected()
    test_external_id_required_when_dry_run_or_success()
    test_confidence_out_of_range_rejected()
    test_notes_required_when_status_failed_or_conflict()
    test_erp_target_system_accepted()
    test_resolve_shopify_success_verified_real_fixtures()
    test_resolve_shopify_blocked_unverified()
    test_resolve_erp_allowed_unverified()
    test_resolve_missing_mapping_fails()
    test_resolve_join_mismatch_raises()
    test_detect_conflict_unknown_current_leaves_unchanged()
    test_detect_conflict_matching_current_leaves_unchanged()
    test_detect_conflict_divergent_current_flags_conflict()
    test_detect_conflict_requires_dry_run_status()
    test_shopify_adapter_writes_only_eligible_records()
    test_erp_adapter_counts_only_eligible_records()
    test_erp_adapter_performs_no_io()
    test_package_reexports_all_public_symbols()
    print("OK")
