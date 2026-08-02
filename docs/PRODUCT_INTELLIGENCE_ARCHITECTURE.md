# Enterprise Product Intelligence Engine — Architecture (ECP-300 Sprint 300.1)

`ai/product_intelligence/` orchestrates the existing attribute/taxonomy/pricing stack into one
canonical, read-only Product Intelligence surface. It is the concrete implementation of what
[VIG-003 (Data Principles)](00_Governance/VIG-003-Data-Principles.md) calls the **"Product
Genome"** and `docs/10_Taxonomy/Entity_Model.md` calls the **"Business Entity"** — one concept, not
a third competing name. See [ADR 0008](adr/2026-08-02-product-intelligence-engine.md) for the full
decision record.

## The hard requirement this design is built around

**The engine owns no business data.** Every field on `ProductAggregate` is resolved live by a
Resolver reading a real upstream system, never independently persisted. A `ProductIntelligenceService`
call produces a fresh, in-memory aggregate every time — there is no `ai/product_intelligence/`
database, cache, or file store anywhere in this package.

## Package layout

```
ai/product_intelligence/
  models.py            ProductIdentity, ProductEntityLink, the five per-source Slices,
                        ProductAggregate, ProductReadModel (+ build_read_model), ValidationIssue,
                        ProductValidationResult, ProductEvent
  ids.py                compute_product_intelligence_id() / compute_event_id() — deterministic
                        uuid5, distinct namespace from every other module's
  resolvers.py           AttributeResolver, TaxonomyResolver, PricingResolver (real, offline) +
                        CollectionResolverPort, MetadataResolverPort (Protocols) + their Fake
                        test doubles
  validation.py           ProductValidationService — cross-slice business-rule validation
  events.py                 build_event() — deterministic ProductEvent construction
  extensions.py               AIGenomeSyncPort, ERPSyncPort, ProductIntelligenceAPIPort — port-only,
                        NotImplementedError until a real target system exists
  observability.py             ProductIntelligenceObserver (ABC) + NullObserver + LoggingObserver
  service.py                    ProductIntelligenceService — the one canonical interface
  test_product_intelligence.py   self-check: python -m ai.product_intelligence.test_product_intelligence
  test_resolvers.py               self-check: python -m ai.product_intelligence.test_resolvers
```

No `models_pydantic.py` — see ADR 0008 §6 for why: this package validates business rules
(`ProductValidationService`), not externally-editable wire input, unlike `ai.eal`/`ai.pricing`.

## Dependency graph

```
                         ┌─────────────────────────────┐
                         │  ProductIntelligenceService  │   <- the ONE canonical interface
                         └──────────────┬───────────────┘
             ┌──────────────┬───────────┼───────────┬──────────────┐
             ▼              ▼           ▼           ▼              ▼
  AttributeResolver TaxonomyResolver PricingResolver  CollectionResolverPort  MetadataResolverPort
        │                  │              │            (Protocol, DI'd)        (Protocol, DI'd)
        ▼                  ▼              ▼                  │                      │
  ai.ear.Registry   ai.taxonomy.        ai.pricing.      FakeCollectionResolver  FakeMetadataResolver
  ai.ead.Definition  TaxonomyCatalog    PricingService     (test/offline;          (test/offline;
    Set + ai.eal            │           + ai.attribute_    live Shopify impl       live Shopify impl
   EALAttributeRecord        │            distribution.     not built this          not built this
     (DI'd list)             │            DistributionRecord sprint)                 sprint)
                             ▼
                    ai.taxonomy joins via
                    EAL attribute.vocabulary
                    + attribute.value <-> Term

  ProductValidationService  <- pure function of a ProductAggregate, no dependencies
  build_event / build_read_model  <- pure functions, no dependencies
  ProductIntelligenceObserver  <- injected, defaults to NullObserver (no-op)
```

