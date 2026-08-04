# Product Knowledge Graph — Resolvers (Build-302)

`ai.knowledge.resolvers` (real) and `ai.knowledge.extensions` (ports) — see
[KNOWLEDGE_GRAPH.md](KNOWLEDGE_GRAPH.md) for the full architecture and why the real/port split
exists.

## Real resolvers (wrap already-built engines, never re-derive their logic)

| Resolver | Wraps | Emits |
|---|---|---|
| `TaxonomyGraphResolver` | `ai.taxonomy.TaxonomyCatalog` | Every Category/AttributeGroup/Vocabulary/Term/Attribute as a node; category `PART_OF` hierarchy edges; every already-recorded taxonomy Relationship, verbatim |
| `ProductGraphResolver` | `ai.product_intelligence.ProductAggregate` + `ProductReadModel` (+ optional `ProductValidationResult`) | The `PRODUCT` node and every commerce-side edge (`HAS_CATEGORY`, `HAS_COLLECTION`, `HAS_OCCASION`/`HAS_THEME`/`HAS_FLAVOR`/`HAS_RECIPIENT`, `HAS_COLOR`/`HAS_STYLE`); composes the next two |
| `PricingGraphResolver` | `ai.pricing` (via the aggregate's already-resolved `PricingSlice`) | `PRICING` node + `HAS_PRICE` edge |
| `SEOGraphResolver` | Shopify `seo{title,description}` (via the read model) | `SEO` node + `OPTIMIZED_FOR` edge |

None of these resolvers reaches into EAL/EAR/EAD or raw Shopify data directly — every one accepts
an already-resolved `ai.product_intelligence`/`ai.taxonomy` object as input. This is the
"Product Intelligence remains canonical" validation rule enforced structurally, not just by
convention.

## Ports (no real backing system exists in this repo)

| Port | Why it's a port, not an implementation |
|---|---|
| `MerchantResolverPort` | No Google Merchant Center read integration exists; CLAUDE.md confirms shipping is Manual, decoupled from Shopify shipping profiles |
| `EmbeddingResolverPort` | `ai/embeddings/`, `ai/vectordb/` are confirmed-empty scaffold directories |
| `RecommendationResolverPort` | No recommendation engine exists anywhere in this repo |
| `AutomationResolverPort` | `ai/automation/` is a confirmed-empty scaffold directory |
| `AnalyticsResolverPort` | No analytics pipeline exists anywhere in this repo |

Every concrete `NotConnected*` class raises `NotImplementedError` — a caller reaching one is hitting
a configuration error, not a routine "empty today" case, the same reasoning
`ai.pricing.domains.erp_integration.NotConnectedERPPort` already established. **AI Genome and ERP
are not redefined here** — `ai.knowledge` reuses `ai.product_intelligence.extensions.AIGenomeSyncPort`
and `ERPSyncPort` directly, per this sprint's own composition-over-duplication principle.

## Why `IMAGE`/`REGION`/`OBJECT`/`GENOME_ATTRIBUTE`/`AI_OBSERVATION`/`HUMAN_REVIEW` have no resolver
this sprint

These `NodeType`s exist (see [ENTITY_MODEL.md](ENTITY_MODEL.md)) but `ai.vision`'s pipeline does not
yet emit structured, queryable EAL records anywhere a resolver could read from — Build-008 ("Vision
structured extraction") has not started. Writing a resolver against data that doesn't exist would
mean fabricating it; the node types stay in the vocabulary, ready, until Build-008 ships.
