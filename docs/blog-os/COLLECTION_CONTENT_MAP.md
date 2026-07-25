# COLLECTION_CONTENT_MAP.md

**Satisfies completion conditions 6 and 7.** Every collection mapped to its supporting content and
its commercial role. Every active product covered by type.

Counts are **active** where stated. Collection `productsCount` includes drafts and is marked where
that materially misleads.

---

## 1. Coverage of active products, by type

602 active products. Coverage runs product → type → collection → pillar.

| Type | Active | Primary collection | Supporting pillar | Covered |
|---|---:|---|---|:---:|
| Theme Cake | **400** | `designer-theme-cakes`, `custom-cakes-meerut` + 9 theme collections | **CG-P1** + CG-1g/1h/1i | ✅ |
| Anniversary Cake | 83 | `anniversary-cakes` | **CG-P8** *(new)* | ✅ |
| Wedding Cake | 68 | `wedding-cakes` | **CG-P7** *(new)* | ✅ |
| Birthday Cake | 41 | `birthday-cakes` | CG-P2, CG-P3, CG-P4 | ✅ |
| Cake | 6 | `cakes` | CG-P2, CG-P3 | ✅ |
| Designer Cake | 1 | `custom-cakes-meerut` | CG-P1 | ✅ |
| Gift Hamper | **0** | `cake-hampers` | — **withheld** | n/a |
| Festive Hamper | **0** | `luxury-diwali-hampers` | — **withheld** | n/a |
| Bento Cake | **0** | — | CG-2d **held** | n/a |

**100% of active products are covered.** The three uncovered types have **zero active
inventory** — writing for them would drive traffic to an empty shelf.

**Theme Cake is 66% of the live catalogue.** Both v1 and v2 under-served it: v1 filed it under
listicles, v2 folded it into one shared pillar. CG-P1 gains three clusters and becomes the
highest-priority pillar in the plan.

---

## 2. All 35 collections

**Support** = enriched description + named supporting article(s).
**Dest** = whether the collection is itself a commercial destination for blog links.

### Tier 1 — pillar hubs and primary destinations (9)

| Collection | Count | Supporting content | Dest |
|---|---:|---|:---:|
| `cakes` | 985 | CG-P2 (sizing), CG-P3 (flavour), CG-P4 (cost) + enriched | ✅ |
| `custom-cakes-meerut` | 617 | **CG-P1** + CG-1a…1i + enriched | ✅ |
| `birthday-cakes` | 279 | CG-P2/P3/P4 + enriched | ✅ |
| `designer-theme-cakes` | 165 | **CG-P1**, CG-P6 (craft) + enriched | ✅ |
| `wedding-cakes` | 134 | **CG-P7** *(new)* + enriched | ✅ |
| `kids-birthday-cakes-meerut` | 128 | CG-P3, CG-1d + enriched | ✅ |
| `anniversary-cakes` | 102 | **CG-P8** *(new)* + enriched | ✅ |
| `showstopper-wedding-cake` | 77 | CG-P7 + CG-7e (setups) + enriched — **after Phase 0 repair** | ✅ |
| `photo-cakes` | 4 | CG-1e (source images) + enriched | ✅ |

### Tier 2 — theme collections, supported by enriched descriptions (10)

Each gets a 150–350 word enriched description linking up to `designer-theme-cakes`, across to 1–2
sibling themes, and down into CG-P1. **No dedicated article** — that was the `cake-ideas` error.

| Collection | Count | Dest |
|---|---:|:---:|
| `butterfly` | 23 | ✅ |
| `jungle-animal-theme` | 17 | ✅ |
| `unicorn` | 16 | ✅ |
| `boy-or-girl-cake` | 12 | ✅ |
| `motu-patlu` | 12 | ✅ |
| `chartered-accountant` | 10 | ✅ |
| `criciket` *(typo in handle)* | 10 | ✅ |
| `kpop-cake` | 9 | ✅ |
| `roblox` | 8 | ✅ |
| `ribbon-cake` (titled "Bow Cake") | 8 | ✅ |
| `teddy` | 7 | ✅ |
| `paw-petrol` *(typo in handle)* | 4 | ✅ |