No circular dependencies: `ai.eal`, `ai.ear`, `ai.ead`, `ai.taxonomy`, `ai.attribute_distribution`,
and `ai.pricing` are all leaf packages with respect to `ai.product_intelligence` — none of them
imports anything from it.

## Aggregate vs. Read Model (DDD)

`ProductAggregate` is the full, rich composition — raw `EALAttributeRecord`s, raw
`ai.taxonomy` `*Model` instances, a `CostResult` — correct for a caller that needs the underlying
detail. `ProductReadModel` (`build_read_model(aggregate)`) is a flattened, denormalized projection:
plain strings/tuples/floats, no nested domain objects to unmarshal — what a future API, AI Genome,
or ERP integration should actually consume.

## The Image↔Product join: `ProductEntityLink`

ECP-100 found this join point missing from every existing package. `ai.taxonomy.Relationship`'s
subject/object types are a closed `TaxonomyEntityType` Literal scoped to taxonomy-internal entities,
and Build-005 is frozen, so extending that Literal was rejected (ADR 0008 §4). `ProductEntityLink`
(`shopify_product_gid`, `eal_entity_id`, `relationship: DEPICTS|PRIMARY_IMAGE|PART_OF_BUNDLE`) is a
small, new, `product_intelligence`-owned record that fills the gap without touching Taxonomy's
contract. A caller supplies the links explicitly — this package never invents one.

## How a product resolves (real join logic, not a stub)

```
ProductEntityLink[] (caller-supplied: which EAL entity_ids belong to this product)
      │
      ▼
AttributeResolver.resolve(links)
      │  looks up each link.eal_entity_id in an injected list[EALAttributeRecord]
      ▼
AttributeSlice (real EAL records)
      │
      ▼
TaxonomyResolver.resolve(attribute_slice)
      │  for each attribute with a `vocabulary`, matches attribute.value against
      │  Term.label / Term.synonyms within that Vocabulary, then pulls any
      │  TaxonomyCatalog relationship attached to a matched Term
      ▼
TaxonomySlice (real Terms/Categories/Relationships)

DistributionRecord[] (caller-supplied) ──► PricingResolver.resolve() ──► PricingSlice
ProductIdentity ──► CollectionResolverPort.fetch() ──► CollectionSlice
ProductIdentity ──► MetadataResolverPort.fetch()   ──► MetadataSlice

All five slices + ProductIdentity + entity_links ──► ProductAggregate
```

## Public interfaces

- `ProductIntelligenceService(attribute_resolver, taxonomy_resolver, pricing_resolver, collection_resolver=None, metadata_resolver=None, validation_service=None, observer=None)`
  - `.resolve_product(identity, entity_links, distribution_records, resolved_at) -> ProductAggregate`
  - `.validate_product(aggregate, validated_at) -> ProductValidationResult`
  - `.get_read_model(aggregate, validation=None) -> ProductReadModel`
- `ProductValidationService().validate(aggregate, validated_at) -> ProductValidationResult`
- `build_read_model(aggregate, validation=None) -> ProductReadModel`
- `build_event(event_type, product_intelligence_id, shopify_product_gid, occurred_at, payload=None) -> ProductEvent`

## Validation rules (`ProductValidationService`)

| Code | Severity | Meaning |
|---|---|---|
| `missing_handle` | error | `ProductIdentity.handle` is empty |
| `metadata_unresolved` | error | `MetadataSlice` is entirely empty — the metadata resolver likely isn't wired |
| `no_attributes_resolved` | warning | No EAL attributes joined for this product's linked entities |
| `no_taxonomy_resolved` | warning | No taxonomy category/term matched |
| `no_tags_resolved` | warning | No Shopify tags — expected today, see below |
| `pricing_unresolved` / `pricing_pending` | warning | No cost result, or an honest Pending one |
| `duplicate_entity_link` | warning | The same `(eal_entity_id, relationship)` linked twice |

Only genuinely product-breaking conditions are errors; empty optional slices are warnings, because
they are often *honest*, not broken — see the next section.

