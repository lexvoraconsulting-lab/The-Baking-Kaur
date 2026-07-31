# Core Web Vitals — Status & Constraints (Phase 6, P6.0)

## Why there are no measured numbers in this document

Real Core Web Vitals (LCP, CLS, INP, TTFB, FCP, TBT, Speed Index) require either a lab tool
(Lighthouse, PageSpeed Insights, WebPageTest) rendering the live page in a real browser, or
real-user field data (Chrome UX Report / Search Console). Neither is obtainable from this
environment right now:

- **The storefront is intentionally password-gated** (`business/BUSINESS_MASTER.md` §16,
  `docs/LIQUID_ARCHITECTURE_AUDIT.md` Finding 0's own note on this same constraint). This blocks
  both this session's `WebFetch` tool and any external crawler — Google's PageSpeed Insights bot
  cannot authenticate through a Shopify storefront password page, so a PSI/Lighthouse run against
  the live URL would return the password page's metrics, not the real storefront's.
- **No field data exists yet** — the site isn't publicly indexed/crawled while gated, so Chrome UX
  Report has no real-user samples to report.
- **No local browser automation** is available in this environment to run Lighthouse against a
  password-bypassed preview URL (`?preview_theme_id=...`) either.

**Fabricating specific millisecond/score numbers here would violate this project's own standing
rule** ("verifiability beats persuasion... no rating, count, certification, or delivery promise
ships without a source" — `CLAUDE.md`). Instead, this document explains each metric, gives a
**code-evidence-based risk assessment** (proxy signals only, clearly labeled as such), and
specifies exactly how to get real numbers once the site is unlocked or a preview-bypass workflow
exists.

## How to get real numbers (recommended, not performed here)

1. Once the password gate is lifted (or via a manual authenticated session), run:
   `https://pagespeed.web.dev/report?url=https://thebakingkaur.com/`
   for both mobile and desktop, on the homepage, a representative product page, and a collection
   page.
2. Alternatively, an authenticated human tester can open Chrome DevTools → Lighthouke tab on the
   live (password-entered) session and run it locally.
3. Repeat after each P6.x optimization sprint to measure real before/after deltas — this is the
   only way to validate the estimated gains in `docs/PERFORMANCE_RECOMMENDATIONS.md`.

## Metric-by-metric: what it means and code-evidence risk signals (not measured values)

### LCP (Largest Contentful Paint)

Time to render the largest visible element (usually the hero image or a large heading).

**Risk signals found in code**:
- Homepage (`templates/index.json`) has 13 `image` blocks and a `slideshow` — if the hero/first
  slideshow image isn't marked `fetchpriority="high"` and preloaded, it competes with everything
  else for bandwidth. Not yet verified whether the homepage hero does this (needs a follow-up
  read in P6.1 scope, not done in this document).
- Product page (`main-product-premium-v2.liquid`) gallery images are Shopify-CDN-served
  (responsive `srcset` likely present, per theme convention seen in `snippets/tbk-gallery.liquid`
  using `image_url`/`image_tag`) — a positive signal, not a risk.
- Render-blocking CSS (`theme.css` 264 KB + `base.css` 129 KB, unconditionally loaded, no
  preload/critical-CSS split) delays the browser's ability to paint anything, including the LCP
  element — a real risk signal, detailed in `docs/PERFORMANCE_AUDIT.md`.
- Render-blocking Google Fonts CSS (synchronous `<link rel="stylesheet">`, no preconnect to
  `fonts.gstatic.com`) delays text rendering, which can affect LCP when the LCP element is
  heading text rather than an image.

### CLS (Cumulative Layout Shift)

Visual stability — how much visible content shifts unexpectedly after initial render.

**Risk signals found in code**:
- Theme Check's own `ImgWidthAndHeight` check found **4 confirmed instances** of `<img>` tags
  missing explicit `width`/`height` attributes (`snippets/tbk-gallery.liquid` ×3,
  `sections/tbk-product.liquid` ×1) — missing dimensions is a textbook CLS cause, since the
  browser can't reserve layout space before the image loads. Note: `tbk-gallery.liquid` is only
  reachable via `tbk-product.liquid`, which has had zero live rendering path since R3.5
  (`docs/TEMPLATE_CENSUS.md`) — so this specific instance carries no live CLS risk today, but
  would if that section were ever reactivated.
- Google Fonts with `&display=swap` mitigates invisible-text CLS from font-swap (a positive) but
  can still cause a *visible* text-reflow shift when the web font's metrics differ from the
  fallback — not measurable without a real render.

### INP (Interaction to Next Paint)

Responsiveness to user input (replaces FID as of March 2024).

**Risk signals found in code**:
- 6 `shine-trust-v4-*.js` files (~124 KB combined) plus `vendor.min.js` (125 KB) and
  `global.min.js` (155 KB) all execute on the main thread; without confirmed `defer`/module-async
  loading for all of them, heavy synchronous JS parsing/execution can block the main thread and
  delay input responsiveness. Loading attributes for these specific files were not individually
  audited in this pass (flagged for P6.1).
- The duplicate, non-deferred `uploadcare.full.min.js` load (`layout/theme.liquid:164,292`) is a
  concrete, confirmed main-thread-blocking third-party script, loaded twice.

### TTFB (Time to First Byte)

Server response time — determined by Shopify's platform infrastructure and app/proxy overhead,
not the theme's Liquid code in most cases. Out of this audit's control surface (Shopify manages
the CDN/edge layer); no code-level finding applies here.

### FCP (First Contentful Paint)

Time to first visible render of anything. Same render-blocking-CSS and render-blocking-fonts risk
signals as LCP above apply directly to FCP as well.

### TBT (Total Blocking Time)

Sum of main-thread blocking time between FCP and TTI. Same JS-weight risk signals as INP above.

### Speed Index

How quickly page content is visually populated. A composite proxy for the above — the same
render-blocking CSS/font/JS risk signals apply.

## Certification

**This document does not certify any Core Web Vitals pass/fail status** — that requires real
measurement, which is not available. It certifies only that the code-evidence risk signals above
are accurately drawn from the repository as of commit `0ea4916`, and that no number in this
document was fabricated or estimated as if it were measured.

## Related

[PERFORMANCE_BASELINE.md](PERFORMANCE_BASELINE.md), [PERFORMANCE_AUDIT.md](PERFORMANCE_AUDIT.md),
[PERFORMANCE_RECOMMENDATIONS.md](PERFORMANCE_RECOMMENDATIONS.md).
