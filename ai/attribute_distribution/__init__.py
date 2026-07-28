"""
Enterprise Attribute Distribution v1 - Build-004 (Workstream: ATTR, per
docs/adr/2026-07-27-workstream-id-convention.md). Re-exports the public
surface so downstream code does `from ai.attribute_distribution import
DistributionRecord` instead of reaching into submodules. Through BL-5: the
record model (BL-1), resolution (BL-2), conflict detection (BL-3), and the
Shopify/ERP Adapters (BL-4/BL-5). See
docs/60_Enterprise_Attribute_Distribution/EAD_SPECIFICATION.md.
"""
from ai.attribute_distribution.models import (
    DISTRIBUTION_VERSION,
    DistributionRecord,
)
from ai.attribute_distribution.models_pydantic import DistributionRecordModel
from ai.attribute_distribution.ids import compute_distribution_id
from ai.attribute_distribution.resolver import resolve_distribution
from ai.attribute_distribution.conflicts import CurrentDownstreamValue, detect_conflict
from ai.attribute_distribution.shopify_adapter import ShopifyAdapter
from ai.attribute_distribution.erp_adapter import ERPAdapter

__all__ = [
    "DISTRIBUTION_VERSION",
    "DistributionRecord",
    "DistributionRecordModel",
    "compute_distribution_id",
    "resolve_distribution",
    "CurrentDownstreamValue",
    "detect_conflict",
    "ShopifyAdapter",
    "ERPAdapter",
]
