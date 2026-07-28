"""
Enterprise Attribute Distribution v1 (Build-004) - plain dataclass models.

WHY
  Human/IDE-facing shape of the DistributionRecord, independent of any
  validation library - mirrors ai.eal/ai.ear/ai.ead's split.
  ai.attribute_distribution.models_pydantic carries the runtime validation
  for the same fields. See
  docs/60_Enterprise_Attribute_Distribution/EAD_SPECIFICATION.md.

WHAT THIS BUILD IS (BL-1 scope: models only)
  Build-004 (Workstream: ATTR, per ADR 0006). The write path from a validated
  EALAttributeRecord, enriched by its EAD (Build-003) Definition's mapping
  guidance, to a target system (Shopify or ERP). This module defines the
  record of one such attempted write - it does not yet resolve, distribute,
  or write anything (later backlog items).
"""
from dataclasses import dataclass
from typing import Any, Literal

from ai.eal.models import ExternalId, VerificationStatus

from ai.attribute_distribution.ids import compute_distribution_id

DISTRIBUTION_VERSION = "1.0"

TargetSystem = Literal["shopify", "erp"]
DistributionStatus = Literal["pending", "dry_run", "success", "failed", "conflict"]


@dataclass(frozen=True)
class DistributionRecord:
    registry_reference: str
    target_system: TargetSystem
    value: Any
    human_verification_status: VerificationStatus
    external_id: ExternalId | None = None
    distribution_id: str = ""
    distribution_version: str = DISTRIBUTION_VERSION
    confidence: float | None = None
    status: DistributionStatus = "pending"
    notes: str | None = None

    def __post_init__(self):
        if not self.distribution_id:
            object.__setattr__(
                self,
                "distribution_id",
                compute_distribution_id(self.registry_reference, self.target_system),
            )