*(12 rows — `criciket` and `paw-petrol` handles are misspelled. Left alone: they return 200 and
renaming costs a redirect for no gain. `CLAUDE.md` handle-optimization discipline applies.)*

### Tier 3 — audience and seasonal (4)

| Collection | Count | Supporting content | Dest |
|---|---:|---|:---:|
| `baby-girl` | 28 | enriched; CG-P2 (sizing for a first birthday) | ✅ |
| `winter-strawberry-collection` | 23 | enriched; CG-3e (fruit seasonality) | ✅ |
| `for-him` | **11** | enriched | ⚠️ thin |
| `for-her` | **1** | — **retire or stock** | ❌ |

### Tier 4 — hampers: supported content **withheld** (2)

| Collection | Count | Active | Verdict |
|---|---:|---:|---|
| `cake-hampers` | 119 | **0 by type** | Enrich the description only. **No pillar.** |
| `luxury-diwali-hampers` | 44 | **0 by type** | Enrich only. ME-3a references it, does not depend on it |

**Blocked on inventory, not on content.** Every hamper product is DRAFT. Publish-vs-archive is the
client's merchandising decision (`CLAUDE.md`), and until it is made, hamper content would rank for
queries the store cannot fulfil. A hamper pillar is drafted and held, not written.

### Tier 5 — retire, repair or `noindex` in Phase 0 (8)

| Collection | Count | Verdict |
|---|---:|---|
| `cake-delivery-meerut` | 985 | **301 → `/collections/cakes`.** Identical rule, identical products |
| `midnight-cake-delivery` | 985 | **301 → `/collections/cakes`** |
| `midnight-cake-delivery-meerut` | 985 | **301 → `/collections/cakes`** |
| `same-day-cake-delivery-meerut` | 985 | **301 → `/collections/cakes`** |
| `best-selling-products` | 1235 | Self-cancelling rule; returns everything incl. 588 drafts. **Fix or retire** |
| `newest-products` | 1235 | ″ |
| `all` | 1235 | Keep, `noindex` |
| `flowers-cake-combos` | **1** | **Retire or stock.** Indexable, full SEO metadata, no inventory |

Delivery *intent* moves to the pages layer (`/pages/cake-delivery-in-meerut`) and the `meerut`
silo. Four 301s, subject to the redirect-chain pre-check against the existing 820.

---

## 3. Every collection has a commercial destination

Condition 5 requires the reverse mapping too: every pillar must reach a page that takes an order.

| Pillar | Hub (links up) | **Commercial destination** (links down) |
|---|---|---|
| CG-P1 Custom ordering | `/collections/custom-cakes-meerut` | same + `designer-theme-cakes` |
| CG-P2 Sizing | `/collections/cakes` | same + `birthday-cakes` |
| CG-P3 Flavour | `/collections/cakes` | same |
| CG-P4 Cost & lead time | `/collections/cakes` | same + `wedding-cakes` |
| CG-P5 Eggless | `/pages/100-percent-eggless-bakery` | **`/collections/cakes`** ← added |
| CG-P6 Keeping & craft | `/pages/freshness-guarantee` | **`/collections/designer-theme-cakes`** ← added |
| **CG-P7 Wedding & event** | `/collections/wedding-cakes` | same + `showstopper-wedding-cake` |
| **CG-P8 Anniversary** | `/collections/anniversary-cakes` | same |
| ME-P1 Delivery | `/pages/cake-delivery-in-meerut` | **`/collections/cakes`** ← added |
| ME-P2 Celebrating | `/pages/about-us` | **`/collections/wedding-cakes`, `birthday-cakes`** ← added |
| ME-P3 Festive calendar | `/collections/luxury-diwali-hampers` | **`/collections/cakes`** ← added; hamper dest is inventory-blocked |

Five pillars previously had a page hub and **no commercial destination at all** — ME-P2 pointed
only at About Us. Fixed. Hub and commercial destination are now separate required fields, and no
article may be commissioned without both.
