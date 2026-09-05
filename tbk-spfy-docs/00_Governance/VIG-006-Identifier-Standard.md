# VIG-006: Identifier Standard

Status: Active
Version: 1.0

## Purpose

Defines how every first-class entity in the platform receives, keeps, and is referenced by a
permanent identifier, so that every present and future module can join data about the same entity
without ambiguity or drift.

## Scope

Applies to every entity type the platform tracks: images today; products, observations, embeddings,
and any future entity type as the platform grows.

## Definitions

- **Entity**: see VIG-000. Anything the platform assigns a permanent identity to.
- **`TBK_*_ID`**: the platform's identifier family. `TBK_IMAGE_ID` is the first instance; future
  entity types receive their own (`TBK_PRODUCT_ID`, `TBK_OBSERVATION_ID`, etc.) following the same
  rules.
- **Deterministic Identifier**: an identifier derived from an entity's content, such that
  reprocessing the same content always yields the same identifier, with no external registry
  required to guarantee that.

## Principles

1. Every entity receives a permanent identifier at admission. No entity is referenced, stored, or
   reasoned about by any other means (file path, database row number, array index) as its primary
   key.
2. Identifiers are never reused and never reassigned to a different entity, even after the original
   entity is retired.
3. Where an entity's identity can be derived deterministically from its content (e.g. an image's
   bytes), the identifier is content-derived rather than randomly generated or counter-assigned —
   this guarantees idempotency without requiring a central registry.
4. Where content-derivation is not meaningful (e.g. an entity with no stable content, like a live
   session), a randomly generated identifier is acceptable, but must still satisfy Principles 1 and
   2.
5. Identifiers are opaque outside their generation logic — no module may parse meaning out of an
   identifier's structure beyond confirming its format.

## Rules

- Every new entity type introduced to the platform must define its `TBK_*_ID` scheme before its
  first record is created, following this standard.
- An identifier's generation method (content hash vs. random) must be documented alongside the
  entity type it identifies.
- No two distinct entities may ever be assigned the same identifier; no module may mutate an
  existing identifier for any reason, including correcting a data error (the record is corrected;
  the identifier is not reassigned).

## Examples

- `TBK_IMAGE_ID` is derived as `"TBK-" + sha256(image_bytes)[:16]`. The same image file, processed
  today or a year from now, produces the same ID. Correct application of Principle 3.
- A future `TBK_PRODUCT_ID` for a Shopify product, which has no single "content" to hash, is
  generated once at product creation and stored permanently. Correct application of Principle 4.

## Non-examples

- An entity is identified by its file path or array position, which changes if the file is moved or
  the array reordered. Violates Principle 1.
- Reprocessing an image assigns it a new random ID each time, breaking the ability to recognize it
  as "the same image" across runs. Violates Principle 3.
- A module infers a product's category by parsing substrings out of its `TBK_PRODUCT_ID`. Violates
  Principle 5 — the ID is a key, not an encoding.

## Implementation Guidance

When introducing a new entity type, ask first whether it has stable, hashable content. If yes, a
content-hash identifier (Principle 3) is the default choice — it requires no coordination or shared
state across modules to stay collision-free and idempotent. Only fall back to random generation
(Principle 4) when no such content exists.

## Future Compatibility

This standard does not fix a specific hash algorithm or ID string format for all future entity
types — `TBK_IMAGE_ID`'s SHA-256-based format is one concrete instance. Future entity types choose
an appropriate deterministic derivation for their own content, consistent with these principles.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. |

## Related Standards

VIG-000 (Constitution — Principle 2), VIG-003 (Data Principles — lineage references identifiers),
VIG-005 (Versioning Standard — the paired standard for artifact rather than entity identity).

## References

- `ai/vision/python/pipeline.py`'s `compute_image_id()` — the first concrete implementation of this
  standard, predating its formalization here.
- `docs/AI/ARCHITECTURE_REVIEW_AR001.md` §6, §13.2 — the review finding that motivated introducing
  `TBK_IMAGE_ID` before platform volume made retrofitting one significantly harder.
