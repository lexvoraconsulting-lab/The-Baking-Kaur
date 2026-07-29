# Schema Audit

Every `application/ld+json` block found in the theme, per file. Two passes: the first surfaced
SEO-020 and SEO-021; a second, broader pass (`grep` for every `@type` value actually emitted, not
just the files already known) found SEO-023 and SEO-024 — both now fixed (`4d23a2e`). See
[`../issues.yml`](../issues.yml) for the full record, [SCHEMA_CHANGELOG.md](SCHEMA_CHANGELOG.md) for
deploy evidence, and [SCHEMA_SCORECARD.md](SCHEMA_SCORECARD.md) for the current per-entity status.

## Files emitting structured data

`snippets/bk-local-business.liquid`, `snippets/structured-data.liquid`,
`snippets/tbk-schema-article.liquid`, `snippets/tbk-schema-breadcrumb.liquid`,
`snippets/tbk-schema-collection.liquid`, `snippets/tbk-schema-website.liquid`,
`sections/main-product-premium-v2.liquid`, `sections/main-product-premium.liquid`,
`sections/main-product.liquid` (this one intentionally, see SEO-023 below),
`layout/theme.liquid`.

## Every `@type` actually emitted (full enumeration, second pass)

`Answer`, `Article`, `Bakery`, `Blog`, `Brand`, `BreadcrumbList`, `City`, `CollectionPage`,
`DefinedRegion`, `EntryPoint`, `FAQPage`, `GeoCoordinates`, `ImageObject`, `ItemList`, `ListItem`,
`MerchantReturnPolicy`, `MonetaryAmount`, `Offer`, `OfferShippingDetails`,
`OpeningHoursSpecification`, `Organization`, `PostalAddress`, `Product`, `QuantitativeValue`,
`Question`, `SearchAction`, `Service`, `ShippingDeliveryTime`, `SiteNavigationElement`, `WebPage`,
`WebSite`. Not found anywhere: `VideoObject`, `Person`, `AggregateRating`, `Review` — the last two
correctly absent (see `bk-local-business.liquid` below).

## `snippets/bk-local-business.liquid` — Bakery (LocalBusiness)

**Verified good**: the file's own header comment explicitly documents that a hardcoded
"4.8 / 500 reviews" `aggregateRating` was removed on 2026-07-16 for being unbacked by real data, and
states the rule going forward: *"AggregateRating may only ever be emitted from a verified review
source, computed from real entries — never typed in."* This is a deliberate, self-documenting
guardrail already in place — no action needed, and a good pattern worth preserving.

Real NAP data present: phone `+918218862928`, address (Fatah Complex, Thapar Nagar Lane 7, Meerut,
UP 250001, IN). **SEO-015 (open, Requires Manual Verification)**: the geo-coordinates
(`28.9931, 77.6939`) carry an in-code comment asking the merchant to verify them against Google
Maps — not yet done as far as this audit could confirm.

## `snippets/structured-data.liquid` — Product & Article (Shopify-native)

Uses Shopify's built-in `| structured_data` filter on the `product`/`article` object. **Verified
safe by construction**: since no review app is connected and no product has real review data, this
filter cannot emit a fabricated `aggregateRating` or `review` block — it only outputs what's
actually present on the object.

