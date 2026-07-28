# Enterprise Attribute Distribution v1

Build-004 of VISIONARY IMAGE GENOME™ (Workstream: **ATTR**), per
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07, implemented incrementally against its own Sprint Charter (one backlog item at a time,
approval gate between each).

## Status: in progress (BL-1 of 7 complete)

- **BL-0** (naming correction) — done, see [ADR 0006](../adr/2026-07-27-workstream-id-convention.md).
- **BL-1** (package skeleton — `DistributionRecord` model) — **done**. `ai/attribute_distribution/`
  now has `models.py`/`models_pydantic.py` (reusing `ai.eal.models_pydantic.ExternalIdModel` and
  `ai.ear.ids.is_valid_attribute_id` directly, not reimplementing either), `ids.py`
  (`compute_distribution_id`, deterministic uuid5), `__init__.py`, and
  `test_attribute_distribution.py` (7 checks, all passing).
- **BL-2** (mapping resolution) through **BL-6** (round-trip test) — not started.
- **BL-7** (full documentation set: `EAD_SPECIFICATION.md`, `Definition_Model.md`-equivalent,
  `Validation.md`, `Examples.md`, `BUILD_004_COMPLETION_REPORT.md`) — not started. This README will
  be expanded into that full set once the resolution engine and adapters exist to document
  meaningfully — writing a complete specification against a model-only skeleton would describe
  behavior that doesn't exist yet.

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
