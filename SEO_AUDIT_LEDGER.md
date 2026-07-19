# SEO AUDIT LEDGER — The Baking Kaur

**Audit date:** 2026-07-18
**Branch:** phase-a/production-safety
**Store:** thebakingkaur.com · Shopify Basic · INR · IST · India
**Shopify access:** full (MCP)  
**Google access:** BLOCKED — session authenticated as `lexvoraconsulting@gmail.com`, which is NOT The Baking Kaur’s Google account. See Phase 0.

> This file is the persistent state for the Google/Shopify SEO programme.
> The audit does not need to be repeated. Update `STATUS` per row as work lands.

---

## PHASE 0 — ACCESS

| System | Access | Notes |
|---|---|---|
| Shopify Admin (MCP) | ✅ FULL | read + write, GraphQL Admin API |
| Theme repo (Liquid) | ✅ FULL | `F:\Shopify\The-Baking-Kaur`, git |
| Live storefront | ✅ READ | robots.txt, sitemap.xml, CDN fetch |
| **Google Search Console** | ⚠️ **ACCESS BLOCKED — WRONG GOOGLE ACCOUNT AUTHENTICATED** | The browser session is signed in as `lexvoraconsulting@gmail.com`, which is **not** the account that owns or manages The Baking Kaur's Google properties. |
| **Google Merchant Center** | ⚠️ **ACCESS BLOCKED — WRONG GOOGLE ACCOUNT AUTHENTICATED** | Same cause. |
| Google & YouTube channel | ✅ **CONFIRMED PRESENT** | `publications` returns `gid://shopify/Publication/136327889065` "Google & YouTube" — this is the live GMC feed source. |

> ### ⚠️ Do not misread the Google access status
>
> The Baking Kaur **has** a Google Search Console property and **has** a Google
> Merchant Center account. They live under a **different Google account**.
>
> The earlier probe returned "you don't have access to this property" and
> "your current account doesn't have access to any Merchant Center account".
> Those messages describe the **authenticated session**, not the business.
> They are **not** evidence that the properties are missing, and must never be
> read that way.
>
> **Never create** a new Search Console property, a new or duplicate Merchant
> Center account, or a new Google integration. The existing properties are the
> ones to use.
>
> Do not retry Google access with `lexvoraconsulting@gmail.com`.

**Consequence:** every GSC/GMC-sourced item (real 404 lists, disapprovals, impressions, CTR, Core Web Vitals field data, manual actions) is **OWNER ACTION REQUIRED — AUTHENTICATE CORRECT THE BAKING KAUR GOOGLE ACCOUNT**. Everything below was derived from Shopify data + theme code + live HTTP, not from Google reports — so it stands on its own and does not need redoing once Google access arrives.

**On Google access, resume the original master mission:** audit the *existing* GSC property and the *existing* GMC account, then cross-reference both against this ledger and the Shopify fixes already completed. Do not re-run the Shopify audit except where verification requires it.

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
- **STATUS:** **VERIFIED FIXED** — `/collections/cakes` created + published (985 products, live 200); 26 Diwali + 2 generic hamper redirects retargeted; `luxury-diwali-hampers` published (it was unpublished, which would have made it a redirect-to-404). 0 redirects now point at a dead target; sampled source URLs resolve single-hop 200.

---

