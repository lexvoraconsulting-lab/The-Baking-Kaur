# CONTENT_TEMPLATES.md — Phase 2F

**6 templates.** The brief lists 13. Four of the 13 would violate the locked architecture and are
mapped elsewhere; three are properties rather than templates. Reconciliation in §8 — nothing is
silently dropped.

Every template maps to one of the 4 locked content types (`P · C · LO · S`).

---

## T1 · Pillar Guide `P`

**Purpose.** Own a decision space. The canonical answer to a broad question, and the hub for 4–8
clusters.
**Use for.** All 11 pillars.
**Length.** 1,800–3,000 · **Update.** 12 months

```
H1 — the decision, phrased as the reader would
Direct answer, ≤60 words — standalone, quotable
Key facts — 3–5 concrete specifics
H2 The short version         (the whole answer in ~150 words, for skimmers and extraction)
H2 [Dimension 1]  H3 sub · H3 sub
H2 [Dimension 2]
H2 [Dimension 3]
H2 How this works at The Baking Kaur   ← first-party section. The differentiator
H2 Common questions          (2–4, prose subheadings, not schema)
H2 What to do next           → commercial destination
Byline · Last reviewed
```

**Links.** 1 up (hub) · **all** its clusters down · ≤3 collections · ≤3 products · ≤1 cross-silo
**Schema.** `Article` + `BreadcrumbList` + `about`/`mentions`
**Media.** 1 lead image + 2–4 inline. All original.
**CTA.** Collection.

> A pillar that does not link to every one of its clusters breaks orphan prevention — pillars are
> the primary inbound link for their clusters.

---

## T2 · Decision Cluster `C`

**Purpose.** Answer one narrow question completely. The workhorse — ~45 of 71 launch articles.
**Use for.** Sizing, flavour, cost, custom-ordering, wedding, anniversary clusters.
**Length.** 900–1,600 · **Update.** 24 months

```
H1 — the specific question
Direct answer, ≤60 words
H2 [The main consideration]
H2 [The trade-off or the exception]
H2 What we'd suggest          ← first-party opinion, stated plainly
H2 One or two questions people ask
H2 Next step                  → commercial destination
Byline · Last reviewed
```

**Links.** 1 up (pillar) · ≤2 lateral · ≤3 collections · ≤3 products
**Schema.** `Article` + `BreadcrumbList` + `about`/`mentions`
**Media.** 1–3 original images. **Text-only is acceptable** and preferable to padding with
unusable assets while photography is blocked.
**CTA.** Collection.

---

## T3 · Craft Explainer `C`

**Purpose.** Demonstrate expertise. The E-E-A-T and LLM-citation engine — nothing else in the
system carries knowledge only this studio has.
**Use for.** CG-P5 (eggless) and CG-P6 (craft) clusters.
**Length.** 900–1,600 · **Update.** 24 months

```
H1 — the thing people get wrong, or genuinely wonder
Direct answer, ≤60 words
H2 What's actually happening      (the mechanism, plainly)
H2 Why it matters to you
H2 How we handle it               ← the first-party core. Specific process, real numbers
H2 What we can't do               ← honesty section. REQUIRED
H2 Related question
Byline · Last reviewed
```

**Links.** 1 up · ≤2 lateral · ≤2 **pages** · ≥1 collection (locked condition 5)
**CTA.** Email capture primary; collection secondary. The reader is not buying yet.

> **"What we can't do" is mandatory in this template.** It is the single strongest trust signal
> available, it is what R12 (Customer) rewards, and it is the thing content written for search
> never contains.

---

## T4 · Local Guide `LO`

**Purpose.** Own a query that is only true in this city.
**Use for.** All `meerut` silo articles.
**Length.** 700–1,200 · **Update.** 12 months

```
H1 — includes the locality or the city
Direct answer, ≤60 words — must contain a REAL specific
H2 What we can actually do here    ← real windows, real fees. NOT generic
H2 How to order for this area
H2 What to know locally             (traffic, timing, venue quirks — real knowledge)
H2 Next step                        → delivery page + collection
Byline · Last reviewed
```

**Links.** 1 up (ME-P1 or ME-P2) · ≤2 lateral · delivery page · ≥1 collection
**Media.** Optional. **Never a stock "map" image.**
**CTA.** WhatsApp with source token + delivery page.

> **Hard gate (G5):** no locality-specific fact → not publishable. Ever. A locality article without
> a real window or fee band is a doorway page, and volume pressure is exactly when this rule gets
> tested.

---

## T5 · Seasonal Guide `S`

