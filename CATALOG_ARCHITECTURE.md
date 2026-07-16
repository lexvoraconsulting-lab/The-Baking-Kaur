# CATALOG_ARCHITECTURE.md — The Baking Kaur

Canonical catalog strategy for the entire store — the reference for all Homepage, Collection, Search, SEO, and Navigation work. Pairs with `INFORMATION_ARCHITECTURE.md` (URLs/clusters) and `MERCHANDISING_GUIDE.md` (what shows where). Planning only — nothing implemented.

---

## 1. Catalog state (live audit)
- **Collections:** 34 total — **4 smart** (`all`, `newest-products`, `best-selling-products`, `wedding-cakes`), **30 manual**.
- **Product types (inconsistent):** `Theme Cake` (dominant), `Birthday Cake`, `Wedding Cake`, `Designer Cake`, `Cake`, `""` (empty, e.g. hampers). Overlapping/ambiguous — the same birthday cake may be typed `Theme Cake` or `Birthday Cake`; some `Wedding Cake` products are tagged only `birthday`.
- **Vendor:** single — `The Baking Kaur`. **Vendor facet is useless → hide from filters.**
- **Tags (low-cardinality, real signal but weak hygiene):** `birthday`, `anniversary`, `theme cake`, `wedding cakes`, `hampers`, `cricket`, `jungle animal theme`. Sparse; some mismatched (wedding tagged birthday).
- **Product metafields (rich):** `shopify.flavor`, `shopify.celebration-type`, `shopify.dietary-preferences`, `shopify.allergen-information`, `shopify.flour-grain-type`, `shopify.color-pattern` (standard taxonomy) · `custom.weightcake`, `custom.product_collection`, `custom.product_category` · `mm-google-shopping.custom_product` · Search & Discovery: `product_search_boost.queries`, `product_recommendation.related_products` / `complementary_products`.
- **Collection metafields:** **NONE** — must add for premium collection pages.
- **Metaobjects:** `shopify--flavor`, `--celebration-type`, `--dietary-preferences`, `--allergen`, `--color`, `--flour-grain`, **`shopify--qa-pair`** (FAQ), and **3 duplicate weight objects** (`weight`, `weights`, `weightr`).
- **Search/Filters:** Shopify **Search & Discovery** app (search boost + related/complementary). Theme uses Shopify facets.

## 1b. ⚠️ INVENTORY HEALTH & DRAFT MERCHANDISING REVIEW  *(audit 2026-07-16 · read-only · nothing published)*

All counts in §1/§6 are **Admin** counts (they include DRAFT). The **shoppable** figure — what a customer can actually buy — is far smaller.

### Catalogue totals
| Metric | Count | % of catalogue |
|---|---|---|
| **Total products** | **1,235** | 100% |
| **Active** (live, purchasable) | **607** | 49.1% |
| **Draft** (invisible to customers) | **584** | 47.3% |
| **Archived** | **44** | 3.6% |
| **Publish-ready** (of the 584 drafts) | **25** | **2.0% of catalogue / 4.3% of drafts** |

### Draft classification — all 584 drafts
Classified from data signals (`mediaCount`, `productType`, `tags`, `priceRangeV2`, title normalisation). Each product is counted **once**, in priority order: Internal/Test → Duplicate → Seasonal → Needs Images → Needs Content → Ready.

| Category | Count | % of drafts | Basis |
|---|---|---|---|
| **Needs Images** | **363** | 62.2% | `mediaCount = 0` — no product photo at all |
| **Duplicate** | **150** | 25.7% | 75 title groups × 2 copies (import artefact) |
| **Seasonal** | **40** | 6.8% | Diwali hampers — correctly parked out of season |
| **Ready to Publish** | **25** | 4.3% | image + price + productType + tags, no dup/season/corruption |
| **Internal/Test** | **6** | 1.0% | 5 × `Addon – …` + 1 × `Minimal Luxe Hamper Testing` |
| **Needs Content** | **0** | 0.0% | *absorbed* — every content-gap draft also has 0 images, so it lands in Needs Images first |
| **Discontinued** | **0** | 0.0% | ⚠️ **not machine-determinable** — needs the client's judgement (see below) |
| **TOTAL** | **584** | 100% | |

