# Technical SEO Audit

## Storefront accessibility — the dominant fact right now

**Verified**: `thebakingkaur.com` and its `ae86ba-2a.myshopify.com` alias both serve a Shopify
password "Coming Soon" page to every visitor, including Google — confirmed via direct fetch of the
homepage and of a known real product URL (the flagship bestseller). Confirmed **intentional**
(pre-launch/relaunch mode) by the business, 2026-07-29 (SEO-022, tracked for context, not a
defect).

**Why this matters for everything below**: while active, no live-crawl-based check (rendered HTML,
actual Google indexing behavior, Core Web Vitals) is meaningful — Google sees the same gate a human
visitor does. The checks below are code-level and Admin-API-level, which remain valid regardless of
the gate.

## robots.txt

**Verified clean.** Standard Shopify-generated file: public product/collection/page/blog/policy/
cart routes crawlable; admin, private cart/checkout routes, and account pages disallowed; AJAX and
filter/sort parameters that could create crawl traps are disallowed; Google's adsbot has separate,
correctly scoped permissions. No issues found.

## sitemap.xml

**SEO-019 (open, Requires Manual Verification)**: returns HTTP 404. Very likely a direct symptom of
the password gate (Shopify's password-page middleware intercepts most routes, sitemap included, in
many configurations) rather than a separate misconfiguration — but this audit could not fetch it
successfully in either state to confirm which. **Action**: re-check the moment the gate lifts,
before assuming this resolves itself.

## Canonical URLs

**Verified correct.** `layout/theme.liquid` line 28: `<link rel="canonical" href="{{ canonical_url }}">`
— uses Shopify's own `canonical_url` object, which correctly resolves per page type (product,
collection, paginated listing, etc.) without any custom override logic that could introduce a bug.

## Meta robots / noindex

**Verified**: no `noindex` or custom `meta name="robots"` logic exists anywhere in the theme. Not a
defect (a storefront generally shouldn't blanket-noindex anything), but also means there's no
per-page-type override for surfaces like internal search results that can become thin/duplicate
content at catalogue scale. Not flagged as an issue — no evidence found that this is currently
causing a real problem — just noted for awareness.

## Duplicate titles/descriptions, thin/orphan pages

**Requires Manual Verification** — needs either a live crawl (blocked by the password gate) or a
bulk Admin API export of every product/collection/page's `seo.title`/`seo.description` fields, which
this session's tool access didn't extend to beyond spot-checks. `CLAUDE.md` already documents that
~602 active products were migrated to a consistent SEO-title format
(`"{Name} - Eggless | Meerut"`), which this audit spot-confirmed still holds for the flagship
product — but a full duplicate-check across all 602 wasn't run this pass.

## URL structure, pagination, faceted navigation, breadcrumbs

Breadcrumb structured data is dynamic and correct (see
[../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md)). URL structure, pagination, and faceted
navigation behavior were not independently audited this pass beyond what robots.txt's own
disallow rules already imply (filter/sort params blocked from crawling, which is the standard
mitigation for faceted-navigation crawl-budget issues).

## Image optimization, lazy loading, compression, caching, security headers, HTTPS/SSL

**Requires Manual Verification / partially out of scope this pass** — these require either a live
page render (blocked by the gate) or infrastructure-level checks (response headers, CDN config) not
performed this session. HTTPS itself is Shopify-default and not in question.

## Related

[../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md), [ONPAGE_SEO.md](ONPAGE_SEO.md),
[../audit/MANUAL_VERIFICATION.md](../audit/MANUAL_VERIFICATION.md).
