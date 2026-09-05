# Enterprise Attribute Language (EAL) v1

The canonical wire format every future module (Vision AI, Knowledge Graph, Shopify, ERP, Search,
Embeddings, JARVIS) uses to exchange attribute and relationship data. Implementation lives in
[`ai/eal/`](../../ai/eal/); these documents are the specification for it, not a substitute for it —
read the code for exact field behavior, read these docs for why it's shaped that way.

## Start here

- [EAL_SPECIFICATION.md](EAL_SPECIFICATION.md) — the umbrella spec and diagrams.
- [`ai/eal/models.py`](../../ai/eal/models.py) — the dataclasses (canonical field reference).
- [`ai/eal/models_pydantic.py`](../../ai/eal/models_pydantic.py) — the validation rules, in code.
- [`ai/eal/test_eal.py`](../../ai/eal/test_eal.py) — run `python -m ai.eal.test_eal` to validate
  every example and regenerate the JSON Schema files.

## Document index

| Document | Covers |
|---|---|
| [EAL_SPECIFICATION.md](EAL_SPECIFICATION.md) | Umbrella spec, diagrams, folder structure. |
| [Naming_Convention.md](Naming_Convention.md) | Casing, segment rules, reserved words. |
| [Attribute_Path_Syntax.md](Attribute_Path_Syntax.md) | The `eal.<namespace>.<group>.<attribute>` grammar. |
| [Namespace_Model.md](Namespace_Model.md) | `core` vs `domain.<name>` — serializes Sprint 2.1's two-tier group split. |
| [Identifier_Strategy.md](Identifier_Strategy.md) | `EAL_ATTRIBUTE_ID` / `EAL_RELATIONSHIP_ID` — content-hash, opaque. |
| [Data_Type_Standard.md](Data_Type_Standard.md) | The 11 canonical `data_type` values. |
| [Enum_Standard.md](Enum_Standard.md) | Enum values resolve to Sprint 2.1 Controlled Vocabulary terms. |
| [Units_Standard.md](Units_Standard.md) | Explicit, controlled `unit` field. |
| [Null_and_Unknown_Standard.md](Null_and_Unknown_Standard.md) | Three-state `value_state`: present / null / unknown. |
| [Confidence_Standard.md](Confidence_Standard.md) | `confidence: float 0.0-1.0`, required when AI-derived. |
| [Provenance_Standard.md](Provenance_Standard.md) | The `provenance` object. |
| [Human_Verification_Standard.md](Human_Verification_Standard.md) | The `human_verification` object. |
| [Relationship_Naming.md](Relationship_Naming.md) | Relationship `type` values as a controlled vocabulary. |
| [External_ID_Standard.md](External_ID_Standard.md) | The `external_ids` join point to Shopify/ERP/etc. |
| [Validation_Standard.md](Validation_Standard.md) | What `models_pydantic.py` actually enforces. |
| [Examples.md](Examples.md) | Walkthrough of `ai/eal/examples/*`. |
| [Migration_Guide.md](Migration_Guide.md) | Mapping today's Vision Engine output onto EAL, without changing it. |
| [Roadmap.md](Roadmap.md) | Build-002+ (EAR, EAD, Master Taxonomy, Knowledge Graph). |
| [Architecture_Review_AR004.md](Architecture_Review_AR004.md) | Independent self-review. |
| [BUILD_001_COMPLETION_REPORT.md](BUILD_001_COMPLETION_REPORT.md) | Delivery report. |

## Related Standards

Implements [VIG-006](../00_Governance/VIG-006-Identifier-Standard.md) (identifiers),
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md) (confidence/provenance/verification),
and serializes [Sprint 2.1](../10_Taxonomy/Architecture.md)'s Entity/Attribute Group/Relationship
Model into a concrete wire format. No governance rule or Sprint 2.1 structure is redefined here.
