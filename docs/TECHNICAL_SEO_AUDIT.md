# Technical SEO Audit (Phase 7.1)

Every requested area, audited with real evidence. Format: Evidence · Finding · Verifiable now? ·
Action. No estimated metrics; where the password gate blocks live verification, stated plainly.

## URL Architecture

- **Structure**: standard Shopify (`/products/<handle>`, `/collections/<handle>`, `/pages/<handle>`,
  `/blogs/<handle>/<article>`) — no custom URL rewriting found in theme code.
- **Handles**: many legacy numeric/short handles (`/products/12`, `/products/b166`) still exist
  alongside descriptive ones — a known, previously-documented, deliberately-deferred item
  (`CLAUDE.md`'s "handle optimization" section — real SEO upside, real URL-stability risk, requires
  the full 8-step checklist there). Not touched here, consistent with that standing decision.

## Canonical URLs — see `docs/CANONICAL_REPORT.md` for full detail

Site-wide `<link rel="canonical" href="{{ canonical_url }}">` (`layout/theme.liquid:28`), dynamic,
present on every page type. No hardcoded/duplicate canonical tags found. No canonical conflicts
found in theme code (Shopify's own `canonical_url` object is the single source).

## Robots — see `docs/ROBOTS_REPORT.md`

No `robots.txt.liquid` override in the theme — Shopify's default `robots.txt` applies. Actual
served content **not verifiable** (password gate).

## XML/HTML Sitemap — see `docs/SITEMAP_REPORT.md`

No sitemap override in the theme — Shopify's native auto-generated `/sitemap.xml` applies. No
custom HTML sitemap page found. Actual served content **not verifiable** (password gate).

## Pagination

`{% paginate %}` correctly used across all 11 listing-type sections (confirmed in Phase 6,
`docs/PERFORMANCE_AUDIT.md` F-3) — not re-audited here, per "never repeat completed work."
`rel="next"/"prev"` pagination link tags: not found in `layout/theme.liquid` head — Shopify has
deprecated the requirement for these (Google stopped using them in 2019), so their absence is not
a defect.

## Breadcrumbs

`snippets/tbk-schema-breadcrumb.liquid` provides `BreadcrumbList` JSON-LD, rendered site-wide from
`layout/theme.liquid` (confirmed in Phase 6, `docs/AEO_READINESS.md`). A **visual** breadcrumb
component's presence/absence was not independently re-confirmed in this pass — flagged as an open
verification item, not assumed present or absent.

## Indexability / Noindex / Nofollow — see `docs/INDEXABILITY_REPORT.md`

No `noindex`/`nofollow` meta tags found anywhere in `layout/theme.liquid` (grep, zero matches) — no
accidental blanket de-indexing. Per-template or per-page noindex logic (e.g., for the intentionally
DRAFT products or thin utility pages) not found in theme code either — if any exists, it would be
set at the page/product level in Shopify Admin, not verifiable from theme code, and not checked via
Admin API in this pass (out of scope; would require a 1,235-product-level metafield sweep with no
specific evidence prompting one).

## Redirect chains, broken links, 404s — see `docs/CRAWL_REPORT.md`

**Found and fixed**: 2 confirmed redirect-chain patterns (25 total redirects affected) — see
`docs/SEO_CHANGELOG.md` for the full before/after record. Live 404/soft-404 detection and
redirect HTTP-status verification are **not verifiable** (password gate) — the fix was verified via
Admin API re-query (target field updated correctly), not a live HTTP crawl.

## Canonical conflicts / duplicate URLs / parameter URLs

Redirect audit (825 entries reviewed) found many `?variant=...`/`?country=...&currency=...`
parameter-URL redirect *sources* — these are expected (old cart/variant links from since-removed
products, correctly redirected to a live collection) — not a defect. No parameter-URL *canonical
conflicts* found in theme code (the canonical tag ignores query parameters by using
`canonical_url`, Shopify's own de-parameterized object).

## Collection URLs / Product URLs / Blog URLs / Search URLs

- **Collections**: 36 total (Admin API, verified this pass).
- **Products**: 1,235 total (R3 census, `docs/TEMPLATE_CENSUS.md` — not re-counted, per "never
  repeat completed work").
- **Blog/Search URLs**: use Shopify's native `/blogs/`/`/search` routes; `main-search.liquid`
  correctly paginated (confirmed above). Not otherwise re-audited this pass.

## Internal links / Anchor text / Orphan pages / Orphan collections — see `docs/INTERNAL_LINKING_AUDIT.md`

Real cross-linking exists from Sprint 2's hub-page work (prior phase, not repeated here). A full
internal-linking graph and orphan-page/collection census was **not** completed in this pass — it
was already flagged as Phase 7 task M-1 in `docs/PHASE7_TASK_BREAKDOWN.md`, scoped as its own
dedicated audit given its size (36 collections × an unknown number of pages × 1,235 products).
Not duplicating that scoping decision here.

## Thin pages / Duplicate titles / Duplicate descriptions

Already substantially addressed by prior project work (the ~602-active-product SEO-title/
description migration referenced in `CLAUDE.md`'s "Key content facts" section — format
`"{Name} - Eggless | Meerut"`). **Not re-verified in this pass** — re-auditing 602+ live product
titles/descriptions for continued compliance would require a fresh full Admin API sweep with no
specific evidence prompting one; flagged as a candidate for Phase 7.2 rather than assumed either
compliant or non-compliant.

## Heading hierarchy

- **Product page** (`main-product-premium-v2.liquid`): exactly 1 `<h1>` — confirmed clean.
- **Collection page** (`heading-collection.liquid`): exactly 1 `<h1>` — confirmed clean.
- **Homepage** (`templates/index.json`): contains a hardcoded `<h1>` inside a raw custom-liquid
  block. This **directly corroborates an already-documented, unresolved finding** — root
  `CHANGELOG.md`'s own Phase A live-promotion verification record (read in full during Phase 7.0)
  states plainly: *"homepage H1 count = 2"*, logged as pre-existing, not introduced by Phase A.
  This pass confirms that condition still exists in the current homepage template. **Not fixed
  here** — it sits inside a custom-liquid content block belonging to the separate "Enterprise
  Transformation" homepage-build workstream (`CLAUDE.md`, updated in Phase 7.0), and per this
  phase's own rule ("never modify business content"), a content-bearing custom-liquid block is
  not a code-architecture fix to make unilaterally. Flagged for that workstream's owner.

## Image indexing / ALT consistency

The live, default product-page image renderer (`snippets/media.liquid`, used by 1,228/1,235
products) uses Shopify's `image_tag` filter **without an explicit `alt:` override** — this is the
correct technical pattern: Shopify's `image_tag` filter automatically emits `alt="{{ image.alt }}"`
from the image's own stored metadata when no override is given, rather than a hardcoded or generic
string. No template-level ALT defect found. **Actual ALT-text content quality/coverage across the
1,235-product catalogue** (i.e., whether merchants filled in real, descriptive alt text per image)
is a content/data-management question requiring an image-level Admin API audit — out of this
architecture-focused pass's scope, not assumed good or bad.

## OpenGraph / Twitter Cards

`snippets/social-meta-tags.liquid` (confirmed live, rendered from `layout/theme.liquid`,
`layout/password.liquid`, and `templates/gift_card.liquid` — R4 finding, `docs/ORPHAN_SNIPPET_AUDIT.md`)
emits `og:site_name`, `og:url`, `og:title`, `og:type`, `og:description`, conditional `og:image`
(+ width/height + secure_url), conditional `og:price:amount`/`og:price:currency` on product pages,
`twitter:card` (`summary_large_image`), `twitter:title`, `twitter:description`, conditional
`twitter:site`. Confirmed present and dynamic — no hardcoded/generic content found.

## Meta Robots / Viewport / Language / Hreflang readiness

- **Viewport**: `<meta name="viewport" content="width=device-width,initial-scale=1">` — correct.
- **Language**: `<html lang="{{ request.locale.iso_code }}" dir="{{ dir }}">` — dynamic, correct,
  RTL-aware.
- **Hreflang**: no `hreflang` tags found — appropriate for a single-locale, single-market storefront
  (per `business/BUSINESS_MASTER.md`, no evidence of a multi-market/multi-language setup). Not a
  defect; would only become relevant if a second market/locale is added.

## Crawl budget / Robots directives / Render blocking

Render-blocking CSS/font findings already fully covered in Phase 6 (`docs/PERFORMANCE_AUDIT.md`
F-5/F-7, `docs/PERFORMANCE_FINAL_REPORT.md`) — not repeated here. No `X-Robots-Tag`-equivalent
Liquid logic found in theme code (that header is typically set server-side by Shopify itself for
password-protected stores, not by theme code).

## Structured navigation / Semantic HTML

`<main id="MainContent" role="main">` landmark present (confirmed Phase 6). Header/footer/nav
landmark elements live in `sections/tbk-header.liquid`/`site-footer.liquid` (not re-verified
line-by-line this pass — no specific evidence prompted a re-check).

## Accessibility (performance- and indexability-relevant aspects)

`prefers-reduced-motion` respected (confirmed Phase 6, `docs/PERFORMANCE_AUDIT.md` F-17) — not
repeated. Full accessibility audit (contrast, focus order, ARIA) is out of this technical-SEO
phase's scope.

## Mobile readiness

Viewport tag correct; responsive images (`srcset`/`sizes`) confirmed extensively in Phase 6
(`docs/PERFORMANCE_AUDIT.md` F-14) — not repeated.

## Related

[TECHNICAL_SEO_MASTER.md](TECHNICAL_SEO_MASTER.md), [CRAWL_REPORT.md](CRAWL_REPORT.md),
[CANONICAL_REPORT.md](CANONICAL_REPORT.md), [ROBOTS_REPORT.md](ROBOTS_REPORT.md),
[SITEMAP_REPORT.md](SITEMAP_REPORT.md), [URL_ARCHITECTURE.md](URL_ARCHITECTURE.md),
[INDEXABILITY_REPORT.md](INDEXABILITY_REPORT.md), [INTERNAL_LINKING_AUDIT.md](INTERNAL_LINKING_AUDIT.md),
[SEO_CHANGELOG.md](SEO_CHANGELOG.md), [TECHNICAL_SEO_SCORECARD.md](TECHNICAL_SEO_SCORECARD.md).
