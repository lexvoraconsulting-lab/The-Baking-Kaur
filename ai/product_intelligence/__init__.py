"""
Enterprise Product Intelligence Engine v1 - orchestrates existing services
(EAL/EAR/EAD, ai.attribute_distribution, ai.taxonomy, ai.pricing, live
Shopify data) into one canonical, read-only Product Intelligence surface.
Owns no business data of its own. See docs/PRODUCT_INTELLIGENCE_ARCHITECTURE.md.
"""
from ai.product_intelligence.events import build_event
from ai.product_intelligence.extensions import (
    AIGenomeSyncPort, ERPSyncPort, NotConnectedAIGenomePort, NotConnectedAPIPort,
    NotConnectedERPPort, ProductIntelligenceAPIPort,
)
from ai.product_intelligence.ids import compute_event_id, compute_product_intelligence_id
from ai.product_intelligence.models import (
    PRODUCT_INTELLIGENCE_VERSION, AttributeSlice, CollectionSlice, MetadataSlice,
    PricingSlice, ProductAggregate, ProductEntityLink, ProductEvent, ProductIdentity,
    ProductReadModel, ProductValidationResult, TaxonomySlice, ValidationIssue, build_read_model,
)
from ai.product_intelligence.observability import (
    LoggingObserver, NullObserver, ProductIntelligenceObserver,
)
from ai.product_intelligence.resolvers import (
    AttributeResolver, CollectionResolverPort, FakeCollectionResolver, FakeMetadataResolver,
    MetadataResolverPort, PricingResolver, TaxonomyResolver,
)
from ai.product_intelligence.service import ProductIntelligenceService
from ai.product_intelligence.validation import ProductValidationService

__all__ = [
    "PRODUCT_INTELLIGENCE_VERSION",
    "AIGenomeSyncPort",
    "AttributeResolver",
    "AttributeSlice",
    "CollectionResolverPort",
    "CollectionSlice",
    "ERPSyncPort",
    "FakeCollectionResolver",
    "FakeMetadataResolver",
    "LoggingObserver",
    "MetadataResolverPort",
    "MetadataSlice",
    "NotConnectedAIGenomePort",
    "NotConnectedAPIPort",
    "NotConnectedERPPort",
    "NullObserver",
    "PricingResolver",
    "PricingSlice",
    "ProductAggregate",
    "ProductEntityLink",
    "ProductEvent",
    "ProductIdentity",
    "ProductIntelligenceAPIPort",
    "ProductIntelligenceObserver",
    "ProductIntelligenceService",
    "ProductReadModel",
    "ProductValidationResult",
    "ProductValidationService",
    "TaxonomyResolver",
    "TaxonomySlice",
    "ValidationIssue",
    "build_event",
    "build_read_model",
    "compute_event_id",
    "compute_product_intelligence_id",
]
