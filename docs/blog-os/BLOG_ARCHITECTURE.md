# BLOG_ARCHITECTURE.md — The Blog Operating System

# 🔒 **v2.1 — LOCKED 2026-07-24**

All 15 completion conditions pass (`COMPLETION_AUDIT.md`). No further architecture work.
Change control: any change to a locked element requires a numbered `DECISION_LOG.md` entry naming
what broke and which condition it affects. Re-open triggers are listed in `COMPLETION_AUDIT.md`.

Supersedes v2.0 (failed conditions 5, 6, 7, 13) and v1.0 (rejected in `DESIGN_REVIEW.md`, 6 fatal
findings). Design only. Nothing here is built.

**v2.1 changes:** verified active-product counts by type for the first time — **602 active, not
651**, with **Theme Cake at 400 (66%)** and **all hamper types at 0**. Two pillars added (wedding,
anniversary) covering 151 active products that had none. Hub and commercial destination separated
into two required fields. `EDITORIAL_STANDARDS.md`, `TEMPLATE_SPEC.md` and
`COLLECTION_CONTENT_MAP.md` added.

---

## 1. Platform constraints — verified, and binding

These are Shopify facts. v1 got two of them wrong and the design broke as a result.

| Constraint | Consequence |
|---|---|
| Article URL is fixed: `/blogs/{blog}/{article}` | The blog handle is the **only** hierarchy level. Silos must be blogs. |
| An article belongs to **exactly one** blog; moving it changes its URL | **Silo assignment is as permanent as the handle.** No design may leave a silo boundary ambiguous. |
| **`Article.templateSuffix` is per-article and is NOT inherited from `Blog.templateSuffix`** | Per-silo *article* templates would require manual configuration on every article. **One article template, branching on `blog.handle`.** `Blog.templateSuffix` controls the index template only — per-silo indexes are fine. |
| **Plan is Basic** — no Shopify Flow | No automation for metafield population. Every required field is typed by hand. **Required fields must be few.** |
| Basic — 2 staff accounts | No multi-role editorial workflow. Design for one operator. |
| `/blogs/{b}/tagged/{t}` **and `/tagged/{t1}+{t2}`** auto-generate | The tag surface is **combinatorial**, not linear. Must be `noindex`. |
| A long-term `noindex` page is eventually treated as `nofollow` | **Tag pages carry no link equity.** No article may depend on one for inbound links. |
| Blog index paginates `?page=N` only, no sub-indexes | Index depth is a hard constraint on silo size. |
| Article metafields supported on Basic | Structured per-article data available without apps. |
| 820 redirects already exist | Any new 301 must be checked for chaining. |

**Non-goals, stated explicitly:** no hreflang, no international, no Shopify Markets, no multi-
currency. Single market, `en-IN`.

---

## 2. The governing rule

> **One intent, one URL, one owner — and the owner is the page that can take an order whenever
> one exists.**

v1 had the first half. The second half is what `DESIGN_REVIEW.md` F-11 forced: v1's largest silo
was 20 articles that would have outranked the 20 collections they were meant to feed.

| Intent | Canonical owner | Blog's role |
|---|---|---|
| Transactional — "buy unicorn cake meerut" | **Collection** | never competes |
| **Inspirational — "unicorn cake ideas"** | **Collection** *(enriched description)* | **never competes — v2 change** |
| Service / policy — "do you deliver at midnight" | **Page** | never competes |
| Decision & understanding — "what size for 20 guests", "why is eggless not drier" | **Blog — `cake-guides`** | owns |
| Local — "delivery to Shastri Nagar" | **Blog — `meerut`** | owns |

**The commissioning test, applied before any article is written:**

1. *Does a collection or page already exist for this query?* → **Yes: it is not an article.** It is
   collection or page copy. Reject.
2. *Does the answer change if the city changes?* → **Yes: `meerut`. No: `cake-guides`.**

Test 2 replaces v1's untestable "reader's position relative to purchase" heuristic
(`DESIGN_REVIEW.md` F-10, S-08). It is observable at commission time, which is the only property
that matters given that silo assignment is permanent.

---

## 3. Silo design — two blogs

