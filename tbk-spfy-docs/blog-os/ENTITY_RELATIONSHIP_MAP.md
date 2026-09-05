# ENTITY_RELATIONSHIP_MAP.md — Digital twin & knowledge graph

**v2.0.** §1 (current state) is an observation and is unchanged. §2, §3, §5 and §6 were rebuilt
after `DESIGN_REVIEW.md`: 4 silos → 2, `Article.about`/`mentions` product edges added (F-27),
`Service` nodes added (S-28), and an **off-site corroboration layer** added (F-21) — the absence
of which was the single largest hole in v1's GEO design.

The working model referenced by every downstream decision.

---

## 1. Digital twin — the store as it exists today

```
                          HOMEPAGE  /
                              |
        +---------------------+---------------------+
        |                     |                     |
     HEADER MENU          MAIN MENU              FOOTER MENU
     (6 collections)      (4 items)              (6 policy links)
        |                     |                     |
        v                     v                     v
   birthday-cakes        /pages/about-us       /policies/*
   anniversary-cakes     /pages/contact        /pages/data-sale-opt-out (UNPUBLISHED)
   luxury-diwali-hampers /collections  --------------------+
   designer-theme-cakes                                    |
   cake-hampers                                            v
   wedding-cakes                                    35 COLLECTIONS
                                                           |
                                                           v
                                                   1,235 PRODUCTS
                                                 (602 act / 588 draft / 45 arch)
                                                           |
                                                     [ NO OUTBOUND LINKS ]

  ORPHANED — reachable from no menu:
    /blogs/news (0 articles)          /pages/100-percent-eggless-bakery
    /pages/cake-delivery-in-meerut    /pages/30-minute-cake-delivery-...
    /pages/theme-cakes                /pages/photo-cakes
    /pages/gift-hampers               /pages/midnight-cake-delivery
    /pages/customised-hampers-meerut  /pages/festive-hampers-meerut
    /pages/surprise-hampers-meerut

  EMPTY MENUS:  explore-cakes · quick-links · meerut-delivery
  BROKEN BINDS: blog-categories (missing) · blog-default (missing) · list (missing)
  DORMANT:      43 shopify--qa-pair metaobjects (rendered nowhere)
                 1 testimonial metaobject · Judge.me @ 0 reviews
```

**The shape of the problem in one line:** a deep, well-optimised catalogue with a two-item
navigation layer sitting on top of it, and every editorial asset floating outside the graph.

### Link-flow reality

| Edge | Exists? |
|---|---|
| Home → Collection | ✅ 6 via header |
| Collection → Product | ✅ |
| Product → Collection | ❌ (breadcrumb schema only, no body links) |
| Product → Page | ❌ |
| Product → Blog | ❌ **and structurally blocked** — `main-product-premium-v2.liquid` is protected |
| Page → Collection | ⚠️ some, inconsistent |
| Page → Page | ❌ |
| Blog → anything | n/a (no articles) |
| anything → Blog | ❌ |

Equity flows **downward only**, and dead-ends at the product. There is no circulation.

---

## 2. Target digital twin

```
   OFF-SITE CORROBORATION                        HOMEPAGE
   GBP · Zomato · Swiggy                            |
   JustDial · Instagram        +--------------+-----+--------+--------------+
   Wedding directories         |              |              |              |
        |                   SHOP NAV      LEARN NAV      LOCAL NAV      TRUST NAV
        |  sameAs (>=6)     (header)   (explore-cakes)  (meerut-      (quick-links)
        v                      |              |          delivery)         |
   [ #organization ] <---------+              |              |             |
        ^                      v              v              v             v
        |                 COLLECTIONS    2 BLOG SILOS   /pages/cake-   /pages/freshness
        |                      |         cake-guides    delivery-in-   /pages/faqs
        |                      |         meerut         meerut         /pages/authors/{slug}
        |                      |              |                              |
        |                      v              v                              |
        |                  PRODUCTS      PILLAR (9) --> CLUSTER (53)         |
        |                      ^              |              |               |
        |                      |              |  HTML down-links             |
        |                      +--------------+              |               |
        |                      ^                             |               |
        |          schema      |   Article.about / mentions  |               |
        |          edge -------+-----------------------------+               |
        |                                                                    |
        +-- publisher ---- all Article.author -------------------------------+
                                                            (Person entity)

  enriched collection descriptions --> link ACROSS into the blog (the reverse edge)
```

