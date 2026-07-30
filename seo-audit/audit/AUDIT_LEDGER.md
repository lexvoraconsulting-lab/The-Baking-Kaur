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
| SEO-013 | Content SEO / GEO | **High** | Open | Verified | `page.faq-01.json`, `page.faq-02.json` | 12× each | — |
| SEO-014 | EEAT | Low | Open | Requires Manual Verification | `sections/footer.liquid` | 122 | — |
| SEO-015 | Local SEO | Medium | Open | Requires Manual Verification | `snippets/bk-local-business.liquid` | 44-46 | — |
| SEO-016 | EEAT | **Critical** | Open | Verified | header (`tbk_header_main`) | — | — |
| SEO-017 | Technical SEO | — | Open | Requires Manual Verification | 5 templates | — | — |
| SEO-018 | EEAT | — | Open | Requires Manual Verification | — | — | — |
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
| SEO-029 | Local SEO | Medium | Open | Verified | 3 files (1 now removed) | see issues.yml | — |
| SEO-030 | Content SEO | Low | Open | Verified | `templates/page.store-locations.json` | — | — |

## Reading this table

- **Fixed** rows are deployed live and re-verified byte-for-byte via a post-push theme pull/diff —
  see [CHANGELOG.md](CHANGELOG.md) for the deploy evidence per commit.
- **Open + Verified** rows are real, confirmed issues not yet fixed because the fix itself would
  require inventing content (SEO-013) or a business decision (SEO-016) — never silently resolved.
- **Open + Requires Manual Verification** rows need either a business fact (SEO-014, SEO-015,
  SEO-018) or a disconnected tool reconnecting (SEO-017, SEO-018) before they can be classified
  further.
- Full detail per category lives in `../schema/`, `../seo/`, `../ux/`, `../security/` — this ledger
  is the index, not a substitute for reading those.

## Related

[VERIFIED_ISSUES.md](VERIFIED_ISSUES.md), [MANUAL_VERIFICATION.md](MANUAL_VERIFICATION.md),
[CHANGELOG.md](CHANGELOG.md), [SCORECARD.md](SCORECARD.md), [../final/EXECUTIVE_REPORT.md](../final/EXECUTIVE_REPORT.md),
[../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md) (SEO-020/023/024 full detail).
