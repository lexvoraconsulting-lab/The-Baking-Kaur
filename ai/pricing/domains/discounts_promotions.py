"""
Discounts & Promotions - a real, generic pricing domain.

WHY THIS ONE IS FULLY IMPLEMENTED, NOT JUST AN INTERFACE
  "10% off," "flat Rs.100 off," "buy 3 get 1 free," and "spend more, save
  more" are universal retail concepts - correct for any business, any
  currency, any catalogue, without needing a single Baking Kaur-specific
  fact. The caller always supplies the actual base amount and the actual
  rule parameters (percentage, tiers, ...); this module only implements the
  arithmetic, the same separation of concerns as ai.pricing.strategy
  (the strategy doesn't know or guess a token's real-world price either).

WHY DiscountResult REUSES ai.pricing.models.CostResult INSTEAD OF A NEW TYPE
  "Reuse existing abstractions, avoid duplicate code" - CostResult already
  models exactly what a discount produces: a total, a currency, a
  category-by-category breakdown, and a status. total_cost here means
  "the amount after discount," breakdown carries "original" and "discount"
  (negative) entries. A second CostResult-shaped type would just be
  CostResult with the fields renamed.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ai.pricing.models import CostResult


@dataclass(frozen=True)
class DiscountContext:
    base_amount: float
    currency: str = "USD"
    quantity: int = 1

    def __post_init__(self):
        if self.base_amount < 0:
            raise ValueError(f"base_amount must be >= 0, got {self.base_amount}")
        if self.quantity < 1:
            raise ValueError(f"quantity must be >= 1, got {self.quantity}")


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, context: DiscountContext) -> CostResult:
        """Never raises for valid input, never returns a negative total_cost
        (a discount can reduce a price to 0, never below it)."""


def _result(context: DiscountContext, discount_amount: float, label: str) -> CostResult:
    discount_amount = min(discount_amount, context.base_amount)  # never discount past 0
    final = round(context.base_amount - discount_amount, 8)
    return CostResult(
        status="calculated",
        currency=context.currency,
        total_cost=final,
        breakdown={"original": context.base_amount, "discount": -round(discount_amount, 8)},
        pricing_version=label,
    )


@dataclass(frozen=True)
class PercentageDiscountStrategy(DiscountStrategy):
    percentage: float  # 0-100

    def __post_init__(self):
        if not 0 <= self.percentage <= 100:
            raise ValueError(f"percentage must be in [0, 100], got {self.percentage}")

    def apply(self, context: DiscountContext) -> CostResult:
        return _result(
            context, context.base_amount * (self.percentage / 100), f"percentage-{self.percentage}"
        )


@dataclass(frozen=True)
class FlatAmountDiscountStrategy(DiscountStrategy):
    amount: float

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError(f"amount must be >= 0, got {self.amount}")

    def apply(self, context: DiscountContext) -> CostResult:
        return _result(context, self.amount, f"flat-{self.amount}")


@dataclass(frozen=True)
class VolumeTier:
    min_quantity: int
    percentage: float  # 0-100

    def __post_init__(self):
        if self.min_quantity < 1:
            raise ValueError(f"min_quantity must be >= 1, got {self.min_quantity}")
        if not 0 <= self.percentage <= 100:
            raise ValueError(f"percentage must be in [0, 100], got {self.percentage}")


@dataclass(frozen=True)
class TieredVolumeDiscountStrategy(DiscountStrategy):
    """The caller supplies the actual tier table - e.g. [VolumeTier(10, 5),
    VolumeTier(50, 10)] means 5% off at 10+ units, 10% off at 50+. Applies
    the best (highest-percentage) tier the quantity actually qualifies for,
    not just the first match, so tier order in the list doesn't matter."""
    tiers: tuple[VolumeTier, ...] = field(default_factory=tuple)

    def apply(self, context: DiscountContext) -> CostResult:
        applicable = [t for t in self.tiers if context.quantity >= t.min_quantity]
        if not applicable:
            return _result(context, 0.0, "no-tier-applies")
        best = max(applicable, key=lambda t: t.percentage)
        return _result(context, context.base_amount * (best.percentage / 100), f"tier-{best.min_quantity}+")


@dataclass(frozen=True)
class BuyXGetYFreeStrategy(DiscountStrategy):
    """buy=3, get_free=1 means every 4th unit (at context.quantity's implied
    per-unit price = base_amount / quantity) is free. Requires quantity > 1
    to mean anything - a single-item context always yields a 0 discount."""
    buy: int
    get_free: int

    def __post_init__(self):
        if self.buy < 1:
            raise ValueError(f"buy must be >= 1, got {self.buy}")
        if self.get_free < 1:
            raise ValueError(f"get_free must be >= 1, got {self.get_free}")

    def apply(self, context: DiscountContext) -> CostResult:
        if context.quantity <= 1:
            return _result(context, 0.0, "buy-x-get-y-not-applicable")
        unit_price = context.base_amount / context.quantity
        group_size = self.buy + self.get_free
        free_units = (context.quantity // group_size) * self.get_free
        return _result(context, free_units * unit_price, f"buy{self.buy}get{self.get_free}free")