### Root-cause signals
- **503 of 584 drafts (86%) have zero images.** This — not content, not pricing — is the single blocker. **0 drafts are priced ₹0**, so pricing is healthy.
- **Duplicate anatomy is systematic, not random.** 75 groups, always exactly 2 copies. In **56 of 75 groups** one copy carries the image and the legacy short handle (`hamper12`, `ch38`, `b22`), and its twin carries the SEO slug handle (`sunshine-cake-…`) with **0 images**. This is a re-import that slugged the titles and dropped the media. → **56 imageless twins are safe to archive** with no content loss. The remaining 19 groups have 0 images on *both* copies and need a decision, not a merge.
- **8 drafts have encoding-corrupted titles** — `ch290`, `ch292`–`ch296`, `ch298` render as `Eternal Wish Birthday Cake ÃÂÃÂ¢?? The Baking Kaur, Meerut`. Mojibake from a bad import. **Must not be published in this state** — it would be visible brand damage on the storefront and in search results.
- **All 40 seasonal drafts are Diwali** (`Festive Hamper` / `Diwali Luxury Hamper`). Draft is the *correct* state for these out of season.
- **The 25 publish-ready drafts skew premium:** predominantly Wedding (`royal-baraat-…`, `sheesh-mahal-…`, `zari-gold-…`) and Anniversary, ₹1,200–₹3,500. This is the highest-AOV pillar sitting invisible.

### ⚠️ Honest limitation — "Discontinued" cannot be derived from data
Nothing in the product record marks a design as retired. `totalInventory = 0` on **every** draft, so it is not a signal (these are made-to-order cakes; inventory is not tracked). Distinguishing *"we stopped making this"* from *"we never finished the listing"* requires the client. **Recommendation:** treat the 19 both-imageless duplicate groups + the 363 Needs-Images drafts as the pool to review for discontinuation — a design nobody has photographed in this long is the most likely candidate.

### Collections affected (Admin vs shoppable)
| Collection | Admin | **Shoppable** | Hidden | Draft tag/type concentration |
|---|---|---|---|---|
| Birthday | 279 | **226** | 53 | 112 drafts tagged `birthday` |
| Anniversary | 102 | **85** | 17 | 95 drafts tagged `anniversary` |
| Wedding | 134 | **70** | 64 | 15 tagged `wedding cakes`; 27 typed `Wedding Cake` |
| Designer & Theme | 165 | **78** | 87 | 160 drafts tagged `theme cake`; 208 typed `Theme Cake` |
| **Cake Hampers** | 119 | **8** | **111** | **174 drafts tagged `hampers`** — the range is effectively unsellable |

**Cake Hampers is the critical one:** 8 of 119 live. The homepage S3 card links to a collection that shows 8 products against an Admin count of 119. The 174 draft hampers are also where the duplicate problem concentrates.

### Merchandising decisions (ratified 2026-07-16)
1. **No bulk publish.** Publishing 584 drafts would put 503 image-less and 8 mojibake-titled products on the storefront. Net effect: worse than the current state.
2. **Homepage surfaces live, purchasable products only.** No draft inventory. Sections must degrade gracefully when a collection is thin (S3 already does — fallback tile, counts OFF).
3. **Corporate Gifting card stays** (B2B lead-gen; approved, not inventory-dependent).
4. **Recommended sequence** (client action, not ours):
   - **① Archive 56 imageless duplicate twins** — zero risk, zero content loss, −9.6% catalogue noise.
   - **② Fix 8 mojibake titles** — reputational, cheap, 10 minutes.
   - **③ Review the 25 publish-ready** (mostly premium Wedding/Anniversary) → publish what's genuinely for sale. **This is the only publishing this audit endorses.**
   - **④ Decide Internal/Test (6)** — the 5 `Addon –` products look like a cart add-on mechanism, not catalogue items; archive or move to a hidden collection.
   - **⑤ Photograph in AOV order** — Hampers first (174 drafts, worst live ratio, highest gifting AOV), then Designer & Theme.
   - **⑥ Leave the 40 Diwali hampers as drafts** until the season; publishing is a calendar trigger, not a backlog item.
