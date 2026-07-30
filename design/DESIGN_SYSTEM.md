# Design System

**Canonical hierarchy**: `business/BUSINESS_MASTER.md` → `business/TBK_BRAND_GUIDELINES.md` → this
document. Never contradict either. This document adds engineering-level implementation detail on
top of `TBK_BRAND_GUIDELINES.md` §2 (Visual Identity) — it does not restate that section in full,
and does not introduce any value not already real and live in the codebase, except where explicitly
marked `BUSINESS APPROVAL REQUIRED` / `DESIGN APPROVAL REQUIRED`.

**Source of truth for every value below**: `snippets/tbk-tokens.liquid`, `snippets/tbk-components.liquid`,
`snippets/tbk-button.liquid`, and `config/settings_schema.json` — live, shipped code, verified this pass.

---

## Grid

No explicit CSS grid framework beyond the primitives already shipped in `tbk-components.liquid`:
`.tbkx-grid` (configurable column count via `--tbkx-grid-cols` / `-md` / `-lg` custom properties,
responsive at the two real breakpoints below) and `.tbkx-split` (2-column split at 768px+, with a
`--reverse` modifier for column order). New layouts should compose from these two primitives rather
than hand-rolling a new grid system.

## Spacing

4px base grid: `--tbk-sp-1` (4px) through `--tbk-sp-12` (48px) — 9 steps, defined in
`tbk-tokens.liquid`. Always reference a token; never hardcode a pixel value in new CSS.

## Container Widths

`.tbkx-container` (from `tbk-components.liquid`): `width: min(100%, var(--tbkx-container-max, 1440px))`
— **1440px is the real, shipped default max-width**. Gutter padding scales with breakpoint:
`--tbk-sp-4` (16px) below 768px, `--tbk-sp-6` (24px) at 768px+, `--tbk-sp-8` (32px) at 1150px+.

## Responsive Breakpoints

Only two real breakpoints exist in the shipped component CSS — **do not invent a third or a
different pixel value**:

| Breakpoint | Value | Use |
|---|---|---|
| Medium | `768px` | Tablet — `.tbkx-grid`/`.tbkx-split` shift to multi-column, container gutter increases |
| Large | `1150px` | Desktop — grid columns expand further, container gutter increases again |

The live header (`tbk-header.liquid`) uses a single burger-triggered drawer navigation for **all**
breakpoints (confirmed via its own header comment) — there is no separate horizontal desktop nav bar
to design around; do not assume one exists when building new header-adjacent UI.

## Colors

Full palette already documented in `TBK_BRAND_GUIDELINES.md` §2 — not repeated here. One addition at
the engineering level: Shopify's native Dawn-style `color_scheme_group`/`color_scheme` setting system
is also present in `config/settings_schema.json` (multiple named scheme variants selectable per
section, e.g. `scheme-1`, `scheme-2`). This is Shopify's per-section palette-swap mechanism, **not**
a light/dark mode toggle — see Dark Mode below for that distinction.

## Typography

Full type scale documented in `TBK_BRAND_GUIDELINES.md` §2. Engineering rule: `--tbk-font-display`
(Cormorant Garamond) for headings only, `--tbk-font-ui` (Manrope) for everything else — never mix a
third family into new component CSS.

## Buttons

Fully documented in `TBK_BRAND_GUIDELINES.md` §2 and `COMPONENT_LIBRARY.md`. Always render through
`{% render 'tbk-button' %}` (`snippets/tbk-button.liquid`) — never hand-roll new button markup.

## Cards

`.tbkx-card` family (`tbk-components.liquid`): base card (white surface, `--tbk-border`, `--tbk-r-xl`
radius, `--tbk-shadow-sm`), `--soft` (ivory bg), `--accent` (gradient tint), `--hover` (lift + shadow
on hover, respects `prefers-reduced-motion`). See `COMPONENT_LIBRARY.md` for Product Card/Collection
Card specifics built on top of this base.

## Forms

**Real architecture note**: forms use a separate, older component naming system (`hdt-` prefix —
Dawn/Ecomus-derived), not the newer `tbk-`/`tbkx-` design-system prefix. Both systems are real and
live simultaneously; this is a documented coexistence, not a conflict to silently resolve. Real,
shipped classes: `.hdt-form__message` / `.hdt-form-message--success` / `.hdt-form-message--error`
(`snippets/form-status.liquid`, `snippets/back-instock.liquid`, `snippets/buy-buttons.liquid`,
`snippets/gift-card-recipient-form.liquid`). New forms should reuse this existing message/error
pattern rather than introduce a third styling convention. **`DESIGN APPROVAL REQUIRED`**: whether
forms should be migrated to the `tbk-`/`tbkx-` token system — not decided, out of scope for this
document.

