# CURRENT_STATE.md — TBK Blog OS, Phase 1 Discovery

**Date:** 2026-07-24 · **Method:** Shopify Admin GraphQL (read-only) + local theme source
**Status:** READ ONLY. Nothing was modified.

---

## 1. Store identity

| Field | Value |
|---|---|
| Shop | The Baking Kaur |
| Primary domain | `https://thebakingkaur.com` |
| Plan | Basic |
| Currency / TZ / Country | INR / IST / India |
| Contact email | thebakingkaur@gmail.com |
| Phone (in schema) | +91 8218862928 |
| Address (in schema) | Fatah Complex, Thapar Nagar Lane 7, Meerut, UP 250001 |
| Geo (in schema) | 28.9931, 77.6939 |

Shop meta description (Admin): *"Welcome to The Baking Kaur, the best bakery and cake shop in Meerut…"* — contains the unverifiable superlative **"best bakery"**. Flagged, not changed.

---

## 2. Blog layer — effectively empty

| Blog | Handle | Articles | Comments |
|---|---|---|---|
| News | `news` | **0** | CLOSED |

**One blog. Zero articles.** This is a greenfield build, not a remediation. There is no existing
blog taxonomy, no article tags, no article schema in production, no editorial history.

**Consequence:** every architectural decision in this phase is free. There are no legacy URLs to
preserve, no redirects to write, no cannibalization to unwind *inside* the blog. The
cannibalization problem is entirely on the collection/page layer (§4, §5).

### Theme support that already exists

| Asset | State |
|---|---|
| `templates/blog.json` | Grid layout, 9/page, sidebar blocks all `disabled: true` |
| `templates/blog.list.json` | List layout, 4/page, sidebar blocks **enabled** |
| `templates/article.json` | Title, image, content, social share, nav, **comments**, related (8) + right sidebar |
| `sections/main-blog.liquid`, `main-article.liquid`, `sidebar-blog.liquid`, `blog.liquid`, `heading-article.liquid` | Present (Ecomus base) |
| `snippets/tbk-schema-article.liquid` | Present, rendered from `main-article.liquid:468` |

**Three defects in the shipped blog templates:**

1. `article.json` enables a **comments** block, but the only blog has `commentPolicy: CLOSED`.
   Dead UI.
2. `blog.list.json` and `article.json` sidebars point at a link list `cat_link_list: "blog-categories"`.
   **No menu with handle `blog-categories` exists** (§6). The category widget renders empty.
3. `article.json` sidebar "Recent Post" block is bound to `blog: "blog-default"` and
   `blog.list.json` to `blog: "list"` — **neither handle exists**. The only blog handle is `news`.

---

## 3. Products

- **1,235 total.** 602 ACTIVE / **588 DRAFT** / 45 ARCHIVED (draft state is intentional per `CLAUDE.md`).
- **9 product types:** Anniversary Cake, Bento Cake, Birthday Cake, Cake, Designer Cake,
  Festive Hamper, Gift Hamper, Theme Cake, Wedding Cake.
- **18 tags total** across 1,235 products — an extremely thin controlled vocabulary:
  `anniversary, baby girl, birthday, butterfly, cricket, Diwali Luxury Hamper, gym, hampers,
  he or she, jungle animal theme, kpop, pinata, retirement cake, roblox, teddy, theme cake,
  unicorn, wedding cakes`.
  Casing is inconsistent (`Diwali Luxury Hamper` vs `kpop`); singular/plural is inconsistent
  (`theme cake` vs `wedding cakes`).

### Product content quality (3 ACTIVE samples inspected)

Strong and consistent. Template shape:
`<p>intro</p> · <h3>How it looks</h3> · <h3>Sizes and flavours</h3> · <h3>Ordering and delivery</h3> · <h3>Notes</h3> (ul) · <h3>Is this eggless?</h3> · <h3>Do you deliver in Meerut?</h3>`

- SEO title format `"{Name} - Eggless | Meerut"` is applied and matches `title` — including on
  `motu-patlu-designer-birthday-cake-meerut`, where the `<title>`/H1 mismatch logged in
  `CLAUDE.md` **is no longer present in the API data**. Re-verify the rendered page before
  closing that roadmap item; the data is clean.
- Image `altText` is populated and descriptive: *"Motu Patlu Designer Birthday Cake — eggless
  birthday cake by The Baking Kaur, Meerut"*.
