# Enterprise Attribute Registry (EAR) v1 — Specification

## What EAR is

The canonical registry of every enterprise attribute used anywhere on the platform. It answers:
does this attribute exist, what is its canonical identifier, which namespace/module owns it, which
datatype it uses, and which taxonomy/EAD content it points at. EAR does **not** contain business
definitions — those are Build-003 (EAD)'s responsibility, referenced here only via
`definition_reference`, an opaque pointer.

EAR is Build-002, per
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07. It reuses [EAL](../20_Attribute_Language/EAL_SPECIFICATION.md)'s canonical-path grammar
and datatype list directly rather than redefining them.

## Field reference

```
registry_uuid        deterministic uuid5 of eal_reference - Identifier Strategy below
attribute_id          sequential "EAR-NNNNNN" - Identifier Strategy below
canonical_name        short registry-local name, e.g. "primary_colour"
namespace             "core" | "domain.<name>" - must match eal_reference's namespace segment
datatype              one of EAL's 11 canonical types (ai.eal.models.DataType), reused not redefined
status                "draft" | "active" | "deprecated" | "retired"
owner                 which module/team owns this attribute, e.g. "vision_engine"
ear_version           "1.0" - this document's version
version               this entry's own version, VIG-005 v1/v2 style
introduced_in         version this attribute was introduced
deprecated_in         version this attribute was deprecated - required iff status is
                     "deprecated"/"retired", forbidden otherwise (Validation.md)
eal_reference          the full EAL canonical_path this entry resolves, e.g.
                     "eal.domain.bakery.colour.primary" - validated against EAL's own
                     CANONICAL_PATH_PATTERN, imported not reimplemented
definition_reference  opaque pointer to a future Build-003 (EAD) definition - null until EAD exists
taxonomy_references   opaque list of Sprint 2.1/2.2 taxonomy pointers - not validated against a
                     live taxonomy yet (Sprint 2.2 hasn't authored real content - Validation.md)
validation_profile    opaque name of a future validation ruleset - not enforced yet
tags                  free-form list[str]
```

## Identifier strategy — two schemes, two reasons

`registry_uuid` is content-hash-derived (`uuid.uuid5`), the same no-coordination-needed philosophy
as [EAL's Identifier_Strategy.md](../20_Attribute_Language/Identifier_Strategy.md) — two processes
computing the same `eal_reference` arrive at the same UUID with zero shared state
(`ai/ear/ids.py::compute_registry_uuid`).

`attribute_id` (`EAR-000001`, `EAR-000002`, ...) is deliberately **sequential**, not content-hash
derived. EAR is a single, centralized catalog with exactly one allocator — unlike EAL records,
which are produced independently by many uncoordinated pipelines. Sequential, human-readable IDs
are only safe when one source is the sole allocator, which is exactly what a registry is
(`ai/ear/ids.py::allocate_attribute_id`).

## Folder structure

```
ai/ear/
  __init__.py           re-exports
  models.py              dataclasses (canonical field reference)
  models_pydantic.py       Pydantic models (validation, JSON Schema generation)
  ids.py                   registry_uuid / attribute_id derivation + format validation
  registry.py              the Registry container (Registry_Model.md)
  validation.py            whole-registry invariants (Validation.md)
  loader.py                import - JSON/YAML -> Registry
  exporter.py               export - Registry -> JSON/YAML; regenerates schemas/ear.schema.json
  api.py                    read-only query surface
  test_ear.py                self-check: regenerates schema, validates every example
  schemas/ear.schema.json     generated - never hand-edited
  examples/
    registry.json
    registry.yaml

docs/40_Enterprise_Attribute_Registry/  this specification
```

## What EAR deliberately does not do

- Does not store business definitions (Build-003/EAD's job).
- Does not validate `taxonomy_references` against a real taxonomy (Sprint 2.2 hasn't authored
  content yet — see [Validation.md](Validation.md)).
- Does not implement Knowledge Graph storage, Vision extraction, or AI prompts — out of scope for
  Build-002 per the roadmap.

## Related Standards

Reuses [EAL_SPECIFICATION.md](../20_Attribute_Language/EAL_SPECIFICATION.md),
[Identifier_Strategy.md](../20_Attribute_Language/Identifier_Strategy.md) (the philosophy, not the
mechanism — see above),
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md),
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md). See [README.md](README.md) for the
full document index.
