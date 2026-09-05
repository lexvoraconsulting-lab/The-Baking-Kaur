# Phase 7 Priority Matrix

Impact × Effort mapping for every task in `docs/PHASE7_TASK_BREAKDOWN.md`. Use this to sequence
work within each priority tier.

| Task ID | Task | Impact | Effort | Quadrant |
|---|---|---|---|---|
| C-1 | Password gate decision | Very High | Low (it's a decision, not a build) | **Do first** |
| C-2 | Reconcile 2 CHANGELOG.md files | Medium | Low | **Do first** |
| H-1 | Real Lighthouse/PSI measurement | High | Low (once C-1 resolved) | **Do next** |
| H-2 | FAQPage schema confirmation | Medium-High | Low | **Do next** |
| H-3 | `shine-trust.liquid` decision | Medium | Low (decision) / Medium (implementation after) | **Do next** |
| H-4 | `tbk-product.liquid` app check + removal | Low-Medium | Low | **Do next** |
| H-5 | Fix `ARCHITECTURE.md` template count | Low | Very Low | **Quick win** |
| M-1 | Internal-linking graph audit | Medium | Medium | **Schedule** |
| M-2 | Content-chunking review | Medium | Medium | **Schedule** |
| M-3 | WebSite `SearchAction` schema check | Low-Medium | Low | **Quick win** |
| M-4 | Reconcile 2 PERFORMANCE_BASELINE.md files | Low-Medium | Low | **Quick win** |
| M-5 | Cross-reference root design docs → `design/` | Low | Low | **Quick win** |
| L-1 | Backfill decision dates | Low | Low | **Backlog** |
| L-2 | CI/linter config | Low | Medium | **Backlog** |
| L-3 | Update `SHOPIFY_ARCHITECTURE.md` font note | Low | Very Low | **Quick win** |
| F-1 | Consolidate 17 card snippets | Medium (maintainability) | Very High | **Dedicated future phase** |
| F-2 | `UndefinedObject`/`HardcodedRoutes` triage | Medium | High | **Dedicated future phase** |
| F-3 | Critical-CSS extraction | High (if real) | High (visual-regression risk) | **After H-1 confirms it's worth the risk** |
| F-4 | Handle optimization | High (long-term SEO) | Very High (301s, QR audit, 8-step checklist) | **Dedicated future phase** |
| B-1…B-6 | Business decisions | Varies, all real | N/A (not an effort question) | **Surface to owner now, in parallel** |
| E-1…E-6 | External-access items | Varies | N/A (blocked on credentials) | **Request access now, in parallel** |
| V-1…V-3 | Manual verification items | Low-Medium | Low once access exists | **Bundle with E-3/E-5/E-6** |

## Quadrant definitions

- **Do first**: highest leverage, lowest effort, unblocks everything else. Start Phase 7 here.
- **Do next**: high value, low-to-medium effort, no external blocker once "Do first" items land.
- **Quick win**: very low effort, worth doing immediately regardless of sequencing, since they cost
  almost nothing and remove real (if minor) risk.
- **Schedule**: real value, real effort — needs a dedicated work session, not a quick pass.
- **Backlog**: low urgency, park until higher-value work is done.
- **Dedicated future phase**: effort or risk too high for Phase 7's own scope; needs its own
  planning cycle (mirroring how R0–R7 broke large cleanup into small, separately-approved steps).

## Recommended first week of Phase 7

1. C-1 (surface the password-gate decision to the business owner — this alone can take the longest
   calendar time since it's not an engineering task, so start it immediately)
2. C-2, H-5, M-3, M-4, M-5, L-3 (all "Quick win"/"Do first" documentation items — can be done in
   one session, in parallel with waiting on C-1)
3. H-2 (FAQPage schema check — fast, valuable, no dependency)
4. H-3, H-4 decisions surfaced to the business/technical owner in parallel with C-1

## Related

[PHASE7_TASK_BREAKDOWN.md](PHASE7_TASK_BREAKDOWN.md), [PHASE7_EXECUTION_PLAN.md](PHASE7_EXECUTION_PLAN.md),
[PHASE7_DEPENDENCIES.md](PHASE7_DEPENDENCIES.md).
