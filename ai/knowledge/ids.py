"""
Enterprise Product Knowledge Graph (Build-302) - identifier strategy.

WHY node_id IS NAMESPACING, NOT HASHING
  Every entity this graph represents already has a canonical identifier
  somewhere else in the platform (a Shopify GID, a TAX-CAT-NNNNNN, an
  EAR-NNNNNN, a TBK_IMAGE_ID). Hashing that ID again would create a second,
  opaque identity for the same thing - exactly the "competing system of
  record" VIG-003 Principle 2 forbids. Namespacing (`f"{node_type}:{native_id}"`)
  keeps the real ID legible inside the graph ID, at the cost of a slightly
  longer string - a fair trade for a debugging surface this graph will be
  queried through constantly.

WHY edge_id IS uuid5, LIKE EVERY OTHER MODULE'S RELATIONSHIP ID
  An edge has no independent natural identifier - (subject, predicate,
  object) is its natural key, the same shape ai.eal.compute_relationship_id
  and ai.taxonomy's relationship_id already use. Distinct namespace UUID
  from every other module's.
"""
import uuid

EDGE_NAMESPACE_UUID = uuid.UUID("3f7c2a9e-5b1d-4e8f-9a2c-6d4b1f8e3c70")


def compute_node_id(node_type: str, native_id: str) -> str:
    return f"{node_type}:{native_id}"


def compute_edge_id(subject_id: str, predicate: str, object_id: str) -> str:
    key = f"{subject_id}|{predicate}|{object_id}"
    return str(uuid.uuid5(EDGE_NAMESPACE_UUID, key))