| Handle | Name | Charter | Scope | Launch | Ceiling |
|---|---|---|---|---:|---:|
| `cake-guides` | Cake Guides | *Helps you decide, or explains how it works — true in any city.* | brand | 53 | ~160 |
| `meerut` | Meerut | *Only true in this city.* | **city-scoped** | 18 | ~90 / city |

**Two, not four.** v1's `eggless-kitchen` and `cake-guides` were merged (the boundary was
ambiguous *and* permanent — the worst combination). v1's `cake-ideas` was **deleted**: 20 of its
38 launch articles mapped onto an existing collection, and a good article beats a thin collection
page, which is v1's own defined defect produced at scale.

**Silo count should equal the number of intents the business can serve with first-party
knowledge.** For a single-city eggless cake studio that is two. Authority comes from depth and
external corroboration, not from folder count — and a URL path is a weak-to-nil ranking signal in
any case (`DESIGN_REVIEW.md` M-15). Silos exist here for **link topology and human navigation**,
which is an honest reason and a sufficient one.

`news` is retained, linked from nowhere, charter: *dated announcements only — new location,
festive schedule, closure notices.* Nothing else may be filed there.

---

## 4. Where inspiration content actually goes

The single largest v2 change. v1's 450-article ideas silo becomes **35 enriched collection
descriptions.**

| | v1 | v2 |
|---|---|---|
| Surface | new article at `/blogs/cake-ideas/…` | existing `/collections/…` |
| Competes with the collection | **yes** | no |
| Converts | via a link | directly |
| Deploy needed | yes | **no — `descriptionHtml` is data** |
| Effort | ~450 articles | ~35 descriptions, 4 days |
| Images needed | original photography (blocked) | already on the collection |

Each enriched description gets: 150–350 words of genuine buying context, 2–3 internal links (up to
a hub page, across to 1–2 sibling collections), and — where one exists — a link to the
`cake-guides` article that serves the decision behind it.

**This also repairs the reverse edge.** Collection descriptions are the mechanism by which the
catalogue links *into* the blog, which is the only available direction given the protected product
template (§8).

Only where **no collection exists** does an ideas-shaped topic become an article, and it is filed
in `cake-guides` as a decision piece, not a listicle.

---

## 5. Content types

`HowTo` was deleted — Google deprecated the rich result, and the type had no other distinguishing
feature (`DESIGN_REVIEW.md` F-02).

| Type | Code | Words | Per silo | Refresh |
|---|---|---:|---|---|
| Pillar | `P` | 1,800–3,000 | 3–6 | 12 months |
| Cluster | `C` | 900–1,600 | 4–8 per pillar | 24 months |
| Local | `LO` | 700–1,200 | `meerut` only | 12 months |
| Seasonal | `S` | 800–1,500 | 6 total | **annual, in place** |

**Seasonal rule unchanged and reaffirmed:** updated in place at the same URL, forever.
`diwali-hamper-ideas-2027` is prohibited. This depends on a working `dateModified`, which is why
that fix is Phase 0.

**Seasonal content is calendar-anchored, not day-counted** (`DESIGN_REVIEW.md` M-35): each
seasonal piece must be live **6–8 weeks before** its peak — Diwali, wedding season, Valentine's,
Rakhi, Christmas/New Year.

---

## 6. Right-sizing — capacity vs target

v1 answered *"will this work with 1,000 articles?"* as a capacity question and set a 920 ceiling.
That ceiling was **4× the maintenance capacity** (`DESIGN_REVIEW.md` F-16).

**The refresh budget is the real constraint:**

```
sustainable output      = 4 articles / week  =  ~200 / year
refresh load at N       = N ÷ 2 years (avg cycle)
steady state            : new + refresh ≤ 200/year
                          N/2 + new = 200
at N = 250 :  125 refreshes + 75 new articles per year   ← sustainable
at N = 920 :  460 refreshes  →  exceeds total capacity    ← v1, fails
```

| | v1 | v2 |
|---|---:|---:|
| Launch set | 97 | **62** |
| Structural ceiling | 920 | **~250** |
| Timeline to launch set | 46 days | **~16 weeks** at 4/week |

**The architecture supports 1,000+ articles; the plan deliberately does not target it.** For a
single-city bakery with 602 active products, 1,000 articles would itself be the scaled-content
pattern Google's spam policy targets. Capacity and target are different questions and v1 conflated
them.