5. **Do not treat draft count as catalogue weakness.** 607 live products is a large, healthy storefront. The drafts are an unfinished import, not lost revenue — with one exception: **Hampers**, which is a real commercial gap.

## 2. Structural findings & principles
1. **Automate the pillars.** 30 manual collections don't scale — new products won't appear. Pillars & sub-types must be **smart collections** (rules on tag / type / metafield).
2. **Govern the taxonomy.** Canonical `product_type` set + required tag conventions + lean on existing metaobjects (`celebration-type`, `flavor`, `dietary-preferences`) as the real categorization spine.
3. **Filters** = flavor · occasion (celebration-type) · dietary (eggless is universal — surface as trust, not filter) · price · weight. **Hide vendor.** Consolidate the 3 weight metaobjects → one.
4. **Collection metafields** (new): `custom.subtitle`, `custom.hero_image`, `custom.seo_intro`, `custom.faq` (→ `qa-pair` refs), `custom.related_collections`.
5. **No thin/duplicate collections** — every collection is smart-populated, has ≥100-word intro + FAQ, and one canonical URL.
6. **Related products** via Search & Discovery automated recommendations (+ manual `complementary_products` for cross-sell/hampers).

## 3. Canonical taxonomy (target)
- **product_type (governed set):** `Birthday Cake` · `Anniversary Cake` · `Wedding Cake` · `Designer Cake` · `Photo Cake` · `Hamper`. (Retire ambiguous `Theme Cake`/`Cake` → map to the above + a theme tag.)
- **Tag conventions:** `occasion:*`, `theme:*`, `flavor:*`, `audience:*`, `delivery:same-day|midnight`. Governs smart rules + filters.
- **Metaobject spine:** `celebration-type` (occasion), `flavor`, `dietary-preferences` drive smart collections + filters + AI entities.

## 4. Breadcrumbs & canonical URLs
- Breadcrumb: `Home › Pillar › Sub › Product` (priority Occasion > Theme > Flavor). Schema via `tbk-schema-breadcrumb.liquid`.
- Canonical: every collection self-canonical; merged/empty collections **301** to their canonical target; `all`/`newest-products` **noindex** (utility, thin-duplicate of catalog).

## 5. SEO / GEO / AI entity model
- Each pillar = a **category entity** ("Birthday Cakes in Meerut") linked to `celebration-type`/`flavor`/`theme` metaobjects → products (Offers, INR).
- `CollectionPage` + `ItemList` + `BreadcrumbList` per collection; `FAQPage` (from `qa-pair`) only where visible. See `SCHEMA_MASTER.md`.
- GEO: one clean entity per intent, question-shaped intro + FAQ, consistent NAP → citable by AI engines.

---

## 6. PER-COLLECTION AUDIT
Two tables cover the 18 required attributes. **Action = one only.**

