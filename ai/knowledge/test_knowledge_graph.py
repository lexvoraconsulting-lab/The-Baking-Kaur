#!/usr/bin/env python3
"""
Self-check for ai.knowledge's core: ids, models, graph store, query engine,
inference chains, observability/health, and the end-to-end
KnowledgeGraphService flow - no network calls.

USAGE
  python -m ai.knowledge.test_knowledge_graph
"""
from ai.attribute_distribution.models import DistributionRecord
from ai.ead.loader import load_definitions
from ai.ear.loader import load_registry
from ai.eal.models import EALAttributeRecord, Provenance
from ai.pricing import FileConfigPricingRepository, PricingService, StandardTokenCostStrategy
from ai.product_intelligence.models import CollectionSlice, MetadataSlice, ProductEntityLink, ProductIdentity
from ai.product_intelligence.resolvers import (
    AttributeResolver, FakeCollectionResolver, FakeMetadataResolver, PricingResolver, TaxonomyResolver,
)
from ai.product_intelligence.service import ProductIntelligenceService
from ai.taxonomy.loader import load_catalog
from ai.taxonomy.models import RelationshipType as TaxonomyRelationshipTypeLiteral

from ai.knowledge.extensions import NotConnectedMerchantResolver
from ai.knowledge.graph import KnowledgeGraph
from ai.knowledge.ids import compute_edge_id, compute_node_id
from ai.knowledge.inference import InferenceChain, InferenceChainRunner
from ai.knowledge.models import EdgeType, KnowledgeEdge, KnowledgeNode
from ai.knowledge.observability import KnowledgeGraphObserver, compute_health_report
from ai.knowledge.query import GraphQueryEngine
from ai.knowledge.service import KnowledgeGraphService

_PROVENANCE = Provenance(
    provider="ollama", model="llava", schema_version="1.0",
    taxonomy_version="1.0", extracted_at="2026-08-02T00:00:00Z",
)


def test_node_id_is_a_namespaced_wrapper_not_a_hash():
    node = KnowledgeNode(node_type="PRODUCT", native_id="gid://shopify/Product/1", label="x", source_system="shopify")
    assert node.node_id == "PRODUCT:gid://shopify/Product/1"
    assert node.node_id == compute_node_id("PRODUCT", "gid://shopify/Product/1")


def test_node_rejects_empty_native_id():
    try:
        KnowledgeNode(node_type="PRODUCT", native_id="", label="x", source_system="shopify")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_edge_id_is_deterministic():
    e1 = compute_edge_id("a", "RELATED_TO", "b")
    e2 = compute_edge_id("a", "RELATED_TO", "b")
    assert e1 == e2
    e3 = compute_edge_id("a", "SIMILAR_TO", "b")
    assert e1 != e3


def test_edge_type_is_superset_of_taxonomy_relationship_type():
    """Guards against EdgeType drifting away from ai.taxonomy's own
    RelationshipType values - see models.py's module docstring."""
    taxonomy_values = set(TaxonomyRelationshipTypeLiteral.__args__)
    knowledge_values = set(EdgeType.__args__)
    assert taxonomy_values <= knowledge_values, taxonomy_values - knowledge_values


def _sample_graph() -> KnowledgeGraph:
    graph = KnowledgeGraph()
    a = KnowledgeNode(node_type="PRODUCT", native_id="p1", label="Cake A", source_system="shopify")
    b = KnowledgeNode(node_type="PRODUCT", native_id="p2", label="Cake B", source_system="shopify")
    cat = KnowledgeNode(node_type="CATEGORY", native_id="c1", label="Birthday Cakes", source_system="ai.taxonomy")
    graph.add_node(a)
    graph.add_node(b)
    graph.add_node(cat)
    graph.add_edge(KnowledgeEdge(subject_id=a.node_id, predicate="HAS_CATEGORY", object_id=cat.node_id, source_system="ai.taxonomy"))
    graph.add_edge(KnowledgeEdge(subject_id=b.node_id, predicate="HAS_CATEGORY", object_id=cat.node_id, source_system="ai.taxonomy"))
    return graph, a, b, cat


