# SEO_GEO_MASTER_PLAN.md — The Baking Kaur

Information architecture, schema strategy, internal linking, AI-search (GEO), local SEO, and content roadmap. Living document.

Brand entity: **The Baking Kaur** — 100% eggless luxury cake studio, Meerut (UP), India. Same-day & midnight delivery. Domain `thebakingkaur.com`.

---

## 1. Schema strategy

### Current state (after Phase A dedup)
| Entity | Canonical source | Status |
|---|---|---|
| Organization + WebSite (SearchAction) | `tbk-schema-website.liquid` | ✅ single source |
| Bakery / LocalBusiness | `bk-local-business.liquid` | ✅ single source (dup removed) |
| BreadcrumbList (page-aware) | `tbk-schema-breadcrumb.liquid` | ✅ single source |
| Product / Article (native) | `structured-data.liquid` | ✅ preserved |
| FAQPage | inline `theme.liquid` | ⚠️ **global — must become page-scoped** |

### Pending (Phase F)
1. **Entity linking:** give `bk-local-business` an `@id` (`#bakery`) and link it to `#organization` so Bakery ⊂ Organization is one graph (not two loose entities).
2. **FAQPage:** remove from global `theme.liquid`; render only on pages with visible matching FAQ (FAQ page, relevant collections). Current global emission risks a rich-result policy hit.
3. **AggregateRating authenticity:** `bk-local-business` asserts 4.8/500 with no on-page reviews → penalty risk. Gate behind a real review source; only emit when backed by visible reviews.
4. **Product schema enrichment:** ensure `Offer` (price, availability, currency INR), brand, and — once real — `AggregateRating`/`Review` on PDP (schema-only; PDP UI protected).
5. **Collection schema:** `CollectionPage` + `ItemList` + breadcrumb.

## 2. Information architecture (target)
Topic clusters → hub collections → product/guide spokes:
- **Occasions:** Birthday · Anniversary · Wedding · Baby/Gender-reveal · Corporate
- **Flavors:** (flavor hub + per-flavor guides)
- **Delivery-in-Meerut:** Same-Day · Midnight · Areas served
- **Gifting:** Hampers (budget/premium/luxury) · Flowers · Balloons
- **Education:** Size guide · Flavor guide · Ordering · Customization · Care/Storage
Every hub links down to spokes and across to sibling hubs; every spoke links up to its hub. Breadcrumbs sitewide.

## 3. Internal linking
- Restore the **footer** as the primary internal-linking backbone (occasion + flavor + support + policy columns). *(Currently MISSING in production — critical.)*
- Mega menu exposes occasion/flavor hubs.
- Collection pages carry "related collections" + buying-guide links.
- Blog/guide articles link to relevant collections and products.


### Homepage internal-link graph (live, as built)
```
Home §1 Hero        → /collections/birthday-cakes ; wa.me/918218862928 (WhatsApp)
Home §2 Delivery Promise (6 trust cards, whole-card links)
   ├─ Same-Day Delivery     → /pages/cake-delivery-in-meerut      [canonical planned: /pages/same-day-cake-delivery]
   ├─ Midnight Delivery     → /pages/midnight-cake-delivery       ✅ canonical
   ├─ 100% Eggless          → /pages/why-choose-the-baking-kaur   [canonical planned: /pages/eggless-cakes-explained]
   ├─ Freshly Made to Order → /pages/freshness-guarantee          [canonical planned: /pages/our-promise]
   ├─ FSSAI Licensed        → /pages/about-us                     ✅ canonical
   └─ Premium Custom Cakes  → /pages/cake-customization-guide     [canonical planned: /pages/cake-customization]
```
**Placeholder routes → Phase G (Missing Pages).** `/collections/eggless-cakes` is deliberately NOT planned: eggless is universal to the catalogue, so it would duplicate `/collections/all` (see CATALOG_ARCHITECTURE). Eggless is served by a **content page** instead.

**GEO terms reinforced by §2 copy** (natural, no stuffing): *same-day cake delivery across Meerut* · *midnight cake delivery in Meerut* · *100% eggless* · *custom designer cakes*.

## 4. GEO / AI search (Google AI Overviews · ChatGPT · Claude · Gemini · Perplexity · Copilot · Voice)
- **Clean entity graph** (Phase A dedup is step 1; no mojibake brand terms — see data cleanup C3).
- **Question-shaped, self-contained answers** on collection/guide pages (delivery, eggless, customization, pricing bands).
- Consistent **NAP + `sameAs`** everywhere; complete `LocalBusiness` (hours, geo, areaServed, makesOffer).
- Structured comparisons (flavor table, hamper tiers) that models can lift verbatim.

## 5. Local SEO (Meerut)
- Accurate NAP (reconcile the two geo/address variants found in schema → one truth).
- Same-Day / Midnight / Delivery-Areas landing pages.
- Service-area markup; Google Business Profile alignment (off-theme).

## 6. Titles & descriptions
- Fix product-title **mojibake at the data source** (client-side JS masking does not fix SERP snippets).
- Template: `{Product} | {Occasion/Flavor} Cake in Meerut | The Baking Kaur`.
- Unique meta descriptions per collection/hub with delivery + eggless USP.

## 7. Content roadmap (Phase G pages)
About/Our Story · Craftsmanship · Same-Day Delivery · Midnight Delivery · Delivery Areas · Cake Size Guide · Flavour Guide · Ordering Guide · Customization Guide · Wedding/Birthday/Corporate hubs · Gift Hampers · FAQ · Support · Track Order · Cake Care/Storage · Reviews · Trust (FSSAI/hygiene).

## Changelog of this document
- v0.1 (Phase A) — schema canonicalized (dedup); IA/GEO/local roadmap seeded. Pending items assigned to Phase F/G.
