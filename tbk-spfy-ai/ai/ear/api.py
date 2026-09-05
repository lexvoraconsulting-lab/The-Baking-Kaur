"""
Enterprise Attribute Registry (EAR) v1 - query surface.

WHY
  The read-only questions EAR is meant to answer (Build-002's stated goal):
  does this attribute exist, what is its canonical identifier, which
  namespace/module owns it, which taxonomy/EAD entry does it reference.
  Every function here reads from an already-validated Registry - it performs
  no I/O and no cross-system resolution (no real taxonomy or EAD content
  exists yet to resolve against; see ai.ear.validation's module docstring).
"""
from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.ear.registry import Registry


def attribute_exists(registry: Registry, canonical_name: str, namespace: str) -> bool:
    return any(
        e.canonical_name == canonical_name and e.namespace == namespace
        for e in registry.entries
    )


def get_attribute(registry: Registry, attribute_id: str) -> EARAttributeEntryModel | None:
    return registry.get(attribute_id=attribute_id)


def get_by_eal_reference(registry: Registry, eal_reference: str) -> EARAttributeEntryModel | None:
    return registry.get(eal_reference=eal_reference)


def by_namespace(registry: Registry, namespace: str) -> list[EARAttributeEntryModel]:
    return [e for e in registry.entries if e.namespace == namespace]


def by_owner(registry: Registry, owner: str) -> list[EARAttributeEntryModel]:
    return [e for e in registry.entries if e.owner == owner]


def by_tag(registry: Registry, tag: str) -> list[EARAttributeEntryModel]:
    return [e for e in registry.entries if tag in e.tags]
