# Enterprise Attribute Definitions (EAD) v1

Build-003 of VISIONARY IMAGE GENOME™, per
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07. The semantic definition layer over EAR (Build-002) attributes — business definition,
purpose, display name, examples, vision/AI guidance, allowed values, mapping guidance, search
behaviour, confidence expectations, and pointers to the Knowledge Graph, Shopify, and ERP.
Implementation lives in [`ai/ead/`](../../ai/ead/); these documents are the specification for it,
not a substitute for it — read the code for exact field behavior, read these docs for why it's
shaped that way.

Renumbered into this slot 2026-07-27 — see
[docs/adr/2026-07-27-build-003-renumbering.md](../adr/2026-07-27-build-003-renumbering.md) for why
"EAD" now means Definitions, not Enterprise Attribute Distribution (moved to Build-004).

## Start here

- [EAD_SPECIFICATION.md](EAD_SPECIFICATION.md) — the umbrella spec, field reference, folder
  structure.
- [`ai/ead/models.py`](../../ai/ead/models.py) — the dataclasses (canonical field reference).
- [`ai/ead/models_pydantic.py`](../../ai/ead/models_pydantic.py) — the validation rules, in code.
- [`ai/ead/test_ead.py`](../../ai/ead/test_ead.py) — run `python -m ai.ead.test_ead` to validate
  every example (including a real cross-reference against `ai/ear/examples/registry.json`) and
  regenerate the JSON Schema.

## Document index

| Document | Covers |
|---|---|
| [EAD_SPECIFICATION.md](EAD_SPECIFICATION.md) | Umbrella spec, field reference, identifier strategy, folder structure. |
| [Definition_Model.md](Definition_Model.md) | The `DefinitionSet` container: uniqueness invariant, EAR cross-referencing. |
| [Mapping_Guide.md](Mapping_Guide.md) | `shopify_mapping`/`erp_mapping`/`knowledge_graph_reference` — what's wired vs. deferred. |
| [Validation.md](Validation.md) | What `models_pydantic.py`/`validation.py` actually enforce vs. what's deferred. |
| [Versioning.md](Versioning.md) | `ead_version`, and why lifecycle version is read from EAR, not duplicated. |
| [Examples.md](Examples.md) | Walkthrough of `ai/ead/examples/*`. |
| [BUILD_003_COMPLETION_REPORT.md](BUILD_003_COMPLETION_REPORT.md) | Delivery report. |

## Related Standards

Reuses [EAL](../20_Attribute_Language/README.md) (`ExternalIdModel`, confidence range) and
[EAR](../40_Enterprise_Attribute_Registry/README.md) (`registry_reference` format, `Registry` for
cross-referencing) directly rather than redefining either. Implements
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) and
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md). Scoped by
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-003) and
[docs/adr/2026-07-27-build-003-renumbering.md](../adr/2026-07-27-build-003-renumbering.md).
