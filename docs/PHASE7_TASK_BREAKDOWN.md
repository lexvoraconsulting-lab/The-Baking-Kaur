# Phase 7 Task Breakdown

Every remaining task across Phases 0–6, organized into the 9 required categories. This is the
single source of task-level truth for Phase 7 — `PHASE7_EXECUTION_PLAN.md`,
`PHASE7_PRIORITY_MATRIX.md`, and `PHASE7_DEPENDENCIES.md` all reference task IDs from this document
rather than re-listing tasks.

## Critical

| ID | Task | Source |
|---|---|---|
| C-1 | Resolve the password-gate decision (unlock, or define a public-preview path) | `docs/AI_SEARCH_READINESS.md`, `docs/PHASE7_HANDOFF.md` |
| C-2 | Reconcile the two `CHANGELOG.md` files (root, stale since 2026-07-17, vs. `seo-audit/audit/CHANGELOG.md`, actively maintained through R0–R7/Phase 6) — a future reader or session could act on the stale one | This review, new finding |

## High

| ID | Task | Source |
|---|---|---|
| H-1 | Run real Lighthouse/PSI measurement once C-1 is resolved; re-baseline before further performance work | `docs/CORE_WEB_VITALS.md` R-9 |
| H-2 | Confirm FAQPage schema wiring on `page.faq-01.json` | `docs/AEO_READINESS.md` |
| H-3 | Resolve the `shine-trust.liquid` on/off decision (now known to gate ~214 KB combined CSS+JS) | `SEO_AUDIT_LEDGER.md` P2-26, `docs/PHASE7_HANDOFF.md` |
| H-4 | Manual Shopify Admin → Apps check on `sections/tbk-product.liquid`, then remove if clear | `docs/TEMPLATE_CENSUS.md`, `docs/FINAL_REPORT.md` |
| H-5 | Correct `docs/ARCHITECTURE.md`'s stale template count ("40 templates" — actual current count is 33, confirmed via `ls templates/`) | This review, new finding |

## Medium

