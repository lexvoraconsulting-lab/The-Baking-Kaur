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

WHY observer IS A THIRD OPTIONAL COLLABORATOR, NOT A NEW METHOD PARAMETER
  Same constructor-injection shape as repository/strategy (Dependency
  Inversion, not a service locator) - PricingService depends on the
  PricingObserver abstraction, never a concrete logger. Defaults to
  NullObserver so every existing caller (ai.vision.python.pipeline calls
  PricingService() with no arguments) is unaffected.
"""
from ai.pricing.models import CostResult, TokenUsage
from ai.pricing.observability import NullObserver, PricingObserver
from ai.pricing.repository import FileConfigPricingRepository, PricingRepositoryBase
from ai.pricing.strategy import CostCalculationStrategy, StandardTokenCostStrategy


class PricingService:
    def __init__(
        self,
        repository: PricingRepositoryBase | None = None,
        strategy: CostCalculationStrategy | None = None,
        observer: PricingObserver | None = None,
    ):
        self._repository = repository or FileConfigPricingRepository()
        self._strategy = strategy or StandardTokenCostStrategy()
        self._observer = observer or NullObserver()

    def calculate_cost(self, usage: TokenUsage, as_of: str | None = None) -> CostResult:
        as_of = as_of or usage.recorded_at
        try:
            pricing = self._repository.get_pricing(usage.provider, usage.model, as_of)
        except Exception as exc:  # noqa: BLE001 - deliberately broad, see module docstring
            return self._pending(usage, f"pricing lookup failed: {exc}")

        if pricing is None:
            return self._pending(
                usage,
                f"no pricing on file for provider={usage.provider!r} model={usage.model!r} as_of={as_of!r}",
            )

        try:
            result = self._strategy.calculate(usage, pricing)
        except Exception as exc:  # noqa: BLE001 - deliberately broad, see module docstring
            return self._pending(usage, f"cost calculation failed: {exc}")

        self._observer.on_cost_calculated(usage, result)
        return result

    def _pending(self, usage: TokenUsage, reason: str) -> CostResult:
        result = CostResult.pending(reason)
        self._observer.on_cost_pending(usage, result)
        return result
