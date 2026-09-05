# ANIMATION_GUIDELINES.md — The Baking Kaur

Motion system. Restraint is the brand. Tokens in `DESIGN_SYSTEM.md` / `tbk-tokens.liquid`.

## Principles
1. Motion clarifies, never decorates.
2. Enter with `--tbk-ease-out`; confirmations may use `--tbk-ease-spring` (add-to-cart, selection).
3. 60fps only — animate `transform`/`opacity`, never layout properties.
4. Everything off under `prefers-reduced-motion: reduce`.

## Tokens
Easing: `--tbk-ease` (standard) · `--tbk-ease-out` (enter) · `--tbk-ease-spring` (celebrate).
Duration: fast 140ms · base 220ms · slow 340ms · drawer 380ms.

## Allowed
- Hover: lift (translateY −1 to −2px) + shadow step-up + media zoom ≤1.03.
- Link: color transition 140–160ms; underline-grow.
- On-scroll reveal: opacity 0→1 + translateY 8px→0, **once**, 300ms ease-out, stagger ≤80ms.
- Accordion/drawer: height/transform ease, 220–380ms.
- Loading: spinner or shimmer skeleton (no CLS).
- Add-to-cart confirm: subtle spring check.

## Forbidden (per brand: no flashy)
Parallax · autoplay carousels · marquee/infinite tickers as hero · glassmorphism · gradient/color animations · bounce/wobble · motion on every element · anything that delays LCP or causes shift.

## Rules
- Reveal animations never gate content (content visible if JS fails / reduced-motion).
- No animation on the hero LCP element.
- Respect reduced-motion globally: `@media (prefers-reduced-motion: reduce){ *{animation:none!important;transition:none!important} }` scoped per section.
- Carousels: CSS scroll-snap first; JS enhances, not required.

_v0.1 — motion standard for all sections._
