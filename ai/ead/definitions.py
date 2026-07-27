"""
Enterprise Attribute Definitions (EAD) v1 - the DefinitionSet container.

WHY
  Holds the whole collection of EADDefinitionModel entries in memory, keyed
  by registry_reference (one Definition per EAR attribute), and runs
  whole-set invariants (ai.ead.validation) at construction time - mirrors
  ai/ear/registry.py::Registry exactly.
  See docs/50_Enterprise_Attribute_Definitions/Definition_Model.md.
"""
from ai.ead.models_pydantic import EADDefinitionModel
from ai.ead.validation import validate_definition_set


class DefinitionSet:
    def __init__(self, definitions: list[EADDefinitionModel]):
        validate_definition_set(definitions)
        self._by_registry_reference = {d.registry_reference: d for d in definitions}

    @property
    def definitions(self) -> list[EADDefinitionModel]:
        return list(self._by_registry_reference.values())

    def __len__(self) -> int:
        return len(self._by_registry_reference)

    def get(self, registry_reference: str) -> EADDefinitionModel | None:
        return self._by_registry_reference.get(registry_reference)

    def all_registry_references(self) -> list[str]:
        return list(self._by_registry_reference.keys())
