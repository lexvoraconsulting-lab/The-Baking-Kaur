# ADR 0010: Attribute Intelligence Engine — multi-source reconciliation, not a new catalog

Date: 2026-08-02

## Status

Accepted

## Context

Build-303 asked for an "Enterprise Attribute Intelligence Engine" responsible for discovering,
normalizing, validating, enriching, resolving, scoring, versioning, and serving every product
attribute — explicitly *not* another taxonomy, metadata engine, or Shopify attribute model.

Repository discovery found four packages already own adjacent, real pieces of this problem:

- `ai.eal` — raw, per-entity attribute records, already carrying `confidence` and `Provenance`.
  Frozen (Build-001).
- `ai.ear` — the attribute *catalog* (which attributes exist, their namespace/owner/status), with
  a read-only query surface (`ear/api.py`: `by_namespace`/`by_owner`/`by_tag`).
- `ai.ead` — business definitions per attribute, including `allowed_values` and
  `confidence_expectations.minimum_confidence` — the exact validation rules Phase 2's "every
  attribute must support ... Validation" already needs.
- `ai.attribute_distribution` — `conflicts.detect_conflict()`, a real, pure conflict-detection
  function, but scoped 1-vs-1 (one resolved value vs. one downstream system's current value).
- `ai.taxonomy` — `Term.label`/`Term.synonyms`, already the controlled-vocabulary mechanism
  Phase 3's "normalize Birthday Cake / Birthday Cakes / Birthday → Birthday" needs.
  `ai.product_intelligence.resolvers.TaxonomyResolver` already implements this exact matching
  inline.
- `ai.knowledge` — `InferenceChainRunner`, a real rule-based traversal mechanism, but over graph
  nodes/edges, not attribute observations.

None of Phase 2's ~30 example attributes (Primary Occasion, Luxury Score, ...) exist as real
`ai.ear` entries yet — they are illustrative of the *kind* of attribute this engine handles, not a
list of attributes to bulk-register. Registering 30 new EAR/EAD entries is a content/curation task
belonging to those packages' own governance, not an engineering task for this sprint.

## Decision

1. **New package at `ai/attribute_intelligence/`** — no pre-existing scaffold reserved this build
   number (unlike `ai/knowledge/` for Build-302).
2. **`AttributeObservation` is new, generalizing `ai.eal.EALAttributeRecord`'s shape across
   sources, without modifying it.** `ai.eal` is frozen (Build-001); a Vision-sourced observation is
   *constructed from* an `EALAttributeRecord` (`integration.observations_from_eal`), never a
   competing reimplementation.
3. **Normalization wraps `ai.taxonomy.Term.label`/`.synonyms` directly** (`normalizer.py`) — the
   same matching rule `ai.product_intelligence.resolvers.TaxonomyResolver` already implements
   inline, extracted as a standalone, reusable function.
4. **`ai.product_intelligence.resolvers.TaxonomyResolver` is deliberately NOT retrofitted** to call
   this new normalizer. `ai.attribute_intelligence.integration` reads FROM
   `ai.product_intelligence` (for its Vision/Shopify source adapters) — making
   `ai.product_intelligence` import back from `ai.attribute_intelligence` would create a real
   circular package dependency. The five duplicated matching lines are the correct, deliberate
   trade-off against that cycle, not an oversight.
5. **Validation wraps `ai.ead`'s existing `allowed_values`/`confidence_expectations` fields**
   (`validator.py`) — no new validation vocabulary is introduced.
6. **Conflict resolution generalizes, but does not import, `ai.attribute_distribution.conflicts`.**
   That module's `detect_conflict()` is 1-vs-1 (resolved value vs. downstream system); this
   package's `AttributeConflictResolver` is N-vs-N (several sources' candidate values before any
   is "the" resolved one). Different shapes, complementary purposes — wiring this package's
   resolved output into `ai.attribute_distribution` as its input is real future work (see
   `docs/ATTRIBUTE_ROADMAP.md`), not built this sprint.
7. **Source trust (`confidence.DEFAULT_SOURCE_TRUST`) is a documented, config-driven business
   policy, not a measured fact** — the same "illustrative, overridable" posture `ai.pricing`'s
   config files already established. Manual and Knowledge Graph outrank raw Vision/Shopify
   observations regardless of the AI's own self-reported confidence, because a human/reconciled
   correction is definitionally more authoritative.
8. **Inference (`inference.py`) is attribute-observation propagation, not graph traversal** —
   complementary to, not a duplicate of, `ai.knowledge.InferenceChainRunner`. Both are rule-based,
   explicitly no ML, per this sprint's Phase 4.
9. **Merchant and Genome sources are honest `NotConnected*` ports** (`extensions.py`), mirroring
   `ai.knowledge.extensions`'s established pattern — no backing system exists for either.
   **Knowledge Graph and Pricing are deliberately not adapted into `AttributeObservation`** — a
   graph edge or a cost figure isn't a competing observation of an attribute value; forcing them
   into this shape would be a type mismatch, not real integration.
10. **This sprint builds the reusable engine generically**, proven end-to-end against one real
    worked example (Occasion/Colour, using real `ai/ear`/`ai/ead`/`ai/taxonomy` example fixtures),
    rather than fabricating data for all ~30 illustrative Phase 2 attributes.

## Consequences

- Any future consumer (Knowledge Graph, Cake Genome, Recommendation Engine, Search/Merchant/
  Customer Intelligence) resolves attribute values through
  `AttributeIntelligenceService.resolve()` instead of building its own multi-source reconciliation.
- The `ai.product_intelligence` ↔ `ai.attribute_intelligence` dependency stays one-directional
  (attribute_intelligence depends on product_intelligence, never the reverse) — confirmed by
  Python's own import success (a real cycle would fail to import).
- Wiring this package's `ResolvedAttribute` output into `ai.attribute_distribution`'s write path,
  and populating real `ai.ear`/`ai.ead` entries for the Phase 2 attribute list, remain open,
  tracked in `docs/ATTRIBUTE_ROADMAP.md` — not silently claimed as done.

## Notes

Satisfies VIG-009's one-decision-one-document rule. Extends
[ADR 0008](2026-08-02-product-intelligence-engine.md) and
[ADR 0009](2026-08-02-product-knowledge-graph.md)'s reasoning (real data over fabricated, ports
over guessed implementations, composition over duplication, explicit circular-dependency avoidance)
to the Attribute Intelligence Engine.
