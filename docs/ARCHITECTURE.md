# Architecture

Three layers live in one repository.

## 1. Live Shopify theme

Ecomus v1.6.1 (Halo/The4 "hdt-" family), Online Store 2.0 — JSON templates + section groups. Deployed as theme `#151307485353` on `ae86ba-2a.myshopify.com`. Full technical detail in [SHOPIFY.md](SHOPIFY.md) and the canonical root `SHOPIFY_ARCHITECTURE.md`.

- **Entry:** `layout/theme.liquid`
- **Templates:** 33 (`templates/`; count corrected 2026-07-31, Phase 7.0 reconciliation — was
  recorded as 40, stale since at least R3.5's removal of `templates/product.tbk.json`, per
  `docs/TEMPLATE_CENSUS.md`); `product.json` → `sections/main-product-premium-v2.liquid`
  (**protected module**)
- **Sections:** ~134 — base Ecomus + `tbk-*` custom + `site-footer`
- **Snippets:** ~146 — base + `bk-*`/`tbk-*` custom (structured data, buy-box, datetime, design tokens, trust)
- **Assets:** large base CSS/JS + 20+ ShineTrust `shine-trust-v4-*` scripts

## 2. Enterprise blueprint (documentation, not code)

~30 root `*.md` files: discovery/audit, design system, brand voice, information architecture, SEO/GEO plan, schema master, homepage spec, QA checklist. Entry point `00_START_HERE.md`; linked index `TABLE_OF_CONTENTS.md`; status in `VERSION.md` / `PROJECT_ROADMAP.md`.

## 3. SEO / catalog operations (`seo-ops/`)

Python tools that read and write the store over the Admin GraphQL API:

| Script | Purpose |
|---|---|
| `fix_seo_snippets.py` | Rewrite product SEO title + meta description (with test) |
| `repoint_redirects.py` | Repoint `/collections/all` catch-all redirects to relevant collections |
| `fix_description_occasion.py` | Correct mis-assigned "occasion" in product descriptions (with test) |

Reusable title-hygiene helpers live in `seo-ops/title_utils.py` (`clean_base`, `is_broken`, `MOJI`). The one-off generators and run artifacts from the 2026-07 title runs (`batches/`, `v2/`, `rollback.csv`, `mutations.jsonl`, `PROGRESS.txt`, etc.) were removed in the cleanup; their rationale is preserved in [DECISIONS.md](DECISIONS.md). Generated outputs (review CSVs, JSONL, logs) are git-ignored.

## Data & integrations

- **Admin GraphQL API** — products, collections, pages, redirects, metafields (SEO tags via `global.title_tag` / `global.description_tag`).
- **Google Merchant Center / Google & YouTube channel** — shipping information set to **Manual**. Background in `FINAL_NAP_AND_MC_ARCHITECTURE.md`.
- **Structured data** — LocalBusiness (`Bakery`), Organization, WebSite, BreadcrumbList, FAQPage sitewide; Product/ProductGroup on PDPs. See `SCHEMA_MASTER.md`.
- **Apps:** HulkApps (product options + cart), ShineTrust v4, BSS (options/search), Uploadcare (PDP reference-image upload — **protected dependency**), Rewind (legacy, unused).

## Protected modules

Product page (design/UX/flow/CSS/JS), logo, brand colors. Only invisible edits — schema, analytics, accessibility, performance — are allowed near the PDP.
