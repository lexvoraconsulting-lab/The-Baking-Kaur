# EAR — Examples Walkthrough

Both files in [`ai/ear/examples/`](../../ai/ear/examples/) hold the same logical 5-entry registry
— one in JSON, one in YAML — validated by [`test_ear.py`](../../ai/ear/test_ear.py), including a
direct equality check between the two
([`test_json_and_yaml_examples_are_equal`](../../ai/ear/test_ear.py)).

## `EAR-000001` — `primary_colour`

`status: "active"`, `namespace: "domain.bakery"`, `datatype: "enum"`, resolving
`eal.domain.bakery.colour.primary` — the same colour attribute already used throughout
[EAL's own examples](../20_Attribute_Language/Examples.md). Shows the ordinary, fully-active case.

## `EAR-000002` — `decoration_type`

`status: "draft"` — an attribute registered but not yet promoted to active use, resolving
`eal.domain.bakery.decoration.type`.

## `EAR-000003` — `image_vector`

`namespace: "core"` (platform-level, not domain-scoped), `datatype: "vector"`,
`owner: "embedding_engine"` — shows a platform-level attribute distinct from a domain one, and a
non-`"vision_engine"` owner.

## `EAR-000004` — `primary_shape`

`status: "deprecated"`, `deprecated_in: "v1"` — demonstrates the deprecated-lifecycle case and its
paired `deprecated_in` requirement (see [Versioning.md](Versioning.md)).

## `EAR-000005` — `primary_material`

`status: "retired"`, `deprecated_in: "v1"` — the terminal lifecycle state, same `deprecated_in`
requirement as `deprecated`.

## Regenerating and re-validating

```bash
python -m ai.ear.test_ear
```

Regenerates `ai/ear/schemas/ear.schema.json` from `EARAttributeEntryModel`, then validates both
example registries, whole-registry invariants, ID determinism/format, and import/export
round-tripping. See [`test_ear.py`](../../ai/ear/test_ear.py)'s module docstring.

## Related Standards

[EAR_SPECIFICATION.md](EAR_SPECIFICATION.md) (field reference these examples instantiate),
[EAL's Examples.md](../20_Attribute_Language/Examples.md) (the attributes these entries resolve).
