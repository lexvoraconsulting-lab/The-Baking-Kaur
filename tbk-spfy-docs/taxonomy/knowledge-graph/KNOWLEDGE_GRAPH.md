# Enterprise Product Knowledge Graph — Overview (Build-302)

`ai/knowledge/` is the semantic relationship layer connecting existing enterprise subsystems
(`ai.product_intelligence`, `ai.pricing`, `ai.taxonomy`) without duplicating their ownership. It is
**not a database** — see [ADR 0009](adr/2026-08-02-product-knowledge-graph.md) for the full scoping
decision: this is Phase 1 of [VIG-003](00_Governance/VIG-003-Data-Principles.md)'s Knowledge Graph
vision (a semantic layer, in memory, resolved live), not the persistent, lineage-tracking system of
record VIG-003 ultimately describes — that remains future work behind its own storage-technology
ADR.

It implements the logical schema `docs/10_Taxonomy/`
[Entity_Model.md](10_Taxonomy/Entity_Model.md) and
[Relationship_Model.md](10_Taxonomy/Relationship_Model.md) already designed in Sprint 2.1 and never
coded, extended with the commerce-side entities those documents explicitly declined to model
("Business Entity" internal structure). Lives at `ai/knowledge/` — the empty scaffold ECP-100
already reserved for Build-007.

## The hard requirement this design is built around

**The graph owns no business data.** Every node/edge is resolved live by a Resolver reading a real
upstream system and held in an in-memory `KnowledgeGraph`, rebuilt on demand — the same discipline
`ai.product_intelligence.ProductAggregate` already established (ADR 0008), applied at graph scale.

## Package layout

```
ai/knowledge/
  models.py           NodeType (29 values), EdgeType (33 values, superset of
                       ai.taxonomy.RelationshipType), KnowledgeNode, KnowledgeEdge,
                       GraphIssue, GraphHealthReport
  ids.py                compute_node_id() — namespaces a REAL existing ID (Shopify GID,
                       TAX-CAT-NNNNNN, ...), never hashes a new one; compute_edge_id() — uuid5
                       of (subject, predicate, object), distinct namespace UUID
  graph.py               KnowledgeGraph — in-memory node/edge store, permissive of dangling
                       edges by design (see graph.py docstring)
  resolvers.py             TaxonomyGraphResolver, PricingGraphResolver, SEOGraphResolver,
                       ProductGraphResolver — all real, wrap already-built engines
  extensions.py               MerchantResolverPort, EmbeddingResolverPort,
                       RecommendationResolverPort, AutomationResolverPort,
                       AnalyticsResolverPort — NotConnected* until a real system exists
                       (AI Genome / ERP reuse ai.product_intelligence.extensions directly)
  query.py                      GraphQueryEngine — find_by_type, find_related,
                       find_by_relationship, find_similar, traverse
  inference.py                    InferenceChain + InferenceChainRunner — rule-based
                       predicate-chain traversal, explicitly no ML
  observability.py                  KnowledgeGraphObserver (ABC) + NullObserver +
                       LoggingObserver; compute_health_report()
  service.py                         KnowledgeGraphService — the one canonical entrypoint
  test_knowledge_graph.py              self-check: python -m ai.knowledge.test_knowledge_graph
  test_resolvers.py                     self-check: python -m ai.knowledge.test_resolvers
```

## Dependency graph

```
                        ┌───────────────────────┐
                        │  KnowledgeGraphService  │   <- the ONE canonical entrypoint
                        └────────────┬────────────┘
              ┌───────────────┬──────┴───────┬────────────────┐
              ▼               ▼              ▼                ▼
   TaxonomyGraphResolver  ProductGraphResolver  GraphQueryEngine  compute_health_report
              │            (composes Pricing+SEO)     │                  │
              ▼                    │                  ▼                  ▼
    ai.taxonomy.TaxonomyCatalog    │            KnowledgeGraph      KnowledgeGraph
                                    ▼            (in-memory store)  (in-memory store)
                    ai.product_intelligence.
                    ProductAggregate / ProductReadModel
                    (already resolved - read only, never re-derived)

  extensions.py ports (Merchant/Embedding/Recommendation/Automation/Analytics):
  NOT wired into KnowledgeGraphService this sprint - no real backing system exists.
  AI Genome / ERP: reuse ai.product_intelligence.extensions.{AIGenomeSyncPort,ERPSyncPort}.

  InferenceChainRunner  <- reads KnowledgeGraph via the same edges_from() GraphQueryEngine uses
  KnowledgeGraphObserver  <- injected, defaults to NullObserver (no-op)
```

