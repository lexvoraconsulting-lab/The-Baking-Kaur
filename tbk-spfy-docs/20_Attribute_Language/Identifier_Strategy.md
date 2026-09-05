# EAL — Identifier Strategy

## Rule

Every EAL Attribute Record gets an `attribute_id`, every Relationship Record a `relationship_id` —
both opaque, deterministic, content-hash-derived, per
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md) (the same pattern behind
`TBK_IMAGE_ID`). The `canonical_path` is the human-readable *name*; the ID is the permanent *key* —
renaming a path later never breaks a stored reference to a record already keyed by its ID.

## Implementation

```python
# ai/eal/models.py
def compute_attribute_id(canonical_path: str) -> str:
    return "EAL-" + hashlib.sha256(canonical_path.encode("utf-8")).hexdigest()[:16]

def compute_relationship_id(source_id: str, relationship_type: str, target_id: str) -> str:
    key = f"{source_id}|{relationship_type}|{target_id}"
    return "EAL-REL-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
```

Both dataclasses (`EALAttributeRecord`, `EALRelationshipRecord`) compute their ID automatically in
`__post_init__` if not supplied — see [`ai/eal/models.py`](../../ai/eal/models.py).

## Why hash-derived, not random

Two different processes computing the same attribute (same `canonical_path`) or the same
relationship (same `source_id`/`type`/`target_id`) independently arrive at the same ID with zero
coordination — no shared registry or counter needed, exactly the property
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md) Principle 3 requires.

## Runnable checks

[`test_attribute_id_is_deterministic`](../../ai/eal/test_eal.py) and
[`test_relationship_id_is_deterministic`](../../ai/eal/test_eal.py) assert same-input-same-ID and
different-input-different-ID for both functions.

## Related Standards

[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md) in full.
