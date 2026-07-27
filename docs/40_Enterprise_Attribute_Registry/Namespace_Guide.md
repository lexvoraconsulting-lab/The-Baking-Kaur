# EAR — Namespace Guide

## Rule

Every `EARAttributeEntryModel.namespace` must equal the namespace segment of its own
`eal_reference` — the same two-tier form EAL already defines in
[Namespace_Model.md](../20_Attribute_Language/Namespace_Model.md): `core` (platform-level) or
`domain.<name>` (one subtree per industry). EAR does not introduce a second namespace mechanism; it
cross-validates against EAL's existing one.

## Enforcement

`ai/ear/models_pydantic.py::EARAttributeEntryModel._namespace_matches_eal_reference` derives the
expected namespace from `eal_reference` the exact same way
`ai/eal/models_pydantic.py::EALAttributeRecordModel._namespace_matches_path` already does, and
rejects any entry where the two disagree. See
[`test_namespace_must_match_eal_reference`](../../ai/ear/test_ear.py).

## Examples

| `eal_reference` | `namespace` |
|---|---|
| `eal.domain.bakery.colour.primary` | `domain.bakery` |
| `eal.core.embeddings.image_vector` | `core` |
| `eal.domain.bakery.shape.primary` | `domain.bakery` |

(All three appear in [`examples/registry.json`](../../ai/ear/examples/registry.json).)

## Why this isn't a duplicated rule

EAR does not reimplement EAL's `CANONICAL_PATH_PATTERN` regex or namespace-derivation logic — both
are imported directly from `ai.eal.models_pydantic` (see
[EAR_SPECIFICATION.md](EAR_SPECIFICATION.md)). This document exists only to state that EAR applies
the same rule to its own `namespace` field, not to redefine what a namespace is.

## Related Standards

[EAL's Namespace_Model.md](../20_Attribute_Language/Namespace_Model.md),
[EAL's Attribute_Path_Syntax.md](../20_Attribute_Language/Attribute_Path_Syntax.md),
[Registry_Model.md](Registry_Model.md).
