# VIG-003: Data Principles

Status: Active
Version: 1.0

## Purpose

States how data flows and is governed across the platform: what is immutable, what is authoritative,
and what applications are permitted to read. This is the data-layer elaboration of VIG-000's
Principles 1, 6, and 10.

## Scope

Applies to every category of data the platform handles: source images, AI observations, taxonomy-
mapped attributes, the Knowledge Graph, the Product Genome, and any future data category
(embeddings, customer data, order data) built on the same foundation.

## Definitions

- **Source Data**: the original, immutable input (an image) admitted to the platform.
- **Observation**: see VIG-000. Raw, unverified, provider-produced evidence about source data.
- **Knowledge Graph**: the authoritative, persistent store of verified, structured relationships and
  attributes derived from observations. The system of record.
- **Product Genome**: the normalized, application-facing view derived from the Knowledge Graph.
  Applications read the Product Genome; they do not read the Knowledge Graph's internal
  representation directly, and never read raw observations directly.
- **Lineage**: the traceable path from a Product Genome attribute back through the Knowledge Graph
  entry that produced it, to the observation(s) and source data that produced that entry.

## Principles

1. Source data is immutable once admitted. Corrections and reprocessing produce new observations
   against the same permanent identity; they do not alter or delete the source.
2. The Knowledge Graph is the single system of record for verified product/image attributes. No
   second, competing system of record may exist for data the Knowledge Graph already governs.
3. The Product Genome is the only data surface applications read from. No application module reads
   raw AI observations directly, no matter how convenient.
4. Every unit of data in the Knowledge Graph is traceable to its lineage: which observation(s),
   which schema/taxonomy version, and which source data produced it.
5. Nothing enters the Knowledge Graph without having passed the verification gate defined in
   VIG-007. An unverified observation is data-in-flight, not a Knowledge Graph fact.

## Rules

- No module may write an application-facing attribute by any path that bypasses the Knowledge
  Graph → Product Genome pipeline.
- Deleting or overwriting source data in place is prohibited. If a source must be retired, it is
  marked retired; its data and lineage remain queryable.
- Every write to the Knowledge Graph must carry enough metadata to reconstruct its lineage without
  external context.

## Examples

- A product photo is reprocessed after a prompt improvement. The original image is untouched; a new
  observation is recorded against the same `TBK_IMAGE_ID`; the Knowledge Graph entry updates with a
  new lineage pointing at the new observation, while the old observation remains queryable. Correct.
- When a future module such as Marketing AI is built, it reads a product's attributes from the
  Product Genome, which was populated from Knowledge Graph entries that passed verification —
  not from raw AI output directly. Correct.

## Non-examples

- A batch job overwrites an existing product image file in place to "fix" a bad crop. Violates
  Principle 1.
- SEO AI calls the Vision Engine directly at page-render time and treats its output as fact, with no
  Knowledge Graph in between. Violates Principle 2 and 3.
- A Knowledge Graph entry exists with no record of which observation produced it. Violates
  Principle 4 — it cannot be traced or reprocessed with confidence.

## Implementation Guidance

Any data store implementing the Knowledge Graph must support, at minimum: an entity's permanent ID,
its verified attributes, and per-attribute lineage back to the observation and schema/taxonomy
version that produced it. A store that can only hold "the latest known value" for an attribute,
with no lineage, does not satisfy this standard.

## Future Compatibility

This document does not mandate a specific database technology (graph database, relational store, or
otherwise) for the Knowledge Graph — that choice is an ADR-level decision made when the Knowledge
Graph module is actually built. The principles here (immutability, single system of record, lineage)
must hold regardless of the storage technology chosen.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. |

## Related Standards

VIG-000 (Constitution — Principles 1, 6, 10), VIG-005 (Versioning Standard — schema/taxonomy
versions referenced in lineage), VIG-006 (Identifier Standard — permanent IDs referenced
throughout), VIG-007 (Quality Standard — the verification gate data must pass before promotion).

## References

- `docs/AI/ARCHITECTURE_REVIEW_AR001.md` §6 (Data Architecture Review) and §8 (Knowledge Graph
  Readiness) — identified the absence of a persistence/lineage layer as the correct next
  prerequisite before any Knowledge Graph work begins.
