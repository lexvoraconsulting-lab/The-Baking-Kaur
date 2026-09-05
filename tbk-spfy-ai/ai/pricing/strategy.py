"""
Enterprise Pricing Service v1 - cost calculation strategy (Strategy pattern).

WHY SEPARATE FROM THE REPOSITORY
  "Cost calculation must be separated from token collection" - and, just as
  importantly, separated from *pricing lookup* too. The repository answers
  "what does this provider/model charge"; the strategy answers "given that
  rate card and this usage, what's the total" - two different jobs with two
  different reasons to change (a new pricing file format vs. a provider that
  bills non-linearly, e.g. tiered/volume pricing).

WHY A STRATEGY OBJECT FOR WHAT IS TODAY ONE LINEAR FORMULA
  Every real provider (OpenAI, Anthropic, Google, OpenRouter) currently bills
  per-token linearly, so StandardTokenCostStrategy is the only concrete class
  this module ships. The seam matters anyway: a future provider with tiered
  or volume-discounted pricing (or a provider-specific promotional rate)
  becomes a second strategy class the PricingService can be pointed at per
  provider, not a growing pile of if/elif branches inside one calculator.
"""
from abc import ABC, abstractmethod

from ai.pricing.models import CostResult, PricingRecord, TokenUsage


class CostCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, usage: TokenUsage, pricing: PricingRecord) -> CostResult:
        """pricing is guaranteed non-None here - PricingService is what
        handles the "no pricing found" Pending case, not the strategy."""


class StandardTokenCostStrategy(CostCalculationStrategy):
    """Linear per-category pricing: sum(unit_price * token_count) across every
    category present in the usage, using PricingRecord.price_for() to look up
    each category's rate. A usage category with no matching rate in the
    pricing record is skipped, not an error - e.g. a provider that doesn't
    price cached tokens separately simply has no "cached" entry in
    categories, and cached tokens contribute 0 rather than failing the whole
    calculation."""

    def calculate(self, usage: TokenUsage, pricing: PricingRecord) -> CostResult:
        breakdown: dict[str, float] = {}
        for category, count in usage.category_counts().items():
            price = pricing.price_for(category)
            if price is None:
                continue
            breakdown[category] = price.cost_for(count)

        return CostResult(
            status="calculated",
            currency=pricing.currency,
            total_cost=round(sum(breakdown.values()), 8),
            breakdown=breakdown,
            pricing_id=pricing.pricing_id,
            pricing_version=pricing.version,
        )
