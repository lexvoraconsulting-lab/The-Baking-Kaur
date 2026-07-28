"""
Enterprise Attribute Distribution v1 (Build-004) - Pydantic models.

WHY
  Runtime validation and JSON Schema generation for the DistributionRecord
  defined in ai.attribute_distribution.models. Reuses
  ai.eal.models_pydantic.ExternalIdModel directly (the system/id_type/value
  shape External_ID_Standard.md already defines) and
  ai.ear.ids.is_valid_attribute_id for registry_reference format - neither
  EAL nor EAR is modified or reimplemented.

USAGE
  python -m ai.attribute_distribution.test_attribute_distribution
"""
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from ai.eal.models_pydantic import ExternalIdModel
from ai.ear.ids import is_valid_attribute_id

DISTRIBUTION_VERSION = "1.0"


class DistributionRecordModel(BaseModel):
    registry_reference: str
    target_system: Literal["shopify", "erp"]
    value: object
    external_id: ExternalIdModel
    human_verification_status: Literal[
        "unverified", "pending_review", "verified", "rejected", "corrected"
    ]
    distribution_id: str
    distribution_version: str = DISTRIBUTION_VERSION
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    status: Literal["pending", "dry_run", "success", "failed", "conflict"] = "pending"
    conflict_notes: str | None = None

    @field_validator("registry_reference")
    @classmethod
    def _registry_reference_must_be_valid_ear_id(cls, v: str) -> str:
        if not is_valid_attribute_id(v):
            raise ValueError(f"registry_reference {v!r} does not match ^EAR-\\d{{6}}$")
        return v

    @model_validator(mode="after")
    def _conflict_notes_only_when_conflict(self):
        if self.status == "conflict" and not self.conflict_notes:
            raise ValueError("status='conflict' requires conflict_notes to be set")
        if self.status != "conflict" and self.conflict_notes:
            raise ValueError("conflict_notes is set but status is not 'conflict'")
        return self
