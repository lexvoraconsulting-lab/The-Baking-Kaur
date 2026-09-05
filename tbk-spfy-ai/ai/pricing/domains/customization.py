"""
Customization Costing - an interface-only extension point.

WHY NO CONCRETE COST IMPLEMENTATION SHIPS HERE
  Same rationale as recipe_costing.py / packaging.py: this project's
  products (see docs/CODING_STANDARDS.md, seo-ops/fix_seo_snippets.py) are
  already known to support photo prints, toppers, and custom messages, but
  no real per-customization cost exists anywhere in this repo to price
  them with. UnconfiguredCustomizationCostStrategy is real and tested; it
  always answers Pending until real rates are supplied.

WHAT'S NEEDED TO COMPLETE THIS DOMAIN
  A per-customization-type cost table (photo print, topper, message text,
  colour-count surcharge, ...) from real pricing decisions.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ai.pricing.models import CostResult


@dataclass(frozen=True)
class CustomizationContext:
    message_text: str | None = None
    photo_print: bool = False
    topper: str | None = None
    colour_count: int = 1
    currency: str = "USD"

    def __post_init__(self):
        if self.colour_count < 1:
            raise ValueError(f"colour_count must be >= 1, got {self.colour_count}")


class CustomizationCostStrategy(ABC):
    @abstractmethod
    def calculate(self, context: CustomizationContext) -> CostResult:
        """Never raises - returns CostResult.pending(...) for any
        customization combination it has no real cost data for."""


class UnconfiguredCustomizationCostStrategy(CustomizationCostStrategy):
    def calculate(self, context: CustomizationContext) -> CostResult:
        requested = [
            label for label, present in (
                ("message_text", bool(context.message_text)),
                ("photo_print", context.photo_print),
                ("topper", bool(context.topper)),
                (f"colour_count={context.colour_count}", context.colour_count > 1),
            ) if present
        ]
        return CostResult.pending(
            f"no customization cost data configured for: {', '.join(requested) or 'no customizations requested'}"
        )
