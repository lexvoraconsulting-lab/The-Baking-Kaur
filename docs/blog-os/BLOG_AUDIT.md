# BLOG_AUDIT.md — Scored audit

Scale 1–10, where **10 = enterprise ideal** and **1 = absent/broken**.
Evidence for every claim is in `CURRENT_STATE.md`.

> **Scope note (v2).** This file scores the **live store**. It is an observation, and it does not
> move because a design document was rewritten — only Phase 0 execution moves it. The separate
> **Design Quality Score** in `DESIGN_REVIEW.md` grades the blueprint. See `DECISION_LOG.md` D-032.

---

## Scorecard

| # | Area | Score | One-line verdict |
|---|---|:---:|---|
| 1 | Blog categories | **1** | One blog, `news`, zero articles, no category system |
| 2 | Topic clusters | **1** | No clusters exist |
| 3 | Cornerstone content | **3** | Cornerstone-grade pages exist but are orphaned and unranked-by-design |
| 4 | Local content | **5** | Good local *copy*, no local *structure*; one city hardcoded everywhere |
| 5 | Commercial content | **8** | Catalogue and collection SEO are genuinely strong |
| 6 | Educational content | **2** | Almost none; two boilerplate Q&As repeated on 602 products |
| 7 | FAQ content | **4** | 43 structured Q&As exist — none rendered; a hardcoded set ships site-wide instead |
| 8 | Thin content | **3** | 4 published pages with empty bodies; 6 finished-title empty drafts |
| 9 | Duplicate intent | **2** | Delivery intent occupies 8+ URLs; hamper intent 6 |
| 10 | Keyword cannibalization | **2** | 5 collections with byte-identical product sets and competing titles |
| 11 | Internal linking | **2** | Zero links in product bodies; 10 published pages unreachable from nav |
| 12 | Orphan content | **2** | Blog itself is orphaned; most published pages are too |
| 13 | Schema | **5** | Good coverage, three structural faults, one site-wide liability |
| 14 | GEO / AI search | **3** | No author entity, no GBP `sameAs`, no citable sourced claims |
| 15 | Trust content | **2** | 0 verified reviews, no FSSAI number, "best bakery" claim unsourced |
| 16 | Conversion content | **6** | Strong PDP copy and WhatsApp CTA; no mid-funnel path into it |

**Weighted architecture score: 33 / 100** (weights and derivation in `FINAL_PHASE1_REPORT.md` §6).

---

## 1. Blog categories — 1/10

One blog (`news`), 0 articles, comments CLOSED. No taxonomy of any kind.

The theme is worse than empty — it is *misconfigured*. `article.json` and `blog.list.json`
sidebars bind to a link list `blog-categories` and to blogs `blog-default` / `list`, **none of
which exist**. `article.json` enables a comments block against a blog with comments disabled.
Three broken bindings shipped from the Ecomus demo and never reconciled.

**Why it scores 1 not 0:** the templates and sections exist and are functional once rebound.

## 2. Topic clusters — 1/10

Nothing to cluster. The nearest thing to a cluster is the hamper page family
(`gift-hampers` → `customised-` / `festive-` / `surprise-hampers-meerut`), which has the *shape*
of a cluster and none of the linking — no hub page links down, no spoke links up.

## 3. Cornerstone content — 3/10

Genuine cornerstone material exists and is well written: `100-percent-eggless-bakery`,
`cake-delivery-in-meerut`, `about-us`, `theme-cakes`, `photo-cakes`.

It scores 3 because **none of it is linked from navigation** and none of it is designated as a
hub. A cornerstone page that nothing links to is a leaf. Additionally
`100-percent-eggless-bakery` is arguably the single most defensible topical asset the brand owns
(100% eggless is a real, verifiable differentiator in a market where "eggless on request" is the
norm) and it is currently unreachable except by search.

## 4. Local content — 5/10

**What is right:** collection SEO descriptions consistently name Meerut; `cake-delivery-meerut`
names actual localities (Civil Lines, Shastri Nagar, Pallavpuram, Modipuram, Garh Road, Sadar
Bazar); `Bakery` schema carries address, geo and `areaServed`.

**What is wrong:**
- Locality names appear **inside one collection description** and nowhere else. There is no
  locality page, no locality article, no locality URL. A query like *"cake delivery in Shastri
  Nagar"* has no landing target.
- The `meerut-delivery` menu exists and is **empty**.
- `store-locator` page body is empty.
- `Bakery.sameAs` omits the Google Business Profile — the primary local entity link.
- Meerut is hardcoded in ~28 collection SEO strings, ~8 page handles, and `areaServed`. Adding a
  second city today means duplicating all of it. See `BLOG_ARCHITECTURE.md` §7.

## 5. Commercial content — 8/10

The strongest area by a wide margin. 602 active products carry consistent
`"{Name} - Eggless | Meerut"` titles, hooked meta descriptions with real price floors and size
counts, descriptive image alt text, and a disciplined seven-heading body template. 28 of 35
collections have hand-written SEO pairs.