- Every description embeds two Q&A headings (`Is this eggless?`, `Do you deliver in Meerut?`) —
  **identical text on ~602 products.** Boilerplate at that scale is near-duplicate content and
  is not a FAQ schema source.
- **Zero internal links in any product description.** No `<a>` to collections, pages, or blogs.

### Metafields observed

`global.title_tag`, `global.description_tag`, `mm-google-shopping.google_product_category`,
`mc-facebook.google_product_category`, `custom.product_collection`, `custom.product_category`,
`shopify.flavor` (metaobject list), plus **Judge.me `badge` + `widget`**.

**Judge.me is installed and returning `data-number-of-reviews='0'` on every product.**

Also observed: `mm-google-shopping.google_product_category: "2194.0"` vs
`mc-facebook.google_product_category: "8271"` on the same product — the two feeds disagree.

---

## 4. Collections — 35 total

| Handle | Title | Products | Rule |
|---|---|---:|---|
| `all` | All | 1235 | VENDOR ≠ "OK Product Personalizer" |
| `best-selling-products` | Best Selling Products | 1235 | TITLE contains "Best Selling" **AND** TITLE not-contains "Best Selling" |
| `newest-products` | Newest Products | 1235 | TITLE contains "Newest" **AND** TITLE not-contains "Newest" |
| `cakes` | Cakes | 985 | TYPE contains "Cake" |
| `cake-delivery-meerut` | Cake Delivery in Meerut | 985 | TYPE contains "Cake" |
| `midnight-cake-delivery` | Midnight Cake Delivery | 985 | TYPE contains "Cake" |
| `midnight-cake-delivery-meerut` | Midnight Cake Delivery Meerut | 985 | TYPE contains "Cake" |
| `same-day-cake-delivery-meerut` | Same Day Cake Delivery Meerut | 985 | TYPE contains "Cake" |
| `custom-cakes-meerut` | Custom Cakes Meerut | 617 | TYPE = Designer Cake OR Theme Cake |
| `birthday-cakes` | Birthday Cakes | 279 | manual |
| `designer-theme-cakes` | Designer & Theme Cakes | 165 | manual |
| `wedding-cakes` | Wedding Cakes | 134 | TITLE contains **"wed"** |
| `kids-birthday-cakes-meerut` | Kids Birthday Cakes Meerut | 128 | TITLE contains any of 13 theme words |
| `cake-hampers` | Cake Hampers | 119 | manual |
| `anniversary-cakes` | Anniversary Cakes | 102 | manual |
| `showstopper-wedding-cake` | **Surprise Cake Setup with Revolving Cake** | 77 | TYPE = Wedding Cake |
| `luxury-diwali-hampers` | Luxury Diwali Hampers | 44 | manual |
| `baby-girl` | Baby Girl | 28 | manual |
| `butterfly` · `winter-strawberry-collection` | | 23 · 23 | manual |
| `jungle-animal-theme` | | 17 | manual |
| `unicorn` | | 16 | manual |
| `boy-or-girl-cake` · `motu-patlu` | | 12 · 12 | manual |
| `for-him` | | 11 | manual |
| `chartered-accountant` · `criciket` | | 10 · 10 | manual |
| `kpop-cake` | | 9 | manual |
| `ribbon-cake` (titled "Bow Cake") · `roblox` | | 8 · 8 | manual |
| `teddy` | | 7 | manual |
| `paw-petrol` · `photo-cakes` | | 4 · 4 | manual / TITLE contains "Photo" |
| `flowers-cake-combos` · `for-her` | | **1** · **1** | manual |

**Broken rules found:**
- `best-selling-products` and `newest-products` carry mutually-contradictory rules
  (`CONTAINS X` + `NOT_CONTAINS X`) and therefore resolve to **all 1,235 products**, drafts
  included. Neither collection means what its name says.
- `wedding-cakes` matches on the substring **`wed`** — it will capture any title containing
  "Wednesday", "wedge", "jewel" etc.
- `showstopper-wedding-cake` has a handle about wedding cakes, a title about revolving surprise
  setups, a rule selecting `TYPE = Wedding Cake`, and SEO copy about surprise setups. Four
  different subjects in one collection.

**SEO metadata:** present and well-written on ~28 of 35 collections, following
`"{Topic} in Meerut - Eggless"` + a specific description. `all`, `best-selling-products`,
`newest-products` have `seo.title: null`.

