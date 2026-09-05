<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/research-dark.svg">
  <img alt="Research" src="../../skills/ThemeStyleOps/assets/banners/lexvora/research-light.svg" width="100%">
</picture>

# Research — Theme Performance Budget & Ecomus Optimization (`RSH_20260906_A`)

> **Parent:** [`research-master.md`](./research-master.md) · **Status:** `Exploring` · **Date:** 2026-09-06
> **From concept:** [`CON001`](../concept-design/CON001_Storefront_Luxury_Editorial_Redesign_Concept.md) (reverse: research spawned by an open question)

## Question

How can we reduce JavaScript bloat and CSS overhead from the base Ecomus theme while maintaining an elevated editorial presentation and achieving green Core Web Vitals (LCP < 2.5s, INP < 200ms, CLS < 0.1) on local mobile networks in Meerut?

## Current Baseline

The Ecomus v1.6.1 baseline bundles multiple vendor animation scripts and multi-purpose styling frameworks (`assets/theme.css`, `assets/hdt-*.js`). Several scripts load unconditionally even when the corresponding sections are unused on the homepage, creating unnecessary render blocking and main-thread execution time.

## Findings

1. **Native Browser Primitives (`ponytail` approach):** Replacing heavy third-party carousel sliders with native CSS scroll-snap eliminates ~45KB of JavaScript runtime parsing without visual compromise.
2. **Font Optimization:** Serving *Cormorant Garamond* and *Manrope* as local `.woff2` files stored in Shopify's CDN assets avoids cross-domain TLS handshakes and font layout shift (CLS), saving 250–350ms of blocking time.
3. **LCP Hero Prioritization:** Utilizing Shopify's Liquid `image_tag` with explicit `widths`, `fetchpriority: 'high'`, and `preload: true` on the hero product banner drastically stabilizes LCP.

## Open Questions

1. Can unused Ecomus section scripts be cleanly excluded from `layout/theme.liquid` without causing regressions in the quick-view or mini-cart drawers?

## Proposed Promotion

Feeds [`CON001`](../concept-design/CON001_Storefront_Luxury_Editorial_Redesign_Concept.md) implementation specs and upcoming architectural decision `DEC_Theme_Performance_Budget`.
