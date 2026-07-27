"""
Enterprise Attribute Definitions (EAD) v1 - plain dataclass models.

WHY
  Human/IDE-facing shape of the EAD entry, independent of any validation
  library - mirrors ai.eal.models / ai.ear.models's split. ai.ead.models_pydantic
  carries the runtime validation for the same fields. See
  docs/50_Enterprise_Attribute_Definitions/EAD_SPECIFICATION.md.

WHAT EAD IS
  Build-003. The semantic definition layer over EAR (Build-002) attributes:
  business meaning, purpose, display name, examples, vision/AI guidance,
  allowed values, mapping guidance, search behaviour, confidence expectations,
  and pointers to the Knowledge Graph, Shopify, and ERP. EAD does not
  implement taxonomy or a validation engine - those stay opaque pointers
  here. See docs/adr/2026-07-27-build-003-renumbering.md for why Build-003
  means this and not Enterprise Attribute Distribution (now Build-004).
"""
from dataclasses import dataclass, field
from typing import Any

from ai.eal.models import ExternalId

from ai.ead.ids import compute_definition_id

EAD_VERSION = "1.0"


@dataclass(frozen=True)
class SearchBehaviour:
    searchable: bool = True
    facetable: bool = False
    boost: float = 1.0
    notes: str | None = None


@dataclass(frozen=True)
class ConfidenceExpectations:
    minimum_confidence: float
    typical_confidence: float | None = None
    notes: str | None = None


@dataclass(frozen=True)
class EADDefinition:
    registry_reference: str
    display_name: str
    business_definition: str
    purpose: str
    examples: list[str]
    vision_guidance: str
    ai_guidance: str
    mapping_guidance: str
    confidence_expectations: ConfidenceExpectations
    definition_id: str = ""
    ead_version: str = EAD_VERSION
    allowed_values: list[str] | None = None
    search_behaviour: SearchBehaviour = field(default_factory=SearchBehaviour)
    knowledge_graph_reference: str | None = None
    shopify_mapping: ExternalId | None = None
    erp_mapping: ExternalId | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.definition_id:
            object.__setattr__(
                self, "definition_id", compute_definition_id(self.registry_reference)
            )
