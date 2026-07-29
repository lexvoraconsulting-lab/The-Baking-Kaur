# Schema Audit

Every `application/ld+json` block found in the theme, per file. See
[`../audit/issues.yml`](../audit/../issues.yml) for SEO-020 and SEO-021, the two issues this audit
surfaced.

## Files emitting structured data

`snippets/bk-local-business.liquid`, `snippets/structured-data.liquid`,
`snippets/tbk-schema-article.liquid`, `snippets/tbk-schema-breadcrumb.liquid`,
`snippets/tbk-schema-collection.liquid`, `snippets/tbk-schema-website.liquid`,
`sections/main-product-premium-v2.liquid` (via `structured-data.liquid`'s render),
`layout/theme.liquid`.

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

## `layout/theme.liquid` — global tags

`<link rel="canonical" href="{{ canonical_url }}">` present and dynamic. Conditional
`<meta name="description">`. No `noindex`/`robots` meta tag logic found anywhere in the theme —
acceptable for a storefront (nothing should be blanket-noindexed), though there's no per-page-type
override either (e.g. for internal search-result pages, which can become thin/duplicate content at
scale — not flagged as an issue this pass since no evidence of it causing a real problem was found,
just noted as a technical-SEO consideration).

## Related

[../audit/VERIFIED_ISSUES.md](../audit/VERIFIED_ISSUES.md), [../seo/GEO_AUDIT.md](../seo/GEO_AUDIT.md)
(schema is the backbone of AI-search readiness).
