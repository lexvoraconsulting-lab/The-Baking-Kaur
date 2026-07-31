# Sitemap Report (Phase 7.1)

## Finding: no theme override — Shopify's native auto-generated sitemap applies

No sitemap-related file found anywhere in the theme (`find . -iname "*sitemap*"`, excluding the
unrelated `ai/` subsystem, returns zero results). Shopify does not support a theme-level sitemap
override in the same way it does robots.txt — `/sitemap.xml` is generated natively by the
platform from the store's actual products, collections, pages, and blog articles, and is not
theme-controllable. This is expected, standard, and requires no theme-level action.

## What this means for the ~1,235-product / 36-collection catalogue

Shopify's native sitemap automatically includes all indexable (non-DRAFT, non-noindexed) products,
collections, and pages. Given 584 of 1,235 products are intentionally DRAFT
(`CLAUDE.md`'s roadmap section — "Drafts stay drafts until [a merchandising decision]"), the
sitemap should exclude those automatically, per Shopify's platform behavior. Not independently
re-verified in this pass (would require fetching the live sitemap, blocked by the password gate).

## Not verifiable this pass (password gate)

The actual served content of `/sitemap.xml` cannot be fetched or confirmed right now — same
constraint as `docs/ROBOTS_REPORT.md`.

## No HTML sitemap found

No customer-facing HTML sitemap page exists in the theme (checked `templates/page.*.json` for a
sitemap-named template — none found). Not flagged as a defect — an HTML sitemap is a supplementary,
optional pattern, not a requirement, and Shopify's native XML sitemap plus the site's own
navigation/collection structure already provide crawl paths.

## Recommendation

Once unlocked: fetch `/sitemap.xml` directly and confirm (1) it excludes DRAFT products as
expected, (2) it includes all 36 collections and all indexable pages, (3) submit/re-verify in
Search Console.

## Related

[TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md), [ROBOTS_REPORT.md](ROBOTS_REPORT.md),
[URL_ARCHITECTURE.md](URL_ARCHITECTURE.md).
