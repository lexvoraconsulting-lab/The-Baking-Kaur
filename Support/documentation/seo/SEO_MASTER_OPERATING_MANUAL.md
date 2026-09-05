<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../skills/ThemeStyleOps/assets/banners/lexvora/documentation-dark.svg">
  <img alt="Documentation" src="../../../skills/ThemeStyleOps/assets/banners/lexvora/documentation-light.svg" width="100%">
</picture>

# SEO & Local Search Operating Manual

> **Authority:** Technical SEO Standard · **Parent:** [`../documentation-plan.md`](../documentation-plan.md)
> **Associated Plans:** [`TRST`](../../plans/02-operations/PLN002-verified-trust-framework-and-localbusiness-schema-plan.md), [`SLOT`](../../plans/01-storefront/PLN001-local-delivery-and-time-slot-order-capture-plan.md)

---

## 1. Title & Meta Tag Formulas

| S.No. | Page Type | Title Tag Template | Character Limit |
| ---: | --- | --- | ---: |
| 1 | Active Products (Standard) | `{Name} - Eggless &#124; Meerut` | ≤ 60 chars |
| 2 | Active Products (Long Title) | `{Name} &#124; Meerut` | ≤ 60 chars |
| 3 | Collections | `{Category} Cakes in Meerut &#124; 100% Eggless - The Baking Kaur` | ≤ 60 chars |
| 4 | Homepage | `The Baking Kaur &#124; 100% Eggless Luxury Cake Studio Meerut` | ≤ 60 chars |

## 2. Admin GraphQL Execution Rules
- Always run scripts in `--dry-run` first.
- Provide both `seo.title` and `seo.description` in mutation inputs.
- Limit mutation batches to ≤ 8–10 aliased mutations per request.