---

## 5. Pages — 27 total (16 published, 11 unpublished)

### Published (16)

| Handle | Title | Body |
|---|---|---|
| `about-us` | About The Baking Kaur \| Premium Eggless Bakery in Meerut | substantive |
| `contact` | Contact Us | **empty** (`contact-2` template) |
| `store-locator` | Store Locator | **empty** (`store-locations` template) |
| `frequently-asked-questions-faqs` | Frequently Asked Questions (FAQs) | **empty** (`faq-01` template) |
| `terms-and-conditions` | Terms and Conditions | **empty** (`term-condition` template) |
| `theme-cakes` | Theme Cakes | substantive |
| `photo-cakes` | Photo Cakes | substantive |
| `gift-hampers` | Gift Hampers | substantive |
| `midnight-cake-delivery` | Midnight Cake Delivery | substantive |
| `cake-delivery-in-meerut` | Cake Delivery in Meerut – Same-Day, Midnight & Express | substantive |
| `30-minute-cake-delivery-in-meerut-premium-reliable-service` | 30-Minute Cake Delivery in Meerut | substantive |
| `100-percent-eggless-bakery` | 100% Eggless Bakery in Meerut | substantive |
| `refund-return-policy` | Refund & Return Policy | substantive |
| `customised-hampers-meerut` | Customised Gift Hampers in Meerut | substantive |
| `festive-hampers-meerut` | Festive Gift Hampers in Meerut | substantive |
| `surprise-hampers-meerut` | Surprise Hampers in Meerut | substantive |

Four published pages have **empty bodies** and rely entirely on section templates —
`contact`, `store-locator`, `frequently-asked-questions-faqs`, `terms-and-conditions`.
The FAQ page in particular has no body text while 43 Q&A metaobjects sit unused (§7).

### Unpublished (11)

`home`, `theme-cake-1`, `data-sale-opt-out`, `rewind-menu-backup-page`,
`return-refund-replacement-policy`, `why-choose-the-baking-kaur`, `cake-customization-guide`,
`freshness-guarantee`, `delivery-information`, `midnight-surprise-delivery`,
`corporate-gifting-solutions`.

Six of these are **finished-title, empty-body drafts** created 2026-07 and touched as recently as
today (`why-choose`, `cake-customization-guide`, `freshness-guarantee`, `delivery-information`,
`midnight-surprise-delivery`, `corporate-gifting-solutions`). They occupy exactly the intent
space a blog would target — see `CONTENT_GAP_ANALYSIS.md`.

`return-refund-replacement-policy` duplicates the published `refund-return-policy`.

---

## 6. Navigation — 9 menus

| Handle | Items |
|---|---|
| `main-menu` | HOME, ABOUT US, CONTACT US, Categories (`/collections`) |
| `header` | Birthday Cake, Anniversary Cake, Diwali Hampers, Theme Cakes, Hampers, Wedding Cakes |
| `footer` | Search, Contact, Privacy, Shipping, Refund, Your Privacy Choices |
| `about-us-menu` | About, Contact, Store Locations |
| `quick-links-menu` | FAQs, Privacy, Refund, Shipping, T&C |
| `customer-account-main-menu` | Orders, Profile |
| `explore-cakes` | **empty** |
| `quick-links` | **empty** |
| `meerut-delivery` | **empty** |

- **No menu anywhere links to `/blogs/news`.** If an article shipped today it would be an orphan
  reachable only by sitemap.
- Three empty menus (`explore-cakes`, `quick-links`, `meerut-delivery`) — scaffolding created and
  never filled. `meerut-delivery` in particular is the local-SEO nav that does not exist.
- No menu handle `blog-categories` — the blog sidebar widget is broken (§2).
- `footer` links to `/policies/contact-information` while `main-menu` links to `/pages/contact`.
  Two contact destinations.
- No navigation link exists to: `100-percent-eggless-bakery`, `cake-delivery-in-meerut`,
  `30-minute-cake-delivery…`, `customised/festive/surprise-hampers-meerut`, `photo-cakes`,
  `theme-cakes`. **Ten published pages are orphaned from navigation.**

---

## 7. Structured data — current emission

