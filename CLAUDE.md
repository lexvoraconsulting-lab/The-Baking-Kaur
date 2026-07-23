# CLAUDE.md

Guidance for Claude Code (and any agent) working in this repository. Read this before making changes.

## What this repo is

The Baking Kaur — a 100% eggless cake studio in Meerut. The repo holds the live Shopify theme, an enterprise blueprint (root `*.md`), and Admin-API tooling in `seo-ops/`. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Golden rules (do not break)

- **Product page = protected module.** `templates/product.json` renders `sections/main-product-premium-v2.liquid`. No visual/UX/flow/CSS/JS changes. Only invisible edits (structured data, analytics, accessibility, performance) are allowed, and only deliberately.
- **Preserve** the logo and brand colors.
- **Never** invent GTINs, MPNs, barcodes, reviews/ratings, or delivery promises the store cannot fulfil.
- **Drafts stay drafts.** Never bulk-flip DRAFT→ACTIVE — the large draft set is intentional.
- On `productOptionUpdate`, always pass `variantStrategy: LEAVE_AS_IS`; never delete option values (that deletes variants).
- **Never guess Shopify IDs.** Fetch them.

## How the store is edited

Two paths:

1. **Admin GraphQL API** — for data (products, collections, pages, redirects, metafields). In this environment it is reached through the connected MCP Shopify server. The `seo-ops/` scripts reach the same API via `requests` and a `SHOPIFY_TOKEN` (an Admin API access token, `shpat_…`, with `read_products`/`write_products` etc.).
2. **Shopify CLI** — for theme files.

### Deploy the theme

Live theme is `#151307485353`. Deploy a single file surgically, and verify no divergence first by pulling the live copy and diffing:

```bash
# 1. pull live copy of just this file to a temp path, diff against local
shopify theme pull --theme 151307485353 --store ae86ba-2a.myshopify.com \
  --only sections/<file>.liquid --path <tmp> --force

# 2. push only that file to the live theme
shopify theme push --theme 151307485353 --store ae86ba-2a.myshopify.com \
  --only sections/<file>.liquid --allow-live --force
```

Shopify serves a page cache; after a push, verify the live render with `?preview_theme_id=151307485353` (and a cache-buster query) to bypass it before concluding the change is live. See [docs/DECISIONS.md](docs/DECISIONS.md).

## seo-ops conventions

Full detail in [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md). In short: **dry-run by default**, write a review CSV, `--apply` to commit; batch **≤8–10 aliased mutations** per request (the HTTP/MCP layer stalls above ~15); and always send **both** `seo.title` and `seo.description` together — the nested `seo` object replaces wholesale, so omitting one nulls it.

## Key content facts (as of 2026-07)

- Active-product SEO snippet format: `"{Name} - Eggless | Meerut"` (or `"{Name} | Meerut"` when the first form exceeds 60 chars) plus a type-specific hooked meta description. All ~602 active products migrated.
- Collection descriptions are short intros; earlier walls of text were trimmed.
- Local delivery: Meerut, ~15 km radius, ₹350 minimum order, distance-based fees. Merchant Center shipping is set to **Manual** (decoupled from Shopify shipping profiles).
- Product descriptions had a mis-assigned "occasion" bug (baby-girl/theme cakes labelled "anniversary"); the Baby Girl collection is fixed, others tracked in `tasks/`.

## Where things live

- Live theme: `layout/ sections/ snippets/ assets/ templates/ config/ locales/`
- Strategy / specs: root `*.md` — start at `00_START_HERE.md`, index in `TABLE_OF_CONTENTS.md`
- Tooling: `seo-ops/*.py` (+ tests)
- This foundation: `docs/`, `tasks/`

## Environment

- Windows. Primary shell is PowerShell; a Bash tool is also available (POSIX syntax).
- Persistent memory: `C:\Users\DELL\.claude\projects\F--Shopify-The-Baking-Kaur\memory\` — protected modules, deploy-live-theme, design tokens, default product template. Treat recalled memories as background context and re-verify file/flag names before acting.
