# INTERNAL_LINKING_BLUEPRINT.md

**v2.0.** Supersedes v1.0. Principal change: the product↔article edge v1 declared impossible is
available in schema (`DESIGN_REVIEW.md` F-27), and inspiration content now lives on collections,
which supplies the reverse edge for free.

---

## 1. Model

**The hub of every cluster is a collection or page, never an article.** The blog's job is to feed
the catalogue; if pillars were hubs, authority would accrue to `/blogs/*` instead of to pages that
can take an order.

```
     COLLECTION or PAGE  (hub — takes the order)
         ^         |
   1 up  |         | link down from the enriched description
         |         v
      PILLAR  (9 total)
         ^         |
   1 up  |         | 4-8 down
         |         v
     CLUSTERS  <--lateral, max 2-->  CLUSTERS
                   |
                   | max 3 down (HTML) + about/mentions (schema)
                   v
               PRODUCTS
```

**An article that outranks its hub is a defect, not a win.** The anchor policy (§4) exists to
prevent it, and the commissioning test (`TOPIC_CLUSTER_MAP.md`) prevents the article existing at
all where a collection already serves the query.

---

## 2. Link budget

Convention with a stated rationale, not a law (`DESIGN_REVIEW.md` M-30). The purpose is to keep
equity per link meaningful and to stop articles reading as link farms.

| Direction | Target | Count |
|---|---|:---:|
| **Up** | parent pillar, or the hub if this *is* the pillar | exactly 1 |
| **Lateral** | sibling clusters, same pillar | max 2 |
| **Down — collection** | from `custom.about_refs` | max 3 |
| **Down — product** | only where genuinely illustrative | max 3 |
| **Cross-silo** | the other silo's **pillar** only | max 1 |
| **External** | first-party evidence or genuine sources | as needed |

~10 internal links per article. Density ceiling: 1 link per 150 words.

**Cross-silo links go pillar-to-pillar only.** With two silos this is a light constraint, but it
keeps `meerut` and `cake-guides` legible as separate territories rather than one mesh.

---

## 3. The product edge — HTML is blocked, schema is not

`templates/product.json` renders `sections/main-product-premium-v2.liquid`, a **protected
module**. No related-articles widget. That is unchanged and not negotiable.

v1 concluded the product↔blog loop was therefore unclosable and wrote a decision record accepting
it. **That was wrong.** The edge exists in schema, emitted from the *article* template, touching
no product file:

```json
"about":    [{ "@id": "https://thebakingkaur.com/products/{handle}#product" }],
"mentions": [{ "@id": "https://thebakingkaur.com/collections/{handle}#collection" }]
```

| Edge | Mechanism | Touches product page? |
|---|---|---|
| Article → Product (HTML) | in-body, ≤3 | no |
| Article → Collection (HTML) | in-body + footer module | no |
| **Article ↔ Product (schema)** | **`about` / `mentions` from `custom.about_refs`** | **no** |
| **Collection → Article (HTML)** | **enriched `descriptionHtml`** | no |
| Page → Article (HTML) | in-body links in hub pages | no |
| Product → Article (HTML) | ❌ unavailable | — |

**The product page remains an HTML link sink.** Accepted, stated, not worked around. But it is no
longer *machine-invisible* — and machine-readable is what AI retrieval traverses, which is the
brief's headline goal.

---

## 4. Anchor text policy

| Rule | Reason |
|---|---|
| Never use a collection's exact primary keyword as anchor from an article | That is precisely how an article outranks the collection it exists to feed |
| Vary anchors across articles pointing at one target | Repeated exact-match at scale reads as manipulation |
| No "click here" / "read more" / "this page" | Zero signal |
| Anchor must make sense read aloud, out of context | Accessibility, and a reliable proxy for whether the link is natural |
| Never link the same target twice in one article | |
| **Never link a tag page from body copy** | Tag pages are `noindex` and carry no equity (`DESIGN_REVIEW.md` S-07) |

---

## 5. Per-silo behaviour

| Silo | Up to | Down to | Conversion module |
|---|---|---|---|
| `cake-guides` | pillar → collection or page hub | collections + products | collection CTA on decision-stage pieces; email capture on craft/eggless pieces |
| `meerut` | ME-P1 → `/pages/cake-delivery-in-meerut` | delivery page + collections | WhatsApp with source token + delivery page |

