<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/architecture-dark.svg">
  <img alt="Architecture" src="../../skills/ThemeStyleOps/assets/banners/lexvora/architecture-light.svg" width="100%">
</picture>

# ARC_20260906_C — Shopify Online Store 2.0 Theme Architecture

> **Date:** 2026-09-06 · **Status:** Current Architecture
> **Related Concepts:** [`CON001`](../concept-design/CON001_Storefront_Luxury_Editorial_Redesign_Concept.md), [`CON003`](../concept-design/CON003_Local_Delivery_Slot_Cart_Architecture_Concept.md)
> **Related Research:** [`RSH_20260906_A`](../research/RSH_20260906_A_theme_performance_budget_ecomus.md)
> **Owning Plans:** [`HOME`](../plans/01-storefront/PLN003-homepage-editorial-rebuild-s1-s8-plan.md), [`SLOT`](../plans/01-storefront/PLN001-local-delivery-and-time-slot-order-capture-plan.md)

---

## 1. Theme Topology

- **Base Theme:** Ecomus v1.6.1 (Online Store 2.0).
- **Design Tokens:** `snippets/tbk-tokens.liquid` providing CSS custom properties:
  - Color ramp: Rose `#7a2147`, soft background `#fff7f8`, pill border `#f2d6dd`.
  - Typography: *Cormorant Garamond* (headings) + *Manrope* (interface body).
- **Component Primitives:** `snippets/tbk-components.liquid`.

## 2. Protected Module Invariant
- `templates/product.json` and `sections/main-product-premium-v2.liquid` are strictly protected modules.
- Slot selection is integrated non-destructively via `"custom_liquid_4rGhVM"` using `snippets/bk-datetime.liquid`.\n