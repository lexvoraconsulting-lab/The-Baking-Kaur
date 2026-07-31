# Technical SEO Master (Phase 7.1)

Hub document for Phase 7.1 (Enterprise Technical SEO Engine). Continues from Phase 7.0
(`docs/PHASE7_READY.md`, commit `c22d895`) — read that first for the reconciled documentation
state this phase builds on. Objective: a technically correct, machine-readable, standards-
compliant, AI-crawler-friendly foundation — not a ranking play, and not a content rewrite.

## Deliverables in this set

| Document | Covers |
|---|---|
| `docs/TECHNICAL_SEO_AUDIT.md` | Full audit findings across every requested area |
| `docs/CRAWL_REPORT.md` | Redirects, redirect chains, 404/broken-link status |
| `docs/INDEXABILITY_REPORT.md` | Noindex, nofollow, meta robots, indexability |
| `docs/CANONICAL_REPORT.md` | Canonical URL architecture |
| `docs/ROBOTS_REPORT.md` | robots.txt |
| `docs/SITEMAP_REPORT.md` | XML/HTML sitemap |
| `docs/URL_ARCHITECTURE.md` | URL structure across products/collections/pages/blog |
| `docs/INTERNAL_LINKING_AUDIT.md` | Internal linking, anchor text, orphan-page risk |
| `docs/SEO_CHANGELOG.md` | What was actually changed in this phase, with evidence |
| `docs/TECHNICAL_SEO_SCORECARD.md` | Scored summary |

## What this phase does NOT do

Per explicit instruction: no ranking optimization, no copy rewrites, no pricing/product/review
changes, no invented metadata, no content changes. One class of change was made — see
`docs/SEO_CHANGELOG.md` — and it is exclusively a technical redirect-architecture fix (collapsing
confirmed redirect chains), not a content or business-data change.

## The password-gate constraint (carried forward, not re-litigated)

As established in Phase 6 (`docs/CORE_WEB_VITALS.md`) and Phase 6.5/7.0, the storefront is
intentionally password-gated. This blocks live crawl-based verification for several categories in
this audit (actual served robots.txt/sitemap.xml content, live 404/soft-404 detection, live
duplicate-title/description detection across rendered pages, live redirect HTTP-status
verification). Where this applies, the relevant report says so explicitly rather than estimating.
What *is* independently verifiable — theme code, Shopify Admin API data (redirects, collection/
product counts) — was verified directly.

## Related

[PHASE7_READY.md](PHASE7_READY.md), [TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md),
[CRAWL_REPORT.md](CRAWL_REPORT.md), [SEO_CHANGELOG.md](SEO_CHANGELOG.md),
[TECHNICAL_SEO_SCORECARD.md](TECHNICAL_SEO_SCORECARD.md).
