"""
Packaging Costing - an interface-only extension point.

WHY NO CONCRETE COST IMPLEMENTATION SHIPS HERE
  Same rationale as ai.pricing.domains.recipe_costing: real box/insert/
  ribbon/ice-pack unit costs aren't established anywhere in this repo.
  UnconfiguredPackagingCostStrategy is real and tested; it always answers
  Pending until a real per-material cost table is supplied.

WHAT'S NEEDED TO COMPLETE THIS DOMAIN
  A packaging-materials cost table (box size/type, inserts, branded ribbon,
  cold-chain inserts for delivery, ...) sourced from real supplier costs.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ai.pricing.models import CostResult


@dataclass(frozen=True)
class PackagingContext:
    box_type: str
    size: str
    add_ons: tuple[str, ...] = field(default_factory=tuple)  # e.g. ("ribbon", "cold-pack")
    currency: str = "USD"

    def __post_init__(self):
        if not self.box_type:
            raise ValueError("box_type must be non-empty")
        if not self.size:
            raise ValueError("size must be non-empty")


class PackagingCostStrategy(ABC):
    @abstractmethod
    def calculate(self, context: PackagingContext) -> CostResult:
        """Never raises - returns CostResult.pending(...) for any box type,
        size, or add-on it has no real cost data for."""


class UnconfiguredPackagingCostStrategy(PackagingCostStrategy):
    def calculate(self, context: PackagingContext) -> CostResult:
        return CostResult.pending(
            f"no packaging cost data configured for box_type={context.box_type!r} "
            f"size={context.size!r} add_ons={context.add_ons!r}"
        )
