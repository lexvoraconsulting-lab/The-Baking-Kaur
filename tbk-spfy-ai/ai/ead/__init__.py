"""
Enterprise Attribute Definitions (EAD) v1 - Build-003. Re-exports the public
surface so downstream modules do `from ai.ead import DefinitionSet` instead
of reaching into submodules. The semantic definition layer over EAR
(Build-002) attributes - see
docs/50_Enterprise_Attribute_Definitions/EAD_SPECIFICATION.md.
"""
from ai.ead.models import (
    EAD_VERSION,
    ConfidenceExpectations,
    EADDefinition,
    SearchBehaviour,
)
from ai.ead.models_pydantic import (
    ConfidenceExpectationsModel,
    EADDefinitionModel,
    SearchBehaviourModel,
)
from ai.ead.ids import compute_definition_id
from ai.ead.definitions import DefinitionSet
from ai.ead.loader import load_definitions
from ai.ead.exporter import export_definitions, regenerate_schema
from ai.ead.api import (
    by_display_name,
    by_tag_in_metadata,
    cross_reference_against_registry,
    get_by_registry_reference,
)

__all__ = [
    "EAD_VERSION",
    "ConfidenceExpectations",
    "EADDefinition",
    "SearchBehaviour",
    "ConfidenceExpectationsModel",
    "EADDefinitionModel",
    "SearchBehaviourModel",
    "compute_definition_id",
    "DefinitionSet",
    "load_definitions",
    "export_definitions",
    "regenerate_schema",
    "by_display_name",
    "by_tag_in_metadata",
    "cross_reference_against_registry",
    "get_by_registry_reference",
]
