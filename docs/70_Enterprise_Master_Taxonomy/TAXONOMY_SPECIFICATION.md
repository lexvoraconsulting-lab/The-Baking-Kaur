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

Four entities, matching `docs/10_Taxonomy/Entity_Model.md`'s Category / Attribute Group / Controlled
Vocabulary Term exactly (Vocabulary itself is modeled explicitly here as the container Terms belong
to, implicit in the Sprint 2.1 docs).

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

## Identifier strategy

Sequential, prefixed, single-allocator IDs (`TAX-{CAT,GRP,VOC,TERM}-NNNNNN`) — same rationale as
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
  schemas/       category.schema.json  attribute_group.schema.json  vocabulary.schema.json  term.schema.json
  examples/      catalog.json  (structural fixture, BL-0 — not real content)
  test_taxonomy.py
```

## What BL-0 deliberately does not validate

`AttributeGroup.ear_namespace` cross-referenced against a live EAR `Registry`, and
`Category.attribute_group_ids` checked against `Inheritance.md`'s additive-only rule across
ancestors — both require real content to check meaningfully, and BL-0 ships none. Tracked as a BL-1+
decision, not a BL-0 gap (mirrors EAR's own precedent: `taxonomy_references` was deliberately
deferred by EAR for the identical reason, until this Build existed).

## Related Standards

[docs/10_Taxonomy/](../10_Taxonomy/Architecture.md) (the architecture this content is authored
against), [EAR_SPECIFICATION.md](../40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md) (the
`namespace`/`taxonomy_references` join points), [EAD_SPECIFICATION.md](../50_Enterprise_Attribute_Definitions/EAD_SPECIFICATION.md)
(`allowed_values`/`knowledge_graph_reference`), [SPRINT_CHARTER.md](SPRINT_CHARTER.md).
