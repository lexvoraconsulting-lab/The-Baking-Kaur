# Build-003 Completion Report: Enterprise Attribute Definitions (EAD) v1

Date: 2026-07-27

## Renumbering performed before this build

This build's own brief collided with already-committed content: `docs/20_Attribute_Language/
Roadmap.md` and `docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md` (reviewed and
passed at AR-005) both defined Build-003 as "EAD: Enterprise Attribute Distribution." Resolved by
renumbering — Enterprise Attribute Definitions becomes Build-003; Distribution and every later
Build shift up by one (Distribution → Build-004, Knowledge Graph → Build-005, and so on). Full
rationale, mapping table, and list of files touched/deliberately-not-touched:
[docs/adr/2026-07-27-build-003-renumbering.md](../adr/2026-07-27-build-003-renumbering.md) (ADR
0005). This was a prerequisite pass, done before any `ai/ead/` code was written.

## Files created (this build)

Code (`ai/ead/`):

- `__init__.py` — public re-exports.
- `models.py` — `EADDefinition` dataclass, `SearchBehaviour`/`ConfidenceExpectations` sub-
  dataclasses, `EAD_VERSION`. Reuses `ai.eal.models.ExternalId` for mapping fields.
- `models_pydantic.py` — `EADDefinitionModel` and its submodels. Reuses
  `ai.eal.models_pydantic.ExternalIdModel` directly for `shopify_mapping`/`erp_mapping`; reuses
  `ai.ear.ids.is_valid_attribute_id` for `registry_reference` format validation.
- `ids.py` — `compute_definition_id` (deterministic uuid5, distinct namespace from EAR's).
- `definitions.py` — `DefinitionSet` container, validated at construction.
- `validation.py` — whole-set invariant: no duplicate `registry_reference`.
- `loader.py` — `load_definitions()`, JSON/YAML.
- `exporter.py` — `export_definitions()`, `regenerate_schema()`.
- `api.py` — query surface, including `cross_reference_against_registry()` — an optional check
  reusing `ai.ear.Registry` directly.
- `test_ead.py` — 13 self-check functions, wired into `if __name__ == "__main__"`.
- `schemas/ead.schema.json` — generated, never hand-edited.
- `examples/definitions.json`, `examples/definitions.yaml` — 5 Definitions, one per entry in
  `ai/ear/examples/registry.json` (real cross-reference, not synthetic IDs), covering active,
  draft, deprecated, and retired EAR lifecycle states plus both `domain.bakery` and `core`
  namespaces.

Documentation (`docs/50_Enterprise_Attribute_Definitions/`):

- `README.md`, `EAD_SPECIFICATION.md`, `Definition_Model.md`, `Mapping_Guide.md`, `Validation.md`,
  `Versioning.md`, `Examples.md`, `BUILD_003_COMPLETION_REPORT.md` (this document).

Renumbering (prerequisite, not this build's implementation):

- `docs/20_Attribute_Language/Roadmap.md` — inserted the new Build-003 section, renumbered the
  rest.
- `docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md` — full renumbering pass.
- `docs/30_Enterprise_Program_Roadmap/EPR_v1_COMPLETION_REPORT.md` — addendum appended.
- `docs/adr/2026-07-27-build-003-renumbering.md` — ADR 0005 (new).

## Files updated

None beyond the renumbering pass listed above. `ai/eal/`, `ai/ear/` (all code), and every document
under `docs/40_Enterprise_Attribute_Registry/` were read for reuse but not modified — EAD imports
EAL's `ExternalIdModel` and EAR's `ids`/`Registry` directly rather than copying either.

## What was deliberately reused, not redesigned

- `shopify_mapping`/`erp_mapping` are `ai.eal.models_pydantic.ExternalIdModel` instances, not a new
  shape.
- `registry_reference` format validation imports `ai.ear.ids.is_valid_attribute_id` directly.
- The `DefinitionSet` container, whole-set validation pattern, and JSON/YAML load/export helpers
  mirror `ai/ear/{registry,validation,loader,exporter}.py` exactly.
- The doc set's style, structure, and self-check convention mirror
  `docs/40_Enterprise_Attribute_Registry/` throughout.

## Validation results

```
$ python -m ai.ead.test_ead
OK
```

13 checks, all passing: both example formats load and are equal to each other; every example's
`definition_id` is cross-checked against a fresh `compute_definition_id` recomputation; **every
example's `registry_reference` resolves against the real, loaded
`ai/ear/examples/registry.json`** — a concrete Build-002/Build-003 integration test, not a
synthetic one; duplicate `registry_reference` and invalid-format `registry_reference` are both
rejected; missing required fields, out-of-range confidence, and `typical_confidence` below
`minimum_confidence` are all rejected; empty `examples` lists are rejected; export-then-reload
round-trips without data loss for both JSON and YAML.

```
$ python -m ai.eal.test_eal
OK
$ python -m ai.ear.test_ear
OK
```

Both frozen modules still pass unchanged, confirming EAD's imports did not perturb either.

Cross-reference sweep (every `[text](path)` link across all 8
`docs/50_Enterprise_Attribute_Definitions/*.md` files, resolved relative to its own file): **0
broken links.**

`git status` after this pass shows only new, untracked files under `ai/ead/` and
`docs/50_Enterprise_Attribute_Definitions/`, plus the modified renumbering files listed above — no
file under `ai/eal/` or `ai/ear/` touched.

## Remaining issues

None blocking. Two items are deliberately deferred, consistent with EAR's own deferred-validation
pattern, each stated explicitly in [Validation.md](Validation.md): `allowed_values` isn't validated
against a real Controlled Vocabulary (Sprint 2.2/Build-006 hasn't authored one yet), and
`knowledge_graph_reference` stays `null` (the Knowledge Graph/Build-005 doesn't exist yet). No
validation engine (WS-07) is implemented, per this build's own Constraints.

## Status

**Not committed.** Per instruction, this build stops here awaiting Architecture Review **AR-006**
before Build-004 (renumbered Enterprise Attribute Distribution) begins. Build-004 has not been
started.
