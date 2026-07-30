# Audit Ledger

Storefront (`thebakingkaur.com`) audit, 2026-07-29. This is the human-readable index over
[`../issues.yml`](../issues.yml), the machine-readable source of truth — update that file first,
this table is derived from it.

Never fabricated: every row is labeled **Verified** (confirmed via code inspection, Admin API data,
or a live/pulled-theme diff), **Estimated** (inferred, not directly confirmed), or **Requires Manual
Verification** (needs a tool, business input, or access this session didn't have).

| ID | Category | Severity | Status | Verification | File | Line | Fixed in |
|---|---|---|---|---|---|---|---|
| SEO-001 | EEAT | Critical | Fixed | Verified | `sections/main-product-premium-v2.liquid` | 647-648 | `52a3821` |
| SEO-002 | EEAT | Critical | Fixed | Verified | `sections/main-product.liquid` | 126-128 | `52a3821` |
| SEO-003 | EEAT | High | Fixed | Verified | `sections/main-product-premium.liquid` | 134-138 | `52a3821` |
| SEO-004 | EEAT | Medium | Fixed | Verified | `sections/tbk-footer.liquid` | 93, 364 | `52a3821` |
| SEO-005 | EEAT | Critical | Fixed | Verified | `sections/tbk-product.liquid` | 197-201 | `52a3821` |
| SEO-006 | EEAT | **Critical** | Fixed | Verified | `sections/tbk-product.liquid` | 275-305 | `52a3821` |
| SEO-007 | EEAT | Critical | Fixed | Verified | `sections/main-product-premium-v2.liquid` | 146 | `eaad74f` |
| SEO-008 | EEAT | Critical | Fixed | Verified | `sections/main-product-premium-v2.liquid` | 645 | `eaad74f` |
| SEO-009 | EEAT | Critical | Fixed | Verified | `sections/site-footer.liquid` | 114 | `eaad74f` |
| SEO-010 | Trust/Contact-Info | High | Fixed | Verified | `templates/page.contact-1.json` | 80 | `eaad74f` |
| SEO-011 | Trust/Contact-Info | High | Fixed | Verified | `templates/page.contact-2.json` | 159 | `eaad74f` |
| SEO-012 | Trust/Contact-Info | High | Fixed | Verified | `templates/page.our-store.json` | 69, 141, 213 | `eaad74f` |
| SEO-013 | Content SEO / GEO | Critical | **Fixed** | Verified | `page.faq-01.json` (live), `page.faq-02.json` (unused) | 12× | 2026-07-30 push |
| SEO-014 | EEAT | Low | Open | Requires Manual Verification | `sections/footer.liquid` | 122 | — |
| SEO-015 | Local SEO | Medium | **Partial** | Verified | 5 theme files (address/geo unified) | 44-46 | 2026-07-30 push |
| SEO-016 | EEAT | Critical | **Resolved** (already fixed live) | Verified | `header-group.json` (`tbk_header_main`) + `tbk-header.liquid` | — | pre-existing (`36e1b0c`) |
| SEO-017 | Technical SEO | — | **Resolved** | Verified | 5 templates → real assignments confirmed | — | — |
| SEO-018 | EEAT | — | **Resolved** | Verified | real counts: 113 customers, 24 orders | — | — |
| SEO-019 | Technical SEO | Medium | Open | Requires Manual Verification | `sitemap.xml` | — | — |
| SEO-020 | Schema | Low | Fixed | Verified | `tbk-schema-website.liquid` vs `bk-local-business.liquid` | — | `4d23a2e` |
| SEO-021 | Schema | Low | Open | Requires Manual Verification | `snippets/tbk-schema-article.liquid` | 8-9 | — |
| SEO-022 | Technical SEO | — | **Resolved** (context, not a defect) | Verified | — | — | — |
| SEO-023 | Schema | **Critical** | Fixed | Verified | `structured-data.liquid` + 2 product templates | see issues.yml | `4d23a2e` |
| SEO-024 | Schema | Medium | Fixed | Verified | `layout/theme.liquid` | 68-157 | `4d23a2e` |
| SEO-025 | Technical SEO | Low | Open | Verified | `layout/theme.liquid` | 171 | — |
| SEO-026 | Core Web Vitals | Medium | Fixed | Verified | `snippets/tbk-gallery.liquid` | 4 | `edf458f` |
| SEO-027 | Local SEO / Trust | **High** | Fixed | Verified | `sections/header-group.json` | 176, 242 | `21457ec` |
| SEO-028 | Trust/Contact-Info | Medium | Fixed | Verified | `sections/header-e-commerce.liquid` | 484 | `21457ec` |
| SEO-029 | Local SEO | Medium | **Partial** | Verified | 5 theme files unified; 2 Admin-only surfaces remain | see issues.yml | 2026-07-30 push |
| SEO-030 | Content SEO | **High** | **Mitigated** | Verified | `templates/page.store-locations.json` | — | (page unpublished via API) |
| SEO-031 | Content SEO / EEAT / Legal | **Critical** | Open | Verified | 2 custom pages + 4 Shop Policies (contradictory) | — | — |
| SEO-032 | EEAT | Critical | **Fixed** | Verified | Page 116138016937 (eggless page) | — | 2026-07-30 Admin write |
| SEO-033 | Technical SEO / Contact-Info | High | **Fixed** | Verified | `templates/page.contact-2.json` | 69 | 2026-07-30 push |
| SEO-034 | Legal / EEAT | High | Open | Verified | Page 110844510377 (Terms and Conditions, empty body) | — | — |
| SEO-035 | Local SEO | Medium | Open | Verified | `site-footer.liquid` vs. delivery page (area-list conflict) | 276 | — |
| SEO-036 | Address / Coordinates | Medium | **Partial** | Verified | 2 schema files now use Admin billing-address coordinates | 44-45 | 2026-07-30 push |

## Implementation Backlog progress (tracked by task ID, not SEO-NNN)

`IMPLEMENTATION_BACKLOG.md`'s tasks aren't individually numbered SEO-NNN audit findings, so their
progress is tracked here separately rather than added as fabricated ledger rows.

| Task | Sprint | Status | Notes |
|---|---|---|---|
| 2.1 (header nav wiring) | 2 — Navigation | **Done**, 2026-07-30 | `main-menu`'s "Categories" item converted to a 6-collection dropdown via `menuUpdate` (Admin API navigation content, no theme file edited). See `CHANGELOG.md` for verification detail. |
| 2.4 (about-us-menu broken link) | 2 — Navigation | **Done**, 2026-07-30 | Removed "Store Locations" item (pointed at the unpublished fake Store Locator page) via `menuUpdate`. See `CHANGELOG.md`. |
| 2.2 (meerut-delivery menu) | 2 — Navigation | **Partial**, 2026-07-30 | Populated with the 3 existing published delivery-mode pages via `menuUpdate`. Hub item and live-section wiring remain blocked/out of scope — see `CHANGELOG.md`. |
| 2.6 (FAQ/delivery/eggless cross-links) | 2 — Navigation | **Done**, 2026-07-30 | Added FAQ links from `cake-delivery-in-meerut` and the eggless page (via `pageUpdate`), and topic links from the FAQ's Delivery/Eggless/Hampers Q&A back out (via theme push, `page.faq-01.json`/`page.faq-02.json`). See `CHANGELOG.md`. |
| 2.7 (hamper cluster cross-links) | 2 — Navigation | **Done**, 2026-07-30 | The 3 location-specific hamper pages now link to the Gift Hampers hub and each other; the hub now links to all 3 (via 4 `pageUpdate` calls). See `CHANGELOG.md`. |
| 2.8 (Gift Hampers "Related Collections" links) | 2 — Navigation | **Done**, 2026-07-30 | All 6 plain-text collection names converted to real links via `pageUpdate`. See `CHANGELOG.md`. |
| B1 (SEO-031, refund/terms policy rewrite) | 1 — Critical Fixes | **Blocked**, 2026-07-30 | Shop Policies are Admin-API-only (not theme files); the Shopify MCP connector disconnected mid-session with no fallback token configured. Cannot execute. See `CHANGELOG.md`/`IMPLEMENTATION_SUMMARY.md`. |
| B2 (SEO-034, empty Terms page) | 1 — Critical Fixes | **Blocked**, 2026-07-30 | Admin-API-only (Page body), also gated on B1. Same tooling blocker as B1. |
| B3 (SEO-015/029/036, address/geo) | 1 — Critical Fixes | **Partial**, 2026-07-30 | Theme-file portion (5 files) completed and deployed — see SEO-015/029/036 rows above. Admin-only portion (Refund policy page body, Shop Policy Contact Information) blocked by the same tooling issue. |
| B4 (SEO-035, delivery-area list) | 1 — Critical Fixes | **Blocked**, 2026-07-30 | No confirmed real area list was supplied; the approved recommendation was to go confirm one against logistics data, not a concrete list to write. Not guessed. |
| B5 (duplicate collection cluster) | 1 — Critical Fixes | **Blocked**, 2026-07-30 | Needs actual merchandising picks (not supplied) and Admin API (down) for execution either way. |
| B6 (SEO-030, Store Locator fate) | 1 — Critical Fixes | **Blocked**, 2026-07-30 | Explicitly sequenced after B4, which is blocked. |

**Sprint 2 (Navigation) status: complete for all in-scope tasks.** 2.3 and 2.5 skipped (hard-blocked
on Sprint 1's unmade policy-terms decision, per explicit instruction not to route around unmade
Sprint 1 decisions). Not continuing to Sprint 3 automatically, per instruction.

## Reading this table

- **Fixed** rows are deployed live and re-verified byte-for-byte via a post-push theme pull/diff —
  see [CHANGELOG.md](CHANGELOG.md) for the deploy evidence per commit.
- **Open + Verified** rows are real, confirmed issues not yet fixed because the fix itself would
  require inventing content or a business decision (SEO-029, SEO-031, SEO-034, SEO-035, SEO-036) —
  never silently resolved. SEO-013, SEO-016, SEO-032, SEO-033 were in this category until 2026-07-30,
  when real, evidence-based fixes shipped for each — see CHANGELOG.md.
- **Open + Requires Manual Verification** rows need either a business fact (SEO-014, SEO-015,
  SEO-018) or a disconnected tool reconnecting (SEO-017, SEO-018) before they can be classified
  further.
- Full detail per category lives in `../schema/`, `../seo/`, `../ux/`, `../security/`, and
  `../final/` (ADDRESS_AUDIT.md, POLICY_CONSOLIDATION.md, DELIVERY_AREA_SPEC.md, EEAT_REPORT.md,
  LOCAL_SEO_ROADMAP.md, CONTENT_PLAN.md) — this ledger is the index, not a substitute for reading
  those.

## Related

[VERIFIED_ISSUES.md](VERIFIED_ISSUES.md), [MANUAL_VERIFICATION.md](MANUAL_VERIFICATION.md),
[CHANGELOG.md](CHANGELOG.md), [SCORECARD.md](SCORECARD.md), [../final/EXECUTIVE_REPORT.md](../final/EXECUTIVE_REPORT.md),
[../final/BUSINESS_DECISION_IMPLEMENTATION.md](../final/BUSINESS_DECISION_IMPLEMENTATION.md),
[../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md) (SEO-020/023/024 full detail).
