"""
Enterprise Product Knowledge Graph (Build-302) - real resolvers.

WHY THESE FOUR ARE REAL AND NOTHING ELSE IS
  TaxonomyGraphResolver, PricingGraphResolver, SEOGraphResolver, and
  ProductGraphResolver (which composes the other three) wrap packages that
  already hold real data - ai.taxonomy, ai.pricing, and
  ai.product_intelligence's own resolved ProductAggregate/ProductReadModel.
  Every other Build-302-requested resolver (Merchant, Embedding,
  Recommendation, Automation, Analytics) has no backing system anywhere in
  this repo - see extensions.py for why those are honest ports instead.

WHY PRODUCT/PRICING/SEO ARE READ-ONLY OVER ai.product_intelligence, NOT A
SECOND EAL/EAR/EAD/TAXONOMY INTEGRATION
  ai.product_intelligence.ProductIntelligenceService already resolves a
  ProductAggregate + ProductReadModel from the real upstream stack (Phase 7's
  "Read only... Product Intelligence Engine... Never replace existing
  ownership"). Rebuilding that join here would be exactly the "duplicated
  service" Build-302's own validation checklist forbids. This module accepts
  an already-resolved ProductAggregate/ProductReadModel and projects it into
  graph nodes/edges - nothing more.
"""
from ai.knowledge.ids import compute_node_id
from ai.knowledge.models import EdgeType, KnowledgeEdge, KnowledgeNode
from ai.product_intelligence.models import ProductAggregate, ProductReadModel, ProductValidationResult
from ai.taxonomy.catalog import TaxonomyCatalog

_TAXONOMY_ENTITY_TYPE_TO_NODE_TYPE = {
    "category": "CATEGORY", "attribute_group": "ATTRIBUTE_GROUP",
    "attribute": "ATTRIBUTE", "vocabulary": "VOCABULARY", "term": "VOCABULARY_TERM",
}

_TAG_NAMESPACE_TO_NODE_TYPE_AND_PREDICATE = {
    "occasion": ("OCCASION", "HAS_OCCASION"),
    "theme": ("THEME", "HAS_THEME"),
    "flavor": ("FLAVOR", "HAS_FLAVOR"),
    "recipient": ("RECIPIENT", "HAS_RECIPIENT"),
}

_VOCABULARY_NAME_KEYWORD_TO_PREDICATE: list[tuple[str, EdgeType]] = [
    ("colour", "HAS_COLOR"), ("color", "HAS_COLOR"),
    ("style", "HAS_STYLE"), ("flavour", "HAS_FLAVOR"), ("flavor", "HAS_FLAVOR"),
    ("occasion", "HAS_OCCASION"), ("theme", "HAS_THEME"), ("recipient", "HAS_RECIPIENT"),
]


def _predicate_for_vocabulary(vocabulary_name: str) -> EdgeType:
    lowered = vocabulary_name.lower()
    for keyword, predicate in _VOCABULARY_NAME_KEYWORD_TO_PREDICATE:
        if keyword in lowered:
            return predicate
    return "RELATED_TO"


class TaxonomyGraphResolver:
    """Projects an entire TaxonomyCatalog into graph nodes/edges - not
    scoped to one product, unlike ProductGraphResolver. Reuses every
    Relationship already recorded in the catalog verbatim: predicate values
    are ai.taxonomy.RelationshipType strings, which EdgeType is a superset
    of (see models.py)."""

    def __init__(self, catalog: TaxonomyCatalog):
        self._catalog = catalog

    def resolve(self) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        nodes: list[KnowledgeNode] = []
        for category in self._catalog.categories:
            nodes.append(KnowledgeNode(
                node_type="CATEGORY", native_id=category.category_id,
                label=category.name, source_system="ai.taxonomy",
            ))
        for group in self._catalog.attribute_groups:
            nodes.append(KnowledgeNode(
                node_type="ATTRIBUTE_GROUP", native_id=group.group_id,
                label=group.name, source_system="ai.taxonomy",
            ))
        for vocabulary in self._catalog.vocabularies:
            nodes.append(KnowledgeNode(
                node_type="VOCABULARY", native_id=vocabulary.vocabulary_id,
                label=vocabulary.name, source_system="ai.taxonomy",
            ))
        for term in self._catalog.terms:
            nodes.append(KnowledgeNode(
                node_type="VOCABULARY_TERM", native_id=term.term_id, label=term.label,
                source_system="ai.taxonomy", attributes={"vocabulary_id": term.vocabulary_id},
            ))
        for attribute in self._catalog.attributes:
            nodes.append(KnowledgeNode(
                node_type="ATTRIBUTE", native_id=attribute.attribute_id,
                label=attribute.name, source_system="ai.taxonomy",
            ))

        edges: list[KnowledgeEdge] = []
        for category in self._catalog.categories:
            if category.parent_id:
                edges.append(KnowledgeEdge(
                    subject_id=compute_node_id("CATEGORY", category.category_id),
                    predicate="PART_OF",
                    object_id=compute_node_id("CATEGORY", category.parent_id),
                    source_system="ai.taxonomy",
                ))
        for relationship in self._catalog.relationships:
            subject_node_type = _TAXONOMY_ENTITY_TYPE_TO_NODE_TYPE[relationship.subject_type]
            object_node_type = _TAXONOMY_ENTITY_TYPE_TO_NODE_TYPE[relationship.object_type]
            edges.append(KnowledgeEdge(
                subject_id=compute_node_id(subject_node_type, relationship.subject_id),
                predicate=relationship.relationship_type,
                object_id=compute_node_id(object_node_type, relationship.object_id),
                source_system="ai.taxonomy",
            ))
        return nodes, edges


