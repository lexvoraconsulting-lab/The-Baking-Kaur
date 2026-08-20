# Documentation Changelog

Record of every documentation-only change made during Phase 7.0's pre-flight reconciliation
(2026-07-31). This is a changelog *about the documentation itself*, distinct from both workstream
changelogs (`seo-audit/audit/CHANGELOG.md`, `CHANGELOG.md` root) — see `docs/FILE_OWNERSHIP.md`.

## 2026-07-31 — Phase 7.0 reconciliation

**Files edited** (all documentation, zero theme/production code changed):

| File | What changed | Why |
|---|---|---|
| `CLAUDE.md` | Corrected the roadmap section's claim that Phase A was "not promoted" | Commit `77861b3` (2026-07-14) and a fresh live pull-diff both confirm Phase A (`layout/theme.liquid`, `snippets/structured-data.liquid`, `sections/site-footer.liquid`, `sections/footer-group.json`) is live and in sync. Also noted design-token restoration (R0) is done. |
| `CHANGELOG.md` (root) | Added a scope-clarifying header; struck through (not deleted) the stale "staged, not yet deployed" line; fixed the Phase A section title to state it was promoted | The file's own later "PROMOTED TO LIVE (2026-07-14)" entry contradicted its own earlier header — an internal self-contradiction, now resolved. |
| `seo-audit/audit/CHANGELOG.md` | Added a matching scope-clarifying header | Establishes the two-changelog structure symmetrically. |
| `docs/PERFORMANCE_BASELINE.md` | Corrected an overstated claim that no live/runtime measurement had ever been attempted | The root `PERFORMANCE_BASELINE.md` contains real (if informal) preview-theme Performance-API data this document didn't know about. |
| `PERFORMANCE_BASELINE.md` (root) | Added a status note marking it the historical Phase-A-era baseline, pointing to `docs/PERFORMANCE_BASELINE.md` as current | Preserves the real historical data (per "never silently delete information") while resolving which is authoritative going forward. |
| `docs/ARCHITECTURE.md` | Corrected the template count (40 → 33) | Verified via `ls templates/*.json templates/*.liquid`; stale since at least R3.5's removal of `product.tbk.json`. |
| `SHOPIFY_ARCHITECTURE.md` (root) | Updated the font render-blocking note and the Uploadcare note with cross-references to Phase 6's actual findings | Both items were already correctly flagged by this pre-existing document; updated to reflect what Phase 6 found (font preconnect gap partially fixed; Uploadcare confirmed not a true duplicate) rather than leaving them looking unaddressed. |
| `DESIGN_SYSTEM.md`, `COMPONENT_LIBRARY.md`, `CONTENT_SYSTEM.md`, `COPY_GUIDELINES.md` (root, all 4) | Added a cross-reference pointer to each file's `design/` counterpart | Previously only `design/*.md` pointed back to these root files — the relationship wasn't stated symmetrically, risking a future session editing the wrong file. |

**Files created** (5 required deliverables + this one):

`docs/CANONICAL_SOURCES.md`, `docs/DOCUMENTATION_INDEX.md`, `docs/REPOSITORY_MAP.md`,
`docs/FILE_OWNERSHIP.md`, `docs/DOCUMENTATION_CHANGELOG.md` (this file), `docs/PHASE7_READY.md`.

