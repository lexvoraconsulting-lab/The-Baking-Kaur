"""
Enterprise Attribute Registry (EAR) v1 - Build-002. Re-exports the public
surface so downstream modules do `from ai.ear import Registry` instead of
reaching into submodules. Resolves EAL's vocabulary/type values against real
attribute definitions once Sprint 2.2 taxonomy content exists - see
docs/40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md.
"""
from ai.ear.models import EAR_VERSION, EARAttributeEntry
from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.ear.ids import allocate_attribute_id, compute_registry_uuid, is_valid_attribute_id
from ai.ear.registry import Registry
from ai.ear.loader import load_registry
from ai.ear.exporter import export_registry, regenerate_schema
from ai.ear.api import (
    attribute_exists,
    by_namespace,
    by_owner,
    by_tag,
    get_attribute,
    get_by_eal_reference,
)

__all__ = [
    "EAR_VERSION",
    "EARAttributeEntry",
    "EARAttributeEntryModel",
    "allocate_attribute_id",
    "compute_registry_uuid",
    "is_valid_attribute_id",
    "Registry",
    "load_registry",
    "export_registry",
    "regenerate_schema",
    "attribute_exists",
    "by_namespace",
    "by_owner",
    "by_tag",
    "get_attribute",
    "get_by_eal_reference",
]
