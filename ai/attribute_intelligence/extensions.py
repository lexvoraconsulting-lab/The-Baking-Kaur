"""
Enterprise Attribute Intelligence Engine (Build-303) - extension ports.

WHY MERCHANT AND GENOME ARE PORTS, NOT REAL ADAPTERS
  Same reasoning as ai.knowledge.extensions (Build-302): no Google Merchant
  Center read integration exists anywhere in this repo (CLAUDE.md - shipping
  is Manual, decoupled), and no AI/Cake Genome system exists yet (both
  ECP-300 and Build-302 deferred it explicitly). Reaching one of these
  classes is a configuration error to surface loudly, not a routine "empty
  today" case - ai.pricing.domains.erp_integration's established pattern.
"""
from abc import ABC, abstractmethod

from ai.attribute_intelligence.models import AttributeObservation


class MerchantAttributeSourcePort(ABC):
    @abstractmethod
    def fetch(self, subject_id: str, observed_at: str) -> list[AttributeObservation]:
        """Google Merchant Center attribute signals (e.g. merchant-side
        category mapping) for this subject."""


class NotConnectedMerchantAttributeSource(MerchantAttributeSourcePort):
    def fetch(self, subject_id: str, observed_at: str) -> list[AttributeObservation]:
        raise NotImplementedError(
            "No Merchant Center read integration exists - shipping is Manual and decoupled "
            "from Shopify shipping profiles per CLAUDE.md; see this module's docstring"
        )


class GenomeAttributeSourcePort(ABC):
    @abstractmethod
    def fetch(self, subject_id: str, observed_at: str) -> list[AttributeObservation]:
        """Cake Genome attribute signals for this subject."""


class NotConnectedGenomeAttributeSource(GenomeAttributeSourcePort):
    def fetch(self, subject_id: str, observed_at: str) -> list[AttributeObservation]:
        raise NotImplementedError(
            "No AI/Cake Genome system exists yet - explicitly deferred by both ECP-300 "
            "and Build-302; see this module's docstring"
        )