Losing 2 points for: identical two-Q&A boilerplate on every product; the
`mm-google-shopping` (2194) vs `mc-facebook` (8271) category disagreement; and no internal links.

## 6. Educational content — 2/10

The only educational content on the entire storefront is the pair of headings
`Is this eggless?` / `Do you deliver in Meerut?` repeated verbatim on ~602 product pages, plus the
`100-percent-eggless-bakery` page.

Nothing exists on: how eggless sponge is made and why it stays moist, cake sizing per guest count,
flavour selection, fondant vs cream, storage and shelf life, transporting a cake in Meerut summer,
lead times by design complexity, allergen handling, how a custom brief becomes a cake.

Every one of those is a real query with real volume and **the studio already has the expertise** —
it is unwritten, not unknown. This is the largest pure-upside gap in the audit.

## 7. FAQ content — 4/10

Three mutually unaware FAQ systems:

1. **43 `shopify--qa-pair` metaobjects** — structured, mostly good, **rendered nowhere**.
2. **A hardcoded `FAQPage` JSON-LD block in `theme.liquid:68`** — inside `<head>`, on every URL.
3. **`/pages/frequently-asked-questions-faqs`** — published, `faq-01` template, **empty body**.

So the store ships FAQ *schema* on 1,300+ URLs while its FAQ *page* is blank and its FAQ *data* is
idle. The schema and the page do not share a single question.

Content defects in the metaobjects requiring an editorial pass before use: `"he Baking Kaur"`
(dropped leading T), `"yes, customers can…"` (lowercase sentence start), `"…special delivery
reques"` (mid-word truncation).

## 8. Thin content — 3/10

- Published with empty bodies: `contact`, `store-locator`,
  `frequently-asked-questions-faqs`, `terms-and-conditions`.
- Unpublished with finished SEO-shaped titles and empty bodies (6): `why-choose-the-baking-kaur`,
  `cake-customization-guide`, `freshness-guarantee`, `delivery-information`,
  `midnight-surprise-delivery`, `corporate-gifting-solutions`.
- `flowers-cake-combos` (**1 product**) and `for-her` (**1 product**) are indexable collection
  pages with hand-written SEO metadata and effectively no inventory. `for-her` is worse than
  thin — it is a *misleading* entry point for a high-intent query.

The six empty drafts matter beyond thinness: they are a **pre-committed content plan** that
overlaps the blog's natural territory. Publishing them as pages and also writing blog posts on
the same topics would manufacture cannibalization from day one. Resolved in
`BLOG_ARCHITECTURE.md` §4.

## 9. Duplicate intent — 2/10

**Delivery intent — 8 URLs:**

| URL | Type | Products |
|---|---|---:|
| `/collections/cake-delivery-meerut` | smart, TYPE~Cake | 985 |
| `/collections/midnight-cake-delivery` | smart, TYPE~Cake | 985 |
| `/collections/midnight-cake-delivery-meerut` | smart, TYPE~Cake | 985 |
| `/collections/same-day-cake-delivery-meerut` | smart, TYPE~Cake | 985 |
| `/collections/cakes` | smart, TYPE~Cake | 985 |
| `/pages/cake-delivery-in-meerut` | page | — |
| `/pages/midnight-cake-delivery` | page | — |
| `/pages/30-minute-cake-delivery-in-meerut-…` | page | — |
| *(+ `/pages/delivery-information`, `/pages/midnight-surprise-delivery` drafted)* | page | — |

**Hamper intent — 6 URLs:** `/collections/cake-hampers`, `/collections/luxury-diwali-hampers`,
`/pages/gift-hampers`, `/pages/customised-hampers-meerut`, `/pages/festive-hampers-meerut`,
`/pages/surprise-hampers-meerut` (+ `/pages/corporate-gifting-solutions` drafted).

**Theme-cake intent — 3 URLs:** `/collections/designer-theme-cakes`,
`/collections/custom-cakes-meerut`, `/pages/theme-cakes` (+ `theme-cake-1` draft).

**Photo-cake intent — 2 URLs:** `/collections/photo-cakes` (4 products), `/pages/photo-cakes`.

**Policy — 2 URLs:** `/pages/refund-return-policy` (live) and
`/pages/return-refund-replacement-policy` (draft).

## 10. Keyword cannibalization — 2/10

The five delivery collections above are not merely similar — they resolve from the **identical
smart rule** `TYPE CONTAINS "Cake"` to the **identical 985 products**. Five URLs, one page of
content, five competing `<title>` tags all containing "Cake … Meerut". Google must pick one; it
will pick unpredictably, and link equity is split five ways.

Compounding:
- `best-selling-products` and `newest-products` carry self-cancelling rules
  (`TITLE CONTAINS x AND TITLE NOT_CONTAINS x`) and therefore both return **all 1,235 products
  including 588 drafts** — two more full-catalogue duplicates of `/collections/all`.
- `showstopper-wedding-cake`: handle says wedding cake, title says "Surprise Cake Setup with
  Revolving Cake", rule selects `TYPE = Wedding Cake`, SEO copy sells surprise setups. It
  cannibalizes `wedding-cakes` while describing something else.
