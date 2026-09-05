"""
Enterprise Product Knowledge Graph v1 (Build-302) - the semantic relationship
layer connecting existing enterprise subsystems (Product Intelligence,
Pricing, Taxonomy, SEO) without duplicating their ownership. Not a database -
see docs/PRODUCT_KNOWLEDGE_GRAPH.md and
docs/adr/2026-08-02-product-knowledge-graph.md.
"""
from ai.knowledge.extensions import (
    AnalyticsResolverPort, AutomationResolverPort, EmbeddingResolverPort,
    MerchantResolverPort, NotConnectedAnalyticsResolver, NotConnectedAutomationResolver,
    NotConnectedEmbeddingResolver, NotConnectedMerchantResolver, NotConnectedRecommendationResolver,
    RecommendationResolverPort,
)
from ai.knowledge.graph import KnowledgeGraph
from ai.knowledge.ids import compute_edge_id, compute_node_id
from ai.knowledge.inference import InferenceChain, InferenceChainRunner, InferenceResult
from ai.knowledge.models import (
    KNOWLEDGE_GRAPH_VERSION, GraphHealthReport, GraphIssue, KnowledgeEdge, KnowledgeNode,
)
from ai.knowledge.observability import (
    KnowledgeGraphObserver, LoggingObserver, NullObserver, compute_health_report,
)
from ai.knowledge.query import GraphQueryEngine, SimilarityResult
from ai.knowledge.resolvers import (
    PricingGraphResolver, ProductGraphResolver, SEOGraphResolver, TaxonomyGraphResolver,
)
from ai.knowledge.service import KnowledgeGraphService

__all__ = [
    "KNOWLEDGE_GRAPH_VERSION",
    "AnalyticsResolverPort",
    "AutomationResolverPort",
    "EmbeddingResolverPort",
    "GraphHealthReport",
    "GraphIssue",
    "GraphQueryEngine",
    "InferenceChain",
    "InferenceChainRunner",
    "InferenceResult",
    "KnowledgeEdge",
    "KnowledgeGraph",
    "KnowledgeGraphObserver",
    "KnowledgeGraphService",
    "KnowledgeNode",
    "LoggingObserver",
    "MerchantResolverPort",
    "NotConnectedAnalyticsResolver",
    "NotConnectedAutomationResolver",
    "NotConnectedEmbeddingResolver",
    "NotConnectedMerchantResolver",
    "NotConnectedRecommendationResolver",
    "NullObserver",
    "PricingGraphResolver",
    "ProductGraphResolver",
    "RecommendationResolverPort",
    "SEOGraphResolver",
    "SimilarityResult",
    "TaxonomyGraphResolver",
    "compute_edge_id",
    "compute_health_report",
    "compute_node_id",
]
