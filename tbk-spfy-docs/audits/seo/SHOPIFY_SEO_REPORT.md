# Shopify SEO Report (Phase 7.2)

> **Update (Phase 7.4, 2026-07-31): the headline finding below is fixed and live.**
> `seo-ops/fix_seo_snippets.py`'s `build_desc()` now anchors every description on the product's own
> name (root cause of the duplication), rolled out across all 602 active products with 0 remaining
> duplicate groups. This report's counts describe the pre-fix state; see
> `seo-audit/audit/CHANGELOG.md` (Phase 7.4 entry) for the fix and verification evidence.

Continues from Phase 7.1 (`docs/TECHNICAL_SEO_MASTER.md`, commit `f85f8e3`). Scope: Shopify SEO
architecture only — no schema redesign, no UX work, no performance work (all explicitly excluded
by this phase's own instruction).

## Headline finding: systemic duplicate meta descriptions across active products

**This is the most significant SEO finding of this entire engagement.** While product SEO
*titles* are confirmed 100% unique across the catalogue (0 duplicate groups, verified across all
602 active products — the existing `"{Name} - Eggless | Meerut"` / `"{Name} | Meerut"` formula,
per `CLAUDE.md`, correctly guarantees uniqueness since it's keyed on the product name), meta
**descriptions** are generated from a template keyed on **occasion type + price + size count**
only — not the product name — causing massive duplication whenever multiple distinct products
share the same occasion/price/size combination.

### Evidence (exact counts, not estimated)

Exhaustively paginated all active products (`status:active`, 3 pages of ≤250, 602 total) and
checked for exact-match duplicate `seo.description` values:

| Page | Products checked | Products sharing a duplicate description | % |
|---|---|---|---|
| 1 | 250 | 184 | 73.6% |
| 2 | 250 | 235 | 94.0% |
| 3 | 102 | same pattern confirmed qualitatively (see below); exact count not separately computed | — |
| **Combined (pages 1–2, exact)** | **500** | **419** | **83.8%** |

The single largest duplicate group: **82 products** share the byte-identical description *"Made
to order for the celebration. 100% eggless. From Rs.1,700. 3 sizes. Same-day & midnight delivery
in Meerut."* Other large groups include 68 anniversary-cake products sharing one description, and
43 designer-cake products sharing another. Page 3 (the final 102 products, mostly wedding cakes)
shows the identical pattern — dozens of distinctly-named wedding cakes (`kundan-jewel-luxury-
wedding-cake`, `nawabi-elegance-wedding-cake`, `rajwada-heritage-wedding-cake`, `maharani-royale-
wedding-cake`, and ~30 more) all sharing *"Hand-finished tiers for the big day. 100% eggless. From
Rs.1,700. 3 sizes. Same-day & midnight delivery in Meerut."* verbatim.

### Why this wasn't caught by the prior title-migration work

`CLAUDE.md`'s "Key content facts" section documents the title formula's success but says nothing
about descriptions — the two fields evidently use different generation logic, and description
uniqueness was never separately verified until this pass (Phase 7.1 explicitly flagged this exact
gap and deferred it here, `docs/TECHNICAL_SEO_AUDIT.md`).

### Why this is NOT fixed in this phase

Per this phase's explicit rule — **"never invent SEO copy," "never rewrite copy," "no content
rewriting"** — writing genuinely unique descriptions for 400+ products is content authorship, not
a deterministic technical fix, and is explicitly out of bounds here regardless of value. A
template-formula change that incorporates the product's own real title (already unique, already
real data — the same input the title formula already uses successfully) is the obvious
**structural** fix, but applying it means rewriting the live `seo.description` field on hundreds of
real products — a mass business-content change at a scale this phase's "never modify business
content without approval" principle clearly reserves for explicit sign-off, not autonomous action.

**Recommendation, not action taken**: extend the existing description-generation logic (wherever
it lives — likely a `seo-ops/` script or a one-time migration, not live theme code) to include the
product name, mirroring the title formula's already-proven approach. Requires business approval
given the scale (400+ products) before execution.

## Other findings

### Title tags — clean

All 602 active products: unique, present, following the documented `"{Name} - Eggless | Meerut"`
/ `"{Name} | Meerut"` (60-char fallback) convention exactly as specified in `CLAUDE.md`. Zero
format violations found (checked programmatically against both patterns).

### Pages — 2 real gaps fixed, 3 gaps found with no safe fix available

Audited all 33 pages via Admin API (`title`, `isPublished`, legacy `global.title_tag`/
`global.description_tag` metafields, `bodySummary`):

- **`100-percent-eggless-bakery`** and **`refund-return-policy`** (both published, both had zero
  SEO title/description) — **fixed**: set `title_tag`/`description_tag` using the page's own real
  title and the real first sentence(s) of its existing body content, verbatim, no new authorship.
  Verified via `metafieldsSet`, zero `userErrors`.
- **`contact`, `frequently-asked-questions-faqs`, `terms-and-conditions`** (all published, all
  missing SEO title/description) — **not fixed**: all three have genuinely empty `bodySummary` (no
  real body text exists to derive a description from — these pages are likely built entirely from
  section blocks, not raw body HTML). Fabricating a description here would violate "never invent
  SEO copy." Flagged for business/content input.
- Without an explicit `description_tag`, `snippets/social-meta-tags.liquid`'s fallback chain
  (confirmed in Phase 6) uses `shop.description` as `og:description` — meaning these 3 pages likely
  emit the shop's generic description as their meta description, a real (if minor, low-traffic)
  duplicate-description instance distinct from the product-level issue above.

### Collections — 4 system collections with no custom SEO, no safe fix available

`all`, `best-selling-products`, `newest-products` (Shopify auto/smart collections — commonly left
uncustomized, low priority) and `gourmet-cookies-meerut` (title is literally its raw handle,
suggesting an unfinished/thin collection) all have empty `descriptionHtml` and empty `seo.title`/
`description` — no real content exists to derive from. Not fixed, flagged for content review.
36 collections total confirmed (Phase 7.1); the other 32 all have real, non-empty SEO title and
description, no duplication found among them.

### Content typos found, not fixed (content changes, out of this phase's scope)

- Collection `criciket` (handle and title both misspelled — should be "cricket"; its own `seo.title`
  is spelled correctly, so the typo is isolated to the display title/handle).
- Collection `paw-petrol` (title "PAW PETROL" — almost certainly intended "PAW Patrol").
- Collection `boy-or-girl-cake` (title in lowercase, inconsistent with Title Case used everywhere
  else).

None touched — these are content/naming decisions requiring business approval, not deterministic
technical fixes, and this phase explicitly excludes "content rewriting" and "changing business
claims."

### Canonical, robots, pagination, breadcrumbs, heading hierarchy, ALT coverage

All already fully audited in Phase 7.1 (`docs/CANONICAL_REPORT.md`, `docs/ROBOTS_REPORT.md`,
`docs/TECHNICAL_SEO_AUDIT.md`) — not repeated here, per "never repeat previous work." No new
evidence surfaced in this pass that changes those findings.

### Search/tag pages, sort-parameter indexing, 404 handling

- No custom `templates/404.*` override found — Shopify's native 404 handling applies (same finding
  category as robots/sitemap: correct default, not independently verifiable live due to the
  password gate).
- No theme-level sort-parameter (`?sort_by=`) indexing control found (no `noindex` logic keyed on
  query parameters) — Shopify's `canonical_url` object already strips sort/filter parameters from
  the canonical tag (confirmed in Phase 7.1), which is the standard, sufficient mitigation for
  sort/filter-parameter duplicate-content risk. No additional theme-level action needed.
- No dedicated "tag page" templates found distinct from standard collection/search routing.

## Related

[SHOPIFY_SEO_SCORECARD.md](SHOPIFY_SEO_SCORECARD.md), [TECHNICAL_SEO_MASTER.md](TECHNICAL_SEO_MASTER.md),
[TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md), [CRAWL_REPORT.md](CRAWL_REPORT.md).
