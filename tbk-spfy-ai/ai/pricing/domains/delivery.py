"""
Delivery Pricing - a real, generic pricing domain.

WHY THIS DOESN'T HARDCODE ANY OF THE BAKING KAUR'S ACTUAL DELIVERY FEES
  CLAUDE.md confirms this store's delivery is distance-based with a minimum
  order, within a ~15km radius - real facts about how delivery pricing here
  is *structured*. The actual current fee schedule (Rs. per band) isn't
  established anywhere this engine can verify, so - same "never invent" rule
  as every other domain in this package - TieredDistanceDeliveryStrategy
  takes the band table and minimum order threshold as caller-supplied
  configuration, not literals in this file. This module encodes the
  *shape* of the real policy (bands, a minimum-order gate), not invented
  numbers.

WHY A DISTANCE BEYOND EVERY BAND RETURNS Pending, NOT AN ERROR OR A GUESS
  A delivery request outside the configured service area has no correct
  fee to report - Pending is the honest answer, the same principle
  ai.pricing.service.PricingService already applies to an unmapped model.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ai.pricing.models import CostResult


@dataclass(frozen=True)
class DistanceBand:
    max_distance_km: float
    fee: float

    def __post_init__(self):
        if self.max_distance_km <= 0:
            raise ValueError(f"max_distance_km must be > 0, got {self.max_distance_km}")
        if self.fee < 0:
            raise ValueError(f"fee must be >= 0, got {self.fee}")


@dataclass(frozen=True)
class DeliveryContext:
    distance_km: float
    order_subtotal: float
    currency: str = "USD"

    def __post_init__(self):
        if self.distance_km < 0:
            raise ValueError(f"distance_km must be >= 0, got {self.distance_km}")
        if self.order_subtotal < 0:
            raise ValueError(f"order_subtotal must be >= 0, got {self.order_subtotal}")


class DeliveryPricingStrategy(ABC):
    @abstractmethod
    def calculate(self, context: DeliveryContext) -> CostResult:
        """Returns CostResult.pending(...) - never raises - for a distance
        outside every configured band, or an order below the configured
        minimum."""


@dataclass(frozen=True)
class TieredDistanceDeliveryStrategy(DeliveryPricingStrategy):
    """bands are checked in ascending max_distance_km order; the first band
    whose max_distance_km covers the actual distance applies (so bands don't
    need to be pre-sorted by the caller). minimum_order_subtotal is optional
    - pass None to skip that check entirely for a caller that doesn't need
    it."""
    bands: tuple[DistanceBand, ...] = field(default_factory=tuple)
    minimum_order_subtotal: float | None = None

    def calculate(self, context: DeliveryContext) -> CostResult:
        if self.minimum_order_subtotal is not None and context.order_subtotal < self.minimum_order_subtotal:
            return CostResult.pending(
                f"order_subtotal={context.order_subtotal} is below the minimum "
                f"{self.minimum_order_subtotal} required for delivery"
            )

        for band in sorted(self.bands, key=lambda b: b.max_distance_km):
            if context.distance_km <= band.max_distance_km:
                return CostResult(
                    status="calculated",
                    currency=context.currency,
                    total_cost=band.fee,
                    breakdown={"delivery_fee": band.fee},
                    pricing_version=f"distance-band-{band.max_distance_km}km",
                )

        return CostResult.pending(
            f"distance_km={context.distance_km} exceeds every configured delivery band "
            f"(furthest band: {max((b.max_distance_km for b in self.bands), default=0)}km)"
        )
