# EAD — Examples Walkthrough

Both files in [`ai/ead/examples/`](../../ai/ead/examples/) hold the same logical 5-entry
`DefinitionSet` — one per entry in
[`ai/ear/examples/registry.json`](../../ai/ear/examples/registry.json) — validated by
[`test_ead.py`](../../ai/ead/test_ead.py), including a direct cross-reference check against the
real EAR registry file.

## `EAR-000001` — Primary Colour

`status: "active"` in EAR. Full mapping guidance: both `shopify_mapping` and `erp_mapping` are set,
`search_behaviour.facetable: true` with a `boost` above 1.0 — the ordinary, fully-wired case.

## `EAR-000002` — Decoration Type

`status: "draft"` in EAR. Both mapping fields are `null` and `search_behaviour.searchable: false` —
shows a Definition explicitly stating "not yet distributed" for a draft attribute, rather than
silently providing mappings a draft attribute shouldn't have yet.

## `EAR-000003` — Image Vector

`namespace: "core"`, `datatype: "vector"` in EAR. `confidence_expectations.minimum_confidence: 0.0`
with `notes` explaining confidence isn't a meaningful concept for a raw embedding — mirrors EAL's
own precedent for vector-typed attributes ([Confidence_Standard.md](../20_Attribute_Language/Confidence_Standard.md)).

## `EAR-000004` — Primary Shape

`status: "deprecated"` in EAR. `vision_guidance`/`ai_guidance` explicitly instruct against using
this attribute for new work, and `metadata.deprecated_reason` records why — showing how a
Definition communicates a lifecycle change in prose, per [Versioning.md](Versioning.md).

## `EAR-000005` — Primary Material

`status: "retired"` in EAR. All guidance fields state the attribute must never be written by any
new pipeline — the terminal lifecycle case.

## Regenerating and re-validating

```bash
python -m ai.ead.test_ead
```

Regenerates `ai/ead/schemas/ead.schema.json`, validates both example files, checks the uniqueness
invariant, ID determinism, confidence-range consistency, import/export round-tripping, and cross-
references every example against the real `ai/ear/examples/registry.json`. See
[`test_ead.py`](../../ai/ead/test_ead.py)'s module docstring.

## Related Standards

[EAD_SPECIFICATION.md](EAD_SPECIFICATION.md) (field reference these examples instantiate),
[EAR's Examples.md](../40_Enterprise_Attribute_Registry/Examples.md) (the registry entries these
Definitions describe).
