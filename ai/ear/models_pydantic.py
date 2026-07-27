"""
Enterprise Attribute Registry (EAR) v1 - Pydantic models.

WHY
  Runtime validation and JSON Schema generation for the EAR entry defined in
  ai.ear.models. Field shapes are kept in lockstep with that module by hand
  (small surface, checked by ai/ear/test_ear.py), mirroring ai.eal's dataclass
  / Pydantic split rationale.

USAGE
  pip install pydantic pyyaml
  python -m ai.ear.test_ear          # validates every example + regenerates schema
"""
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from ai.eal.models_pydantic import CANONICAL_PATH_PATTERN  # reused, not reimplemented

EAR_VERSION = "1.0"

DataTypeLiteral = Literal[
    "string", "integer", "float", "boolean", "enum",
    "date", "datetime", "array", "object", "vector", "reference",
]


class EARAttributeEntryModel(BaseModel):
    canonical_name: str
    namespace: str
    datatype: DataTypeLiteral
    owner: str
    eal_reference: str
    status: Literal["draft", "active", "deprecated", "retired"] = "draft"
    ear_version: str = EAR_VERSION
    registry_uuid: str
    attribute_id: str
    version: str = "v1"
    introduced_in: str = "v1"
    deprecated_in: str | None = None
    definition_reference: str | None = None
    taxonomy_references: list[str] = Field(default_factory=list)
    validation_profile: str = "default"
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _eal_reference_must_match_grammar(self):
        if not CANONICAL_PATH_PATTERN.match(self.eal_reference):
            raise ValueError(
                f"eal_reference {self.eal_reference!r} does not match "
                f"eal.<core|domain.NAME>.<group>.<attribute>"
            )
        return self

    @model_validator(mode="after")
    def _namespace_matches_eal_reference(self):
        path_namespace = ".".join(self.eal_reference.split(".")[1:-2])
        if path_namespace != self.namespace:
            raise ValueError(
                f"namespace {self.namespace!r} does not match eal_reference "
                f"{self.eal_reference!r}"
            )
        return self

    @model_validator(mode="after")
    def _deprecated_in_matches_status(self):
        is_deprecated_status = self.status in ("deprecated", "retired")
        has_deprecated_in = self.deprecated_in is not None
        if is_deprecated_status != has_deprecated_in:
            raise ValueError(
                f"status={self.status!r} and deprecated_in={self.deprecated_in!r} are "
                f"inconsistent - deprecated_in is required if and only if status is "
                f"'deprecated' or 'retired'"
            )
        return self
