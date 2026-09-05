# Phase 7 Risk Register

Risks identified during the Phase 6.5 reconciliation review. Each includes evidence, impact, and
recommended mitigation. Task IDs reference `docs/PHASE7_TASK_BREAKDOWN.md`.

| Risk | Evidence | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| **A future session edits the stale root `CHANGELOG.md` instead of `seo-audit/audit/CHANGELOG.md`**, fragmenting the project's history further | Root `CHANGELOG.md` (36.7 KB, last modified 2026-07-17) exists alongside the actively-maintained `seo-audit/audit/CHANGELOG.md` — confirmed via file timestamps and content inspection | Medium — history becomes harder to reconstruct, future audits may miss real work | Medium — this exact ambiguity ("Update CHANGELOG.md") has already been interpreted consistently as the `seo-audit/audit/` path throughout R0–R7/Phase 6, but nothing prevents a future session from choosing differently | C-2: explicitly reconcile — either merge, deprecate one with a pointer comment, or document the split's rationale if intentional |
| **A future session edits root `DESIGN_SYSTEM.md`/`COMPONENT_LIBRARY.md`/`CONTENT_SYSTEM.md`/`COPY_GUIDELINES.md` believing it's current**, drifting further from the `design/*.md` versions that are actually referenced by the canonical hierarchy | `design/*.md` files explicitly declare `business/BUSINESS_MASTER.md → TBK_BRAND_GUIDELINES.md → design/*` as canonical; root files don't reference this hierarchy or point forward | Medium — brand/design guidance could fork into two inconsistent versions over time | Medium | M-5: add explicit forward-pointers from root docs to their `design/` counterparts |
| **Root `PERFORMANCE_BASELINE.md` and `docs/PERFORMANCE_BASELINE.md` make different claims about what performance measurement was actually attempted** | Root: "best-effort from the browser Performance API on the preview theme." `docs/`: "not a lab-measured report... no live measurement." | Low-Medium — could mislead Phase 7 into thinking real measurement already happened, or into distrusting real preview-theme data that may exist | Low | M-4: reconcile explicitly — determine which claim is accurate (was preview-theme Performance API data ever actually captured?) and correct the other |
| **`docs/ARCHITECTURE.md`'s template count (40) is stale** (actual: 33) | Verified via `ls templates/*.json templates/*.liquid` | Low — cosmetic, but any reader trusting this number for planning purposes gets a wrong count | High — confirmed already occurring | H-5: correct the count, note R3.5's removal as the most recent driver of the change |
| **`sections/tbk-product.liquid` remains in the repo, unreachable, pending an external check that has no owner or timeline assigned** | `docs/TEMPLATE_CENSUS.md`, `docs/FINAL_REPORT.md` | Low — dead code sitting indefinitely isn't harmful, but it's an open item with no forcing function | Medium — could sit unresolved indefinitely without a Phase 7 owner | H-4: assign an owner and a check-in point in Phase 7's execution plan |
| **`shine-trust.liquid` decision continues to sit unresolved** (now 2+ weeks since first flagged, 2026-07-18) | `SEO_AUDIT_LEDGER.md` P2-26 | Low-Medium — ~214 KB of either dead weight or a disabled real feature persists either way | Medium — has already gone unresolved across 3+ separate phases (SEO audit → R4/R5 → Phase 6) | H-3: escalate explicitly in Phase 7's kickoff, don't let it silently persist into Phase 8 |
| **The password gate blocks all verification of Phase 6's performance and Phase 6.5's SEO/GEO/AEO architecture claims** | `docs/CORE_WEB_VITALS.md`, `docs/AI_SEARCH_READINESS.md` | High for confidence, Low for actual site quality (the architecture is real and evidenced at the code level regardless) | Certain — already confirmed blocking | C-1: this is the single highest-priority item in the entire Phase 7 backlog |
| **Two unresolved TODOs in canonical docs** (`docs/DECISIONS.md` date backfill, `docs/CODING_STANDARDS.md` CI/linter gap) | Confirmed via grep | Low | Low | L-1, L-2: low-priority cleanup, not blocking |
| **Business-blocked items (B1–B6, reviews, photography, FSSAI) continue to accumulate across phases without a forcing function** | Carried in `CLAUDE.md`'s own roadmap section since before this review | Medium — the longer these sit, the more the "temporary" state (watermarked images, no FSSAI number, no reviews) reads as permanent to visitors | Medium | B-3 through B-6: Phase 7 should include an explicit check-in/escalation step, not just re-list these again |

## Overall risk posture

**No risk in this register is severe enough to block Phase 7 from starting.** The highest-impact
items (password gate, `shine-trust.liquid`) are already known, already documented, and already
correctly classified as business decisions rather than engineering gaps. The new findings from this
review (the two document-collision pairs, the stale template count) are real but low-severity —
documentation hygiene issues, not architectural flaws. They should be fixed early in Phase 7
(Track A in `docs/PHASE7_DEPENDENCIES.md`) precisely because they're cheap to fix now and would
compound if left through another phase.

## Related

[PHASE7_BLOCKERS.md](PHASE7_BLOCKERS.md), [PHASE7_TASK_BREAKDOWN.md](PHASE7_TASK_BREAKDOWN.md),
[PHASE7_PRIORITY_MATRIX.md](PHASE7_PRIORITY_MATRIX.md), [PHASE7_EXECUTION_PLAN.md](PHASE7_EXECUTION_PLAN.md).
