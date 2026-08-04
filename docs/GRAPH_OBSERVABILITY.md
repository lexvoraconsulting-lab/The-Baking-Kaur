# Product Knowledge Graph — Observability (Build-302)

`ai.knowledge.observability` — two parts, deliberately separate:

## Per-call hooks: `KnowledgeGraphObserver`

Mirrors `ai.pricing.observability.PricingObserver` / `ai.product_intelligence.observability.ProductIntelligenceObserver`
exactly: an `ABC` with no-op-by-default hooks, `NullObserver` as the default (opting in is
additive), `LoggingObserver` as the stdlib-`logging`-based reference implementation.

| Hook | Fires when |
|---|---|
| `on_resolver_completed(resolver_name, node_count, edge_count)` | A resolver call inside `KnowledgeGraphService` succeeds |
| `on_resolver_failed(resolver_name, error)` | A resolver call raises — the exception is caught, never propagated (see [GRAPH_VALIDATION.md](GRAPH_VALIDATION.md)) |
| `on_health_report(report)` | `KnowledgeGraphService.health_report()` is called |

## Graph-level signal: `compute_health_report(graph, generated_at, resolver_failures=None)`

A pure function of a `KnowledgeGraph` snapshot — not an event, a report. Tracks exactly the signals
Build-302 Phase 8 asked for:

| Phase 8 signal | Field / mechanism |
|---|---|
| Missing Nodes | `dangling_edge_subject` / `dangling_edge_object` issues |
| Duplicate Nodes | `possible_duplicate_node` issues |
| Broken Relationships | same dangling-edge issues (an edge referencing a node that doesn't exist) |
| Resolver Failures | `resolver_failed` issues, sourced from `KnowledgeGraphService`'s own caught exceptions |
| Graph Coverage | `node_count_by_type` / `edge_count_by_predicate` — which node/edge types have zero entries is directly readable from these dicts |
| Relationship Density | `edge_count / node_count` (0.0 on an empty graph, never a division error) |
| Performance | not measured this sprint — no query volume exists yet to profile; flagged in [GRAPH_ROADMAP.md](GRAPH_ROADMAP.md) |
| Query Metrics | not measured this sprint, same reason |
| Validation Failures | surfaced via `GraphIssue.severity == "error"` → `GraphHealthReport.is_healthy` |

## Usage

```python
service = KnowledgeGraphService(taxonomy_catalog=catalog, observer=LoggingObserver())
service.load_taxonomy()
service.load_product(aggregate, read_model, validation)
report = service.health_report(generated_at="2026-08-02T00:00:00Z")
if not report.is_healthy:
    ...  # report.issues has every error/warning, with node_id/edge_id pointers where relevant
```
