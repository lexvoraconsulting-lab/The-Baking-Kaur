"""
ERP Integration - a port interface, no implementation.

WHY THIS IS A PORT (HEXAGONAL/CLEAN ARCHITECTURE TERM), NOT A CLIENT
  This engine has no real ERP system to integrate with - EAD_SPECIFICATION.md
  and the Enterprise Attribute Distribution program elsewhere in this repo
  (ai/attribute_distribution/) already treat "erp" as a stubbed target
  system for exactly the same reason: no first-contact API inspection has
  been possible. ERPPriceSyncPort defines the contract a real adapter would
  satisfy (push a calculated price out, pull an authoritative price in) so
  that when a real ERP exists, writing the adapter is additive - nothing in
  ai.pricing changes shape to accommodate it.

WHAT'S NEEDED TO COMPLETE THIS DOMAIN
  A real ERP system, its API/auth details, and a mapping between this
  engine's PricingRecord/CostResult shapes and that system's own price
  fields - none of which exist yet (matches the ai/attribute_distribution
  ERP stub's own documented blocker).
"""
from abc import ABC, abstractmethod

from ai.pricing.models import CostResult, PricingRecord


class ERPPriceSyncPort(ABC):
    @abstractmethod
    def push_price(self, record: PricingRecord) -> bool:
        """Send a locally-authored PricingRecord to the ERP system as the
        authoritative rate. Returns True on confirmed success - a concrete
        adapter decides what "confirmed" means for its own ERP."""

    @abstractmethod
    def pull_price(self, provider: str, model: str) -> PricingRecord | None:
        """Fetch the ERP's own current rate for (provider, model), if it has
        one - None, not an exception, when the ERP has no rate for that key."""


class NotConnectedERPPort(ERPPriceSyncPort):
    """The only concrete implementation until a real ERP integration is
    built. Both methods fail loudly and immediately (unlike the Pending-cost
    pattern used elsewhere in this engine) because a caller that reaches this
    class is trying to synchronize with a system that, today, doesn't exist -
    that's a configuration error to surface, not a routine "we don't know
    the cost yet" the rest of this package handles."""

    def push_price(self, record: PricingRecord) -> bool:
        raise NotImplementedError("No ERP system is connected - see this module's docstring")

    def pull_price(self, provider: str, model: str) -> PricingRecord | None:
        raise NotImplementedError("No ERP system is connected - see this module's docstring")


def calculated_cost_to_erp_fields(cost: CostResult) -> dict:
    """The one piece of real, useful logic this module can ship without an
    actual ERP: the field-mapping shape a real adapter would send, expressed
    generically (most ERPs want a flat key-value record, not this engine's
    nested dataclasses). A real adapter's push_price() would call this and
    then do whatever HTTP/SDK call its ERP needs - that call is what's
    missing, not this mapping."""
    return {
        "status": cost.status,
        "total_cost": cost.total_cost,
        "currency": cost.currency,
        "pricing_version": cost.pricing_version,
    }
