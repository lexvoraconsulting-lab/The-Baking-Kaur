# Phase 7 Execution Plan

Entry point for actually starting Phase 7. Reads alongside `docs/PHASE7_HANDOFF.md` (context) and
draws its task list, sequencing, and criteria from the other Phase 7 planning documents rather than
restating them.

## Plan structure

This plan does not re-list tasks — see `docs/PHASE7_TASK_BREAKDOWN.md` for the full list,
`docs/PHASE7_DEPENDENCIES.md` for what blocks what, `docs/PHASE7_PRIORITY_MATRIX.md` for
impact/effort sequencing, `docs/PHASE7_ACCEPTANCE_CRITERIA.md` for done-criteria, and
`docs/PHASE7_SUCCESS_METRICS.md` for how completion gets measured.

## Week 1 — Do-first + Quick-win tracks (parallel, no dependency conflicts)

Per `docs/PHASE7_PRIORITY_MATRIX.md`'s recommended first week:

1. **Surface C-1 (password gate) to the business owner** — start immediately, since it's not an
   engineering task and may take the longest calendar time of anything in this plan.
2. **Documentation reconciliation sweep** (C-2, H-5, M-3, M-4, M-5, L-3) — all low-effort, zero
   external dependency, can be done in one session. Verify via
   `find . -iname "*.md" | xargs -n1 basename | sort | uniq -d` before and after, per
   `docs/PHASE7_ACCEPTANCE_CRITERIA.md`'s overall-kickoff check.
3. **H-2 (FAQPage schema confirmation)** — fast, valuable, no dependency.
4. **Surface H-3 (`shine-trust.liquid`) and H-4 (`tbk-product.liquid`) decisions** in parallel with
   #1 — both are quick asks, don't wait for C-1 to resolve first.

## Week 2+ — Do-next track (once Week 1's quick items land)

5. Once C-1 resolves (or a public-preview path is agreed): **H-1, real Lighthouse/PSI measurement**
   — re-baseline before prioritizing any further performance work, per
   `docs/PERFORMANCE_ROADMAP.md`'s own P6.2 sequencing rationale, carried forward into Phase 7.
6. Execute whichever decision was made on H-3 (`shine-trust.liquid`) and H-4 (`tbk-product.liquid`)
   — both follow the established pull→diff→edit→push→re-pull→diff pattern.

## Ongoing / scheduled — Medium track

7. **M-1 (internal-linking audit)** and **M-2 (content-chunking review)** — schedule as dedicated
   work sessions, not squeezed into the quick-win week.

## Explicitly NOT in Phase 7's scope (future phases)

Per `docs/PHASE7_TASK_BREAKDOWN.md`'s Future/Out-of-Scope categories: the 17-card-snippet
consolidation (F-1), `UndefinedObject`/`HardcodedRoutes` triage (F-2), critical-CSS extraction
(F-3, gated on H-1's real data first), and handle optimization (F-4). None of these should be
pulled into Phase 7 opportunistically — each needs its own planning cycle, matching how R0–R7 broke
large cleanup into small, separately-approved steps.

## Execution discipline (carried forward, not reinvented)

Every code change in Phase 7 follows the same discipline established across R0–R7 and Phase 6:
pull → diff-confirm zero drift → edit → push (scoped `--only`, never an unscoped sync) → re-pull →
diff-confirm live → Theme Check before/after → update `seo-audit/audit/CHANGELOG.md` and
`AUDIT_LEDGER.md` → one commit per logical change. Content changes (once any business decisions
unblock them) follow `CLAUDE.md`'s standing rule: no rating, count, certification, or delivery
promise ships without a source.

## What triggers moving to Phase 8

Per `docs/PHASE7_ACCEPTANCE_CRITERIA.md`'s overall kickoff-acceptance section: every Phase 7 task
is either complete, explicitly deferred with a reason, or assigned to a named future phase; no new
documentation conflicts exist; the changelog/ledger are current. A Phase 7 final report (mirroring
`docs/PERFORMANCE_FINAL_REPORT.md`'s structure) should be generated at that point, per
`docs/PHASE7_SUCCESS_METRICS.md`'s reporting guidance.

## Related

[PHASE7_HANDOFF.md](PHASE7_HANDOFF.md), [PHASE7_TASK_BREAKDOWN.md](PHASE7_TASK_BREAKDOWN.md),
[PHASE7_DEPENDENCIES.md](PHASE7_DEPENDENCIES.md), [PHASE7_PRIORITY_MATRIX.md](PHASE7_PRIORITY_MATRIX.md),
[PHASE7_RISK_REGISTER.md](PHASE7_RISK_REGISTER.md), [PHASE7_BLOCKERS.md](PHASE7_BLOCKERS.md),
[PHASE7_ACCEPTANCE_CRITERIA.md](PHASE7_ACCEPTANCE_CRITERIA.md), [PHASE7_SUCCESS_METRICS.md](PHASE7_SUCCESS_METRICS.md).