## Inputs

Real, shipped class: `.hdt-input` (e.g. `snippets/back-instock.liquid`'s email field). No dedicated
`tbkx-input` component exists yet. **`DESIGN APPROVAL REQUIRED`** for a token-based input component
if the design system is extended to cover forms fully.

## Icons

Documented in `TBK_BRAND_GUIDELINES.md` §2: inline SVG, stroke-based (not filled), `stroke-width:
1.9`, round caps/joins. Sizes `--tbk-icon-xs` (14px) through `--tbk-icon-lg` (22px). The `hdt-`
component family (predictive search, cart drawer) uses its own separate icon set — do not mix stroke
styles within one visual region.

## Shadows

`--tbk-shadow-xs` / `-sm` / `-md` / `-lg` (escalating blur/spread, warm-toned via `rgba(26,8,16,...)`
+ a pink-tinted secondary shadow layer), plus purpose-specific `--tbk-shadow-header` and
`--tbk-shadow-dropdown`. Focus rings use `--tbk-focus-ring` (3px pink-tinted ring) and
`--tbk-search-ring` (4px, for the search field specifically). Always use a token; never hand-tune a
one-off `box-shadow` value.

## Border Radius

`--tbk-r-xs` (4px) through `--tbk-r-full` (100px). Buttons: full/pill. Cards: `--tbk-r-xl` (24px).
Media/images within cards: `--tbk-r-lg` (16px) or `--tbk-r-xl` depending on context — see
`.tbkx-card__media` vs. `.tbkx-media` in `tbk-components.liquid`.

## Animation

Easing: `--tbk-ease` (standard), `--tbk-ease-out`, `--tbk-ease-spring` (bouncy, for playful
micro-interactions). Durations: `--tbk-dur-fast` (140ms) through `--tbk-dur-drawer` (380ms, the
mobile drawer's own transition length). **Rule, already enforced at the token level**: under
`prefers-reduced-motion: reduce`, all four duration tokens collapse to `0ms` automatically — any new
animated component inherits this for free by using the duration tokens; do not hardcode a duration
that bypasses this.

## Loading

**No dedicated skeleton-screen or loading-spinner design pattern was found as a documented,
reusable component.** Scattered "loading" references exist in cart/buy-button JS but not as a named,
reusable visual pattern. **`DESIGN APPROVAL REQUIRED`** before building a new loading-state
component — don't invent one ad hoc per feature.

## Accessibility

- Touch targets: `--tbk-touch` (44px, WCAG 2.5.5 minimum) and `--tbk-touch-lg` (48px) — real,
  already-defined tokens; never ship an interactive element smaller than 44px.
- `prefers-reduced-motion` respected at the token level (see Animation above).
- Native semantic disclosure (`<details>/<summary>`) used for both the FAQ accordion
  (`sections/accordion.liquid`) and the mobile navigation drawer (`tbk-header.liquid`) — a real,
  consistent, accessible pattern; extend it for new collapsible UI rather than building a custom JS
  accordion.
- Icon-only buttons require `aria-label` — already enforced in `tbk-button.liquid`'s own logic.

## Dark Mode

**Not implemented.** No `prefers-color-scheme` media query, no `data-theme` attribute toggle, and no
dark-palette token set exist anywhere in `tbk-tokens.liquid` or the theme. Shopify's native
`color_scheme_group`/`color_scheme` settings (`config/settings_schema.json`) provide **per-section
palette variants** (e.g. `scheme-1`, `scheme-2`), which is a different mechanism from an automatic
light/dark toggle and should not be conflated with one. **`BUSINESS APPROVAL REQUIRED`** if dark
mode is ever wanted — this would be new design and engineering work, not a hidden existing feature.

---

## What this document does not do

No code is written or modified by this document. It documents the real, already-shipped design
system exactly as it exists in the live codebase, and marks every genuine gap (forms/inputs token
coverage, loading states, dark mode) as requiring design or business approval rather than inventing a
new standard unilaterally.

## Related

[../business/BUSINESS_MASTER.md](../business/BUSINESS_MASTER.md),
[../business/TBK_BRAND_GUIDELINES.md](../business/TBK_BRAND_GUIDELINES.md),
[COMPONENT_LIBRARY.md](COMPONENT_LIBRARY.md), [CONTENT_SYSTEM.md](CONTENT_SYSTEM.md),
[COPY_GUIDELINES.md](COPY_GUIDELINES.md).
