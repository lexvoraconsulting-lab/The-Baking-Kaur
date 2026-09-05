#!/usr/bin/env python3
"""
Self-check for ai.product_intelligence's core domain: ids, models,
validation, events, extensions, and the end-to-end
ProductIntelligenceService flow - no network calls.

USAGE
  python -m ai.product_intelligence.test_product_intelligence
"""
from ai.attribute_distribution.models import DistributionRecord
from ai.ead.loader import load_definitions
from ai.ear.loader import load_registry
from ai.eal.models import EALAttributeRecord, Provenance
from ai.pricing import FileConfigPricingRepository, PricingService, StandardTokenCostStrategy
from ai.taxonomy.loader import load_catalog

from ai.product_intelligence.events import build_event
from ai.product_intelligence.extensions import (
    NotConnectedAIGenomePort, NotConnectedAPIPort, NotConnectedERPPort,
)
from ai.product_intelligence.ids import compute_event_id, compute_product_intelligence_id
from ai.product_intelligence.models import (
    CollectionSlice, MetadataSlice, ProductAggregate, ProductEntityLink, ProductIdentity,
    build_read_model,
)
from ai.product_intelligence.observability import ProductIntelligenceObserver
from ai.product_intelligence.resolvers import (
    AttributeResolver, FakeCollectionResolver, FakeMetadataResolver, PricingResolver, TaxonomyResolver,
)
from ai.product_intelligence.service import ProductIntelligenceService
from ai.product_intelligence.validation import ProductValidationService

_PROVENANCE = Provenance(
    provider="ollama", model="llava", schema_version="1.0",
    taxonomy_version="1.0", extracted_at="2026-08-02T00:00:00Z",
)


def test_product_intelligence_id_is_deterministic_and_namespaced():
    gid = "gid://shopify/Product/123"
    assert compute_product_intelligence_id(gid) == compute_product_intelligence_id(gid)
    assert ProductIdentity(shopify_product_gid=gid, handle="x").product_intelligence_id == \
        compute_product_intelligence_id(gid)


def test_product_identity_rejects_empty_gid():
    try:
        ProductIdentity(shopify_product_gid="", handle="x")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_build_event_is_deterministic_for_identical_inputs():
    e1 = compute_event_id("product.resolved", "pi-1", "2026-08-02T00:00:00Z")
    e2 = compute_event_id("product.resolved", "pi-1", "2026-08-02T00:00:00Z")
    assert e1 == e2
    event = build_event("product.resolved", "pi-1", "gid://shopify/Product/1", "2026-08-02T00:00:00Z")
    assert event.event_id == e1


def test_build_read_model_flattens_aggregate():
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="motu-patlu-cake")
    aggregate = ProductAggregate(
        identity=identity, resolved_at="2026-08-02T00:00:00Z",
        collections=CollectionSlice(tags=("occasion:birthday",)),
        metadata=MetadataSlice(title="Motu Patlu Cake", status="ACTIVE"),
    )
    read_model = build_read_model(aggregate)
    assert read_model.product_intelligence_id == identity.product_intelligence_id
    assert read_model.title == "Motu Patlu Cake"
    assert read_model.tags == ("occasion:birthday",)
    assert read_model.attribute_count == 0
    assert read_model.is_valid is None


def test_validation_service_flags_missing_metadata_as_error():
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="x")
    aggregate = ProductAggregate(identity=identity, resolved_at="2026-08-02T00:00:00Z")
    result = ProductValidationService().validate(aggregate, validated_at="2026-08-02T00:00:00Z")
    assert result.is_valid is False
    codes = {issue.code for issue in result.issues}
    assert "metadata_unresolved" in codes


def test_validation_service_warns_but_stays_valid_when_only_optional_slices_missing():
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="x")
    aggregate = ProductAggregate(
        identity=identity, resolved_at="2026-08-02T00:00:00Z",
        metadata=MetadataSlice(title="Some Cake", status="ACTIVE"),
    )
    result = ProductValidationService().validate(aggregate, validated_at="2026-08-02T00:00:00Z")
    assert result.is_valid is True
    codes = {issue.code for issue in result.issues}
    assert {"no_attributes_resolved", "no_taxonomy_resolved", "no_tags_resolved", "pricing_unresolved"} <= codes
    assert all(issue.severity == "warning" for issue in result.issues)


