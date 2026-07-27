# EAL — Examples Walkthrough

Every file in [`ai/eal/examples/`](../../ai/eal/examples/) is validated against its model by
[`ai/eal/test_eal.py`](../../ai/eal/test_eal.py) — these are not illustrative snippets that could
silently rot, they are the fixtures the self-check actually loads.

## `vision_output_example.json`

An `EALAttributeRecord` shaped exactly as the Vision Engine would emit it: an `enum`-typed colour
attribute, `present`, AI-derived (`confidence: 0.82`), unverified. The canonical
Attribute Record example every other example is a variant of. See
[Enum_Standard.md](Enum_Standard.md), [Confidence_Standard.md](Confidence_Standard.md).

## `api_payload_example.json`

A batch shape — `{ entity_id, attributes: [...] }` — for an endpoint returning every attribute
known about one entity in one response. Its second attribute (`decoration.type`) demonstrates
`value_state: "unknown"` with `value: null` and `confidence: null`, and `human_verification.status:
"pending_review"` — the "not yet determined, flagged for a human" case. See
[Null_and_Unknown_Standard.md](Null_and_Unknown_Standard.md).

## `shopify_mapping_example.yaml` / `erp_mapping_example.yaml`

The *same* attribute (`attribute_id: EAL-fa3c900429a739de`, the colour attribute from
`vision_output_example.json`), each with a different `external_ids` entry — one joins to a Shopify
metafield, the other to an ERP SKU attribute code. Both also show `human_verification.status:
"verified"` with a `reviewer_id`/`reviewed_at` — the "a human confirmed this before it reached a
downstream system" case. See [External_ID_Standard.md](External_ID_Standard.md),
[Human_Verification_Standard.md](Human_Verification_Standard.md).

## `knowledge_graph_node_example.json`

An `EALRelationshipRecord` — "topper `ON` cake" — showing the Relationship Record shape: `type`,
`source_id`, `target_id`, its own `relationship_id`, `confidence`, `provenance`. No
`human_verification` or `external_ids` — Relationship Records don't carry either field (see
`ai/eal/models.py::EALRelationshipRecord`). See [Relationship_Naming.md](Relationship_Naming.md).

## `embedding_metadata_example.json`

An Attribute Record with `data_type: "vector"`, `namespace: "core"` (platform-level — every
domain gets the same Embeddings group, not a per-domain one), `confidence: null` (a raw embedding
has nothing to be "confident" about), and a populated `model_version` in `provenance`. See
[Data_Type_Standard.md](Data_Type_Standard.md), [Namespace_Model.md](Namespace_Model.md).

## Regenerating and re-validating

```bash
python -m ai.eal.test_eal
```

Regenerates `ai/eal/schemas/*.schema.json` from the Pydantic models, then loads and validates every
file above. See [`test_eal.py`](../../ai/eal/test_eal.py)'s module docstring.

## Related Standards

[EAL_SPECIFICATION.md](EAL_SPECIFICATION.md) (field reference these examples instantiate),
[Migration_Guide.md](Migration_Guide.md) (how `vision_output_example.json`'s shape maps onto the
Vision Engine's actual current output).
