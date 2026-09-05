# Product Knowledge Graph — Validation (Build-302)

There is no separate `GraphValidationService` class — graph-level correctness is exactly what
`ai.knowledge.observability.compute_health_report` already checks (see
[GRAPH_OBSERVABILITY.md](GRAPH_OBSERVABILITY.md) for the mechanism). This document is the
validation checklist Build-302 Phase 11 asked for, with how each item is actually verified.

| Requirement | How it's verified |
|---|---|
| No duplicate source of truth | Every resolver reads an already-resolved upstream object (`ProductAggregate`, `TaxonomyCatalog`); none recomputes cost, taxonomy, or product data — enforced by code review / architecture, not a runtime check |
| No duplicated entities | `NodeType` reuses Entity_Model.md's vocabulary verbatim for the image side; commerce-side types fill a documented gap — see [ENTITY_MODEL.md](ENTITY_MODEL.md) |
| No duplicated relationships | `EdgeType` reuses `ai.taxonomy.RelationshipType` verbatim — enforced by `test_edge_type_is_superset_of_taxonomy_relationship_type`, a runtime-checked guarantee, not just a convention |
| No circular dependencies | `ai.taxonomy`, `ai.pricing`, `ai.product_intelligence` are dependency-graph leaves w.r.t. `ai.knowledge` — verified by inspection (no import cycle exists; Python would fail to import otherwise) |
| Product Intelligence remains canonical | `ProductGraphResolver` only ever accepts `ProductAggregate`/`ProductReadModel` as input, never raw EAL/EAR/EAD/Shopify data — structural, not just documented |
| Graph remains semantic only | No persistence layer, no storage-tech ADR created this sprint — see ADR 0009 |
| Future Cake Genome / Vision AI / ERP / Recommendation / AI Search readiness | See [GRAPH_ROADMAP.md](GRAPH_ROADMAP.md) |

## Graph-instance-level checks (what `compute_health_report` actually catches)

- **Dangling edges** (`dangling_edge_subject`/`dangling_edge_object`, error) — an edge whose subject
  or object node was never added to the graph. `KnowledgeGraph.add_edge` deliberately never rejects
  these at write time (see `graph.py`'s docstring) — they are only ever *reported*, which is what
  makes a coverage gap visible instead of silently absent.
- **Possible duplicate nodes** (`possible_duplicate_node`, warning) — two distinct `node_id`s
  sharing the same `(node_type, label)`. A heuristic, not a hash-collision-proof guarantee: two
  genuinely different products that happen to share a title would also trip this, which is the
  correct trade-off for a warning-level signal.
- **Resolver failures** (`resolver_failed`, error) — any exception a resolver raised, caught by
  `KnowledgeGraphService._run_resolver` and folded into the same health report rather than crashing
  the caller.

A `GraphHealthReport.is_healthy` is `True` iff no `error`-severity issue exists — `warning`s (a
possible duplicate, an empty optional slice) do not fail the graph, matching this platform's
system-wide "empty/pending is often honest, not broken" convention (see
`ai.product_intelligence.validation`'s identical error/warning split).
