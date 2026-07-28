# Enterprise Attribute Distribution v1

Build-004 of VISIONARY IMAGE GENOME™ (Workstream: **ATTR**), per
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07. The write path from a validated `EALAttributeRecord` to Shopify and ERP — implemented
incrementally, one backlog item at a time, approval gate between each. Implementation lives in
[`ai/attribute_distribution/`](../../ai/attribute_distribution/); these documents are the
specification for it, not a substitute — read the code for exact field behavior, read these docs
for why it's shaped that way.

## Status: complete — all 7 backlog items done, awaiting Architecture Gate AR-011

See [SPRINT_CHARTER.md](SPRINT_CHARTER.md) for the full backlog history and
[BUILD_004_COMPLETION_REPORT.md](BUILD_004_COMPLETION_REPORT.md) for the Build-level delivery
report.

## Start here

- [EAD_SPECIFICATION.md](EAD_SPECIFICATION.md) — the umbrella spec, field reference, module
  reference, folder structure.
- [`ai/attribute_distribution/test_attribute_distribution.py`](../../ai/attribute_distribution/test_attribute_distribution.py) —
  run `python -m ai.attribute_distribution.test_attribute_distribution` to validate everything
  (23 checks).

## Document index

| Document | Covers |
|---|---|
| [EAD_SPECIFICATION.md](EAD_SPECIFICATION.md) | Umbrella spec, `DistributionRecord` field reference, every module's reference, folder structure, identifier strategy. |
| [Validation.md](Validation.md) | What's enforced today vs. deliberately deferred. |
| [Examples.md](Examples.md) | Why this Build has no `examples/` directory of its own, and the real EAL/EAR/EAD fixtures it reuses. |
| [SPRINT_CHARTER.md](SPRINT_CHARTER.md) | Sprint Goal, Scope, Risks, and the full BL-0 through BL-7 backlog history with commit hashes. |
| [BUILD_004_COMPLETION_REPORT.md](BUILD_004_COMPLETION_REPORT.md) | Build-level delivery report. |

## Related Standards

Reuses [EAL](../20_Attribute_Language/README.md) (`ExternalIdModel`, `VerificationStatus`,
confidence range, `value_state`) and [EAR](../40_Enterprise_Attribute_Registry/README.md)
(`registry_reference` format) directly — neither modified. Scoped by
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-004) and [ADR 0006](../adr/2026-07-27-workstream-id-convention.md).