def test_graph_store_indexes_nodes_and_edges():
    graph, a, b, cat = _sample_graph()
    assert len(graph) == 3
    assert graph.get_node(a.node_id) is a
    assert {n.node_id for n in graph.nodes_by_type("PRODUCT")} == {a.node_id, b.node_id}
    assert len(graph.edges_from(a.node_id)) == 1
    assert len(graph.edges_to(cat.node_id)) == 2


def test_graph_store_permits_dangling_edges():
    graph = KnowledgeGraph()
    graph.add_edge(KnowledgeEdge(subject_id="PRODUCT:missing", predicate="RELATED_TO", object_id="PRODUCT:also-missing", source_system="test"))
    assert len(graph.edges) == 1  # never raises


def test_query_engine_find_related_and_by_relationship():
    graph, a, b, cat = _sample_graph()
    engine = GraphQueryEngine(graph)
    assert {n.node_id for n in engine.find_related(cat.node_id)} == {a.node_id, b.node_id}
    assert {n.node_id for n in engine.find_related(cat.node_id, predicate="HAS_CATEGORY")} == {a.node_id, b.node_id}
    assert engine.find_related(cat.node_id, predicate="SIMILAR_TO") == []

    edges = engine.find_by_relationship(subject_type="PRODUCT", predicate="HAS_CATEGORY", object_type="CATEGORY")
    assert len(edges) == 2


def test_query_engine_find_similar_ranks_by_shared_neighbours():
    graph, a, b, cat = _sample_graph()
    engine = GraphQueryEngine(graph)
    results = engine.find_similar(a.node_id, node_type="PRODUCT")
    assert len(results) == 1
    assert results[0].node.node_id == b.node_id
    assert results[0].shared_edge_count == 1
    assert results[0].shared_predicates == ("HAS_CATEGORY",)


def test_query_engine_traverse_is_breadth_first_and_terminates():
    graph, a, b, cat = _sample_graph()
    engine = GraphQueryEngine(graph)
    edges = engine.traverse(a.node_id, max_depth=5)
    assert len(edges) == 1  # a -> cat, then cat has no outgoing edges - terminates on empty frontier


def test_inference_chain_returns_partial_path_when_a_step_is_missing():
    graph, a, b, cat = _sample_graph()
    runner = InferenceChainRunner(graph)
    chain = InferenceChain(name="category_then_delivery", steps=("HAS_CATEGORY", "DELIVERED_BY"))
    result = runner.run(chain, a.node_id)
    assert result.path == (cat,)  # first hop resolves, second has no matching edge yet - honest partial path


def test_inference_chain_full_path_when_every_step_resolves():
    graph, a, b, cat = _sample_graph()
    delivery = KnowledgeNode(node_type="DELIVERY", native_id="meerut", label="Meerut", source_system="test")
    graph.add_node(delivery)
    graph.add_edge(KnowledgeEdge(subject_id=cat.node_id, predicate="DELIVERED_BY", object_id=delivery.node_id, source_system="test"))
    runner = InferenceChainRunner(graph)
    chain = InferenceChain(name="category_then_delivery", steps=("HAS_CATEGORY", "DELIVERED_BY"))
    result = runner.run(chain, a.node_id)
    assert result.path == (cat, delivery)


def test_health_report_flags_dangling_edges_and_possible_duplicates():
    graph = KnowledgeGraph()
    p1 = KnowledgeNode(node_type="PRODUCT", native_id="p1", label="Same Label", source_system="shopify")
    p2 = KnowledgeNode(node_type="PRODUCT", native_id="p2", label="Same Label", source_system="shopify")
    graph.add_node(p1)
    graph.add_node(p2)
    graph.add_edge(KnowledgeEdge(subject_id=p1.node_id, predicate="RELATED_TO", object_id="PRODUCT:ghost", source_system="test"))

    report = compute_health_report(graph, generated_at="2026-08-02T00:00:00Z", resolver_failures=["SEOGraphResolver: boom"])
    codes = {issue.code for issue in report.issues}
    assert "dangling_edge_object" in codes
    assert "possible_duplicate_node" in codes
    assert "resolver_failed" in codes
    assert report.is_healthy is False  # errors present
    assert report.node_count == 2 and report.edge_count == 1