**Files NOT touched, and why**: the `ai/` enterprise-attribute-system documentation tree (a
separate subsystem, its internal per-module duplication is intentional design, not a conflict
with the Shopify/SEO documentation this pass covers); the extensive Phase C1/S1–S8 homepage-build
entries within root `CHANGELOG.md` (real content, but re-auditing their current live/preview
status is a dedicated task of its own, out of this pass's documentation-hygiene scope — flagged in
`CLAUDE.md`'s updated roadmap note instead of silently assumed current).

**Verification performed**: full repo-wide duplicate-filename scan
(`find . -iname "*.md" | xargs -n1 basename | sort | uniq -d`); every hit read in full before
classification, not just filename-matched; a live pull-diff of all 4 Phase A files to confirm the
promotion claim; `git log`/`git show` on the Phase A promotion commit; git status clean at
commit time.

**No theme file, template, section, snippet, or asset was modified in this pass.**

## 2026-08-20 — Cake Intelligence documentation integration pass

Documentation only. **No production code, Shopify data, database, taxonomy content, or branch was
touched.** Scope: register six architecture documents produced by the preceding
discovery/reconciliation phase, repair cross-links, normalize terminology, and correct stale facts
found while doing so. This pass covers the `ai/` platform tree, which the 2026-07-31 pass above
explicitly scoped out.

**Files created (7)** — six accepted from the preceding discovery/reconciliation phase, plus the
module README this pass added to follow the `docs/N0_*/README.md` convention:

| File | Purpose |
|---|---|
| `docs/adr/2026-08-20-n8n-python-system-of-record.md` | ADR 0011 — ownership split, API boundaries, failure/retry/provenance/versioning |
| `docs/80_Dynamic_Structure_Discovery/SPECIFICATION.md` | Discovery/proposal specification, nine-state model, output contract |
| `docs/80_Dynamic_Structure_Discovery/README.md` | Module entry point, following the `docs/70_` README convention |
| `docs/AI/VisionExtractionContract.md` | Build-008 extraction contract — two-channel output |
| `docs/30_Enterprise_Program_Roadmap/ECP-200_Architecture_Gap_Analysis.md` | Current vs. required system, gap register X-1…X-15 |
| `docs/30_Enterprise_Program_Roadmap/IMPLEMENTATION_DEPENDENCY_MAP.md` | Work items D0–D15, dependency graph, critical path |
| `docs/00_Foundation/GLOSSARY.md` | Cross-program terminology, alias rulings |

**Files edited (9), all documentation** — seven pre-existing, plus in-pass corrections to three of
the newly created documents (ECP-200, the dependency map, and the glossary):

| File | What changed | Why |
|---|---|---|
| `docs/00_Foundation/FOUNDATION_v1.md` | §7 ADR index: added 0008, 0009, 0010, 0011. New §7A registering the six architecture/contract documents. §8: corrected the `ai/` package list and added `docs/70_`/`docs/80_`. §11: corrected Build-005 and Build-007 status | ADRs 0008–0010 (2026-08-02) were never indexed — registering 0011 alone would have left the list jumping 0007→0011. §8/§11 corrections made under this document's own §14 rule ("the linked source is correct and this document should be updated to match it") |
| `docs/30_Enterprise_Program_Roadmap/ECP-100_Architecture_Review.md` | Three in-place notes: §20's Cake Genome finding corrected, §15's empty-directory claim corrected, successor pointer to ECP-200 added | A closed review is not rewritten. Corrections are added beside the original text, per this repository's existing "correct in place, never delete" convention |
| `docs/CANONICAL_SOURCES.md` | New 2026-08-20 section: five platform-tree conflicts (system of record, Cake Genome naming, two taxonomies, empty-directory claims, Build-status staleness) | This is the file `FILE_OWNERSHIP.md` designates for exactly this |
| `docs/FILE_OWNERSHIP.md` | Ownership rows for FOUNDATION_v1, GLOSSARY, ECP-*, the dependency map, `docs/80_`, and the Vision Extraction Contract | New canonical documents need a designated owner before the next session edits the wrong one |
| `docs/DOCUMENTATION_INDEX.md` | Scope note now names FOUNDATION_v1 §7/§7A/§8 and GLOSSARY as the platform tree's own index | This index explicitly excludes the `ai/` tree. Forcing the six documents in would have violated its declared scope; pointing at the correct index respects both |
| `docs/AI/Roadmap.md` | Phase 2 now points at `VisionExtractionContract.md` | Registers the contract where Build-008's pending work is already described |
| `docs/00_Foundation/GLOSSARY.md` | Alias ruling section; removed a self-contradiction the ruling introduced | See terminology note below |
| `docs/30_Enterprise_Program_Roadmap/ECP-200_*.md` | Corrected an inherited empty-directory claim; added gap X-15 | The claim was inherited from ECP-100 and was wrong |
| `docs/30_Enterprise_Program_Roadmap/IMPLEMENTATION_DEPENDENCY_MAP.md` | Same correction in work item D15 | Same reason |

**Terminology normalized.** "TBK Cake Genome" registered as an accepted equivalent of "Cake
Genome™". "Cake Intelligence" / "TBK Cake Intelligence" registered as accepted **informal**
programme names that do **not** supersede "VISIONARY IMAGE GENOME™" —
[VIG-000](00_Governance/VIG-000-Constitution.md) establishes that name constitutionally and defines
its own amendment process; a documentation pass has no authority to invoke it. "Cake DNA" recorded
as not canonical and not to be introduced (zero occurrences repository-wide).

**Files deliberately NOT touched**: every VIG governance document (amending VIG-000's platform name
requires the constitutional amendment process, not a documentation pass); every frozen module spec
in `docs/10_`–`docs/70_` (no finding required changing one); `ai/**` source, `ai/taxonomy/content/`,
all n8n workflows and Data Tables, all theme files, `seo-ops/`; the storefront and SEO-audit
documentation trees (out of scope, separate programs).

**Verification performed**: relative-link resolution check across all 8 new and 9 edited files (0
broken); `git status` confirmed additions and documentation edits only; every "empty directory" and
Build-status claim re-verified against disk rather than against the document asserting it.

## Related

[CANONICAL_SOURCES.md](CANONICAL_SOURCES.md), [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md),
[REPOSITORY_MAP.md](REPOSITORY_MAP.md), [FILE_OWNERSHIP.md](FILE_OWNERSHIP.md),
[PHASE7_READY.md](PHASE7_READY.md).
