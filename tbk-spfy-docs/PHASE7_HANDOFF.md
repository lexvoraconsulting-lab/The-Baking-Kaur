# Phase 7 Handoff — Enterprise SEO + GEO + AEO + AI Search Engineering

Generated 2026-07-31. This document is the entry point for whoever (or whichever session) starts
Phase 7. Read this first, then follow its pointers — don't re-derive what's already established.

## What's frozen and complete (never repeat)

- **Business Foundation, Brand System, Design System, Documentation System** — established in
  earlier phases, canonical in `business/`, `design/`, `docs/`.
- **Repository Cleanup R0–R7** — 9 commits, fully certified. Read `docs/FINAL_REPORT.md` if you
  need the detail; don't re-audit the Liquid architecture, don't re-run the orphan-snippet sweep,
  don't re-census the product templates.
- **Phase 6 Performance Engineering (P6.0–P6.7)** — audited and executed everything that met the
  "safe, deterministic, zero-behavior-change" bar. Read `docs/PERFORMANCE_FINAL_REPORT.md` for the
  full record. Don't re-run the static performance audit — it's done and current.

## What Phase 7 should NOT re-do

- Don't re-verify R0–R7's file removals (R1's 10 files, R3.5's template, R5's 11 snippets) — all
  independently re-verified as recently as R7's own certification pass.
- Don't re-audit images, pagination, or responsive-image usage — P6.1 confirmed these are already
  correct.
- Don't re-investigate the Uploadcare scripts or `shine-trust.liquid` from scratch — P6.5 already
  did the deep read; both are documented with their exact current status.

## Open items Phase 7 inherits (in priority order)

1. **The password-gate business decision.** This is the prerequisite for almost everything else in
   this list. See `docs/AI_SEARCH_READINESS.md` — no AI crawler, search engine, or lab performance
   tool can reach the real site until this is resolved. **Not an engineering task** — surface it to
   the business owner explicitly, don't work around it.
2. **Real Lighthouse/PSI measurement**, once #1 is resolved. See `docs/CORE_WEB_VITALS.md`'s R-9
   for exact instructions. Re-baseline before prioritizing further performance work.
3. **FAQPage schema confirmation** (`docs/AEO_READINESS.md`) — check whether `page.faq-01.json`'s
   content is wrapped in `FAQPage`/`Question`/`Answer` JSON-LD. Fast, low-risk, high-value if
   missing.
4. **`shine-trust.liquid` on/off business decision** (`SEO_AUDIT_LEDGER.md` P2-26) — now known to
   gate ~214 KB combined (78 KB CSS + 136 KB JS, per Phase 6's P6.5 trace). Surface to the business
   owner: turn the bundle/upsell widget on, or delete both the CSS and all 7 JS files.
5. **`sections/tbk-product.liquid`'s app-reference check** — needs a manual Shopify Admin → Apps
   review (external access this environment doesn't have). If confirmed clear, remove alongside
   the template already removed in R3.5.
6. **Internal-linking graph audit** (`docs/GEO_READINESS.md`) — builds on, doesn't repeat, the
   Sprint 2 hub-linking work already done.
7. **Content-chunking review** beyond the product page's existing tabs (`docs/GEO_READINESS.md`).
8. **17 near-duplicate `card-product*.liquid` snippets** (`docs/PERFORMANCE_AUDIT.md` F-2) — a
   dedicated future consolidation phase, high behavioral-equivalence risk, not urgent.
9. **`UndefinedObject`/`HardcodedRoutes` triage** (77 combined Theme Check findings) — carried over
   from `docs/FINAL_REPORT.md`'s own future roadmap, still untouched.
10. **The broader business roadmap already tracked in `CLAUDE.md`** — B1–B6 decisions, reviews,
    photography, FSSAI licence number, handle optimization. Unrelated to Phase 6/7 engineering
    work, but still open and worth surfacing if the business owner is available.

## Canonical documents for Phase 7 to start from

| Topic | Document |
|---|---|
| Overall repo state / R0–R7 | `docs/FINAL_REPORT.md` |
| Performance state | `docs/PERFORMANCE_FINAL_REPORT.md` |
| AEO architecture | `docs/AEO_READINESS.md` |
| GEO architecture | `docs/GEO_READINESS.md` |
| AI Search / crawler readiness | `docs/AI_SEARCH_READINESS.md` |
| Business facts (never guess, always read) | `business/BUSINESS_MASTER.md` |
| Brand/design constraints | `business/TBK_BRAND_GUIDELINES.md`, `design/DESIGN_SYSTEM.md` |
| Standing engineering rules | `CLAUDE.md` (protected product-page module, drafts-stay-drafts, no fabricated facts, etc.) |

## Standing rules that still apply in Phase 7

Everything in `CLAUDE.md`'s "Golden rules" section — the product page is still a protected module,
never invent business facts (ratings, GTINs, reviews, delivery promises), drafts stay drafts, never
guess Shopify IDs. Phase 7's SEO/GEO/AEO work will touch content and metadata directly — these
rules matter even more there than they did in Phase 6's code-only work.

## Related

[PERFORMANCE_FINAL_REPORT.md](PERFORMANCE_FINAL_REPORT.md), [FINAL_REPORT.md](FINAL_REPORT.md),
[AEO_READINESS.md](AEO_READINESS.md), [GEO_READINESS.md](GEO_READINESS.md),
[AI_SEARCH_READINESS.md](AI_SEARCH_READINESS.md).
