# EAL — Enum Standard

## Rule

An attribute with `data_type: "enum"` must set `vocabulary` to the name of the
[Controlled Vocabulary](../10_Taxonomy/Controlled_Vocabulary.md) its `value` resolves against — EAL
never inlines a hardcoded enum value list. This is a direct reuse of Sprint 2.1's vocabulary
mechanism, not a second one.

## Example

```json
{
  "canonical_path": "eal.domain.bakery.colour.primary",
  "data_type": "enum",
  "vocabulary": "colour_name",
  "value": "white"
}
```

(See [`vision_output_example.json`](../../ai/eal/examples/vision_output_example.json).)

## What EAL does NOT do

EAL does not define what `colour_name`'s valid terms are — that's Sprint 2.2's job (authoring the
real Master Taxonomy), per [Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md).
`ai/eal/models_pydantic.py` validates that `vocabulary` is present when `data_type == "enum"` is
*not yet enforced as a cross-field check* — flagged in
[Architecture_Review_AR004.md](Architecture_Review_AR004.md) as a Minor finding, since Build-001
has no live vocabulary registry yet to validate `value` against.

## Related Standards

[Data_Type_Standard.md](Data_Type_Standard.md),
[Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md).
