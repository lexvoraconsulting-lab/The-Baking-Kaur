"""
Enterprise Attribute Registry (EAR) v1 - identifier strategy.

WHY TWO DIFFERENT ID SCHEMES
  registry_uuid is content-hash-derived (uuid5), the same no-coordination-needed
  philosophy as ai.eal's compute_attribute_id - two independent processes
  computing the same eal_reference arrive at the same UUID with zero shared
  state. attribute_id ("EAR-000001") is deliberately sequential instead: EAR is
  a single, centralized catalog with exactly one allocator (this registry),
  unlike EAL records which are produced independently by many uncoordinated
  pipelines. Sequential, human-readable IDs are only safe when one source is
  the sole allocator - which is exactly what a "registry" is.
  See docs/40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md.
"""
import re
import uuid

ATTRIBUTE_ID_PATTERN = re.compile(r"^EAR-\d{6}$")

# Fixed, arbitrary namespace UUID for this registry's uuid5 derivations - a
# constant, not a secret; changing it would change every registry_uuid.
EAR_NAMESPACE_UUID = uuid.UUID("6f1c1b6e-3b1a-4e7e-9d1b-6a2f7a2d5c10")


def compute_registry_uuid(eal_reference: str) -> str:
    return str(uuid.uuid5(EAR_NAMESPACE_UUID, eal_reference))


def is_valid_attribute_id(attribute_id: str) -> bool:
    return bool(ATTRIBUTE_ID_PATTERN.match(attribute_id))


def allocate_attribute_id(existing_ids: list[str]) -> str:
    """Next sequential EAR-NNNNNN not already present in existing_ids."""
    max_seq = 0
    for existing in existing_ids:
        if is_valid_attribute_id(existing):
            max_seq = max(max_seq, int(existing.split("-")[1]))
    return f"EAR-{max_seq + 1:06d}"
