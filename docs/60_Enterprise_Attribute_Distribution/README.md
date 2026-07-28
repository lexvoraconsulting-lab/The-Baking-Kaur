# Enterprise Attribute Distribution v1

Build-004 of VISIONARY IMAGE GENOME™ (Workstream: **ATTR**), per
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07, implemented incrementally against its own Sprint Charter (one backlog item at a time,
approval gate between each).

## Status: in progress — see [SPRINT_CHARTER.md](SPRINT_CHARTER.md) for the live backlog status

BL-0 and BL-1 done and committed (`02dd93d`, `ce31d79`); BL-2 (mapping resolution) is in planning —
its implementation plan is under review before any code is written. The full documentation set
(`EAD_SPECIFICATION.md`, `Validation.md`, `Examples.md`, `BUILD_004_COMPLETION_REPORT.md`) is
deferred to BL-7, once the resolution engine and adapters exist to document meaningfully.

## `DistributionRecord` — field reference (current, BL-1 scope)

```
distribution_id             deterministic uuid5(registry_reference, target_system) - ai/attribute_distribution/ids.py
registry_reference           EAR attribute_id - format-validated via ai.ear.ids.is_valid_attribute_id
target_system                "shopify" | "erp"
value                        the value being distributed
external_id                  ExternalIdModel (reused from ai.eal) - the concrete system/id_type/value target
human_verification_status      reuses ai.eal's VerificationStatus values
confidence                   float | None, range [0,1]
status                       "pending" | "dry_run" | "success" | "failed" | "conflict"
conflict_notes               required iff status == "conflict", forbidden otherwise
distribution_version          "1.0"
```

## Related Standards

Reuses [EAL](../20_Attribute_Language/README.md) (`ExternalIdModel`, confidence range) and
[EAR](../40_Enterprise_Attribute_Registry/README.md) (`registry_reference` format) directly.
Scoped by
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-004) and
[docs/adr/2026-07-27-workstream-id-convention.md](../adr/2026-07-27-workstream-id-convention.md).
