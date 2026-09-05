"""
Enterprise Product Knowledge Graph (Build-302) - the canonical service.

WHY THIS IS "THE" ENTRYPOINT
  KnowledgeGraphService is the only class a caller should need: load_taxonomy()
  and load_product() run the real resolvers and merge their output into one
  in-memory KnowledgeGraph (never independently persisted - see graph.py);
  query_engine() and health_report() expose read access. Every resolver
  failure is caught, recorded, and surfaced via the observer AND the health
  report - a broken resolver degrades the graph's coverage, it never crashes
  the caller (the same Pending-not-failing discipline as every other engine
  in this repo).
"""
from ai.knowledge.graph import KnowledgeGraph
from ai.knowledge.models import GraphHealthReport
from ai.knowledge.observability import KnowledgeGraphObserver, NullObserver, compute_health_report
from ai.knowledge.query import GraphQueryEngine
from ai.knowledge.resolvers import ProductGraphResolver, TaxonomyGraphResolver
from ai.product_intelligence.models import ProductAggregate, ProductReadModel, ProductValidationResult
from ai.taxonomy.catalog import TaxonomyCatalog


class KnowledgeGraphService:
    def __init__(self, taxonomy_catalog: TaxonomyCatalog, observer: KnowledgeGraphObserver | None = None):
        self._taxonomy_resolver = TaxonomyGraphResolver(taxonomy_catalog)
        self._product_resolver = ProductGraphResolver(taxonomy_catalog)
        self._observer = observer or NullObserver()
        self._graph = KnowledgeGraph()
        self._resolver_failures: list[str] = []

    @property
    def graph(self) -> KnowledgeGraph:
        return self._graph

    def load_taxonomy(self) -> None:
        self._run_resolver("TaxonomyGraphResolver", self._taxonomy_resolver.resolve)

    def load_product(
        self, aggregate: ProductAggregate, read_model: ProductReadModel,
        validation: ProductValidationResult | None = None,
    ) -> None:
        self._run_resolver(
            "ProductGraphResolver",
            lambda: self._product_resolver.resolve(aggregate, read_model, validation),
        )

    def _run_resolver(self, name: str, fn) -> None:
        try:
            nodes, edges = fn()
        except Exception as exc:  # a resolver failure degrades coverage, never crashes the caller
            self._resolver_failures.append(f"{name}: {exc}")
            self._observer.on_resolver_failed(name, exc)
            return
        for node in nodes:
            self._graph.add_node(node)
        for edge in edges:
            self._graph.add_edge(edge)
        self._observer.on_resolver_completed(name, len(nodes), len(edges))

    def query_engine(self) -> GraphQueryEngine:
        return GraphQueryEngine(self._graph)

    def health_report(self, generated_at: str) -> GraphHealthReport:
        report = compute_health_report(self._graph, generated_at, self._resolver_failures)
        self._observer.on_health_report(report)
        return report
