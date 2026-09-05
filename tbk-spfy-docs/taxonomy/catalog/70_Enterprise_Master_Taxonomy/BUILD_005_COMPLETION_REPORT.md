# Build-005 Completion Report — Enterprise Master Taxonomy

Workstream: **TAX**. Date: 2026-07-29. Status: **Frozen** — all 5 backlog items (BL-0 through BL-4)
done, committed, and verified.

## Executive Summary

Build-005 authored the platform's first real Enterprise Master Taxonomy — the content EAR
(Build-002) and EAD (Build-003) have referenced as an opaque, unresolvable pointer since they were
built. Delivered as a six-entity content model (`Category`, `AttributeGroup`, `Vocabulary`, `Term`,
`TaxonomyAttribute`, `Relationship`) plus one real Bakery-domain content file: 6 Categories, 30
Attribute Groups, 26 Attributes, 17 Controlled Vocabularies, 96 Terms, 24 typed Relationships.
Zero changes to any frozen Build (EAL, EAR, EAD, Attribute Distribution) across all five backlog
items — verified by `git show --stat` on every commit, not assumed.

Four real architecture conflicts were found and resolved *before* implementation across this
Build's five items, never silently — see each backlog item's own charter section for the specific
evidence and resolution:
1. BL-0's originally-proposed 8-item backlog collided with Build-002/004/006's already-built or
   already-planned responsibilities.
2. BL-1's ~53-item scope-expansion request was sorted into existing-groups / new-groups /
   vocabulary-terms / out-of-taxonomy, with the 13 out-of-taxonomy items logged in
   `CROSS_SYSTEM_OWNERSHIP.md` rather than built.
3. BL-2's "Parent Category" / single "Attribute Group" field request conflicted directly with
   `Hierarchy.md`'s explicit reusability principle; rejected, enforced by a dedicated test.
4. BL-3's six "Label" relationship types conflicted with the already-built `Term.external_ids`
   mechanism; rejected as duplicate models, applying the same reuse decision BL-2 established.

## Backlog Items Delivered

| Item | Description | Status | Commit |
|---|---|---|---|
| BL-0 | Repository preparation — `ai/taxonomy/` skeleton (4 entities), `docs/70_Enterprise_Master_Taxonomy/` skeleton | Done | `0545f2e` |
| BL-1 | Real Bakery-domain content — 6 Categories, 29→30 Attribute Groups, 15 Attributes, 6 Vocabularies, 43 Terms; 5th entity `TaxonomyAttribute` | Done | `f5575de` |
| BL-2 | 11 new Controlled Vocabularies, 55+ new Terms, flagship fully-enriched term (Rose Gold) — zero schema changes | Done | `0bc6ad0` |
| BL-3 | 6th entity `Relationship` (10 types), 24 real relationships, Vision-to-Knowledge-Graph chain documented | Done | `9a57980` |
| BL-4 | Verification, freeze, this report | Done | *(this commit)* |

## Traceability Matrix

| Backlog Item | Requirement Source | Implementation | Tests | Documentation |
|---|---|---|---|---|
| BL-0 | User Sprint Charter request, narrowed after conflict review | `ai/taxonomy/{models,models_pydantic,ids,validation,catalog,loader,exporter,__init__}.py` | `test_taxonomy.py` (13 checks) | `SPRINT_CHARTER.md`, `TAXONOMY_SPECIFICATION.md`, `README.md` |
| BL-1 | "10-year enterprise scope" content request, reconciled to 25 legitimate items | `content/bakery_v1.json` categories/groups/attributes; `TaxonomyAttribute` entity | +7 checks (20 total) | `SPRINT_CHARTER.md` BL-1 section, `CROSS_SYSTEM_OWNERSHIP.md` |
| BL-2 | "First real Controlled Vocabulary" request, 19 vocabularies | `content/bakery_v1.json` vocabularies/terms | +4 checks (24 total) | `SPRINT_CHARTER.md` BL-2 section, spec's `external_ids` convention table |
| BL-3 | "Enterprise Relationship Layer" request | `Relationship` entity, `content/bakery_v1.json` relationships | +8 checks (32 total) | `SPRINT_CHARTER.md` BL-3 section, spec's Relationship + Vision-chain sections |
| BL-4 | "Freeze Build-005" request | Verification only, no code | Full regression re-run | This report |