Index depth at 250: `cake-guides` ~160 articles ÷ 12 per page ≈ 14 pages. Acceptable. At v1's 450
it was ~38 pages and the tail was uncrawlable (`DESIGN_REVIEW.md` S-14).

---

## 7. Article anatomy — 4 required, the rest recommended

v1 mandated ten elements on every article. Enforced uniformity across hundreds of pages is itself
a Helpful-Content risk (`DESIGN_REVIEW.md` M-26).

**Required (4):**
1. **H1** matching the primary intent.
2. **A direct answer within the first 60 words.** Not a fixed-length block — just: answer the
   title before anything else. This is what gets extracted.
3. **Byline** — a named `Person` once available; `Organization` in the interim.
4. **`Last reviewed: {date}`**, visible, bound to `dateModified`.

**Recommended, used where they genuinely help:** key-facts list, Q&A prose, first-party evidence
(process photos, real lead times, real price bands), comparison table, conversion module.

**Q&A is prose, not schema.** `FAQPage` gets no rich result for a commercial site
(`DESIGN_REVIEW.md` F-01). Question-shaped subheadings with direct answers still serve LLM
extraction — that value comes from the *writing*, not the markup.

**Links:** 1 up, ≤2 lateral, ≤3 down. Convention, not law (`DESIGN_REVIEW.md` M-30).

---

## 8. Internal linking — and the product-page edge v1 missed

Hub-and-spoke, hub is always a collection or page. Detail in `INTERNAL_LINKING_BLUEPRINT.md`.

### Hub ≠ commercial destination (v2.1)

Every pillar and cluster carries **two required fields**:

| Field | Definition |
|---|---|
| **Hub** | The page the article links *up* to. May be a collection or a page. |
| **Commercial destination** | A **collection** the article links *down* to. Required even when the hub is a page. |

v2.0 conflated them, and five pillars ended up with a page hub and **no commercial destination at
all** — ME-P2 pointed only at `/pages/about-us`. That failed completion condition 5. An article
that cannot reach a page which takes an order is not part of a commercial content system.

Full mapping: `COLLECTION_CONTENT_MAP.md` §3. Enforced at the publish gate:
`EDITORIAL_STANDARDS.md` §7.

The v1 decision that the product↔blog loop was unclosable was **wrong**
(`DESIGN_REVIEW.md` F-27). It is unclosable in **HTML** — the product template is protected — but
fully available in **schema**, emitted from the *article* template:

```
Article
  ├ about    → Product/Collection @id   (the 1–2 things the article is really about)
  └ mentions → Product/Collection @id   (things referenced in passing)
```

Zero product-page changes. And a machine-readable article↔product edge is precisely what AI
retrieval traverses — so the edge v1 gave up on is the one that most mattered for the brief's
stated goal.

| Edge | v1 | v2 |
|---|---|---|
| Article → Product (HTML) | ✅ | ✅ |
| Collection → Article (HTML) | ✅ | ✅ |
| **Article ↔ Product (schema)** | ❌ declared impossible | ✅ **`about` / `mentions`** |
| Product → Article (HTML) | ❌ protected module | ❌ — accepted, unchanged |

---

## 9. Schema architecture

**Prerequisite:** delete the hardcoded `FAQPage` from `theme.liquid:68` (every URL, all 1,300+).

| Page type | Entities |
|---|---|
| Article | `Article` — `author`→`#person-*`, `publisher`→`#organization`, `isPartOf`→`#blog-*`, **`about`/`mentions`→Product/Collection** + `BreadcrumbList` |
| Blog index | `Blog` + `ItemList` + `BreadcrumbList` |
| Tag page | none — `noindex` |
| Author page | `ProfilePage` + `Person` |
| FAQ page | **one** `FAQPage`, sitewide, legacy-value only |
| Site-wide | one reconciled `Bakery` node + `WebSite` + **`Service` nodes** |

**Removed from v1:** per-article `FAQPage` (F-01), `HowTo` (F-02), `speakable` (F-03).

