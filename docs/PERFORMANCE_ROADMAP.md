# Performance Roadmap (Phase 6)

Phased plan following P6.0's audit (`docs/PERFORMANCE_AUDIT.md`,
`docs/PERFORMANCE_RECOMMENDATIONS.md`). **P6.0 (this phase) is audit-only — complete.** No
optimization work has been implemented yet; the phases below are proposed, pending approval.

## P6.0 — Enterprise Performance Audit (this phase, complete)

Deliverables: `PERFORMANCE_BASELINE.md`, `PERFORMANCE_AUDIT.md`, `PERFORMANCE_RECOMMENDATIONS.md`,
`CORE_WEB_VITALS.md`, `PERFORMANCE_SCORECARD.md`, this roadmap. `CHANGELOG.md`/`AUDIT_LEDGER.md`
updated. No code changed.

## P6.1 — Safe, zero-behavior-change fixes (proposed next sprint)

Scope: **only** R-1 and R-2 from `docs/PERFORMANCE_RECOMMENDATIONS.md` — the two findings that meet
this phase's own "safe, deterministic, no behavior change" bar:

1. Add the missing `fonts.gstatic.com` preconnect to `layout/theme.liquid`.
2. Remove the duplicate `uploadcare.full.min.js` script tag.

Both purely additive/subtractive with zero UX risk. Same deploy-safety pattern as R0–R7: pull →
diff-confirm → edit → push (scoped `--only`) → re-pull → diff-confirm → Theme Check before/after.

**Also in P6.1's scope, as investigation (not code change)**:
- R-4: trace the `shine-trust-v4-*.js` files' actual reference paths.
- R-8: full Theme App Extension block sweep.
- R-3: check for a synchronous-dependency on Uploadcare's global before adding `defer`.

## P6.2 — Real measurement (should happen as early as possible, ideally before P6.3)

R-9 and R-10: a real Lighthouse/PageSpeed Insights run (mobile + desktop, 3 page types) plus a
DevTools Coverage run, once the storefront is reachable by an authenticated session. This replaces
every proxy risk signal in `docs/PERFORMANCE_AUDIT.md` with real numbers and should reprioritize
everything after it. **Recommended before committing significant engineering time to P6.3's
higher-effort items**, so effort isn't spent optimizing something the real data doesn't support.

## P6.3 — Business-decision-gated and higher-complexity work (pending approval, sequenced by real data from P6.2)

- R-5: resolve the `shine-trust.liquid` on/off decision (business/product owner).
- R-6: critical-CSS extraction for `theme.css`/`base.css` — requires visual regression testing and
  extra sign-off given the protected product-page module.
- R-7: live `content_for_header` third-party script inventory.

## P6.4 — Future, out of this program's current scope

- R-11: consolidate the 17 near-duplicate `card-product*.liquid` snippets (maintainability, not
  runtime performance) — a dedicated phase given the 17-way behavioral-equivalence risk.
- A dedicated `assets/` audit (already flagged as future work in `docs/FINAL_REPORT.md`'s own
  roadmap, R0–R7 series) — unused/duplicate/superseded stylesheet and script cleanup beyond what
  P6.1's two fixes address.
- `UndefinedObject`/`HardcodedRoutes` triage (77 combined Theme Check findings, carried over from
  `docs/FINAL_REPORT.md`'s own future roadmap) — correctness issues with indirect performance
  relevance (e.g., an undefined-object reference that silently no-ops vs. one that should render
  something), not addressed in this performance phase.

## Sequencing rationale

P6.1 first because it's zero-risk and immediately actionable. P6.2 next, deliberately *before*
P6.3's heavier items, because real measurement should determine whether R-6's visual-regression
risk is even worth taking — if real Lighthouse data shows FCP/LCP are already acceptable, R-6 may
not be worth its risk at all. This ordering avoids optimizing based on proxy signals when real data
will soon be available.

## Related

[PERFORMANCE_AUDIT.md](PERFORMANCE_AUDIT.md), [PERFORMANCE_RECOMMENDATIONS.md](PERFORMANCE_RECOMMENDATIONS.md),
[PERFORMANCE_SCORECARD.md](PERFORMANCE_SCORECARD.md), [PERFORMANCE_BASELINE.md](PERFORMANCE_BASELINE.md),
[CORE_WEB_VITALS.md](CORE_WEB_VITALS.md), [FINAL_REPORT.md](FINAL_REPORT.md) (R0–R7 series' own
future roadmap, referenced above where it overlaps).
