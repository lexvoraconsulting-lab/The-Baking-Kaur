"""
Enterprise Product Intelligence Engine v1 - plain dataclass models.

WHAT THIS PACKAGE IS
  A thin orchestration/read-model layer over the existing stack (EAL, EAR,
  EAD, ai.attribute_distribution, ai.taxonomy, ai.pricing, plus live Shopify
  collection/SEO data). It owns NO business data of its own - every field on
  ProductAggregate is resolved live from one of those systems by a Resolver
  (see resolvers.py) and never independently persisted. This is the concrete
  implementation of what docs/00_Governance/VIG-003-Data-Principles.md calls
  the "Product Genome" and docs/10_Taxonomy/Entity_Model.md calls the
  "Business Entity" - one concept, cross-referenced here rather than given a
  third competing name (see docs/adr/2026-08-02-product-intelligence-engine.md).

AGGREGATE VS READ MODEL (DDD)
  ProductAggregate is the full, rich, internal composition (raw EAL records,
  raw taxonomy entities) - correct for callers that need the underlying
  detail. ProductReadModel (build_read_model) is a flattened, denormalized
  projection - what a future API, AI Genome, or ERP integration actually
  wants: simple fields, no nested domain objects to unmarshal.

WHY NO models_pydantic.py HERE, UNLIKE ai.eal / ai.pricing
  Those modules validate externally-editable input (hand-written JSON/YAML
  config or extraction output) - exactly where a validated wire format earns
  its keep. Everything on ProductAggregate is assembled in-memory from
  already-validated upstream systems; the correctness surface this package
  actually needs is business-rule validation (ProductValidationService, in
  validation.py), not a second schema for third-party input that doesn't
  exist at this layer.

WHY ProductEntityLink IS NEW, NOT A REUSE OF ai.taxonomy.models.Relationship
  ECP-100's review found the Image<->Product join point genuinely missing
  from every existing package. ai.taxonomy.Relationship's subject/object
  types are a closed Literal (TaxonomyEntityType) scoped to taxonomy-internal
  entities, and Build-005 (Master Taxonomy) is frozen - extending that Literal
  would mean editing frozen, out-of-scope code. ProductEntityLink is a small,
  deliberately new record, owned by this package, that fills exactly that gap
  without touching Taxonomy's contract.
"""
from dataclasses import dataclass, field
from typing import Any, Literal

from ai.eal.models import EALAttributeRecord
from ai.pricing.models import CostResult
from ai.taxonomy.models_pydantic import CategoryModel, RelationshipModel, TermModel

from ai.product_intelligence.ids import compute_product_intelligence_id

PRODUCT_INTELLIGENCE_VERSION = "1.0"

EntityLinkRelationship = Literal["DEPICTS", "PRIMARY_IMAGE", "PART_OF_BUNDLE"]
ValidationSeverity = Literal["error", "warning"]
ProductEventType = Literal[
    "product.resolved", "product.validated", "product.validation_failed", "product.pending_slice",
]


@dataclass(frozen=True)
class ProductIdentity:
    """Wraps the real, already-canonical Shopify product GID - never a
    competing primary key. product_intelligence_id is a derived correlation
    id for this engine's own internal use only (caching, eventing, logs)."""
    shopify_product_gid: str
    handle: str
    product_intelligence_id: str = ""

    def __post_init__(self):
        if not self.shopify_product_gid:
            raise ValueError("shopify_product_gid is required")
        if not self.product_intelligence_id:
            object.__setattr__(
                self, "product_intelligence_id",
                compute_product_intelligence_id(self.shopify_product_gid),
            )


@dataclass(frozen=True)
class ProductEntityLink:
    """The Image<->Product join point - see module docstring. eal_entity_id
    is an ai.eal entity_id (an image/region/object), never a second copy of
    the EAL record itself."""
    shopify_product_gid: str
    eal_entity_id: str
    relationship: EntityLinkRelationship
    confidence: float | None = None


@dataclass(frozen=True)
class AttributeSlice:
    attributes: tuple[EALAttributeRecord, ...] = ()
    source_entity_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class TaxonomySlice:
    """Holds ai.taxonomy's *Model (Pydantic) instances, not the plain
    dataclasses - ai.taxonomy.TaxonomyCatalog stores and returns Model
    instances (see catalog.py), so that is genuinely what this slice
    resolves, not a re-typed copy."""
    categories: tuple[CategoryModel, ...] = ()
    terms: tuple[TermModel, ...] = ()
    relationships: tuple[RelationshipModel, ...] = ()