No circular dependencies: `ai.taxonomy`, `ai.pricing`, and `ai.product_intelligence` are all
dependency-graph leaves with respect to `ai.knowledge` — none of them imports anything from it
(confirmed: point 6 of ADR 0009 is exactly the fact that this dependency direction is the reverse
of VIG-003's eventual ideal, flagged there, not hidden).

## How a graph builds (real join logic)

```
KnowledgeGraphService(taxonomy_catalog)
      │
      ├─► load_taxonomy()
      │        TaxonomyGraphResolver.resolve() -> CATEGORY/ATTRIBUTE_GROUP/VOCABULARY/
      │        VOCABULARY_TERM/ATTRIBUTE nodes + PART_OF (category hierarchy) + every
      │        already-recorded ai.taxonomy Relationship, verbatim
      │
      └─► load_product(aggregate, read_model, validation)
               ProductGraphResolver.resolve(...)
                 PRODUCT node (+ is_valid/issue_count if validation given)
                 ├─► HAS_CATEGORY edges (aggregate.taxonomy.categories)
                 ├─► HAS_COLOR / HAS_STYLE / HAS_FLAVOR / ... edges (aggregate.taxonomy.terms,
                 │      predicate chosen from the matched Term's Vocabulary name)
                 ├─► HAS_COLLECTION edges (read_model.collection_handles)
                 ├─► HAS_OCCASION / HAS_THEME / HAS_FLAVOR / HAS_RECIPIENT edges (read_model.tags,
                 │      parsed by the "occasion:"/"theme:"/"flavor:"/"recipient:" namespace the
                 │      Enterprise Collection Architecture already specified)
                 ├─► PricingGraphResolver.resolve(aggregate)  -> PRICING node + HAS_PRICE edge
                 └─► SEOGraphResolver.resolve(read_model)     -> SEO node + OPTIMIZED_FOR edge

Every add_node()/add_edge() call merges into ONE in-memory KnowledgeGraph -
never persisted, rebuilt fresh on every KnowledgeGraphService() construction.
```

## Public interfaces

- `KnowledgeGraphService(taxonomy_catalog, observer=None)`
  - `.load_taxonomy()` / `.load_product(aggregate, read_model, validation=None)`
  - `.graph -> KnowledgeGraph` (property)
  - `.query_engine() -> GraphQueryEngine`
  - `.health_report(generated_at) -> GraphHealthReport`
- `GraphQueryEngine(graph)` — see [GRAPH_QUERY_ENGINE.md](GRAPH_QUERY_ENGINE.md)
- `InferenceChainRunner(graph).run(chain, start_node_id) -> InferenceResult`
- `compute_node_id(node_type, native_id)` / `compute_edge_id(subject_id, predicate, object_id)`

## Validation checklist (Build-302's own success criteria)

- **No duplicate source of truth** — every node/edge is a projection of data
  `ai.product_intelligence`/`ai.taxonomy`/`ai.pricing` already resolved; nothing is recomputed.
- **No duplicated entities** — `NodeType` reuses Entity_Model.md's vocabulary verbatim for the
  image side; commerce-side types fill a gap that document explicitly left open.
- **No duplicated relationships** — `EdgeType` reuses `ai.taxonomy.RelationshipType`'s values
  verbatim (guarded by a test), never redefines them.
- **No circular dependencies** — confirmed above.
- **Product Intelligence remains canonical** — `ProductGraphResolver` reads
  `ProductAggregate`/`ProductReadModel`, never re-derives from raw EAL/EAR/EAD.
- **Graph remains semantic only** — no persistence, no storage-tech decision; see ADR 0009.
- **Future Cake Genome / Vision AI / ERP / Recommendation / AI Search readiness** — see
  [GRAPH_ROADMAP.md](GRAPH_ROADMAP.md).

## Known, honestly-flagged gap

This sprint's `KnowledgeGraphService` reads FROM `ai.product_intelligence`, the reverse of
VIG-003's end-state (Product Genome reads FROM the Knowledge Graph). See ADR 0009 point 6 — a
deliberate, documented bootstrap decision, not an oversight, with its resolution recommended as a
Sprint 303+ item once the Knowledge Graph has real persistence and lineage.
