# DATA_ARCHITECTURE.md — The Baking Kaur

Canonical data model for the storefront. Every reusable component reads from a defined source (Shopify object · metafield · metaobject · section setting) — **no hardcoded content**. Pairs with `CATALOG_ARCHITECTURE.md` (taxonomy), `CONTENT_SYSTEM.md` (homepage content), `COMPONENT_LIBRARY.md` (UI).

Legend: ✅ exists live · 🆕 to create. Namespaces: `shopify.*` = standard taxonomy · `custom.*` = merchant · `*discovery*` = Search & Discovery app.

---

## 1. Product Data Model
| Facet | Source | Notes |
|---|---|---|
| Product type | `product.type` | ✅ Govern to: Birthday/Anniversary/Wedding/Designer/Photo/Hamper (retire Theme/Cake) |
| Tags | `product.tags` | ✅ Convention: `occasion:*`, `theme:*`, `flavor:*`, `audience:*`, `delivery:same-day\|midnight` |
| Collections | `product.collections` | via smart rules (tags/type/metafield) |
| Variants | `product.variants` | flavor × weight (existing PDP) |
| Options | `product.options` | Flavor, Weight (+ delivery date/time via PDP custom) |
| Flavor | `shopify.flavor` (list.metaobject_ref) ✅ | filter + entity |
| Occasion | `shopify.celebration-type` (metaobject_ref) ✅ | smart collections + filter + entity |
| Dietary | `shopify.dietary-preferences` ✅ | "eggless" = universal trust, not filter |
| Allergen | `shopify.allergen-information` ✅ | PDP info |
| Weight | `custom.weightcake` ✅ / variant option | ⚠️ consolidate 3 weight metaobjects → 1 |
| Bestseller | `custom.is_bestseller` (boolean) 🆕 | home merchandising |
| Badge | `custom.badge` (text) 🆕 | card badge |
| Same-day / Midnight | `custom.same_day_eligible` / `custom.midnight_eligible` (bool) 🆕 | delivery cues + smart collections |
| Related / Complementary | `discovery.related_products` / `complementary_products` ✅ | cross-sell/hampers |
| Search boost | `discovery.product_search_boost.queries` ✅ | populate on pillars |
| Google Shopping | `mm-google-shopping.custom_product` ✅ | feed |

## 2. Collection Data Model
| Field | Source | Status |
|---|---|---|
| Title / description / SEO | `collection.*` | ✅ |
| Rule set (smart) | `collection.ruleSet` | ✅ (only 4 smart today → expand) |
| Subtitle | `collection.metafield custom.subtitle` (text) | 🆕 |
| Hero image | `collection.metafield custom.hero_image` (file_ref) | 🆕 |
| SEO intro (long) | `collection.metafield custom.seo_intro` (rich_text) | 🆕 |
| FAQ | `collection.metafield custom.faq` (list.metaobject_ref → `qa-pair`) | 🆕 |
| Related collections | `collection.metafield custom.related_collections` (list.collection_ref) | 🆕 |
(No collection metafields exist today — all 🆕.)

## 3. Homepage Content Model
| Section | Source | Status |
|---|---|---|
| Hero | metaobject `home_hero_slide` (headline, subtext, cta, image_desktop/mobile, alt) | 🆕 |
| Occasions | metaobject `occasion_tile` OR collection + `custom.subtitle`/`custom.hero_image` | 🆕 |
| Bestsellers | `best-selling-products` collection / `custom.is_bestseller` | ✅/🆕 |
| Delivery | section settings + `/pages/*delivery*` | ✅ |
| Craft | metaobject `craft_step` | 🆕 |
| Customization | section settings + `cake-customization-guide` page | ✅ |
| Hampers | `cake-hampers` collection | ✅ |
| Reviews | metaobject `testimonial` | 🆕 |
| Trust stats | metaobject `trust_stat` | 🆕 |
(See `CONTENT_SYSTEM.md` for field lists.)

## 4. Navigation Data Model
- **Menus:** Shopify `linklists` (main menu, footer menu) — merchant-editable in Admin → Navigation.
- **Mega menu:** menu items + per-item metafields (image, blurb) OR a `mega_menu_column` metaobject 🆕 for featured cards.
- **Utility/city cue/WhatsApp:** header section settings.
- Target hierarchy: `CATALOG_ARCHITECTURE.md §9` (nav shows full tree; unstocked nodes → nearest parent).

## 5. Search Data Model
- Engine: Shopify **Search & Discovery** app.
- Boost: `discovery.product_search_boost.queries` (populate on pillars).
- Synonyms 🆕: eggless=egg-free, hamper=gift, midnight=12am, meerut localities.
- Filters: Flavor (`shopify.flavor`) · Occasion (`shopify.celebration-type`) · Price · Weight. **Hide Vendor** (single vendor).
- Predictive search: products + collections + pages + suggested queries.

