# URL Architecture (Phase 7.1)

## Current structure (standard Shopify, no custom routing)

| Type | Pattern | Count | Notes |
|---|---|---|---|
| Products | `/products/<handle>` | 1,235 | Per R3 census (`docs/TEMPLATE_CENSUS.md`) — 602 active, 588 draft, 45 archived |
| Collections | `/collections/<handle>` | 36 | Verified this pass, Admin API |
| Pages | `/pages/<handle>` | not recounted this pass | Many legacy page handles found redirected away (`docs/CRAWL_REPORT.md`) |
| Blog articles | `/blogs/<handle>/<article-handle>` | not audited this pass | Native Shopify routing, no custom logic found |
| Search | `/search?q=...` | — | Native, paginated (`main-search.liquid`) |

## Handle quality — real, deliberately deferred issue (not new, not re-litigated)

A meaningful fraction of product handles are non-descriptive legacy identifiers: numeric
(`/products/12`), short codes (`/products/b166`, `/products/ch297`, `/products/h37`,
`/products/hamper28`). `CLAUDE.md`'s own standing roadmap section addresses this directly:
**deliberately deferred**, "real SEO upside, real risk: it changes live URLs and can silently kill
printed QR codes," gated on a full 8-step checklist (mapping → 301s → internal links → QR audit →
indexing → sitemap → canonicals → monitoring). This audit does not reopen that decision or
recommend acting on it now — restated here only because URL architecture is this document's named
scope, not as a new finding.

## Parameter URLs

Confirmed via the redirect audit (`docs/CRAWL_REPORT.md`): many old `?variant=...`/
`?country=...&currency=...` URLs exist as redirect *sources* (not live, crawlable URLs) — these are
artifacts of removed products' old cart/share links, correctly redirected, not a live
parameter-URL-duplication risk today.

## Redirect architecture — see `docs/CRAWL_REPORT.md` for full detail

825 redirects total; 2 chain patterns found and fixed this phase (25 redirects collapsed from
2-hop to 1-hop). One minor inconsistency noted, not fixed (low priority, cosmetic): a handful of
redirects use absolute target URLs (`https://thebakingkaur.com/collections/all`) while the
overwhelming majority use relative paths (`/collections/...`) — both work correctly, but the
inconsistency is worth normalizing to relative paths in a future pass for consistency, not urgent.

## Related

[TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md), [CRAWL_REPORT.md](CRAWL_REPORT.md),
[CANONICAL_REPORT.md](CANONICAL_REPORT.md).