@dataclass(frozen=True)
class CollectionSlice:
    """Sourced from live Shopify `tags` - CLAUDE.md notes this field is
    never queried or written by anything in this repo today, so this slice
    resolves empty until a live CollectionResolverPort implementation is
    wired in. Empty is the honest, correct answer, not a bug."""
    tags: tuple[str, ...] = ()
    collection_handles: tuple[str, ...] = ()


@dataclass(frozen=True)
class PricingSlice:
    cost_result: CostResult | None = None


@dataclass(frozen=True)
class MetadataSlice:
    title: str | None = None
    status: str | None = None
    product_type: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None


@dataclass(frozen=True)
class ProductAggregate:
    """The Canonical Product Aggregate - assembled live by
    ProductIntelligenceService from Resolver outputs, never independently
    persisted. resolved_at is caller-supplied (this package makes no
    wall-clock calls itself), matching ai.pricing.TokenUsage.recorded_at's
    convention."""
    identity: ProductIdentity
    resolved_at: str
    attributes: AttributeSlice = field(default_factory=AttributeSlice)
    taxonomy: TaxonomySlice = field(default_factory=TaxonomySlice)
    collections: CollectionSlice = field(default_factory=CollectionSlice)
    pricing: PricingSlice = field(default_factory=PricingSlice)
    metadata: MetadataSlice = field(default_factory=MetadataSlice)
    entity_links: tuple[ProductEntityLink, ...] = ()
    product_intelligence_version: str = PRODUCT_INTELLIGENCE_VERSION


@dataclass(frozen=True)
class ProductReadModel:
    """The canonical, flattened read surface this engine exposes - what a
    future API, AI Genome, or ERP integration should actually consume.
    Denormalized on purpose: no nested domain objects to unmarshal."""
    product_intelligence_id: str
    shopify_product_gid: str
    handle: str
    resolved_at: str
    title: str | None = None
    status: str | None = None
    product_type: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None
    tags: tuple[str, ...] = ()
    collection_handles: tuple[str, ...] = ()
    attribute_count: int = 0
    taxonomy_category_names: tuple[str, ...] = ()
    price_status: str | None = None
    price_total: float | None = None
    price_currency: str | None = None
    is_valid: bool | None = None


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: ValidationSeverity
    message: str
    field: str | None = None


@dataclass(frozen=True)
class ProductValidationResult:
    product_intelligence_id: str
    is_valid: bool
    validated_at: str
    issues: tuple[ValidationIssue, ...] = ()

    @staticmethod
    def ok(product_intelligence_id: str, validated_at: str) -> "ProductValidationResult":
        return ProductValidationResult(product_intelligence_id, True, validated_at, ())


def build_read_model(
    aggregate: ProductAggregate, validation: "ProductValidationResult | None" = None,
) -> ProductReadModel:
    """The one place ProductAggregate -> ProductReadModel flattening
    happens - a pure function, not a method, so both ProductIntelligenceService
    and any future direct caller build the exact same projection."""
    cost = aggregate.pricing.cost_result
    return ProductReadModel(
        product_intelligence_id=aggregate.identity.product_intelligence_id,
        shopify_product_gid=aggregate.identity.shopify_product_gid,
        handle=aggregate.identity.handle,
        resolved_at=aggregate.resolved_at,
        title=aggregate.metadata.title,
        status=aggregate.metadata.status,
        product_type=aggregate.metadata.product_type,
        seo_title=aggregate.metadata.seo_title,
        seo_description=aggregate.metadata.seo_description,
        tags=aggregate.collections.tags,
        collection_handles=aggregate.collections.collection_handles,
        attribute_count=len(aggregate.attributes.attributes),
        taxonomy_category_names=tuple(c.name for c in aggregate.taxonomy.categories),
        price_status=cost.status if cost else None,
        price_total=cost.total_cost if cost else None,
        price_currency=cost.currency if cost else None,
        is_valid=validation.is_valid if validation else None,
    )


@dataclass(frozen=True)
class ProductEvent:
    """What ProductIntelligenceService emits to an injected observer -
    mirrors ai.pricing's observer-hook shape rather than a message-bus
    payload, since no event bus exists anywhere in this repo yet."""
    event_id: str
    event_type: ProductEventType
    product_intelligence_id: str
    shopify_product_gid: str
    occurred_at: str
    payload: dict[str, Any] = field(default_factory=dict)
