# Internal Linking Audit (Phase 7.1)

## Scope of this pass

A **light-touch** review, not the full internal-linking graph audit already scoped as its own
dedicated task (Phase 6.5's task M-1, `docs/PHASE7_TASK_BREAKDOWN.md` — "builds on, doesn't
repeat, Sprint 2's hub-linking work"). This document doesn't re-do or shrink that scoping decision;
it records what this pass specifically checked.

## What was checked

- **Redirect targets** (`docs/CRAWL_REPORT.md`): all 825 redirect targets point to either a real,
  live collection/product/page, or the homepage — none point to a dead or non-existent destination
  (every target referenced in the redirect data corresponds to a collection or product handle seen
  elsewhere in this project's own census work, or the homepage).
- **Anchor text pattern**: not sampled at scale this pass (would require rendering live pages,
  partially blocked by the password gate for a full site-wide sample).

## Orphan-page / orphan-collection risk — not resolved this pass

36 collections exist (verified, Admin API). Whether all 36 are actually linked from navigation or
any other page is **not verified in this pass** — this is exactly the scope of task M-1, already
correctly identified as needing a dedicated session rather than a quick check folded into this
phase. Restating the recommendation rather than attempting a shortcut version of it here.

## What this pass does recommend, concretely, for M-1's eventual execution

When M-1 runs: cross-reference the 36 collection handles (Admin API) against every `link_list`
referenced by the header/footer/mega-menu, and against every collection referenced by any
`sections/*.liquid` file's block settings (many homepage sections reference specific collections by
handle) — a collection appearing in neither list is a genuine orphan-collection candidate.

## Related

[TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md), [PHASE7_TASK_BREAKDOWN.md](PHASE7_TASK_BREAKDOWN.md)
(task M-1), [GEO_READINESS.md](GEO_READINESS.md) (internal-linking architecture, Phase 6).