Four changes turn a tree into a graph:
1. the blog links **down** to collections and products in HTML,
2. **enriched collection descriptions link across into the blog** — the reverse edge,
3. **`Article.about` / `mentions` create a machine-readable article↔product edge** that requires
   no change to the protected product template (`DESIGN_REVIEW.md` F-27),
4. every article resolves to a **named person**, and the organization resolves to **≥6 external
   corroborating nodes**.

v1 had only (1) and (4). It declared (3) impossible and did not contain (2) or the off-site layer
at all.

---

## 3. Knowledge graph — entity nodes

| `@id` | Type | Status | Notes |
|---|---|---|---|
| `#organization` | `Organization` | ✅ live | Has `@id`; `sameAs` = [Instagram] only |
| *(unnamed)* | `Bakery` | ⚠️ live, **no `@id`** | Address, geo, hours, `areaServed`; `sameAs` = [Instagram, Facebook] |
| `#website` | `WebSite` | ✅ live | `SearchAction` present |
| `#person-{slug}` | `Person` | ❌ **missing** | The critical gap; needs **≥2** external profiles, not one |
| `#blog-cake-guides`, `#blog-meerut` | `Blog` ×2 | ❌ planned | v1 planned 4 |
| per-article | `Article` | ⚠️ snippet exists, no articles | `author` → Organization (wrong); **no `about`/`mentions`** |
| `#service-*` | `Service` ×4 | ❌ **missing** | Midnight, same-day, custom design, corporate gifting. v1 had one stub `makesOffer` |
| per-article | `FAQPage` | ❌ **and now deliberately not planned** | No rich result for commercial sites (`DESIGN_REVIEW.md` F-01). One sitewide emission only |
| per-product | `Product` | ✅ | |
| per-collection | `CollectionPage` | ✅ | |
| `City/Meerut` | `Place` | ⚠️ | Only as `areaServed` string; localities not modelled |
| FSSAI credential | `hasCredential` | ❌ **blocked** | Claimed in prose, no number |
| Google Business Profile | `sameAs` | ❌ | **Highest impact-per-hour fix in the plan** |

### Reconciliation required

`Organization` and `Bakery` currently describe one business as two unlinked nodes with different
`sameAs` arrays. Target:

```
Bakery @id = https://thebakingkaur.com/#organization      ← single node, Bakery subtype
  ├ sameAs: [ ★ Google Business Profile, Instagram, Facebook,
  │           Zomato, Swiggy, JustDial, wedding directory ]   ← >=6, NAP-identical
  ├ address, geo, openingHoursSpecification, areaServed
  ├ founder      → #person-{slug}
  ├ hasCredential→ FSSAI (blocked)
  └ makesOffer   → #service-midnight, #service-same-day,
                   #service-custom-design, #service-corporate

Service @id = .../#service-midnight            (x4)
  ├ provider     → #organization
  ├ areaServed   → City/Meerut
  └ hoursAvailable

Person @id = https://thebakingkaur.com/#person-{slug}
  ├ worksFor  → #organization
  ├ url       → /pages/authors/{slug}
  └ sameAs    → [ >=2 real external profiles ]     ← one does not resolve a person

Article  → author      → #person-{slug}     (Organization in the interim)
         → publisher   → #organization
         → isPartOf    → #blog-{silo}
         → about       → Product / Collection @id   ← the product edge v1 gave up on
         → mentions    → Product / Collection / Place @id
```

**`about` / `mentions` is the load-bearing addition.** It is emitted from the *article* template,
touches no product file, and is exactly the relationship AI retrieval traverses — so the edge v1
declared impossible was the one that most mattered for the brief's stated goal.

---

## 4. Entity → content mapping

