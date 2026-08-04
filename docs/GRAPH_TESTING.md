# Product Knowledge Graph — Testing (Build-302)

Hand-written, `assert`-based self-checks — this repo's established convention (no pytest/framework
anywhere in `ai/`). Two files, run via `python -m ai.knowledge.test_<module>`:

## `test_knowledge_graph.py` (15 tests) — core mechanics

- Identity: `node_id` is a namespaced wrapper (not a hash), `edge_id` is deterministic, empty
  `native_id` is rejected.
- **Drift guard**: `test_edge_type_is_superset_of_taxonomy_relationship_type` asserts every
  `ai.taxonomy.models.RelationshipType` value is a valid `ai.knowledge.EdgeType` value — fails
  immediately if either Literal is edited out of sync, rather than silently diverging (see
  [RELATIONSHIP_MODEL.md](RELATIONSHIP_MODEL.md)).
- `KnowledgeGraph` store: indexing, and the explicit "dangling edges are permitted, never rejected"
  contract (`graph.py`'s own design decision, tested directly).
- `GraphQueryEngine`: `find_related` (with and without a predicate filter), `find_by_relationship`,
  `find_similar` (ranking by shared-neighbour count), `traverse` (terminates on an empty frontier).
- `InferenceChainRunner`: both an honest partial path (a missing hop) and a full resolved path,
  against a hand-built 3-node fixture graph, not live data — this is inference *mechanism* testing,
  not a claim that the Birthday-Cake example chain resolves against real data today.
- `compute_health_report`: dangling-edge detection, possible-duplicate detection, resolver-failure
  folding, and the healthy/warning-only case.
- **End-to-end**: `KnowledgeGraphService` wired to a real `ai.product_intelligence.ProductIntelligenceService`
  (itself wired to real `ai.ear`/`ai.ead`/`ai.taxonomy` example fixtures) — `load_taxonomy()` +
  `load_product()` + a `find_related(..., predicate="HAS_COLOR")` query + a health report, all
  against real joined data, not mocks.
- Extension ports fail loudly (`NotImplementedError`), not silently.

## `test_resolvers.py` (5 tests) — real resolver behavior

- `TaxonomyGraphResolver` against the real `ai/taxonomy/examples/catalog.json` fixture — asserts
  the real parent/child category produces a real `PART_OF` edge.
- `PricingGraphResolver` — a calculated cost projects correctly; no cost result projects nothing
  (not a fabricated Pending node).
- `SEOGraphResolver` — real SEO fields from a full `ai.product_intelligence` round-trip project
  correctly.
- `ProductGraphResolver` — the full composition: a real EAL colour attribute matched against the
  real "Colour Name" vocabulary produces a real `HAS_COLOR` edge (not a hardcoded one); real tags
  (`occasion:birthday`, `theme:spiderman`, and one deliberately-untagged `no-namespace-tag` to prove
  the namespace parser skips what it doesn't recognize rather than mis-typing it) produce the
  correct `OCCASION`/`THEME` nodes and skip the untagged one.

## What is not tested (honestly, not silently)

Performance/load testing — no query volume exists yet to benchmark against (see
[GRAPH_OBSERVABILITY.md](GRAPH_OBSERVABILITY.md)). Live-Shopify integration — `CollectionResolverPort`/
`MetadataResolverPort` are exercised only via their `Fake*` doubles (inherited from
`ai.product_intelligence`), consistent with this repo's no-network-calls-in-tests convention.

## Regression

Every existing suite (`ai.eal`, `ai.ear`, `ai.ead`, `ai.taxonomy`, `ai.attribute_distribution`,
`ai.pricing`, `ai.pricing.domains`, `ai.product_intelligence`) re-ran green after this sprint —
`ai.knowledge` reads from all of them and modifies none.
