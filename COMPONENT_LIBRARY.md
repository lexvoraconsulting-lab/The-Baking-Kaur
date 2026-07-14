# COMPONENT_LIBRARY.md — The Baking Kaur

Reusable UI component specs. Extends `DESIGN_SYSTEM.md` (tokens) with per-component structure, variants, states, a11y. All components use `tbk-tokens` — no hardcoded colors, one card/radius/shadow language.

## Conventions
- Snippet-per-component; props via `{% render %}` params or metaobject/metafield.
- Every interactive element: visible `:focus-visible` ring (`--tbk-focus-ring`), ≥44px target, semantic element.
- States each component must define: default · hover · focus · active · loading · disabled · empty · error.

## Buttons (`button` classes)
Variants: Primary (solid `--tbk-pink`, white) · Secondary (ink outline) · Ghost/Text · WhatsApp (green, functional only) · Gold-Signature (rare). Sizes 40/48/56px. Sentence case. Hover: `pink-mid` + 1px lift + `shadow-md`.

## Product card — `card-product-premium`
Media 4:5 (`responsive-image`), `r-lg`, `shadow-sm`; title (Manrope 700), price (gold), one micro-trust ("100% eggless"), ≤2 badges. Hover: `shadow-md` + media zoom 1.03 + quick-add reveal. Empty: skeleton. Error: aspect-boxed placeholder.

## Occasion tile — `occasion-tile`
1:1 image + overline + Cormorant title + "Explore →". Source: `occasion_tile` metaobject or collection + `custom.subtitle`/`custom.hero_image`. Hover: image zoom + title→pink.

## Trust row — `trust-row`
Line-icon + label items, hairline separators (desktop), ivory bg. Mobile: wraps to ≤2 lines (no scroll). Content-driven (list). High-contrast ink text.

## Review card — `review-card`
Avatar/initial, name, verified chip, star row (gold), date, body, optional photo, source (Google/Zomato). Source: `testimonial` metaobject. Section hides if none.

## Hamper card — `hamper-card`
Larger media, title, price, "gifting" gold cue. Same card language, hamper aspect.

## Editorial split — `editorial-split`
5/7 or 4/8 image+text; overline + Cormorant heading + body + CTA. Stacks image-first on mobile. Used by Craft, Customization.

## Rating hero
Big Cormorant number + gold stars + count + source logos. Real data only (else omit).

## Badge — pill `r-full`
Trust (ivory/ink) · Merch (pink/white "Bestseller/New") · Signature (gold outline) · Status (green "Same-Day"). Max 2/card.

## Form controls
`surface-sub` fill, label above, 48px, focus pink ring, error (ink-red + msg + icon), success (subtle check). PDP controls set the metric standard (PDP protected — replicate, don't edit).

## FAQ accordion
One open at a time, `ease` height, chevron rotate, hairline dividers, ink question/muted answer. `aria-expanded`/`aria-controls`. Schema only if visible (`SCHEMA_MASTER.md`).

## Icon — `icon`
One thin-line set (1.5–1.6px stroke), 24px grid, currentColor, hover pink. **No emoji as UI.** Decorative icons `aria-hidden`; icon-only controls get `aria-label`.

## Section heading — `section-heading`
Overline (Manrope 600, +0.14em, uppercase, muted-but-AA) + Cormorant display title. One display-hero/page.

## Skeleton / Empty / Error (shared)
Skeleton: shimmer on `surface-sub`, matches final layout, no CLS. Empty: line illustration + calm headline + guiding CTA. Error: human copy + recovery, no raw system text.

_v0.1 — governs all section/snippet builds._
