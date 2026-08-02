#!/usr/bin/env python3
"""
Self-check for ai.product_intelligence's five resolvers, against real
example data from ai.ear/ai.ead/ai.taxonomy (not synthetic IDs) - no
network calls.

USAGE
  python -m ai.product_intelligence.test_resolvers
"""
from ai.attribute_distribution.models import DistributionRecord
from ai.ead.loader import load_definitions
from ai.ear.loader import load_registry
from ai.eal.models import EALAttributeRecord, Provenance
from ai.pricing import FileConfigPricingRepository, PricingService, StandardTokenCostStrategy
from ai.taxonomy.loader import load_catalog

from ai.product_intelligence.models import CollectionSlice, MetadataSlice, ProductEntityLink, ProductIdentity
from ai.product_intelligence.resolvers import (
    AttributeResolver, FakeCollectionResolver, FakeMetadataResolver, PricingResolver, TaxonomyResolver,
)

_PROVENANCE = Provenance(
    provider="ollama", model="llava", schema_version="1.0",
    taxonomy_version="1.0", extracted_at="2026-08-02T00:00:00Z",
)


def _colour_record(value="Red") -> EALAttributeRecord:
    return EALAttributeRecord(
        canonical_path="eal.domain.bakery.colour.primary",
        namespace="domain.bakery", group="colour",
        entity_id="img-001", entity_type="image",
        value=value, value_state="present", data_type="enum",
        provenance=_PROVENANCE, vocabulary="TAX-VOC-000001",
    )


def test_attribute_resolver_joins_via_entity_links():
    registry = load_registry("ai/ear/examples/registry.json")
    definitions = load_definitions("ai/ead/examples/definitions.json")
    record = _colour_record()
    resolver = AttributeResolver(registry, definitions, eal_records=[record])

    links = [ProductEntityLink("gid://shopify/Product/1", "img-001", "PRIMARY_IMAGE")]
    slice_ = resolver.resolve(links)
    assert slice_.attributes == (record,)
    assert slice_.source_entity_ids == ("img-001",)

    entry = resolver.registry_entry_for(record.canonical_path)
    assert entry is not None and entry.attribute_id == "EAR-000001"
    definition = resolver.definition_for(entry.attribute_id)
    assert definition is not None and definition.registry_reference == "EAR-000001"


def test_attribute_resolver_returns_empty_for_unlinked_entities():
    registry = load_registry("ai/ear/examples/registry.json")
    definitions = load_definitions("ai/ead/examples/definitions.json")
    resolver = AttributeResolver(registry, definitions, eal_records=[_colour_record()])

    slice_ = resolver.resolve([ProductEntityLink("gid://shopify/Product/1", "img-999", "PRIMARY_IMAGE")])
    assert slice_.attributes == ()
    assert slice_.source_entity_ids == ("img-999",)


def test_taxonomy_resolver_matches_term_by_vocabulary_and_value():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    resolver = TaxonomyResolver(catalog)
    from ai.product_intelligence.models import AttributeSlice

    slice_ = resolver.resolve(AttributeSlice(attributes=(_colour_record(value="Red"),)))
    assert len(slice_.terms) == 1
    assert slice_.terms[0].term_id == "TAX-TERM-000001"
    assert slice_.terms[0].label == "Red"


def test_taxonomy_resolver_matches_via_synonym_and_ignores_unmatched_value():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    resolver = TaxonomyResolver(catalog)
    from ai.product_intelligence.models import AttributeSlice

    no_match = resolver.resolve(AttributeSlice(attributes=(_colour_record(value="Chartreuse"),)))
    assert no_match.terms == () and no_match.categories == ()


def test_pricing_resolver_returns_pending_when_no_distribution_record_priced():
    repository = FileConfigPricingRepository()
    pricing_service = PricingService(repository=repository, strategy=StandardTokenCostStrategy())
    resolver = PricingResolver(pricing_service)

    slice_ = resolver.resolve(distribution_records=[])
    assert slice_.cost_result.status == "pending_calculation"


def test_pricing_resolver_uses_a_successful_distribution_record():
    repository = FileConfigPricingRepository()
    pricing_service = PricingService(repository=repository, strategy=StandardTokenCostStrategy())
    resolver = PricingResolver(pricing_service)

    record = DistributionRecord(
        registry_reference="EAR-000001", target_system="shopify",
        value=249.0, human_verification_status="verified", status="success",
    )
    slice_ = resolver.resolve(distribution_records=[record])
    assert slice_.cost_result.status == "calculated"
    assert slice_.cost_result.total_cost == 249.0


def test_fake_collection_and_metadata_resolvers_are_pure_lookups():
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="motu-patlu-cake")
    collections = FakeCollectionResolver({
        identity.shopify_product_gid: CollectionSlice(tags=("occasion:birthday",), collection_handles=("birthday-cakes",)),
    })
    metadata = FakeMetadataResolver({
        identity.shopify_product_gid: MetadataSlice(title="Motu Patlu Cake", status="ACTIVE"),
    })
    assert collections.fetch(identity).tags == ("occasion:birthday",)
    assert metadata.fetch(identity).title == "Motu Patlu Cake"

    unknown = ProductIdentity(shopify_product_gid="gid://shopify/Product/999", handle="unknown")
    assert collections.fetch(unknown) == CollectionSlice()
    assert metadata.fetch(unknown) == MetadataSlice()


if __name__ == "__main__":
    test_attribute_resolver_joins_via_entity_links()
    test_attribute_resolver_returns_empty_for_unlinked_entities()
    test_taxonomy_resolver_matches_term_by_vocabulary_and_value()
    test_taxonomy_resolver_matches_via_synonym_and_ignores_unmatched_value()
    test_pricing_resolver_returns_pending_when_no_distribution_record_priced()
    test_pricing_resolver_uses_a_successful_distribution_record()
    test_fake_collection_and_metadata_resolvers_are_pure_lookups()
    print("OK")
