"""
Enterprise Pricing Service v1 - observability hooks.

WHY AN OBSERVER, NOT JUST LOGGING CALLS SCATTERED IN service.py
  "Observable" needs to mean more than "prints something" - a future
  consumer (metrics dashboard, alerting on repeated Pending results, a trace
  exporter) needs a stable extension point, not scraped log lines. PricingService
  calls a small, fixed set of hooks; what happens inside those hooks (log,
  emit a metric, push a trace span) is entirely the observer's business.

WHY BACKWARD COMPATIBLE BY DEFAULT
  PricingService's existing constructor signature (repository=, strategy=)
  must keep working unchanged - ai/vision/python/pipeline.py already calls
  PricingService() with no arguments. NullObserver is the default, so
  opting into observability is additive, never required.
"""
import logging
from abc import ABC

from ai.pricing.models import CostResult, TokenUsage

_logger = logging.getLogger("ai.pricing")


class PricingObserver(ABC):
    """Every hook has a no-op default so a concrete observer only needs to
    override the events it actually cares about - the same "implement only
    what you use" shape as Python's own logging.Handler."""

    def on_cost_calculated(self, usage: TokenUsage, cost: CostResult) -> None:
        pass

    def on_cost_pending(self, usage: TokenUsage, cost: CostResult) -> None:
        pass

    def on_usage_recorded(self, usage: TokenUsage, cost: CostResult) -> None:
        pass


class NullObserver(PricingObserver):
    """The default - all three hooks are already no-ops via the base class;
    this subclass exists so `NullObserver()` reads as an explicit choice at
    call sites, not an accidental omission."""


class LoggingObserver(PricingObserver):
    """Reference implementation: structured log lines via the stdlib
    logging module (this repo adds no logging-framework dependency
    anywhere else, so none is added here either). A future MetricsObserver
    or TracingObserver satisfies the same PricingObserver contract."""

    def on_cost_calculated(self, usage: TokenUsage, cost: CostResult) -> None:
        _logger.info(
            "pricing.calculated provider=%s model=%s total_cost=%s currency=%s pricing_version=%s",
            usage.provider, usage.model, cost.total_cost, cost.currency, cost.pricing_version,
        )

    def on_cost_pending(self, usage: TokenUsage, cost: CostResult) -> None:
        _logger.warning(
            "pricing.pending provider=%s model=%s reason=%s",
            usage.provider, usage.model, cost.reason,
        )

    def on_usage_recorded(self, usage: TokenUsage, cost: CostResult) -> None:
        _logger.info(
            "pricing.usage_recorded provider=%s model=%s input_tokens=%s output_tokens=%s status=%s",
            usage.provider, usage.model, usage.input_tokens, usage.output_tokens, cost.status,
        )
