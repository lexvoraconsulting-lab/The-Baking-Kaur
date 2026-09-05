#!/usr/bin/env python3
"""
Self-check for ai.knowledge's real resolvers, against real ai.taxonomy
example data and a real ai.product_intelligence-resolved ProductAggregate -
no network calls.

USAGE
  python -m ai.knowledge.test_resolvers
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

from ai.knowledge.ids import compute_node_id
from ai.knowledge.resolvers import (
    PricingGraphResolver, ProductGraphResolver, SEOGraphResolver, TaxonomyGraphResolver,
)

_PROVENANCE = Provenance(
    provider="ollama", model="llava", schema_version="1.0",
    taxonomy_version="1.0", extracted_at="2026-08-02T00:00:00Z",
)


def _build_product_intelligence_service(catalog):
    registry = load_registry("ai/ear/examples/registry.json")
    definitions = load_definitions("ai/ead/examples/definitions.json")
    eal_record = EALAttributeRecord(
        canonical_path="eal.domain.bakery.colour.primary", namespace="domain.bakery", group="colour",
        entity_id="img-001", entity_type="image", value="Red", value_state="present",
        data_type="enum", provenance=_PROVENANCE, vocabulary="TAX-VOC-000001",
    )
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="motu-patlu-cake")
    service = ProductIntelligenceService(
        attribute_resolver=AttributeResolver(registry, definitions, eal_records=[eal_record]),
        taxonomy_resolver=TaxonomyResolver(catalog),
        pricing_resolver=PricingResolver(PricingService(
            repository=FileConfigPricingRepository(), strategy=StandardTokenCostStrategy(),
        )),
        collection_resolver=FakeCollectionResolver({
            identity.shopify_product_gid: CollectionSlice(
                tags=("occasion:birthday", "theme:spiderman", "no-namespace-tag"),
                collection_handles=("birthday-cakes",),
            ),
        }),
        metadata_resolver=FakeMetadataResolver({
            identity.shopify_product_gid: MetadataSlice(
                title="Motu Patlu Cake", status="ACTIVE",
                seo_title="Motu Patlu Cake - Eggless | Meerut", seo_description="A fun birthday cake.",
            ),
        }),
    )
    aggregate = service.resolve_product(
        identity=identity,
        entity_links=[ProductEntityLink(identity.shopify_product_gid, "img-001", "PRIMARY_IMAGE")],
        distribution_records=[DistributionRecord(
            registry_reference="EAR-000001", target_system="shopify",
            value=249.0, human_verification_status="verified", status="success",
        )],
        resolved_at="2026-08-02T00:00:00Z",
    )
    validation = service.validate_product(aggregate, validated_at="2026-08-02T00:01:00Z")
    read_model = service.get_read_model(aggregate, validation)
    return aggregate, read_model, validation


def test_taxonomy_graph_resolver_produces_categories_and_part_of_edge():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    nodes, edges = TaxonomyGraphResolver(catalog).resolve()

    category_nodes = [n for n in nodes if n.node_type == "CATEGORY"]
    assert len(category_nodes) == 2
    term_nodes = [n for n in nodes if n.node_type == "VOCABULARY_TERM"]
    assert len(term_nodes) == 2

    part_of_edges = [e for e in edges if e.predicate == "PART_OF"]
    assert len(part_of_edges) == 1
    assert part_of_edges[0].subject_id == compute_node_id("CATEGORY", "TAX-CAT-000002")
    assert part_of_edges[0].object_id == compute_node_id("CATEGORY", "TAX-CAT-000001")


def test_pricing_graph_resolver_projects_calculated_cost():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    aggregate, _, _ = _build_product_intelligence_service(catalog)
    nodes, edges = PricingGraphResolver().resolve(aggregate)

    assert len(nodes) == 1 and nodes[0].node_type == "PRICING"
    assert nodes[0].attributes["total_cost"] == 249.0
    assert len(edges) == 1 and edges[0].predicate == "HAS_PRICE"


def test_pricing_graph_resolver_returns_nothing_when_no_cost_result():
    from ai.product_intelligence.models import ProductAggregate
    aggregate = ProductAggregate(
        identity=ProductIdentity(shopify_product_gid="gid://shopify/Product/2", handle="x"),
        resolved_at="2026-08-02T00:00:00Z",
    )
    nodes, edges = PricingGraphResolver().resolve(aggregate)
    assert nodes == [] and edges == []


def test_seo_graph_resolver_projects_real_seo_fields():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    _, read_model, _ = _build_product_intelligence_service(catalog)
    nodes, edges = SEOGraphResolver().resolve(read_model)

    assert len(nodes) == 1 and nodes[0].node_type == "SEO"
    assert nodes[0].label == "Motu Patlu Cake - Eggless | Meerut"
    assert edges[0].predicate == "OPTIMIZED_FOR"


def test_product_graph_resolver_composes_everything():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    aggregate, read_model, validation = _build_product_intelligence_service(catalog)
    resolver = ProductGraphResolver(catalog)
    nodes, edges = resolver.resolve(aggregate, read_model, validation)

    product_node = next(n for n in nodes if n.node_type == "PRODUCT")
    assert product_node.attributes["is_valid"] is True
    assert product_node.native_id == "gid://shopify/Product/1"

    predicates = {e.predicate for e in edges}
    assert "HAS_COLOR" in predicates, "the matched 'Red' term is in the Colour Name vocabulary"
    assert "HAS_COLLECTION" in predicates
    assert "HAS_OCCASION" in predicates
    assert "HAS_THEME" in predicates
    assert "HAS_PRICE" in predicates
    assert "OPTIMIZED_FOR" in predicates

    occasion_nodes = [n for n in nodes if n.node_type == "OCCASION"]
    assert len(occasion_nodes) == 1 and occasion_nodes[0].native_id == "birthday"

    theme_nodes = [n for n in nodes if n.node_type == "THEME"]
    assert len(theme_nodes) == 1 and theme_nodes[0].native_id == "spiderman"

    # the untagged "no-namespace-tag" must be silently skipped, not mis-typed
    assert all(n.native_id != "no-namespace-tag" for n in nodes)


if __name__ == "__main__":
    test_taxonomy_graph_resolver_produces_categories_and_part_of_edge()
    test_pricing_graph_resolver_projects_calculated_cost()
    test_pricing_graph_resolver_returns_nothing_when_no_cost_result()
    test_seo_graph_resolver_projects_real_seo_fields()
    test_product_graph_resolver_composes_everything()
    print("OK")
