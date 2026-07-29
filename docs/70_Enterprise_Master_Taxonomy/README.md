# Enterprise Master Taxonomy v1

Build-005 of VISIONARY IMAGE GENOME™, Workstream **TAX** (new — the first non-ATTR workstream,
assigned at Sprint Charter time per [ADR 0006](../adr/2026-07-27-workstream-id-convention.md)). The
real, authored taxonomy content — Category tree, Attribute Groups, Controlled Vocabularies and their
Terms — that the architecture in [docs/10_Taxonomy/](../10_Taxonomy/Architecture.md) (Sprint 2.1)
was designed for, and that EAR's `taxonomy_references` and EAD's `allowed_values`/
`knowledge_graph_reference` fields have been pointing at as opaque, unresolvable placeholders since
Build-002/003. Implementation lives in [`ai/taxonomy/`](../../ai/taxonomy/).

**Build-005 is a knowledge layer, not a framework layer.** It does not redefine EAR's registry, EAD's
definitions, or Build-004's distribution engine — it reuses all three directly (see
[TAXONOMY_SPECIFICATION.md](TAXONOMY_SPECIFICATION.md)'s "Reuse, not redesign" section).

## Status: BL-1 complete — real Bakery-domain content authored (seed depth, not exhaustive)

See [SPRINT_CHARTER.md](SPRINT_CHARTER.md) for the full backlog, the BL-0 scope-narrowing decision,
and the BL-1 scope-expansion reconciliation (both resolved before any conflicting code was written).

## Start here

- [TAXONOMY_SPECIFICATION.md](TAXONOMY_SPECIFICATION.md) — the umbrella spec, field reference,
  module reference, folder structure.
- [`ai/taxonomy/test_taxonomy.py`](../../ai/taxonomy/test_taxonomy.py) — run
  `python -m ai.taxonomy.test_taxonomy` to validate the structural example and regenerate schemas.

## Document index

| Document | Covers |
|---|---|
| [TAXONOMY_SPECIFICATION.md](TAXONOMY_SPECIFICATION.md) | Umbrella spec, entity field reference, identifier strategy, folder structure, reuse boundaries. |
| [SPRINT_CHARTER.md](SPRINT_CHARTER.md) | Sprint Goal, Scope, the conflict-and-narrowing decision, backlog history. |
| [CROSS_SYSTEM_OWNERSHIP.md](CROSS_SYSTEM_OWNERSHIP.md) | The 13 concepts considered and excluded from taxonomy content, with their real owning Build/track. |

## Related Standards

Implements the architecture in [docs/10_Taxonomy/](../10_Taxonomy/Architecture.md) (Sprint 2.1) —
does not redefine it. Reuses [EAL](../20_Attribute_Language/README.md)'s `ExternalIdModel` directly
for cross-system labels (Vision/ERP/Shopify/SEO/Search), and is the intended real content behind
[EAR](../40_Enterprise_Attribute_Registry/README.md)'s `taxonomy_references` and
[EAD](../50_Enterprise_Attribute_Definitions/README.md)'s `allowed_values`/
`knowledge_graph_reference` fields. Scoped by
[docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-005) and Architecture Gate AR-007.
