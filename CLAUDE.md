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

## Where this project is going

Read this section first when starting a session with no other instruction. It is the standing
plan — the ideas already agreed, in priority order. Sources: `PROJECT_ROADMAP.md` (detail),
`tasks/README.md` (open items). Keep this section current; it is the entry point.

### Live defects — fix before anything cosmetic

1. **Wrong `<title>` on the #1 bestseller.** `/products/motu-patlu-designer-birthday-cake-meerut`
   has an H1 of *Motu Patlu Designer Birthday Cake* but a `<title>` naming a different cake
   (*Celestial Charm*), plus mojibake. Google shows the wrong product name today. Fix is data-only,
   no theme deploy. Sweep the full catalogue (1,235 products, `title`/`seo.title`/`seo.description`/
   `descriptionHtml`) for both faults — the 8 known mojibake drafts and 1 live mismatch surfaced
   incidentally, assume more. **Repair encoding, never strip.** Never rename a handle here.
2. **Unverified "★ 4.9 Rated" in the site header** (`tbk_header_main`) — hardcoded, unlinked, and
   a different number from the hero's already-removed 4.8. Last unverified rating on the storefront.
   Remove it, or link it to the real Google Business Profile. Needs an explicit go-ahead.
3. **Occasion mismatch in descriptions** — ~100+ products still labelled "anniversary" wrongly.
   Tool is written: `seo-ops/fix_description_occasion.py` (dry-run → CSV → `--apply`).

### The build track (Phase A is done and waiting)

Phase A (schema dedup, footer restore) is **validated on preview, not promoted**. Promoting it is
the cheapest open win. Then B → C → E in that order: design tokens unlock the homepage build,
which unlocks navigation. D/F/G/H/I/J follow. Product page stays 🔒 throughout.

### Blocked on the client — don't build placeholders

- **Reviews.** 0 verified reviews exist; S5 Social Proof is built and renders nothing. It needs 3.
  Fabricated testimonials were removed and that route is permanently closed. Fastest path is
  transcribing existing Google Business Profile reviews with `source_url`; best long-term is
  Judge.me (verified-buyer, automatic, no gating).
- **Photography.** Homepage hero is a temporary product shot; S6 Craft Story ships text-only.
  Every catalogue image carries a Zomato/TWC watermark or a piped customer name; the theme's
  stock assets are Ecomus demo content. One studio shoot unblocks both. Swap cost is zero code.
- **FSSAI licence number.** The storefront says "FSSAI approved" with no number. Minutes of work,
  high trust-per-effort, and a checkable entity fact for GEO.
- **584 of 1,235 products are DRAFT** (Cake Hampers shows 8 of 119). Publish-vs-archive is a
  merchandising decision, not ours. Drafts stay drafts until then.
- **S8 Trust section** is gated on the FSSAI number or real reviews landing — it has no other
  genuinely new content.

### Deliberately deferred

- **Handle optimization** (`b158`, `hamper13`, `chNN` → keyword handles). Real SEO upside, real
  risk: it changes live URLs and can silently kill printed QR codes. Never urgent; current handles
  return 200. Starts only after the homepage ships and the duplicate drafts are archived, and only
  with the full 8-step checklist (mapping → 301s → internal links → QR audit → indexing → sitemap →
  canonicals → monitoring).
- **Variant option typos** (`fruit-cocoktail`, `chocolate-moouse`) — touching options risks deleting
  variants. Needs a metaobject fix first.

### Standing principles for this project

- Verifiability beats persuasion. No rating, count, certification, or delivery promise ships
  without a source. This has already caused three removals; assume it will cause more.
- Data fixes before theme work — they're reversible, need no deploy, and reach Google faster.
- One decision, one document. The Jul-19 NAP cluster is five files for one decision; don't repeat it.
  See `MD_FILE_INVENTORY.md`.

## Where things live

- Live theme: `layout/ sections/ snippets/ assets/ templates/ config/ locales/`
- Strategy / specs: root `*.md` — start at `00_START_HERE.md`, index in `TABLE_OF_CONTENTS.md`
- Tooling: `seo-ops/*.py` (+ tests)
- This foundation: `docs/`, `tasks/`

## Environment

- Windows. Primary shell is PowerShell; a Bash tool is also available (POSIX syntax).
- Persistent memory: `C:\Users\DELL\.claude\projects\F--Shopify-The-Baking-Kaur\memory\` — protected modules, deploy-live-theme, design tokens, default product template. Treat recalled memories as background context and re-verify file/flag names before acting.
