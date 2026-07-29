# BUILD-005 Sprint Charter — Enterprise Master Taxonomy

Workstream: **TAX** (new — per [ADR 0006](../adr/2026-07-27-workstream-id-convention.md)'s
standing convention, a genuinely new business capability gets a new Workstream ID at Sprint Charter
time; TAX is the first non-ATTR workstream this platform has assigned).

Status: **BL-2 complete**. BL-3 not started — awaiting approval per this project's per-item review
gate ([VIG-010](../00_Governance/VIG-010-Execution-Protocol.md)).

## Sprint Goal

Author the real Enterprise Master Taxonomy content — Category tree, Attribute Groups, Controlled
Vocabularies, Terms — that Sprint 2.1's architecture (`docs/10_Taxonomy/`) was designed to hold, at
a scale target of 500+ Attribute Groups and 10,000+ Controlled Vocabulary Terms, reusing EAR
(Build-002), EAD (Build-003), and Attribute Distribution (Build-004) exactly as built.

## Scope-narrowing decision (before any code was written)

The originally proposed backlog (Schema, Attribute Dictionary, Validation Framework, Mapping Layer,
Registry, Testing, Documentation) was cross-checked against the existing repository and found to
substantially duplicate three other Builds:

| Originally proposed | Collided with |
|---|---|
| "Enterprise Taxonomy Schema" | Sprint 2.1 (`docs/10_Taxonomy/Entity_Model.md`, `Hierarchy.md`, `Attribute_Group_Architecture.md`, `Inheritance.md`, `Versioning.md`) — already built |
| "Validation Framework...rule engine" | Sprint 2.1's `Validation.md` **and** Build-006 (Enterprise Validation Engine, not yet started, [ADR 0007](../adr/2026-07-28-build-005-007-resequencing.md)) |
| "Mapping Layer: Canonical → Vision → ERP → Shopify → SEO → Search..." | Build-004 (Attribute Distribution), frozen and tagged `build-004-complete` |
| "Registry: lookup, search, canonical resolution" | Build-002 (Enterprise Attribute Registry) — its own name |

Resolved by explicit user decision: Build-005 is content-authoring only. It reuses Build-002/003/004
infrastructure directly and does not redesign, replace, or duplicate it. If any of the above
responsibilities are found genuinely missing during BL-1+, that's flagged as a conflict per this
same protocol — not silently absorbed into Build-005.

## Backlog Items

| Item | Description | Status | Commit |
|---|---|---|---|
| BL-0 | Repository preparation — `ai/taxonomy/` skeleton (4 entities: Category, AttributeGroup, Vocabulary, Term; ID allocation; whole-catalog validation; loader/exporter; schema generation; structural self-check), `docs/70_Enterprise_Master_Taxonomy/` skeleton | **Done** | `0545f2e` |
| BL-1 | Author real Category tree, Attribute Groups, Attributes, Controlled Vocabularies, Terms, synonyms, and cross-system labels — **expanded scope**, see below | **Done** | *(this commit)* |
| BL-2 | First real Enterprise Controlled Vocabularies — 11 new vocabularies + 1 flagship fully-enriched term — **zero schema changes**, see below | **Done** | *(this commit)* |
| BL-3 | Ontology relationship instances beyond parent/child hierarchy (Object-to-Object, Image-to-Business-Entity per `docs/10_Taxonomy/Relationship_Model.md`) — deferred, needs real Image/Object instances that don't exist yet | Not started | — |
| BL-4 | Testing, documentation, completion report, freeze | Not started | — |

### BL-2 conflict resolution (before implementation)

Three requested fields/vocabularies conflicted with already-documented or already-committed
decisions, flagged and resolved before coding:
- **"Delivery"** conflicted with BL-1's `CROSS_SYSTEM_OWNERSHIP.md` (which excluded it as the
  storefront track's logistics/fee system) — resolved as a **narrow product-attribute vocabulary**
  only (`Requires Refrigeration`, `Same-Day Eligible`, ...), never the fee/logistics system itself.
  `test_bl2_delivery_vocabulary_is_product_attribute_scoped_not_logistics` asserts no fee/currency
  content ever lands in it.
- **"Parent Category" / a single "Attribute Group" field on Term or Vocabulary** conflicted directly
  with `Hierarchy.md`'s explicit reusability principle ("a Controlled Vocabulary Term never
  hardcodes which Category it's valid for"). Rejected — hierarchy still flows only through
  Category → Attribute Group → Attribute → Vocabulary. `test_bl2_no_term_hardcodes_a_category_or_single_group`
  and `test_bl2_shape_vocabulary_reused_across_two_groups` assert this holds (Shape stays used by
  both Geometry and Board).
- **AI Vision / Shopify / ERP / SEO / Search "Labels" and "Search Aliases"** as new dedicated
  fields — rejected as redundant with the already-built `Term.external_ids` (`system`-discriminated)
  mechanism. Populated via `external_ids` entries instead, zero schema change.

### What BL-2 actually delivered

**No code/schema changes** — `ai/taxonomy/` models are identical to BL-1. Pure content: 1 new
Attribute Group (Delivery), 11 new Controlled Vocabularies (Style, Finish, Texture, Decoration
Style, Flower, Tier Style, Recipient, Delivery Attribute, Packaging Type, Cream & Icing, Ganache),
11 new `TaxonomyAttribute` entries backing them, ~55 new Terms across those vocabularies, plus one
flagship fully-enriched term (**Rose Gold** — 3 synonyms, 9 `external_ids` spanning all 5 systems)
demonstrating the richness ceiling every term can reach. Catalog total: 6 Categories, 30 Attribute
Groups, 26 Attributes, 17 Vocabularies, 96 Terms.

