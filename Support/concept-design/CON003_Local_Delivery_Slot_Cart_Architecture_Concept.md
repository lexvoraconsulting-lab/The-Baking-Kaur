<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-dark.svg">
  <img alt="Concept Design" src="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-light.svg" width="100%">
</picture>

# Concept — Local Delivery & Slot Cart Architecture (`CON003`)

> **Parent:** [`concept-design-master.md`](./concept-design-master.md) · **Status:** `Planned` · **Date:** 2026-09-06
> **Cross-cut:** none
> **Decision:** [`DEC_Pending`](../decisions/decisions-master.md) · **Fed Plan:** [`SLOT`](../plans/01-storefront/PLN001-local-delivery-and-time-slot-order-capture-plan.md)

---

## 1. Problem

The studio operates locally in Meerut (~15 km radius, ₹350 minimum order) delivering fragile, freshly baked cakes. However, the "Date Time Picker" custom liquid block in `templates/product.json` is currently empty (`"custom_liquid": ""`). Customers can add cakes to cart without specifying delivery date, time slot, or personalized message, causing operational friction and manual WhatsApp follow-ups.

## 2. Concept

Implement a zero-bloat native picker utilizing `bk-datetime.liquid` (from `tbk-spfy-design/theme_files/snippets/`):
- **Line-Item Properties:** Bind inputs directly to `properties[Delivery Date]`, `properties[Time Slot]`, and `properties[Cake Message]`, ensuring order details flow natively to Shopify Admin and checkout without third-party app fees.
- **Lead-Time Rules:** Provide calendar validation restricting same-day orders past baking cutoffs and enforcing minimum notice for multi-tier fondant cakes.
- **Visual Harmony:** Match the existing theme styling (rose `#7a2147`, soft border `#f2d6dd`, pill background `#fff7f8`) without altering the product page layout or purchase button flow.

## 3. Ideas Backlog

| S.No. | Idea | Notes |
| ---: | --- | --- |
| 1 | Render `bk-datetime` in Product Template | Connect snippet into `"custom_liquid_4rGhVM"` in `templates/product.json`. |
| 2 | Time Slot Selector | Provide structured slots (e.g., 10 AM–1 PM, 1 PM–4 PM, 4 PM–7 PM, 7 PM–10 PM). |
| 3 | Personalized Cake Inscription Field | Allow custom piping text up to 25 characters stored as a line-item property. |
| 4 | Cart & Checkout Line Display | Ensure properties display cleanly in cart drawer and checkout order summary. |

## 4. Scope

- **In Scope:** `snippets/bk-datetime.liquid`, block integration in `templates/product.json`, cart display confirmation.
- **Out of Scope:** Core product page redesign (remains strictly a protected module).

## 5. Open Questions

1. What is the exact kitchen lead-time cutoff for same-day delivery orders (e.g., 4 hours notice)?
2. Should midnight delivery have a dedicated separate slot and surcharge handling?

## 6. Promotion Path

`CON003` -> Decision -> Architecture / Rules -> Plan -> Worklog.

## Footer

Parent: [`concept-design-master.md`](./concept-design-master.md) ·
Decisions: [`../decisions/decisions-master.md`](../decisions/decisions-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
