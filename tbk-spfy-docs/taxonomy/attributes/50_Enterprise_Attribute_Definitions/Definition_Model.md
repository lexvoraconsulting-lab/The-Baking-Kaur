# EAD — Definition Model

## What a DefinitionSet is

`ai/ead/definitions.py::DefinitionSet` holds the whole collection of `EADDefinitionModel` entries
in memory, keyed by `registry_reference`. A `DefinitionSet` that exists is guaranteed internally
consistent — its constructor runs [`validate_definition_set`](Validation.md) before building its
lookup index, mirroring `ai/ear/registry.py::Registry` exactly.

## Uniqueness invariant

Enforced by `ai/ead/validation.py::validate_definition_set` at construction time: **no two
Definitions may share a `registry_reference`.** Exactly one Definition describes one EAR attribute
— a second Definition claiming the same `registry_reference` would make "what does this attribute
mean" ambiguous. Runnable assertion:
[`test_duplicate_registry_reference_rejected`](../../ai/ead/test_ead.py).

## Why this is the only whole-set invariant (unlike EAR's two)

EAR enforces both duplicate-ID and duplicate-name checks because it has two identifying fields
(`attribute_id`, and `(namespace, canonical_name)`). EAD has one identifying field —
`registry_reference` — since a Definition doesn't introduce its own name a second entry could
collide on; `display_name` is descriptive, not an identity key (two Definitions could plausibly
share a `display_name` string without ambiguity, unlike EAR's `canonical_name`).

## Cross-referencing a real EAR Registry

`ai/ead/api.py::cross_reference_against_registry` is the concrete link between Build-002 and
Build-003: given a `DefinitionSet` and a real `ai.ear.Registry`, it returns every
`registry_reference` with no matching EAR entry — empty means every Definition resolves. This is
**optional**, not required to construct or load a `DefinitionSet` — keeping the module
standalone-loadable without an EAR file always on hand — but
[`test_cross_reference_against_real_ear_registry`](../../ai/ead/test_ead.py) runs it against the
actual `ai/ear/examples/registry.json` on every test run, proving the two Builds integrate without
either modifying the other.

## Query surface

`ai/ead/api.py` exposes: `get_by_registry_reference`, `by_display_name`, `by_tag_in_metadata`,
`cross_reference_against_registry`. Every function reads from an already-validated `DefinitionSet`
— none perform I/O beyond the optional registry cross-check.

## Related Standards

[Validation.md](Validation.md), [Mapping_Guide.md](Mapping_Guide.md),
[EAR's Registry_Model.md](../40_Enterprise_Attribute_Registry/Registry_Model.md) (the pattern this
mirrors).
