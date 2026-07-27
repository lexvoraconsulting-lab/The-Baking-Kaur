# Enterprise Attribute Definitions (EAD) v1 — Specification

## What EAD is

Build-003. The semantic definition layer over EAR (Build-002) attributes — the business meaning,
display name, guidance, and mappings a human or an AI consumer needs to use an attribute correctly.
EAD does not implement taxonomy or a validation engine; it enforces its own record shape only. See
[docs/adr/2026-07-27-build-003-renumbering.md](../adr/2026-07-27-build-003-renumbering.md) for why
Build-003 means this and not Enterprise Attribute Distribution (renumbered to Build-004).

## Field reference

```
definition_id            deterministic uuid5 of registry_reference - Identifier Strategy below
ead_version               "1.0" - this document's version
registry_reference         an EAR attribute_id (e.g. "EAR-000001") - format-validated via
                          ai.ear.ids.is_valid_attribute_id, imported not reimplemented. One
                          Definition per EAR entry (Definition_Model.md).
display_name              human-facing label, e.g. "Primary Colour"
business_definition         plain-English meaning of the attribute
purpose                    why this attribute exists / what business decision it drives
examples                   list[str], at least one - example values or example sentences
vision_guidance             instructions for how the Vision Engine should extract this attribute
ai_guidance                 instructions for how downstream AI (Marketing AI, JARVIS) should
                          reason about/use this attribute - descriptive metadata, not executable
                          prompt text (VIG-004 "no business logic in prompts")
mapping_guidance             general prose on how this attribute maps across systems, complementing
                          the concrete shopify_mapping/erp_mapping fields
allowed_values              optional list[str] - candidate values ahead of a formal Sprint 2.2
                          Controlled Vocabulary (Mapping_Guide.md / Validation.md)
search_behaviour             {searchable, facetable, boost, notes} - machine-actionable flags for
                          the future Search workstream (WS-10)
confidence_expectations       {minimum_confidence, typical_confidence, notes} - reuses EAL's 0-1
                          confidence range convention
knowledge_graph_reference      opaque nullable pointer - the Knowledge Graph (Build-005) doesn't
                          exist yet (Mapping_Guide.md)
shopify_mapping             Optional[ExternalIdModel] - reuses ai.eal.models_pydantic.ExternalIdModel
                          directly, not a new shape (Mapping_Guide.md)
erp_mapping                 Optional[ExternalIdModel] - same reuse
metadata                    free-form dict[str, Any] catch-all, distinct from EAR's tags
```

## Identifier strategy

`definition_id` is content-hash-derived (`uuid.uuid5`), same philosophy as
[EAR's Identifier_Strategy](../40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md) —
two processes computing a Definition for the same `registry_reference` arrive at the same ID with
zero shared state (`ai/ead/ids.py::compute_definition_id`). A distinct namespace UUID
(`EAD_NAMESPACE_UUID`, separate from EAR's `EAR_NAMESPACE_UUID`) guarantees a `definition_id` can
never collide with a `registry_uuid` even given the same input string.

Unlike EAR's `attribute_id` (sequential, single-allocator), EAD needs no sequential scheme — there
is exactly one Definition per EAR attribute, so `registry_reference` itself is already the natural
join key; `definition_id` exists only to give this record its own permanent identity per VIG-006.

## Folder structure

```
ai/ead/
  __init__.py           re-exports
  models.py              dataclasses (canonical field reference)
  models_pydantic.py       Pydantic models (validation, JSON Schema generation)
  ids.py                  definition_id derivation
  definitions.py           the DefinitionSet container (Definition_Model.md)
  validation.py            whole-set invariants (Validation.md)
  loader.py                import - JSON/YAML -> DefinitionSet
  exporter.py               export - DefinitionSet -> JSON/YAML; regenerates schemas/ead.schema.json
  api.py                    read-only query surface + optional EAR cross-reference check
  test_ead.py                self-check: regenerates schema, validates every example, cross-checks
                          against a real EAR Registry
  schemas/ead.schema.json    generated - never hand-edited
  examples/
    definitions.json
    definitions.yaml

docs/50_Enterprise_Attribute_Definitions/  this specification
```

## What EAD deliberately does not do

- Does not implement taxonomy content or a validation engine (`allowed_values` stays opaque, not
  checked against a real Controlled Vocabulary — see [Validation.md](Validation.md)).
- Does not write to Shopify, ERP, or the Knowledge Graph — `shopify_mapping`/`erp_mapping`/
  `knowledge_graph_reference` are guidance and pointers only; Build-004 (Enterprise Attribute
  Distribution) is the only code that writes anywhere.
- Does not modify `ai/eal/` or `ai/ear/` — both are read-only contracts, imported directly.

## Related Standards

Reuses [EAL](../20_Attribute_Language/EAL_SPECIFICATION.md) (`ExternalIdModel`, confidence range
convention) and [EAR](../40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md) (`registry_reference`
format, `Registry` for cross-reference checks) directly rather than redefining either. Implements
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) (versioning) and
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md) (identifiers). Scoped by
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-003). See [README.md](README.md) for the full document index.