## Technical Summary

Six-entity content model, dataclass + Pydantic split (mirroring EAL/EAR/EAD's established pattern),
sequential single-allocator IDs (`TAX-{CAT,GRP,VOC,TERM,ATTR,REL}-NNNNNN`), dict-indexed
`TaxonomyCatalog` container for O(1) lookup at the stated 500+/10,000+ scale target, whole-catalog
validation running at construction (a `TaxonomyCatalog` that exists is guaranteed internally
consistent). Cross-system labels (Vision/Shopify/ERP/SEO/Search/Google Merchant) live exclusively in
`Term.external_ids`, reusing `ai.eal.models_pydantic.ExternalIdModel` directly — never duplicated as
dedicated fields, even under three separate requests to do so.

## Architecture Summary

`ai/taxonomy/` reuses EAL's `ExternalIdModel` and `DataType` directly; joins to EAR via a plain,
deliberately-unvalidated string (`ear_namespace`) — never registers into EAR, never modifies it.
Zero coupling to EAD or Build-004's distribution engine (both remain untouched). Relationship cycle
detection is scoped to the three hierarchical/transitive types only (`IS_A`, `PART_OF`,
`BELONGS_TO`); associative types are exempt by design, verified by a dedicated test. Category-tree
cycle safety is *not* structurally enforced by `validate_catalog()` (only `parent_id` resolution
is) — verified ad-hoc as acyclic for the real content during this freeze pass (see Known
Limitations).

## Files Created (across the whole Build)

`ai/taxonomy/` (14 files: 9 modules, 6 schemas, 1 example fixture, 1 real content file, 1 test
suite), `docs/70_Enterprise_Master_Taxonomy/` (5 files: README, Sprint Charter, Specification,
Cross-System Ownership, this Completion Report).

## Files Modified

`docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md` (Build-005 status, five
times, once per backlog item), `docs/10_Taxonomy/Roadmap.md` (Sprint 2.2 status, once).

## Files Deleted

None.

## Database / API / Configuration Changes

None — this Build produces no live database, no API endpoint, no runtime service.

## Dependencies Added / Removed

None — reuses `pydantic`/`PyYAML` already in `requirements.txt` since Build-004.

## Tests Executed

`python -m ai.taxonomy.test_taxonomy` → `OK`, 32 checks (0 in BL-0's initial commit → 13 → 20 → 24 →
32, growing with each backlog item, never shrinking or skipped). Full regression
(`ai.eal`/`ai.ear`/`ai.ead`/`ai.attribute_distribution`/`ai.taxonomy`) re-run at the end of every
single commit across all five backlog items, always green.

## Coverage

Every public function in `ai/taxonomy/` is exercised by at least one test. Real content
(`bakery_v1.json`) is loaded, validated, and spot-checked by dedicated tests for each backlog item's
own claims (e.g. `test_bl2_shape_vocabulary_reused_across_two_groups`,
`test_real_content_relationships_load_and_resolve`).

## Performance Impact

None measured or claimed — no live service exists to measure. `TaxonomyCatalog`'s dict-indexed
design is a forward-looking choice for the stated 500+/10,000+ scale target, not a benchmarked
result at today's 199-entry catalog.

## Security Impact

None — no network calls, no credentials, no external I/O anywhere in `ai/taxonomy/` (same
dry-run/no-live-write posture as Build-004).

## Known Limitations

- **Category-tree cycle safety is not structurally enforced.** `validate_catalog()` checks
  `parent_id` resolves to a real Category but does not run cycle detection over the Category tree
  the way it does for hierarchical Relationship types. Verified acyclic for the current 6-node real
  tree via an ad-hoc script during this freeze pass, not by the codebase itself. Recommended
  addition for a future backlog item if the Category tree grows large enough for manual review to
  stop being sufficient.
- **7 Attribute Groups have zero authored Attributes** (`Classification`, `Material`, `Business`,
  `Topper`, `Size`, `Flavour`, `Allergens`) — found during this freeze pass's orphan detection.
  Expected and consistent with "seed depth, not exhaustive" (stated at every backlog item); not a
  defect, just unauthored content, tracked as Future Work below.
- `AttributeGroup.ear_namespace` and `TaxonomyAttribute.ear_namespace` remain plain, unvalidated
  string join keys to EAR — never cross-checked against a live EAR `Registry` (deliberate, same
  deferral EAR itself used before this Build existed).

## Known Risks

Unchanged from BL-0: Kitchen ERP's real API remains uninspected (EPR Risk R-3); this taxonomy's
`erp`-system `external_ids` are illustrative, not verified against a real ERP schema.

## Repository Health Assessment (Build-005 scope)

| Check | Result | Evidence |
|---|---|---|
| Full regression | ✅ | 5/5 suites green, re-run this pass |
| Taxonomy suite | ✅ | 32/32 checks, `OK` |
| JSON validity | ✅ | Both `examples/catalog.json` and `content/bakery_v1.json` parse and load |
| ID uniqueness | ✅ | All 6 entity types, 199 total entries, zero duplicates (explicit re-check this pass) |
| Category tree acyclic | ✅ | Ad-hoc verified this pass (see Known Limitations for why it's not structural) |
| Relationship integrity | ✅ | All 24 relationships resolve; enforced at load by `validate_catalog()` |
| No frozen Build modified | ✅ | `git show --stat` on all 4 code-bearing commits, zero hits in `ai/eal\|ear\|ead\|attribute_distribution` |
| Cross-reference sweep | ✅ | 9 known false positives, unchanged across every pass this Build |
| Doc/implementation consistency | ✅ | Catalog counts (6/30/26/17/96/24) identical across README, Sprint Charter, Specification, Roadmap |

## Audit Cross-Reference

Repository/Architecture/Testing audits: see Repository Health Assessment above. Dependency audit:
see Dependencies Added/Removed (none). Security audit: see Security Impact (none — no I/O).
Documentation audit: see Doc/implementation consistency row above.

## Rollback Procedure

Every backlog item is its own commit (`0545f2e`, `f5575de`, `0bc6ad0`, `9a57980`, plus this report's
commit) — any one reverts independently with `git revert` without affecting the others or any other
Build. No live system holds Build-005 state, so there is no external rollback surface.

## Future Work

- Author real content for the 7 currently-empty Attribute Groups, as real business need is
  confirmed (per `VIG-001`/`Inheritance.md`'s "no speculative scaffolding" principle — not before).
- Deepen vocabulary coverage generally toward the 500+/10,000+ scale target — ongoing content
  operations, not a single future backlog item.
- Genuine Image-to-Object relationships (Build-008's real instance data, not yet available).
- Consider adding structural Category-tree cycle detection to `validate_catalog()` if the tree grows
  past what manual review can verify.
- Multilingual label support and per-term AI confidence — both explicitly deferred, noted in
  `TAXONOMY_SPECIFICATION.md`.

## Recommended Next Step

Architecture Gate **AR-007** ("Review Enterprise Master Taxonomy content (Build-005)... Content
matches Sprint 2.1's architecture; no Category/Vocabulary contradicts an existing one" — Roadmap
§09). Per this platform's standing practice, the verdict is not self-issued here; a submission
package (mirroring `AR011_GATE_PACKAGE.md`'s pattern) is a good candidate for a future,
separately-approved task if desired — not assumed as part of this freeze.

## ADR Updates

None required — no naming collision, no architecture decision requiring a new ADR surfaced during
Build-005. Every conflict found was resolved by scope reconciliation (documented in the Sprint
Charter) or by reuse of an existing mechanism, neither of which VIG-009 requires a new ADR for.

## Documentation Updated (this item, BL-4)

This report (new), `SPRINT_CHARTER.md` (status → frozen), `README.md` (status → frozen).

## Commit Summary

`0545f2e` BL-0, `f5575de` BL-1, `0bc6ad0` BL-2, `9a57980` BL-3, plus this commit for BL-4. Five
commits total, each independently reviewable and revertible.
