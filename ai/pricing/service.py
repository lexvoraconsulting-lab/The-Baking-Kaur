"""
Enterprise Pricing Service v1 - orchestration.

WHY THIS IS THE ONLY CLASS CALLERS SHOULD IMPORT
  Everything else in this package (repository, strategy, models) is a moving
  part PricingService assembles. A caller that just wants "usage in, cost
  out, never an exception" should depend on this one class and its
  constructor's two swappable collaborators - not reach into
  ai.pricing.repository or ai.pricing.strategy directly.

WHY calculate_cost NEVER RAISES
  "If pricing is unavailable, record token usage and mark cost as Pending
  Calculation rather than failing execution" is a hard requirement, not a
  best-effort one - a corrupt config file, an unmapped model, or a future
  strategy bug must never be able to take down whatever business logic
  called this (e.g. the vision pipeline finishing a real, billable API call).
  Every failure mode collapses to CostResult.pending(reason), never an
  exception escaping this method.
"""
from ai.pricing.models import CostResult, TokenUsage
from ai.pricing.repository import FileConfigPricingRepository, PricingRepositoryBase
from ai.pricing.strategy import CostCalculationStrategy, StandardTokenCostStrategy


class PricingService:
    def __init__(
        self,
        repository: PricingRepositoryBase | None = None,
        strategy: CostCalculationStrategy | None = None,
    ):
        self._repository = repository or FileConfigPricingRepository()
        self._strategy = strategy or StandardTokenCostStrategy()

    def calculate_cost(self, usage: TokenUsage, as_of: str | None = None) -> CostResult:
        as_of = as_of or usage.recorded_at
        try:
            pricing = self._repository.get_pricing(usage.provider, usage.model, as_of)
        except Exception as exc:  # noqa: BLE001 - deliberately broad, see module docstring
            return CostResult.pending(f"pricing lookup failed: {exc}")

        if pricing is None:
            return CostResult.pending(
                f"no pricing on file for provider={usage.provider!r} model={usage.model!r} as_of={as_of!r}"
            )

        try:
            return self._strategy.calculate(usage, pricing)
        except Exception as exc:  # noqa: BLE001 - deliberately broad, see module docstring
            return CostResult.pending(f"cost calculation failed: {exc}")