### 6A. Strategy (purpose · intent · keywords · local/GEO/AI · conversion · ACTION)
| Collection | Cnt | Purpose / Customer intent | Primary KW / Secondary | Local·GEO·AI | Conversion | **ACTION** |
|---|---|---|---|---|---|---|
| birthday-cakes | 279 | Top pillar; buy a birthday cake | "birthday cake Meerut" / kids, designer, number | H·H·H | filter→PDP | **IMPROVE** → convert to smart |
| designer-theme-cakes | 165 | Custom/theme pillar | "designer/theme cake Meerut" / character, custom | H·H·H | PDP/customize | **IMPROVE** → smart |
| wedding-cakes | 134 | Wedding pillar (already smart) | "wedding cake Meerut" / tiered, engagement | H·H·H | enquiry/PDP | **KEEP** (+enrich) |
| cake-hampers | 119 | Gifting/AOV pillar | "cake hamper Meerut" / gift, corporate | H·H·M | PDP (AOV) | **IMPROVE** → smart + content |
| anniversary-cakes | 102 | Anniversary pillar | "anniversary cake Meerut" / romantic, heart | H·H·H | PDP | **IMPROVE** → smart |
| luxury-diwali-hampers | 44 | Seasonal festive AOV | "Diwali hampers Meerut" | H·M·M | PDP | **KEEP** (seasonal evergreen) + content |
| winter-strawberry-collection | 23 | Seasonal flavor | "strawberry cake" / winter | M·M·M | PDP | **KEEP** + add SEO meta |
| butterfly / unicorn / jungle-animal-theme / motu-patlu / kpop-cake / roblox / teddy / paw-petrol / ribbon-cake | 4–23 | Theme sub-collections | "{theme} cake Meerut" | M·M·H (entity) | PDP | **CONVERT → SMART** (theme tag) + 100-word intro |
| criciket *(typo)* | 10 | Cricket theme | "cricket cake" | M·M·M | PDP | **CONVERT → SMART** (fix handle → `cricket`) |
| baby-girl | 28 | Baby occasion | "baby girl cake" / 1st birthday | M·M·M | PDP | **CONVERT → SMART** |
| boy-or-girl-cake | 12 | Gender reveal (overlaps baby) | "gender reveal cake" | M·M·M | PDP | **MERGE** → Baby & Gender-Reveal |
| for-him | 11 | Gifting audience | "cake for him" | L·M·M | PDP | **CONVERT → SMART** (audience tag) |
| for-her | 1 | Thin audience | "cake for her" | L·L·L | — | **MERGE** → occasions (thin) |
| chartered-accountant | 10 | Niche profession theme | "CA cake Meerut" | M·L·M | PDP | **IMPROVE** → smart (long-tail) |
| flowers-cake-combos | 1 | Flowers+cake combo | "flowers and cake Meerut" | M·M·M | PDP | **IMPROVE** (populate; else merge to hampers) |
| same-day-cake-delivery-meerut | 0 | Delivery service (not a filter) | "same day cake delivery Meerut" | H·H·H | landing→collections | **CONVERT → LANDING PAGE** |
| midnight-cake-delivery *(2579 desc)* | 0 | Midnight service (rich content) | "midnight cake delivery Meerut" | H·H·H | landing→collections | **CONVERT → LANDING PAGE** (canonical) |
| midnight-cake-delivery-meerut | 0 | Duplicate of above | — | dup | — | **REDIRECT** → canonical midnight |
| cake-delivery-meerut | 0 | Duplicates delivery-hub page | "cake delivery Meerut" | dup | — | **REDIRECT** → `/pages/cake-delivery-in-meerut` |
| custom-cakes-meerut | 0 | Duplicates designer/theme | "custom cakes Meerut" | dup | — | **REDIRECT** → designer-theme-cakes |
| kids-birthday-cakes-meerut | 0 | Real kids category | "kids birthday cake Meerut" | H·M·H | PDP | **CONVERT → SMART** (theme/kids tags) |
| photo-cakes *(3174 desc)* | 0 | Real product type | "photo cake Meerut" | H·M·H | PDP | **CONVERT → SMART** (`Photo Cake` type) |
| showstopper-wedding-cake | 0 | Niche service, no SEO | — | L·L·L | — | **REMOVE** → 301 to wedding-cakes |
| all / newest-products | 1235 | Utility | — | — | browse | **KEEP** (noindex) |
| best-selling-products | 1235 | Merchandising source (home) | — | — | PDP | **KEEP** |

