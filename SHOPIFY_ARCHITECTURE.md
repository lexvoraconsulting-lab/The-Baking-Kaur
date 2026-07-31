# SHOPIFY_ARCHITECTURE.md — The Baking Kaur

Canonical reference for the theme's technical architecture. Source: Phase-1 audit. Update as structure changes.

## Theme
Ecomus v1.6.1 (Halo/The4 "hdt-" family; `theme_author` mislabeled "Shopify"). Online Store 2.0 — JSON templates + section groups. Fonts: Cormorant Garamond (display) + Manrope (UI), loaded via Google Fonts in `layout/theme.liquid` (render-blocking — Phase I; **partial fix 2026-07-31**: missing `fonts.gstatic.com` preconnect added, `docs/PERFORMANCE_FINAL_REPORT.md` P6.6 — the render-blocking Google Fonts `<link>` itself remains, only the preconnect gap was closed).

## Folder inventory
| Dir | Count | Notes |
|---|---|---|
| layout | 2 | `theme.liquid` (entry), `password.liquid` |
| templates | 40 | 5 product templates; `product.json` → `main-product-premium-v2` (protected) |
| sections | ~123 (post Phase-A cleanup) | base Ecomus + `tbk-*` custom + `site-footer` |
| snippets | ~141 | base + `bk-/tbk-*` (schema, buy-box, datetime, tokens, trust) |
| assets | 77 | `theme.css` 264KB, `base.css` 128KB, `global.min.js` 152KB, `vendor.min.js` 124KB, 20+ `shine-trust-v4-*.js` |
| config | 2 | `settings_schema.json` (Ecomus), `settings_data.json` |
| locales | 4 | en only (en.default + AU/CA); RTL scaffolding unused |

## Render flow (`layout/theme.liquid`)
head: fonts · `bk-local-business` (Bakery) · `theme.css` · `social-meta-tags` · `css-variables` · `js-head` · global FAQPage (⚠ placement, Phase F) · Uploadcare (⚠ loaded twice) → body: `header-group` → `main` (JSON template) → `footer-group` (**restored Phase A** → `site-footer`) → `system-group` → `structured-data` (Product/Article) · `tbk-schema-website` · `tbk-schema-breadcrumb` · sticky WhatsApp · **3 whole-document MutationObservers** (⚠ Phase B/H).

## Section groups
`header-group.json` (active: `tbk-announcement-bar`, `tbk-header`; disabled: `announcement-bar`, `header-e-commerce`, `header-menu-bottom-hulkapps-backup`) · `footer-group.json` (**new, Phase A** → `site-footer`) · `system-group.json` (cart-drawer, popups, cookies, newsletter) · `config-group.json`.

## Product templates
`product.json`→`main-product-premium-v2` (default, **protected**) · `product.premium` (same section) · `product.tbk` · `product.hampers-template` · `product.only_config`.

## Third-party apps / integrations
HulkApps (product options `hulk_po_vd` + cart, backups removed Phase A) · ShineTrust v4 (20+ JS: sticky cart, countdown, BOGO, quantity discount, email popup, announcement, cookie banner, free-shipping, feature icons, bought-together) · BSS (product options / search) · Uploadcare (PDP reference-image upload — **protected dependency**) · Rewind (legacy `rewind_*`, unused) · Facebook domain verification.

## Known debt (tracked, phased)
theme.liquid observers + duplicate Uploadcare (B/H; **independently re-investigated 2026-07-31**, `docs/PERFORMANCE_AUDIT.md`/`PERFORMANCE_FINAL_REPORT.md` P6.5 — confirmed NOT a true duplicate, the second load sets distinct config for what's very likely the protected-PDP photo-upload feature; not removed) · render-blocking fonts + heavy CSS/JS + app-script audit (I) · duplicate section families (product×3, slideshow×4, testimonials×5, header×2) (E/B) · 7 homepage `custom-liquid` blocks (C) · product-title mojibake at data source (B/data) · 8 empty collections (collection audit) · theme-check 1,365 offenses baseline (mostly base/app — `PERFORMANCE_BASELINE.md`).

## Protected modules
Product page (design/UX/flow/CSS/JS), logo, brand colors. See `protected-modules` memory. Only schema/analytics/perf/a11y-invisible changes allowed around PDP.

_v0.1 — from Phase-1 audit + Phase-A changes._
