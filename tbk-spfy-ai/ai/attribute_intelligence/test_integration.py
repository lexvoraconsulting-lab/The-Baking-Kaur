#!/usr/bin/env python3
"""
Self-check for ai.attribute_intelligence.integration - the real source
adapters over an already-resolved ai.product_intelligence round-trip - and
extensions.py's port contract. No network calls.

USAGE
  python -m ai.attribute_intelligence.test_integration
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

from ai.attribute_intelligence.extensions import NotConnectedGenomeAttributeSource, NotConnectedMerchantAttributeSource
from ai.attribute_intelligence.integration import observations_from_eal, observations_from_tags

_PROVENANCE = Provenance(
    provider="ollama", model="llava", schema_version="1.0",
    taxonomy_version="1.0", extracted_at="2026-08-02T00:00:00Z",
)


def _build_product_intelligence():
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    registry = load_registry("ai/ear/examples/registry.json")
    definitions = load_definitions("ai/ead/examples/definitions.json")
    eal_record = EALAttributeRecord(
        canonical_path="eal.domain.bakery.colour.primary", namespace="domain.bakery", group="colour",
        entity_id="img-001", entity_type="image", value="Red", value_state="present",
        data_type="enum", provenance=_PROVENANCE, vocabulary="TAX-VOC-000001", confidence=0.92,
    )
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="motu-patlu-cake")
    service = ProductIntelligenceService(
        attribute_resolver=AttributeResolver(registry, definitions, eal_records=[eal_record]),
        taxonomy_resolver=TaxonomyResolver(catalog),
        pricing_resolver=PricingResolver(PricingService(
            repository=FileConfigPricingRepository(), strategy=StandardTokenCostStrategy(),
        )),
        collection_resolver=FakeCollectionResolver({
            identity.shopify_product_gid: CollectionSlice(tags=("occasion:birthday", "no-namespace")),
        }),
        metadata_resolver=FakeMetadataResolver({
            identity.shopify_product_gid: MetadataSlice(title="Motu Patlu Cake", status="ACTIVE"),
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
    read_model = service.get_read_model(aggregate)
    return registry, aggregate, read_model


def test_observations_from_eal_uses_real_ear_join_and_preserves_confidence():
    registry, aggregate, _ = _build_product_intelligence()
    observations = observations_from_eal(aggregate, registry, observed_at="2026-08-02T00:00:00Z")
    assert len(observations) == 1
    obs = observations[0]
    assert obs.registry_reference == "EAR-000001"
    assert obs.source == "vision"
    assert obs.value == "Red"
    assert obs.confidence == 0.92
    assert obs.subject_id == "gid://shopify/Product/1"


def test_observations_from_tags_maps_namespace_and_skips_unmapped():
    _, _, read_model = _build_product_intelligence()
    observations = observations_from_tags(
        read_model, tag_namespace_to_registry_reference={"occasion": "EAR-000010"},
        observed_at="2026-08-02T00:00:00Z",
    )
    assert len(observations) == 1
    assert observations[0].registry_reference == "EAR-000010"
    assert observations[0].value == "birthday"
    assert observations[0].source == "shopify"
    assert observations[0].confidence == 1.0


def test_observations_from_tags_returns_nothing_for_unrecognized_namespace_mapping():
    _, _, read_model = _build_product_intelligence()
    observations = observations_from_tags(read_model, tag_namespace_to_registry_reference={}, observed_at="t")
    assert observations == []


def test_extension_ports_fail_loudly():
    for port, in ((NotConnectedMerchantAttributeSource(),), (NotConnectedGenomeAttributeSource(),)):
        try:
            port.fetch("gid://shopify/Product/1", "2026-08-02T00:00:00Z")
            assert False, f"expected NotImplementedError from {port.__class__.__name__}"
        except NotImplementedError:
            pass


if __name__ == "__main__":
    test_observations_from_eal_uses_real_ear_join_and_preserves_confidence()
    test_observations_from_tags_maps_namespace_and_skips_unmapped()
    test_observations_from_tags_returns_nothing_for_unrecognized_namespace_mapping()
    test_extension_ports_fail_loudly()
    print("OK")
