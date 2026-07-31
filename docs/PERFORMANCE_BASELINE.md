# Performance Baseline (Phase 6, P6.0)

Generated 2026-07-31. This is a **static, code-level baseline** — objective, measurable facts
about the repository as it stands after R0–R7 certification (`docs/FINAL_REPORT.md`, commit
`0ea4916`). It is not a Lighthouse/PSI lab report; see `docs/CORE_WEB_VITALS.md` for why that
specific measurement isn't obtainable in this environment and what to run once it is.

`docs/ENGINEERING_BASELINE.md` does not exist in this repository — checked, confirmed absent, not
assumed.

**Correction (added 2026-07-31, Phase 7.0 reconciliation)**: this document originally implied no
live/runtime measurement had ever been attempted anywhere in this project. That was incomplete —
the root-level `PERFORMANCE_BASELINE.md` (an earlier, "Phase A"-era document, not written by this
Phase 6 pass) contains real preview-theme runtime data captured via the browser Performance API
(DOMContentLoaded ~4.9s, Load ~9.2s, ~139 resources) — directional, not certified, but genuine
measured data, not a fabrication. That document is preserved as the historical baseline; this
document remains the current static/code-level reference. Neither Lighthouse/PSI nor CrUX field
data exists for either document — that gap, described below, stands.

## Asset inventory

| Category | Count | Total size |
|---|---|---|
| JavaScript (`assets/*.js`) | 24 | 689,419 bytes (~673 KB) |
| CSS (`assets/*.css`) | 48 | 699,783 bytes (~683 KB) |
| SVG | 3 | 1,505 bytes |
| PNG | 1 | 122,172 bytes |
| **Total `assets/`** | — | **~1.7 MB** |

No product/marketing images live in `assets/` — confirmed normal, since real product imagery is
served from Shopify's CDN (`cdn.shopify.com`), not bundled in the theme. No local font files
(`.woff`/`.woff2`/`.ttf`) — fonts are loaded via Google Fonts and `fonts.shopifycdn.com` (see
Font Loading below), not self-hosted.

### 10 largest JS files

| File | Size |
|---|---|
| `global.min.js` | 155,603 B |
| `vendor.min.js` | 125,829 B |
| `custom.js` | 80,306 B |
| `es-photoswipe.min.js` | 60,033 B |
| `importmap.min.js` | 33,126 B |
| `shine-trust-v4-bought-together.js` | 31,382 B |
| `hdt-currencies.js` | 25,379 B |
| `shine-trust-v4-buyx-gety.js` | 22,396 B |
| `shine-trust-v4-product-badge.js` | 21,701 B |
| `shine-trust-v4-countdown-timer.js` | 17,779 B |

Six separate `shine-trust-v4-*.js` files total ~124 KB — a third-party app's JS footprint, loaded
independently of the broken `shine-trust.liquid` CSS include (`docs/ORPHAN_SNIPPET_AUDIT.md`,
`SEO_AUDIT_LEDGER.md` P2-26) — the JS and CSS are two separate delivery paths for the same app; the
CSS is confirmed dead, the JS's live/dead status is a separate question not yet audited here (see
`docs/PERFORMANCE_AUDIT.md`, JavaScript section).

### 10 largest CSS files

| File | Size |
|---|---|
| `theme.css` | 264,048 B |
| `base.css` | 129,167 B |
| `testimonials.css` | 29,793 B |
| `hdt-collections-list.css` | 19,441 B |
| `hdt-search-form.css` | 17,706 B |
| `hdt-cart-drawer.css` | 17,392 B |
| `facets.css` | 15,780 B |
| `hdt-main-collection.css` | 14,942 B |
| `hdt-main-cart.css` | 13,735 B |
| `hdt-widget.css` | 10,202 B |

`theme.css` + `base.css` alone = ~393 KB (56% of all CSS weight), both loaded on every page via
`layout/theme.liquid`'s unconditional `stylesheet_tag` calls — see Loading Strategy below.

## Render-tree complexity

| File | Metric |
|---|---|
| `sections/main-product-premium-v2.liquid` (default product template, 1,228/1,235 products) | 4,642 lines; 31 `render`/`section` calls |
| `sections/tbk-header.liquid` (renders on every page) | 1,246 lines |
| `layout/theme.liquid` (renders on every page) | 368 lines |
| `templates/index.json` (homepage) | 17 distinct block/section types across the page (13× `image`, 13× `collection_item`, 7× `custom-liquid`, 6× `slide_base`, plus 10 more single-instance types) |
| `snippets/card-product*.liquid` family | 17 near-duplicate files (`card-product1`–`card-product11`, `-discount2`, `-discount3`, `-wishlist`, `-price-tables`, `-list`) |

## Loading strategy — current state

- **Font loading**: Google Fonts (`Cormorant Garamond`, `Manrope`) loaded via a synchronous
  `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?...&display=swap">`
  (`layout/theme.liquid:41`) — render-blocking. `font-display: swap` is present (good — avoids
  invisible text), but the CSS fetch itself still blocks.
- **Preconnect**: present for `fonts.shopifycdn.com` (line 36) and `fonts.googleapis.com` (line 40).
  **Missing**: `fonts.gstatic.com` — the actual font-file host Google's CSS response points to.
  Confirmed via grep: 0 occurrences anywhere in `layout/theme.liquid`.
- **Third-party script duplication**: `https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js`
  is loaded **twice** in `layout/theme.liquid` (lines 164 and 292), neither with `defer`/`async`.
- **`assets/hamper-addons.js`** is the only script tag in `layout/theme.liquid` using `defer`
  (line 283) — the rest of the inline `<script>` blocks (lines 161, 219, 230, 265, 284, 294) render
  in document order, unminified inline logic.
- **CSS delivery**: `theme.css` and `hdt-policy.css` (conditional) loaded via plain `stylesheet_tag`
  (lines 59, 61) — no `preload`, no critical-CSS split, no media-query gating.

## Theme Check baseline carried over from R0–R7 (unchanged, for reference)

343 files inspected, 1,350 offenses, 80 files flagged, 1,161 errors, 189 warnings
(`docs/FINAL_REPORT.md`). Of direct performance relevance: `ImgWidthAndHeight` (4 findings — CLS
risk), `ParserBlockingScript` (3 findings), `RemoteAsset` (7 findings — third-party CDN
dependencies).

## What this baseline does NOT include

- No Lighthouse/PageSpeed Insights run — the storefront is intentionally password-gated
  (`business/BUSINESS_MASTER.md` §16), which blocks both this environment's `WebFetch` and any
  external lab tool (Google's PSI crawler cannot pass the password gate). See
  `docs/CORE_WEB_VITALS.md`.
- No real-user (CrUX/field) data — would require Search Console access, not available here.
- No JS/CSS coverage analysis (actual unused-byte percentage) — would require a live browser
  DevTools Coverage run against an unlocked preview; not performed here. Static duplication/size
  evidence is used as a proxy instead (see `docs/PERFORMANCE_AUDIT.md`).

## Related

[PERFORMANCE_AUDIT.md](PERFORMANCE_AUDIT.md), [CORE_WEB_VITALS.md](CORE_WEB_VITALS.md),
[PERFORMANCE_RECOMMENDATIONS.md](PERFORMANCE_RECOMMENDATIONS.md),
[PERFORMANCE_SCORECARD.md](PERFORMANCE_SCORECARD.md), [PERFORMANCE_ROADMAP.md](PERFORMANCE_ROADMAP.md),
[FINAL_REPORT.md](FINAL_REPORT.md).
