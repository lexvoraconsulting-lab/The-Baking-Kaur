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

**Re-verified 2026-07-30 (Phase 4)**: all 6 rows above unchanged — Shopify MCP still disconnected, no
`SHOPIFY_TOKEN` fallback, no new business input for B4/B5. B3's 5 files re-pulled and confirmed still
live. See `SPRINT_REPORT.md` for the full re-verification record.

| R0 (design-token render restoration) | Phase 5 — Liquid Architecture Refactor | **Done**, 2026-07-31 | Added `render 'tbk-tokens'` and `render 'tbk-components'` to `layout/theme.liquid` — previously rendered only by `layout/password.liquid`, leaving 177 real `var(--tbk-*)` references across 3 confirmed-live sections undefined on every real storefront page. Purely additive, no theme file other than `theme.liquid` touched. See `CHANGELOG.md` and `docs/LIQUID_ARCHITECTURE_AUDIT.md` (Finding 0). |
| R1 (remove confirmed-dead `-hulkapps-backup` files) | Phase 5 — Liquid Architecture Refactor | **Done**, 2026-07-31 | Removed 10 files (5 sections, 5 snippets) with zero references confirmed by both a repo-wide grep and Theme Check's `OrphanedSnippet` detector. Deployed via a scoped `--only` push, deliberately avoiding an unscoped sync after discovering 3 unrelated pre-existing drifts (`layout/password.liquid`, `sections/main-password.liquid`, `sections/tbk-header.liquid`) that an unscoped delete-enabled push would have silently overwritten. All 3 confirmed untouched post-deployment. `rewind_menu_backup_do_not_delete` and the disabled-but-referenced `header-menu-bottom-hulkapps-backup` explicitly excluded (deferred to R2). See `CHANGELOG.md`. |
| R2 (`header-menu-bottom-hulkapps-backup` disposition) | Phase 5 — Liquid Architecture Refactor | **Decided: KEEP**, 2026-07-31 | Investigated fully — referenced by a real, `disabled: true` block (`header_menu_bottom_hulkapps_backup_kgkQBL`) in the live, active `sections/header-group.json`, the same file that defines the currently-live header. Not orphaned (Theme Check confirms — only a minor `HardcodedRoutes` warning, no unused-code flag). Not removed: doing so safely would require also editing the block/order entries out of the active `header-group.json`, a materially bigger and riskier change than a plain file deletion, for a block that's already fully inert and causes no live harm. No functional file changed this pass — documentation only. See `CHANGELOG.md`. |
| R3 (exhaustive product-template census) | Phase 5 — Liquid Architecture Refactor | **Done (audit only)**, 2026-07-31 | Paginated all 1,235 products for `templateSuffix` (no sampling) — default `product.json` 1,228, `product.premium.json` 3, `product.hampers-template.json` 4, `product.tbk.json` 0, `product.only_config.json` 0. `only_config`'s zero count is by design (it's an alternate quick-view/quick-add template reached via `view=` query string, not `templateSuffix`) — not a cleanup candidate. `product.tbk.json`/`tbk-product.liquid` has zero usage and no alternate-view wiring — marked **SAFE TO REMOVE** pending a manual app-reference check, but **not removed this phase**. Full matrix and evidence: `docs/TEMPLATE_CENSUS.md`. |
| R3.5 (remove `templates/product.tbk.json`) | Phase 5 — Liquid Architecture Refactor | **Done**, 2026-07-31 | Re-verified R3's finding from scratch (fresh full 1,235-product re-pagination, zero `tbk` assignments, no alternate-view wiring, no section/render dependencies) before deleting. Removed only `templates/product.tbk.json`, deployed via a scoped `--only` push (pull → diff-confirm zero drift → delete → push → re-pull → diff-confirm live). `sections/tbk-product.liquid` deliberately left in place, out of scope. Theme Check: 354 files (was 355), same 1,362 offenses/87 files/1,162 errors/200 warnings — no regression. See `CHANGELOG.md`. |
| R4 (orphan snippet verification & risk classification) | Phase 5 — Liquid Architecture Refactor | **Done (audit only)**, 2026-07-31 | Re-verified all 17 in-scope files via direct grep, not Theme Check's label alone — found Theme Check's `OrphanedSnippet` detector unreliable in both directions: 4 files falsely flagged dead (`product-form-bundle.liquid`, `product-form-bundle2.liquid`, `product_tabs.liquid`, `cake-addons.liquid` — all genuinely live on the product templates, including the default protected one) reclassified **ACTIVE**; `shine-trust.liquid` falsely counted as referenced but its include is broken (`{% include 'shine-trust.liquid' %}` with the extension included, resolves to a non-existent path) — corroborates pre-existing `SEO_AUDIT_LEDGER.md` P2-26. Zero fabrication risk found across all reviews/ratings/testimonial-related files checked. Result: 4 ACTIVE, 2 MANUAL REVIEW (`bk-datetime.liquid`, `shine-trust.liquid`), 11 SAFE TO REMOVE — none removed this phase. Full matrix: `docs/ORPHAN_SNIPPET_AUDIT.md`. |
| R5 (remove 11 verified-safe orphan snippets) | Phase 5 — Liquid Architecture Refactor | **Done**, 2026-07-31 | Independently re-verified all 11 R4 safe-to-remove files (fresh grep, zero references confirmed a second time) before deleting. Removed 8 snippets + 3 sections via a scoped `--only` push (pull → diff-confirm zero drift → delete → push → re-pull → diff-confirm gone). `bk-datetime.liquid` and `shine-trust.liquid` confirmed untouched, byte-for-byte. Theme Check: 343 files (was 354, −11), 1,351 offenses/80 files, 1,162 errors (unchanged), 189 warnings (was 200, −11, exactly matching the removed files' own `OrphanedSnippet` flags) — no regression. See `CHANGELOG.md`. |
| R6 (missing asset & broken reference repair) | Phase 5 — Liquid Architecture Refactor | **Done**, 2026-07-31 | Full Theme Check JSON scan, triaged programmatically: 8 `MissingAsset`, 1 `MissingTemplate`, 3 `UnknownFilter`, 3 `DuplicateRenderSnippetArguments`, 1 `ValidJSON`. Only 1 qualified as a deterministic, low-risk, in-scope asset repair — `assets/no-image.svg` (Finding 6), added and deployed via scoped push. 6 `MissingAsset` findings under `design_handoff_shopify_product/` are non-live (Finding 5); `shine-trust.liquid`'s broken include is a pre-existing unresolved business decision (P2-26); the `UnknownFilter` bug lives in now-fully-unreachable `tbk-product.liquid` (its only assigning template was removed in R3.5); `DuplicateRenderSnippetArguments` and `ValidJSON` are code-quality/copy issues, not reference repairs — all correctly left untouched. Theme Check: 1,350 offenses (−1), 1,161 errors (−1, exactly the resolved finding), 189 warnings (unchanged). See `CHANGELOG.md`. |
| R7 (final repository certification) | Phase 5 — Liquid Architecture Refactor | **CERTIFIED**, 2026-07-31 | Verification-only phase, no files changed. Confirmed all 9 R0–R6 commits present, tree clean. Theme Check re-run: 343/1,350/80/1,161/189, byte-identical to R6 — zero drift. Re-verified R1/R3.5/R5 removals still have zero functional references. Cross-referenced remaining `LiquidHTMLSyntaxError`/`UnclosedHTMLElement`/`ValidJSON`/`ValidSchemaName` findings against files this series touched — zero overlap, zero regressions. Documentation cross-checked consistent across all 5 audit docs. Full pre-R0→final Theme Check trajectory, risk register, and production-readiness scoring (Overall 4.3/5) in `docs/FINAL_REPORT.md`. |
| P6.0 (Enterprise Performance Audit) | Phase 6 — Performance Engineering | **Done (audit only)**, 2026-07-31 | 17 findings (F-1–F-17) across render tree, assets, loading strategy, Shopify-specifics, JS/CSS/images/fonts, and performance-linked accessibility — every finding evidence-cited, no fabricated lab metrics. No Core Web Vitals measured (storefront password-gated, blocks all lab/field tools — see `docs/CORE_WEB_VITALS.md`). Only 2 findings meet the "safe, deterministic, no behavior change" bar (missing `fonts.gstatic.com` preconnect; duplicate `uploadcare.full.min.js` script tag) — recommended for P6.1, **not implemented this phase**. Overall Performance Readiness scored 3.1/5 (`docs/PERFORMANCE_SCORECARD.md`), deliberately conservative pending real measurement. 6 new docs: `PERFORMANCE_BASELINE.md`, `PERFORMANCE_AUDIT.md`, `PERFORMANCE_RECOMMENDATIONS.md`, `CORE_WEB_VITALS.md`, `PERFORMANCE_SCORECARD.md`, `PERFORMANCE_ROADMAP.md`. |
| P6.1 (Image Optimization) | Phase 6 — Performance Engineering | **Audited, no action required**, 2026-07-31 | Confirmed the theme's existing image strategy is already correct (responsive `srcset`/`sizes`, correct `eager`+`fetchpriority`/`lazy` split, zero unoptimized local images, all product imagery on Shopify's CDN). No safe optimization found to implement — a confirmed strength, not a gap. |
| P6.2 + P6.3 (CSS + JS Optimization) | Phase 6 — Performance Engineering | **Done**, 2026-07-31 | Removed 3 verified-orphaned assets (`hdt-section-password.css`, `video_with_text2.css`, `day.js`) — zero references confirmed twice independently (quoted-filename grep + broad unrestricted grep). Deployed via scoped `--only` push, re-pulled to confirm gone live. Theme Check unchanged (343/1,350/80/1,161/189) — expected, since Theme Check has no CSS/JS-asset orphan check; grep evidence is authoritative here. See `CHANGELOG.md`. |
| P6.5 investigation (Uploadcare correction; shine-trust-v4 JS traced) | Phase 6 — Performance Engineering | **Corrected finding, no removal**, 2026-07-31 | Deeper read of `layout/theme.liquid`'s two Uploadcare script loads found the second is **not** a redundant duplicate — it sets 4 additional config globals (multi-file, camera/URL tabs, images-only, 1600×1600 shrink) absent from the first, indicating a distinct real feature (very likely personalized-cake photo upload). **P6.0's F-8/R-2 finding is retracted** — not implemented, to avoid breaking real functionality. Separately, traced all 7 `shine-trust-v4-*.js` files (~136 KB): each is referenced only inside the already-confirmed-dead `snippets/shine-trust.liquid` (broken include, P2-26) — transitively dead, but tied to the same unresolved business decision (turn the widget on vs. delete) as the CSS. Not removed, consistent with project precedent of never unilaterally resolving a flagged business decision. |
| P6.4 (Liquid Rendering Optimization) | Phase 6 — Performance Engineering | **Audited, no deterministic action found**, 2026-07-31 | Render-tree complexity (F-1 protected module, F-2 17 near-duplicate card snippets) confirmed real but neither has a same-session fix that's simultaneously deterministic/low-risk/behavior-preserving. Pagination/collection/search rendering re-confirmed already correct. |
| P6.6 (Font Optimization) | Phase 6 — Performance Engineering | **Done**, 2026-07-31 | Added missing `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` to `layout/theme.liquid` (1 line, purely additive). Deployed via scoped push, re-pulled byte-identical. Theme Check: 1,351 offenses (+1), 190 warnings (+1) — the +1 is a `RemoteAsset` false positive on the new preconnect line itself (confirmed via before/after JSON diff; the two pre-existing font lines already carry this identical warning) — not a real regression. See `CHANGELOG.md`. |

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
