"""
Enterprise Attribute Definitions (EAD) v1 - Pydantic models.

WHY
  Runtime validation and JSON Schema generation for the EAD entry defined in
  ai.ead.models. Reuses ai.eal.models_pydantic.ExternalIdModel directly for
  shopify_mapping/erp_mapping (the system/id_type/value shape
  External_ID_Standard.md already defines) and ai.ear.ids.is_valid_attribute_id
  for registry_reference format - neither EAL nor EAR is modified or
  reimplemented.

USAGE
  pip install pydantic pyyaml
  python -m ai.ead.test_ead          # validates every example + regenerates schema
"""
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from ai.eal.models_pydantic import ExternalIdModel
from ai.ear.ids import is_valid_attribute_id

EAD_VERSION = "1.0"


class SearchBehaviourModel(BaseModel):
    searchable: bool = True
    facetable: bool = False
    boost: float = Field(default=1.0, ge=0.0)
    notes: str | None = None


class ConfidenceExpectationsModel(BaseModel):
    minimum_confidence: float = Field(ge=0.0, le=1.0)
    typical_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    notes: str | None = None

    @model_validator(mode="after")
    def _typical_not_below_minimum(self):
        if self.typical_confidence is not None and self.typical_confidence < self.minimum_confidence:
            raise ValueError(
                f"typical_confidence={self.typical_confidence!r} is below "
                f"minimum_confidence={self.minimum_confidence!r}"
            )
        return self


class EADDefinitionModel(BaseModel):
    registry_reference: str
    display_name: str
    business_definition: str
    purpose: str
    examples: list[str] = Field(min_length=1)
    vision_guidance: str
    ai_guidance: str
    mapping_guidance: str
    confidence_expectations: ConfidenceExpectationsModel
    definition_id: str
    ead_version: str = EAD_VERSION
    allowed_values: list[str] | None = None
    search_behaviour: SearchBehaviourModel = Field(default_factory=SearchBehaviourModel)
    knowledge_graph_reference: str | None = None
    shopify_mapping: ExternalIdModel | None = None
    erp_mapping: ExternalIdModel | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("registry_reference")
    @classmethod
    def _registry_reference_must_be_valid_ear_id(cls, v: str) -> str:
        if not is_valid_attribute_id(v):
            raise ValueError(f"registry_reference {v!r} does not match ^EAR-\\d{{6}}$")
        return v
