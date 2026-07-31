# Indexability Report (Phase 7.1)

Noindex, nofollow, meta robots, and general indexability. Evidence: repo-wide grep of theme code;
Admin API not queried for per-product/page indexability flags (see scope note below).

## Findings

| Check | Result | Evidence |
|---|---|---|
| Blanket `noindex` in layout | **None found** | `grep -i "noindex" layout/theme.liquid` — zero matches |
| Blanket `nofollow` in layout | **None found** | Same grep pass, zero matches |
| Per-template meta-robots overrides | **None found in theme code** | No conditional `meta name="robots"` logic anywhere in `layout/theme.liquid` or checked section files |
| `X-Robots-Tag` header logic | **N/A** | Not set by theme code — this is a server-response header, controlled by Shopify's platform layer, not Liquid |
| Password-gate interaction with indexability | **Total block, confirmed** | Every page currently returns the password-page content to any unauthenticated request/crawler — this is Shopify's platform-level password-protection feature, not a theme `noindex`, but has the same practical effect: nothing is indexable right now |

## What "indexability" means right now, concretely

Because of the password gate, **the entire storefront is currently non-indexable by any real
search engine or AI crawler**, regardless of what any individual page's meta tags say. This is the
same root cause already documented in `docs/AI_SEARCH_READINESS.md` (Phase 6) and reiterated in
`docs/PHASE7_BLOCKERS.md` (Phase 6.5) — not a new finding, restated here because "indexability" is
this document's specific named scope.

## Not verifiable this pass

- Whether any individual DRAFT product or thin utility page has been explicitly marked `noindex`
  at the Shopify Admin level (a per-product/page setting, not a theme-code setting) — would require
  a metafield-level Admin API sweep across all 1,235 products + all pages, with no specific evidence
  prompting one. Not performed.
- Actual served meta-robots content per page type — requires a live page render, blocked by the
  password gate.

## Recommendation

Once the password gate is resolved (`docs/PHASE7_BLOCKERS.md` C-1), re-verify indexability via
Search Console's URL Inspection tool on a representative sample of page types, rather than
continuing to infer from theme code alone.

## Related

[TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md), [ROBOTS_REPORT.md](ROBOTS_REPORT.md),
[AI_SEARCH_READINESS.md](AI_SEARCH_READINESS.md).
