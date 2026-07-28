"""
Enterprise Attribute Distribution v1 (Build-004) - identifier strategy.

WHY
  Same content-hash-derived, no-coordination-needed philosophy as
  ai.ear.ids.compute_registry_uuid / ai.ead.ids.compute_definition_id - every
  platform entity gets a permanent identifier (VIG-006). A distribution_id is
  derived from (registry_reference, target_system) rather than registry_reference
  alone, since one EAR attribute can be distributed to more than one target
  system (Shopify and ERP) - each is a distinct distribution attempt with its
  own identity. See docs/60_Enterprise_Attribute_Distribution/EAD_SPECIFICATION.md.
"""
import uuid

# Fixed, arbitrary namespace UUID for this module's uuid5 derivations - distinct
# from ai.ear.ids.EAR_NAMESPACE_UUID and ai.ead.ids.EAD_NAMESPACE_UUID so a
# distribution_id can never collide with a registry_uuid or definition_id even
# given the same input string.
DISTRIBUTION_NAMESPACE_UUID = uuid.UUID("2f7c8e1a-4d3b-4a5c-9e2f-1a6b8c3d7e40")


def compute_distribution_id(registry_reference: str, target_system: str) -> str:
    key = f"{registry_reference}|{target_system}"
    return str(uuid.uuid5(DISTRIBUTION_NAMESPACE_UUID, key))
