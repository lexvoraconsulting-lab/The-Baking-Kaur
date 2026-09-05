"""
Enterprise Attribute Registry (EAR) v1 - plain dataclass models.

WHY
  Human/IDE-facing shape of the EAR entry, independent of any validation
  library - mirrors ai.eal.models's split. ai.ear.models_pydantic carries the
  runtime validation for the same fields. See
  docs/40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md.

WHAT EAR IS
  The canonical registry of every enterprise attribute used anywhere on the
  platform: does this attribute exist, what is its canonical identifier,
  which namespace/module owns it, which datatype does it use. EAR does not
  contain business definitions (Build-003/EAD) or real taxonomy content
  (Sprint 2.2) - both are referenced here only as opaque pointers.
"""
from dataclasses import dataclass, field
from typing import Literal

from ai.eal.models import DataType  # reused, not redefined - see plan's decision 3

from ai.ear.ids import compute_registry_uuid

EAR_VERSION = "1.0"

Status = Literal["draft", "active", "deprecated", "retired"]


@dataclass(frozen=True)
class EARAttributeEntry:
    canonical_name: str
    namespace: str
    datatype: DataType
    owner: str
    eal_reference: str
    status: Status = "draft"
    ear_version: str = EAR_VERSION
    registry_uuid: str = ""
    attribute_id: str = ""
    version: str = "v1"
    introduced_in: str = "v1"
    deprecated_in: str | None = None
    definition_reference: str | None = None
    taxonomy_references: list[str] = field(default_factory=list)
    validation_profile: str = "default"
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.registry_uuid:
            object.__setattr__(self, "registry_uuid", compute_registry_uuid(self.eal_reference))
