# EAL — Relationship Naming

## Rule

`EALRelationshipRecord.type` (`ai/eal/models.py`) is a string field today, but its values are a
[Controlled Vocabulary](../10_Taxonomy/Controlled_Vocabulary.md), not an open string — the same
governance [Relationship_Model.md](../10_Taxonomy/Relationship_Model.md) already places on Sprint
2.1's relationship types (`ON`, `NEAR`, `PART_OF`, `MATCHES`). EAL does not define a second,
competing relationship vocabulary; `type` is where Sprint 2.1's vocabulary is carried on the wire.

## Convention

Relationship type values are **UPPER_SNAKE_CASE** verbs or verb phrases (`ON`, `NEAR`, `PART_OF`,
`MATCHES`) — deliberately distinct casing from the lowercase `snake_case` of canonical paths (see
[Naming_Convention.md](Naming_Convention.md)), so a reader can tell an Attribute path from a
Relationship type at a glance in mixed logs or payloads.

## Example

```json
{
  "relationship_id": "EAL-REL-fe42e1532d3a5459",
  "type": "ON",
  "source_id": "TBK-OBJ-topper-01",
  "target_id": "TBK-OBJ-cake-01"
}
```

(See [`knowledge_graph_node_example.json`](../../ai/eal/examples/knowledge_graph_node_example.json)
— "topper ON cake".)

## What EAL does NOT do

`ai/eal/models_pydantic.py` does not yet validate `type` against a live enum of known relationship
types — same deferral as [Enum_Standard.md](Enum_Standard.md)'s `vocabulary` field, for the same
reason: no vocabulary registry exists yet to validate against. Flagged in
[Architecture_Review_AR004.md](Architecture_Review_AR004.md). New relationship types are added the
same way a new Controlled Vocabulary term is added — additively, versioned per
[Versioning.md](../10_Taxonomy/Versioning.md) — never invented ad hoc inline in code.

## Related Standards

[Relationship_Model.md](../10_Taxonomy/Relationship_Model.md),
[Identifier_Strategy.md](Identifier_Strategy.md) (`relationship_id` derivation),
[Naming_Convention.md](Naming_Convention.md).
