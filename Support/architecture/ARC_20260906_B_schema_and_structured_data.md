<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/architecture-dark.svg">
  <img alt="Architecture" src="../../skills/ThemeStyleOps/assets/banners/lexvora/architecture-light.svg" width="100%">
</picture>

# ARC_20260906_B — Schema.org & LocalBusiness Structured Data Architecture

> **Date:** 2026-09-06 · **Status:** Current Architecture
> **Related Concepts:** [`CON004`](../concept-design/CON004_Verified_Trust_Framework_Fssai_Entity_Concept.md)
> **Related Research:** [`RSH_20260906_C`](../research/RSH_20260906_C_localbusiness_precision_geo_coordinates.md)
> **Owning Plan:** [`TRST`](../plans/02-operations/PLN002-verified-trust-framework-and-localbusiness-schema-plan.md)

---

## 1. System Boundary

This architecture governs all machine-readable JSON-LD structured data rendered to search engine crawlers and AI answer engines across `thebakingkaur.com`.

## 2. Graph Node Specifications

| S.No. | Schema Entity | Target Surface | Implementation File | Key Properties |
| ---: | --- | --- | --- | --- |
| 1 | `LocalBusiness` / `Bakery` | Site-wide `<head>` | `snippets/bk-local-business.liquid` | Name, NAP, GeoCoordinates (`28.9845, 77.7064`), FSSAI PropertyValue, openingHours |
| 2 | `Product` | Product detail pages | `snippets/structured-data.liquid` | Name, image, offers (Price, INR, inStock), brand, itemCondition (strictly no fake ratings) |
| 3 | `Organization` | Site-wide | `snippets/structured-data.liquid` | Logo, sameAs (Instagram, GBP listing), contactPoint |
| 4 | `BreadcrumbList` | Category & Product | Theme templates | Hierarchy trail |

## 3. Invariants & Zero Duplication Rule
- Never emit duplicate `LocalBusiness` nodes.
- Only emit `AggregateRating` when backed by verified third-party reviews (Google Business Profile or Judge.me).\n