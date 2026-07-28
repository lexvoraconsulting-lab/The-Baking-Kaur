# Enterprise Attribute Distribution v1

Build-004 of VISIONARY IMAGE GENOME™ (Workstream: **ATTR**), per
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07, implemented incrementally against its own Sprint Charter (one backlog item at a time,
approval gate between each).

## Status: in progress — see [SPRINT_CHARTER.md](SPRINT_CHARTER.md) for the live backlog status

BL-0, BL-1, and BL-2 done and committed (`02dd93d`, `ce31d79`, and this pass). BL-3 (conflict
detection) is next. The full documentation set (`EAD_SPECIFICATION.md`, `Validation.md`,
`Examples.md`, `BUILD_004_COMPLETION_REPORT.md`) is deferred to BL-7, once the resolution engine
and adapters exist to document meaningfully.

## `DistributionRecord` — field reference (current, through BL-2)

```
distribution_id             deterministic uuid5(registry_reference, target_system) - ai/attribute_distribution/ids.py
registry_reference           EAR attribute_id - format-validated via ai.ear.ids.is_valid_attribute_id
target_system                "shopify" | "erp"
value                        the value being distributed
external_id                  ExternalIdModel | None (reused from ai.eal) - required iff status in
                            ("dry_run", "success"); None when resolution failed (no mapping, or
                            blocked by verification gating)
human_verification_status      reuses ai.eal's VerificationStatus values
confidence                   float | None, range [0,1]
status                       "pending" | "dry_run" | "success" | "failed" | "conflict"
notes                        required iff status in ("failed", "conflict"), forbidden otherwise
                            (renamed from conflict_notes in BL-2, generalized to cover both)
distribution_version          "1.0"
```

## `resolve_distribution()` — BL-2, pure mapping resolution

`ai/attribute_distribution/resolver.py::resolve_distribution(eal_record, ear_entry, ead_definition,
target_system) -> DistributionRecordModel`. Pure function - no HTTP, no Shopify/ERP calls, no
database, no file writes, no AI calls, no retries.

1. Validates the three inputs actually describe the same attribute (`ear_entry.eal_reference ==
   eal_record.canonical_path`, `ead_definition.registry_reference == ear_entry.attribute_id`) -
   raises `ValueError` on mismatch (a caller bug, not a business outcome).
2. Looks up `ead_definition.shopify_mapping`/`erp_mapping` for the target system. `None` → resolves
   to `status="failed"` (no mapping defined yet, e.g. a draft attribute).
3. **Verification gate (Risk R-9)** - the one real policy decision this item makes: Shopify is
   treated as customer-facing (requires `human_verification.status` in `verified`/`corrected`);
   ERP is treated as internal/low-stakes (any status allowed). Fails cleanly to
   `status="failed"` with an explanatory `notes`, not an exception, when blocked.
4. Otherwise resolves to `status="dry_run"` with the concrete `external_id` and `value` to write.

Tested against real fixtures cross-referenced from `ai/eal/examples/`, `ai/ear/examples/
registry.json`, and `ai/ead/examples/definitions.json` - not synthetic data, per this project's
established testing convention.

## Related Standards

Reuses [EAL](../20_Attribute_Language/README.md) (`ExternalIdModel`, confidence range) and
[EAR](../40_Enterprise_Attribute_Registry/README.md) (`registry_reference` format) directly.
Scoped by
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-004) and
[docs/adr/2026-07-27-workstream-id-convention.md](../adr/2026-07-27-workstream-id-convention.md).
