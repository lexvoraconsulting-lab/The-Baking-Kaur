"""
Corporate & Negotiated Pricing - a real, generic pricing domain.

WHY THIS IS DIFFERENT MATH FROM discounts_promotions.py, NOT A DUPLICATE
  A discount is "list price minus X%." Corporate/negotiated pricing is
  usually a flat, contract-specific unit rate that doesn't reference a list
  price at all (a bulk-order client pays $N/unit, full stop, however that
  number was negotiated) - graduated by volume tier the same shape as a
  volume discount, but the tier stores an absolute rate, not a percentage.

WHY "NO RATE ON FILE" RETURNS Pending, THE SAME AS ai.pricing.service
  A corporate account with no negotiated rate captured yet is exactly the
  "pricing unavailable" case ai.pricing.models.CostResult.pending() already
  models - reusing it here means every caller of any pricing domain in this
  engine handles "we don't know the cost yet" the same one way.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ai.pricing.models import CostResult


@dataclass(frozen=True)
class CorporateRateTier:
    min_quantity: int
    unit_price: float

    def __post_init__(self):
        if self.min_quantity < 1:
            raise ValueError(f"min_quantity must be >= 1, got {self.min_quantity}")
        if self.unit_price < 0:
            raise ValueError(f"unit_price must be >= 0, got {self.unit_price}")


@dataclass(frozen=True)
class CorporatePricingContext:
    account_id: str
    quantity: int
    currency: str = "USD"

    def __post_init__(self):
        if not self.account_id:
            raise ValueError("account_id must be non-empty")
        if self.quantity < 1:
            raise ValueError(f"quantity must be >= 1, got {self.quantity}")


class CorporatePricingStrategy(ABC):
    @abstractmethod
    def calculate(self, context: CorporatePricingContext) -> CostResult:
        """Returns CostResult.pending(...) - never raises - when the
        account/quantity combination has no negotiated rate on file."""


@dataclass(frozen=True)
class TieredCorporateRateStrategy(CorporatePricingStrategy):
    """The caller supplies the actual negotiated tier table per account -
    e.g. rates_by_account={"acct-123": (CorporateRateTier(50, 8.5),
    CorporateRateTier(200, 7.0))}. Applies the highest-min_quantity tier the
    order actually qualifies for (the best negotiated rate available at that
    volume), not the first match in the table."""
    rates_by_account: dict[str, tuple[CorporateRateTier, ...]] = field(default_factory=dict)

    def calculate(self, context: CorporatePricingContext) -> CostResult:
        tiers = self.rates_by_account.get(context.account_id)
        if not tiers:
            return CostResult.pending(f"no negotiated rate table for account={context.account_id!r}")

        applicable = [t for t in tiers if context.quantity >= t.min_quantity]
        if not applicable:
            return CostResult.pending(
                f"account={context.account_id!r} has a rate table, but none of its tiers "
                f"apply at quantity={context.quantity}"
            )

        best = max(applicable, key=lambda t: t.min_quantity)
        total = round(best.unit_price * context.quantity, 8)
        return CostResult(
            status="calculated",
            currency=context.currency,
            total_cost=total,
            breakdown={"unit_price": best.unit_price, "quantity": context.quantity},
            pricing_version=f"corporate-tier-{best.min_quantity}+",
        )
