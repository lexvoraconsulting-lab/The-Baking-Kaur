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

---

## 🔒 B2 — BUTTON SYSTEM: FROZEN (2026-07-15)
Files: `snippets/tbk-components.liquid` (CSS, rendered once via `tbk-header`) + `snippets/tbk-button.liquid` (render helper). Token-only.
**CSS namespace: `.tbkx-btn*`** — renamed from `.tbk-btn` after discovering `.tbk-btn`/`.tbk-card` already exist in `base.css` + `tbk-header` + the **protected** `main-product-premium-v2` PDP. All new B-phase component classes use the collision-free `tbkx-` prefix so they never touch existing/protected UI. Snippet API (`{% render 'tbk-button' %}`) unchanged.
- **Variants:** primary (solid pink/white) · secondary (ink outline) · ghost · whatsapp (green accent, ink label) · signature (gold accent, ink label).
- **Sizes:** xs 32 · sm 40 · md 48 · lg 56 · xl 64. Primary mobile actions ≥ md (touch ≥44px); xs/sm = dense/desktop non-primary only.
- **States:** default · hover (mid + lift + shadow) · active · focus-visible (pink ring) · disabled (50%, no pointer) · loading (per-variant spinner, pointer blocked) · success (#1B7A3D + check).
- **Icons:** left · right · only (square, aria-label required); thin-line 1.6px, 18px, currentColor; gap 8px.
- **Accessibility validated:** white-on-pink ~6:1 AA, white-on-success ~5:1 AA, ink labels AAA; gold/green as accents only (fail small-text). Real `<a>`/`<button>`; motion off under reduced-motion.
- **Usage:** `{% render 'tbk-button', label:'…', href:'…', variant:'…', size:'…', block:true, icon:ic, icon_position:'left|right|only', state:'loading|success' %}`.
Frozen — no button changes without explicit unfreeze.

## 🔒 B3 — CARD SYSTEM: FROZEN (2026-07-15)
`snippets/tbk-components.liquid`, `.tbkx-card*` namespace (collision-free). One card language, 6 commerce types.
- **Types:** product (4:5, price gold, badge, ATC foot) · collection (1:1, display title) · content (3:2, guide/story) · review (media-less, stars+author) · trust (icon+copy) · delivery (icon+pill+copy).
- **States:** default · hover (lift −2px + 1.03 media zoom + shadow-md) · focus-visible · loading (skeleton shimmer) · empty (guiding CTA) · error (message + Retry) · image fallback (aspect-boxed placeholder).
- **Edge cases validated:** long/short title, missing image/price/rating/description → graceful omission, no CLS.
- **Per-card strategy** (business/intent/conversion/SEO/GEO/analytics/links/metafields/metaobjects/extensibility) documented in the card-validation deliverable; data sources per `DATA_ARCHITECTURE.md` (product: `custom.badge/is_bestseller/same_day_eligible`; collection: `custom.subtitle/hero_image`; review: `testimonial`; trust: `trust_stat`; delivery: `same_day/midnight_eligible`).
- **A11y:** one focusable link per card (avoid nested interactives), focus ring, alt images, decorative icons aria-hidden, star ratings need text equivalent, ≥4.5:1 text.
- **Responsive:** grid 4→2→1; fixed media ratios (no CLS); equal heights via flex; foot pinned bottom.
Frozen — no card changes without explicit unfreeze.

## 🔒 B4 — COMMERCE FORM SYSTEM: FROZEN (2026-07-15)
`snippets/tbk-components.liquid`, `.tbkx-` namespace, **class-scoped only** (native inputs — incl. the protected PDP's — untouched).
- **Base:** `tbkx-field` · `tbkx-label` (+`__req`) · `tbkx-input` / `tbkx-select` (chevron) / `tbkx-textarea` · `tbkx-help` · `tbkx-error` · `tbkx-check` (checkbox/radio, brand accent). States: default · focus (pink border + glow) · error `#A3123A` · success `#1B7A3D` · disabled.
- **5 commerce primitives:** `tbkx-pills`/`tbkx-pill` (radiogroup chips, **44px** touch) · `tbkx-input-group` (coupon) · `tbkx-file` (upload) · `tbkx-counter` (+`--over`) · `tbkx-field-grid` (address 2-col → 1-col ≤520px).
- **12 commerce fields compose from those primitives** (no one-offs): delivery date (native `type=date`, min today/max +30d) · delivery time (pills) · cake message (40-char + counter) · upload design (image/*, ≤10 MB) · flavour · weight · shape · theme (pills) · occasion (select ← `celebration-type`) · address (field-grid + autocomplete) · coupon (input-group + loading/success/error/retry) · gift message (200-char + counter).
- **Contract:** validate on blur + submit (focus first invalid) · loading = button spinner · success = green + confirm line · error = red + human message · **retry never clears input** · required marked `*` + `required` (never colour alone).
- **Keyboard/autofill:** `inputmode=tel|numeric`; `autocomplete=name|tel|street-address|address-level2|postal-code`; coupon `autocapitalize=characters`.
- **A11y:** bound labels / fieldset+`role=radiogroup`; `aria-describedby`+`aria-invalid` for errors; 44px targets; focus-visible ring; counters are text not colour.
- **Validation finding fixed:** choice pills were 40px → raised to `--tbk-touch` (44px).
Frozen — no form changes without explicit unfreeze.


## 🔒 S1 — EDITORIAL HERO (Homepage §1): **VERSION 1.0** — FROZEN (2026-07-15)
`sections/home-hero.liquid`. **Assembly only — zero new components.** Composed from frozen tokens + frozen `tbk-button` (`primary`, `whatsapp`). `tbkx-` namespaced → protected PDP isolated.
- Layout: editorial 5:7 grid ≥990px; single column below; CTAs full-width <560px.
- Image: WebP · srcset 600/900/1200/1600 · explicit w/h · `fetchpriority=high` · `eager` · `decoding=async` · art-directed preload · SEO alt + title. Source resolution: uploaded Files master **overrides** temporary product source (merchant-editable, zero code to swap).
- Validated: one H1 · CLS 0 · desktop 3:2 / mobile 4:5 · no sliders/autoplay/carousels · no overflow.
- Asset status: **Temporary Production Hero** (product `b32`) — see backlog "Flagship Hero Photoshoot".
Frozen — no changes without explicit unfreeze.

_v1.0 — S1 Editorial Hero frozen (Homepage §1). v0.4 — B4 commerce forms frozen. v0.3 — B3 cards frozen. v0.2 — B2 buttons frozen. v0.1 — governs all section/snippet builds._
