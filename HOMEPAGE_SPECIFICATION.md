# HOMEPAGE_SPECIFICATION.md — The Baking Kaur

Implementation-ready homepage blueprint (approved). Structure & behavior source of truth. Copy → `HOMEPAGE_CONTENT_STRATEGY.md`. Visuals → `DESIGN_SYSTEM.md` / `COMPONENT_LIBRARY.md`. Content model → `CONTENT_SYSTEM.md`. Motion → `ANIMATION_GUIDELINES.md`. Schema → `SCHEMA_MASTER.md`.

## Section order (replaces current 19-section home; retires 7 `custom-liquid` blocks)
1 Hero · 2 Occasions · 3 Bestsellers · 4 Delivery Promise · 5 Craft Story · 6 Customization · 7 Hampers · 8 Reviews · 9 Explore (link band)

## Wireframes
Desktop 1280px, asymmetric editorial (5/7 splits for 1,5,6; 4-up grids for 2,3,7). Mobile single-column, 56–72px rhythm, occasion tiles 2-up, product/hamper carousels with peek, sticky bottom utility (Search·WhatsApp·Cart).

## Per-section spec (Why · KPI · Intent · Links · Schema · GEO)
| # | Section | Why | KPI | Intent | Links | Schema | GEO |
|---|---|---|---|---|---|---|---|
| 1 | Hero | Premium+local first impression, primary path | bounce↓, hero CTR, LCP | Awareness | birthday-cakes, search | H1 (head graph) | brand+local entity |
| 2 | Occasions | Route by intent | tile CTR | Consideration | birthday/anniversary/wedding/baby-girl/corporate | ItemList | occasion entities |
| 3 | Bestsellers | Convert proven products | add-to-cart | Decision | top PDPs, best-selling-products | ItemList | product entities |
| 4 | Delivery | Kill delivery anxiety | scroll depth, CTR | Decision/local | same-day, midnight, delivery-information | — | delivery+voice |
| 5 | Craft | Eggless+fresh trust | engagement, About CTR | Consideration | about-us, freshness-guarantee, why-choose | WebPage | quality entity |
| 6 | Customization | Bespoke capability | WhatsApp clicks | Consideration | designer-theme-cakes, cake-customization-guide | HowTo(opt) | customization entity |
| 7 | Hampers | Raise AOV | hamper CTR, AOV | Consideration | cake-hampers, gift-hampers, luxury-diwali-hampers | ItemList | gifting entity |
| 8 | Reviews | Trust spike | reviews CTR | Decision | /pages/reviews | Review/AggregateRating (real only) | reputation entity |
| 9 | Explore | SEO discovery | internal CTR | Consideration | pillars+guides | — | cluster reinforcement |

## Required Shopify sections (new)
`home-hero` · `home-occasions` · `home-bestsellers` · `home-delivery-promise` · `home-craft-story` · `home-customization` · `home-hampers` · `home-reviews` · `home-link-band`. Each: `{% schema %}` (headings, pickers, toggles) + `presets` + scoped token CSS + `blocks` for repeatables.

## Required snippets
`card-product-premium` · `occasion-tile` · `trust-row` · `review-card` · `hamper-card` · `editorial-split` · `responsive-image` · `icon` · `section-heading`. See `COMPONENT_LIBRARY.md`.

## Internal linking
Home → 5 pillars (nav+occasions+link band) → subs → PDPs. Cross-links occasion↔flavor↔theme. Every section → a commercial destination. See `INFORMATION_ARCHITECTURE.md §13`.

## Objectives (global)
Business: conversion+AOV+assisted revenue. UX: ≤1 tap to pillar, trust every scroll, ≤1 primary action/section. SEO: one H1, semantic sections, pillar links. GEO/AI: entity reinforcement + question-shaped microcopy for AI Overviews/voice.

