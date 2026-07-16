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

_v1.3 — S3 Occasion Navigation frozen (Version 1.0). v1.2 — S2 Delivery Promise frozen (Version 1.0). v1.1 — S1 Editorial Hero recorded as Version 1.0 (frozen). v1.0 — approved. Build in small reviewable phases, one section at a time, validated on preview._
