# Product Knowledge Graph — Roadmap (Build-302)

What Build-302 did not build, in priority order, with what unblocks each item. None of this is
started; nothing here should be read as committed or scheduled — it is the honest list of what
"ready for future evolution" actually requires next.

## 1. Invert the Product Intelligence ↔ Knowledge Graph dependency (recommended first)

Today `ai.knowledge.KnowledgeGraphService` reads FROM `ai.product_intelligence` — the reverse of
[VIG-003](00_Governance/VIG-003-Data-Principles.md) Principle 3's end-state ("Product Genome reads
from the Knowledge Graph"). Flagged, not fixed, in
[ADR 0009](adr/2026-08-02-product-knowledge-graph.md) point 6. Requires: the Knowledge Graph to
have real persistence and lineage first (item 2) — inverting the dependency before that would mean
`ai.product_intelligence` reading from a graph that itself has no durable storage, which solves
nothing.

## 2. Persistence and lineage (the actual VIG-003 Knowledge Graph)

A storage-technology ADR (graph database vs. relational vs. hybrid — VIG-003 explicitly reserves
this decision), plus per-attribute lineage back to the observation that produced it, plus the
VIG-007 verification gate. This is the largest remaining gap and the one VIG-003 itself already
flagged as the correct prerequisite (`ARCHITECTURE_REVIEW_AR001.md` §8).

## 3. Live Collection/Metadata resolution

`ProductGraphResolver`'s `HAS_OCCASION`/`HAS_THEME`/`HAS_FLAVOR`/`HAS_RECIPIENT`/`HAS_COLLECTION`
edges are real code paths that resolve to nothing today because
`ai.product_intelligence.CollectionResolverPort`/`MetadataResolverPort` have no live-Shopify
implementation yet (that gap belongs to `ai.product_intelligence`, not this package — see its own
`docs/PRODUCT_INTELLIGENCE_ARCHITECTURE.md`). Once that's wired, these edges populate with zero
changes to `ai.knowledge` itself.

## 4. Variant modeling

`ai.product_intelligence.ProductReadModel` has no variant slice — `HAS_VARIANT` has no resolver.
Belongs to `ai.product_intelligence` as a new `VariantSlice`, then a thin `ai.knowledge` projection,
matching the existing Pricing/SEO pattern.

## 5. Vision structured extraction (Build-008) → Image-side resolvers

Once `ai.vision` emits structured, queryable EAL records for Image/Region/Object entities (not
started), `ai.knowledge` gets real `IMAGE`/`REGION`/`OBJECT`/`AI_OBSERVATION` resolvers for free —
the `NodeType`s and `EdgeType`s already exist (see [ENTITY_MODEL.md](ENTITY_MODEL.md)).

## 6. Real extension implementations

Each of `MerchantResolverPort`, `EmbeddingResolverPort`, `RecommendationResolverPort`,
`AutomationResolverPort`, `AnalyticsResolverPort` (extensions.py) becomes real the moment its
backing system exists — a real Merchant Center read integration, a real vector store
(`ai/embeddings`/`ai/vectordb`), a real recommendation model, a real automation runner, a real
analytics pipeline. None of these changes `ai.knowledge`'s call sites; that's what the port exists
for.

## 7. Cake Genome integration

`ai.product_intelligence.extensions.AIGenomeSyncPort` (reused by `ai.knowledge`, not redefined) is
the seam. Explicitly out of scope for this sprint and the one before it — the user's own stop
condition on both ECP-300 and Build-302.

## 8. Real API layer

See [GRAPH_API.md](GRAPH_API.md) — waits for a concrete consumer.

## 9. Performance/query-metrics observability

[GRAPH_OBSERVABILITY.md](GRAPH_OBSERVABILITY.md)'s "not measured this sprint" items — meaningful
once real query volume exists to profile against; premature to instrument now.
