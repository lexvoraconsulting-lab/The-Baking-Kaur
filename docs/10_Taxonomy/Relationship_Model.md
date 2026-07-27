# Image Taxonomy — Relationship Model

Sprint 2.1. Defines how entities relate to each other — the edges that, taken together with the
entities from [Entity_Model.md](Entity_Model.md), form the Knowledge Graph
([VIG-003](../00_Governance/VIG-003-Data-Principles.md)).

## Relationship types

| Relationship | Cardinality | Meaning |
|---|---|---|
| Image → Region | 1 → N | An Image contains zero or more localized Regions. |
| Image/Region → Object | 1 → N | An Image or Region contains zero or more detected Objects. |
| Object → Object | N → N | Two Objects relate spatially or functionally (e.g. "topper ON cake", "balloon NEAR cake"). Typed and directional. |
| Image/Region/Object → Attribute | 1 → N | Any of these carries candidate Attributes describing it. |
| Attribute → Genome Attribute | 1 → 1 | An Attribute is promoted to at most one Genome Attribute once verified. |
| Attribute/Genome Attribute → Human Review | 1 → N | Zero or more review records over an Attribute's lifetime. |
| Genome Attribute → Controlled Vocabulary Term | N → 1 | A Genome Attribute's value may normalize to one authoritative Term. |
| Image/Object → Category | N → 1 | Classification assignment (may be more than one Category for cross-cutting cases, e.g. an Object that is both "Decoration" and "Character"). |
| Image → Business Entity | N → N | The join to Shopify/ERP/CRM. Deliberately many-to-many, not many-to-one: this store's Cake Hampers bundle multiple distinct sellable items (a cake, a card, a balloon) that can share one product photo, so one Image may relate to more than one Business Entity, and a Business Entity may have many Images. |
| Attribute → Attribute Group | N → 1 | Schema-level membership (see [Attribute_Group_Architecture.md](Attribute_Group_Architecture.md)). |
| AI Observation → Attribute | 1 → N | One Observation may yield multiple candidate Attributes on parsing. |

## Typed edges, not a generic graph

Every Object-to-Object relationship carries an explicit type (`ON`, `NEAR`, `PART_OF`, `MATCHES`,
and future types as they're needed) rather than a single generic "related to" edge. An untyped edge
answers "these are connected" but not "how" — which is exactly the information Visual Search,
Recommendation, and Similarity Search (Sprint 2.1 §10) need to be useful rather than merely
descriptive.

Relationship type values are themselves a [Controlled Vocabulary](Controlled_Vocabulary.md), not an
open string — consistent with [VIG-000](../00_Governance/VIG-000-Constitution.md) Principle 5
("taxonomy is authoritative"). New relationship types are added the same way a new vocabulary Term
is added (additively, versioned per [Versioning.md](Versioning.md)), never invented ad hoc inline.

## Relationship provenance

Every Relationship, like every Genome Attribute, carries the confidence and provenance fields
required by [VIG-007](../00_Governance/VIG-007-Quality-Standard.md) — a Relationship inferred by an
AI provider is evidence until verified, exactly like an Attribute. This means "topper ON cake" is
itself a Genome-Attribute-like record, not a structurally different kind of fact.

## Knowledge Graph mapping

This Relationship Model, combined with the Entity Model, *is* the Knowledge Graph's logical schema
— [VIG-003](../00_Governance/VIG-003-Data-Principles.md) states the Knowledge Graph is the system
of record; this document is the first concrete definition of what its nodes and edges are. The
choice of graph database, relational store, or hybrid to physically implement this is a future
ADR-level decision, not fixed here (per
[VIG-002](../00_Governance/VIG-002-Architecture-Principles.md)).

## Vector Search / Embedding compatibility

Embeddings are modeled as an Attribute within the platform-level Embeddings group (see
Attribute_Group_Architecture.md), scoped to whichever entity was embedded (an Image, a Region, or
an Object) — not as a new entity type. This means a Vector Search implementation queries "give me
Objects whose Embeddings-group vector is nearest to X" using the same Relationship Model already
defined here, rather than requiring a parallel entity/relationship system for vectors.

## Related Standards

Implements [VIG-003](../00_Governance/VIG-003-Data-Principles.md) (Knowledge Graph as system of
record, lineage), [VIG-007](../00_Governance/VIG-007-Quality-Standard.md) (confidence/provenance on
every derived fact, including relationships).
