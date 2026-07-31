# Performance Audit (Phase 6, P6.0)

Full audit across every requested performance area. Every finding is backed by a repo-verifiable
citation (file, line, size, or count) — no estimated/lab metric is presented as measured (see
`docs/CORE_WEB_VITALS.md` for why). **Audit only — nothing in this document has been implemented.**

Format per finding: Evidence · Reason · Impact · Risk · Recommended fix · Expected gain ·
Implementation complexity.

---

## 1. Liquid render tree & rendering performance

### F-1: `main-product-premium-v2.liquid` is a 4,642-line, 31-render-call monolith
- **Evidence**: `wc -l` = 4,642; `grep -c "render\|section"` = 31, on the default product template
  rendering for 1,228 of 1,235 products.
- **Reason**: a single section file carries gallery, variant picker, delivery-date logic, bundle
  upsell, tabs, trust pills, and inline `<style>`/`<script>` blocks all in one file.
- **Impact**: large server-side Liquid compile/render cost per request; large HTML payload; harder
  to isolate what's render-blocking within it.
- **Risk**: Medium — this is the **protected product-page module** (`CLAUDE.md`: "No visual/UX/
  flow/CSS/JS changes... only invisible edits"). Any restructuring here requires extreme caution and
  is likely out of bounds for an "invisible edit."
- **Recommended fix**: not a code change — a measurement task. Profile actual server render time
  once real access exists; do not restructure the protected module speculatively.
- **Expected gain**: Unknown without measurement — flagged for future investigation, not action.
- **Complexity**: N/A (measurement, not implementation).

### F-2: 17 near-duplicate `card-product*.liquid` snippets
- **Evidence**: `ls snippets/ | grep -c "^card-product"` = 17 (`card-product1`–`card-product11`,
  `-discount2`, `-discount3`, `-wishlist`, `-price-tables`, `-list`).
- **Reason**: each variant appears to be a near-duplicate product-card layout (confirmed sharing
  identical class patterns like `hdt-product-btns hdt-pr-btns-group1/2` across all 17, seen during
  R4's grep sweep) — likely one per configurable card "style" the theme's settings expose, rather
  than 17 independently-maintained features.
- **Impact**: maintainability cost (a bug/improvement must be replicated 17×) more than a runtime
  performance cost — only the *one* style a given section actually uses is rendered per page, so
  this isn't extra runtime weight unless multiple styles render simultaneously on one page.
- **Risk**: Low to audit, but consolidating 17 near-duplicate files is a structural change with
  real regression risk (must verify indistinguishable output for each style) — not a "does not
  change storefront behaviour" change, so out of this phase's auto-implement scope.
- **Recommended fix**: a dedicated future consolidation phase (parameterize one snippet by
  `card_style` instead of 17 files), only after a full behavioral diff of all 17.
- **Expected gain**: maintainability, not measurable runtime performance.
- **Complexity**: High (17-way behavioral equivalence required).

### F-3: Collection/search/listing pagination is correctly implemented (positive finding)
- **Evidence**: `{% paginate %}` used in 11 sections (`main-article`, `main-collection`,
  `main-search`, `main-wishlist`, `tabs-collections-grid`, `main-list-collections`,
  `featured-collection-grid`, `main-account`, `main-addresses`, `main-blog`, `main-brands`).
  `main-collection.liquid`'s `products_count` setting: `min: 1, max: 50, default: 8`.
- **Reason/Impact**: pages don't load unbounded product lists; default page size (8) is
  conservative and merchant-configurable up to a reasonable cap (50).
- **Risk**: None — no action needed. Documented as a baseline strength, not a finding to fix.

### F-4: Homepage composition is moderately heavy but bounded
- **Evidence**: `templates/index.json` — 17 distinct block/section types, largest counts being
  13× `image` and 13× `collection_item`.
- **Reason**: a content-rich homepage (image blocks, carousels, collection highlights) is a
  deliberate merchandising choice, not a defect.
- **Impact**: more DOM nodes and image requests than a minimal homepage, but within normal range for
  an e-commerce homepage of this kind.
- **Risk**: Low. Not flagged as an issue — noted for completeness.

---

## 2. Asset audit (images, CSS, JS, fonts, SVG, video)

### F-5: `theme.css` (264 KB) + `base.css` (129 KB) = ~393 KB, unconditionally render-blocking
- **Evidence**: `layout/theme.liquid:59` — `echo 'theme.css' | asset_url | stylesheet_tag`, no
  `preload`/media split. File sizes confirmed via `ls -la`.
- **Reason**: both files load as plain `<link rel="stylesheet">` on every single page regardless of
  page type, with no critical-CSS extraction.
- **Impact**: render-blocking CSS delays First Contentful Paint and Largest Contentful Paint on
  every page (see `docs/CORE_WEB_VITALS.md`).
- **Risk**: Low to audit further, Medium to fix — splitting critical CSS risks visual regressions
  if done incorrectly; the product page in particular is protected (`CLAUDE.md`).
- **Recommended fix**: a dedicated critical-CSS extraction pass (above-the-fold styles inlined,
  rest deferred via `media="print" onload="this.media='all'"` or `rel="preload"` + swap) — requires
  visual regression testing before/after, not a blind automated change.
- **Expected gain**: Meaningful FCP/LCP improvement (unquantified without lab measurement).
- **Complexity**: Medium-High (visual regression risk on the protected product page).

### F-6: No local font files; Google Fonts + Shopify CDN fonts, correctly `display: swap`
- **Evidence**: `layout/theme.liquid:41` —
  `Cormorant+Garamond:ital,wght@0,600;0,700;1,500&family=Manrope:wght@400;600;700&display=swap`.
- **Reason/Impact**: `font-display: swap` is a real, already-present best practice (avoids
  invisible-text flash) — a positive finding, not an issue by itself. The *delivery* of this CSS
  (synchronous stylesheet link) is the actual finding — see F-7.
- **Risk**: None on its own.

### F-7: Missing `preconnect` to `fonts.gstatic.com`
- **Evidence**: `grep -c "fonts.gstatic.com" layout/theme.liquid` = 0. Existing preconnects:
  `fonts.shopifycdn.com` (line 36), `fonts.googleapis.com` (line 40) only.
- **Reason**: Google Fonts' CSS response (from `fonts.googleapis.com`) references actual font
  binaries hosted on `fonts.gstatic.com` — a *different* origin, discovered only after the CSS
  itself downloads. Preconnecting only to the CSS host doesn't save connection-setup time for the
  font-file fetch that follows.
- **Impact**: an extra full DNS+TCP+TLS round-trip before each font file starts downloading —
  directly delays text rendering (FCP/LCP when text is the LCP element).
- **Risk**: **None** — adding a `preconnect` link is purely additive, cannot change rendered output
  or behavior. This is a textbook safe, deterministic, evidence-based fix.
- **Recommended fix**: add `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`
  next to the existing font preconnects.
- **Expected gain**: removes one round-trip (typically 50–200ms depending on network) from the
  critical font-loading path.
- **Complexity**: Trivial (one line, zero behavior change) — **candidate for auto-implementation
  in P6.1**, since it meets this phase's "safe, deterministic, no behavior change" bar. Not applied
  in this phase per the explicit stop instruction ("do not begin optimization yet").

### F-8: Third-party script `uploadcare.full.min.js` loaded twice, neither deferred
- **Evidence**: `layout/theme.liquid:164` and `:292` — identical
  `<script src="https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js">` tags, no `defer`/
  `async` on either.
- **Reason**: appears to be an accidental duplicate script include (same exact URL, same file),
  likely from two separate integration steps that were never deduplicated.
- **Impact**: downloads and parses the same ~unknown-size remote script twice; blocks the main
  thread and delays parsing of everything after each occurrence, twice over.
- **Risk**: **Low to remove the duplicate** (the second identical tag is provably redundant —
  removing it cannot change behavior, since the first tag already loads and initializes the exact
  same widget). Adding `defer` to the remaining tag carries a small risk if any inline script
  immediately after depends on Uploadcare's global being synchronously available — needs a quick
  check before doing so.
- **Recommended fix**: remove the duplicate tag (line 292) outright — deterministic, zero risk.
  Separately evaluate adding `defer` to the remaining tag (needs the dependency check above).
- **Expected gain**: one fewer full script download+parse+execute cycle on every single page.
- **Complexity**: Trivial for the duplicate removal — **candidate for auto-implementation in
  P6.1**. The `defer` addition is a separate, slightly higher-complexity follow-up.

### F-9: Six `shine-trust-v4-*.js` files (~124 KB combined) — live/dead status not yet determined
- **Evidence**: `assets/shine-trust-v4-{bought-together,buyx-gety,product-badge,countdown-timer,
  quantity-discount,sticky-cart,email-popup}.js` — 7 files, ~139 KB combined actually (corrected:
  bought-together 31KB + buyx-gety 22KB + product-badge 21KB + countdown-timer 18KB +
  quantity-discount 17KB + sticky-cart 17KB + email-popup 10KB ≈ 136 KB).
- **Reason**: this project already confirmed the *CSS* half of this same app
  (`snippets/shine-trust.liquid`) never renders due to a broken `{% include %}`
  (`docs/ORPHAN_SNIPPET_AUDIT.md`, `SEO_AUDIT_LEDGER.md` P2-26) — a pending, unresolved business
  decision (turn the whole widget on vs. remove it entirely). The **JS files' own loading
  mechanism was not traced in this pass** — they may be loaded via a different, separate
  `<script>` tag not yet located, or an app-embed block via `content_for_header` (see F-11), or may
  be entirely dead alongside the CSS.
- **Impact**: if unreferenced, ~136 KB of pure dead weight; if referenced independently of the
  broken CSS, an active but unaudited script bundle.
- **Risk**: Cannot assess without first tracing every JS file's actual `<script src>` reference —
  not completed in this pass.
- **Recommended fix**: trace `shine-trust-v4-*.js` reference paths in a follow-up (P6.1 scope);
  resolve alongside the pending `shine-trust.liquid` business decision, not separately.
- **Expected gain**: up to ~136 KB if confirmed fully dead.
- **Complexity**: Low to trace, but the removal decision itself depends on the same pending
  business call as `shine-trust.liquid`.

### F-10: No video assets in the theme
- **Evidence**: asset-type scan found 0 `.mp4`/`.webm` files in `assets/`.
- **Reason/Impact**: any video content (e.g., `sections/video-2.liquid`'s pattern, though that
  specific section was removed in R5) uses Shopify's native `video_tag`/external embeds, not
  theme-bundled video files — no local video weight to audit.
- **Risk**: None. Positive baseline fact, no action.

---

## 3. Loading strategy

### F-11: `content_for_header` present — installed-app scripts are outside this audit's visibility
- **Evidence**: `layout/theme.liquid:65` — `{{ content_for_header }}`.
- **Reason**: this is Shopify's required hook where every installed app's embed blocks and
  tracking scripts inject their own `<script>`/`<link>` tags automatically, at render time — their
  actual content isn't present anywhere in this repository and can't be statically audited.
- **Impact**: unknown — could include additional render-blocking or heavy scripts invisible to a
  code-only audit.
- **Risk**: Real, but **out of this audit's control surface**. A live-page view-source (once
  unlocked) is the only way to inventory what apps actually inject here.
- **Recommended fix**: none from this repository; flag for the same manual live-page check already
  recommended for Core Web Vitals measurement.
- **Complexity**: N/A (external dependency).

### F-12: `loading="lazy"` used pervasively; `fetchpriority="high"` used for the main product image
- **Evidence**: `snippets/tbk-gallery.liquid:4` — main product image uses
  `loading="eager" fetchpriority="high"` (correct — above-the-fold LCP candidate should not lazy-load);
  thumbnails at line 15 use `loading="lazy"` (correct — below-the-fold, should lazy-load). This
  pattern (eager+fetchpriority for the primary image, lazy for the rest) is the textbook-correct
  approach.
- **Risk**: None — positive finding, no action.

### F-13: No critical-CSS split, no `preload` for the two largest CSS files
- Same finding as F-5 — cross-referenced here under "loading strategy" per the requested audit
  structure.

---

## 4. Shopify-specific issues

### F-14: Responsive images (`srcset`/`sizes`) are used correctly and extensively
- **Evidence**: seen repeatedly across snippet reads this project has done (e.g.
  `lookbook-card-product.liquid`'s `widths: '165, 340, 500, 600, 680'`,
  `product-form-bundle2.liquid`'s responsive `image_url` calls) — a consistent, theme-wide pattern
  of real responsive image delivery via Shopify's native `image_url`/`image_tag` filters, not
  fixed-size images.
- **Risk**: None. Positive finding.

### F-15: No Theme App Extension blocks found in the audited templates
- **Evidence**: no `{% content_for 'block' %}`/app-block schema entries encountered during this
  project's extensive prior section/template reading (R0–R7). The only identified third-party
  integrations are the Uploadcare widget (F-8) and the Shine Trust bundle (F-9), both delivered as
  static theme assets, not live Theme App Extension blocks.
- **Risk**: Low confidence this is exhaustive — a full `templates/*.json` block-type sweep for
  `"type"` values matching an app's UUID-style block ID was not performed in this pass. Flagged as
  an open item, not a confirmed absence.

### F-16: Shopify CDN usage for product imagery is correct
- **Evidence**: no product images bundled in `assets/`; all product imagery flows through
  Shopify's `image_url`/`cdn.shopify.com` pipeline (confirmed via the asset-type scan finding 0
  product photos locally, and via every product-image-rendering snippet read this project has
  done using `image_url`/`image_tag` filters).
- **Risk**: None. Positive finding — this is the correct, performant pattern.

---

## 5. JavaScript review

Covered above: F-8 (duplicate Uploadcare script), F-9 (Shine Trust JS bundle, live/dead status
unresolved). **Not performed in this pass** (require a live browser or deeper static analysis
beyond this audit's time budget): unused-JS percentage (needs DevTools Coverage against a real
render), event-listener audit, memory-leak detection. These require either live tooling or a much
deeper line-by-line review of `vendor.min.js`/`global.min.js`/`custom.js` and are flagged as
**future work**, not silently skipped.

## 6. CSS review

Covered above: F-5 (theme.css/base.css size and render-blocking delivery). **Not performed in this
pass**: exact unused-selector percentage (needs live coverage tooling), expensive-selector
profiling, animation-cost profiling — same reasoning as the JS gaps above.

## 7. Images review

Covered above: F-14 (responsive images, positive), Theme Check's own `ImgWidthAndHeight` finding
(4 instances, cross-referenced from `docs/PERFORMANCE_BASELINE.md`/`docs/FINAL_REPORT.md` — the
3 in `tbk-gallery.liquid` are inside the now-unreachable `tbk-product.liquid` per R3.5; the 1 in
`tbk-product.liquid` itself is the same unreachable section). No live-page CLS risk today, but
would apply if that section were ever reactivated.

## 8. Fonts review

Covered above: F-6 (positive: `display: swap` present), F-7 (missing `gstatic.com` preconnect).
No self-hosted or variable fonts in use — Google Fonts + Shopify's own font CDN only.

## 9. Accessibility (performance-related)

### F-17: `prefers-reduced-motion` is respected
- **Evidence**: `grep -l "prefers-reduced-motion"` matches `assets/base.css`, `assets/theme.css`,
  and both `es-photoswipe.min.js` and `global.min.js`.
- **Reason/Impact**: motion-sensitive users get reduced/no animation — both an accessibility and a
  (minor) rendering-cost win, since disabling animation for these users also reduces their
  main-thread work.
- **Risk**: None. Positive finding, no action needed.

Focus-visible and contrast were not audited in this pass — those are primarily accessibility
concerns with only indirect performance relevance (e.g., focus-ring paint cost is negligible) and
fall outside this phase's explicit "performance-related accessibility" scope as narrowly
interpreted here; flagged as a gap, not silently dropped.

---

## Summary of confirmed, actionable findings (safe-to-auto-implement candidates for P6.1)

| Finding | Risk | Complexity | Behavior change? |
|---|---|---|---|
| F-7: add `preconnect` for `fonts.gstatic.com` | None | Trivial | No |
| F-8: remove duplicate `uploadcare.full.min.js` tag | Low | Trivial | No |

Every other finding either requires further investigation (F-9, F-11, F-15, JS/CSS coverage gaps),
carries real behavior-change/regression risk requiring sign-off (F-5, F-2), or is already a
confirmed strength requiring no action (F-3, F-6, F-10, F-12, F-14, F-16, F-17).

## Related

[PERFORMANCE_BASELINE.md](PERFORMANCE_BASELINE.md), [CORE_WEB_VITALS.md](CORE_WEB_VITALS.md),
[PERFORMANCE_RECOMMENDATIONS.md](PERFORMANCE_RECOMMENDATIONS.md),
[PERFORMANCE_SCORECARD.md](PERFORMANCE_SCORECARD.md), [PERFORMANCE_ROADMAP.md](PERFORMANCE_ROADMAP.md).