## Observability

`ProductIntelligenceObserver` (ABC, no-op-by-default hooks: `on_product_resolved`,
`on_product_validated`, `on_slice_pending`) mirrors `ai.pricing.observability.PricingObserver`
exactly. `NullObserver` is the default — opting in (`LoggingObserver`, or a future metrics/tracing
observer) is additive, never required.

## Extension points (future work, deliberately not built here)

- **`AIGenomeSyncPort`** — the seam a future Cake Genome / AI Genome system plugs into. No such
  system exists yet; ECP-300 explicitly defers it.
- **`ERPSyncPort`** — same "no first-contact API inspection possible" blocker
  `ai.attribute_distribution.erp_adapter` and `ai.pricing.domains.erp_integration` already document.
- **`ProductIntelligenceAPIPort`** — the seam a future HTTP/GraphQL API layer implements against
  `ProductReadModel`. No API framework exists in this repo yet.

All three are `ABC`s with a `NotConnected*`/`NotImplementedAPIPort` concrete class that raises
`NotImplementedError` — the same "fail loudly, this is a configuration error, not a Pending case"
reasoning `ai.pricing.domains.erp_integration.NotConnectedERPPort` established. Wiring a real
implementation later changes zero call sites in `ai.product_intelligence` itself.

## Known real gap this sprint surfaces honestly, does not fabricate around

`CollectionResolverPort` and `MetadataResolverPort` have no live-Shopify implementation in this
sprint — CLAUDE.md confirms Shopify `tags` is queried nowhere in this repo today, so there is no
existing call site to reuse. `CollectionSlice`/`MetadataSlice` resolve empty via the `Fake*`
doubles until a real implementation is written (future work, additive per the port contract above)
— empty is the honest, correct answer today, not a bug, and `ProductValidationService` reports it
as a `warning`, never an `error`.

## Validation checklist (ECP-300's own success criteria)

- **No duplicate models** — `ProductAggregate` composes existing types (`EALAttributeRecord`,
  `ai.taxonomy.*Model`, `CostResult`) by reference; it defines no re-typed copy of any of them.
  `ProductEntityLink` is new because the join it represents did not exist anywhere, confirmed by
  ECP-100.
- **No circular dependencies** — confirmed above; every wrapped package is a dependency-graph leaf.
- **No duplicated services** — `ProductIntelligenceService` calls into `PricingService`,
  `Registry`/`DefinitionSet`, and `TaxonomyCatalog` rather than reimplementing any of their logic.
- **DDD followed** — Aggregate vs. Read Model separation, Resolvers as anti-corruption-layer
  adapters, `ProductValidationService` as a pure domain service.
- **Dependency inversion respected** — every resolver is constructor-injected;
  `ProductIntelligenceService` depends on `CollectionResolverPort`/`MetadataResolverPort`
  (Protocols), never a concrete Shopify client.
- **Reusable extension points exist** — `extensions.py`'s three ports, plus the resolver Protocols
  themselves (a real live-Shopify resolver is a pure addition).
- **Future AI Genome integration possible** — `AIGenomeSyncPort` + `ProductReadModel`.
- **Future ERP integration possible** — `ERPSyncPort`, consistent with `ai.attribute_distribution`'s
  existing ERP stub shape.

## Testing

`test_product_intelligence.py` and `test_resolvers.py` — hand-written `assert`-based self-checks
(no framework, this repo's established convention), run via `python -m ai.product_intelligence.test_*`.
Resolver tests load real example fixtures (`ai/ear/examples/registry.json`,
`ai/ead/examples/definitions.json`, `ai/taxonomy/examples/catalog.json`) rather than synthetic IDs —
the same standard `ai/ead/test_ead.py` set for cross-referencing real Build-002/003 data. No network
calls anywhere in the suite; `CollectionResolverPort`/`MetadataResolverPort` are exercised only via
their `Fake*` doubles.