def test_validation_service_detects_duplicate_entity_link():
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="x")
    link = ProductEntityLink(identity.shopify_product_gid, "img-001", "PRIMARY_IMAGE")
    aggregate = ProductAggregate(
        identity=identity, resolved_at="2026-08-02T00:00:00Z",
        metadata=MetadataSlice(title="Some Cake", status="ACTIVE"),
        entity_links=(link, link),
    )
    result = ProductValidationService().validate(aggregate, validated_at="2026-08-02T00:00:00Z")
    codes = {issue.code for issue in result.issues}
    assert "duplicate_entity_link" in codes


class _SpyObserver(ProductIntelligenceObserver):
    def __init__(self):
        self.resolved = []
        self.validated = []
        self.pending = []

    def on_product_resolved(self, event):
        self.resolved.append(event)

    def on_product_validated(self, event, result):
        self.validated.append((event, result))

    def on_slice_pending(self, event):
        self.pending.append(event)


def test_service_resolves_validates_and_builds_read_model_end_to_end():
    registry = load_registry("ai/ear/examples/registry.json")
    definitions = load_definitions("ai/ead/examples/definitions.json")
    catalog = load_catalog("ai/taxonomy/examples/catalog.json")
    eal_record = EALAttributeRecord(
        canonical_path="eal.domain.bakery.colour.primary", namespace="domain.bakery", group="colour",
        entity_id="img-001", entity_type="image", value="Red", value_state="present",
        data_type="enum", provenance=_PROVENANCE, vocabulary="TAX-VOC-000001",
    )
    pricing_service = PricingService(
        repository=FileConfigPricingRepository(), strategy=StandardTokenCostStrategy(),
    )
    observer = _SpyObserver()
    identity = ProductIdentity(shopify_product_gid="gid://shopify/Product/1", handle="motu-patlu-cake")

    service = ProductIntelligenceService(
        attribute_resolver=AttributeResolver(registry, definitions, eal_records=[eal_record]),
        taxonomy_resolver=TaxonomyResolver(catalog),
        pricing_resolver=PricingResolver(pricing_service),
        collection_resolver=FakeCollectionResolver({
            identity.shopify_product_gid: CollectionSlice(tags=("occasion:birthday",)),
        }),
        metadata_resolver=FakeMetadataResolver({
            identity.shopify_product_gid: MetadataSlice(title="Motu Patlu Cake", status="ACTIVE"),
        }),
        observer=observer,
    )

    aggregate = service.resolve_product(
        identity=identity,
        entity_links=[ProductEntityLink(identity.shopify_product_gid, "img-001", "PRIMARY_IMAGE")],
        distribution_records=[],
        resolved_at="2026-08-02T00:00:00Z",
    )
    assert aggregate.attributes.attributes == (eal_record,)
    assert aggregate.taxonomy.terms[0].label == "Red"
    assert aggregate.pricing.cost_result.status == "pending_calculation"
    assert len(observer.resolved) == 1
    assert len(observer.pending) == 1, "pending pricing must fire on_slice_pending"

    validation = service.validate_product(aggregate, validated_at="2026-08-02T00:01:00Z")
    assert validation.is_valid is True
    assert len(observer.validated) == 1

    read_model = service.get_read_model(aggregate, validation)
    assert read_model.title == "Motu Patlu Cake"
    assert read_model.taxonomy_category_names == ()
    assert read_model.is_valid is True


def test_extension_ports_fail_loudly_not_silently():
    for port, method, args in (
        (NotConnectedAIGenomePort(), "push_product", (None,)),
        (NotConnectedERPPort(), "push_product", (None,)),
        (NotConnectedERPPort(), "pull_product", ("gid://shopify/Product/1",)),
        (NotConnectedAPIPort(), "serialize", (None,)),
    ):
        try:
            getattr(port, method)(*args)
            assert False, f"expected NotImplementedError from {port.__class__.__name__}.{method}"
        except NotImplementedError:
            pass


if __name__ == "__main__":
    test_product_intelligence_id_is_deterministic_and_namespaced()
    test_product_identity_rejects_empty_gid()
    test_build_event_is_deterministic_for_identical_inputs()
    test_build_read_model_flattens_aggregate()
    test_validation_service_flags_missing_metadata_as_error()
    test_validation_service_warns_but_stays_valid_when_only_optional_slices_missing()
    test_validation_service_detects_duplicate_entity_link()
    test_service_resolves_validates_and_builds_read_model_end_to_end()
    test_extension_ports_fail_loudly_not_silently()
    print("OK")
