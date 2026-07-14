# INFORMATION_ARCHITECTURE.md — The Baking Kaur

The canonical 5-year storefront architecture. Living document — keep updated as pages/collections ship. Governed by [flagship-operating-standard]; feeds `SEO_GEO_MASTER_PLAN.md` and every page-building phase.

Per-page attribute key: **P** purpose · **KW** keywords · **SI** search intent · **CJ** journey stage · **IL** internal links · **S** schema · **GEO** value · **CG** conversion goal.

---

## 17. URL structure
| Type | Pattern | Example |
|---|---|---|
| Pillar collection | `/collections/{handle}` | `/collections/birthday-cakes` |
| Sub-collection | `/collections/{parent}-{child}` | `/collections/birthday-cakes-kids` |
| Product | `/products/{handle}` | `/products/party-bliss-birthday-cake` |
| Local landing | `/pages/{service}-meerut` | `/pages/same-day-cake-delivery-meerut` |
| Guide | `/pages/{topic}-guide` | `/pages/cake-size-guide` |
| Blog | `/blogs/{hub}/{post}` | `/blogs/cake-guides/anniversary-cake-ideas` |

Rules: lowercase, hyphenated, keyword-first, no dates in slugs, one canonical URL per intent, 301 duplicates/empties.

## 14. Breadcrumbs
`Home › {Pillar} › {Sub} › {Product}`. ≥2 levels, keyword labels, `BreadcrumbList` via `tbk-schema-breadcrumb.liquid`. Product uses primary collection (priority Occasion > Theme > Flavor).

## 1. Header
Sticky, one header. Utility bar (city cue · Track Order · Help · WhatsApp · Login · Wishlist · Cart) + main bar (Logo · Birthday · Anniversary · Wedding · Theme Cakes · Hampers · Occasions▾ · Same-Day/Midnight · Search · Cart).

## 2. Mega menu (per pillar: sub-type · occasion/flavor · featured card)
- Birthday: Kids/Adults/Him/Her/Milestone/Number · themes (Unicorn, Jungle, Cricket, Roblox, KPOP, Motu Patlu, Paw Patrol, Teddy, Butterfly) · flavors · same-day card
- Anniversary: Romantic/Floral/Heart/Photo/Milestone/Midnight
- Wedding: Tiered/Engagement/Showstopper/Enquiry
- Theme/Designer: theme taxonomy + custom-from-photo
- Hampers: Cake/Flowers&Cake/Corporate/Festive/Budget
- Occasions: Baby/Farewell/Congratulations/Corporate/Seasonal

## 3. Mobile menu
Accordion drawer; L1 pillars + Same-Day/Midnight + Track Order + Help; sticky bottom utility (Search·WhatsApp·Call·Cart); ≤2 taps to a collection.

## 4. Footer (5 cols)
Occasion · Type/Theme · Delivery · Support · Company/Legal+NAP. Internal-linking backbone + NAP.

## 5 & 6. Collection & category hierarchy
Axes: OCCASION (primary) × TYPE/THEME (secondary) × FLAVOR (tertiary). Pillars evergreen; facets → pages on demand+inventory.
Pillars (live counts): Birthday 279 · Anniversary 102 · Wedding 134 · Designer/Theme 165 · Cake Hampers 119 · Festive (Diwali 44, Winter Strawberry 23).
Theme subs (live): Unicorn 16 · Jungle 17 · Butterfly 23 · Baby Girl 28 · Motu Patlu 12 · boy-or-girl 12 · For Him 11 · Cricket 10 · CA 10 · KPOP 9 · Roblox 8 · Bow 8 · Teddy 7 · Paw Patrol 4.
**8 empty (0-product) collections pending audit** (see Collection Audit): same-day/midnight(×2)/custom/kids/photo/cake-delivery/showstopper — do NOT auto-populate.

## 18. Collection relationships
Related-collections module (siblings + one cross-axis); occasion⇄flavor⇄theme cross-links; hampers cross-sell everywhere; seasonal surfaces in-season, evergreen URL retained.

## 7–12. Page inventory
Local/Delivery landings (same-day, midnight, delivery-areas, cake-delivery hub, store locator) · SEO/trust (about, why-choose, freshness, reviews🆕, FSSAI🆕, eggless-explained🆕) · Buying guides (size🆕, flavour🆕, customization, ordering🆕, care🆕, occasion ideas🆕) · Help center hub (FAQs, delivery, track-order🆕, returns, contact, customization). FAQPage schema page-scoped only.

## 15. Topic clusters
Occasion Cakes · Theme & Custom · Delivery in Meerut · Flavors · Gifting. Each = pillar hub + spokes (collections/guides/blog), fully interlinked.

## 16. Entity graph
Organization → Bakery/LocalBusiness(@id #bakery, Meerut) → Product(Cake) with hasOccasion/hasFlavor/hasTheme/availableDelivery/makesOffer(Offer INR). Single deduped graph (Phase A). Add Product/Offer/Review (Phase F). Consistent NAP + sameAs.

## 13. Internal linking
Vertical hub→sub→product→hub; horizontal siblings+cross-axis; contextual guide⇄collection; every info page → commercial page in ≤1 click; footer+mega distribute equity.

## 19. Blog
`/blogs/cake-guides` + `/blogs/inspiration` (+ `/blogs/news`). Article schema, breadcrumb, 2–4 internal links, funnel to collections.

## 20. Five-year expansion
0–6mo fix empties + local landings + guides + reviews + enterprise footer/mega + PDP schema · 6–18mo flavor collections + blog cluster + corporate hub + locality pages + Hindi · 18–36mo nearby-town area pages + loyalty + seasonal evergreen hubs · 3–5yr multi-location LocalBusiness + B2B portal + PWA + content authority.
Principles: pillar URLs permanent; facets promote on demand; one intent per URL; automated collections auto-categorize; every new page ships schema+breadcrumb+2 internal links.

---
_v0.1 — established. Update as pages/collections ship._
