"""
Enterprise Attribute Definitions (EAD) v1 - query surface.

WHY
  Read-only questions this build answers, plus one optional integration
  check: does every Definition's registry_reference actually resolve in a
  real EAR Registry. cross_reference_against_registry only runs when a
  caller supplies an ai.ear.Registry - it is not required to load or use a
  DefinitionSet standalone, keeping ai/ead/ decoupled from needing an EAR
  file present at every call site.
"""
from ai.ead.definitions import DefinitionSet
from ai.ead.models_pydantic import EADDefinitionModel
from ai.ear.registry import Registry


def get_by_registry_reference(definition_set: DefinitionSet, registry_reference: str) -> EADDefinitionModel | None:
    return definition_set.get(registry_reference)


def by_display_name(definition_set: DefinitionSet, display_name: str) -> list[EADDefinitionModel]:
    return [d for d in definition_set.definitions if d.display_name == display_name]


def by_tag_in_metadata(definition_set: DefinitionSet, key: str, value: str) -> list[EADDefinitionModel]:
    return [d for d in definition_set.definitions if d.metadata.get(key) == value]


def cross_reference_against_registry(definition_set: DefinitionSet, ear_registry: Registry) -> list[str]:
    """Returns registry_reference values with no matching entry in ear_registry.
    Empty list means every Definition resolves - a real Build-002/Build-003
    integration check, without EAD depending on EAR being loaded at all."""
    return [
        ref for ref in definition_set.all_registry_references()
        if not ear_registry.exists(attribute_id=ref)
    ]
