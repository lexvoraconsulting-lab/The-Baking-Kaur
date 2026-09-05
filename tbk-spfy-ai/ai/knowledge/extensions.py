"""
Enterprise Product Knowledge Graph (Build-302) - extension ports.

WHY FIVE NEW PORTS, NOT SEVEN
  Build-302 asked for Genome and ERP-adjacent resolvers too - both already
  have a real port defined by ai.product_intelligence.extensions
  (AIGenomeSyncPort, ERPSyncPort). Reusing them directly (imported, not
  redefined) is the composition-over-duplication rule this sprint's own
  principles require; only the five ports below have no existing equivalent
  anywhere in this repo.

WHY EVERY CONCRETE CLASS RAISES NotImplementedError, NOT RETURNS EMPTY
  Unlike ai.product_intelligence's CollectionResolverPort/MetadataResolverPort
  (which have a real target - live Shopify - just not wired this sprint, so
  a Fake-returns-empty double is the honest test seam), none of these five
  has ANY real backing system anywhere in this repo: `ai/embeddings/`,
  `ai/vectordb/`, `ai/automation/`, `ai/api/` are confirmed-empty scaffold
  directories (ECP-100), no Merchant Center read integration exists
  (CLAUDE.md: shipping is Manual, decoupled), no recommendation engine
  exists, and no analytics pipeline exists. Reaching one of these classes is
  a configuration error to surface loudly, the same reasoning
  ai.pricing.domains.erp_integration.NotConnectedERPPort already established
  - not a routine "empty today" case.
"""
from abc import ABC, abstractmethod

from ai.knowledge.models import KnowledgeEdge, KnowledgeNode


class MerchantResolverPort(ABC):
    @abstractmethod
    def resolve(self, shopify_product_gid: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        """Google Merchant Center product status/feed data for this product."""


class NotConnectedMerchantResolver(MerchantResolverPort):
    def resolve(self, shopify_product_gid: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        raise NotImplementedError(
            "No Merchant Center read integration exists - shipping is Manual and decoupled "
            "from Shopify shipping profiles per CLAUDE.md; see this module's docstring"
        )


class EmbeddingResolverPort(ABC):
    @abstractmethod
    def resolve(self, node_id: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        """A vector embedding for an already-resolved node."""


class NotConnectedEmbeddingResolver(EmbeddingResolverPort):
    def resolve(self, node_id: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        raise NotImplementedError("ai/embeddings and ai/vectordb are empty scaffolds - no vector store exists yet")


class RecommendationResolverPort(ABC):
    @abstractmethod
    def resolve(self, node_id: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        """RECOMMENDED_WITH candidates for an already-resolved node."""


class NotConnectedRecommendationResolver(RecommendationResolverPort):
    def resolve(self, node_id: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        raise NotImplementedError("No recommendation engine exists yet - see this module's docstring")


class AutomationResolverPort(ABC):
    @abstractmethod
    def resolve(self, node_id: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        """GENERATED_BY / automation-run provenance for an already-resolved node."""


class NotConnectedAutomationResolver(AutomationResolverPort):
    def resolve(self, node_id: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        raise NotImplementedError("ai/automation is an empty scaffold - no automation runner exists yet")


class AnalyticsResolverPort(ABC):
    @abstractmethod
    def resolve(self, node_id: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        """Usage/performance signal nodes for an already-resolved node."""


class NotConnectedAnalyticsResolver(AnalyticsResolverPort):
    def resolve(self, node_id: str) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        raise NotImplementedError("No analytics pipeline exists yet - see this module's docstring")
