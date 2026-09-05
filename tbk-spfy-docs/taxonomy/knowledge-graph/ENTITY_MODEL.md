# Product Knowledge Graph — Entity Model (Build-302)

Scope note: this document covers `ai.knowledge.models.NodeType` — the Knowledge Graph's *code*
implementation. It is not a competing design document. Read
[docs/10_Taxonomy/Entity_Model.md](10_Taxonomy/Entity_Model.md) first — that Sprint 2.1 document
designed the image-side half of this schema; this page only documents how it was implemented and
what was added on the commerce side. See [KNOWLEDGE_GRAPH.md](KNOWLEDGE_GRAPH.md) for the full
architecture.

## Image-side node types (implements Entity_Model.md verbatim)

| NodeType | Source Entity_Model.md entity | Resolved by (this sprint) |
|---|---|---|
| `IMAGE` | Image | not yet — no resolver reads `ai.eal` image entities into the graph this sprint |
| `REGION` | Region | not yet |
| `OBJECT` | Object | not yet |
| `DECORATION` | Decoration | not yet |
| `WRITING` | Writing | not yet |
| `ATTRIBUTE` | Attribute | via `TaxonomyGraphResolver` (taxonomy-defined attributes only) |
| `GENOME_ATTRIBUTE` | Genome Attribute | not yet — no promotion/verification pipeline exists yet |
| `AI_OBSERVATION` | AI Observation | not yet |
| `HUMAN_REVIEW` | Human Review | not yet |
| `CATEGORY` | Category | `TaxonomyGraphResolver`, `ProductGraphResolver` |
| `ATTRIBUTE_GROUP` | Attribute Group | `TaxonomyGraphResolver` |
| `VOCABULARY` | (implicit — Term's parent grouping) | `TaxonomyGraphResolver` |
| `VOCABULARY_TERM` | Controlled Vocabulary Term | `TaxonomyGraphResolver`, `ProductGraphResolver` |
| `BUSINESS_ENTITY` | Business Entity | represented concretely as `PRODUCT` (see below) |

`VOCABULARY` has no entry in Entity_Model.md's own table (only "Controlled Vocabulary Term" is
listed as an entity) — added here because a Term's Vocabulary needs its own addressable node once
represented in a real graph. Not a departure from Entity_Model.md's intent, just a code-level
completion of it.

The `IMAGE`/`REGION`/`OBJECT`/`DECORATION`/`WRITING`/`GENOME_ATTRIBUTE`/`AI_OBSERVATION`/
`HUMAN_REVIEW` node types exist in the vocabulary (schema-complete, ready for a future resolver)
but have no resolver this sprint — `ai.vision`'s pipeline does not yet emit structured EAL records
into any queryable store (Build-008, "Vision structured extraction," is not started). Building a
resolver for these today would mean fabricating data with no real source; the vocabulary exists so
that work is additive when Build-008 ships, per the "extension points, not implementations" rule
this whole platform follows.

## Commerce-side node types (Build-302's own scope)

Entity_Model.md explicitly left this out: *"The taxonomy does not model Business Entities' internal
structure; it only defines how an Image relates to one."* This is that structure.

| NodeType | Represents | Resolved by |
|---|---|---|
| `PRODUCT` | A Shopify product — the concrete Business Entity | `ProductGraphResolver` (real) |
| `VARIANT` | A Shopify product variant | none — `ai.product_intelligence.ProductReadModel` has no variant slice yet; flagged in [GRAPH_ROADMAP.md](GRAPH_ROADMAP.md) |
| `COLLECTION` | A Shopify collection | `ProductGraphResolver`, from `read_model.collection_handles` |
| `OCCASION` / `THEME` / `RECIPIENT` / `FLAVOR` | A value from the `occasion:`/`theme:`/`recipient:`/`flavor:` Shopify tag namespace ([ENTERPRISE_COLLECTION_ARCHITECTURE.md](ENTERPRISE_COLLECTION_ARCHITECTURE.md)) | `ProductGraphResolver`, from `read_model.tags` |
| `INGREDIENT` / `RECIPE` | Recipe costing inputs | none — `ai.pricing.domains.recipe_costing` already documents why no real ingredient cost data exists yet |
| `PACKAGING` | Packaging cost/type | none — `ai.pricing.domains.packaging` is interface-only |
| `DELIVERY` | A delivery zone/band | none — `ai.pricing.domains.delivery` has real cost logic but no enumerable zone list to resolve as nodes |
| `PRICING` | A product's resolved cost | `PricingGraphResolver` (real, composed into `ProductGraphResolver`) |
| `INVENTORY` | Stock level | none — no inventory read path in this repo's `ai/` layer |
| `MERCHANT` | Google Merchant Center listing | none — see `extensions.MerchantResolverPort` |
| `SEO` | A product's `seo{title,description}` | `SEOGraphResolver` (real, composed into `ProductGraphResolver`) |
| `SCHEMA` | schema.org structured data | none — lives in `snippets/structured-data.liquid` (theme layer), outside this Python package's reach |
| `VIDEO` | A product video | none — no video pipeline exists |
| `REVIEW` | A customer review | none, deliberately — 0 verified reviews exist (CLAUDE.md); this node type must never be populated with fabricated data |
| `CUSTOMER_INTENT` | A search/browse intent signal | none — no analytics pipeline exists |
| `RECOMMENDATION` | A recommended-product edge target | none — see `extensions.RecommendationResolverPort` |
| `AI_GENOME` | A future Cake Genome record | none — see `ai.product_intelligence.extensions.AIGenomeSyncPort` (reused, not redefined) |
| `EMBEDDING` | A vector embedding | none — `ai/embeddings`, `ai/vectordb` are empty scaffolds |
| `AUTOMATION` | An automation run record | none — `ai/automation` is an empty scaffold |
| `ANALYTICS` | A usage/performance signal | none — see `extensions.AnalyticsResolverPort` |

"Knowledge Entity" (from the original Build-302 brief) is not a separate `NodeType` — every node
already *is* a knowledge entity by construction; adding a literal member for that would be a
vacuous, duplicate category.

## Identity

Every `KnowledgeNode.node_id` is `f"{node_type}:{native_id}"`, where `native_id` is the entity's
**real, pre-existing identifier** — a Shopify GID, a `TAX-CAT-NNNNNN`, an `EAR-NNNNNN`. No node type
gets a newly-invented, hash-derived identity; see `ai/knowledge/ids.py` and ADR 0009 point 5.
