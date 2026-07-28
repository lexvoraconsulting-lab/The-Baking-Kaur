"""
Enterprise Attribute Distribution v1 - Build-004 (Workstream: ATTR, per
docs/adr/2026-07-27-workstream-id-convention.md). Re-exports the public
surface so downstream code does `from ai.attribute_distribution import
DistributionRecord` instead of reaching into submodules. BL-1 scope: the
record model only - resolution, adapters, and distribution logic are later
backlog items. See docs/60_Enterprise_Attribute_Distribution/EAD_SPECIFICATION.md.
"""
from ai.attribute_distribution.models import (
    DISTRIBUTION_VERSION,
    DistributionRecord,
)
from ai.attribute_distribution.models_pydantic import DistributionRecordModel
from ai.attribute_distribution.ids import compute_distribution_id

__all__ = [
    "DISTRIBUTION_VERSION",
    "DistributionRecord",
    "DistributionRecordModel",
    "compute_distribution_id",
]
