# Phase 7 Success Metrics

Measurable criteria for Phase 7 completion. Distinguishes what can be objectively measured today
from what depends on the password-gate decision (`docs/PHASE7_BLOCKERS.md` C-1).

## Measurable now (no external dependency)

| Metric | Current state | Target |
|---|---|---|
| Duplicate-filename documentation conflicts | 2 confirmed (`CHANGELOG.md`, `PERFORMANCE_BASELINE.md`) + 1 partial (design-doc cross-reference asymmetry) | 0 unresolved — each either merged, deprecated-with-pointer, or explicitly justified |
| Stale factual claims in canonical docs | 1 confirmed (`ARCHITECTURE.md`'s template count) | 0 — all counts/facts in canonical docs match current repo state |
| Unresolved TODOs in canonical docs | 2 (`DECISIONS.md`, `CODING_STANDARDS.md`) | 0, or explicitly re-flagged with a reason if still open |
| Theme Check error count | 1,161 (stable since P6.6, `docs/PERFORMANCE_FINAL_REPORT.md`) | No increase attributable to Phase 7 work; any decrease is a bonus, not a target (Phase 7 is SEO/GEO/AEO-focused, not another cleanup pass) |
| FAQPage schema wiring status | Unconfirmed | Confirmed (either present or a specific, documented gap) |
| Business decisions surfaced with a clear ask | Documented in `docs/PHASE7_BLOCKERS.md` but not yet formally presented to an owner | All 6 (B-1 through B-6) formally surfaced, each with a yes/no or multiple-choice framing |

## Measurable once the password gate is resolved (C-1)

| Metric | Current state | Target |
|---|---|---|
| Lighthouse Performance score (mobile) | Not measured | Real number recorded in `docs/CORE_WEB_VITALS.md`, replacing every proxy signal |
| Lighthouse Performance score (desktop) | Not measured | Real number recorded |
| LCP, CLS, INP, TTFB, FCP, TBT, Speed Index | Not measured | Real numbers for homepage, one product page, one collection page |
| Pages indexed by Google (Search Console) | 0 (site not crawlable) | Real count, once Search Console access exists and the site is crawlable |
| AI crawler access (GPTBot, ClaudeBot, Google-Extended, PerplexityBot) | Blocked entirely | `robots.txt` explicitly confirmed to allow (or deliberately disallow, if that's the business choice) each named crawler |

## Non-metrics (explicitly not targets, to avoid fabricated-improvement pressure)

Per this project's own standing rule ("do not claim improvements that cannot be measured"), Phase 7
must **not** report estimated Lighthouse score improvements, estimated ranking improvements, or
estimated AI-citation-rate improvements as if they were measured. Only the "measurable now" table
above and real post-unlock measurements count as reportable success metrics.

## How to report Phase 7 completion

A Phase 7 final report (mirroring `docs/PERFORMANCE_FINAL_REPORT.md`'s structure) should state,
for each metric above: the before value, the after value (or "still blocked, reason X" if
unmeasurable), and the evidence source. No metric should appear without one of those three states.

## Related

[PHASE7_ACCEPTANCE_CRITERIA.md](PHASE7_ACCEPTANCE_CRITERIA.md), [PHASE7_TASK_BREAKDOWN.md](PHASE7_TASK_BREAKDOWN.md),
[CORE_WEB_VITALS.md](CORE_WEB_VITALS.md).