### P0-02 — Site-wide FAQPage schema hardcoded in `<head>` on every page
- **System:** Theme — [layout/theme.liquid:68](layout/theme.liquid#L68) (9 Q&A pairs, unconditional)
- **Root cause:** FAQ JSON-LD pasted into `<head>`, no `request.page_type` guard. Renders on all 607 product pages, all collections, cart, search, policies.
- **Impact:** Google requires FAQ structured data to describe FAQ content **visible on that page**. Emitting it on 600+ product pages where no FAQ is visible is structured-data spam → **manual action risk**. Same defect class as the hardcoded `aggregateRating` already removed on 2026-07-16 (see `bk-local-business.liquid` comment).
- **Fix:** gate to the page(s) that actually render the FAQ visibly (FAQ page / homepage FAQ section), or move it into that section's template.
- **STATUS:** **FIXED IN REPO — PENDING THEME PUSH.** Block removed from `layout/theme.liquid`; valid FAQ microdata via `sections/accordion.liquid` left intact. Not live until the theme is pushed.

---

### P0-03 — Two conflicting business entities in schema
- **System:** Theme — [snippets/bk-local-business.liquid](snippets/bk-local-business.liquid) + [snippets/tbk-schema-website.liquid](snippets/tbk-schema-website.liquid)
- **Root cause:** `bk-local-business` emits `@type: Bakery` **with no `@id`**; `tbk-schema-website` emits `@type: Organization` with `@id: #organization`. Google sees two unlinked business entities per page with different data (Bakery has `streetAddress` + `geo` + hours + Facebook; Organization has none of those).
- **Impact:** Entity fragmentation, knowledge-panel confusion, weakened local signal.
- **Fix:** give the Bakery node `"@id": "https://thebakingkaur.com/#organization"` so the two merge into one entity, or collapse both into a single node.
- **STATUS:** **STRUCTURAL CONFLICT FIXED IN REPO — PENDING THEME PUSH.** Bakery given `@id` `#organization` so the two nodes merge; duplicated telephone/address/sameAs removed from the Organization node. The canonical street address itself remains **OWNER INPUT REQUIRED** (see P1-09) — no business data was invented.

---

### P0-04 — 8 zero-product collections indexed as thin/doorway pages
- **System:** Shopify collections
- **Root cause:** Keyword-targeted local landing collections created with body copy but never populated.
- **Affected:** `midnight-cake-delivery` (0), `midnight-cake-delivery-meerut` (0), `cake-delivery-meerut` (0), `same-day-cake-delivery-meerut` (0), `custom-cakes-meerut` (0), `kids-birthday-cakes-meerut` (0), `photo-cakes` (0), `showstopper-wedding-cake` (0)
- **Impact:** Empty commercial pages = soft 404 and, because they are near-identical keyword permutations of each other, a **doorway-page pattern** — explicitly against Google's spam policy and against this project's own brief.
- **Also:** `midnight-cake-delivery` and `midnight-cake-delivery-meerut` cannibalise the same query, both empty.
- **Fix:** populate each with genuinely relevant products (they exist in the catalogue) **or** merge duplicates and `noindex` the rest. Do not leave empty + indexed.
- **STATUS:** **FIXED IN REPO — PENDING THEME PUSH.** 6 of the 8 turned out to be **unpublished** (absent from the collections sitemap), so never indexed and not doorway pages. Only `photo-cakes` and `midnight-cake-delivery` were live+empty. Redirecting them to `/pages/photo-cakes` and `/pages/midnight-surprise-delivery` was rejected — both pages have **empty bodies**. Replaced with a rule: any collection with 0 products gets `noindex,follow`. Self-healing and covers future empties.

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
- **STATUS:** **IN PROGRESS — 250/607 applied** (b00–b04, zero errors). Remaining b05–b12 committed under `seo-ops/`.

---

### P1-06 — Brand name duplicated in every product SEO title
- **System:** Shopify product SEO
- **Root cause:** Template applied as `{title} | The Baking Kaur` then a second pass appended `| The Baking Kaur Meerut`.
- **Example:** `Celebration Glow Birthday Cake | The Baking Kaur | The Baking Kaur Meerut` (78 chars)
- **Impact:** every title truncated in SERP; ~30 chars of every title wasted on a repeated brand token instead of intent keywords.
- **Fix:** single suffix, target ≤60 chars: `Celebration Glow Birthday Cake in Meerut | The Baking Kaur`.
- **STATUS:** **IN PROGRESS — 250/607 applied** (same pass as P1-05).

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
- **STATUS:** **FIXED IN REPO — PENDING THEME PUSH.** `image` now `settings.logo`, an already-verified asset.

---

### P1-11 — `all` / `best-selling-products` / `newest-products` are three indexable copies of the same 1,235 products
- **System:** Shopify collections
- **Impact:** large-scale duplicate content, crawl budget waste, canonical ambiguity.
- **Fix:** `noindex` the two sort-order collections; keep `/collections/all` as the canonical listing (or noindex all three and rely on topical collections).
- **STATUS:** **FIXED IN REPO — PENDING THEME PUSH.** `all`, `best-selling-products`, `newest-products` get `noindex,follow`; `/collections/cakes` is the canonical category page.

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
- **STATUS:** **FIXED IN REPO — PENDING THEME PUSH.** `@id` added to BreadcrumbList; both sides aligned to `canonical_url`.

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

### P2-25 — Typos baked into live product titles (NEW, found 2026-07-18)
- **System:** Shopify product titles
- **Examples:** `Chocolate Strawbeery`, `Dubai Viral Kunafa Starberry` (both should be "Strawberry")
- **Impact:** the misspelling is the H1, the product title and now the SEO title. Zero ranking for "strawberry cake", which is a live seasonal line (`winter-strawberry-collection`, 23 products).
- **Why not auto-fixed:** the SEO title rule deliberately derives from `product.title` and preserves product wording. Renaming a product changes the storefront H1 and customer-facing name — a merchandising decision, not a technical one.
- **Fix:** correct the product titles, then re-run the affected `seo-ops` batch to propagate.
- **STATUS:** OWNER INPUT REQUIRED (confirm renames)

---

### P2-26 — Dead snippet include: 78KB never renders (NEW, found 2026-07-18)
- **System:** [layout/theme.liquid:152](layout/theme.liquid#L152)
- **Code:** `{% include 'shine-trust.liquid' %}` — Liquid resolves this to `snippets/shine-trust.liquid.liquid`, which does not exist. `snippets/shine-trust.liquid` (78 KB) does.
- **Impact:** `include` fails silently in production, so a 78 KB trust-badge snippet has never rendered. Surfaced by `shopify theme check` as `MissingTemplate`.
- **Why not auto-fixed:** "fixing" it would suddenly inject 78 KB of markup into every page — a visual and Core Web Vitals change. Whether that content is still wanted is a UI decision.
- **Fix:** either drop the `.liquid` extension from the include (turns it on) or delete the include and the snippet (removes 78 KB of dead weight). Deleting is the ponytail default if nobody misses it.
- **STATUS:** OWNER INPUT REQUIRED (decide on/off)

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
| 1 | **Authenticate the browser session as the Google account that actually manages The Baking Kaur's Search Console** (not `lexvoraconsulting@gmail.com`). Alternatively, grant that account access from the owning account. | Every real 404 list, indexing-exclusion breakdown, query/CTR data, Core Web Vitals field data and manual-action check comes from GSC. None of it is inferable from Shopify. **The property exists — it is an authentication problem, not a missing-property problem.** | Phases 3, 4, 20 execute against the **existing** property; "Validate Fix" gets submitted for the P0-01 redirect repair, which is already done and waiting. |
| 2 | **Authenticate the same correct Google account for Merchant Center.** | Disapprovals, account-level warnings, feed diagnostics and Free-Listing eligibility are GMC-only. The feed source is already confirmed: the "Google & YouTube" Shopify channel. | Phases 9–12 execute against the **existing** account. |
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

## SEO TITLE ARCHITECTURE v2 — supersedes v1

**v1 was over-optimised and is being reverted.** It appended "in Meerut" to 606/607 SEO titles. Evidence that this was wrong:

- only **81 / 607 (13%)** product titles mention Meerut natively — appending to 100% imposed a template the catalogue does not support
- product titles are already unique (**606 distinct of 607**, avg 32 chars) — uniqueness needs no template
- a locality token repeated across 606 titles is a title-rewrite signal to Google and buys nothing in the map pack, which is driven by GBP, proximity and reviews
- **Merchant Center is unaffected either way** — GMC reads the Shopify *product title*, not the SEO meta title, and no product titles were ever changed

**Architecture:**

| Level | Pattern | Carries "Meerut"? |
|---|---|---|
| **Product** | `{Clean Product Title} \| The Baking Kaur` | **No** |
| **Collection** | `{Category} in Meerut \| {qualifier} \| The Baking Kaur` | Yes |
| **Local landing / service page** | full local intent | Yes |

Locality is held where the query volume is — category and service pages — not spread across 600 product pages.

**Deferred deliberately:** a strategic per-product locality subset. Choosing it without Search Console impression data would be guessing. Revisit once GSC access is restored and genuine local-intent product queries can be identified.

**Was anything good destroyed?** No. Segmenting the pre-change export: **532 brand-duplicated + 74 mojibake + 1 empty = 607. Zero clean originals existed.** There were no unique optimised titles to preserve.

Result of v2: 606 products, **606 distinct titles**, 30–65 chars (avg 46), zero mechanical locality.

---

## IDENTIFIER_EXISTS — segmented, not blanket-applied

Segmentation from the export (evidence, not assumption):

| Segment | Count |
|---|---|
| A — custom / made-to-order, no manufacturer GTIN | **606** |
| B — legitimate GTIN / barcode | **0** |
| C — branded packaged / resold | **0** |
| D — has MPN | **0** |
| E — uncertain | **0** |

Basis: **Vendor is "The Baking Kaur" on all 607** — there are no resold third-party goods. **0 barcodes across 21,562 variant rows; 0 MPNs.** Three hampers were reviewed as possible segment C and resolved to A: the sold unit is an in-house assembled hamper, not a branded packaged good.

Because segments B/C/D are empty, `identifier_exists = FALSE` is correct for the whole active catalogue. Had any branded packaged product existed, it would have been excluded.

**Source of truth:** metafield `mm-google-shopping.custom_product` (boolean) — a defined metafield on this store. Set via `productUpdate`, in the same write as the SEO title, so there is one pass, not two.

**Status: TECHNICALLY FIXED AT SOURCE — AWAITING MERCHANT CENTER REPROCESSING.** Shopify now holds the correct value; only Merchant Center can confirm the feed consumes it, and that needs the correct Google account.

---

## IN-FLIGHT WORK — RESUME HERE

### Bulk SEO title repair (P1-05 / P1-06) — **250 of 607 applied** (b00–b04)

Paused at b04, not because of an error. `bulkOperationRunMutation`
is blocked, so each batch must be pasted through the MCP tool, which costs
context on both the read and the write. The run was halted with state committed
rather than risk exhausting context mid-batch and losing the ledger.

**Remaining: b05–b12, 357 products.** Batches are independent and idempotent.

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

**Verified after b00–b02** (Shopify API read-back):

| Product | Before | After |
|---|---|---|
| Motu Patlu Designer Birthday Cake | `Celestial Charm Cake ÃÂÃÂ¢?? 100% Eggless…` (wrong product, mojibake) | `Motu Patlu Designer Birthday Cake in Meerut \| The Baking Kaur` |
| Best Husband Cake Design | `Best Husband Cake Design ÃÂÃÂ¢?? 100%…` | `Best Husband Cake Design in Meerut \| The Baking Kaur` |

Two rule bugs were caught by spot-checking mid-run and fixed before they shipped:
`"X The Baking Kaur, Meerut"` → `"…Meerut in Meerut"`, and `"Bespoke Wedding Cake
by <brand>"` → `"Bespoke Wedding Cake by in Meerut"`. Neither reached the 150
already applied (verified by diffing the regenerated rule against applied rows).

---

### PENDING DEPLOY — theme changes are committed but NOT live

`layout/theme.liquid` and the schema snippets are fixed in git and pass
`shopify theme check`, but **nothing is live until the theme is pushed** to
theme `151307485353`. Until then P0-02, P0-03, P0-04, P1-10 and P2-16 are
FIXED-IN-REPO, not VERIFIED FIXED.

Recommended: push to an unpublished preview theme first, confirm with Google's
Rich Results Test that (a) no FAQPage appears on a product URL, (b) exactly one
merged business entity appears, (c) `noindex` appears on `/collections/photo-cakes`
and not on a populated collection — then publish.

---

## VERIFICATION LEDGER

| Claim | Method | Result |
|---|---|---|
| `/collections/cakes` does not exist | `collectionByHandle(handle:"cakes")` | `null` — confirmed |
| `/collections/gift-hampers` does not exist | `collectionByHandle(handle:"gift-hampers")` | `null` — confirmed |
| 194 + 29 redirects target them | `urlRedirectsCount(query:"target:...")` | 194 / 29 — confirmed |
| LocalBusiness image is dead | HTTP GET `…/storefront.jpg` | 404 — confirmed |
| GSC not reachable **from this session** | Navigated to the property | "you don't have access to this property" — confirms the **signed-in account** lacks access. Says nothing about whether the property exists. It does. |
| GMC not reachable **from this session** | Navigated to merchants.google.com | "doesn't have access to any Merchant Center account" — same: a property of the session, not of the business. |
| FAQ schema unconditional | Read `layout/theme.liquid:68` | No page_type guard — confirmed |
| `meta-tags.liquid` unreferenced | `grep -rl "render 'meta-tags'"` across theme | Zero hits — confirmed |
| Mojibake rate | 50-product sample | 17/50 (~34%) — sampled, not exhaustive |
| `nan` alt text rate | 20-product sample | 3/20 — sampled, not exhaustive |

---

## NEW FINDINGS FROM THE CATALOGUE EXPORT (2026-07-18)

| ID | Finding | Count | Status |
|---|---|---|---|
| N1 | Active products **not published** to Online Store — live in admin, absent from storefront and sitemap | 46 | Classify (see below) |
| N2 | Active products with **no image at all** — cannot be listed in Merchant Center, `image_link` is required | 12 | OWNER INPUT REQUIRED — PRODUCT IMAGE NEEDED |
| N3 | Products with **no usable image alt text** — only 100/607 have any; 62 images literally read `nan` | 507 | Ready, not executed |
| N4 | `identifier_exists` unset | 607 | Sample applied; bulk pending |
| N5 | Active products with empty `Type` (feeds `product_type`) | 4 | Ready |
| N6 | Draft products with non-descriptive handles (`ch107`, `b54`, `98`) | 278 of 584 | Gate before any bulk publish |
| N7 | **Junk product live in catalogue**: "Shopify flow" (`shopify-flow`) — ACTIVE, unpublished, 0 inventory, no image, no variants. A Shopify Flow app artifact. | 1 | Recommend ARCHIVE — owner confirm (not deleted) |
| N8 | **Two apps write different Google product categories** — `mm-google-shopping.google_product_category` = `2194.0` vs `mc-facebook.google_product_category` = `8271`. Conflicting taxonomy values on the same product. | catalogue-wide | Investigate once GMC access restored |
| N9 | **Judge.me is already installed** (`judgeme.badge` / `judgeme.widget` metafields) and reports "0 reviews". P4-24 is therefore *not* "install a review app" — the platform exists and has no review volume. `aggregateRating` still must not be emitted until real reviews exist. | — | Revises P4-24 |

### N7 note
"Shopify flow" is simultaneously one of the 46 unpublished (N1) and one of the 12 imageless (N2), so both counts include a record that is not a real product. It was **excluded from the SEO title batches** rather than dressed up with a meta title.


---

# PHASE 13 — GOOGLE ACCESS RESTORED + VERIFIED RECONCILIATION (2026-07-19)

**Google access: RESOLVED.** Root cause was **not** a missing property and **not** an OAuth
connector misconfiguration. There is **no GSC/GMC connector installed at all** — access rides
entirely on the Chrome session's Google identity, which was defaulting to
`lexvoraconsulting@gmail.com`. Signing Chrome in as **`thebakingkaur@gmail.com`** (the account
matching the Shopify store owner email) opened both properties immediately.

| System | Access | Identifier |
|---|---|---|
| Google Search Console | ✅ VERIFIED | `sc-domain:thebakingkaur.com` |
| Google Merchant Center | ✅ VERIFIED | account `5552376763` — single account, no duplicate |

**Recommended durable fix (not yet done):** add `lexvoraconsulting@gmail.com` as a delegated
user from inside GSC (Settings → Users and permissions) and GMC (Settings → People and access).

---

## P4 — CATALOGUE IMPORT: ✅ COMPLETE (verified 2026-07-19)

1,235 products imported. Verified against live Shopify, not assumed:

| Handle | Status | Evidence |
|---|---|---|
| `ch241` | ACTIVE | live description matches generated copy verbatim |
| `addon-balloons` | DRAFT | reads "non-edible celebration item and is not a food product" — the non-food fix landed |

**⚠️ DEFECT NOW LIVE (from the import):** `ch241` renders the flavour list as
*"a choice of Lotus Biscoffstrawberry Vanilla, …"*. This traces to the malformed source option
value `lotus-biscoffStrawberry Vanila` (two values concatenated in the Shopify variant data).
The generator normalised it into prose rather than skipping it. **This is on an ACTIVE product
and is customer-visible.** Fix at source (rename the variant option value in Admin), then the
prose can be regenerated for that one product.

---

## PHASE 1 BASELINE — MEASURED FROM GSC (data as of 10/07/2026)

| Metric | Value |
|---|---:|
| Web search clicks (~18 Apr → 11 Jul) | 3,526 |
| Indexed pages | 769 |
| Not indexed | 1,907 (11 reasons) |
| Core Web Vitals — mobile good | 231 (0 poor) |
| HTTPS | 237 (0 non-HTTPS) |
| Product snippets | 344 valid, 0 invalid |
| Merchant listings | 4,243 valid, 3 invalid |
| Breadcrumbs | 269 valid, **32 invalid** |
| Review snippets | 135 valid, 0 invalid |

---

## NOT-INDEXED DIAGNOSIS — 1,594 URLs classified

### 554 "Not found (404)" — TWO distinct causes

Cross-referenced sampled URLs against live Shopify:

| Sample handle | Shopify | Cause |
|---|---|---|
| `ch154`, `ch49`, `ch146`, `ch7` | **does not exist** | deleted or handle-renamed |
| `hamper26`, `addon-ferrero-rocher-24-pcs`, `any-day-treat-…-hamper` | **DRAFT** | exists, unpublished → storefront 404 |
| `ch10`, `ch101`, `ch103`, `ch107`, `hamper1`, `hamper10`, `b1`, `b10` | **DRAFT** | same |
| `b100`, `b157` | **ACTIVE** | fine |

Drafts are the dominant cause. A redirect cannot fix a draft product.

### 1,040 "Crawled — currently not indexed" — NOT products

Zero product URLs in the sample. Composition:

- CDN JS assets: `/cdn/shop/t/21/assets/{vendor,global,day,importmap,es-photoswipe}.min.js?v=…`
- Collection `.atom` feeds: `/collections/wedding-cakes.atom`, `/collections/cake-hampers.atom`
- Collection pagination: `/collections/cake-hampers?page=5`
- `/llms.txt`

**The rewritten product descriptions will NOT reduce this number.** Verified before assuming.

### 9 "Blocked by robots.txt" — all legitimate
`/cart/add`, `/account`, `/search/suggest`, `/policies/*`, `/customer_authentication/redirect`.
No action needed.

---

## ⚠️ P0 — RETRACTED. DO NOT BULK-PUBLISH DRAFTS

Earlier guidance said "publish the 584 drafts — costs nothing." **That was wrong.**

Sampled 50 draft products. **All 50** had:

- `featuredImage: null` — no image
- `totalInventory: 0` — no stock
- bare-numeric handles (`5`, `28`, `29`, `38`, `42` …)

These are placeholder/junk records, not sellable products. Publishing them would create
hundreds of thin, imageless, zero-stock pages, be rejected by Merchant Center
(`image_link` is required), and look broken to customers.

**Revised action:** publish only a *curated, verified* subset with images and stock. Requires
owner selection. The corresponding 404s should mostly remain 404/410 — that content is not lost,
it never existed.

---

## ⚠️ P1 — 2 OF 3 PROPOSED ROBOTS.TXT RULES RETRACTED AS UNSAFE

Re-verified each rule against the live site before execution.

| Proposed rule | Verdict | Reason |
|---|---|---|
| `Disallow: /*.atom$` | SAFE but low value | `.atom` feeds are not intended to rank. Benefit is cosmetic — cleans a GSC report, does not affect rankings. |
| `Disallow: /*?page=` | **UNSAFE — RETRACTED** | Collection pagination is how Googlebot discovers products beyond page 1. With 35 collections and 607 active products, blocking it risks orphaning deep products and breaking GMC landing-page crawling. |
| `Disallow: /cdn/shop/t/*/assets/` | **UNSAFE — RETRACTED** | Blocks **CSS and JavaScript**. Google requires access to these to render pages; blocking degrades indexing and Core Web Vitals assessment. Directly contradicts Google's own guidance. |

**Also relevant:** `templates/robots.txt.liquid` does **not** exist in the theme — robots.txt is
Shopify's default. Any rule change requires creating that file (reversible by deleting it).

**Decision: P1 NOT EXECUTED.** The only safe rule is cosmetic; the cost of introducing a
robots.txt override for it is not justified.

---

## P5 — MERCHANT CENTER FEED: EARLIER CLAIM CORRECTED

An earlier note in this session stated "there is no Shopify feed reaching Merchant Center."
**That was an over-claim.** Verified state:

| Check | Result |
|---|---|
| Google & YouTube publication exists in Shopify | ✅ `gid://shopify/Publication/136327889065` |
| Products published to that channel | ✅ **YES** — `classy-tuxedo-husband-birthday-cake-meerut`, `romantic-whisper-wedding-cake-meerut` both `isPublished: true` |
| Products NOT published to that channel | `b157` — Online Store + POS only |
| MC account 5552376763 primary sources | **1: "Local Feed Partnership", 0 products, never updated** |
| MC managed product count | **0** |
| MC "Found by Google" | 4.14k auto-crawled products, 2k organic clicks/30 days, **not ad-eligible** |

**Accurate conclusion:** products *are* published to the Google & YouTube channel in Shopify,
but Merchant Center account `5552376763` shows **zero managed products and no Shopify data
source**. This is a **disconnect between the channel and this MC account**, not an absent feed.

Possible causes, none yet confirmed — **do not change feed architecture until resolved**:
1. The Google & YouTube channel is linked to a *different* Merchant Center account
2. Sync is broken or pending
3. Channel-sourced products surface differently in the MC data-sources UI

Note: 4.14k auto-discovered products vs 1,235 actual products suggests variant-level URLs or a
stale crawl — worth confirming.

---

## ACTIONS TAKEN THIS SESSION

**Read-only throughout. No Shopify write, no redirect, no robots.txt change, no MC change,
no GSC validation submitted.**

| # | Action | Type |
|---|---|---|
| 1 | Restored Google access via correct Chrome account | Config (user-performed) |
| 2 | Verified P4 import against live Shopify | Read |
| 3 | Classified 554 404s + 1,040 crawled-not-indexed | Read |
| 4 | Retracted P0 and 2 of 3 P1 rules on safety grounds | Analysis |
| 5 | Corrected the P5 feed claim | Analysis |
| 6 | Created `.claude/settings.json` with read-only permissions + deny list for Shopify writes | Config |

**Known side effect:** an earlier navigation in this session used a Google `/accounts/Logout`
URL, which signed both Chrome Google accounts out. Recovered by user re-authentication.

---

## NEXT ACTIONS — REVISED PRIORITY

| P | Action | Blocker |
|---|---|---|
| **P0-rev** | Fix the malformed `lotus-biscoffStrawberry Vanila` option value in Admin, then regenerate `ch241` copy | None — small, safe |
| **P1-rev** | Resolve the Google & YouTube ↔ MC `5552376763` disconnect | Needs MC/channel investigation |
| **P2-rev** | Curated publish of draft products **that have images and stock** | Owner selection required |
| **P3-rev** | 404 triage: separate deleted-with-backlinks from junk-handle placeholders | Needs backlink/traffic data |
| **P4-rev** | Re-run GSC validation **after** the above | Sequencing |
| **P5-rev** | Investigate 32 invalid breadcrumbs (structured data) | None — safe to start |

---

# PHASE 14 — G&Y → MERCHANT CENTER DISCONNECT: ROOT CAUSE FOUND (2026-07-19)

**Method:** READ-ONLY. Four independent surfaces cross-checked. Nothing modified.

## VERIFIED CONNECTION MAP

```
Shopify Store  ae86ba-2a.myshopify.com  (thebakingkaur.com)
    │
    ├─► Google & YouTube channel ......... INSTALLED, status "Active"        ✅
    │       products published to channel . VERIFIED on sampled products     ✅
    │
    ├─► Google Account (OAuth) ........... thebakingkaur@gmail.com           ✅ CORRECT
    │
    ├─► Merchant Center account .......... 5552376763                        ✅ CORRECT
    │       confirmed from BOTH ends:
    │         · Shopify Settings → "Google Merchant Center 5552376763"
    │         · MC → Apps and services → "Shopify  ae86ba-2a.myshopify.com"
    │
    ├─► Product sync toggle .............. ON                                ✅
    │
    └─► PRODUCTS SUBMITTED ............... 0                          ❌ ◄── BREAK POINT
            Shopify channel dashboard: Total 0 · Approved 0 · Limited 0
                                       Not Approved 0 · Under Review 0
```

## ROOT CAUSE

**The channel is fully and correctly connected, product sync is ON, and yet zero products have
ever been submitted. The only Google integration actually operating is Local Inventory (LIA),
which is stuck at "Pending".**

Evidence — all four surfaces agree:

| Surface | Evidence |
|---|---|
| Shopify channel Overview | GMC "Active"; **Total 0 / Approved 0 / Limited 0 / Not Approved 0 / Under Review 0**; "Local inventory: **Pending** — may take 3–5 business days for approval" |
| Shopify channel Settings | Google account `thebakingkaur@gmail.com`; MC `5552376763`; **Product sync: On**; "Additional settings to sync with GMC (3)" collapsed |
| MC → Data sources | Primary sources: **1 — "Local Feed Partnership", 0 products, last updated "—"**. No Shopify/Content-API product source. |
| MC → API diagnostics (30d) | **102 calls, 0 failed.** Methods: `accounts.get` (41), `liasettings.get` (30), `liasettings.getaccessiblegmbaccounts` (31). **ZERO `products.*` calls.** |

`liasettings` = Local Inventory Ads settings. The entire API footprint is account + local-inventory
polling. **Nothing has ever pushed an online product feed.** This is not a broken sync — it is a
sync that was never established.

## ANSWERS TO THE 12 INVESTIGATION POINTS

| # | Question | Finding |
|---|---|---|
| 1 | MC account the G&Y channel connects to | **5552376763** |
| 2 | Is 5552376763 the linked account? | **Yes** — confirmed from both ends |
| 3 | Another MC account / sub-account? | **No.** Single account; account switcher shows only "The Baking Kaur 5552376763" |
| 4 | G&Y channel connection status | **Active**, healthy |
| 5 | Google/OAuth identity | **thebakingkaur@gmail.com** — correct account |
| 6 | MC data sources | 1 primary: "Local Feed Partnership", 0 products, never updated |
| 7 | Product sync status / last sync | Toggle **On**; **0 products submitted; no last-sync timestamp exists** |
| 8 | Pending / failed sync | **0 failed API calls.** Local inventory **Pending**. No product sync ever attempted. |
| 9 | Product eligibility / approval | All counters 0 — nothing submitted, so nothing to approve |
| 10 | Products under a different MC resource/source type? | **No.** Zero `products.*` API calls confirms no alternate push path |
| 11 | Are the 4.14k auto-discovered products crawled, not fed? | **Yes — website-crawled.** MC labels them "Found by Google … They won't be included in ads automatically". 4.14k ≫ 1,235 products, consistent with variant/paginated URL crawling |
| 12 | Duplicate / stale / legacy feed architecture? | **Yes — see below** |

## STALE / DUPLICATE LINKS FOUND (not the cause, but should be reviewed)

MC → Apps and services lists **7 linked services**:

| Service | Detail | Note |
|---|---|---|
| Shopify | `ae86ba-2a.myshopify.com` | ✅ correct, current |
| Simprosys | — | ⚠️ **linked in MC, but the app is NOT installed in Shopify** (Shopify Apps shows only "OTP Login & Notify"). Orphaned legacy link. Not pushing — zero `products.*` calls. |
| Google Ads | 758-779-6693 | ⚠️ two Ads accounts linked |
| Google Ads | 861-415-9595 "The Baking Kaur Google Ads account" | ⚠️ duplicate/legacy? |
| Google Analytics | 454136195 | ok |
| Google Business Profile | Thapar Nagar, Meerut listing | ok |
| Google Business Profile | thebakingkaur@gmail.com | ⚠️ two GBP entries |

**Correction to an earlier note in this ledger:** a previous entry stated "no third-party feed
apps present." That was derived from Shopify *publications*, which is the wrong surface —
Simprosys integrates via Content API, not as a sales channel. The correct statement is: Simprosys
**is** linked in Merchant Center but is **not installed in Shopify** and is **not** pushing data.

## PROPOSED FIX — NOT EXECUTED, USER ACTION REQUIRED

The break is a configuration gap, not a broken connection. Nothing needs disconnecting or
recreating. **Do not disconnect Google & YouTube, do not touch Simprosys yet, do not create a
new MC account.**

**Step 1 — expand "Additional settings to sync with Google Merchant Center (3)"**
Shopify admin → Google & YouTube → Settings → Product feed. The description states these settings
derive from *Shopify markets, published languages, and shipping profiles*. A missing target market
or shipping profile is the most probable gate on a sync that is toggled On but has submitted 0
products. This is read-only inspection and safe.

**Step 2 — resolve the Local inventory "Pending" state**
The entire API footprint is `liasettings`. If LIA onboarding is gating the channel, completing or
disabling it should release the online product feed.

**Step 3 — only then allow the online product feed to populate**
Expect ~607 active products to submit. Note: ~12 active products have **no image**; Merchant
Center requires `image_link`, so those will be disapproved. That is a small, expected,
self-correcting backlog — not a reason to delay.

**Step 4 — after the feed is live, review the orphaned Simprosys link and duplicate Ads/GBP
entries.** Do not remove them before the feed is confirmed working; if Simprosys ever resumes,
two sources pushing to one account would create conflicts.

## RISK ASSESSMENT

| Item | Risk | Reversible |
|---|---|---|
| Inspecting additional sync settings | **None** — read-only | n/a |
| Completing/disabling LIA onboarding | **Low** | Yes |
| Allowing the product feed to populate | **Low–Medium** — outward-facing; 607 products become Shopping-eligible | Yes — product sync can be toggled Off |
| Removing the orphaned Simprosys link | **Medium** — do **not** do this before the feed works | Reversible but requires re-auth |

**Product IDs, account history and existing Shopping eligibility are not at risk** in any of the
above. There is currently no product data in MC to lose.

## SEPARATE ITEM — LOGGED FOR SURGICAL CORRECTION

**`ch241` malformed flavour string.** ACTIVE product, customer-visible, reads:
*"a choice of Lotus Biscoffstrawberry Vanilla, …"*. Source cause: the Shopify variant option value
`lotus-biscoffStrawberry Vanila` is two values concatenated. Fix at source in Admin (rename the
option value), then regenerate that single product's description. **Do not bulk-regenerate.**

## ACTIONS TAKEN THIS PHASE

**READ-ONLY. Zero modifications.** No disconnection, no MC settings change, no feed creation,
no OAuth re-auth, no product change, no robots.txt change, no draft publishing.

---

# PHASE 15 — EXACT BLOCKER IDENTIFIED: NO SHIPPING RATES CONFIGURED (2026-07-19)

**Method:** READ-ONLY. Shopify Admin GraphQL API (the embedded Google & YouTube app iframe
repeatedly froze the browser renderer and could not be expanded — the API provided the same
underlying configuration more reliably).

## THE BLOCKER

**Shopify has ZERO shipping rates configured. Not one zone, not one rate, not one country.**

Measured from `deliveryProfiles`:

| Field | General profile (default) | Fresh Cakes – Local Delivery |
|---|---:|---:|
| `activeMethodDefinitionsCount` | **0** | **0** |
| `zoneCountryCount` | **0** | **0** |
| `originLocationCount` | **0** | **0** |
| `locationsWithoutRatesCount` | **2** | **2** |
| `locationGroupZones` | **empty** | **empty** |

Both delivery profiles exist by name but contain no zones, no rates, and no origin locations.

## WHY THIS BLOCKS THE FEED

Google Merchant Center **requires shipping information** before a product is eligible for free
listings or Shopping ads. The Shopify Google & YouTube app derives Merchant Center shipping
settings from Shopify's shipping profiles — the app's own Settings copy states the product feed
settings are *"based on your Shopify markets, published languages, and **shipping profiles**."*

With zero zones and zero rates, the app cannot construct a valid shipping configuration, so no
product can be submitted. This reconciles every observation:

| Observation | Explained |
|---|---|
| Product sync toggle **On** | Correct — the toggle is not the problem |
| MC account link correct | Correct — not the problem |
| OAuth identity correct | Correct — not the problem |
| Products published to the channel | Correct — not the problem |
| **Total 0 / Approved 0 / Not Approved 0** | Nothing submitted, because shipping config is empty |
| Content API: zero `products.*` calls | Consistent — no submission ever attempted |
| MC data source: "Local Feed Partnership", 0 products | Only the local/LIA path was ever configured |

## SUPPORTING CONFIGURATION (verified, all correct)

| Setting | Value | Status |
|---|---|---|
| Market | **India** — `enabled: true`, `primary: true` | ✅ correct |
| Market web presence | `webPresence: null` | ⚠️ worth review, not the blocker |
| Google account (OAuth) | `thebakingkaur@gmail.com` | ✅ correct |
| Merchant Center account | `5552376763` | ✅ correct |
| Product sync | **On** | ✅ correct |
| Shipping rates | **NONE** | ❌ **BLOCKER** |
| Local inventory (LIA) | **Pending** | ⚠️ secondary |

## HONEST LIMITATION

The three collapsed "Additional settings to sync with Google Merchant Center" could **not** be
opened — the embedded app iframe froze the browser renderer on every attempt (CDP screenshot
timeouts). The shipping finding comes from the Shopify Admin API rather than from an explicit
in-app error message.

**Confidence: high but not absolute.** The evidence is strong and convergent — Merchant Center
requires shipping, Shopify has literally none, and the app names shipping profiles as a feed
input. But no in-app message was observed that says verbatim "configure shipping to continue".
If shipping is configured and products still do not submit, the remaining candidates are the
market `webPresence: null` and the LIA Pending state.

## NOTE — 15 ORDERS EXIST DESPITE ZERO SHIPPING RATES

The store shows 15 orders in admin. With no shipping rates configured, standard Shopify checkout
would normally block. Delivery is likely arranged manually or through an app. **This is a
business-operations question for the owner, not an SEO finding** — flagged because configuring
shipping rates may change the live checkout experience and must be done deliberately.

## SAFE FIX — NOT EXECUTED, OWNER ACTION REQUIRED

**Where:** Shopify Admin → Settings → Shipping and delivery → General profile

**Action:** create at least one shipping zone containing **India** with at least one rate.

**Why the owner and not the agent:** this changes the **live checkout experience** for real
customers. It is a pricing and fulfilment decision, not a technical repair. It is outward-facing
and commercially material.

**Risk:** LOW technically, MEDIUM commercially — a wrong rate charges customers incorrectly.
Fully reversible (rates can be edited or removed).

## EXPECTED SEQUENCE AFTER THE FIX

1. Shopify Google & YouTube app picks up the shipping configuration (minutes to hours)
2. Product sync begins submitting the **607 active** products
3. `products.*` calls appear in MC → API diagnostics — currently **zero**
4. MC → Data sources gains a Shopify/Content-API product source alongside "Local Feed Partnership"
5. Shopify channel Overview counters move off zero into "Under Review"
6. Google review takes ~3–5 business days; products then move to Approved / Limited / Not Approved
7. ~12 active products with no image will be **disapproved** (`image_link` required) — expected and small

## VERIFICATION CHECKLIST (all read-only)

| # | Check | Where | Currently | Expect after fix |
|---|---|---|---|---|
| 1 | Shipping zones exist | `deliveryProfiles.zoneCountryCount` | **0** | ≥1 |
| 2 | Active rate methods | `deliveryProfiles.activeMethodDefinitionsCount` | **0** | ≥1 |
| 3 | Products submitted | Shopify → Google & YouTube → Overview | **Total 0** | ~607 |
| 4 | Product API activity | MC → API diagnostics | **zero `products.*`** | `products.insert` / `custombatch` present |
| 5 | Product data source | MC → Data sources | only "Local Feed Partnership" (0) | Shopify source with product count |
| 6 | Approval status | MC → Products | 0 | Approved / Limited / Not Approved populated |

## ACTIONS TAKEN THIS PHASE

**READ-ONLY. Zero modifications.** No shipping change, no disconnection, no MC change, no feed
creation, no LIA change, no Simprosys removal, no product modification.

---

# PHASE 16 — DELIVERY & CHECKOUT ARCHITECTURE (2026-07-19)

**Method:** READ-ONLY, Shopify Admin API. Nothing modified.

## ⚠️ CORRECTION TO PHASE 15

Phase 15 recommended *"create a shipping zone containing **India** with at least one rate."*
**That recommendation is withdrawn.** It would create a false India-wide delivery promise for a
catalogue that is **97.7% perishable fresh cakes** deliverable only in Meerut. See below.

## HOW CHECKOUT CURRENTLY WORKS

| Component | State |
|---|---|
| Locations | **1** — "The Baking Kaur", Meerut 250002, active, fulfils online orders |
| Local **pickup** | ✅ **ENABLED** — `pickupTime: FOUR_HOURS` |
| Local **delivery** | ❌ not configured (lives in delivery-profile zones, which are empty) |
| Shipping rates | ❌ **none** — 0 zones, 0 rates, 0 origin locations |
| Carrier services (app-provided rates) | ❌ **none** — `carrierServices` returns empty |
| Delivery apps | ❌ none — Shopify Apps lists only "OTP Login & Notify" |
| Checkout scripts | Not observable via this API scope (Basic plan has no Scripts) |

**Conclusion: local pickup is currently the ONLY checkout path that can complete.** Any customer
selecting delivery cannot check out. This is a **live revenue blocker**, independent of SEO.

## HOW THE 15 ORDERS COMPLETED — RATES EXISTED AND WERE REMOVED

Every historical order carries `shippingLine.source: "shopify"` — these were **native Shopify
rates**, not app-generated. Rate names evolved over time:

| Period | Rate name | Price |
|---|---|---|
| Aug 2024 | "12:00 PM To 4:00 PM" | ₹0 |
| Oct 2024 – Feb 2026 | "Delivery Charge" | ₹100 |
| Sep 2025 | "Standard 1 Cake Delivery Rate" | ₹100 |
| Dec 2025 – Jul 2026 | "The Baking Kaur" | ₹0 |

The most recent order **#1023 (2026-07-07)** used rate "The Baking Kaur". Delivery profiles now
report zero rates.

**Therefore the shipping rates were deleted between 2026-07-07 and 2026-07-19** — within roughly
the last twelve days. This is very likely an accidental deletion during recent store work, and it
is the direct cause of both the broken delivery checkout and the Merchant Center feed blocker.

## ORDER GEOGRAPHY — EVIDENCE THE SERVICE AREA IS MEERUT

| Destination | Orders | Fulfilment outcome |
|---|---|---|
| Meerut (250001/250002) | 9 | 3 FULFILLED, rest ON_HOLD |
| New Delhi | 2 | 1 FULFILLED, 1 UNFULFILLED |
| Bangalore | 1 | **ON_HOLD — never fulfilled** |
| Gandhidham, Gujarat | 1 | **ON_HOLD — never fulfilled** |
| No address | 1 | UNFULFILLED |

Distant orders were accepted but **not fulfilled**. This corroborates that fresh cakes are not
deliverable outside the local area.

Data-quality note: order #1016 has city "meerut" with ZIP **201301** (that is Noida, not Meerut —
Meerut is 250xxx). Customer-entered error; relevant if postcode-based delivery zones are used.

## CATALOGUE SHIPPABILITY — 607 ACTIVE PRODUCTS

| Class | Count | % | Segments |
|---|---:|---:|---|
| **Perishable — local delivery only** | **593** | **97.7%** | birthday 274, anniversary 170, wedding 110, cake 20, designer 13, theme 4, kunafa 1, custom 1 |
| **Potentially shippable** | **13** | 2.1% | non-food add-ons 10, balloons 3 |
| Needs review | 1 | 0.2% | unclassified |

**This is a local bakery, not a national e-commerce catalogue.** Any architecture must reflect that.

## SAFEST ARCHITECTURE (recommendation — NOT executed)

### 1. Shopify customer checkout
- Restore **local delivery** on the Meerut location, scoped by postcode list (250001, 250002, …)
  or delivery radius — **not** a national shipping zone
- Keep **local pickup** enabled (already configured, 4-hour)
- Optionally add a genuine shipping zone covering **only** the 13 shippable non-perishables

### 2. Meerut local delivery
- Shopify native **Local delivery** per location, with the delivery fee that matches the real
  charge (historically ₹100, most recently ₹0)
- Postcode list is safer than radius here, given the 201301 data-entry case

### 3. Google Merchant Center shipping eligibility — without a false promise
Three options, in order of accuracy:

| Option | Accuracy | Note |
|---|---|---|
| **A. MC shipping service scoped to Meerut postal codes** | ✅ accurate | Represents the true service area. Products show as deliverable only where they truly are. |
| **B. Local Inventory Ads / local surfaces only** | ✅ accurate | Best fit for a local bakery. GBP already linked. LIA already "Pending". |
| **C. India-wide shipping zone** | ❌ **inaccurate — do not use** | Promises Bangalore delivery of fresh cakes. Bangalore/Gujarat orders were never fulfilled. Risks MC misrepresentation policy and customer harm. |

**Recommended: B as primary, A for the online feed.**

⚠️ **Unverified integration nuance:** Shopify's Google & YouTube app syncs MC shipping from
Shopify **shipping profiles**. Shopify **local delivery is a distinct mechanism from shipping
rates**, and it is not confirmed that the app translates local delivery into MC shipping settings.
If it does not, MC shipping may need configuring directly in Merchant Center (option A) rather
than relying on the Shopify sync. **This needs verification before relying on it.**

### 4. Local Inventory / free listings
- The **Local Feed Partnership** data source and LIA "Pending" state already exist — this is the
  correct architecture for this business and is half-built
- Google Business Profile is already linked (Thapar Nagar, Meerut)
- Completing LIA is likely higher-value than online Shopping for 97.7% of the catalogue
- Free listings currently already generate ~2k organic clicks/30 days via Google's automatic crawl

## PRIORITY REORDERING

| P | Action | Rationale |
|---|---|---|
| **P0** | **Restore delivery rates / local delivery** | Live revenue blocker — only pickup works today |
| P1 | Complete Local Inventory (LIA) setup | Correct primary channel for a local bakery |
| P2 | Configure MC shipping scoped to Meerut (option A) | Accurate online eligibility |
| P3 | Separate the 13 shippable products into their own profile | Enables genuine wider reach without false promises |

## ACTIONS TAKEN THIS PHASE

**READ-ONLY. Zero modifications.** No shipping change, no delivery change, no checkout change,
no MC change, no product change.

---

# PHASE 17 — DELIVERY/GMC ARCHITECTURE VERIFIED + CRITICAL CONTENT DEFECT (2026-07-19)

**Method:** READ-ONLY. Shopify Admin API + official Google/Shopify documentation. Nothing modified.

## 🔴 P0 CRITICAL — LIVE CONTENT DEFECT INTRODUCED BY THE PHASE-13 CATALOGUE RUN

**143 products describe cakes as "not a food product". 13 are ACTIVE and customer-visible now.**

| Handle | Price | Title | Live text |
|---|---|---|---|
| `ch249` | ₹4,800 | **Candlelight Wedding Cake** | "This is a non-edible celebration item and is not a food product." / "Is this a food item? **No.**" |
| `b75`, `b76`, `b77`, `b78`, `b81`, `b82`, `b83`, `b176` | ₹1,700 | Teddy … **Cake** (8 products) | same |
| `teddy-rainbow-theme-cake-meerut` | ₹3,100 | Teddy Rainbow Theme **Cake** | same |
| `hamper13`, `hamper14`, `hamper23` | ₹3,500 | Cake + Flower + Balloon combos | same |

Plus **130 draft** products with the same defect (segment BALLOON).

**Cause — this is a defect in the corrected-run content generator, not pre-existing store data.**
The segmentation classifier tested non-food patterns (`\bteddy`, `\bcandle`, `\bballoon`) *before*
any food test, and matched them inside titles that are actually cakes ("Teddy Love **Cake**",
"**Candlelight** Wedding **Cake**", "Cake Flowers **Balloon** Gift Box"). The non-food branch then
asserted the item is not food.

**Severity: HIGH.** A ₹4,800 wedding cake is publicly described as non-edible. For a food business
this is factually wrong, commercially damaging, and a potential consumer-information problem.

**Fix (surgical, not executed):** add a guard so any title containing a food noun
(`cake|brownie|cookie|kunafa|cupcake|hamper|chocolate`) can never be classified non-food; then
regenerate **only** these 143 descriptions. Do not bulk-regenerate the catalogue.

**This also invalidates the earlier "13 potentially shippable products" claim.** All 13 are cakes
or cake combos. **Zero of the 607 active products are shippable.** The catalogue is 100%
perishable, Meerut-local.

## VERIFIED ANSWERS TO THE 10 QUESTIONS

### 1. Current Local Delivery configuration
**None.** Both delivery profiles return zero zones and zero method definitions:

| Profile | Zones | Method definitions | Location |
|---|---|---|---|
| General profile (default) | **0** | **0** | The Baking Kaur, Meerut 250002 |
| Fresh Cakes – Local Delivery (custom) | **0** | **0** | same |

No radius, no postcode list, no local delivery method. The "Fresh Cakes – Local Delivery" profile
exists **by name only** and is empty.

### 2. Why delivery checkout is unavailable; is pickup the only method?
- Shipping rates: **none**
- Local delivery: **not configured**
- Carrier services (app-supplied rates): **none** (`carrierServices` empty)
- Local **pickup**: ✅ **configured** — `pickupTime: FOUR_HOURS`

**Yes — local pickup is currently the only checkout method that can complete.** Delivery customers
cannot check out. Live revenue blocker.

### 3. Will restoring local delivery affect existing workflows?
- **Existing/manual/draft orders:** no effect — historical orders are immutable
- **COD:** unaffected — payment method is independent of delivery method
- **WhatsApp / phone orders:** unaffected — they bypass Shopify checkout
- **Online checkout:** **will change** — delivery becomes selectable again alongside pickup
- **Risk:** if a rate is set wrongly, customers are charged wrongly. Reversible.

### 4. Can MC online listings use the genuine Meerut area without an India-wide promise?
**Yes.** Google documents two methods for Shopify merchants: import shipping from Shopify, **or**
*"set your shipping rates manually in Google Merchant Center… set your shipping settings to manual
in your Google sales channel"* — described as suited to *"advanced or customized shipping settings"*.
Manual MC shipping can be scoped to the real service area.

### 5. Should MC shipping be configured directly instead?
**Yes — recommended.** Two documented constraints make the Shopify auto-import unsuitable here:

> *"Only shipping rates in your **General** shipping profile can sync to Google Merchant Center.
> If you use custom shipping profiles, then rates will sync incorrectly … and cause errors."*

The intended setup ("Fresh Cakes – Local Delivery") is a **custom** profile — it would sync
incorrectly. And auto-import is organised at **country level**, which cannot express "Meerut only"
without over-promising. **Manual MC shipping is the accurate route.**

⚠️ **Still unconfirmed:** Google's doc does **not** explicitly state whether Shopify Local Delivery
alone satisfies MC shipping requirements without zone-based rates. It says only that pickup and
local delivery "can be set up". **Do not assume local delivery alone will unblock the feed.**

### 6. Requirements to complete the Pending Local Inventory (LIA) setup
Per Google's documentation:

| Requirement | Current state |
|---|---|
| Physical retail location | ✅ Meerut 250002 |
| POS inventory with per-location quantities | ⚠️ needs verification |
| **More than 10 products with APPROVED status** | ❌ **0 approved** — nothing submitted |
| Google & YouTube onboarding complete, MC linked | ✅ done |
| Verified Google Business Profile | ✅ linked |
| **Same address in GBP and Shopify** | ⚠️ see #7 |

**Critical dependency chain — LIA is blocked *behind* product sync, not the cause of it:**
`shipping configured → products sync → >10 approved → LIA can complete`
This corrects the earlier hypothesis that LIA Pending was gating the online feed. It is downstream.

### 7. Is GBP correctly matched to Merchant Center?
Google requires *"the same address in both Google Business Profile and your Shopify."*

| Source | Address |
|---|---|
| Shopify location | Fateh Complex, 390/1, Lane Number 7, opposite Ice Factory, Thapar Nagar Gali Number 7 Lajpat Bazaar, Meerut, Uttar Pradesh, **250002** |
| GBP (as shown in MC) | Fateh Complex 390/1, Opposite Ice Factory, Near Hemkund Car Accessories Lane Number 7, Thapar Nagar, Meerut, Uttar Pradesh |

**Substantively the same premises.** Formatting differs and the GBP entry shows no postcode in the
MC display. **Verify the GBP postcode is 250002** before LIA setup — an address mismatch is a
documented LIA failure cause. Note also **two GBP entries** are linked to MC; confirm which is
authoritative.

### 8 & 9. Which products participate — CORRECTED
| Group | Count | Products |
|---|---:|---|
| **A. Local Inventory / local free listings** | **607** | all active products — perishable, Meerut-local |
| **B. Online free listings with Meerut-scoped delivery** | **607** | same set, via manual MC shipping scoped to Meerut |
| **C. Neither** | 628 | draft/archived — not sellable (no image, no stock) |
| **Genuinely shippable outside Meerut** | **0** | previous "13" were misclassified cakes |

### 10. Safest configuration
See execution order below.

## RECOMMENDED ARCHITECTURE — EXECUTION ORDER

| Step | Action | Where | Risk | Who |
|---:|---|---|---|---|
| **1** | Fix the 143 non-food descriptions (13 active first) | Shopify products | Low | Agent, on approval |
| **2** | Restore delivery so checkout works — local delivery on the Meerut location, postcode-scoped (250001, 250002…), plus keep pickup | Settings → Shipping and delivery | Low tech / **Medium commercial** | **Owner** |
| **3** | Add a real rate in the **General** profile covering the served area — required for any Shopify→MC sync, and Google ignores custom profiles | Settings → Shipping and delivery → General | Medium | **Owner** |
| **4** | Set Google channel shipping to **manual**, then configure MC shipping scoped to Meerut postal codes | Google & YouTube app → MC | Low | **Owner** |
| **5** | Verify product sync starts — `products.*` calls appear; counters leave zero | MC API diagnostics | None | Agent (read-only) |
| **6** | After >10 products are APPROVED, complete LIA | Google & YouTube app | Low | **Owner** |
| **7** | Confirm GBP postcode = 250002 and resolve the duplicate GBP link | GBP / MC | Low | **Owner** |
| **8** | Fix the `lotus-biscoffStrawberry Vanila` option value, regenerate `ch241` | Shopify Admin | Low | **Owner** then agent |

**Never do:** create an India-wide shipping zone to satisfy Merchant Center. Bangalore and Gujarat
orders were accepted and **never fulfilled** — that is the evidence. A national promise on
perishable cakes would be false and risks MC misrepresentation policy.

## ACTIONS TAKEN THIS PHASE
**READ-ONLY. Zero modifications.** No shipping, delivery, MC, LIA, GBP or product change.

---

# PHASE 18 — STEP 1 EXECUTED: NON-FOOD DEFECT FIXED ON 13 ACTIVE PRODUCTS (2026-07-19)

**First write operation of this engagement.** Approved scope: option B — 13 × `descriptionHtml`
+ 10 × `SEO Description`. Permission: `graphql_mutation` removed from the `deny` list in
`.claude/settings.json` on explicit owner instruction.

## RESULT: ✅ 13/13 SUCCESSFUL — all protected fields intact

## ⚠️ INCIDENT DURING EXECUTION — SEO TITLE WIPED, THEN RESTORED

**What happened.** `ProductInput.seo` is an **object, not a patch**. Supplying
`seo: { description }` without `title` replaced the entire SEO object and set
`seo.title` to `null` on the 10 products that received a meta update.

**Detected by:** the mandated post-write regression re-fetch. Not by the mutation itself —
all 13 returned `userErrors: []`.

**Scope:** 10 products (`b75 b76 b77 b78 b81 b82 b83 b176 ch249 teddy-rainbow-theme-cake-meerut`).
The 3 hampers sent body-only were unaffected, which isolated the mechanism precisely.

**Impact while broken:** Shopify falls back to the product title for `<title>`, so pages were not
broken, but 10 crafted local-intent titles ("… in Meerut | The Baking Kaur") were lost. Duration
approximately one verification cycle.

**Restored:** 10/10 via a second mutation sending `seo.title` **and** `seo.description` together,
using the exact values captured in `STEP1_LIVE_PRESTATE.md`. `userErrors: []` on all 10.

**Root cause of the mistake:** an incorrect assurance given before execution — that
`productUpdate` "modifies only the fields present in the input". True at field level, **false
within the nested `seo` object**. Verified pre-state capture is what made recovery exact.

**Rule for all future writes:** when updating any nested input object (`seo`, and by extension
similar composite inputs), **always send every sub-field**, not only the one being changed.

## FINAL VERIFIED STATE — all 13 re-fetched from live Shopify

| Handle | descriptionHtml | SEO description | SEO title | Protected fields |
|---|---|---|---|---|
| b75 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| b76 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| b77 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| b78 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| b81 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| b82 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| b83 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| b176 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| ch249 | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |
| hamper13 | ✅ fixed | n/a (was correct) | ✅ never touched | ✅ unchanged |
| hamper14 | ✅ fixed | n/a (was correct) | ✅ never touched | ✅ unchanged |
| hamper23 | ✅ fixed | n/a (was correct) | ✅ never touched | ✅ unchanged |
| teddy-rainbow-theme-cake-meerut | ✅ fixed | ✅ fixed | ✅ restored | ✅ unchanged |

## REGRESSION CHECK — protected fields, live vs pre-state

| Field | Result |
|---|---|
| Title | 13/13 identical |
| Handle | 13/13 identical |
| Status (ACTIVE) | 13/13 identical |
| Variant count (24/24/24/24/24/24/24/24/24/1/1/1/16) | 13/13 identical |
| totalInventory (0) | 13/13 identical |
| Featured image URL | 13/13 identical |
| productType | 13/13 identical |
| Tags | 13/13 identical |
| Vendor | 13/13 identical |
| **Prices / SKUs / options / metafields / Google fields / publications** | not in any input — untouched |

## CONTENT VERIFICATION

- Products still saying "not a food product": **0 / 13**
- SEO descriptions containing "add-on": **0 / 13**
- SEO descriptions over 155 chars: **0 / 13**
- SEO fields losing "Meerut": **0 / 13**
- Unbalanced HTML: **0 / 13**

Example — `ch249` (₹4,800 wedding cake), before and after:

> **BEFORE:** "Candlelight Wedding Cake is a celebration add-on … **This is a non-edible
> celebration item and is not a food product.** … Is this a food item? **No.**"
>
> **AFTER:** "Candlelight Wedding Cake is one of our weddings and receptions designs —
> handcrafted, **completely eggless**, made to order. … available in 3 kg, 4 kg and 5 kg with a
> choice of Lotus Biscoff, Vanilla Fresh Fruit … **Is this eggless? Yes.**"

## STILL OUTSTANDING (deliberately not done in this pass)

| Item | Count | Note |
|---|---:|---|
| Draft products with the same non-food defect | **130** | invisible to customers; owner deferred |
| `lotus-biscoffStrawberry Vanila` malformed option value | 1 | needs Admin rename, then regenerate `ch241` |

## ARTEFACTS

`STEP1_LIVE_PRESTATE.md` · `STEP1_ROLLBACK.csv` · `STEP1_PROPOSED_CHANGES.csv` ·
`STEP1_FINAL_CHANGESET.csv/.json` · `STEP1_VARS.json`

**Next: returning to the P0 Merchant Center objective. No further catalogue work.**

---

# PHASE 19 — POSTCODE FIXED + GMC PRE-FLIGHT AUDIT (2026-07-19)

## NAP: Shopify location postcode corrected 250002 -> 250001 ✅

Executed via `locationEdit`. **Schema was checked first** — `LocationEditInput.address` is a
nested object with the same wholesale-replace behaviour as `seo`, so all seven sub-fields
(`address1 address2 city phone zip countryCode provinceCode`) were sent, changing only `zip`.
`userErrors: []`. Re-verified independently: every other field byte-identical, delivery profiles
untouched, local pickup untouched.

**All four NAP surfaces now agree on 250001:** GBP (authoritative, Google-verified) · Shopify
location · Shopify billing · website footer + schema. **LIA address-match blocker cleared.**

## Authoritative GBP: RESOLVED — only ONE exists

GBP Manager: **1 business, 100% verified, shop code GOOBK1**, address matches canonical NAP at
250001, genuine recent 5★ reviews. The earlier "two GBP entries" in Merchant Center were the same
profile surfaced twice. **No duplicate. Nothing to merge or delete.**

## Service area: PROPOSED, AWAITING APPROVAL

Modinagar (`201204`, Ghaziabad district, ~25-30 km via NH-58) makes a radius unworkable.
Separately, **Pallavpuram — already named in the site footer — is `250110`, not `2500xx`**, so
declared coverage was already wider than the city core. **Explicit postcode list is the correct
model.** Tiers A–E proposed in `PROPOSED_SERVICE_AREA.md`. Not configured.

## GMC PRE-FLIGHT AUDIT — 606 active products (read-only)

Run against the approved CSV to predict disapprovals *before* the feed is unblocked.

| Severity | Issue | Count | % |
|---|---|---:|---:|
| **DISAPPROVAL** | `MISSING_IMAGE_LINK` | **11** | 1.8% |
| CRITICAL | `NONFOOD_CLAIM_ON_CAKE` | 13 | **STALE — 0 live**, fixed in Phase 18 |
| WARNING | `PROMOTIONAL_TEXT_IN_TITLE` | 4 | 0.7% |
| INFO | `CONDITION_BLANK` | 606 | defaults to `new`, acceptable |
| INFO | `CUSTOM_PRODUCT_BLANK` | 606 | should be TRUE for made-to-order |
| INFO | `MISSING_PRODUCT_TYPE` | 3 | hamper13/14/23 |

**Clean across all other required attributes:** title, description, price, brand, SKU/id and
`google_product_category` are present on **all 606**. No title-length, description-length,
encoding or capitalisation failures.

### PROJECTED OUTCOME WHEN THE FEED IS UNBLOCKED
```
Will be DISAPPROVED :  11 of 606  ( 1.8%)
Expected APPROVED   : 595 of 606  (98.2%)
LIA requires >10 approved: PASS
```

### The 11 disapprovals — all missing images

`b19 b20 b21 b25 b30 ch225 ch226 ch241 ch246 ch299 ch300`

**9 of 11 are strawberry products** (Strawberry Fresh Fruit, Strawberry Birthday, Chocolate
Strawbeery, London Viral Strawberry, Dubai Viral Kunafa Starberry, Belgian Strawberry Truffle,
Strawberry Truffle Delight, Fresh Strawberry Cream Truffle, Signature Strawberry Truffle) — this
looks like a recently-added product line that was never photographed. Two others (`ch299`,
`ch300`) carry titles ending "The Baking Kaur, Meerut" without a separator.

Note `ch241` appears here **and** carries the malformed `lotus-biscoffStrawberry Vanila` option
value — consistent with the strawberry line being incomplete.

Also note titles `Chocolate Strawbeery` and `Dubai Viral Kunafa Starberry` contain spelling errors
(**Strawbeery**, **Starberry**) — customer-visible, and these are product titles, so not touched.

### 4 promotional-title warnings
`jungle-theme-classic-birthday-cake-meerut` · `jungle-theme-custom-cake-meerut` ·
`designer-wedding-cake-meerut` · `classy-tuxedo-husband-birthday-cake-meerut`
Merchant-authored names containing "best"/"classy". Low risk; not blocking.

### Two feed-level settings worth setting once (not per product)
- `condition = new` — blank on all 606; Google defaults to `new`, so acceptable
- `custom_product = TRUE` — blank on all 606; **should be TRUE** for made-to-order cakes, and
  pairs with `identifier_exists = no`. Best set in the Google & YouTube channel, not the CSV.

**Headline: product data is in good shape. Only 11 items (1.8%) will fail, all for a missing
image. Shipping configuration remains the sole blocker on the feed itself.**

## ACTIONS THIS PHASE
1 write (`locationEdit`, zip only, verified). Everything else read-only.

---

## BACKLOG — PARKED, DO NOT ACTION WITHOUT INSTRUCTION

| # | Item | Detail | Parked |
|---|---|---|---|
| B1 | **130 draft products with non-food defect** | Same classifier bug fixed on the 13 active in Phase 18. Invisible to customers (draft). Fix before any future publish. Change-set already computed in `STEP1_PROPOSED_CHANGES.csv`. | 2026-07-19 |
| B2 | Malformed option value `lotus-biscoffStrawberry Vanila` | Variant key — Admin rename required, then regenerate `ch241` copy | 2026-07-19 |
| B3 | 11 active products missing images | `b19 b20 b21 b25 b30 ch225 ch226 ch241 ch246 ch299 ch300` — will be GMC-disapproved; needs photography | 2026-07-19 |
| B4 | Title spelling errors | "Chocolate Strawbeery", "Dubai Viral Kunafa Starberry" | 2026-07-19 |
| B5 | GBP name keyword-stuffing | `The Baking Kaur \| Premium Bakery... \| Best cakes in meerut` — suspension risk | 2026-07-19 |
| B6 | Website "Fatah" vs canonical "Fateh" | Footer + LocalBusiness schema | 2026-07-19 |
| B7 | Pan-India hamper claim in FAQ schema | Pending owner verification | 2026-07-19 |
| B8 | 32 invalid breadcrumbs (GSC) | Structured data | 2026-07-19 |
| B9 | 554 404s / 1,040 crawled-not-indexed | Post-MC work | 2026-07-19 |

