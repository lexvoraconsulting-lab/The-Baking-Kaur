<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../skills/ThemeStyleOps/assets/banners/lexvora/documentation-dark.svg">
  <img alt="Documentation" src="../../../skills/ThemeStyleOps/assets/banners/lexvora/documentation-light.svg" width="100%">
</picture>

# Living Design System — The Baking Kaur

> **Authority:** Living Design Standard · **Parent:** [`../documentation-plan.md`](../documentation-plan.md)
> **Active Tokens:** `snippets/tbk-tokens.liquid` · **Components:** `snippets/tbk-components.liquid`
> **Associated Plan:** [`HOME`](../../plans/01-storefront/PLN003-homepage-editorial-rebuild-s1-s8-plan.md)

---

## 1. Editorial Aesthetic Principles (`stitch-design-taste`)

The visual design elevates The Baking Kaur to the aesthetic stature of a bespoke luxury cake atelier:
- **Quiet Confidence:** Generous whitespace, airy margins, and intentional negative space instead of cluttered card walls.
- **Micro-Delight:** Refined border radii (`12px` cards, `9999px` pill tags), soft 1px borders (`#f2d6dd`), and subtle ambient depth rather than heavy drop shadows.
- **Tactile Materiality:** Warm rose, soft ivory parchment, and subtle champagne gold accents.

## 2. Color Tokens

| S.No. | Token Name | Hex Value | Semantic Usage |
| ---: | --- | --- | --- |
| 1 | `--tbk-color-primary` | `#7a2147` | Canonical Deep Brand Rose: primary buttons, emphasis typography |
| 2 | `--tbk-color-pill-bg` | `#fff7f8` | Soft Rose Cream: badge and pill backgrounds |
| 3 | `--tbk-color-pill-border` | `#f2d6dd` | Delicate Border Accent: card and tag outlines |
| 4 | `--tbk-color-accent-gold` | `#c5a059` | Champagne Gold: luxury badges and artisanal flourishes |
| 5 | `--tbk-color-surface` | `#ffffff` | Pure White: primary card background |
| 6 | `--tbk-color-text-body` | `#2b2b2b` | High-contrast readable charcoal for editorial copy |

## 3. Typographic Ramp

| S.No. | Element | Font Family | Weight / Style | Line Height / Letter Spacing |
| ---: | --- | --- | --- | --- |
| 1 | Hero H1 | *Cormorant Garamond* | 700 / Italic accent | 1.1 / -0.02em |
| 2 | Section H2 | *Cormorant Garamond* | 600 Semi-Bold | 1.2 / -0.01em |
| 3 | Subsection H3 | *Cormorant Garamond* | 600 Semi-Bold | 1.3 / Normal |
| 4 | Body Copy | *Manrope* | 400 Regular | 1.6 / Normal |
| 5 | UI Labels / Pills | *Manrope* | 600 Semi-Bold | 1.2 / +0.05em uppercase |
