# Product Knowledge Graph — Relationship Model (Build-302)

Scope note: this document covers `ai.knowledge.models.EdgeType` — the Knowledge Graph's *code*
implementation of typed edges. Read
[docs/10_Taxonomy/Relationship_Model.md](10_Taxonomy/Relationship_Model.md) first — its "typed
edges, not a generic graph" principle and its confidence/provenance requirement are implemented
here verbatim, not redesigned. See [KNOWLEDGE_GRAPH.md](KNOWLEDGE_GRAPH.md) for the full
architecture.

## Reused verbatim from `ai.taxonomy.models.RelationshipType`

`IS_A`, `PART_OF`, `BELONGS_TO`, `USES`, `RELATED_TO`, `PAIRS_WITH`, `CONTRASTS_WITH`,
`COMPLEMENTS`, `AVAILABLE_IN`, `SUITABLE_FOR` — every string value `ai.taxonomy`'s frozen Build-005
`Relationship` model already defines. `test_edge_type_is_superset_of_taxonomy_relationship_type`
asserts `EdgeType` is a strict superset of these, so a future edit to either Literal that breaks
compatibility fails a test instead of silently diverging.

## Reused from Relationship_Model.md's Object-to-Object vocabulary

`ON`, `NEAR`, `MATCHES` — Relationship_Model.md's own example set for typed Object-to-Object edges
("topper ON cake", "balloon NEAR cake"). No resolver emits these yet (no Object-level EAL data
exists to resolve from — see [ENTITY_MODEL.md](ENTITY_MODEL.md)'s image-side table) but the
predicate vocabulary is ready for when one does.

## New in Build-302 (commerce-side predicates)

| EdgeType | Emitted by | Meaning |
|---|---|---|
| `HAS_CATEGORY` | `ProductGraphResolver` | Product → a taxonomy Category |
| `HAS_COLLECTION` | `ProductGraphResolver` | Product → a Shopify Collection |
| `HAS_OCCASION` / `HAS_THEME` / `HAS_FLAVOR` / `HAS_RECIPIENT` | `ProductGraphResolver` | Product → a tag-namespace or vocabulary-matched value |
| `HAS_STYLE` / `HAS_COLOR` | `ProductGraphResolver` | Product → a taxonomy Term, predicate chosen from the Term's Vocabulary name |
| `HAS_INGREDIENT` / `HAS_RECIPE` / `HAS_VARIANT` / `HAS_SCHEMA` / `HAS_IMAGE` / `HAS_VIDEO` / `HAS_EMBEDDING` / `HAS_GENOME` | none yet | reserved — no resolver has real data to emit these (see ENTITY_MODEL.md) |
| `HAS_PRICE` | `PricingGraphResolver` | Product → its resolved Pricing node |
| `SIMILAR_TO` | none (computed on demand) | `GraphQueryEngine.find_similar` computes this as a query result, not a stored edge — see [GRAPH_QUERY_ENGINE.md](GRAPH_QUERY_ENGINE.md) |
| `RECOMMENDED_WITH` | none | reserved for a future `RecommendationResolverPort` implementation |
| `DELIVERED_BY` | none | reserved — no enumerable delivery-zone entity exists to resolve as a node yet |
| `OPTIMIZED_FOR` | `SEOGraphResolver` | Product → its SEO node |
| `INDEXED_BY` | none | reserved for a future search-index integration |
| `GENERATED_BY` | none | reserved for `AutomationResolverPort` |
| `VALIDATED_BY` | none | reserved — real semantic fit is Genome Attribute → Human Review (Relationship_Model.md), not built yet; today's product-level validation outcome is instead carried as `PRODUCT` node attributes (`is_valid`, `issue_count`), not a separate edge |

## Confidence and provenance

Every `KnowledgeEdge` carries `confidence: float | None` and `source_system: str`, matching
Relationship_Model.md's requirement that a relationship is evidence until verified, exactly like an
Attribute. A deterministic join this sprint produces (e.g. Product → its own resolved Category) has
no meaningful confidence score and is left `None` — it isn't AI-derived evidence to verify, it's a
direct lookup. A future AI-derived edge (a real `SIMILAR_TO`/`RECOMMENDED_WITH` stored edge) would
carry a real confidence score per VIG-007 Principles 1–2.
