"""
Enterprise Product Intelligence Engine v1 - the canonical service.

WHY THIS IS "THE ONE CANONICAL PRODUCT INTELLIGENCE INTERFACE"
  ProductIntelligenceService is the only class a caller (a future API layer,
  AI Genome integration, or ERP sync) should ever need: resolve_product()
  assembles a ProductAggregate live from the injected resolvers, never from
  its own storage; validate_product() runs ProductValidationService and
  reports the result; get_read_model() flattens either into the external-
  facing projection. Every dependency is constructor-injected (Dependency
  Inversion) with the same "sensible default, opt in to more" shape
  ai.pricing.PricingService established - collection_resolver/metadata_resolver
  default to fakes that resolve empty (so this service is fully usable and
  testable before any live Shopify wiring exists), while attribute/taxonomy/
  pricing resolvers have no default since they need real EAR/EAD/Taxonomy/
  Pricing data a caller must actually provide.
"""
from ai.attribute_distribution.models import DistributionRecord
from ai.product_intelligence.events import build_event
from ai.product_intelligence.models import (
    ProductAggregate, ProductEntityLink, ProductIdentity, ProductReadModel,
    ProductValidationResult, build_read_model,
)
from ai.product_intelligence.observability import NullObserver, ProductIntelligenceObserver
from ai.product_intelligence.resolvers import (
    AttributeResolver, CollectionResolverPort, FakeCollectionResolver, FakeMetadataResolver,
    MetadataResolverPort, PricingResolver, TaxonomyResolver,
)
from ai.product_intelligence.validation import ProductValidationService


class ProductIntelligenceService:
    def __init__(
        self,
        attribute_resolver: AttributeResolver,
        taxonomy_resolver: TaxonomyResolver,
        pricing_resolver: PricingResolver,
        collection_resolver: CollectionResolverPort | None = None,
        metadata_resolver: MetadataResolverPort | None = None,
        validation_service: ProductValidationService | None = None,
        observer: ProductIntelligenceObserver | None = None,
    ):
        self._attribute_resolver = attribute_resolver
        self._taxonomy_resolver = taxonomy_resolver
        self._pricing_resolver = pricing_resolver
        self._collection_resolver = collection_resolver or FakeCollectionResolver()
        self._metadata_resolver = metadata_resolver or FakeMetadataResolver()
        self._validation_service = validation_service or ProductValidationService()
        self._observer = observer or NullObserver()

    def resolve_product(
        self,
        identity: ProductIdentity,
        entity_links: list[ProductEntityLink],
        distribution_records: list[DistributionRecord],
        resolved_at: str,
    ) -> ProductAggregate:
        """Assembles a ProductAggregate live from every injected resolver -
        the aggregate itself is never stored by this service; it is a
        fresh, in-memory composition every call, which is what "must NOT
        own business data" means in practice."""
        attributes = self._attribute_resolver.resolve(entity_links)
        taxonomy = self._taxonomy_resolver.resolve(attributes)
        pricing = self._pricing_resolver.resolve(distribution_records)
        collections = self._collection_resolver.fetch(identity)
        metadata = self._metadata_resolver.fetch(identity)

        aggregate = ProductAggregate(
            identity=identity,
            resolved_at=resolved_at,
            attributes=attributes,
            taxonomy=taxonomy,
            collections=collections,
            pricing=pricing,
            metadata=metadata,
            entity_links=tuple(entity_links),
        )

        self._observer.on_product_resolved(build_event(
            "product.resolved", identity.product_intelligence_id,
            identity.shopify_product_gid, resolved_at,
        ))
        if pricing.cost_result is not None and pricing.cost_result.status == "pending_calculation":
            self._observer.on_slice_pending(build_event(
                "product.pending_slice", identity.product_intelligence_id,
                identity.shopify_product_gid, resolved_at,
                payload={"slice": "pricing", "reason": pricing.cost_result.reason},
            ))
        return aggregate

    def validate_product(self, aggregate: ProductAggregate, validated_at: str) -> ProductValidationResult:
        result = self._validation_service.validate(aggregate, validated_at)
        event = build_event(
            "product.validated" if result.is_valid else "product.validation_failed",
            aggregate.identity.product_intelligence_id,
            aggregate.identity.shopify_product_gid,
            validated_at,
            payload={"issue_count": len(result.issues)},
        )
        self._observer.on_product_validated(event, result)
        return result

    def get_read_model(
        self, aggregate: ProductAggregate, validation: ProductValidationResult | None = None,
    ) -> ProductReadModel:
        return build_read_model(aggregate, validation)
