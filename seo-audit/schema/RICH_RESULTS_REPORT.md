# Rich Results Report

Which entity types are likely eligible for Google Rich Results, based on code-level review only —
**no live Rich Results Test has been run**, since the storefront is password-gated (SEO-022). This
report states what the markup *should* qualify for structurally; it is not a substitute for running
the real test once the site is public (see [SCHEMA_VALIDATION.md](SCHEMA_VALIDATION.md)).

## Likely eligible, structurally (Estimated — not live-tested)

| Entity | Page type | Notes |
|---|---|---|
| `Product` | Every product page | Now exactly one entity per page (SEO-023 fixed); has `offers`/`price`/`availability` — the minimum Google requires. `main-product.liquid`'s richer version additionally has real `MerchantReturnPolicy`/`shippingDetails`, which Google's Merchant Listing rich result increasingly expects |
| `BreadcrumbList` | Product/collection/article/page | Correct `position`/`item` structure |
| `Article` | Blog posts | Has `headline`/`image`/`datePublished`/`author` — the required fields for Article rich results |
| `Organization`/`WebSite` | Sitewide | Powers the Sitelinks Search Box and knowledge-panel-style branding, not a "rich result" in the strict sense but part of the same eligibility family |

## Not currently eligible, and why

| Entity | Page type | Reason |
|---|---|---|
| `FAQPage` | `page.faq-01`/`page.faq-02` | Google restricted FAQ rich results to "well-known, authoritative government and health websites" in 2023 — a general bakery site is very unlikely to qualify for the rich result regardless of schema correctness. The schema is still valuable for AI-search/GEO purposes (see [../seo/GEO_AUDIT.md](../seo/GEO_AUDIT.md)) even without the SERP rich result. Currently also blocked separately by SEO-013's placeholder content |
| `Product` — merchant listing experience specifically | Every product page | Full Merchant Listing eligibility typically also wants a connected reviews source for star ratings in the SERP snippet — none exists (0 real reviews, correctly not fabricated) |

## Not present, not applicable

`VideoObject`, `Person` — no video content or named-author content exists on this storefront
currently; not a gap, just not a content type in use.

## Recommended verification sequence once public

1. Google Rich Results Test on: one product per template (4 total), one collection, one blog
   article, homepage.
2. Google Search Console's own Enhancements reports, once the site is indexed, for any
   Google-detected structured-data errors this code-level review couldn't catch (e.g. render-time
   Liquid bugs that only manifest for specific product/edge-case data).

## Related

[SCHEMA_VALIDATION.md](SCHEMA_VALIDATION.md), [SCHEMA_SCORECARD.md](SCHEMA_SCORECARD.md).
