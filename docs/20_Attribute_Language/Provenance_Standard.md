# EAL — Provenance Standard

## Rule

Every Attribute and Relationship Record carries a `provenance` object
(`ai/eal/models.py::Provenance`):

```python
provider: str            # e.g. "ollama"
model: str                # e.g. "qwen2.5vl:3b"
schema_version: str        # taxonomy schema version, e.g. "v1"
taxonomy_version: str       # taxonomy version, e.g. "v1"
extracted_at: str            # ISO 8601 timestamp
model_version: str | None    # optional
prompt_version: str | None   # optional
```

This is the direct extension of the Vision Engine's existing
[`Provenance`-shaped fields](../../ai/vision/python/pipeline.py) (`schema_version`,
`taxonomy_version` already exist on `VisionResult`) into a reusable, standalone object every future
module's records carry, not just Vision's.

## Why `schema_version`/`taxonomy_version` are required, not optional

Per [VIG-005](../00_Governance/VIG-005-Versioning-Standard.md), every derived record must be
traceable to the taxonomy/schema version active when it was produced — `provenance` is where that
traceability lives at the individual-attribute level, mirroring
[VIG-003](../00_Governance/VIG-003-Data-Principles.md) Principle 4 (lineage).

## Related Standards

[VIG-003](../00_Governance/VIG-003-Data-Principles.md),
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md),
[Confidence_Standard.md](Confidence_Standard.md).
