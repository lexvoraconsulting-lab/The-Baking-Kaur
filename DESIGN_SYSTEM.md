# DESIGN_SYSTEM.md — The Baking Kaur

**Cross-reference (added 2026-07-31, Phase 7.0 reconciliation)**: `design/DESIGN_SYSTEM.md` is a
later, code-verified companion to this document — it adds engineering-level implementation detail
grounded directly in shipped code (`snippets/tbk-tokens.liquid`, `tbk-components.liquid`,
`tbk-button.liquid`, `config/settings_schema.json`) on top of this blueprint. Read both; this file
is the original vision document, `design/DESIGN_SYSTEM.md` is the implementation-detail layer.
Neither supersedes the other. See `docs/CANONICAL_SOURCES.md`.

The single UI standard for the flagship. Source of truth for tokens:
**`snippets/tbk-tokens.liquid`** ("Design System v1.0"), rendered once from the header — all CSS custom properties cascade page-wide. This document explains and governs those tokens; ⊕NEW marks approved Foundation (B★) extensions not yet implemented.

Protected (never change): logo · brand colors · product page design/UX/flow.

---

## 1. Color (preserved — governed)
Canonical ramp (from `tbk-tokens.liquid`):

| Token | Hex | Role |
|---|---|---|
| `--tbk-pink` | #C01457 | Primary — CTAs, links, active, price |
| `--tbk-pink-mid` / `-deep` | #A81248 / #8B0D3C | Hover / deep accents |
| `--tbk-gold` / `-light` | #B8852A / #D4A645 | Luxury accent (rare) |
| `--tbk-ink` / `-soft` | #1A0810 / #3B1F2E | Text |
| `--tbk-muted` / `-light` | #876575 / #B39BAA | Secondary text |
| `--tbk-surface` / `-el` / `-sub` | #FDFAF8 / #FFFFFF / #F8F2F6 | Surfaces |
| `--tbk-tint-1` / `-2` | #FEF3F8 / #FDEAF2 | Hover / selected |
| `--tbk-border` / `-strong` | #EDD8E3 / #D4ADC0 | Hairlines / emphasis |
| WhatsApp green | #25D366 | **Functional only** |

**Rules:** 60-30-10 (surface/ink/accent) · one pink (retire drift shades `#ff4d88`,`#ff2b6d`,`#d81b63` → map to ramp) · gold is scarce · green = WhatsApp only · warm neutrals only (no cold grey / pure black).

## 2. Typography
Families: `--tbk-font-display` = **Cormorant Garamond** (editorial) · `--tbk-font-ui` = **Manrope** (UI).
⊕ Extended scale (v1.0 tops at 22px — too small for flagship). Fluid `clamp()`:

| Token | Font | mobile→desktop |
|---|---|---|
| display-hero ⊕ | Cormorant 600 | 40→72px |
| display-1 ⊕ | Cormorant 600 | 32→52px |
| display-2 ⊕ | Cormorant 600 | 26→38px |
| heading | Cormorant 700 | 22→28px |
| title | Manrope 700 | 18→20px |
| body-lg / body | Manrope 400 | 16 / 14–15px |
| label / caption | Manrope 600 / 500 | 12.5 / 11px |
| overline ⊕ | Manrope 600 +0.14em UPPER | 11px |

Line-height: display 1.05–1.15 · body 1.55–1.7. Measure ≤66ch. One display-hero per page.

## 3. Spacing (4px grid)
`--tbk-sp-1…12` = 4→48px. ⊕ Add `sp-16/20/24/32` = 64/80/96/128px for section rhythm.
Section gaps: desktop 96–128px · mobile 56–72px. Title→content 40–48 / 28–32. "When unsure, add space."

## 4. Radius / 5. Shadow / 6. Motion (from v1.0)
- Radius: `xs4 sm8 md12 lg16 xl24 full100`. Inputs/buttons md · cards lg · media lg/xl · pills full.
- Shadow: `xs→lg` + `header`/`dropdown`, warm pink-tinted. Ladder: flat→sm card→md hover→lg modal.
- Motion: easing `ease`/`ease-out`/`ease-spring`; durations 140/220/340/380ms. Animate transform/opacity only; honor `prefers-reduced-motion`.

## 7. Components (specs — see Foundation doc for full detail)
- **Buttons:** primary solid pink / secondary ink-outline / ghost / WhatsApp(green, functional) / gold-signature. Heights 40/48/56. Visible focus ring. Sentence case.
- **Cards:** one card language sitewide — fixed media ratio, `r-lg`, `shadow-sm`, hover `shadow-md`+zoom 1.03, ≤2 badges.
- **Forms:** `surface-sub` fill, label above, 48px, focus pink ring, error/success states. (PDP controls set the metric standard — PDP itself protected.)
- **Badges:** pill `r-full`; trust / merch / signature / status. Max 2/card.
- **Icons:** ⊕ one thin-line set (1.5px), 24px grid. **Retire emoji-as-UI.**
- **Trust / Review / FAQ / Banner:** per Foundation blueprints; FAQ schema page-scoped only.

## 8. States
Hover (lift+shadow+zoom) · Loading (spinner/disabled) · ⊕Skeleton (shimmer, no CLS) · ⊕Empty (guiding CTA) · ⊕Error (human copy+recovery) · ⊕Success (`ease-spring` confirm+next step).

## 9. Accessibility (WCAG 2.2 AA target)
Contrast ≥4.5:1 body (gold not for small text) · visible focus ring · semantic elements · aria on menus/accordions/drawers · no emoji-as-control · honor reduced-motion · labelled forms.

## 🔒 FOUNDATION STATUS — FROZEN (B1 FINAL, 2026-07-14)
Foundation tokens (color, typography incl. extended display scale, spacing incl. section rhythm, grid, radius, shadow, motion) are **frozen** in `snippets/tbk-tokens.liquid`. No further token changes without an explicit unfreeze. All components (B2+) build on these.

**Validated (measured):** contrast — ink/ink-soft/pink-deep on ivory AAA; pink & white-on-pink AA (~6:1); muted AA (≥4.87:1); **gold = large/decorative only (3.14:1)**. Line-length ≤66ch, body line-height 1.65, touch targets 44/48px, responsive display scale holds 40px floor (320–430px) → ~70px desktop. No issues → frozen.

**Locked usage rule:** gold never for small/body text (large price/number/decorative only).

## Changelog of this document
- v1.1 (Phase B1) — foundation **FROZEN & validated**.
- v0.1 (Phase A) — seeded from `tbk-tokens.liquid v1.0` + Foundation B★ extensions.
