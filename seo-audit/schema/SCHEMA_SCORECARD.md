# Schema Scorecard

Per-entity qualitative status, post-fix (`4d23a2e`). No numeric scores — each band cites the
specific evidence, per this audit's standing no-fabrication rule.

| Entity | Status | Evidence |
|---|---|---|
| `Organization` | Verified good | Dynamic (real logo/phone/address), `sameAs` now consistent with `Bakery` entity (SEO-020 fixed) |
| `Bakery` (LocalBusiness) | Verified good, one open input | Real NAP, deliberate `aggregateRating` omission with a self-documenting in-code guardrail; geo-coordinates unverified (SEO-015, open) |
| `WebSite` + `SearchAction` | Verified good | Dynamic, correctly wired search endpoint |
| `BreadcrumbList` | Verified good | Fully dynamic across all page types, correct structure |
| `CollectionPage` | Verified good | Fully dynamic, real product loop |
| `Product` | **Was Critical (duplicate on all 602 active products), now Fixed** | SEO-023 — exactly one `Product` entity per page now, richest available version kept per template |
| `Article` | Verified good, one open question | Real dates/author; `dateModified` always equals `datePublished` (SEO-021, open, needs Shopify Liquid docs check) |
| `FAQPage` | **Was Critical (sitewide, unconditional), placement now Fixed; content gap remains open** | SEO-024 fixed (no longer renders off-topic sitewide); SEO-013 (Lorem Ipsum on the two real FAQ pages) still open, needs business content |
| `ImageObject` | Verified good | Used correctly within `Organization`/`Article`, no fabrication |
| `Brand` | Verified good | Present within `Product` entities, real business name, no fabricated brand claims |
| `MerchantReturnPolicy`, `OfferShippingDetails` | Verified good | Present in the retained `main-product.liquid` Product block, real values (0-day handling, India-only shipping destination) |
| `VideoObject`, `Person` | Not present | Confirmed absent theme-wide — not a gap, just not yet a content type this store uses |
| `AggregateRating`, `Review` | Correctly absent | No review data exists; both schema types stay absent by design, not by omission |

## What would move this scorecard further

- SEO-013 (real FAQ content) — the last schema-adjacent Critical/High item, needs business input.
- SEO-015 (geo-coordinates verification) — needs Google Maps access.
- SEO-021 (Article `dateModified`) — needs a Shopify Liquid documentation check, low priority.

## Related

[SCHEMA_AUDIT.md](SCHEMA_AUDIT.md), [../audit/SCORECARD.md](../audit/SCORECARD.md).