**Added in v2:**
- `Article.about` / `mentions` → Product/Collection (F-27).
- **`Service` nodes** (S-28) — Midnight Delivery, Same-Day Delivery, Custom Cake Design, Corporate
  Gifting; each with `provider`→`#organization`, `areaServed`, `hoursAvailable`. These are the
  business's actual services and v1 had one stub `makesOffer`.
- **≥6 `sameAs` nodes** on the organization (S-23) — entity disambiguation, not decoration.

**Repairs to existing snippets:**

| File | Change |
|---|---|
| `layout/theme.liquid:68` | **Delete** the hardcoded `FAQPage` |
| `tbk-schema-article.liquid` | `dateModified` → `custom.last_reviewed`, fallback `updated_at`, **never** `published_at` |
| `tbk-schema-article.liquid` | `author` → `#person-{slug}`; add `about` / `mentions` |
| `tbk-schema-website.liquid` + `bk-local-business.liquid` | Reconcile to **one** `@id`, one `sameAs` array, add GBP |
| new `tbk-schema-blog.liquid` | `Blog` + `ItemList` |

**Standing prohibition, reaffirmed:** no `aggregateRating`, no `review`, no rating count from any
source that is not a real verified review.

---

## 10. Entity & E-E-A-T layer

- One `Person` — founder/head baker — `@id` `#person-{slug}`, resolvable at
  `/pages/authors/{slug}`, `worksFor`→`#organization`, **≥2 external profiles** in `sameAs`
  (one is not enough to resolve a person — `DESIGN_REVIEW.md` M-29).
- **Interim state, defined:** articles ship with an `Organization` byline and are retro-updated in
  one pass when the identity arrives. v1 made every article depend on a blocked entity with no
  fallback.
- **Client-blocked:** name, title, photograph, bio, two profile URLs. No persona may be invented.

---

## 11. GEO — on-site *and* off-site

v1's entire GEO strategy was on-site. For a local business, **LLM answer engines cite what third
parties corroborate** (`DESIGN_REVIEW.md` F-21). A perfectly written page on an uncorroborated
domain does not get retrieved.

### On-site
Direct answer in the first 60 words · question-shaped subheadings · first-party evidence
(real lead times, real price bands, process photos, named baker) · resolvable entities ·
`about`/`mentions` product edges · honest `dateModified`.

### Off-site — the track v1 did not have

| Surface | Action | Value |
|---|---|---|
| **Google Business Profile** | Claim/verify; NAP identical to schema; weekly posts; GBP Q&A seeded from the 43 metaobjects; products; real photos | **Highest.** Feeds Maps, AI Overviews and every local LLM answer |
| **Zomato / Swiggy** | NAP consistency; correct category | Major India-specific corroboration |
| **JustDial / Magicpin** | Claim, NAP-consistent | Entity corroboration |
| **Instagram** | Already exists — make it a proper `sameAs` node with consistent NAP in bio | Corroboration + discovery |
| **Wedding directories** | WedMeGood, ShaadiSaga — Meerut vendor listings | Corroboration + qualified referral |
| **Local press / bloggers** | Earned mentions | Strongest citation signal available |

**NAP must be byte-identical everywhere**, including against the `Bakery` schema. `CLAUDE.md`
records a five-file NAP reconciliation cluster from Jul-19; that work is the input here.

### AI crawler access — an explicit decision (`DESIGN_REVIEW.md` S-22)

No custom `robots.txt.liquid` exists, so the current posture is an accident. **Decision: allow**
GPTBot, ClaudeBot, PerplexityBot, CCBot and Google-Extended. Recorded in `DECISION_LOG.md` D-024.
Note that `Google-Extended` governs Gemini grounding and is independent of `Googlebot`.

### The retrieval-lag reality (`DESIGN_REVIEW.md` S-24)

New articles on an unknown-authority domain are not retrieved or cited for months. So the roadmap
front-loads what can return sooner: the **off-site track** (weeks), **enriched collections** on
pages that already rank (weeks), and only then new articles (months).

---

## 12. Multi-city expansion

Only `meerut` is city-scoped. To add a city: create the blog, add `loc-*` tags, add a
`LocalBusiness` node, add the hub page, add nav. Done.

`cake-guides` is **never duplicated per city.** A guide to cake sizing is not different in Noida,
and publishing a Noida copy is the doorway-page pattern.

