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
    human_verification_status: Literal[
        "unverified", "pending_review", "verified", "rejected", "corrected"
    ]
    external_id: ExternalIdModel | None = None
    distribution_id: str
    distribution_version: str = DISTRIBUTION_VERSION
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    status: Literal["pending", "dry_run", "success", "failed", "conflict"] = "pending"
    notes: str | None = None

    @field_validator("registry_reference")
    @classmethod
    def _registry_reference_must_be_valid_ear_id(cls, v: str) -> str:
        if not is_valid_attribute_id(v):
            raise ValueError(f"registry_reference {v!r} does not match ^EAR-\\d{{6}}$")
        return v

    @model_validator(mode="after")
    def _notes_required_iff_failed_or_conflict(self):
        needs_notes = self.status in ("failed", "conflict")
        if needs_notes and not self.notes:
            raise ValueError(f"status={self.status!r} requires notes to be set")
        if not needs_notes and self.notes:
            raise ValueError(f"notes is set but status={self.status!r} does not require it")
        return self

    @model_validator(mode="after")
    def _external_id_required_when_resolved(self):
        if self.status in ("dry_run", "success") and self.external_id is None:
            raise ValueError(f"status={self.status!r} requires external_id to be set")
        return self
