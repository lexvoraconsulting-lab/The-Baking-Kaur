# Robots.txt Report (Phase 7.1)

## Finding: no theme override — Shopify's platform default applies

`find . -iname "robots.txt.liquid"` returns zero results anywhere in the theme. Shopify supports an
optional `templates/robots.txt.liquid` for custom robots.txt logic (e.g., custom disallow rules,
custom sitemap references, per-crawler rules) — this theme does not use that override, so Shopify's
own platform-default `robots.txt` is what's actually served.

## What Shopify's default robots.txt does (documented platform behavior, not verified live here)

Shopify's default robots.txt disallows admin/cart/checkout/account paths and search-result pages by
default, and includes a reference to the store's sitemap. This is standard, sound behavior for most
stores and requires no theme-level customization unless a specific crawl-control need exists (e.g.,
blocking a specific AI crawler by name, which none of this project's business decisions have called
for).

## Not verifiable this pass (password gate)

The **actual served content** of `/robots.txt` right now cannot be fetched or confirmed — the
password gate returns the password page for any unauthenticated request, including to
`/robots.txt` itself. This means even Shopify's own default robots.txt is not currently reachable
by any real crawler.

## AI crawler considerations (architecture only, per this phase's explicit "do not optimize content
yet" instruction)

If the business wants to explicitly allow or disallow specific AI crawlers (GPTBot, ClaudeBot,
Google-Extended, PerplexityBot, etc.) once unlocked, that requires a `templates/robots.txt.liquid`
override with explicit `User-agent`/`Allow`/`Disallow` blocks per crawler — not present today, and
not added in this pass (a business/product decision on which crawlers to allow, not a deterministic
technical fix — flagged in `docs/AI_SEARCH_READINESS.md`'s existing recommendation, not repeated
as new work here).

## Recommendation

Once the password gate is resolved: (1) fetch and confirm the actual served robots.txt content;
(2) decide, with the business, whether any AI-crawler-specific rules are wanted; (3) only then add
a `robots.txt.liquid` override if needed — don't add one speculatively.

## Related

[TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md), [SITEMAP_REPORT.md](SITEMAP_REPORT.md),
[AI_SEARCH_READINESS.md](AI_SEARCH_READINESS.md).
