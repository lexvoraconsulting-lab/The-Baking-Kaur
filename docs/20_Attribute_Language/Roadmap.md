# EAL — Roadmap

## Build-001 (this work) — the envelope, validated

`EALAttributeRecord` / `EALRelationshipRecord` as dataclasses + Pydantic models, canonical-path
grammar, identifier strategy, one example per real consumer (Vision Engine, batch API, Shopify,
ERP, Knowledge Graph, Embeddings), generated JSON Schema, and this specification. No vocabulary
registry, no cross-field enforcement of the deferred checks in
[Validation_Standard.md](Validation_Standard.md), no real consumer wired up yet.

## Build-002 (not started) — EAR: Enterprise Attribute Registry

A live registry resolving `vocabulary` names (see [Enum_Standard.md](Enum_Standard.md)) and
`type` values (see [Relationship_Naming.md](Relationship_Naming.md)) to the real Sprint 2.2 Master
Taxonomy, once that taxonomy exists. This is what turns today's deferred cross-field validators
(AI-derived ⇒ confidence set; enum ⇒ vocabulary set and value in it) from "not yet enforceable" to
"enforced," per [Architecture_Review_AR004.md](Architecture_Review_AR004.md).

## Build-003 (not started) — EAD: Enterprise Attribute Distribution

The write path from a validated `EALAttributeRecord` to each `external_ids`-named system —
Shopify metafields, ERP attribute codes — including conflict handling when a downstream system's
own value diverges from EAL's (see [External_ID_Standard.md](External_ID_Standard.md)).

## Build-004 (not started) — Knowledge Graph physical implementation

Choosing and implementing the actual graph/relational/hybrid store that persists
`EALAttributeRecord`/`EALRelationshipRecord` at volume — an ADR-level decision per
[VIG-002](../00_Governance/VIG-002-Architecture-Principles.md), deliberately not fixed by this
wire-format work. Reuses [Relationship_Model.md](../10_Taxonomy/Relationship_Model.md)'s existing
logical schema rather than defining a new one.

## Depends on, not blocked by

- Sprint 2.2 Master Taxonomy authoring ([docs/10_Taxonomy/Roadmap.md](../10_Taxonomy/Roadmap.md)) —
  Build-002's registry has nothing real to resolve against until this exists, but EAL's wire format
  itself does not require it to be usable today (it validates shape, not vocabulary membership).
- Sprint 2.3+ Vision Engine structured-output parsing
  ([Migration_Guide.md](Migration_Guide.md)) — the first real producer of `EALAttributeRecord`s at
  volume.

## Explicitly deferred, tracked for awareness only

Unit-conversion service ([Units_Standard.md](Units_Standard.md)), embeddings/vector-search
infrastructure consuming `data_type: "vector"` records, Recommendation/Search/JARVIS integration —
all future consumers of this wire format, none designed or implemented here. Mirrors
[docs/10_Taxonomy/Roadmap.md](../10_Taxonomy/Roadmap.md)'s same "documented, not scaffolded"
approach.

## Related Standards

[docs/10_Taxonomy/Roadmap.md](../10_Taxonomy/Roadmap.md),
[docs/AI/Roadmap.md](../AI/Roadmap.md), [Architecture_Review_AR004.md](Architecture_Review_AR004.md)
(every deferred item's rationale), [VIG-001](../00_Governance/VIG-001-Platform-Principles.md)
Principle 4 (no speculative scaffolding).
