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
   ├─ 100% Eggless          → /pages/why-choose-the-baking-kaur   [canonical planned: /pages/100-percent-eggless-bakery]
   ├─ Freshly Made to Order → /pages/freshness-guarantee          [canonical planned: /pages/our-promise]
   ├─ FSSAI Licensed        → /pages/about-us                     ✅ canonical
   └─ Premium Custom Cakes  → /pages/cake-customization-guide     [canonical planned: /pages/cake-customization]
Home §3 Occasion Navigation (6 collection cards, whole-card links, ItemList schema)
   ├─ Birthday Cakes          → /collections/birthday-cakes
   ├─ Anniversary Cakes       → /collections/anniversary-cakes
   ├─ Wedding Cakes           → /collections/wedding-cakes
   ├─ Designer & Theme Cakes  → /collections/designer-theme-cakes   (absorbs "custom cakes" intent)
   ├─ Cake Hampers            → /collections/cake-hampers
   └─ Corporate Gifting       → /pages/corporate-gifting-solutions  (B2B lead-gen)
```
**S3 excludes** Kids / Custom / Same-Day / Midnight collections (all 0 products; delivery already linked from §2) — no links to empty collections, no duplicate internal links.
**S3 AI/GEO:** ItemList makes each occasion a first-class entity with an absolute URL, tying `Bakery → occasion category → products` for AI Overviews / ChatGPT / Gemini / Perplexity.

```
Home §4 Bestsellers (8 product cards, whole-card links, ItemList of Product entities)
   └─ best-selling-products (smart, BEST_SELLING) → top 8 live PDPs + "View all cakes" → /collections/all
```
**S4 SEO:** 8 crawlable links straight to the store's highest-converting PDPs — the homepage passes authority to proven revenue pages, not to arbitrary picks. Self-maintaining: the smart collection re-ranks on real sales, so the link graph follows demand without manual edits.
**S4 AI/GEO:** ItemList of **Product** entities (name · image · brand · offers.price · offers.priceCurrency · offers.availability) completes the chain `Bakery → occasion category (S3) → individual product with a price (S4)`. This is what lets an AI answer *"how much is a birthday cake at The Baking Kaur?"* with a real number and a real URL — the single highest-value GEO addition so far, because price is the question AI assistants are most often asked and most often cannot answer.
**S4 honesty guarantee:** `availability` is bound to `product.available`; the section cannot render draft inventory (storefront Liquid cannot see drafts); and at 0 products it emits **no schema at all** rather than an empty ItemList. Verified on preview.
**⚠️ Open SEO debt — deferred by client directive:** 3 of the top 8 bestsellers sit on legacy handles (`/products/b158`, `/products/b155`, `/products/hamper13`) — keyword-free URLs on the highest-traffic PDPs. All HTTP 200; nothing is broken.
**🚫 NO handle renames during Homepage development** (client directive, 2026-07-16). Deferred in full to the **SEO MIGRATION – Product Handle Optimization** project (`PROJECT_ROADMAP.md`), whose 8 mandatory steps are: handle mapping → 301 redirect plan → internal link update → QR code audit → Google indexing verification → sitemap update → canonical validation → Search Console monitoring.
**Standing URL rule for all remaining homepage phases (S5–S9):** sections link to handles **exactly as they exist**. Never rename, never "tidy", never hardcode a prettier URL that does not resolve. A URL that works is worth more than a URL that reads well.
**Placeholder routes → Phase G (Missing Pages).**

### "100% Eggless" — site-wide trust signal (RATIFIED)
**No `/collections/eggless-cakes` — ever.** 100% of the catalogue is eggless, so a collection would duplicate `/collections/all`. Eggless is a **brand attribute + trust signal**, served by an editorial page:
- **Canonical page:** `/pages/100-percent-eggless-bakery` — philosophy, what eggless means here, FAQs, links to primary cake collections.
- **Targets:** "eggless bakery in Meerut", "eggless cakes Meerut", "are your cakes eggless".
- **Consistent surfaces:** homepage hero trust row · homepage §2 trust card · product pages · footer trust strip · About · FAQ · schema.
- **Schema:** `dietary-preferences` metaobject on products + LocalBusiness/Bakery description; **FAQPage only on this page** (visible FAQ) — per SCHEMA_MASTER page-scoping rule.
- **GEO:** the page is the canonical answer target for "is The Baking Kaur eggless?" across AI Overviews / ChatGPT / Gemini / Perplexity / voice.

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


---

## Reviews, ratings & AggregateRating — hard rules  *(2026-07-16 · full detail in `REVIEW_STRATEGY.md`)*

### 🚫 The storefront emits NO review schema. Anywhere.
No `Review`, no `AggregateRating` — not on the homepage, not sitewide, not on PDPs.

**Why, in order of severity:**
1. **Self-serving markup is disallowed.** Google's review-snippet guidelines exclude ratings a business collects and marks up **about itself** from rich-result eligibility for `LocalBusiness`/`Organization`. Not merely ineligible — a hardcoded value is the shape that earns a **manual action** for spammy structured data.
2. **A featured subset is not an aggregate.** Computing a rating from 3 hand-picked 5★ reviews declares a 5.0 the data does not support. Never compute an aggregate from what is displayed.
3. **Genuine Google ratings need no help from us.** They already surface in Google's knowledge panel and Maps. Re-declaring them imports all the risk for no visibility.

**Removed from production 2026-07-16:** a hardcoded `"aggregateRating": {"ratingValue":"4.8","reviewCount":"500"}` in `snippets/bk-local-business.liquid`. Because that snippet renders in `<head>`, the unverifiable rating was on **every page of the site (~1,200 URLs)**, not just the homepage. A permanent guard comment now sits where it was.
**PDP `Product` schema carries no `aggregateRating`** — verified 2026-07-16. Keep it that way until a genuine product-review source exists.

### GEO / AI-search
**Visible text is sufficient.** AI Overviews, ChatGPT, Gemini and Perplexity read rendered content, not only markup — so genuine reviews earn AI-search visibility with **zero schema**. Emitting none costs nothing.
**Fabricated claims are worse than silence.** AI systems cross-reference against Google, Maps, Zomato and social. A site claiming reviews that exist nowhere else creates a **contradiction in the entity graph**, undermining every other claim — including the true ones (NAP, hours, eggless, delivery) this plan has worked to establish.
**The honest lever for "is The Baking Kaur good?" is to collect more real reviews** — not to author them. Backlogged as *"Collect genuine reviews"*.

### Standing rule for all remaining phases
Any section proposing a star, a rating, a count or a testimonial must first satisfy `REVIEW_STRATEGY.md` §0: **traceable to a real customer at a verifiable public URL, or it does not ship.**