**Parameterise before city one** (`DECISION_LOG.md` D-009): `areaServed`, delivery radius, minimum
order, locality list, phone become metafield-driven. Two days now; a re-platforming job later.

Cross-city comparisons live in the larger city's silo and are canonical there.

---

## 13. Measurement — the layer v1 did not have

v1 proposed ~86 days of work with **no KPI and no attribution** (`DESIGN_REVIEW.md` F-31). Full
detail in `MEASUREMENT_PLAN.md`.

| Question | Metric | Mechanism |
|---|---|---|
| Is the content found? | impressions, avg position by silo | GSC — **access required** |
| Does it reach the catalogue? | clicks from article → collection | UTM on internal blog→collection links |
| Does it convert? | enquiries attributed to a blog page | **WhatsApp prefill source token** |
| Does it earn an owned asset? | email captures with occasion date | form on article + hub pages |
| Is it retrieved by AI? | branded/entity mentions in AI answers | monthly manual prompt panel |
| Is it maintainable? | articles past their refresh date | monthly audit script |

**WhatsApp source token** — the store's primary CTA is currently one fixed `wa.me` link, so every
enquiry looks identical (`DESIGN_REVIEW.md` S-32). Per-surface prefill makes the source visible in
the chat itself, with no analytics integration and no app:

```
wa.me/918218862928?text=Hi%2C%20I%20read%20your%20guide%20on%20cake%20sizes%20%5Bcg-p2%5D
```

---

## 14. Theme work

| Item | Action |
|---|---|
| **One** `article.json` | Branch internally on `blog.handle`. **Not** four suffixes (F-04) |
| Blog index templates | `blog.guides.json`, `blog.city.json` — index only, via `Blog.templateSuffix` |
| `blog-categories` link list | Create the menu the templates already expect |
| Sidebar bindings | Rebind `blog-default` / `list` → real handles |
| Comments block | Remove (blog has comments CLOSED) |
| Tag pages | `noindex, follow` — covers `+`-combination URLs too |
| Article template | Direct-answer position, byline, `Last reviewed`, cluster-scoped related, email capture |
| Nav | Fill `explore-cakes`, `quick-links`, `meerut-delivery`; add blog to `main-menu` |
| Verify | `social-meta-tags` emits `og:type=article` (N-38); articles appear in theme search (N-39) |
| Product page | **🔒 UNTOUCHED.** Schema edge (§8) closes the loop without it |

---

## 15. Quality gates — re-checked against the cluster map

v1 self-graded ✅ on gates its own cluster map failed (`DESIGN_REVIEW.md` N-42). Re-checked here
against `TOPIC_CLUSTER_MAP.md` v2, not against intent.

| Gate | Verdict | Evidence |
|---|---|---|
| No duplicate categories | ✅ | 2 silos, 2 disjoint charters, one testable boundary rule |
| No duplicate intent | ✅ design / ❌ inherited | Blog layer clean; the live 8-URL delivery collision is Phase 0 |
| No cannibalization | ✅ | Commissioning test 1 forbids an article where a collection exists; per-pillar collision table in the cluster map |
| Clear topic hierarchy | ✅ | 11 pillars, 1:4–8 ratio, **verified against the map** |
| Scales to 1,000+ | ✅ structurally | ~250 targeted deliberately; capacity and target separated (§6) |
| Strong topical authority | ✅ | Depth over breadth; eggless as the thesis; off-site corroboration |
| Strong local SEO | ✅ conditional | Conditional on GBP + real delivery data |
| Strong GEO | ✅ conditional | On-site + off-site; conditional on author identity and reviews |
| AI-search friendly | ✅ | Answer-first prose, resolvable entities, product schema edges, crawler allow |
| Easy to maintain | ✅ | Sized to refresh budget (§6); 5 metafields; 1 template; ~20 tags |

Two gates remain conditional. Both depend on client input or Phase 0 execution, not on
architecture. That is stated rather than graded away.

---

→ `BLOG_TAXONOMY.md` · `TOPIC_CLUSTER_MAP.md` · `INTERNAL_LINKING_BLUEPRINT.md` ·
`MEASUREMENT_PLAN.md` · `DESIGN_REVIEW.md`
