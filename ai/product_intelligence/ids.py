"""
Enterprise Product Intelligence Engine v1 - identifier strategy.

WHY CONTENT-HASH, DERIVED FROM THE REAL SHOPIFY ID
  This engine never allocates a product's primary identity - that's Shopify's
  job (the GID already is the canonical, single-allocator identifier for a
  product, the same role EAR's sequential IDs play within EAR's own single-
  registry scope). product_intelligence_id is a *secondary*, deterministic
  correlation id (uuid5 of the Shopify GID) used only for this engine's own
  internal purposes - caching, eventing, log correlation - never as a
  competing primary key. Distinct namespace UUID from every other module's
  (ai.eal, ai.ear, ai.ead, ai.attribute_distribution, ai.pricing), so no
  collision is possible even given the same input string.
"""
import uuid

PRODUCT_INTELLIGENCE_NAMESPACE_UUID = uuid.UUID("9d2b6a1e-4c7f-4a3d-8e1b-5f2c9a6d3b40")

PRODUCT_EVENT_NAMESPACE_UUID = uuid.UUID("2e5a8c3f-6d1b-4f9e-a2c7-8b3f5e1d9a60")


def compute_product_intelligence_id(shopify_product_gid: str) -> str:
    return str(uuid.uuid5(PRODUCT_INTELLIGENCE_NAMESPACE_UUID, shopify_product_gid))


def compute_event_id(event_type: str, product_intelligence_id: str, occurred_at: str) -> str:
    key = f"{event_type}|{product_intelligence_id}|{occurred_at}"
    return str(uuid.uuid5(PRODUCT_EVENT_NAMESPACE_UUID, key))
