"""
Enterprise Product Intelligence Engine v1 - event construction.

WHY A FACTORY FUNCTION, NOT A CLASS
  ProductEvent (models.py) is the data shape; build_event is the one place
  that computes its deterministic event_id (ai.product_intelligence.ids) and
  fills occurred_at from the caller - this engine makes no wall-clock calls
  itself, matching ai.pricing.TokenUsage's recorded_at convention. No event
  bus exists anywhere in this repo yet (confirmed absent during ECP-100), so
  "emit" today means "hand this to an injected ProductIntelligenceObserver",
  not publish to a queue - see service.py.
"""
from ai.product_intelligence.ids import compute_event_id
from ai.product_intelligence.models import ProductEvent, ProductEventType


def build_event(
    event_type: ProductEventType,
    product_intelligence_id: str,
    shopify_product_gid: str,
    occurred_at: str,
    payload: dict | None = None,
) -> ProductEvent:
    return ProductEvent(
        event_id=compute_event_id(event_type, product_intelligence_id, occurred_at),
        event_type=event_type,
        product_intelligence_id=product_intelligence_id,
        shopify_product_gid=shopify_product_gid,
        occurred_at=occurred_at,
        payload=payload or {},
    )
