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

## Related

[CANONICAL_SOURCES.md](CANONICAL_SOURCES.md), [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md),
[REPOSITORY_MAP.md](REPOSITORY_MAP.md), [FILE_OWNERSHIP.md](FILE_OWNERSHIP.md),
[PHASE7_READY.md](PHASE7_READY.md).