| Entity | Owned by | Reinforced by |
|---|---|---|
| **The Baking Kaur** (brand) | `/` + `/pages/about-us` | every page's site-wide schema |
| **100% eggless** (differentiator) | `/pages/100-percent-eggless-bakery` | pillar CG-P5 + 6 clusters |
| **Meerut** (place) | `/pages/cake-delivery-in-meerut` | silo `meerut`, `loc-*` tags, GBP |
| **Custom cake** (service) | `/collections/custom-cakes-meerut` | pillar CG-P1, `#service-custom-design` |
| **{Named baker}** (person) | `/pages/authors/{slug}` | every article byline — **blocked** |
| **Occasions** | occasion collections | **enriched collection descriptions**, `occ-*` tags |
| **Formats** | product types + format collections | **enriched collection descriptions** |
| **Delivery** (service) | `/pages/cake-delivery-in-meerut` | `#service-midnight`, `#service-same-day`, ME-P1 |
| **Localities** | *nothing today* | `meerut` ME-1c–1f, `loc-*` tags — **gated on real delivery data** |

Occasions and formats are reinforced by **collection copy, not articles** — v1 assigned them to a
`cake-ideas` silo that would have outranked the very collections that own them
(`DESIGN_REVIEW.md` F-11).

Two entities the brand genuinely owns and does not currently claim: **"100% eggless"** (stated on
one orphaned page) and **the person who bakes** (stated nowhere).

---

## 5. Customer journey → content map

| Stage | Query shape | Content today | Content in target |
|---|---|---|---|
| **Unaware** | "eggless cake safe for kids?" | ❌ none | `cake-guides` CG-P5 |
| **Problem-aware** | "what size cake for 20 people" | ❌ none | `cake-guides` CG-P2 |
| **Solution-aware** | "unicorn cake ideas" | ⚠️ thin collection | **enriched collection description** — *not* an article |
| **Vendor-aware** | "cake shops in Meerut", "is it really eggless" | ⚠️ orphaned pages | `meerut` + **GBP/off-site corroboration** |
| **Ready** | "buy unicorn cake meerut" | ✅ collections/products | unchanged — **the blog never competes here** |
| **Post-purchase** | "how to store the cake" | ❌ none | `cake-guides` CG-P6 |
| **Advocacy** | leaving a review | ❌ 0 reviews | client-blocked |

The solution-aware row is the v2 correction. v1 answered it with a 450-article ideas silo; the
correct answer is the collection page that already holds the images and the products.

**Four of seven stages have no content at all**, and they are the four that feed the two that do.
The catalogue is a very good bottom-of-funnel with nothing above it.

---

## 6. AI-search retrieval model

What an answer engine needs, and whether it can get it today:

| Requirement | Today | Target |
|---|---|---|
| Resolvable business entity | ⚠️ two unlinked nodes | one `Bakery` node with `@id` |
| Resolvable author entity | ❌ | `Person` + author page, ≥2 profiles |
| **External corroboration (`sameAs`)** | ⚠️ IG/FB only, **no GBP** | **≥6 nodes, NAP-identical — the off-site track** |
| Article↔product machine edge | ❌ | **`about` / `mentions`** |
| Extractable answer near the top | ❌ | direct answer within the first 60 words |
| Q&A-formatted content | ⚠️ 43 metaobjects, unrendered | rendered on the FAQ page + **seeded into GBP Q&A** + question-shaped subheadings in articles |
| Attributable claims | ❌ | **first-party evidence** — real lead times, real price bands, process photos, named baker |
| Verifiable differentiator | ✅ exists, ❌ unpublished | CG-P5 pillar |
| Freshness signal | ❌ `dateModified` is wrong | `custom.last_reviewed` |
| AI crawler access | ⚠️ **undecided by default** | explicit **allow** in `robots.txt.liquid` |
| Entity disambiguation | ❌ "Kaur" is near-universal; 2 `sameAs` cannot resolve it | ≥6 corroborating nodes |
| Ratings | 0 real | **stays 0 until real** |

An LLM asked *"where can I get a fully eggless custom cake in Meerut?"* currently finds: a
catalogue with the right products, a `Bakery` node with the right address, and **no prose it can
quote, no person it can attribute, and nothing independent that corroborates any of it.**

**The corroboration gap is the important one, and v1 missed it entirely.** v1's answer was to
write better prose on `thebakingkaur.com`. Answer engines do not cite a local business because it
describes itself well; they cite it because GBP, Zomato, JustDial and a directory listing all
agree it exists, where it is, and what it does. That work returns in weeks, costs 1.5 days, and is
now Phase 0.6.

---

→ `INTERNAL_LINKING_BLUEPRINT.md`