## Performance / A11y / Schema / Analytics / Responsive / Loading / Images / Motion / Empty / Error
- Perf: hero LCP preload + dimensions; below-fold lazy; no new fonts; no whole-doc observers; budgets LCP<2s CLS<0.1 INP good (see `PERFORMANCE_BASELINE.md`).
- A11y: one H1, landmarks, keyboard carousels, focus, contrast, reduced-motion (see `QA_CHECKLIST.md`).
- Schema: head graph + ItemList; Review only if real; FAQ only if visible (see `SCHEMA_MASTER.md`).
- Analytics: view/select_promotion, view_item_list, select_item, add_to_cart, whatsapp_click, delivery_shortcut_click, link_band_click (Phase J).
- Responsive: bp ≤767/768–1023/≥1024/≥1440; grids 5→3→2, 4→3→2/carousel; splits stack image-first.
- Loading priority: hero eager; occasions+delivery high; rest lazy on scroll.
- Images: AVIF→WebP srcset [360,540,768,1024,1440]; ratios hero 4:5/3:2, cards 4:5, tiles 1:1; art-directed hero; keyword alt.
- Motion: subtle reveal (opacity+8px, once, 300ms); no parallax/autoplay/marquee. See `ANIMATION_GUIDELINES.md`.
- Empty: sections self-hide when data missing; never empty grid.
- Error: image fallback (aspect-boxed), JS-off progressive enhancement, app-failure hides section.