### 6B. Build requirements (internal links · related · guides · landing · schema · FAQ · content depth · expected # · scalability)
| Collection | Related collections | Guide / Landing | Schema | FAQ | Content depth | Expected # | Scalability |
|---|---|---|---|---|---|---|---|
| birthday-cakes | anniversary, kids, themes, same-day | Birthday ideas guide | CollectionPage+ItemList+Breadcrumb | 4–6 (qa-pair) | 300–500w intro | 400+ | smart tag `occasion:birthday` |
| designer-theme-cakes | themes, custom guide, photo | Customization guide | + | 4–6 | 300–500w | 250+ | smart `type:Designer` OR `theme:*` |
| wedding-cakes | anniversary, hampers, engagement | Wedding cake guide | + | 4–6 | 400–600w | 180+ | already smart |
| anniversary-cakes | birthday, wedding, romantic, midnight | Anniversary ideas | + | 4–6 | 300–500w | 150+ | smart `occasion:anniversary` |
| cake-hampers | flowers-cake, corporate, festive | Gifting guide | + | 3–5 | 200–400w | 150+ | smart `hampers` |
| theme subs | parent pillar + sibling themes | (link to designer) | CollectionPage+Breadcrumb | 2–3 | 100–200w | varies | smart `theme:{x}` |
| seasonal (Diwali, Winter) | hampers / flavors | seasonal hub | + | 2–3 | 200–300w | seasonal | evergreen URL, smart seasonal tag |
| delivery landings | occasion pillars | delivery hub | Service+FAQ+Breadcrumb | 5+ | 500–800w | n/a (page) | one canonical service page |
| kids / photo (→smart) | birthday / designer | ideas guide | CollectionPage+ItemList | 3–4 | 150–300w | 30–80 | smart rule |

---

## 7. Cross-cutting recommendations
- **Filters (Search & Discovery):** Flavor · Occasion (celebration-type) · Price · Weight · Theme. Hide Vendor. Eggless = universal trust badge, not a filter. Consolidate weight metaobjects → one; wire `custom.weightcake` or variant option.
- **Search:** keep Search & Discovery; add synonyms (eggless=egg-free, hamper=gift, midnight=12am), boost bestsellers, ensure `product_search_boost.queries` populated on pillars.
- **Related products:** enable Search & Discovery automated recommendations sitewide; curate `complementary_products` for hamper/add-on cross-sell.
- **Data hygiene (prereq for smart collections):** normalize `product_type` to the governed set; backfill occasion/theme/flavor tags; fix mismatches (wedding tagged birthday); fix handle typos (`criciket`→`cricket`, `paw-petrol`→`paw-patrol`). Mojibake title cleanup (tracked separately).
- **Collection metafields (new):** subtitle, hero_image, seo_intro, faq, related_collections — powers premium collection pages + homepage tiles.

## 8. Action summary
| Action | Collections |
|---|---|
| **Keep** | wedding-cakes, best-selling-products; all/newest (noindex) |
| **Improve** (→ smart + content) | birthday, anniversary, designer-theme, cake-hampers, diwali, winter-strawberry, chartered-accountant, flowers-cake-combos |
| **Convert → Smart** | unicorn, jungle, butterfly, motu-patlu, cricket, kpop, roblox, teddy, paw-patrol, ribbon, baby-girl, for-him, kids-birthday, photo-cakes |
| **Convert → Landing Page** | same-day-delivery, midnight-delivery (canonical) |
| **Merge** | boy-or-girl→baby, for-her→occasions, (flowers-cake→hampers if not populated) |
| **Redirect** | midnight-meerut, cake-delivery-meerut, custom-cakes-meerut |
| **Remove** (301) | showstopper-wedding-cake |