def test_health_report_is_healthy_with_only_warnings():
    graph, a, b, cat = _sample_graph()
    report = compute_health_report(graph, generated_at="2026-08-02T00:00:00Z")
    assert report.is_healthy is True
    assert report.relationship_density == 2 / 3


class _SpyObserver(KnowledgeGraphObserver):
    def __init__(self):
        self.completed = []
        self.failed = []
        self.health = []

    def on_resolver_completed(self, resolver_name, node_count, edge_count):
        self.completed.append((resolver_name, node_count, edge_count))

    def on_resolver_failed(self, resolver_name, error):
        self.failed.append((resolver_name, error))

    def on_health_report(self, report):
        self.health.append(report)


def test_service_loads_taxonomy_and_product_end_to_end():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    registry = load_registry("ai/ear/examples/registry.json")
    definitions = load_definitions("ai/ead/examples/definitions.json")
    eal_record = EALAttributeRecord(
        canonical_path="eal.domain.bakery.colour.primary", namespace="domain.bakery", group="colour",
        entity_id="img-001", entity_type="image", value="Red", value_state="present",
        data_type="enum", provenance=_PROVENANCE, vocabulary="TAX-VOC-000001",
    )
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="motu-patlu-cake")
    pi_service = ProductIntelligenceService(
        attribute_resolver=AttributeResolver(registry, definitions, eal_records=[eal_record]),
        taxonomy_resolver=TaxonomyResolver(catalog),
        pricing_resolver=PricingResolver(PricingService(
            repository=FileConfigPricingRepository(), strategy=StandardTokenCostStrategy(),
        )),
        metadata_resolver=FakeMetadataResolver({
            identity.shopify_product_gid: MetadataSlice(title="Motu Patlu Cake", status="ACTIVE"),
        }),
    )
    aggregate = pi_service.resolve_product(
        identity=identity,
        entity_links=[ProductEntityLink(identity.shopify_product_gid, "img-001", "PRIMARY_IMAGE")],
        distribution_records=[],
        resolved_at="2026-08-02T00:00:00Z",
    )
    read_model = pi_service.get_read_model(aggregate)

    observer = _SpyObserver()
    service = KnowledgeGraphService(taxonomy_catalog=catalog, observer=observer)
    service.load_taxonomy()
    service.load_product(aggregate, read_model)

    assert len(observer.completed) == 2
    assert observer.failed == []

    query_engine = service.query_engine()
    product_node = service.graph.get_node(compute_node_id("PRODUCT", identity.shopify_product_gid))
    assert product_node is not None
    related_terms = query_engine.find_related(product_node.node_id, predicate="HAS_COLOR")
    assert len(related_terms) == 1 and related_terms[0].label == "Red"

    report = service.health_report(generated_at="2026-08-02T00:05:00Z")
    assert len(observer.health) == 1
    assert report.node_count > 0


def test_extension_ports_fail_loudly():
    port = NotConnectedMerchantResolver()
    try:
        port.resolve("gid://shopify/Product/1")
        assert False, "expected NotImplementedError"
    except NotImplementedError:
        pass


if __name__ == "__main__":
    test_node_id_is_a_namespaced_wrapper_not_a_hash()
    test_node_rejects_empty_native_id()
    test_edge_id_is_deterministic()
    test_edge_type_is_superset_of_taxonomy_relationship_type()
    test_graph_store_indexes_nodes_and_edges()
    test_graph_store_permits_dangling_edges()
    test_query_engine_find_related_and_by_relationship()
    test_query_engine_find_similar_ranks_by_shared_neighbours()
    test_query_engine_traverse_is_breadth_first_and_terminates()
    test_inference_chain_returns_partial_path_when_a_step_is_missing()
    test_inference_chain_full_path_when_every_step_resolves()
    test_health_report_flags_dangling_edges_and_possible_duplicates()
    test_health_report_is_healthy_with_only_warnings()
    test_service_loads_taxonomy_and_product_end_to_end()
    test_extension_ports_fail_loudly()
    print("OK")
