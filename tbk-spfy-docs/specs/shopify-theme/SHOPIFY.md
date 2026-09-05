# Shopify

Store- and theme-specific reference. The canonical, detailed audit is the root `SHOPIFY_ARCHITECTURE.md`; this file is the working summary.

## Store

| | |
|---|---|
| Storefront | https://thebakingkaur.com |
| Admin | `ae86ba-2a.myshopify.com` |
| Live theme | `Baking Kaur — Draft` · `#151307485353` |
| Base theme | Ecomus v1.6.1 (Halo/The4 "hdt-" family); `theme_author` is mislabelled "Shopify" |
| Platform | Online Store 2.0 — JSON templates + section groups |
| Fonts | Cormorant Garamond (display) + Manrope (UI), via Google Fonts in `layout/theme.liquid` (render-blocking — perf debt) |

## Folder inventory

| Dir | Count | Notes |
|---|---|---|
| `layout` | 2 | `theme.liquid` (entry), `password.liquid` |
| `templates` | 40 | 5 product templates; `product.json` → `main-product-premium-v2` (**protected**) |
| `sections` | ~134 | base Ecomus + `tbk-*` custom + `site-footer` |
| `snippets` | ~146 | base + `bk-*`/`tbk-*` (schema, buy-box, datetime, tokens, trust) |
| `assets` | ~77 | heavy base CSS/JS + 20+ `shine-trust-v4-*.js` |
| `config` | 2 | `settings_schema.json` (Ecomus), `settings_data.json` |
| `locales` | 4 | en only (en.default + AU/CA); RTL scaffolding unused |

## Product templates

`product.json` → `main-product-premium-v2` (default, **protected**) · `product.premium` (same section) · `product.tbk` · `product.hampers-template` · `product.only_config`.

## Structured data (snippets)

`bk-local-business` (Bakery/LocalBusiness — full NAP, geo, hours, sameAs, areaServed) · `structured-data` (Product/Article) · `tbk-schema-website` · `tbk-schema-breadcrumb` · global FAQPage in `theme.liquid` head. Verified live: LocalBusiness, Organization, WebSite, BreadcrumbList, FAQPage sitewide; Product + ProductGroup on PDPs. See `SCHEMA_MASTER.md`.

## Third-party apps / integrations

HulkApps (product options `hulk_po_vd` + cart) · ShineTrust v4 (20+ JS: sticky cart, countdown, BOGO, quantity discount, email popup, cookie banner, free-shipping bar, feature icons, bought-together) · BSS (options/search) · **Uploadcare** (PDP reference-image upload — **protected dependency**) · Rewind (legacy `rewind_*`, unused) · Facebook domain verification.

## Deploying

Live theme `#151307485353`. Deploy single files with `shopify theme push --only … --allow-live`; **pull + diff the live copy first** to avoid clobbering divergence, and verify with `?preview_theme_id=151307485353` to bypass the page cache. Full recipe in [CLAUDE.md](../CLAUDE.md).

## Known debt (tracked, phased)

`theme.liquid` whole-document MutationObservers + duplicate Uploadcare load · render-blocking fonts + heavy CSS/JS · duplicate section families (product ×3, slideshow ×4, testimonials ×5, header ×2) · homepage `custom-liquid` blocks · empty theme/character collections · theme-check baseline ~1,365 offences (mostly base/app). Detail and phase mapping in `SHOPIFY_ARCHITECTURE.md` and `PERFORMANCE_BASELINE.md`.

## Protected modules

Product page (design/UX/flow/CSS/JS), logo, brand colors. Only schema/analytics/perf/a11y-invisible changes are allowed around the PDP.
