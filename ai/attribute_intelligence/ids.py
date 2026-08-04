"""
Enterprise Attribute Intelligence Engine (Build-303) - identifier strategy.

WHY CONTENT-HASH, DISTINCT NAMESPACE PER ID KIND
  Same "many uncoordinated producers" reasoning as ai.eal/ai.pricing (see
  those modules' ids.py): observations arrive from independent sources with
  no shared allocator, so two identical observations (same attribute,
  subject, source, timestamp) must resolve to the same observation_id with
  no coordination. Distinct namespace UUIDs from every other module's, so
  no id can collide across packages even given the same input string.
"""
import uuid

OBSERVATION_NAMESPACE_UUID = uuid.UUID("6e2b8f4a-3c7d-4e1f-9b5a-8d2f6c4e1a90")
RESOLUTION_NAMESPACE_UUID = uuid.UUID("1a9d5e3f-7b2c-4f8a-9e6d-3c1f8b4a2d70")


def compute_observation_id(registry_reference: str, subject_id: str, source: str, observed_at: str) -> str:
    key = f"{registry_reference}|{subject_id}|{source}|{observed_at}"
    return str(uuid.uuid5(OBSERVATION_NAMESPACE_UUID, key))


def compute_resolution_id(registry_reference: str, subject_id: str, resolved_at: str) -> str:
    key = f"{registry_reference}|{subject_id}|{resolved_at}"
    return str(uuid.uuid5(RESOLUTION_NAMESPACE_UUID, key))