No thin collections created; every duplicate consolidated to one canonical URL; every survivor is smart-populated + content-backed + IA-aligned + scalable.

---

## 9. Target Category Hierarchy (canonical nav + catalog taxonomy)
Client-approved tree, mapped to live inventory. **Rule: a node becomes a collection only at ≥~8–12 products; thinner nodes are filters, roadmap product-lines, or nav-only to the nearest parent — never a thin collection.**

```
Cake
├── Birthday (279)                    ✅ pillar (→smart)
│   ├── Kids            ✅ smart sub (theme tags)
│   ├── Adults          ✅ smart sub (tag)
│   ├── Men (~4)        ⚠️ filter/defer (thin)
│   ├── Women (~10)     ⚠️ filter/defer (thin)
│   ├── Baby (~40)      ✅ smart (merge baby-girl + boy-or-girl)
│   └── Milestone       ✅ smart (needs number/25th/50th tagging)
├── Anniversary (102)                 ✅ pillar (→smart)
├── Wedding (134)                     ✅ pillar (smart)
├── Engagement (0)                    → roadmap; nav→Wedding until SKUs exist
├── Corporate (0 products)            → LANDING PAGE (corporate-gifting), not a collection
├── Photo Cakes (~4)                  ⚠️ smart; grow inventory
├── Theme Cakes (165)                 ✅ pillar (→smart) + theme sub-collections
├── Bento (4)                         🚫 new line — build inventory first
├── Cupcakes (0)                      🚫 new line — build inventory first
├── Brownies (2)                      🚫 new line — build inventory first
├── Hampers (119)                     ✅ pillar (→smart)
├── Flowers (few real SKUs)           🚫 product line — needs bouquet SKUs; not a cake collection
└── Balloons (few/draft add-ons)      🚫 add-on line — attach to PDP/hampers; not a collection
```

**Implementation policy for this tree:**
- **Now (inventory-backed):** Birthday(+Kids/Adults/Baby/Milestone), Anniversary, Wedding, Theme Cakes, Hampers, Photo Cakes → smart collections per §6/§7.
- **Filters not collections (thin):** Men, Women → surface via occasion/audience filter until inventory grows.
- **Landing page:** Corporate → `/pages/corporate-gifting-solutions` (already exists).
- **Product-line roadmap (build SKUs → then collection):** Bento, Cupcakes, Brownies, Flowers (bouquets), Engagement.
- **Add-on:** Balloons → PDP/hamper add-on (Uploadcare/line-item), not a browse collection.
- **Nav shows the full tree** (ambition), but nav entries for not-yet-built nodes point to the nearest populated parent or a "coming soon"/landing — never a 0-product collection.


## 10. RULE — "100% Eggless" is a BRAND ATTRIBUTE, not a product category  *(ratified 2026-07-15)*
**Never create an "Eggless Cakes" collection.** The Baking Kaur is a completely eggless bakery: **all 607 active products are eggless**. A `/collections/eggless-cakes` would return essentially the same set as `/collections/all` → duplicate/thin content, competing URLs, and a diluted entity.

| | |
|---|---|
| **Is** | A site-wide **trust signal** + brand/entity attribute (`shopify.dietary-preferences`) |
| **Is NOT** | A collection, a facet/filter (it has zero filtering power at 100% coverage), or a category node |
| **Served by** | An **editorial content page** → `/pages/100-percent-eggless-bakery` |
| **Surfaced in** | Homepage hero trust row + §2 trust card · product pages · footer trust strip · About · FAQ · schema (`dietary-preferences`, LocalBusiness description) |

Corollary: any attribute with ~100% catalogue coverage is a **brand attribute**, never a collection or filter. (Same logic would apply to e.g. "Handcrafted".)

_v0.3 — eggless ratified as brand attribute (no collection). v0.2 — canonical catalog strategy + target category hierarchy. Awaiting approval before implementation._
