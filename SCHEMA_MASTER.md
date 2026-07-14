# SCHEMA_MASTER.md — The Baking Kaur

Canonical structured-data reference. One entity per source; no duplicates (enforced Phase A). Detailed strategy in `SEO_GEO_MASTER_PLAN.md §1`.

## Entity graph
```
Organization (#organization)
   └─ is a ─▶ Bakery / LocalBusiness (#bakery, Meerut, NAP+geo+hours+areaServed)
Product (Cake) ─ hasOccasion / hasFlavor / hasTheme / availableDelivery / makesOffer(Offer, INR)
WebSite (#website) ─ SearchAction (sitelinks searchbox)
BreadcrumbList ─ per template
```

## Canonical sources (who emits what)
| Entity | Source snippet | Scope |
|---|---|---|
| Organization + WebSite (+SearchAction) | `tbk-schema-website.liquid` | all pages |
| Bakery / LocalBusiness | `bk-local-business.liquid` | all pages |
| BreadcrumbList (page-aware) | `tbk-schema-breadcrumb.liquid` | all pages |
| Product / Article (native) | `structured-data.liquid` | product/article only |
| FAQPage | inline `theme.liquid` | ⚠ currently global — MUST become page-scoped (Phase F) |

## Per-template plan
- **Home:** Org+WebSite+Bakery+Breadcrumb; + `ItemList` (occasions/bestsellers/hampers); Review/AggregateRating only if real; no Product schema.
- **Collection:** + `CollectionPage` + `ItemList` + Breadcrumb.
- **Product (protected UI):** native `Product` + `Offer`(INR, availability) + brand; add `AggregateRating`/`Review` only when real. Schema-only additions allowed.
- **Article/Blog:** `Article` + Breadcrumb.
- **Pages (landings/guides):** `WebPage`/`Service`/`HowTo`/`FAQPage` as fits, page-scoped.
- **Footer:** `SiteNavigationElement` (site-footer).

## Rules
1. One instance per entity per page (no duplicates).
2. `AggregateRating`/`Review` ONLY with real, on-page-verifiable reviews (no self-asserted ratings — removed Phase A pending).
3. FAQPage only on pages with visible matching FAQ.
4. NAP + `sameAs` identical everywhere (reconcile the two historical geo/address variants → one truth).
5. Validate every changed template in Google Rich Results Test before promoting to live.

## Pending (Phase F)
Link `Bakery @id` into `Organization`; remove self-asserted AggregateRating; page-scope FAQ; add Product/Offer/Review; add CollectionPage/ItemList.

_v0.1 — reflects Phase-A dedup._