## 🔒 S1 — EDITORIAL HERO: **VERSION 1.0** — FROZEN (2026-07-15)
`sections/home-hero.liquid`. Assembled ONLY from frozen DS parts (tokens + `tbk-button` primary/whatsapp) — **zero new components**. `tbkx-` namespaced → PDP isolated.
- **Content:** one H1 · sub "Luxury handcrafted eggless cakes with same-day & midnight delivery in Meerut." · CTA "Order Now" → birthday-cakes · "Customise on WhatsApp" → canonical 918218862928 · microcopy · 5 trust items (Eggless / Same-Day / Midnight / 4.8★ Google / FSSAI).
- **Image (TEMPORARY PRODUCTION HERO):** product `b32` Classic Strawberry Whipped Cream Cake. WebP · srcset 600/900/1200/1600 · sizes `(min-width:990px) 46vw, 100vw` · explicit width/height (1196×1600) · `fetchpriority=high` · `loading=eager` · `decoding=async` · art-directed `<link rel=preload>` · SEO alt + title. Merchant-editable: uploading the Flagship Hero master overrides with no code change.
- **Validated:** desktop 1280 → 5:7 grid, H1 70.4px, image 633×422 = **3:2**, CLS **0** · tablet 768 → 4:5, CLS 0 · mobile 375 → single column, CTAs full-width 56px · **one H1** (fixed: removed layout's hidden H1 on index + disabled legacy hero block) · no sliders/autoplay/carousels · no overflow.
- **Known:** Lighthouse not runnable in this environment (see PERFORMANCE_BASELINE); hero asset is temporary — see backlog "Flagship Hero Photoshoot".
Frozen — no S1 changes without explicit unfreeze.


## 🔒 S2 — DELIVERY PROMISE (Homepage §2): **VERSION 1.0** — FROZEN (2026-07-15)
`sections/home-delivery-promise.liquid`. **Assembly only — zero new components** (FROZEN `tbkx-card--trust` + frozen icon slot + tokens). `tbkx-` namespaced → PDP isolated. **Zero JS, zero images** (inline SVG only).
- Layout: mobile **2-col** · tablet 3 · desktop **one row** (columns = block count, 4–6). CLS 0 at every width.
- Semantics: `<ul>/<li>` + `aria-label="Our promise"`; **0 headings** (no H2 pollution); decorative icons `aria-hidden`.
- Cards clickable: **one semantic `<a>` per card, 0 nested links, ~98% card coverage, 166px target (≥44px), `:focus-visible` ring**. Hover = frozen card lift.
- Contrast: title `#1A0810` on white (AAA); body `#876575` on white 5.07:1 (AA).

### S2 internal-link graph (all destinations verified HTTP 200)
| Card | Live destination (wired) | Planned canonical route (PLACEHOLDER — not yet created) |
|---|---|---|
| Same-Day Delivery | `/pages/cake-delivery-in-meerut` | `/pages/same-day-cake-delivery` |
| Midnight Delivery | `/pages/midnight-cake-delivery` | ✅ already canonical |
| 100% Eggless | `/pages/why-choose-the-baking-kaur` | **`/pages/100-percent-eggless-bakery`** *(RATIFIED editorial page — **never** `/collections/eggless-cakes`: 100% of the catalogue is eggless → would duplicate `/collections/all`. Eggless = site-wide brand attribute, see CATALOG_ARCHITECTURE §10)* |
| Freshly Made to Order | `/pages/freshness-guarantee` | `/pages/our-promise` |
| FSSAI Licensed | `/pages/about-us` | ✅ already canonical |
| Premium Custom Cakes | `/pages/cake-customization-guide` | `/pages/cake-customization` |

**Rule applied:** recommended routes `/pages/same-day-cake-delivery`, `/collections/eggless-cakes`, `/pages/our-promise`, `/pages/cake-customization` all returned **404** — no URLs were invented. Cards link to verified pages; canonical routes are placeholders above and become real in **Phase G (Missing Pages)**, at which point the links swap via section settings (no code change).
Frozen — no S2 changes without explicit unfreeze.


## 🔒 S3 — OCCASION NAVIGATION (Homepage §3): **VERSION 1.0** — FROZEN (2026-07-15)
`sections/home-occasions.liquid`. **Assembly only — zero new components** (FROZEN `tbkx-card--collection` + `--link/--interactive` + `tbkx-card__media--fallback` + tokens). `tbkx-` namespaced → PDP isolated.
- Layout: mobile-first **2-col** → tablet 3 → desktop one row (cols = block count). **CLS 0**, no overflow, 260px tap targets.
- Hierarchy: **H1 (hero) → H2 "Shop by occasion" → H3 per card** (6).
- Links: **one canonical destination per card**, 1 `<a>`, **0 nested links**, all verified **HTTP 200**.
- Schema: **ItemList** (6 ListItems, absolute URLs).
- Perf: **0 JS**; images **lazy + WebP srcset + explicit w/h + fixed 1:1** ratio.
- **Product counts: OFF** (clean editorial). Setting retained (`show_counts`) for a later optimization phase.
- **Corporate Gifting retained** (B2B lead-gen); no collection exists → renders the approved graceful fallback until an image is set (`image` block setting ready).

### S3 per-card documentation
| Card | Business objective | User intent | KPI | Internal link (200 ✅) | Schema support | GEO signals | AI-search signals |
|---|---|---|---|---|---|---|---|
| **Birthday Cakes** | Route to the largest revenue pillar | Commercial — "birthday cake near me" | Tile CTR → collection → PDP | `/collections/birthday-cakes` | ItemList → future CollectionPage+ItemList | "birthday cakes Meerut" | Answers "what birthday cakes do you have?" |
| **Anniversary Cakes** | Second occasion pillar; romantic/midnight upsell | Commercial — anniversary gifting | Tile CTR, assisted midnight orders | `/collections/anniversary-cakes` | ItemList → CollectionPage | "anniversary cake Meerut" | Occasion entity ↔ midnight delivery |
| **Wedding Cakes** | High-AOV + enquiry pipeline | Commercial/considered — tiered, engagement | Tile CTR → enquiry/PDP | `/collections/wedding-cakes` | ItemList → CollectionPage | "wedding cake Meerut" | Entity: bakery ↔ wedding service |
| **Designer & Theme Cakes** | Showcase craft; absorbs "custom/theme" intent | Commercial — character/custom design | Tile CTR → PDP/WhatsApp | `/collections/designer-theme-cakes` | ItemList → CollectionPage | "designer cake / theme cake Meerut" | Answers "can you make a custom/designer cake?" |
| **Cake Hampers** | Raise AOV; gifting entry | Commercial — gifting | Tile CTR, AOV | `/collections/cake-hampers` | ItemList → CollectionPage | "gift hampers Meerut" | Entity: gifting ↔ bakery |
| **Corporate Gifting** | **B2B lead generation / future growth** | Commercial B2B — bulk & branded | Lead/enquiry rate | `/pages/corporate-gifting-solutions` | ItemList → future Service | "corporate gifting Meerut" | Entity: bakery ↔ B2B service |

**Deliberate exclusions (evidence-based):** *Kids Cakes* (`kids-birthday-cakes-meerut` = 0 products), *Custom Cakes* (`custom-cakes-meerut` = 0; audit redirects → Designer & Theme, which is the card), *Same-Day / Midnight* (both collections 0 products **and** already linked from S2 — duplicating would add no crawl value). Kids returns once Phase A.1 makes it a smart collection.
Frozen — no S3 changes without explicit unfreeze.


## 🔒 S4 — BESTSELLERS (Homepage §4): **VERSION 1.0** — FROZEN (2026-07-16)
`sections/home-bestsellers.liquid`. **Assembly only — zero new components** (FROZEN `tbkx-card--product` + `--link/--interactive` + `tbkx-card__media--fallback` + `tbkx-btn--secondary` via `tbk-button` + tokens). `tbkx-` namespaced → **0 legacy classes inside the section; PDP untouched (verified in DOM)**.

### ⚠️ Naming conflict resolved — "Featured Collections" vs "Bestsellers"
The brief's homepage list names S4 **"Featured Collections"**. This spec's canonical order (§ top of file) sequences **Bestsellers** here. **Bestsellers was built**, because a "Featured Collections" section would have duplicated **S3 Occasion Navigation** exactly — same frozen card, same collection destinations, same internal links — adding a second crawl path to the same six URLs and diluting, not strengthening, the link graph. S3 answers *"what occasion?"*; S4 answers *"what do people actually buy?"*. **Flagged for client confirmation.**

### Purpose & mechanics
| Attribute | Value |
|---|---|
| **Business objective** | Convert on proven demand — the shortest path from homepage to a PDP that already sells |
| **User intent** | Decision — "just show me what's good" |
| **KPI** | Tile CTR → PDP → add-to-cart; assisted conversion rate |
| **Source** | `best-selling-products` **smart collection**, `sortOrder: BEST_SELLING` — real sales data, self-maintaining, no manual curation |
| **Count** | 8 (setting `limit`, 4–12) |
| **Schema** | **ItemList of Product entities** — name, url, image, brand, offers (price, INR, availability) |
| **Perf** | **0 JS** · lazy WebP srcset · explicit w/h · fixed 4:5 → **CLS 0** |
| **Layout** | mobile 2-col → tablet 3 → desktop 4×2. Verified 375px / 624px / 1280px: no overflow, ratio 0.80 exact at every width |

### Deliberate decision — no add-to-cart on the homepage
The spec's §3 row lists `add-to-cart` as the target action. **Not implemented, by design.** The protected PDP owns the customization flow (weight, flavour, message, photo). A homepage ATC would bypass it and ship the wrong cake — a fulfilment failure, not a conversion win. The card converts by routing to the PDP, which is the real decision surface. **Raise with client if ATC is genuinely wanted; it would require a product-level rule for which SKUs are safe to buy unconfigured.**

### Merchandising safety (ties to CATALOG_ARCHITECTURE §1b)
- **Live products only — structurally, not by configuration.** Storefront Liquid cannot see DRAFT products, so the 584 drafts are unreachable here by construction.
- **Graceful degradation — tested, not asserted.** Section was pointed at a real 0-product collection on preview: the entire section disappeared — **no orphan heading, no empty grid, and no stray ItemList schema** (which would otherwise declare an empty list to Google). Other sections unaffected. Reverted after the test.
- **`availability` is honest** — bound to `product.available`, not hardcoded `InStock`.
- **No breadth claims in copy** — per the HOMEPAGE_CONTENT_STRATEGY merchandising constraint.

### Validation (preview theme 151370334377)
Sections render 4/4 · 8 product cards · H1→H2→H3 order intact · **1 link per card, 0 nested links** · **all 9 destinations HTTP 200** · 8/8 images lazy + WebP + explicit w/h + alt · ItemList valid, 8 items, absolute URLs · 0 `<script>` in section · settings survived push (verified by pull-back).

### 🔎 Finding — legacy handles on best-selling products (deferred by client decision)
3 of the top 8 bestsellers resolve to **`/products/b158`, `/products/b155`, `/products/hamper13`** — opaque, keyword-free URLs from the import defect in CATALOG_ARCHITECTURE §1b, now on the **highest-traffic PDPs in the store**. All resolve HTTP 200; nothing is broken.
**🚫 CLIENT DIRECTIVE (2026-07-16): NO handle renames during Homepage development.** Deferred in full to the **SEO MIGRATION – Product Handle Optimization** project (`PROJECT_ROADMAP.md`). S4 links to these handles exactly as they are.

Frozen — no S4 changes without explicit unfreeze.


## 🔒 S5 — SOCIAL PROOF / REVIEWS (Homepage §5): **VERSION 1.0** — FROZEN (2026-07-16)
`sections/home-reviews.liquid`. **Assembly only — zero new components** (FROZEN `tbkx-card--review`: `__stars`, `__author`, `__avatar`, `__verified`; `tbk-button`; tokens). `tbkx-` namespaced → PDP untouched.

### ⚠️ Frozen rendering NOTHING — this is correct, not a defect
There are **0 verified reviews** and **no approved review source is installed** (verified 2026-07-16: no Judge.me, Loox, Shopify Product Reviews, Okendo, Stamped or Yotpo). The section therefore renders **nothing at all** to customers: no heading, no cards, no schema. It activates **automatically** on the first verified review — no code change, no deploy.

### Fabrication is impossible by construction, not by policy
The section has **no setting capable of holding review text, a reviewer name, a rating or a count**. All content comes from `testimonial` metaobjects ("Verified Review"), where **every field is mandatory — including `source_url`, a public link to the original review**. An entry cannot be saved without its proof. Only `verified == true` entries render.
This is the structural answer to the fabricated testimonials found live on 2026-07-16 (`REVIEW_STRATEGY.md` §8): the previous section stored review text in theme settings, which is indistinguishable from fiction and carries no provenance.

### 🚫 Emits NO structured data — deliberately
No `Review`, no `AggregateRating`. Google's review-snippet guidelines disallow **self-serving** ratings for `LocalBusiness`/`Organization` — a business marking up ratings about itself is not eligible for rich results, and a hardcoded value is the shape that earns a manual action. **Re-adding it would be wrong even with genuine data.** Separately, computing an aggregate from a hand-picked subset would declare a rating no data supports. Full reasoning: `REVIEW_STRATEGY.md` §4–§5.
**GEO is unaffected:** AI assistants read visible text, so real reviews earn AI-search visibility with no markup at all.

### Purpose & mechanics
| Attribute | Value |
|---|---|
| **Business objective** | Trust spike at the decision point — proof from real customers |
| **User intent** | Decision — "is this place actually good?" |
| **KPI** | Scroll-depth past §5; reviews CTR; assisted conversion |
| **Source** | `testimonial` metaobjects, `verified == true` only |
| **Count** | 3 (setting `limit`, 3–9) |
| **Schema** | **None** — by design (see above) |
| **Perf** | **0 JS** · no images · CLS 0 |
| **Layout** | mobile 1-col → desktop 3-col |
| **Editor placeholder** | *"Waiting for verified review source."* — `request.design_mode` only; **never reaches a customer** |

### Validation (preview 151370334377)
**Empty state:** section wrapper renders **0 bytes** — no heading, no cards, no schema, placeholder not leaked; S1–S4 unaffected.
**Populated state (tested with disposable non-review test entries, then deleted):** verified entry rendered; **unverified entry did NOT leak** — the core filter guarantee; stars rendered ★★★★☆ / `aria-label="4 out of 5"` from a seeded rating of **4**, proving the rating is data-driven and not hardcoded; avatar initial derived; source link carries `rel="nofollow noopener ugc"`; H2→H3 hierarchy intact; 0 `<script>`; still no schema.
**Cleanup verified:** test entries deleted; storefront returned to the clean empty state.

Frozen — no S5 changes without explicit unfreeze. Governance: `REVIEW_STRATEGY.md`.


## 🔒 S6 — CRAFT STORY (Homepage §6): **VERSION 1.0** — FROZEN (2026-07-16)
`sections/home-craft-story.liquid`. **Assembly only — zero new components** (FROZEN `tbk-button` primary + ghost; FROZEN tokens). The 5/7 editorial split is **section-scoped layout**, not a component — same precedent as S1 hero / S3 / S4 grids. No new button, card, form, badge or typography introduced. `tbkx-` namespaced → PDP untouched.

### Why the trust points are a plain list, not `tbkx-card--trust`
S2 Delivery Promise already owns the trust-card pattern. Re-using cards here would duplicate a component's **job**, dilute S2's distinctiveness, and put two competing trust blocks on one page. The component-reuse rule forbids duplicate components — this extends it to duplicate **uses**. Trust points render as a token-styled `<ul>`: 3 short proofs, zero new CSS vocabulary.

### 🚫 Image is optional and client-supplied — no stock asset
The theme's stock images (`p1`, `p2`, `c1`, `c2`, `h1`, `h2`, `g1`) are **Ecomus demo content — the same source as the fabricated testimonials removed on 2026-07-16**. Shipping one as this bakery's "craft" would be the identical mistake in a new costume. No image is hardcoded.
**With no image the section renders text-only, centred, max 72ch** — no broken layout, no placeholder, no fallback icon. The copy is the substance; the image is an enhancement. It can be added later via the section setting with **no code change and no deploy**.
Compounding the earlier hero finding (watermarks, third-party branding and customer names burned into catalogue photos), **no compliant craft asset exists**. Folded into the existing **Flagship Hero Photoshoot** backlog rather than raised as a new blocker.

### 🚫 Emits NO structured data — deliberately
Craft story is prose, not a list or Q&A: there is no honest schema type for it. The eggless / freshly-baked facts do their GEO work as **visible text** — AI assistants read rendered content (same reasoning as S5, `REVIEW_STRATEGY.md` §4). Inventing `FAQPage` for non-Q&A prose would be exactly the "markup that doesn't match visible content" pattern this project has been removing.

### Purpose & mechanics
| Attribute | Value |
|---|---|
| **Business objective** | Convert the brand's two strongest differentiators — 100% eggless, baked-to-order — into stated, checkable trust |
| **User intent** | Reassurance — "is this actually eggless, and is it fresh?" |
| **KPI** | Scroll-depth; CTR to `/pages/about-us` + `/pages/freshness-guarantee` |
| **Copy source** | `HOMEPAGE_CONTENT_STRATEGY.md` §5 — verbatim, no ad-libbing in Liquid |
| **Schema** | **None** — by design |
| **Perf** | **0 JS** · lazy WebP srcset · explicit w/h → CLS 0 |
| **Layout** | mobile 1-col (image → text) · desktop **5fr / 7fr** split |
| **Links** | `/pages/about-us` (primary) · `/pages/freshness-guarantee` (ghost) — both **HTTP 200** |

### SEO / GEO
Answers the two highest-intent questions asked about this bakery — *"are the cakes eggless?"* and *"are they fresh?"* — in plain prose an AI can quote. Keywords ("100% eggless cakes", "freshly baked") appear **once each, naturally**, per `BRAND_VOICE.md`. Two internal links to the pages that substantiate the claims — the claim and its proof are one click apart.

### Validation (preview 151370334377)
**Text-only (shipped) state:** renders; `--noimg` single column; H2-only hierarchy (no orphan H3); both CTAs **HTTP 200**; buttons resolve to the frozen `tbkx-btn tbkx-btn--primary/--ghost tbkx-btn--md`; 0 `<script>`; no schema emitted; S1–S5 unaffected.
**With-image state:** tested by temporarily setting an image, then reverted. Desktop split measured **0.714 = exactly 5/7**; `format=webp` in `src` and `srcset` (500/750/1100w); `loading="lazy"`; **CLS 0 proven structurally** — the browser reserved ratio **1.500** from the `width`/`height` attributes (4096×2731) *before* the image loaded, matching the rendered ratio exactly. Revert verified.
**Mobile (375px):** 1 column, no overflow, CTA tap targets **48px** (≥44px), trust points wrap cleanly to 2 rows.

### ⚠️ Open claim — "FSSAI approved"
Rendered as a trust point. It is the client's own claim (already live in the trust bar), **not** review data — so it is out of `REVIEW_STRATEGY.md` scope. But it is a **factual claim**, held to the same standard as the "20,000+ celebrations" milestone (§5b): **an FSSAI licence number is public, legally required to be displayed, and would convert an unverifiable adjective into checkable proof.** Recommended, not blocking. Backlogged.

Frozen — no S6 changes without explicit unfreeze.

_v1.7 — S6 Craft Story frozen (Version 1.0) — text-only until a compliant craft photo exists; no stock demo asset used. v1.6 — S5 Social Proof frozen (Version 1.0) — renders nothing until a verified review source exists; emits no review schema (self-serving markup disallowed). v1.5 — S4 Bestsellers frozen (Version 1.0); handle renames deferred to the SEO Migration project. v1.4 — S4 Bestsellers built, awaiting review. v1.3 — S3 Occasion Navigation frozen (Version 1.0). v1.2 — S2 Delivery Promise frozen (Version 1.0). v1.1 — S1 Editorial Hero recorded as Version 1.0 (frozen). v1.0 — approved. Build in small reviewable phases, one section at a time, validated on preview._
