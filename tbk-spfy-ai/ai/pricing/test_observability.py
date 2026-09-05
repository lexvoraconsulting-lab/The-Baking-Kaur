#!/usr/bin/env python3
"""
Self-check for pricing observability hooks - no network calls.

USAGE
  python -m ai.pricing.test_observability
"""
from ai.pricing.models import CostResult, TokenUsage
from ai.pricing.observability import LoggingObserver, NullObserver, PricingObserver

_USAGE = TokenUsage(
    provider="acme", model="m1", input_tokens=10, output_tokens=5,
    recorded_at="2026-01-01T00:00:00Z",
)
_CALCULATED = CostResult(status="calculated", currency="USD", total_cost=1.0, pricing_version="v1")
_PENDING = CostResult.pending("no rate on file")


def test_null_observer_never_raises():
    observer = NullObserver()
    observer.on_cost_calculated(_USAGE, _CALCULATED)
    observer.on_cost_pending(_USAGE, _PENDING)
    observer.on_usage_recorded(_USAGE, _CALCULATED)


def test_base_class_hooks_are_all_noop_by_default():
    class Bare(PricingObserver):
        pass
    Bare().on_cost_calculated(_USAGE, _CALCULATED)


def test_logging_observer_does_not_raise(caplog=None):
    observer = LoggingObserver()
    observer.on_cost_calculated(_USAGE, _CALCULATED)
    observer.on_cost_pending(_USAGE, _PENDING)
    observer.on_usage_recorded(_USAGE, _CALCULATED)


def test_custom_observer_only_overrides_what_it_needs():
    events = []

    class Recorder(PricingObserver):
        def on_cost_calculated(self, usage, cost):
            events.append(("calculated", usage.provider, cost.total_cost))

    observer = Recorder()
    observer.on_cost_calculated(_USAGE, _CALCULATED)
    observer.on_cost_pending(_USAGE, _PENDING)  # inherited no-op, must not raise
    assert events == [("calculated", "acme", 1.0)]


if __name__ == "__main__":
    test_null_observer_never_raises()
    test_base_class_hooks_are_all_noop_by_default()
    test_logging_observer_does_not_raise()
    test_custom_observer_only_overrides_what_it_needs()
    print("OK")