## 6. Review Data Model
| Field | Source |
|---|---|
| Testimonial (author, rating, body, avatar, source, verified, date) | metaobject `testimonial` 🆕 |
| Aggregate rating | computed from real reviews OR review app — **schema only if real** |
| External proof | Google 4.8 / Zomato — `trust_stat` metaobject 🆕 |
Existing: ShineTrust widgets on PDP. Rule: `AggregateRating` schema only with verifiable reviews (`SCHEMA_MASTER.md`).

## 7. Delivery Data Model
| Field | Source |
|---|---|
| Product eligibility | `custom.same_day_eligible` / `custom.midnight_eligible` (bool) 🆕 |
| Cutoff / slots | PDP `bk-datetime` (existing) + section settings |
| Delivery copy | `/pages/delivery-information`, `/pages/midnight-*`, `same-day` landing |
| Areas | section setting / `service_areas` (footer setting ✅) |
Delivery is an **attribute + service page**, not a product filter grid.

## 8. FAQ Data Model
- Source: metaobject **`shopify--qa-pair`** ✅ (question, answer).
- Attached via: `collection.custom.faq` / `page` FAQ blocks / PDP tab.
- Schema: `FAQPage` **only where visible** (page-scoped) — fixes the global-FAQ issue.

## 9. Trust Signal Data Model
| Signal | Source |
|---|---|
| Stats (20,000+, 4.8, Top-Rated) | metaobject `trust_stat` (value, label, icon) 🆕 |
| Eggless / FSSAI / Freshness | section settings / `trust_row` snippet content |
| Same-day/Midnight | delivery metafields + settings |
Placement matrix: `HOMEPAGE_CONTENT_STRATEGY.md`.

## 10. AI Entity Model
```
Organization(#organization) ─▶ Bakery/LocalBusiness(#bakery, Meerut NAP)
Product(Cake) ─ celebration-type ─▶ Occasion entity
              ─ flavor           ─▶ Flavor entity
              ─ theme (tag)      ─▶ Theme entity
              ─ dietary          ─▶ "eggless" attribute
              ─ makesOffer       ─▶ Offer(INR, availability)
Collection ─▶ CategoryEntity (Occasion/Theme/Flavor × Meerut)
```
Metaobjects (celebration-type, flavor, dietary) ARE the entity spine — reuse them for schema `additionalProperty`/`about`. Consistent NAP + sameAs.

---

## Component data contracts
For every reusable component: **source · Shopify object · metafield/metaobject · fallback · empty state · validation.**

| Component | Data source | Shopify object | Metafield/Metaobject | Fallback | Empty state | Validation |
|---|---|---|---|---|---|---|
| `product-card-premium` | product | Product | `custom.badge`, `custom.same_day_eligible`, price | featured image, no badge | skeleton | image ratio enforced; price required; ≤2 badges |
| `occasion-tile` | metaobject/collection | Collection | `occasion_tile` OR `custom.subtitle`+`custom.hero_image` | collection title + image | hide tile | url resolves; image present or ratio placeholder |
| `review-card` | metaobject | — | `testimonial` | — | hide section | rating 1–5; body ≤300 chars; verified bool |
| `trust-row` | settings/metaobject | — | `trust_stat` | hardcoded defaults in settings | hide row | ≤5 items; label required |
| `hamper-card` | product | Product | price, image | featured image | hide | price required |
| `home-hero` | metaobject | — | `home_hero_slide` | token-styled default headline | default headline (never blank) | headline required; one CTA; alt required |
| `faq` | metaobject | — | `qa-pair` via `custom.faq` | — | hide FAQ + its schema | Q & A non-empty; schema only if visible |
| `delivery-band` | settings + metafield | Product/Page | `same_day/midnight_eligible` | show generic delivery copy | show copy only | boolean |
| `section-heading` | settings | — | — | — | render title only | one display-hero/page |
| `nav / mega-menu` | menus | Linklist | item metafields / `mega_menu_column` | menu labels only | hide featured card | url resolves; unstocked node → parent |

## Principles (enforced)
1. **No hardcoded content** — every string/data point is a Shopify object, metafield, metaobject, or section setting.
2. **Reusable everywhere** — one component contract; snippets consume the same source across templates.
3. **Merchant-editable where practical** — metaobjects + section settings + menus, edited in Admin.
4. **Scalable** — smart collections + metaobject taxonomy auto-absorb new products; new categories add data, not code.
5. **Graceful degradation** — every component defines fallback + empty state; never render blank/broken.
6. **Consolidate before extend** — merge duplicate weight metaobjects; reuse `celebration-type`/`flavor`/`qa-pair` before inventing new.

_v0.1 — canonical data model. Governs Phase B+ implementation._
