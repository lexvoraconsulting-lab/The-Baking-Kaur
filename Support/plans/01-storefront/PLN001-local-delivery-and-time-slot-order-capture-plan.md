# Plan — Local Delivery and Time Slot Order Capture (`SLOT`)

> **Parent:** [`../plans-master.md`](../plans-master.md) · **Code:** `SLOT`
> **Status:** Active · **Owner:** Agent

## Sources and Traceability

| S.No. | Code | Source record | Plan role | Status |
| ---: | --- | --- | --- | --- |
| 1 | `RUL` | [`../../rules.md`](../../rules.md) | Binding constraints and governance | Current |
| 2 | `CON` | `../../concept-design/CON003_Local_Delivery_Slot_Cart_Architecture_Concept.md` | Delivery slot and line-item properties specification | Current |

## Statistics

`TL = PD + IP + CD`. From task markers below.

| S.No. | Plan Scope | TL | PD | IP | CD |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `SLOT` direct tasks | 6 | 6 | 0 | 0 |
| 2 | Total | **6** | **6** | **0** | **0** |

## Context

The studio operates locally in Meerut (~15 km radius, ₹350 minimum order) delivering fresh, fragile eggless cakes. This plan connects `snippets/bk-datetime.liquid` into `"custom_liquid_4rGhVM"` of `templates/product.json` to capture `Delivery Date`, `Time Slot`, and `Custom Cake Inscription` as cart line-item properties natively, without third-party app dependencies or recurring fees.

## 01. Integration Tasks

- [ ] `SLOT-01.01` Create baseline restore point of `templates/product.json` before modification.
- [ ] `SLOT-01.02` Deploy `snippets/bk-datetime.liquid` into local theme repository.
- [ ] `SLOT-01.03` Connect `{% render 'bk-datetime' %}` into `"custom_liquid_4rGhVM"` within `templates/product.json`.
- [ ] `SLOT-01.04` Validate line-item properties (`properties[Delivery Date]`, `properties[Time Slot]`, `properties[Cake Message]`) on product form submission.
- [ ] `SLOT-01.05` Deploy scoped changes to preview theme `#151370334377` and verify zero visual regression on protected product page.
- [ ] `SLOT-01.06` Confirm properties display in cart drawer, checkout order summary, and Shopify Admin order details.

## Footer Navigation

Parent: [`../plans-master.md`](../plans-master.md) · Plans Master: [`../plans-master.md`](../plans-master.md)
