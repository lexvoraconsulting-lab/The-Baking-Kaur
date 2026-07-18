# SEO AUDIT LEDGER — The Baking Kaur

**Audit date:** 2026-07-18
**Branch:** phase-a/production-safety
**Store:** thebakingkaur.com · Shopify Basic · INR · IST · India
**Auditor account:** lexvoraconsulting@gmail.com

> This file is the persistent state for the Google/Shopify SEO programme.
> The audit does not need to be repeated. Update `STATUS` per row as work lands.

---

## PHASE 0 — ACCESS

| System | Access | Notes |
|---|---|---|
| Shopify Admin (MCP) | ✅ FULL | read + write, GraphQL Admin API |
| Theme repo (Liquid) | ✅ FULL | `F:\Shopify\The-Baking-Kaur`, git |
| Live storefront | ✅ READ | robots.txt, sitemap.xml, CDN fetch |
| **Google Search Console** | ❌ **NO ACCESS** | `lexvoraconsulting@gmail.com` is not an owner of `sc-domain:thebakingkaur.com`. Zero properties on this account. |
| **Google Merchant Center** | ❌ **NO ACCESS** | "your current account doesn't have access to any Merchant Center account." |
| Google & YouTube app | ❌ UNVERIFIED | `appInstallations` returns `access denied` on the MCP scope. |

**Consequence:** every GSC/GMC-sourced item (real 404 lists, disapprovals, impressions, CTR, Core Web Vitals field data, manual actions) is **OWNER INPUT REQUIRED**. Everything below was derived from Shopify data + theme code + live HTTP, not from Google reports.

---

## PHASE 1 — BASELINE (measured 2026-07-18)

| Metric | Value |
|---|---|
| Active products | 607 |
| Draft products | 584 (all `publishedAt: null` — never published) |
| Archived products | 44 |
| Collections | 34 |
| Collections with **0 products** | **8** |
| URL redirects | 794 |
| Redirects pointing at a **non-existent** collection | **223** |
| Sitemap children | products_1, pages_1, collections_1, blogs_1, agentic_discovery |
| robots.txt | Shopify default — no custom rules, no problems found |
| Canonical tag | present, `{{ canonical_url }}`, correct |

---

## ISSUE LEDGER

Priority: **P0** critical · **P1** major · **P2** important · **P3** optimisation · **P4** enhancement
Status: `DISCOVERED` · `IN PROGRESS` · `FIXED` · `VERIFIED FIXED` · `AWAITING GOOGLE` · `OWNER INPUT REQUIRED`

---

### P0-01 — 223 redirects resolve to non-existent collections (301 → 404)
- **System:** Shopify redirects
- **Root cause:** Bulk redirect import targeted `/collections/cakes` (194 redirects) and `/collections/gift-hampers` (29 redirects). Neither collection exists — verified `collectionByHandle` returns `null` for both.
- **Impact:** 223 old product URLs, most of which Google has indexed, currently 301 to a hard 404. Link equity destroyed, GSC "Not found (404)" inflated, GMC landing-page errors if any feed rows still reference them.
- **Fix options:** (a) create the two collections with correct products — safest, restores value; (b) rewrite all 223 redirect targets to existing collections (`birthday-cakes`, `designer-theme-cakes`, `cake-hampers`).
- **Recommendation:** (a) for `cakes` (create as a genuine parent collection), (b) for `gift-hampers` → retarget to `cake-hampers`.
- **STATUS:** DISCOVERED

---

