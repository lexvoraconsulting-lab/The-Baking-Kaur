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

1. **Admin GraphQL API** — for data (products, collections, pages, redirects, metafields). In this environment it is normally reached through the connected MCP Shopify server. The `seo-ops/` scripts reach the same API via `requests` and a `SHOPIFY_TOKEN` (an Admin API access token, `shpat_…`, with `read_products`/`write_products` etc.). **If MCP is down and no token is set**, `shopify store auth --store ae86ba-2a.myshopify.com --scopes read_products,write_products` (one-time, opens a browser) followed by `shopify store execute --store ae86ba-2a.myshopify.com --query-file <f> [--variable-file <f>] [--allow-mutations] --json` reaches the identical Admin GraphQL API through the authenticated CLI session — no token typed or stored. `fix_mojibake.py`'s `gql_via_cli()` wires this in automatically whenever `SHOPIFY_TOKEN` is unset.
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

1. ~~Wrong `<title>` on the #1 bestseller + catalogue-wide mojibake.~~ — **resolved 2026-08-01**
   (Phase 7.6, `seo-ops/fix_mojibake.py`). Full live sweep of all 1,235 products: 0 mojibake found
   anywhere; the Motu Patlu bestseller's `<title>` already matched its H1 (fixed by an earlier
   phase's active-product rollout, this item had gone stale). The sweep did surface one different
   real defect — a product's own raw handle leaked into its `seo.title`/`seo.description`/visible
   body copy — fixed live. Two smaller findings came out of this pass and are now their own open
   items: an ambiguous product name (`a-touch-of-elegance-hamper`, title vs `seo.title` disagree
   with no body content to arbitrate) and ~62 products where `title` is literally the raw handle
   (never named) — both need business/content input, not further engineering. See
   `seo-audit/audit/CHANGELOG.md` (Phase 7.6) for full evidence.
2. ~~Unverified "★ 4.9 Rated" in the site header (`tbk_header_main`)~~ — **already resolved live**,
   confirmed 2026-07-30 via a live theme pull/diff of `sections/tbk-header.liquid` and
   `sections/header-group.json`; no rating content exists in either. This item was carried in the
   roadmap after the underlying fix (`36e1b0c`) had already shipped — verify against the live theme
   before re-actioning stale roadmap items like this one.
3. **Occasion mismatch in descriptions** — ~100+ products still labelled "anniversary" wrongly.
   Tool is written: `seo-ops/fix_description_occasion.py` (dry-run → CSV → `--apply`).

### The build track (Phase A promoted; design tokens unlocked)

**Phase A (schema dedup, footer restore) was promoted to live on 2026-07-14** (root `CHANGELOG.md`,
commit `77861b3`; re-verified live 2026-07-31 during Phase 7.0 reconciliation — `layout/theme.liquid`,
`snippets/structured-data.liquid`, `sections/site-footer.liquid`, `sections/footer-group.json` all
byte-identical to the live theme). This corrects a stale claim carried in this file until Phase 7.0.

**Design-token rendering (the roadmap's "unlocks the homepage build" step) is also done** — R0 of
the separate Phase 5 Liquid-architecture series (`docs/FINAL_REPORT.md`, 2026-07-31) restored
`render 'tbk-tokens'`/`render 'tbk-components'` to `layout/theme.liquid`, live and verified.

Root `CHANGELOG.md` additionally logs substantial further homepage-build work (Phase C1 §2/§3,
S1–S8 hero/trust-strip/section work) marked preview-only, not yet promoted — this predates and is
separate from the Phase 5/6/6.5 SEO-audit-and-performance track documented in
`seo-audit/audit/CHANGELOG.md`. **Not re-audited in Phase 7.0** (out of that pass's documentation-
hygiene scope) — recommend a dedicated homepage-build status review before assuming any of it is
current. Product page stays 🔒 throughout.

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