class PricingGraphResolver:
    """Given an already-resolved ProductAggregate, projects its PricingSlice
    into a PRICING node + a HAS_PRICE edge - never recomputes cost, only
    represents what ai.pricing (via ai.product_intelligence) already
    calculated."""

    def resolve(self, aggregate: ProductAggregate) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        cost = aggregate.pricing.cost_result
        if cost is None:
            return [], []
        product_node_id = compute_node_id("PRODUCT", aggregate.identity.shopify_product_gid)
        pricing_native_id = f"{aggregate.identity.shopify_product_gid}:price"
        pricing_node = KnowledgeNode(
            node_type="PRICING", native_id=pricing_native_id,
            label=f"{cost.total_cost} {cost.currency}" if cost.total_cost is not None else "pending",
            source_system="ai.pricing",
            attributes={"status": cost.status, "total_cost": cost.total_cost, "currency": cost.currency},
        )
        edge = KnowledgeEdge(
            subject_id=product_node_id, predicate="HAS_PRICE",
            object_id=pricing_node.node_id, source_system="ai.pricing",
        )
        return [pricing_node], [edge]


class SEOGraphResolver:
    """Given an already-resolved ProductReadModel, projects its SEO fields
    into an SEO node + an OPTIMIZED_FOR edge - real data (ai.product_intelligence
    already reads Shopify's seo{title,description}), never fabricated."""

    def resolve(self, read_model: ProductReadModel) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        if read_model.seo_title is None and read_model.seo_description is None:
            return [], []
        product_node_id = compute_node_id("PRODUCT", read_model.shopify_product_gid)
        seo_native_id = f"{read_model.shopify_product_gid}:seo"
        seo_node = KnowledgeNode(
            node_type="SEO", native_id=seo_native_id, label=read_model.seo_title or "",
            source_system="shopify", attributes={"seo_description": read_model.seo_description},
        )
        edge = KnowledgeEdge(
            subject_id=product_node_id, predicate="OPTIMIZED_FOR",
            object_id=seo_node.node_id, source_system="shopify",
        )
        return [seo_node], [edge]


class ProductGraphResolver:
    """The main commerce-side resolver: PRODUCT node + HAS_CATEGORY/
    HAS_COLLECTION/HAS_OCCASION/HAS_THEME/HAS_FLAVOR/HAS_RECIPIENT/HAS_COLOR/
    HAS_STYLE edges, composing PricingGraphResolver and SEOGraphResolver
    rather than duplicating their logic. taxonomy_catalog is DI'd only to
    resolve a matched Term's Vocabulary name (for the HAS_COLOR/HAS_STYLE/...
    predicate choice) - never to re-derive taxonomy data ai.product_intelligence
    already resolved."""

    def __init__(self, taxonomy_catalog: TaxonomyCatalog):
        self._catalog = taxonomy_catalog
        self._pricing_resolver = PricingGraphResolver()
        self._seo_resolver = SEOGraphResolver()

    def resolve(
        self, aggregate: ProductAggregate, read_model: ProductReadModel,
        validation: ProductValidationResult | None = None,
    ) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        product_node = KnowledgeNode(
            node_type="PRODUCT", native_id=aggregate.identity.shopify_product_gid,
            label=read_model.title or aggregate.identity.handle, source_system="shopify",
            attributes=(
                {"status": read_model.status, "product_type": read_model.product_type}
                if validation is None else
                {"status": read_model.status, "product_type": read_model.product_type,
                 "is_valid": validation.is_valid, "issue_count": len(validation.issues)}
            ),
        )
        nodes = [product_node]
        edges: list[KnowledgeEdge] = []

        for category in aggregate.taxonomy.categories:
            edges.append(KnowledgeEdge(
                subject_id=product_node.node_id, predicate="HAS_CATEGORY",
                object_id=compute_node_id("CATEGORY", category.category_id),
                source_system="ai.taxonomy",
            ))
        for term in aggregate.taxonomy.terms:
            vocabulary = self._catalog.get_vocabulary(term.vocabulary_id)
            predicate = _predicate_for_vocabulary(vocabulary.name) if vocabulary else "RELATED_TO"
            edges.append(KnowledgeEdge(
                subject_id=product_node.node_id, predicate=predicate,
                object_id=compute_node_id("VOCABULARY_TERM", term.term_id),
                source_system="ai.taxonomy", confidence=None,
            ))
        for handle in read_model.collection_handles:
            collection_node = KnowledgeNode(
                node_type="COLLECTION", native_id=handle, label=handle, source_system="shopify",
            )
            nodes.append(collection_node)
            edges.append(KnowledgeEdge(
                subject_id=product_node.node_id, predicate="HAS_COLLECTION",
                object_id=collection_node.node_id, source_system="shopify",
            ))
        for tag in read_model.tags:
            if ":" not in tag:
                continue
            namespace, _, value = tag.partition(":")
            mapping = _TAG_NAMESPACE_TO_NODE_TYPE_AND_PREDICATE.get(namespace)
            if mapping is None:
                continue
            node_type, predicate = mapping
            tag_node = KnowledgeNode(node_type=node_type, native_id=value, label=value, source_system="shopify")
            nodes.append(tag_node)
            edges.append(KnowledgeEdge(
                subject_id=product_node.node_id, predicate=predicate,
                object_id=tag_node.node_id, source_system="shopify",
            ))

        pricing_nodes, pricing_edges = self._pricing_resolver.resolve(aggregate)
        seo_nodes, seo_edges = self._seo_resolver.resolve(read_model)
        nodes.extend(pricing_nodes)
        nodes.extend(seo_nodes)
        edges.extend(pricing_edges)
        edges.extend(seo_edges)
        return nodes, edges
