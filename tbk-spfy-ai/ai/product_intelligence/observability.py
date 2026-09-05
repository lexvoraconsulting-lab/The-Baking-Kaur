"""
Enterprise Product Intelligence Engine v1 - observability hooks.

Mirrors ai.pricing.observability's shape exactly (see that module's
docstring for the full rationale) - a small, fixed hook set with a
no-op-by-default ABC, NullObserver as the default so opting in stays
additive, and a LoggingObserver reference implementation.
"""
import logging
from abc import ABC

from ai.product_intelligence.models import ProductEvent, ProductValidationResult

_logger = logging.getLogger("ai.product_intelligence")


class ProductIntelligenceObserver(ABC):
    def on_product_resolved(self, event: ProductEvent) -> None:
        pass

    def on_product_validated(self, event: ProductEvent, result: ProductValidationResult) -> None:
        pass

    def on_slice_pending(self, event: ProductEvent) -> None:
        pass


class NullObserver(ProductIntelligenceObserver):
    """The default - see ai.pricing.observability.NullObserver's rationale."""


class LoggingObserver(ProductIntelligenceObserver):
    def on_product_resolved(self, event: ProductEvent) -> None:
        _logger.info(
            "product_intelligence.resolved product_intelligence_id=%s shopify_product_gid=%s",
            event.product_intelligence_id, event.shopify_product_gid,
        )

    def on_product_validated(self, event: ProductEvent, result: ProductValidationResult) -> None:
        level = logging.INFO if result.is_valid else logging.WARNING
        _logger.log(
            level,
            "product_intelligence.validated product_intelligence_id=%s is_valid=%s issue_count=%d",
            event.product_intelligence_id, result.is_valid, len(result.issues),
        )

    def on_slice_pending(self, event: ProductEvent) -> None:
        _logger.warning(
            "product_intelligence.slice_pending product_intelligence_id=%s payload=%s",
            event.product_intelligence_id, event.payload,
        )
