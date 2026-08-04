# Product Knowledge Graph — Query Engine (Build-302)

`ai.knowledge.query.GraphQueryEngine(graph)` — real, in-memory traversal over whatever
`KnowledgeGraph` a `KnowledgeGraphService` has resolved. No ranking model, no ML anywhere in this
module (see [GRAPH_ROADMAP.md](GRAPH_ROADMAP.md) for what a real recommendation engine would need).
See [KNOWLEDGE_GRAPH.md](KNOWLEDGE_GRAPH.md) for the full architecture.

## Methods, mapped to Build-302's requested query list

| Requested query | Method |
|---|---|
| Find Products by Theme / Occasion / Flavor / Color | `find_related(theme_node_id, predicate="HAS_THEME")` (swap predicate per facet) |
| Find Related Products | `find_related(product_node_id)` (no predicate filter — every one-hop neighbour) |
| Find Similar Cakes | `find_similar(product_node_id, node_type="PRODUCT")` |
| Find Products by Delivery | `find_related(delivery_node_id, predicate="DELIVERED_BY")` — returns `[]` today, no `DELIVERY` nodes exist yet |
| Find Products by Merchant Attributes | not available — `MerchantResolverPort` is unconnected |
| Find AI Genome Data | not available — no `AI_GENOME` nodes exist yet |
| Find Knowledge Relationships | `find_by_relationship(subject_type, predicate, object_type)` |
| Find Recommendation Candidates | not available — `RecommendationResolverPort` is unconnected; `find_similar` is the closest real substitute today |
| Find SEO / GEO / AEO Entities | `find_by_type("SEO")`, then `find_related(seo_node_id)` for what it's `OPTIMIZED_FOR` |
| Find Internal Linking Candidates | `find_related(category_node_id, predicate="HAS_CATEGORY")` — every product sharing a category is a real internal-linking candidate |

## `find_similar` — what it actually computes

A Jaccard-style overlap count: candidates of the same `node_type` are ranked by how many outgoing
one-hop neighbours (categories, collections, occasions, themes, ...) they share with the query
node. This is a real, cheap, honest heuristic — explicitly *not* a recommendation model. It answers
"how much taxonomy/collection overlap does this pair of products have," which is useful on its own
and is also the substrate a future ML-ranked recommendation step would sit on top of, not replace.

```python
from ai.knowledge.query import GraphQueryEngine

engine = GraphQueryEngine(service.graph)
results = engine.find_similar(product_node.node_id, node_type="PRODUCT", limit=10)
for r in results:
    print(r.node.label, r.shared_edge_count, r.shared_predicates)
```

## `traverse` — the mechanism `inference.py` runs on

Breadth-first, outgoing-edge-only, bounded by `max_depth` (terminates early once the frontier is
empty — never scans a graph with no more reachable nodes). This is the traversal primitive
`InferenceChainRunner` (see [KNOWLEDGE_GRAPH.md](KNOWLEDGE_GRAPH.md)'s inference section) walks a
declared predicate sequence over.

## What is deliberately not built here

A GraphQL/HTTP query surface — see [GRAPH_API.md](GRAPH_API.md). Ranking, personalization, or any
learned scoring — Build-302 Phase 6 explicitly forbids ML this sprint.
