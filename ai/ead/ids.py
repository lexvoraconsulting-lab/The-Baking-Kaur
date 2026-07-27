"""
Enterprise Attribute Definitions (EAD) v1 - identifier strategy.

WHY
  Same content-hash-derived, no-coordination-needed philosophy as
  ai.ear.ids.compute_registry_uuid - every platform entity gets a permanent
  identifier (VIG-006), EAD is no exception. One Definition per EAR
  attribute_id, so definition_id is derived from registry_reference rather
  than needing its own separate allocator.
  See docs/50_Enterprise_Attribute_Definitions/EAD_SPECIFICATION.md.
"""
import uuid

# Fixed, arbitrary namespace UUID for this module's uuid5 derivations -
# distinct from ai.ear.ids.EAR_NAMESPACE_UUID so a definition_id and a
# registry_uuid can never collide even if both were derived from the same
# input string.
EAD_NAMESPACE_UUID = uuid.UUID("9b6f2b6a-3a1e-4e6a-8c1e-7b2f6a2d5c20")


def compute_definition_id(registry_reference: str) -> str:
    return str(uuid.uuid5(EAD_NAMESPACE_UUID, registry_reference))
