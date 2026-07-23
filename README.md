# The Baking Kaur — Shopify

Repository for **The Baking Kaur**, a 100% eggless luxury cake studio in Meerut, Uttar Pradesh. It contains three layers:

1. **The live Shopify theme** — `layout/`, `sections/`, `snippets/`, `assets/`, `templates/`, `config/`, `locales/`. Deploys go to theme *Baking Kaur — Draft* (`#151307485353`).
2. **The enterprise blueprint** — ~30 planning & standards documents at the repo root (`00_START_HERE.md`, `SHOPIFY_ARCHITECTURE.md`, `DESIGN_SYSTEM.md`, `SEO_GEO_MASTER_PLAN.md`, …). Strategy and specs, not code. Index: `TABLE_OF_CONTENTS.md`.
3. **SEO / catalog operations** — `seo-ops/`, Python tooling that reads and writes the store over the Shopify Admin GraphQL API.

New here? Read **[CLAUDE.md](CLAUDE.md)** for how to work in this repo, then **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

## Store facts

| | |
|---|---|
| Storefront | https://thebakingkaur.com |
| Admin store | `ae86ba-2a.myshopify.com` |
| Live theme | `Baking Kaur — Draft` · `#151307485353` |
| Theme base | Ecomus v1.6.1 (Halo/The4 "hdt-" family), Online Store 2.0 |
| Catalogue | ~1,235 products (≈602 active, rest draft/archived) · eggless only |
| Market | Meerut, UP — local delivery within ~15 km |

## Layout

```
├── layout/ sections/ snippets/ assets/ templates/ config/ locales/   # live theme
├── docs/                # this documentation foundation
│   ├── ARCHITECTURE.md  SHOPIFY.md  CODING_STANDARDS.md  DECISIONS.md
├── tasks/               # work tracking (see tasks/README.md)
├── seo-ops/             # Admin-API Python tooling + tests
├── reports/  logs/  scripts/    # TODO: present but currently empty / ad-hoc
└── *.md                 # enterprise blueprint — start at 00_START_HERE.md
```

## Hard rules

See [CLAUDE.md](CLAUDE.md) and the `memory/` store for the full set. In brief:

- **The product page is a protected module** — no visual/UX/flow/CSS/JS change. Only invisible edits (schema, analytics, a11y, performance) are permitted, and only with care. `templates/product.json` renders `sections/main-product-premium-v2.liquid`.
- **Preserve** the logo and brand colors.
- **Never** invent GTINs / MPNs / barcodes / reviews, or advertise delivery the store cannot fulfil.
- Drafts stay drafts — do not bulk-flip DRAFT→ACTIVE.

## The blueprint documents

The ~30 root `*.md` files are a planning & standards library (design system, brand voice, information architecture, SEO/GEO plan, schema master, homepage spec, QA). Rather than duplicate the list here, start at `00_START_HERE.md` and use `TABLE_OF_CONTENTS.md` as the linked index. Status and phases live in `VERSION.md` and `PROJECT_ROADMAP.md`.

> Note: the older README described this repo as "documentation only — no theme code." That is no longer true — the live theme and `seo-ops/` tooling now live here alongside the docs.