| ID | Task | Source |
|---|---|---|
| M-1 | Internal-linking graph audit (builds on Sprint 2's hub-linking work) | `docs/GEO_READINESS.md` |
| M-2 | Content-chunking review beyond the product page's existing tabs | `docs/GEO_READINESS.md` |
| M-3 | Confirm WebSite schema includes a `SearchAction` (sitelinks search box eligibility) | `docs/GEO_READINESS.md` |
| M-4 | Reconcile root-level `PERFORMANCE_BASELINE.md` (claims some preview-theme Performance-API measurement) against `docs/PERFORMANCE_BASELINE.md` (explicitly static-only, no live measurement) — the two make different epistemic claims about what was measured | This review, new finding |
| M-5 | Add explicit cross-reference notes to root `DESIGN_SYSTEM.md`/`COMPONENT_LIBRARY.md`/`CONTENT_SYSTEM.md`/`COPY_GUIDELINES.md` pointing forward to their `design/*.md` counterparts (currently only `design/*.md` references back to root/business docs — the relationship isn't stated symmetrically) | This review, new finding |

## Low

| ID | Task | Source |
|---|---|---|
| L-1 | Back-fill exact dates for pre-2026-07 decisions in `docs/DECISIONS.md` (existing TODO, line 53) | `docs/DECISIONS.md` |
| L-2 | Add CI/linter/formatter config for `seo-ops/` scripts (existing TODO) | `docs/CODING_STANDARDS.md` |
| L-3 | Update root `SHOPIFY_ARCHITECTURE.md`'s font "perf debt" note — the `fonts.gstatic.com` preconnect gap it implicitly described is now fixed (P6.6), though the underlying render-blocking Google Fonts link itself remains | This review, new finding |

## Future

| ID | Task | Source |
|---|---|---|
| F-1 | Consolidate the 17 near-duplicate `card-product*.liquid` snippets | `docs/PERFORMANCE_AUDIT.md` F-2 |
| F-2 | `UndefinedObject`/`HardcodedRoutes` triage (77 combined Theme Check findings) | `docs/FINAL_REPORT.md` |
| F-3 | Critical-CSS extraction for `theme.css`/`base.css` (real visual-regression risk, needs the protected-module sign-off process) | `docs/PERFORMANCE_RECOMMENDATIONS.md` R-6 |
| F-4 | Handle optimization (`b158`, `hamper13`, `chNN` → keyword handles) — deliberately deferred per `CLAUDE.md`, full 8-step checklist required | `CLAUDE.md` |

## Out of Scope

| ID | Task | Why |
|---|---|---|
| O-1 | `design_handoff_shopify_product/` folder's `MissingAsset` findings | Non-live reference folder, outside the theme's actual root (Finding 5, `docs/LIQUID_ARCHITECTURE_AUDIT.md`) |
| O-2 | `MatchingTranslations` (1,126 findings) / `VariableName` (74 findings) | i18n-completeness and code-style categories — a different audit dimension entirely |
| O-3 | Variant option typos (`fruit-cocoktail`, `chocolate-moouse`) | Touching options risks deleting variants; needs a metaobject fix first, per `CLAUDE.md` |

## External Dependency

| ID | Task | Blocked on |
|---|---|---|
| E-1 | Real Lighthouse/PSI/CrUX measurement | Password gate (see C-1) |
| E-2 | AI/search crawler indexing | Password gate (see C-1) |
| E-3 | `sections/tbk-product.liquid`'s app-reference check | Shopify Admin → Apps access, not available in this environment |
| E-4 | B1 (Shop Policy refund/terms rewrite), B2 (empty Terms page) | Admin API write access (Shop Policy is an Admin-only surface) |
| E-5 | Merchant Center / Google Search Console verification and monitoring | External account credentials not available in this environment |
| E-6 | Google Business Profile review/reconciliation | External account credentials |

## Business Decision

| ID | Task | Decision needed |
|---|---|---|
| B-1 | Password gate (see C-1) | Unlock, define public-preview path, or keep gated |
| B-2 | `shine-trust.liquid` on/off (see H-3) | Turn the bundle/upsell widget on, or delete ~214 KB |
| B-3 | B4 (delivery-area list confirmation), B5 (duplicate-collection merchandising decision), B6 (Store Locator repurposing, sequenced after B4) | Real business input, not yet supplied |
| B-4 | Reviews — 0 verified reviews exist; fastest path is transcribing Google Business Profile reviews, best long-term is a verified-buyer app (Judge.me) | Business owner choice of path and timeline |
| B-5 | Photography — homepage hero is a temporary product shot, catalogue images carry watermarks | One studio shoot; a scheduling/budget decision |
| B-6 | FSSAI licence number — storefront claims "FSSAI approved" with no number shown | Business owner to supply the real number |

## Manual Verification

| ID | Task | Why manual |
|---|---|---|
| V-1 | `sections/tbk-product.liquid` app-reference check (same as E-3) | Requires live Shopify Admin access this environment lacks |
| V-2 | Live `content_for_header` third-party script inventory | Requires an authenticated live-page view-source, per `docs/PERFORMANCE_AUDIT.md` F-11 |
| V-3 | Full Theme App Extension block sweep | `docs/PERFORMANCE_AUDIT.md` F-15, not exhaustively confirmed |

## Related

[PHASE7_EXECUTION_PLAN.md](PHASE7_EXECUTION_PLAN.md), [PHASE7_DEPENDENCIES.md](PHASE7_DEPENDENCIES.md),
[PHASE7_PRIORITY_MATRIX.md](PHASE7_PRIORITY_MATRIX.md), [PHASE7_RISK_REGISTER.md](PHASE7_RISK_REGISTER.md),
[PHASE7_BLOCKERS.md](PHASE7_BLOCKERS.md).