### Deliberately deferred (documented, not built)

- **AI confidence per term** — noted as a future optional field in
  [TAXONOMY_SPECIFICATION.md](TAXONOMY_SPECIFICATION.md); not added now, per explicit instruction
  ("optional future field").
- **Multilingual support** — `label`/synonym strings stay plain strings; a future locale-keyed
  extension is noted, not implemented, per explicit instruction ("do not implement translations
  yet").

### BL-1 scope expansion (approved before implementation)

The originally-planned BL-1 (4 groups) was expanded on request to a 10-year enterprise scope: ~53
candidate concepts, cross-checked against Sprint 2.1's architecture before implementation. Resolved
as:
- **9 already-existing Sprint 2.1 groups** (Classification, Geometry, Colour, Material, Texture,
  Decoration, Characters, Writing, Occasion, Theme, Packaging, Business — 12 total) — real
  Attributes populated, no new group architecture.
- **17 new domain groups** (Recipient, Style, Finish, Flowers, Topper, Tier, Board, Size, Weight,
  Servings, Flavour, Sponge, Filling, Cream, Ganache, Dietary, Allergens) — additive, real Attribute
  justifies each, per `Inheritance.md`'s extension pattern.
- **7 items modeled as Vocabulary Terms, not new groups** (Wedding, Corporate, Festival, Luxury,
  Seasonal, Regional, Gifting) — avoids fragmenting `Hierarchy.md`'s "one Attribute, one Group" model.
- **13 items excluded as out-of-taxonomy** (Pricing, ERP, SEO, Manufacturing, etc.) — recorded in
  [CROSS_SYSTEM_OWNERSHIP.md](CROSS_SYSTEM_OWNERSHIP.md), not built here.

### What BL-1 actually delivered

6 Categories (Bakery domain, 3-level tree), 29 Attribute Groups, 15 `TaxonomyAttribute` entries
(enum/integer/float/string, spanning existing and new groups), 6 Controlled Vocabularies, 43 real
Terms with synonyms and cross-system `external_ids` (Shopify/ERP/Search) on the highest-value terms.
Seed depth, not exhaustive — additive growth to the 500+/10,000+ scale target is ongoing work
(BL-2+), not a BL-1 claim.

## Scope

Authoring taxonomy *content* as data (JSON/YAML), plus the minimal loader/validator/catalog code
needed to load, structurally validate, and query it. Workstream: **TAX**.

## Out of Scope

- Any new schema, registry, mapping engine, or validation rule engine — those are Build-002/004/006's
  jobs, reused not rebuilt.
- Modifying `ai/eal/`, `ai/ear/`, `ai/ead/`, or `ai/attribute_distribution/` code (all frozen,
  read-only contracts to this Build).
- Real content for any domain other than Bakery this sprint (Flowers, Gifts, etc. per
  `docs/10_Taxonomy/Roadmap.md`'s own "Future domains, no timeline" — same additive-only extension
  pattern applies whenever a real business reason exists).
- Wiring the Vision Engine's structured-output parsing to this content (Sprint 2.3+/Build-008's job).

## Risks

- Real attribute counts at authoring time are unknown until BL-1 begins — the 500+/10,000+ scale
  target is a design target for the catalog's indexing (already dict-based, O(1) lookup), not a
  claim that BL-1 will author that many entries in one pass.
- `AttributeGroupModel.ear_namespace` is a plain string reference to EAR's `namespace` field, not
  cross-validated against a live EAR `Registry` in BL-0 (deliberately deferred, same pattern EAR
  itself used for `taxonomy_references` before this Build existed) — BL-1+ should decide whether to
  add that cross-validation once real content makes it meaningful.

## Technical Dependencies

`ai/eal/` (frozen, reused for `ExternalIdModel`), `ai/ear/` (frozen, `namespace` is the join key),
`docs/10_Taxonomy/` (the architecture this content is authored against, unmodified),
[VIG-010](../00_Governance/VIG-010-Execution-Protocol.md) (execution protocol).

## Architecture Gate

**AR-007** — "Review Enterprise Master Taxonomy content (Build-005)... Content matches Sprint 2.1's
architecture; no Category/Vocabulary contradicts an existing one" (Roadmap §09). Sought after BL-1
through BL-4 are complete — not after BL-0, which ships no content to review yet.

## Testing Strategy

Per-backlog-item `test_taxonomy.py` self-check (`python -m ai.taxonomy.test_taxonomy`, no
framework, `assert`-based), mirroring every other Build. BL-0's fixture is explicitly structural,
not real content (`ai/taxonomy/examples/catalog.json`'s own `_note` field states this).

## Rollback Strategy

Every backlog item is its own commit — a bad item reverts with `git revert` on its own commit. No
frozen module is touched, so rollback never risks Build-002/003/004.

## Success Criteria (Build-005 overall, not just BL-0)

Real Category tree + 4 domain Attribute Groups + 3 Controlled Vocabularies with real Terms
authored; every `AttributeGroup.ear_namespace` and cross-system label backed by real EAR/EAD data
where one exists; `ai.taxonomy` test suite green; AR-007 submission package prepared (verdict not
self-issued, per [VIG-010](../00_Governance/VIG-010-Execution-Protocol.md)); zero changes to
Build-002/003/004 code.

## Related Standards

[Enterprise Program Roadmap](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-005), [ADR 0006](../adr/2026-07-27-workstream-id-convention.md),
[VIG-010](../00_Governance/VIG-010-Execution-Protocol.md), [README.md](README.md).
