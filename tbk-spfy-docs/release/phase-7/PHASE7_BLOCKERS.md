# Phase 7 Blockers

Every blocker, categorized. Task IDs reference `docs/PHASE7_TASK_BREAKDOWN.md`.

## Business Decisions

| Blocker | Task | Detail |
|---|---|---|
| Password gate | B-1/C-1 | Intentional per `business/BUSINESS_MASTER.md` §16. Blocks all real measurement and crawl indexing. Highest-leverage decision in the whole program. |
| `shine-trust.liquid` on/off | B-2/H-3 | Pre-existing since 2026-07-18 (P2-26), now known to gate ~214 KB combined CSS+JS. |
| Delivery-area list, collection-cluster merchandising, Store Locator repurposing | B-3 | Needs real business input, not a technical question. |
| Reviews strategy | B-4 | 0 verified reviews exist; path (transcribe GBP reviews vs. install Judge.me) and timeline need an owner decision. |
| Photography | B-5 | Studio shoot needed; homepage hero is a temporary shot, catalogue images carry watermarks. Scheduling/budget decision. |
| FSSAI licence number | B-6 | Storefront claims "FSSAI approved" with no number — needs the business owner to supply it. |

## Credentials / External Access

| Blocker | Task | Detail |
|---|---|---|
| Shopify Admin → Apps access | E-3/V-1 | Needed to confirm `sections/tbk-product.liquid` has zero app dependencies before removal. |
| Admin API write access (Shop Policy pages) | E-4 | Blocks B1 (refund/terms rewrite) and B2 (empty Terms page) — these are Admin-only surfaces, not theme files. |
| Google Search Console credentials | E-5 | Not available in this environment; needed for crawl-status verification, sitemap submission monitoring. |
| Google Merchant Center credentials | E-5 | Not available; needed for product-feed/Shopping-listing verification. |
| Google Business Profile access | E-6 | Not available; needed for review reconciliation and listing-data verification. |

## Password Gate (called out separately per instruction, though it overlaps Business Decisions above)

The single largest cross-cutting blocker in this entire report. It simultaneously blocks:
- Real Core Web Vitals measurement (`docs/CORE_WEB_VITALS.md`)
- All AI/search crawler access (`docs/AI_SEARCH_READINESS.md`)
- Any Search Console/Merchant Center crawl-status verification (those tools need a publicly
  reachable — or at least crawler-reachable — site)

It does **not** block the architecture-level work already confirmed sound in Phase 6 (structured
data, semantic HTML, internal-linking review) — see `docs/PHASE7_DEPENDENCIES.md`'s "key insight."

## Manual Content Approval

| Blocker | Task | Detail |
|---|---|---|
| Any future SEO/GEO/AEO copy change | (Phase 7 scope generally) | Per `CLAUDE.md`'s standing rule: no rating, count, certification, or delivery promise ships without a source — every content change in Phase 7 needs the same verification discipline already established, not a new process. |

## Legal

No open legal blockers identified in this review. (The FSSAI number, above, is a trust/compliance
item, not a legal blocker per se — flagged under Business Decisions.)

## Technical

| Blocker | Task | Detail |
|---|---|---|
| Two conflicting `CHANGELOG.md` files | C-2 | Root-level file stale since 2026-07-17; `seo-audit/audit/CHANGELOG.md` is the one actually maintained through R0–R7/Phase 6. Needs reconciliation before Phase 7 adds more entries to either. |
| `docs/ARCHITECTURE.md`'s stale template count | H-5 | Claims 40 templates; actual current count (verified via `ls templates/`) is 33. |
| Two conflicting `PERFORMANCE_BASELINE.md` files | M-4 | Root version claims some preview-theme Performance-API measurement was attempted; `docs/` version explicitly states no live measurement was performed. Different epistemic claims about the same topic. |

## Architecture

| Blocker | Task | Detail |
|---|---|---|
| Root vs. `design/` duplicate-named documentation (`DESIGN_SYSTEM.md`, `COMPONENT_LIBRARY.md`, `CONTENT_SYSTEM.md`, `COPY_GUIDELINES.md`) | M-5 | Not a content conflict — `design/*.md` correctly declares itself downstream of `business/` and the root blueprint docs. But the relationship isn't stated symmetrically (root docs don't point forward to their `design/` refinements), creating a real risk that a future session edits the wrong file. |
| `sections/tbk-product.liquid` unreachable but unremoved | E-3/H-4 | Confirmed zero live rendering path since R3.5; removal blocked only on the external app-reference check. |

## Related

[PHASE7_TASK_BREAKDOWN.md](PHASE7_TASK_BREAKDOWN.md), [PHASE7_RISK_REGISTER.md](PHASE7_RISK_REGISTER.md),
[PHASE7_DEPENDENCIES.md](PHASE7_DEPENDENCIES.md), [PHASE7_EXECUTION_PLAN.md](PHASE7_EXECUTION_PLAN.md).