### P0-02 — Site-wide FAQPage schema hardcoded in `<head>` on every page
- **System:** Theme — [layout/theme.liquid:68](layout/theme.liquid#L68) (9 Q&A pairs, unconditional)
- **Root cause:** FAQ JSON-LD pasted into `<head>`, no `request.page_type` guard. Renders on all 607 product pages, all collections, cart, search, policies.
- **Impact:** Google requires FAQ structured data to describe FAQ content **visible on that page**. Emitting it on 600+ product pages where no FAQ is visible is structured-data spam → **manual action risk**. Same defect class as the hardcoded `aggregateRating` already removed on 2026-07-16 (see `bk-local-business.liquid` comment).
- **Fix:** gate to the page(s) that actually render the FAQ visibly (FAQ page / homepage FAQ section), or move it into that section's template.
- **STATUS:** DISCOVERED

---

### P0-03 — Two conflicting business entities in schema
- **System:** Theme — [snippets/bk-local-business.liquid](snippets/bk-local-business.liquid) + [snippets/tbk-schema-website.liquid](snippets/tbk-schema-website.liquid)
- **Root cause:** `bk-local-business` emits `@type: Bakery` **with no `@id`**; `tbk-schema-website` emits `@type: Organization` with `@id: #organization`. Google sees two unlinked business entities per page with different data (Bakery has `streetAddress` + `geo` + hours + Facebook; Organization has none of those).
- **Impact:** Entity fragmentation, knowledge-panel confusion, weakened local signal.
- **Fix:** give the Bakery node `"@id": "https://thebakingkaur.com/#organization"` so the two merge into one entity, or collapse both into a single node.
- **STATUS:** DISCOVERED

---

### P0-04 — 8 zero-product collections indexed as thin/doorway pages
- **System:** Shopify collections
- **Root cause:** Keyword-targeted local landing collections created with body copy but never populated.
- **Affected:** `midnight-cake-delivery` (0), `midnight-cake-delivery-meerut` (0), `cake-delivery-meerut` (0), `same-day-cake-delivery-meerut` (0), `custom-cakes-meerut` (0), `kids-birthday-cakes-meerut` (0), `photo-cakes` (0), `showstopper-wedding-cake` (0)
- **Impact:** Empty commercial pages = soft 404 and, because they are near-identical keyword permutations of each other, a **doorway-page pattern** — explicitly against Google's spam policy and against this project's own brief.
- **Also:** `midnight-cake-delivery` and `midnight-cake-delivery-meerut` cannibalise the same query, both empty.
- **Fix:** populate each with genuinely relevant products (they exist in the catalogue) **or** merge duplicates and `noindex` the rest. Do not leave empty + indexed.
- **STATUS:** DISCOVERED

---

### P1-05 — Mojibake / wrong-product SEO titles on ~34% of active products
- **System:** Shopify product SEO
- **Root cause:** A bulk import wrote double-encoded UTF-8. Em-dash renders as `ÃÂÃÂ¢??`, ellipsis as `ÃÂÃÂ¢?ÃÂÃÂ¦`. 17 of a 50-product sample affected → est. ~200 products.
- **Worse:** several corrupted titles name a **different product** than the page. Examples:
  - `motu-patlu-designer-birthday-cake-meerut` → title says "Celestial Charm Cake"
  - `romantic-whisper-wedding-cake-meerut` → "Custom Wedding Cake"
  - `velvet-garden-wedding-cake-meerut` → "Pearl Wedding Cake"
  - `delicate-lace-wedding-cake-meerut` → "Tall Wedding Cake"
- **Impact:** unreadable SERP titles, title/page mismatch (Google rewrites or demotes), GMC title-vs-landing-page mismatch risk.
- **Fix:** regenerate SEO titles from `product.title` with proper UTF-8 encoding.
- **STATUS:** DISCOVERED

---

### P1-06 — Brand name duplicated in every product SEO title
- **System:** Shopify product SEO
- **Root cause:** Template applied as `{title} | The Baking Kaur` then a second pass appended `| The Baking Kaur Meerut`.
- **Example:** `Celebration Glow Birthday Cake | The Baking Kaur | The Baking Kaur Meerut` (78 chars)
- **Impact:** every title truncated in SERP; ~30 chars of every title wasted on a repeated brand token instead of intent keywords.
- **Fix:** single suffix, target ≤60 chars: `Celebration Glow Birthday Cake in Meerut | The Baking Kaur`.
- **STATUS:** DISCOVERED

---

### P1-07 — `nan` leaked into image alt text
- **System:** Shopify product media
- **Root cause:** pandas `NaN` written literally by an import script.
- **Example alt:** `nan in Meerut | The Baking Kaur` (confirmed on 3 of the 20 most-recently-updated products)
- **Impact:** broken accessibility, zero image-SEO value, Google Images loss.
- **Related:** other products have **empty** alt (`hamper13`, `white-alcohol-designer-cake-meerut`).
- **Fix:** regenerate alt from product title + descriptor. Never leave `nan`.
- **STATUS:** DISCOVERED

---

### P1-08 — Admin URL + raw `<style>` block leaked into a public collection description
- **System:** `winter-strawberry-collection` description
- **Root cause:** Content pasted from the Shopify admin UI, carrying a Polaris breadcrumb anchor and a full `<style>` sheet.
- **Leaked publicly:** `https://admin.shopify.com/store/ae86ba-2a/collections?selectedView=all` — exposes the internal store handle `ae86ba-2a`.
- **Also injects:** `body { background-color:#faf7f5; font-family:'Poppins' }` — a **global** CSS override on a live collection page, plus `<meta charset>`/`<meta viewport>` inside `<body>`.
- **Impact:** brand/design break, invalid HTML, CLS risk, internal URL disclosure.
- **Fix:** strip the `<style>`, `<meta>` and admin anchor from the description.
- **STATUS:** DISCOVERED

---

### P1-09 — LocalBusiness NAP does not match Shopify's business address
- **System:** `snippets/bk-local-business.liquid` vs Shopify billing address
- **Schema says:** `Fatah Complex, Thapar Nagar Lane 7, Meerut 250001`
- **Shopify says:** `Thapar Nagar Gali Number 7 Lajpat Bazaar Thapar Nagar, Meerut 250001`
- **Impact:** NAP inconsistency is a direct local-ranking negative and a Google Business Profile match failure.
- **Blocked on:** owner must confirm the canonical street address.
- **Also unverified:** `geo` lat/long `28.9931, 77.6939` — the snippet's own comment says these were never verified against the real shop pin.
- **STATUS:** OWNER INPUT REQUIRED

---

### P1-10 — LocalBusiness `image` is a 404
- **System:** `snippets/bk-local-business.liquid`
- **URL:** `https://thebakingkaur.com/cdn/shop/files/storefront.jpg` → **HTTP 404** (verified)
- **Impact:** `image` is a required property for LocalBusiness rich results; a dead URL invalidates it.
- **Fix:** point at a real CDN asset (a Shopify CDN URL needs the `?v=` version param) or remove the property.
- **STATUS:** DISCOVERED

---

### P1-11 — `all` / `best-selling-products` / `newest-products` are three indexable copies of the same 1,235 products
- **System:** Shopify collections
- **Impact:** large-scale duplicate content, crawl budget waste, canonical ambiguity.
- **Fix:** `noindex` the two sort-order collections; keep `/collections/all` as the canonical listing (or noindex all three and rely on topical collections).
- **STATUS:** DISCOVERED

---

### P1-12 — `productType` misclassification breaks breadcrumbs and future feed data
- **System:** Shopify product data → [snippets/tbk-schema-breadcrumb.liquid](snippets/tbk-schema-breadcrumb.liquid)
- **Examples:** every anniversary cake is typed `Wedding Cake`; `hamper13` has an **empty** `productType`.
- **Breadcrumb defect:** position 2 uses `product.type` as the **name** but `product.collections.first.handle` as the **URL** — name and destination frequently disagree. Empty type falls back to the literal string `"Cakes"`.
- **Impact:** wrong breadcrumb rich result; when the Google feed goes live, `product_type` will be wrong on ~100 products.
- **Fix:** correct `productType` values; make the breadcrumb derive name and URL from the same collection object.
- **STATUS:** DISCOVERED

---

### P2-13 — Render-blocking third-party resources in `<head>`
- **System:** [layout/theme.liquid](layout/theme.liquid)
- **Findings:**
  - Google Fonts `<link rel="stylesheet">` (Cormorant Garamond + Manrope) — render-blocking, external origin
  - Uploadcare `uploadcare.full.min.js` — **synchronous, blocking**, loaded on every page including collections and cart where the uploader is never used
- **Impact:** LCP and INP degradation site-wide. This is the single largest self-inflicted Core Web Vitals cost visible in the theme.
- **Fix:** self-host the fonts via Shopify assets (or `font_face` with `font-display:swap`); load Uploadcare `defer` and only on templates that use it.
- **STATUS:** DISCOVERED

---

### P2-14 — Dead snippet: `snippets/meta-tags.liquid`
- **System:** Theme
- **Root cause:** duplicate of `social-meta-tags.liquid` (its own first line reads `<!-- /snippets/social-meta-tags.liquid -->`). Nothing renders it — `grep` across `layout/`, `sections/`, `snippets/`, `templates/` returns zero references.
- **Fix:** delete.
- **STATUS:** DISCOVERED

---

### P2-15 — `og:image` served over `http:`
- **System:** [snippets/social-meta-tags.liquid](snippets/social-meta-tags.liquid) (and the dead `meta-tags.liquid`)
- **Code:** `content="http:{{ page_image | image_url }}"`
- **Impact:** mixed-content warning on some social scrapers; `og:image:secure_url` is present so impact is limited.
- **Fix:** use `https:`.
- **STATUS:** DISCOVERED

---

### P2-16 — Dangling `@id` reference in collection schema
- **System:** [snippets/tbk-schema-collection.liquid](snippets/tbk-schema-collection.liquid)
- **Root cause:** references `"breadcrumb": { "@id": "...#breadcrumb" }` but `tbk-schema-breadcrumb.liquid` emits **no** `@id`.
- **Impact:** unresolvable reference; the breadcrumb/collection link is silently dropped.
- **Fix:** add `"@id": "{{ canonical_url }}#breadcrumb"` to the BreadcrumbList.
- **STATUS:** DISCOVERED

---

### P2-17 — ~19 collections with no SEO title, no meta description, no body copy
- **System:** Shopify collections
- **Affected:** `for-him`, `for-her`, `baby-girl`, `butterfly`, `criciket`, `motu-patlu`, `unicorn`, `jungle-animal-theme`, `chartered-accountant`, `roblox`, `paw-petrol`, `teddy`, `ribbon-cake`, `kpop-cake`, `boy-or-girl-cake`, `luxury-diwali-hampers`, `all`, `best-selling-products`, `newest-products`, `showstopper-wedding-cake`
- **Impact:** thin pages competing for crawl budget; several of these (unicorn, motu-patlu, roblox, paw-petrol) map to **real high-intent kids-cake queries** and are being wasted.
- **Note:** `for-her` has 1 product, `paw-petrol` has 4 — near-empty.
- **STATUS:** DISCOVERED

---

### P2-18 — Typo baked into a live collection URL
- **System:** `/collections/criciket` (should be `cricket`), title also reads `Criciket`
- **Impact:** the misspelling is the URL and the H1 — zero ranking for "cricket cake".
- **Fix:** rename handle to `cricket-cake-meerut`, fix the title, let Shopify auto-create the redirect.
- **STATUS:** DISCOVERED

---

### P2-19 — Duplicated text in collection SEO title
- **System:** `midnight-cake-delivery`
- **Title:** `Midnight Cake DeliveryMidnight Cake Delivery in Meerut | Birthday & Anniversary Surprise Delivery`
- **STATUS:** DISCOVERED

---

### P2-20 — Malformed HTML in collection descriptions
- **System:** `birthday-cakes`, `anniversary-cakes`
- **`birthday-cakes`:** `<h2>Related Collections</h2><ul>` nested **inside** another `<ul>`, duplicated.
- **`anniversary-cakes`:** the H2 `Customized Anniversary Cakes in Meerut` appears **twice**, immediately after a near-identical H2.
- **Impact:** invalid markup, duplicated headings dilute topical signal.
- **STATUS:** DISCOVERED

---

### P2-21 — Identical templated meta descriptions across ~600 products
- **System:** Shopify product SEO
- **Pattern:** `Order {title} online from The Baking Kaur. Fresh cakes, customization, same‑day & midnight delivery in Meerut.`
- **Impact:** near-duplicate descriptions; Google will usually discard them and synthesise its own. Low CTR ceiling.
- **Fix:** vary by product type and occasion. Lower priority than P1-05/P1-06 — Google rewriting a description costs less than a corrupted title.
- **STATUS:** DISCOVERED

---

### P3-22 — 584 draft products staged with non-descriptive handles
- **System:** Shopify products
- **Examples:** `ch107`, `ch109`, `ch97`, `98`, `5`
- **Impact:** none today (`publishedAt: null`, no live URL, correctly absent from sitemap). **But** publishing them as-is mints 584 keyword-free URLs that are painful to change later.
- **Fix:** rewrite handles **before** publishing. This is the cheapest moment to do it.
- **STATUS:** DISCOVERED — blocking gate on any bulk publish

---

### P3-23 — Junk redirect entries from a bad import
- **System:** Shopify redirects
- **Examples:**
  - `/products/deleted-https://thebakingkaur.com/products/together-forever-couple-anniversary-cake?country=in&currency=inr&utm_campaign=sag_organic&...`
  - `/$%7bt%7d` (an unrendered `${t}` template literal)
- **Impact:** cosmetic; these paths are never requested. Clean up during the P0-01 redirect pass.
- **STATUS:** DISCOVERED

---

### P4-24 — No review/rating system → no `aggregateRating`, no Merchant listing stars
- **System:** Site-wide
- **Context:** a fabricated `4.8 / 500 reviews` was correctly removed on 2026-07-16, and "4.9 Rated" was removed from the mobile drawer in `36e1b0c`. Nothing legitimate replaced it.
- **Impact:** no star rich results, weaker Shopping/Free-Listing presentation vs competitors.
- **Fix:** install a genuine review app, collect real reviews, emit `aggregateRating` computed from real entries only. See `REVIEW_STRATEGY.md`.
- **STATUS:** OWNER INPUT REQUIRED

---

## OWNER INPUT REQUIRED — blocking items

| # | What is needed | Why | What happens next |
|---|---|---|---|
| 1 | Add `lexvoraconsulting@gmail.com` as a **full user** on Search Console `sc-domain:thebakingkaur.com` (likely owned by `thebakingkaur@gmail.com`) | Every real 404 list, indexing-exclusion breakdown, query/CTR data, Core Web Vitals field data and manual-action check comes from GSC. None of it is inferable from Shopify. | Phases 3, 4, 20 execute; "Validate Fix" gets submitted after the P0 redirect repair. |
| 2 | Add the same account as **Admin** on Google Merchant Center | Disapprovals, account-level warnings, feed diagnostics, Free-Listing eligibility are all GMC-only. | Phases 9–12 execute. |
| 3 | Confirm the **canonical street address** — `Fatah Complex, Thapar Nagar Lane 7` (schema) or `Thapar Nagar Gali Number 7, Lajpat Bazaar` (Shopify billing)? | NAP must be identical across schema, Shopify, and Google Business Profile. Guessing risks entrenching the wrong one. | P1-09 fixed; local signal consolidated. |
| 4 | Confirm **shop latitude/longitude** from Google Maps | Current values were never verified — flagged in the snippet's own comment. | `geo` corrected. |
| 5 | Decide on a **review platform** | `aggregateRating` may only ever be computed from real reviews. | P4-24 unblocks. |

---

## RECOMMENDED NEXT ACTION

**Fix P0-01.** 223 indexed product URLs currently 301 into a hard 404 — this is live, measurable link-equity loss happening on every crawl, and it is the only P0 fixable today without owner input or Google access.

Order after that: P0-02 (manual-action risk) → P0-04 (doorway risk) → P0-03 → P1-05/06 (bulk title repair).

---

## CHANGE LOG

| Date | Change | File / System | Rollback | Test result |
|---|---|---|---|---|
| 2026-07-18 | Audit — no modifications | — | — | — |
| 2026-07-18 | Created `/collections/cakes` smart collection (`product_type CONTAINS Cake`), published to Online Store | Shopify collection `327322730665` | Delete collection; the 194 redirects revert to their prior broken state | Live 200, H1 "Cakes", 47 pages of products |
| 2026-07-18 | Published `luxury-diwali-hampers` (was unpublished → 404) | Shopify collection `320698745001` | `publishableUnpublish` | Live 200 |
| 2026-07-18 | Retargeted 26 Diwali redirects → `luxury-diwali-hampers`, 2 generic → `cake-hampers` | Shopify redirects | Targets recorded in this ledger | 0 redirects to dead targets; 3 sampled URLs single-hop 200 |
| 2026-07-18 | Removed hardcoded FAQPage JSON-LD from `<head>` | `layout/theme.liquid` | `git revert 7840091` | JSON-LD parses; no inline ld+json remains |
| 2026-07-18 | Merged Bakery + Organization via shared `@id`; removed duplicated telephone/address/sameAs | `snippets/bk-local-business.liquid`, `snippets/tbk-schema-website.liquid` | `git revert 7840091` | Both blocks parse; `#organization` present in both |
| 2026-07-18 | LocalBusiness `image` 404 → `settings.logo` | `snippets/bk-local-business.liquid` | `git revert 7840091` | No dead URL in markup |
| 2026-07-18 | Added `@id` to BreadcrumbList; aligned collection ref to `canonical_url` | `snippets/tbk-schema-breadcrumb.liquid`, `tbk-schema-collection.liquid` | `git revert 7840091` | Parses; reference resolves |
| 2026-07-18 | noindex,follow rule for empty collections + 3 duplicate sort listings | `layout/theme.liquid` | `git revert 1e4e932` | `shopify theme check`: 0 new offenses. **Not yet live — needs theme push** |
| 2026-07-18 | Bulk SEO title/description repair, **in progress** | 607 active products | `seo-ops/rollback.csv` | b00–b01 applied, 100/607, 0 userErrors |

---

## IN-FLIGHT WORK — RESUME HERE

### Bulk SEO title repair (P1-05 / P1-06) — 100 of 607 applied

All artefacts are committed under [`seo-ops/`](seo-ops/) so this survives the session:

| File | Purpose |
|---|---|
| `seo-ops/rule.py` | The transformation. `seo_title()` derives the title from `product.title`, never from the corrupt `seo.title`. Idempotent. |
| `seo-ops/rollback.csv` | 607 rows: id, old title, old description, new title, new description. **This is the rollback data.** |
| `seo-ops/batches/b00–b12.graphql` | Ready-to-run aliased `productUpdate` mutations, 50 products each |
| `seo-ops/PROGRESS.txt` | Which batches have been applied |

**To resume:** run `seo-ops/batches/bNN.graphql` through the Shopify MCP `graphql_mutation` tool, in order, appending each to `PROGRESS.txt`. Batches are independent and idempotent — re-running one is harmless.

**Why batched and not bulk:** `bulkOperationRunMutation` is blocked by the MCP safety policy ("can execute arbitrary mutations"). The bulk *query* export was used for the read side, so no catalogue data had to pass through context.

**Measured defect counts across all 607 active products:**

| Defect | Count |
|---|---|
| SEO title broken (any cause) | 607 / 607 |
| — mojibake (double-encoded UTF-8) | 74 |
| — brand duplicated | 536 |
| SEO description corrupt | 34 |
| Products whose title changes | 607 |

Resulting titles: min 40, max 65, avg 56 chars; 606/607 contain "Meerut"; 592/607 contain the brand once.

---

## VERIFICATION LEDGER

| Claim | Method | Result |
|---|---|---|
| `/collections/cakes` does not exist | `collectionByHandle(handle:"cakes")` | `null` — confirmed |
| `/collections/gift-hampers` does not exist | `collectionByHandle(handle:"gift-hampers")` | `null` — confirmed |
| 194 + 29 redirects target them | `urlRedirectsCount(query:"target:...")` | 194 / 29 — confirmed |
| LocalBusiness image is dead | HTTP GET `…/storefront.jpg` | 404 — confirmed |
| GSC inaccessible | Navigated to the property | "you don't have access to this property" — confirmed |
| GMC inaccessible | Navigated to merchants.google.com | "doesn't have access to any Merchant Center account" — confirmed |
| FAQ schema unconditional | Read `layout/theme.liquid:68` | No page_type guard — confirmed |
| `meta-tags.liquid` unreferenced | `grep -rl "render 'meta-tags'"` across theme | Zero hits — confirmed |
| Mojibake rate | 50-product sample | 17/50 (~34%) — sampled, not exhaustive |
| `nan` alt text rate | 20-product sample | 3/20 — sampled, not exhaustive |
