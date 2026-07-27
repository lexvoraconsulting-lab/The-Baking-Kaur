"""
Enterprise Attribute Language (EAL) v1 - Pydantic models.

WHY
  Runtime validation and JSON Schema generation for the EAL envelope defined
  in ai.eal.models. Field shapes are kept in lockstep with that module by
  hand (small surface, checked by ai/eal/test_eal.py) rather than generated
  from it, since dataclasses and Pydantic models solve different problems
  (typed data vs. validated wire format) and forcing one to generate the
  other would couple them unnecessarily.

USAGE
  pip install pydantic pyyaml
  python -m ai.eal.test_eal          # validates every example + regenerates schemas
"""
import re
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

EAL_VERSION = "1.0"

CANONICAL_PATH_PATTERN = re.compile(
    r"^eal\.(core|domain\.[a-z][a-z0-9_]*)\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$"
)


class ExternalIdModel(BaseModel):
    system: str
    id_type: str
    value: str


class ProvenanceModel(BaseModel):
    provider: str
    model: str
    schema_version: str
    taxonomy_version: str
    extracted_at: str
    model_version: str | None = None
    prompt_version: str | None = None


class HumanVerificationModel(BaseModel):
    status: Literal["unverified", "pending_review", "verified", "rejected", "corrected"] = "unverified"
    reviewer_id: str | None = None
    reviewed_at: str | None = None
    original_value: Any = None


class EALAttributeRecordModel(BaseModel):
    canonical_path: str
    namespace: str
    group: str
    entity_id: str
    entity_type: Literal["image", "region", "object"]
    value: Any
    value_state: Literal["present", "null", "unknown"]
    data_type: Literal[
        "string", "integer", "float", "boolean", "enum",
        "date", "datetime", "array", "object", "vector", "reference",
    ]
    provenance: ProvenanceModel
    attribute_id: str
    eal_version: str = EAL_VERSION
    unit: str | None = None
    vocabulary: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    human_verification: HumanVerificationModel = Field(default_factory=HumanVerificationModel)
    external_ids: list[ExternalIdModel] = Field(default_factory=list)

    @field_validator("canonical_path")
    @classmethod
    def _path_must_match_grammar(cls, v: str) -> str:
        if not CANONICAL_PATH_PATTERN.match(v):
            raise ValueError(
                f"canonical_path {v!r} does not match eal.<core|domain.NAME>.<group>.<attribute>"
            )
        return v

    @model_validator(mode="after")
    def _namespace_matches_path(self):
        path_namespace = ".".join(self.canonical_path.split(".")[1:-2])
        if path_namespace != self.namespace:
            raise ValueError(
                f"namespace {self.namespace!r} does not match canonical_path {self.canonical_path!r}"
            )
        return self

    @model_validator(mode="after")
    def _value_state_consistency(self):
        if self.value_state in ("null", "unknown") and self.value is not None:
            raise ValueError(
                f"value_state={self.value_state!r} requires value=None, got {self.value!r}"
            )
        return self


class EALRelationshipRecordModel(BaseModel):
    type: str
    source_id: str
    target_id: str
    provenance: ProvenanceModel
    relationship_id: str
    eal_version: str = EAL_VERSION
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
