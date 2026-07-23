# Coding Standards

Derived from the existing `seo-ops/` tooling and the store's constraints. Follow the patterns already in the code.

## seo-ops Python scripts

The three maintained scripts (`fix_seo_snippets.py`, `repoint_redirects.py`, `fix_description_occasion.py`) share one shape — match it:

- **Dry-run by default.** Running the script scans and writes a **review CSV**; nothing is written to Shopify until `--apply` is passed.
- **Config via environment:** `SHOPIFY_STORE` and `SHOPIFY_TOKEN` (Admin API access token). The script exits early if either is unset.
- **Batch mutations small.** Send **≤8** aliased mutations per GraphQL request (`BATCH = 8`); the HTTP/MCP layer becomes unreliable above ~15.
- **Retry on throttling.** 429 / GraphQL `errors` → exponential backoff, capped retries.
- **Escape GraphQL string literals** with the `esc()` helper (`\\` and `"`); or use the Liquid/JSON-safe form where applicable.
- **Report `userErrors`.** Count and print them; never assume success.
- **Leave a runnable check.** Non-trivial logic ships with a small offline `test_*.py` of `assert`-style cases (see `test_fix_seo_snippets.py`, `test_fix_description_occasion.py`). No frameworks.
- Standard library + `requests` only. No new dependencies for what a few lines can do.

## Shopify Admin API rules

- **`ProductInput.seo` replaces wholesale.** Always send **both** `title` and `description`; sending one nulls the other.
- **Pages have no `seo` field.** Set SEO via metafields: namespace `global`, keys `title_tag` / `description_tag`, type `single_line_text_field`.
- **Collections:** update visible body via `collectionUpdate(input: {id, descriptionHtml})`; SEO tags are the separate `seo` field / `global.*` metafields — don't conflate them.
- **`productOptionUpdate`:** always `variantStrategy: LEAVE_AS_IS`; never delete option values.
- **Never guess IDs** — query them. Never invent GTIN/MPN/barcode/review data.

## Liquid / theme

- The product template (`main-product-premium-v2.liquid`) is **protected** — see [CLAUDE.md](../CLAUDE.md).
- **Build JSON-LD with the `| json` filter**, never `| escape`. `escape` handles HTML entities but not JSON control characters; unescaped newlines in a description silently break the whole schema block. (This was a live bug — see `docs/DECISIONS.md`.)
- Deploy single files and verify against the page cache; don't push the whole theme when one file changed.

## Content / copy

- Keep collection and page intros short and scannable; avoid keyword-stuffed walls (they read as spam and were removed).
- SEO title ≤ 60 chars, meta description ≤ 155 chars.
- Follow `BRAND_VOICE.md` and `COPY_GUIDELINES.md` for tone; never fabricate claims (delivery windows, prices, ratings).

## Git

- Work on a branch; the current working branch is `phase-a/production-safety`.
- Commit theme/data changes with a clear message; end co-authored commits with the required trailer.
- TODO: no CI, linter, or formatter config is present in the repo. Add one if scripts grow.
