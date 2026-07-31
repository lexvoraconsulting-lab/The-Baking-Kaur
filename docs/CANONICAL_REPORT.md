# Canonical URL Report (Phase 7.1)

## Finding: correctly implemented, site-wide, dynamic

```liquid
<link rel="canonical" href="{{ canonical_url }}">
```

`layout/theme.liquid:28`. `canonical_url` is Shopify's own native Liquid object — it already
correctly handles pagination (canonicalizing paginated collection/blog pages to page 1, per
Shopify's built-in behavior), variant/parameter URLs (stripping `?variant=`/`?country=`/etc., per
the same built-in behavior), and per-page-type routing (product/collection/page/article/etc. each
get their own correct canonical). No theme-level override, duplication, or conflicting canonical
logic found anywhere in the codebase.

## Canonical conflicts checked

- **No second `<link rel="canonical">` tag found anywhere else in the theme** (grep across all
  `.liquid` files for `rel="canonical"` — exactly 1 occurrence, the one above).
- **No hardcoded absolute-URL canonical** that could drift from the real domain — uses the dynamic
  object, not a literal string.
- **Redirect targets reviewed for canonical consistency** (`docs/CRAWL_REPORT.md`): the fixed
  redirect chains now point directly at their final collection URL — consistent with, not
  conflicting with, that collection's own canonical tag.

## Not verifiable this pass

Whether Google/other engines *respect* the canonical as intended requires Search Console data
(external credential, per `docs/PHASE7_BLOCKERS.md` E-5) and a crawlable (unlocked) site.

## Related

[TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md), [URL_ARCHITECTURE.md](URL_ARCHITECTURE.md).