| Snippet | Rendered from | Entity |
|---|---|---|
| `bk-local-business.liquid` | `theme.liquid:43` (head, every page) | `Bakery` — address, geo, hours 09:00–23:59 daily, `areaServed: City/Meerut`, `makesOffer: Midnight Cake Delivery`, `sameAs` [Instagram, Facebook] |
| `tbk-schema-website.liquid` | `theme.liquid:194` | `@graph` [`WebSite` + `Organization`] with `#organization` @id, `SearchAction` |
| `tbk-schema-breadcrumb.liquid` | `theme.liquid:200` | `BreadcrumbList`, branches on `request.page_type` incl. `article` |
| `tbk-schema-article.liquid` | `main-article.liquid:468` | `Article` |
| `tbk-schema-collection.liquid` | `main-collection.liquid:741` | Collection |
| **inline block** | `theme.liquid:68` | **`FAQPage`, hardcoded, in `<head>`, on EVERY page** |

### Findings

1. **A hardcoded `FAQPage` is emitted in `<head>` on every URL of the site** — homepage, all 1,235
   product pages, all 35 collections, all pages, and any future article. Same six-plus questions
   everywhere. This is the single largest structured-data liability in the store and it will
   collide with any FAQ schema the Blog OS adds.
2. `tbk-schema-article.liquid` sets `"dateModified"` to `article.published_at` — it can never
   reflect an update. Freshness signals will be permanently wrong.
3. Article `author` is `Organization`, not a `Person`. **No author entity exists anywhere on the
   site.** This is the weakest E-E-A-T signal in the audit and the most consequential one for AI
   Overviews and LLM citation.
4. `Bakery.sameAs` lists Instagram and Facebook. **The Google Business Profile URL is absent** —
   the single highest-value entity link for Maps and local AI answers.
5. Two `Organization`-class entities are emitted per page (`Organization` via
   `tbk-schema-website`, `Bakery` via `bk-local-business`) with **different `sameAs` arrays**
   (`bk-local-business` includes Facebook; `tbk-schema-website` does not) and only one carries an
   `@id`. They are not reconciled into one node.
6. No `Blog` or `CollectionPage` schema on blog index templates.
7. `aggregateRating` is correctly absent, with an explicit in-code prohibition
   (`bk-local-business.liquid`). Preserve this.

---

## 8. Metaobjects

| Type | Name | Count |
|---|---|---:|
| `shopify--qa-pair` | Question and Answer Pairs | **43** |
| `shopify--flavor` | Flavor | 9 |
| `shopify--allergen-information` | Allergen information | 4 |
| `weight` | weight | 3 |
| `shopify--dietary-preferences` | Dietary preferences | 2 |
| `shopify--color-pattern`, `shopify--flour-grain-type`, `shopify--celebration-type` | | 1 each |
| `testimonial` | **Verified Review** | **1** |
| `weights`, `weightr` | | **0** (empty duplicates of `weight`) |

**43 Q&A pairs exist as structured metaobjects and are rendered nowhere.** `grep` across all
`.liquid` finds no reference to `qa-pair` / `qa_pair`. They are a complete, ready, structured FAQ
corpus sitting idle while the FAQ page body is empty and a separate hardcoded FAQ block ships in
`<head>`.

Quality is mixed and needs an editorial pass before use — sampled defects: `"he Baking Kaur…"`
(dropped T), `"yes, customers can…"` (lowercase start), `"…special delivery reques"` (truncated).

`testimonial` = **1** entry, and Judge.me reports 0 reviews. The review situation in `CLAUDE.md`
is confirmed unchanged.

---

## 9. Other

- **820 URL redirects** already in place. Handle churn has a history here; treat any future URL
  change as expensive.
- **No custom `robots.txt.liquid`** — Shopify defaults apply. Blog tag pages
  (`/blogs/{blog}/tagged/{tag}`) will be crawlable and indexable by default.
- Everything is single-language (`inLanguage: en-IN`), single-market, single-city. There is no
  city parameterisation anywhere: "Meerut" is hardcoded in collection SEO strings, page handles,
  and `Bakery.areaServed`.

---

## 10. One-line summary

A strong, well-optimised **product and collection** catalogue with disciplined SEO metadata,
sitting on top of an **empty blog**, a **fragmented page layer**, a **navigation layer that links
to almost none of it**, and a **site-wide hardcoded FAQPage** that will fight anything the blog
emits. The blog is greenfield; the prerequisites are not.

→ Audit and scoring: `BLOG_AUDIT.md`
