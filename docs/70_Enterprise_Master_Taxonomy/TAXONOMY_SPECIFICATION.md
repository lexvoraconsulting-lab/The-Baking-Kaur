# Enterprise Master Taxonomy — Specification

Build-005, Workstream TAX, BL-0. The umbrella spec for `ai/taxonomy/` — field reference, module
reference, folder structure, identifier strategy, and where this package's responsibility ends and
an already-built Build's begins.

## Reuse, not redesign

This is the single most important boundary in this package, restated per-field below:

| Concern | This package | Reused from |
|---|---|---|
| An attribute's canonical existence, datatype, owner | Not modeled here | EAR (`EARAttributeEntry.attribute_id`) |
| An attribute's business meaning, mapping guidance | Not modeled here | EAD (`EADDefinitionModel`) |
| Writing a resolved value to Shopify/ERP | Not modeled here | Build-004 (`ai.attribute_distribution`) |
| Cross-system labels (Vision/ERP/Shopify/SEO/Search) on a Term | `TermModel.external_ids` | `ai.eal.models_pydantic.ExternalIdModel`, reused directly |
| Which Attribute Group an EAR attribute belongs to | `AttributeGroupModel.ear_namespace` (a plain string join key to EAR's `namespace` field) | EAR's `namespace` field itself is unmodified |

`ai/taxonomy/` never imports from, and is never imported by, `ai/eal`, `ai/ear`, `ai/ead`, or
`ai/attribute_distribution` — all four remain frozen, read-only contracts to this Build (verified by
grep at the end of every backlog item, per
[VIG-010](../00_Governance/VIG-010-Execution-Protocol.md)).

## Entities

Five entities, matching `docs/10_Taxonomy/Entity_Model.md`'s Category / Attribute Group / Controlled
Vocabulary Term exactly (Vocabulary itself is modeled explicitly here as the container Terms belong
to, implicit in the Sprint 2.1 docs), plus `TaxonomyAttribute` (added BL-1) representing the
individual named fields `Hierarchy.md` describes as living inside an Attribute Group ("Attribute
Group → Attribute → Value").

### Category

| Field | Type | Notes |
|---|---|---|
| `category_id` | `str` | `TAX-CAT-NNNNNN`, sequentially allocated |
| `domain` | `str` | e.g. `"bakery"` — the top-level industry scope (Hierarchy.md) |
| `name` | `str` | |
| `parent_id` | `str \| None` | Must resolve to another `category_id` in the same catalog |
| `attribute_group_ids` | `list[str]` | Groups *added* at this node (Inheritance.md — additive only, not the full inherited set) |
| `status` | `"active" \| "deprecated"` | |

### AttributeGroup

| Field | Type | Notes |
|---|---|---|
| `group_id` | `str` | `TAX-GRP-NNNNNN` |
| `name` | `str` | |
| `tier` | `"platform" \| "domain"` | Attribute_Group_Architecture.md's two-tier split |
| `ear_namespace` | `str \| None` | Join key to EAR's `namespace` field — not cross-validated in BL-0 |
| `version` | `str` | Per-group version, Versioning.md |
| `status` | `"active" \| "deprecated"` | |

### Vocabulary

| Field | Type | Notes |
|---|---|---|
| `vocabulary_id` | `str` | `TAX-VOC-NNNNNN` |
| `name` | `str` | |
| `scope` | `"global" \| "domain"` | Controlled_Vocabulary.md |
| `domain` | `str \| None` | Required if and only if `scope == "domain"` |
| `version` | `str` | |
| `status` | `"active" \| "deprecated"` | |

### Term

| Field | Type | Notes |
|---|---|---|
| `term_id` | `str` | `TAX-TERM-NNNNNN` |
| `vocabulary_id` | `str` | Must resolve to a real `Vocabulary` |
| `label` | `str` | Canonical label |
| `synonyms` | `list[str]` | Free-text normalization aliases |
| `parent_term_id` | `str \| None` | Shallow within-vocabulary hierarchy (Controlled_Vocabulary.md) |
| `status` | `"active" \| "deprecated"` | |
| `superseded_by` | `str \| None` | Required if and only if `status == "deprecated"` |
| `external_ids` | `list[ExternalIdModel]` | Cross-system labels — reused from EAL, not redefined |

### TaxonomyAttribute (added BL-1)

| Field | Type | Notes |
|---|---|---|
| `attribute_id` | `str` | `TAX-ATTR-NNNNNN` |
| `group_id` | `str` | Must resolve to a real `AttributeGroup` |
| `name` | `str` | e.g. `primary_colour` |
| `data_type` | `str` | Reused verbatim from `ai.eal.models.DataType` — not redefined |
| `vocabulary_id` | `str \| None` | Required if and only if `data_type == "enum"` |
| `ear_namespace` | `str \| None` | Join key to EAR's `namespace` field — not cross-validated in BL-1 (same deliberate deferral as `AttributeGroup.ear_namespace`) |
| `status` | `"active" \| "deprecated"` | |

**Not the same thing as an EAR `EARAttributeEntry`.** This entity describes a field's shape and
where its values come from *within the taxonomy's knowledge model* — it does not register the
field platform-wide (that remains EAR's exclusive job) and carries no `owner`, no `eal_reference`,
no lifecycle beyond active/deprecated. See "Reuse, not redesign" above.

## Identifier strategy

Sequential, prefixed, single-allocator IDs (`TAX-{CAT,GRP,VOC,TERM,ATTR}-NNNNNN`) — same rationale as
EAR's `EAR-NNNNNN`: this catalog is centrally authored by one process, so a coordinated sequential
allocator is safe (content-hash IDs are for uncoordinated producers, which this isn't). IDs are
stable across relabeling and reparenting, per `Hierarchy.md`'s explicit requirement.

## Module reference

| Module | Responsibility |
|---|---|
| `models.py` | Plain dataclasses — human/IDE-facing shape |
| `models_pydantic.py` | Runtime validation, per-entity invariants |
| `ids.py` | ID format validation + sequential allocation, per entity type |
| `validation.py` | Whole-catalog invariants (duplicate IDs, unresolved cross-references) |
| `catalog.py` | `TaxonomyCatalog` — in-memory container, O(1) lookup by ID, runs `validate_catalog()` at construction |
| `loader.py` | JSON/YAML import |
| `exporter.py` | JSON/YAML export + JSON Schema regeneration |

## Folder structure

```
ai/taxonomy/
  models.py  models_pydantic.py  ids.py  validation.py  catalog.py  loader.py  exporter.py
  __init__.py
  schemas/       category.schema.json  attribute_group.schema.json  vocabulary.schema.json
                 term.schema.json  attribute.schema.json
  examples/      catalog.json  (structural fixture, BL-0 — not real content)
  content/       bakery_v1.json  (real content, grown additively BL-1 -> BL-2 — 6 categories,
                 30 groups, 17 vocabularies, 96 terms, 26 attributes)
  test_taxonomy.py
```

## What's deliberately not validated (still true after BL-1)

`AttributeGroup.ear_namespace` and `TaxonomyAttribute.ear_namespace` cross-referenced against a live
EAR `Registry`, and `Category.attribute_group_ids` checked against `Inheritance.md`'s additive-only
rule across ancestors — both require a live EAR registration pass to check meaningfully, and remain
plain, unvalidated string join keys through BL-1. Tracked as a later decision, not a gap (mirrors
EAR's own precedent: `taxonomy_references` was deliberately deferred by EAR for the identical reason,
until this Build existed).

## `external_ids` system-value convention (established BL-2)

`Term.external_ids` is the single mechanism for every cross-system label — no dedicated
`ai_vision_labels`/`shopify_labels`/etc. fields exist, or should be added. Convention for `system`:

| `system` value | Represents | Example `id_type` |
|---|---|---|
| `ai_vision` | A label the Vision Engine (Build-008) matches against | `label` |
| `shopify` | A Shopify-side tag/handle (Build-004 resolves against this) | `tag` |
| `erp` | An ERP-side code (Build-004 resolves against this) | `sku_code`, `colour_code` |
| `search` | A query-expansion alias (Build-009 consumes this) | `alias`, `facet` |
| `seo` | An SEO-facing phrase (storefront track consumes this — never built here) | `phrase` |

A Term may carry any number of `external_ids` entries, including several with the same `system`
(e.g. three `ai_vision` labels for one colour) — this is what replaces a "Search Aliases" or "Vision
Labels" list field.

## Future extension points (noted, not implemented)

- **Per-term AI confidence** — a term could eventually carry an expected-confidence range for how
  reliably Vision AI matches it, mirroring `VIG-007`'s confidence model. Not added in BL-2 — no
  concrete consumer needs it yet, and the instruction requesting it explicitly called it "optional,
  future." Add only when Build-008 (Vision Extraction) has a real use for it.
- **Multilingual labels/synonyms** — `label`, `display` text, and `synonyms` are plain strings
  today. A future locale-keyed extension (`{"en": "Rose Gold", "hi": "..."}`) would replace the
  string type, not add a parallel field — deferred until real localization is scoped, per explicit
  instruction not to implement it yet.

## What's out of taxonomy scope

Thirteen concepts raised during BL-1 planning (Pricing, ERP, SEO, Manufacturing, etc.) were
evaluated and excluded as belonging to another Build's or track's ownership — see
[CROSS_SYSTEM_OWNERSHIP.md](CROSS_SYSTEM_OWNERSHIP.md) for the full table and reasoning.

## Related Standards

[docs/10_Taxonomy/](../10_Taxonomy/Architecture.md) (the architecture this content is authored
against), [EAR_SPECIFICATION.md](../40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md) (the
`namespace`/`taxonomy_references` join points), [EAD_SPECIFICATION.md](../50_Enterprise_Attribute_Definitions/EAD_SPECIFICATION.md)
(`allowed_values`/`knowledge_graph_reference`), [SPRINT_CHARTER.md](SPRINT_CHARTER.md).