- `wedding-cakes` matches the substring **`wed`**, so its 134 products are not a trustworthy set.

**This is the hard blocker.** A blog layered on top of five identical delivery collections will
add a sixth, seventh and eighth competitor for the same query. Consolidation is a
**prerequisite**, not a parallel workstream — see `BLOG_OS_ROADMAP.md` Phase 0.

## 11. Internal linking — 2/10

- **Zero `<a>` elements in any product description** across 1,235 products. The catalogue is a
  link desert.
- The product page renders `main-product-premium-v2.liquid`, a **protected module** — so
  product→blog links cannot be added without touching it. This is a real architectural
  constraint and it shapes the entire linking blueprint (`INTERNAL_LINKING_BLUEPRINT.md` §3).
- Collection descriptions contain no links either.
- `main-menu` has 4 items and reaches 2 pages. Ten published pages are reachable from no menu.
- Three menus (`explore-cakes`, `quick-links`, `meerut-delivery`) are empty.

## 12. Orphan content — 2/10

Orphaned from navigation: `/blogs/news` itself, plus `100-percent-eggless-bakery`,
`cake-delivery-in-meerut`, `30-minute-cake-delivery-…`, `photo-cakes`, `theme-cakes`,
`gift-hampers`, `midnight-cake-delivery`, `customised-hampers-meerut`, `festive-hampers-meerut`,
`surprise-hampers-meerut`.

Roughly **two-thirds of published pages** are discoverable only via sitemap or search. The blog,
if launched today, would join them.

## 13. Schema — 5/10

**Credit where due:** `Bakery` + `WebSite` + `Organization` + `BreadcrumbList` + `Article` +
collection schema all exist, the breadcrumb correctly branches on `article` page type, `@id`
referencing is used, and **`aggregateRating` is deliberately absent with an in-code prohibition**
explaining why. That last point is better discipline than most stores of this size.

**Four faults:**

| Fault | Location | Effect |
|---|---|---|
| Hardcoded `FAQPage` in `<head>` on **every** URL | `theme.liquid:68` | Same FAQ declared on 1,300+ pages; guaranteed conflict with per-article FAQ schema; structured-data spam exposure |
| `dateModified` = `published_at` | `tbk-schema-article.liquid` | Freshness signal permanently wrong; updated articles look stale |
| `author` = `Organization`, no `Person` anywhere | `tbk-schema-article.liquid` | No E-E-A-T author signal — see §14 |
| Two org-class nodes, unreconciled `sameAs` | `tbk-schema-website` vs `bk-local-business` | `Organization` (`@id` set, IG only) and `Bakery` (no `@id`, IG + FB) are separate nodes describing one business |

Missing: `Blog` / `CollectionPage` on blog index; `ItemList` on collections;
`speakable`; `HowTo` opportunities; `Recipe` (deliberately — see `DECISION_LOG.md` D-011).

## 14. GEO / AI search — 3/10

LLM search engines cite entities they can resolve and claims they can attribute. Current state:

| Signal | Status |
|---|---|
| Named author / `Person` entity | **absent** |
| Google Business Profile in `sameAs` | **absent** |
| FSSAI licence number | **absent** ("FSSAI approved" claimed without one) |
| Verified reviews | **0** (Judge.me installed, empty) |
| Sourced/citable statistics | **none** |
| Q&A-shaped content on-page | 43 metaobjects, **unrendered** |
| Distinctive first-party knowledge | exists offline, unwritten |
| Consistent NAP | good — address/phone/geo present and consistent |
| Crawlable, JS-free content | good |

The brand has the rarest ingredient for GEO — a **verifiable, unusual, first-party fact**
("100% eggless, every product, not on request", across a 1,235-item catalogue). It is stated on
one orphaned page. An LLM asked *"where can I get a fully eggless cake in Meerut?"* has almost
nothing to retrieve and no entity to attribute it to.

## 15. Trust content — 2/10

- 0 verified reviews; 1 `testimonial` metaobject; Judge.me returning `0` on every product.
- "FSSAI approved" is claimed on the storefront with no licence number.
- Shop meta description opens *"…the best bakery and cake shop in Meerut…"* — an unverifiable
  superlative in the store's own metadata, which sits badly beside the project's stated standard
  that no claim ships without a source.
- No named human anywhere on the site. For a *studio* brand — where the craft is the product —
  this is both a trust gap and a differentiation gap.
- Correctly done: no fabricated ratings, and an explicit code-level ban on adding one.

## 16. Conversion content — 6/10

Working: PDP copy is specific and honest about hand-finishing variance; price floors are stated;
sticky WhatsApp CTA is present site-wide and correctly suppressed on product pages; delivery
options are surfaced consistently.

Missing: any mid-funnel surface. There is no path from *"I am researching a cake"* to *"I am
buying this cake"* because the researching stage has no content. The blog's primary commercial
job is to build that path — see `INTERNAL_LINKING_BLUEPRINT.md`.

---

→ Gaps and priorities: `CONTENT_GAP_ANALYSIS.md`
→ The design that answers them: `BLOG_ARCHITECTURE.md`