**Purpose.** Own a recurring calendar moment, permanently, at one URL.
**Use for.** ME-P3 clusters — Diwali, Rakhi, wedding season, Christmas/New Year, Valentine's.
**Length.** 800–1,500 · **Update.** **Annually, in place, at the same URL**

```
H1 — the occasion, no year
Direct answer, ≤60 words — includes the ordering deadline
H2 When to order                   ← the whole reason this ranks
H2 What works for this occasion
H2 Bulk and corporate              (only if inventory supports it)
H2 Next step
Byline · Last reviewed  ← the load-bearing field for this template
```

**Rules.**
- **No year in the handle, title, or H1.** `diwali-hampers-2027` never exists.
- **Live 6–8 weeks before the peak**, not when the day-count reaches it.
- Annual refresh = re-verify dates, prices and lead times, then update `last_reviewed`.
  **A date bump without re-reading is a freshness lie.**

---

## T6 · Collection Enrichment — *not an article*

**Purpose.** Own inspirational and browse intent **on the collection page**, where the products
already are.
**Use for.** All 35 collections. This is what replaced v1's 450-article `cake-ideas` silo.
**Length.** 150–350 words in `descriptionHtml` · **Update.** 24 months, or on range change

```
Opening — what this range is and who it's for  (2-3 sentences)
The practical bit — sizes, flavours, lead time, price floor
What makes ours different                      (eggless, hand-finished, made to order)
Links: 1 up (hub page) · 1-2 sibling collections · 1 guide article where one exists
```

**No theme deploy** — `descriptionHtml` is data, editable via the Admin API.
**Max 4 links.** A collection description is merchandising copy, not a link hub.
**Not tracked in `blog_master.csv`** — tracked in `COLLECTION_CONTENT_MAP.md`.

---

## 7. Selection

```
Is it a collection or page query?          → T6 (or nothing)
Is it only true in this city?              → T4
Is it a calendar moment?                   → T5
Does it own a whole decision space?        → T1
Is it about how the craft works?           → T3
Otherwise                                  → T2
```

---

## 8. The 13 requested templates, reconciled

Nothing dropped without a reason.

| Requested | Resolution |
|---|---|
| **Buying Guide** | → **T2**. Same thing under a different name |
| **How-To** | → **T3**. The separate How-To type was deleted in v2 — `HowTo` schema is deprecated and it had no other distinguishing feature |
| **Comparison** | → **T2**. A comparison is a decision cluster ("truffle vs mousse"). A separate template would produce near-identical output |
| **Local Guide** | → **T4** ✓ |
| **Occasion Guide** | → **T6**. Occasions **are** collections (`birthday-cakes`, `anniversary-cakes`). An occasion article would outrank the collection it feeds — the `cake-ideas` failure. **Blocked by locked condition** |
| **Theme Guide** | → **T6**. Same reason. Themes are 12 live collections |
| **Cake Inspiration** | → **T6**. This was the deleted silo. Inspiration lives where the images and products are |
| **Gift Guide** | → **T6**, and **withheld** — Gift Hamper and Festive Hamper have **0 active products**. Content would drive traffic to an empty shelf |
| **Corporate Guide** | → **a page**, not an article. `/pages/corporate-gifting-solutions` publishes in Phase 0.3. Also inventory-blocked |
| **FAQ** | → **not a template**. One `FAQPage` site-wide on `/pages/faqs` from the 43 metaobjects. Per-article FAQ is prose inside T1–T5 |
| **Knowledge Base** | → **T3**. That is what the craft explainer is |
| **Landing Article** | → **a collection**, not an article. In this architecture the landing page for commercial intent is always the collection |
| **Evergreen Article** | → **a property, not a template.** T1–T4 are all evergreen; T5 is the only seasonal one. A separate template would encode nothing |

**Four requested templates (Occasion, Theme, Inspiration, Gift) would each produce articles that
outrank the collections they exist to feed** — the exact defect that got v1's largest silo deleted
(`DESIGN_REVIEW.md` F-11). They are routed to T6, which serves the same intent from a page that
converts.

Two more (Corporate, Landing) belong to the pages/collections layer, not the blog.

The architecture is not being redesigned here — **implementation revealed the collision**, which is
the stated condition for pushing back, and the resolution keeps every requested intent served.

---

## 9. Template governance

- A new template requires a `DECISION_LOG.md` entry stating which intent no existing template
  serves.
- **Templates are skeletons, not scripts.** If three articles in a cluster read identically,
  the template is being followed too literally — vary them (G8, R1).
- Any template change is versioned; live articles are not retrofitted except at their next
  scheduled refresh.
