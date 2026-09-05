"""
Enterprise Attribute Registry (EAR) v1 - the Registry container.

WHY
  Holds the whole collection of EARAttributeEntryModel entries in memory,
  keyed for O(1) lookup by the two identifiers a caller might have
  (attribute_id or eal_reference), and runs whole-registry invariants
  (ai.ear.validation) at construction time - a Registry that exists is
  guaranteed internally consistent, never a partially-checked one.
  See docs/40_Enterprise_Attribute_Registry/Registry_Model.md.
"""
from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.ear.validation import validate_registry


class Registry:
    def __init__(self, entries: list[EARAttributeEntryModel]):
        validate_registry(entries)
        self._by_attribute_id = {e.attribute_id: e for e in entries}
        self._by_eal_reference = {e.eal_reference: e for e in entries}

    @property
    def entries(self) -> list[EARAttributeEntryModel]:
        return list(self._by_attribute_id.values())

    def __len__(self) -> int:
        return len(self._by_attribute_id)

    def exists(self, attribute_id: str = None, eal_reference: str = None) -> bool:
        if attribute_id is not None:
            return attribute_id in self._by_attribute_id
        if eal_reference is not None:
            return eal_reference in self._by_eal_reference
        raise ValueError("exists() requires attribute_id or eal_reference")

    def get(self, attribute_id: str = None, eal_reference: str = None) -> EARAttributeEntryModel | None:
        if attribute_id is not None:
            return self._by_attribute_id.get(attribute_id)
        if eal_reference is not None:
            return self._by_eal_reference.get(eal_reference)
        raise ValueError("get() requires attribute_id or eal_reference")

    def all_attribute_ids(self) -> list[str]:
        return list(self._by_attribute_id.keys())