**SEO-023 (Fixed, `4d23a2e`)**: this native Product emission was found to duplicate a second,
hand-rolled `@type: "Product"` block that three separate product section files each carried
independently — see the Product schema section below for full detail. This snippet now excludes its
own native emission specifically for `template.suffix == 'hampers-template'`, since that template's
own hand-rolled block is richer (has fields the native filter doesn't produce) and is kept instead.

## Product schema — was duplicated across all three custom product templates, now reconciled (SEO-023, Fixed)

Three files each had their own hand-rolled `@type: "Product"` JSON-LD block, entirely independent of
the native one above, meaning every product page emitted **two** Product entities:

| File | Template | Richness vs. native filter | Resolution |
|---|---|---|---|
| `sections/main-product-premium-v2.liquid` | `templates/product.json` (default — **all 602 active products**) | No added value — same fields the native filter already provides | Removed outright |
| `sections/main-product-premium.liquid` | `templates/product.premium.json` | Same, no added value | Removed outright |
| `sections/main-product.liquid` | `templates/product.hampers-template.json` (confirmed live) | **Richer**: `sku`, `category`, `seller`, `shippingDetails` (`OfferShippingDetails`/`MonetaryAmount`/`DefinedRegion`/`ShippingDeliveryTime` — real handling/transit days), `hasMerchantReturnPolicy` (`MerchantReturnPolicy`, `returnPolicyCategory`, `merchantReturnDays`) | **Kept** — native filter now skipped for this template instead (see above) |

`sections/tbk-product.liquid` (`templates/product.tbk.json`) has no standalone Product block of its
own — confirmed to rely on the native filter alone, no duplication there.

## `snippets/tbk-schema-website.liquid` — WebSite + Organization

Fully dynamic (`settings.logo`, real phone/address), `SearchAction` correctly wired to
`/search?q={search_term_string}`. **SEO-020 (open, Low, Verified)**: `sameAs` lists only Instagram;
`bk-local-business.liquid`'s `sameAs` lists Instagram *and* Facebook. Same business entity, two
schema sources, inconsistent social-profile list — not fabricated, just needs reconciling to
whichever list is actually current.

## `snippets/tbk-schema-breadcrumb.liquid` — BreadcrumbList

Fully dynamic across product/collection/article/page page types, correct `@type`/`position`
structure. **Verified correct**, no issues found.

## `snippets/tbk-schema-collection.liquid` — CollectionPage

Fully dynamic (`collection.products_count`, real product loop up to 20 items). **Verified
correct**, no issues found.

## `snippets/tbk-schema-article.liquid` — Article

Real `published_at` date, real author/publisher Organization reference, correctly falls back to the
shop logo when an article has no image. **SEO-021 (open, Low, Requires Manual Verification)**:
`dateModified` is hardcoded to equal `datePublished` — if Shopify's Liquid `article` object exposes
a real last-modified property, this under-reports freshness for edited articles. Needs checking
against Shopify's documented Liquid objects before concluding this is fixable; low priority either
way (affects freshness signals only, not indexability).

## `layout/theme.liquid` — global tags + FAQPage (SEO-024, Fixed)

`<link rel="canonical" href="{{ canonical_url }}">` present and dynamic. Conditional
`<meta name="description">`. No `noindex`/`robots` meta tag logic found anywhere in the theme —
acceptable for a storefront (nothing should be blanket-noindexed), though there's no per-page-type
override either (e.g. for internal search-result pages, which can become thin/duplicate content at
scale — not flagged as an issue this pass since no evidence of it causing a real problem was found,
just noted as a technical-SEO consideration).

**SEO-024 (Fixed, `4d23a2e`)**: this file also contained a 9-question `FAQPage` block with no
`request.page_type`/`template.suffix` gate at all — it rendered identically on every page in the
theme (home, every product, every collection, every blog post), regardless of whether that page's
visible content had anything to do with FAQs. This violates Google's own structured-data guideline
that markup should reflect content genuinely present on the page, and duplicated the dedicated FAQ
pages' own schema. Now excluded when `template.suffix` is `faq-01` or `faq-02` (the two pages that
already carry their own `FAQPage` entity via their accordion sections' Microdata). The 9 Q&A pairs
themselves are unchanged — they read as genuine business facts (delivery, WhatsApp ordering, pickup)
consistent with facts verified elsewhere in the codebase, not fabricated, so the fix was a placement
correction, not a content deletion.

A pre-existing, unrelated drift was found and reconciled in this same file before the fix: two
`render` calls (`tbk-tokens`, `tbk-components`) present in git (commit `011f9be`) were absent from
the live theme, apparently abandoned/incomplete work. Local was synced to the live truth for this
file before applying the FAQPage gate.

## Related

[../audit/VERIFIED_ISSUES.md](../audit/VERIFIED_ISSUES.md), [../seo/GEO_AUDIT.md](../seo/GEO_AUDIT.md)
(schema is the backbone of AI-search readiness), [SCHEMA_CHANGELOG.md](SCHEMA_CHANGELOG.md),
[SCHEMA_SCORECARD.md](SCHEMA_SCORECARD.md), [SCHEMA_VALIDATION.md](SCHEMA_VALIDATION.md),
[ENTITY_GRAPH.md](ENTITY_GRAPH.md), [RICH_RESULTS_REPORT.md](RICH_RESULTS_REPORT.md).