Decision-stage pieces (sizing, cost, flavour) point at collections — the reader is close to
buying. Craft and eggless pieces point at pages and capture email — the reader is not, and pushing
a collection at them wastes the link.

---

## 6. Collection descriptions — the reverse edge

The 35 enriched collection descriptions (`TOPIC_CLUSTER_MAP.md`) are the mechanism by which the
catalogue links **into** the blog. This is data, editable via the Admin API, **no theme deploy**.

Per collection: 150–350 words of buying context, plus
- 1 link up to a hub page,
- 1–2 links across to sibling collections,
- 1 link to the `cake-guides` article serving the decision behind the purchase — where one exists.

Never more than 4 links. A collection description is merchandising copy, not a link hub.

---

## 7. Navigation

Three empty menus already exist. Fill them; create no new ones.

**`explore-cakes`**
```
Cake Guides              /blogs/cake-guides
Meerut Delivery & Areas  /blogs/meerut
100% Eggless             /pages/100-percent-eggless-bakery
All Cakes                /collections/cakes
```

**`meerut-delivery`**
```
Cake Delivery in Meerut  /pages/cake-delivery-in-meerut
Midnight Delivery        /pages/midnight-cake-delivery
Delivery Areas           /blogs/meerut
Store Location           /pages/store-locator
```

**`quick-links`**
```
FAQs                /pages/frequently-asked-questions-faqs
Freshness Promise   /pages/freshness-guarantee
About the Baker     /pages/authors/{slug}    ← blocked on author identity
```

**`main-menu`** — add `Guides → /blogs/cake-guides`.

This resolves C6 and H6 in `CONTENT_GAP_ANALYSIS.md`: ten orphaned published pages plus the blog
re-enter the link graph. Half a day against High/High/Med impact — the best effort-to-impact ratio
in the roadmap after the schema fixes.

---

## 8. Article template modules

Structural, so linking discipline does not depend on editorial memory.

| Module | Source | Cap |
|---|---|---|
| Breadcrumb | `Home > {Blog} > {Article}` | — |
| Up-link | `custom.hub_url` | 1 |
| Related collections | `custom.about_refs` | 3 |
| Related articles | **same `cluster_id` only** | 4 |
| Sidebar categories | the 2 silos (fixes the broken `blog-categories` bind) | 2 |
| Sidebar recent | current silo only | 3 |
| Email capture | occasion-date field | 1 |
| Conversion | per §5, WhatsApp links carry a source token | 1 |

**Related articles filters on `cluster_id`, not "same blog".** The Ecomus `article_related` block
currently pulls 8 from the whole blog; at 160 articles that is random and dilutes the cluster.

---

## 9. Orphan prevention

An article is **orphaned** if fewer than 2 internal links point at it. Tag pages do not count —
they carry no equity (`DESIGN_REVIEW.md` S-07). v1 counted them, which made its orphan definition
unsound.

Every article receives, by construction:
1. a down-link from its pillar (pillars link to all their clusters — this is why pillars are
   capped at 6 per silo and clusters at 8 per pillar),
2. a listing on its blog index,
3. inclusion in ≥1 sibling's cluster-scoped related module.

**Audit script — a named Phase 1 deliverable, not an aside.** v1 leaned every governance claim on
a "~40 line" script that did not exist (`DESIGN_REVIEW.md` M-19). Spec:

- input: all articles via Admin API
- extract every `<a href>` from `article.body` and every collection `descriptionHtml`
- build the inbound-count map; flag anything under 2
- flag any article past `custom.last_reviewed` + its refresh interval
- dry-run by default, CSV out, per `seo-ops/` convention in `docs/CODING_STANDARDS.md`

Owner and phase: Phase 1, before the first pillar publishes.

---

## 10. What must not happen

| Anti-pattern | Why banned here |
|---|---|
| An article where a collection already serves the query | The `cake-ideas` failure. Commissioning test 1 |
| Auto-generated related posts by tag across both blogs | Merges the silos into one mesh |
| Sitewide footer block of article links | Dilutes every page |
| An article outranking its hub | The blog exists to feed the catalogue — fix the anchors, don't celebrate the ranking |
| Body links to tag pages | `noindex`, no equity, dead end |
| Cross-city article linking | Creates the doorway-page footprint |
| Product-page link modules | Protected module. Use the schema edge (§3) |
| Relying on tag pages for inbound links | Long-term `noindex` → effectively `nofollow` |
