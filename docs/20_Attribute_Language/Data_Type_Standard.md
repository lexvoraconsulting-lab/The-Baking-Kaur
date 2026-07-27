# EAL — Data Type Standard

## The 11 canonical types

```python
DataType = Literal[
    "string", "integer", "float", "boolean", "enum",
    "date", "datetime", "array", "object", "vector", "reference",
]
```

(`ai/eal/models.py`, enforced identically in `ai/eal/models_pydantic.py`.)

| Type | Meaning | Example |
|---|---|---|
| `string` | Free text | An unstructured description fragment. |
| `integer` / `float` | Numbers | A count; a confidence-adjacent score. |
| `boolean` | True/false | Has visible text: yes/no. |
| `enum` | A value from a [Controlled Vocabulary](../10_Taxonomy/Controlled_Vocabulary.md) — see [Enum_Standard.md](Enum_Standard.md). | `shape: round`. |
| `date` / `datetime` | ISO 8601 strings | Extraction timestamps live in `provenance`, not here — this type is for domain data (e.g. an event date on a themed cake). |
| `array` | An ordered list of same-typed values | Multiple colours present. |
| `object` | A nested structure | Reserved for compound attributes; not used by any Build-001 example, kept for forward compatibility. |
| `vector` | A numeric embedding | See [`embedding_metadata_example.json`](../../ai/eal/examples/embedding_metadata_example.json). |
| `reference` | A pointer to another entity's ID | Not a `Relationship Record` (see [Relationship_Naming.md](Relationship_Naming.md)) — a lightweight same-record pointer, e.g. an Attribute that names which `Category` ID classified it. |

No 12th type is added without a real consumer needing it — this list is closed by
[VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4, not by convention alone.

## Related Standards

[Enum_Standard.md](Enum_Standard.md), [Units_Standard.md](Units_Standard.md).
