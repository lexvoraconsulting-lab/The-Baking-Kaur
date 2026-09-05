# ADR 0008: Product Intelligence Engine as the "Product Genome" / "Business Entity" implementation

Date: 2026-08-02

## Status

Accepted

## Context

[ECP-100](../30_Enterprise_Program_Roadmap/ECP-100_Architecture_Review.md) found that no package
in this repository models "a whole product" as an aggregate — but that this gap is a *named,
deliberate* one, not a missed piece: [VIG-003 (Data Principles)](../00_Governance/VIG-003-Data-Principles.md)
already names it "Product Genome" ("the normalized, application-facing view derived from the
Knowledge Graph"), and `docs/10_Taxonomy/Entity_Model.md` already names it "Business Entity" — two
governance documents, written independently, describing the same not-yet-implemented concept.

ECP-300 Sprint 300.1 asked for an "Enterprise Product Intelligence Engine" that orchestrates
existing services and exposes one canonical read model, explicitly stating it must NOT own business
data and must consume EAL → EAR → EAD → Distribution → Taxonomy → Pricing → Collections → SEO →
Vision → Business Entity. Introducing a third name ("Product Intelligence") for the same concept
VIG-003 and Entity_Model.md already name would repeat the exact "EAD means two different things"
collision [ADR 0006](2026-07-27-workstream-id-convention.md) had to correct.

ECP-100 also found the Image↔Product join point genuinely missing everywhere: `ai.taxonomy`'s
`Relationship` type is closed to a `TaxonomyEntityType` Literal scoped to taxonomy-internal
entities (`category`/`attribute_group`/`attribute`/`vocabulary`/`term`), and Build-005 (Master
Taxonomy) is frozen — extending that Literal to add `product`/`business_entity` would mean editing
frozen, out-of-scope code for a concern that isn't Taxonomy's.

## Decision

1. **One concept, cross-referenced, not a third name.** `ai/product_intelligence/` is built as the
   concrete implementation of VIG-003's "Product Genome" / `Entity_Model.md`'s "Business Entity" —
   every relevant docstring and doc cross-references both terms explicitly rather than presenting
   "Product Intelligence" as a fourth independent concept.
2. **The engine owns no business data.** `ProductAggregate` is assembled live, on demand, by
   Resolvers reading the real upstream systems (EAL/EAR/EAD via `ai.ear.registry.Registry` and
   `ai.ead.definitions.DefinitionSet`, `ai.taxonomy.catalog.TaxonomyCatalog`,
   `ai.pricing.PricingService`, `ai.attribute_distribution.models.DistributionRecord`) and is never
   independently persisted — satisfying VIG-003 Principle 2 ("No second, competing system of record
   may exist for data the Knowledge Graph already governs").
3. **`ProductIdentity` wraps the real Shopify GID.** It is never a competing primary key. A
   secondary, deterministic `product_intelligence_id` (uuid5 of the GID, distinct namespace UUID
   from every other module's) exists only for this engine's own internal correlation, caching, and
   eventing.
4. **`ProductEntityLink` is new, not a Taxonomy `Relationship` extension.** A small,
   `product_intelligence`-owned record fills the Image↔Product join gap ECP-100 identified, without
   touching Taxonomy's frozen, closed `TaxonomyEntityType` contract.
5. **Two resolver tiers.** `AttributeResolver`, `TaxonomyResolver`, and `PricingResolver` wrap
   pure-Python packages with no live dependency — fully real, fully offline-testable today.
   `CollectionResolverPort` and `MetadataResolverPort` are DI'd Protocols with fake
   (`FakeCollectionResolver`/`FakeMetadataResolver`) implementations for tests; a real live-Shopify
   implementation is deliberately not built in this sprint (CLAUDE.md confirms Shopify `tags` is
   queried nowhere in this repo today — there is no existing call site to extend).
6. **No `models_pydantic.py`.** Unlike `ai.eal`/`ai.pricing` (which validate externally-editable
   config/extraction files), everything on `ProductAggregate` is assembled in-memory from
   already-validated upstream systems. The correctness surface this package actually needs is
   business-rule validation (`ProductValidationService`), not a second wire-format schema for
   third-party input that doesn't exist at this layer.
7. **Extension points are ports, not implementations.** `AIGenomeSyncPort`, `ERPSyncPort`, and
   `ProductIntelligenceAPIPort` mirror `ai.pricing.domains.erp_integration`'s pattern exactly:
   define the contract, fail loudly (`NotImplementedError`) until a real target system exists,
   never guess at one.

## Consequences

- Any future Cake Genome / AI Genome work reads `ProductReadModel` (or implements
  `AIGenomeSyncPort`), not a fourth reinvention of what a product is.
- A future live Shopify collection/metadata integration is additive — it implements
  `CollectionResolverPort`/`MetadataResolverPort` and is injected into
  `ProductIntelligenceService`; no other file changes shape.
- `docs/10_Taxonomy/Entity_Model.md` and `docs/00_Governance/VIG-003-Data-Principles.md` should be
  updated (follow-up, not part of this ADR) to point at `ai/product_intelligence/` as their
  concrete implementation, closing the "named but never implemented" gap ECP-100 flagged.
- `ai.taxonomy`'s frozen Build-005 contract is unmodified — zero risk to already-shipped taxonomy
  content.

## Notes

Satisfies VIG-009's one-decision-one-document rule. Supersedes no prior ADR; extends the reasoning
in [ADR 0006](2026-07-27-workstream-id-convention.md) (naming discipline) and
[ADR 0007](2026-07-28-build-005-007-resequencing.md) (frozen-Build discipline) to this new package.
