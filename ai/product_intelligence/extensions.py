"""
Enterprise Product Intelligence Engine v1 - extension interfaces.

WHY THREE PORTS, ALL UNIMPLEMENTED
  Mirrors ai.pricing.domains.erp_integration's pattern exactly: a Port
  defines the contract a real future integration would satisfy, so building
  it later is additive - nothing in ProductIntelligenceService changes shape
  to accommodate it. Every concrete class here fails loudly
  (NotImplementedError), the same "reaching this is a configuration error,
  not a routine Pending case" reasoning ai.pricing already established -
  none of these three integrations has a real target system today:

  - AIGenomeSyncPort: no Cake Genome / AI Genome system exists yet (ECP-300
    explicitly defers it to a future sprint) - this is the seam it will
    plug into without a rewrite.
  - ERPSyncPort: same "no first-contact API inspection possible" blocker
    ai.attribute_distribution.erp_adapter and ai.pricing.domains.erp_integration
    both already document - not reimplemented here, just given the Product
    Intelligence-shaped version of the same contract.
  - ProductIntelligenceAPIPort: no HTTP/GraphQL API surface exists in this
    repo for anything AI-related yet - this is the seam a future API layer
    (Sprint 300.x or later) would implement against ProductReadModel.
"""
from abc import ABC, abstractmethod

from ai.product_intelligence.models import ProductAggregate, ProductReadModel


class AIGenomeSyncPort(ABC):
    @abstractmethod
    def push_product(self, aggregate: ProductAggregate) -> bool:
        """Send a resolved ProductAggregate to a future AI/Cake Genome
        system as its source input. Returns True on confirmed acceptance."""


class NotConnectedAIGenomePort(AIGenomeSyncPort):
    def push_product(self, aggregate: ProductAggregate) -> bool:
        raise NotImplementedError(
            "No AI Genome system exists yet - Cake Genome is explicitly out of scope "
            "for ECP-300 Sprint 300.1, see this module's docstring"
        )


class ERPSyncPort(ABC):
    @abstractmethod
    def push_product(self, aggregate: ProductAggregate) -> bool:
        """Send a resolved ProductAggregate to an ERP system as authoritative
        product data. Returns True on confirmed acceptance."""

    @abstractmethod
    def pull_product(self, shopify_product_gid: str) -> ProductReadModel | None:
        """Fetch the ERP's own view of a product, if it has one - None, not
        an exception, when the ERP has no record for that GID."""


class NotConnectedERPPort(ERPSyncPort):
    def push_product(self, aggregate: ProductAggregate) -> bool:
        raise NotImplementedError("No ERP system is connected - see this module's docstring")

    def pull_product(self, shopify_product_gid: str) -> ProductReadModel | None:
        raise NotImplementedError("No ERP system is connected - see this module's docstring")


class ProductIntelligenceAPIPort(ABC):
    @abstractmethod
    def serialize(self, read_model: ProductReadModel) -> dict:
        """Produce the wire representation a future API endpoint would
        return - deliberately not built here; no API framework or contract
        exists in this repo to build it against yet."""


class NotConnectedAPIPort(ProductIntelligenceAPIPort):
    def serialize(self, read_model: ProductReadModel) -> dict:
        raise NotImplementedError(
            "No API layer is configured - see this module's docstring"
        )
