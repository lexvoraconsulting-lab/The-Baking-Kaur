# Enterprise Attribute Registry (EAR) v1

Build-002 of VISIONARY IMAGE GENOME™, per
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07. The canonical registry of every enterprise attribute used anywhere on the platform —
does this attribute exist, what is its canonical identifier, which namespace/module owns it, which
datatype it uses. Implementation lives in [`ai/ear/`](../../ai/ear/); these documents are the
specification for it, not a substitute for it — read the code for exact field behavior, read these
docs for why it's shaped that way.

## Start here

- [EAR_SPECIFICATION.md](EAR_SPECIFICATION.md) — the umbrella spec, field reference, folder
  structure.
- [`ai/ear/models.py`](../../ai/ear/models.py) — the dataclasses (canonical field reference).
- [`ai/ear/models_pydantic.py`](../../ai/ear/models_pydantic.py) — the validation rules, in code.
- [`ai/ear/test_ear.py`](../../ai/ear/test_ear.py) — run `python -m ai.ear.test_ear` to validate
  every example and regenerate the JSON Schema.

## Document index

| Document | Covers |
|---|---|
| [EAR_SPECIFICATION.md](EAR_SPECIFICATION.md) | Umbrella spec, field reference, identifier strategy, folder structure. |
| [Registry_Model.md](Registry_Model.md) | The `Registry` container: uniqueness invariants, query surface. |
| [Namespace_Guide.md](Namespace_Guide.md) | `namespace` ↔ `eal_reference` cross-validation, reusing EAL's own rule. |
| [Validation.md](Validation.md) | What `models_pydantic.py`/`validation.py` actually enforce vs. what's deferred. |
| [Versioning.md](Versioning.md) | Registry-format version vs. per-attribute lifecycle version. |
| [Examples.md](Examples.md) | Walkthrough of `ai/ear/examples/*`. |
| [BUILD_002_COMPLETION_REPORT.md](BUILD_002_COMPLETION_REPORT.md) | Delivery report. |

## Related Standards

Reuses [EAL](../20_Attribute_Language/README.md) directly (canonical-path grammar, datatype list,
namespace rule) rather than redefining any of them. Implements
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) (versioning) and
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md) (identifiers). Scoped by
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-002).
