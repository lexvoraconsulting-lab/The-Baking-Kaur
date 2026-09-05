# Product Knowledge Graph — Future API (Build-302)

No HTTP/GraphQL API is built this sprint — `ai/api/` is a confirmed-empty scaffold directory, and
no API framework exists anywhere in this repo's `ai/` layer to build one against. This document
prepares the seam, per Build-302 Phase 5's "Prepare future Graph APIs."

## The seam that already exists

`ai.product_intelligence.extensions.ProductIntelligenceAPIPort` (ADR 0008) is already the port a
future API layer implements against — `serialize(read_model: ProductReadModel) -> dict`. The
Knowledge Graph's query results (`KnowledgeNode`, `KnowledgeEdge`, `SimilarityResult`,
`InferenceResult` — all plain, frozen dataclasses) are the natural extension of that same
serialization surface once a real API framework is chosen. `ai.knowledge` does not redefine a
second API port — reusing the existing one when the time comes is the composition-over-duplication
call, consistent with reusing `AIGenomeSyncPort`/`ERPSyncPort` rather than redefining them (see
[GRAPH_RESOLVERS.md](GRAPH_RESOLVERS.md)).

## What a real implementation would need to decide (not decided here)

- **Transport**: REST, GraphQL, or both — no requirement in this repo favors one yet.
- **Query shape**: whether `GraphQueryEngine`'s methods map 1:1 to endpoints/resolvers, or whether a
  GraphQL schema wraps `NodeType`/`EdgeType` as first-class types (the latter is a more natural fit
  given the domain is already graph-shaped).
- **Auth/rate limiting**: none of this repo's `ai/` packages have ever needed it (all are
  library/CLI code today); a real API is this project's first network-facing AI surface and would
  need its own security review before shipping.

## Why not built now

Building an API against zero real consumers and a graph resolved from `ai.taxonomy`'s example
fixtures plus one live-Shopify integration point would be speculative — exactly what this project's
`ai/pricing/domains/ai_quote_generation.py` already flagged as the wrong instinct ("a real
specification... doesn't exist yet anywhere in this repo"). The port stays ready; the
implementation waits for a concrete consumer.
