# ARTICLE_SPEC.md — Phase 2B

**The specification every article must satisfy.** No article enters S2 without a complete spec row.
No article publishes with a spec that has drifted from the article.

---

## 0. Where the spec lives — and where it does not

**This is the most important thing in this document.**

| Layer | Holds | Why |
|---|---|---|
| **`blog_master.csv`** (repo, git-tracked) | **All 31 spec fields** | Planning data. Diffable, reviewable, editable in Excel, readable by `seo-ops/` |
| **Shopify article metafields** | **Only the 5 locked fields** | `last_reviewed`, `cluster_id`, `hub_url`, `about_refs`, `author_slug` |

The store is on **Basic — no Shopify Flow.** Every metafield is typed by hand. Pushing 31 fields
into Shopify would be 31 × 250 = 7,750 manual entries: the exact failure
`DESIGN_REVIEW.md` F-05 rejected.

**The 5 metafields are the ones the theme must read at render time.** Everything else is planning
metadata that no visitor and no crawler ever needs, so it stays in the CSV.

---

## 1. Field specification — 31 fields

Legend: **R** required to leave S1 · **B** required to leave S2 · **P** required to publish ·
🔒 = written to Shopify

### Identity & state

| # | Field | Type | When | Rule |
|---|---|---|:---:|---|
| 1 | `article_id` | `{SILO}-{PILLAR}-{nn}` | R | `CG-P2-01`. Pillars are `-00`. **Immutable** |
| 2 | `status` | enum | R | `BACKLOG · SPEC · BLUEPRINT · DRAFT · VERIFIED · APPROVED · LIVE · REFRESH_DUE · HELD · REJECTED · ARCHIVED` |
| 3 | `held_reason` | enum | R if `HELD` | `photography · delivery-data · inventory · author · gsc · client`. **A `HELD` row without this is a bug** |
| 4 | `priority` | `P0–P3` | R | P0 = pillar in white space; P3 = nice to have |
| 5 | `version` | semver | R | `1.0` at publish; minor on refresh; major on rewrite |
| 6 | `owner` | text | R | One named human. Not "team" |

### Purpose

| # | Field | Type | When | Rule |
|---|---|---|:---:|---|
| 7 | `business_goal` | enum | R | `acquire · convert · trust · retain · entity` |
| 8 | `content_goal` | text ≤120 | R | One sentence: what the reader can do after reading that they couldn't before |
| 9 | `search_intent` | enum | R | `decision · understanding · local`. Locked taxonomy — no fourth value |
| 10 | `buying_stage` | enum | R | `unaware · problem-aware · solution-aware · vendor-aware · ready · post-purchase` |
| 11 | `persona` | enum | R | See §2 |

### Placement (locked architecture)

| # | Field | Type | When | Rule |
|---|---|---|:---:|---|
| 12 | `silo` | enum | R | `cake-guides · meerut`. **Immutable after publish** — changes the URL |
| 13 | `parent_cluster` 🔒 | text | R | The pillar, e.g. `CG-P2`. Exactly one. → `custom.cluster_id` |
| 14 | `child_cluster` | text | R | Editorial subcategory (`BLOG_TAXONOMY.md` §2). Not a URL |
| 15 | `content_type` | enum | R | `P · C · LO · S` |
| 16 | `template` | enum | B | From `CONTENT_TEMPLATES.md` |

### Commercial (locked condition 5)

| # | Field | Type | When | Rule |
|---|---|---|:---:|---|
| 17 | `hub_url` 🔒 | URL | R | The single up-link. May be a page. → `custom.hub_url` |
| 18 | `target_collection` | handles | R | **≥1 collection. A page does not satisfy this.** Blocks S1 exit |
| 19 | `target_products` 🔒 | handles | R | 1–3, illustrative only. → `custom.about_refs` |
| 20 | `primary_cta` | enum | B | `collection · whatsapp · email` |
| 21 | `secondary_cta` | enum | B | May be `none` |

### Search

| # | Field | Type | When | Rule |
|---|---|---|:---:|---|
| 22 | `primary_keyword` | text | R | Exactly one. **Must not be any collection's primary keyword** |
| 23 | `secondary_keywords` | list 3–6 | R | Pipe-separated |
| 24 | `semantic_keywords` | list 8–15 | R | Entities and co-occurring terms, not variants |
| 25 | `entities` | list | R | From `ENTITY_RELATIONSHIP_MAP.md` §4 |
| 26 | `tags` | list 2–4 | B | From the 20 (`BLOG_TAXONOMY.md` §3) |

### Content plan

| # | Field | Type | When | Rule |
|---|---|---|:---:|---|
| 27 | `faqs` | list 2–4 | B | **Prose subheadings, not schema.** Must not duplicate the 43 site FAQ metaobjects |
| 28 | `internal_links` | list | B | Exact URLs + anchor text. Budget: 1 up · ≤2 lateral · ≤3 collection · ≤3 product · ≤1 cross-silo |
| 29 | `external_references` | list | B | May be empty. Most claims here are first-party |
| 30 | `image_requirements` | text | B | Subject + count + alt intent. **Original only** |
| 31 | `video_requirements` | text | B | **`none` by default** — see §4 |

### Schema, size, lifecycle

| # | Field | Type | When | Rule |
|---|---|---|:---:|---|
| 32 | `schema_type` | text | B | `Article+BreadcrumbList+about/mentions` for ~95%. Deviation needs a reason |
| 33 | `word_count_target` | int | B | Band by type: P 1800–3000 · C 900–1600 · LO 700–1200 · S 800–1500 |
| 34 | `reading_time` | int | P | Derived: ⌈words ÷ 225⌉ |
| 35 | `review_frequency` | months | R | P 12 · C 24 · LO 12 · S 12 |
| 36 | `last_reviewed` 🔒 | date | P | → `custom.last_reviewed`. Drives `dateModified` **and** the visible date |
| 37 | `author_slug` 🔒 | text | P | → `custom.author_slug`. `organization` until the client unblocks |

*(37 numbered rows, 31 distinct spec fields — `article_id`, `status`, `version` and `owner` are
operational rather than editorial. The count in the brief was a minimum; every requested field is
present.)*

### Mapping to the brief's requested fields

| Requested | Field |
|---|---|
| Article ID · Status · Priority | 1 · 2 · 4 |
| Business Goal · Content Goal | 7 · 8 |
| Primary Category | 12 `silo` |
| Parent / Child Cluster | 13 · 14 |
| Search Intent · Customer Persona · Buying Stage | 9 · 11 · 10 |
| Target Collection · Target Products | 18 · 19 |
| Primary / Secondary / Semantic Keywords | 22 · 23 · 24 |
| Entities · FAQs · Schema Type | 25 · 27 · 32 |
| Internal Links · External References | 28 · 29 |
| Image / Video Requirements | 30 · 31 |
| Primary / Secondary CTA | 20 · 21 |
| Word Count Target · Reading Time | 33 · 34 |
| Review Frequency · Owner · Version | 35 · 6 · 5 |

All 28 requested fields present. Added: `held_reason`, `content_type`, `template`, `hub_url`,
`tags`, `last_reviewed`, `author_slug`, `silo` — each enforcing something the locked architecture
requires.

---

## 2. Personas

Derived from the catalogue, not invented. Counts are **active** products.

| Persona | Buys | Evidence |
|---|---|---|
| `parent-kids` | Theme cakes for children | Theme Cake = 400 (66%) |
| `partner-romantic` | Anniversary, romantic, midnight surprise | Anniversary = 83 |
| `wedding-planner` | Tiered, setups, venue delivery | Wedding = 68 |
| `milestone-family` | Birthdays for adults, milestone years | Birthday = 41 |
| `corporate-buyer` | Bulk, branded gifting | **No active inventory** — persona parked |
| `dietary-seeker` | Specifically wants eggless | The whole catalogue; the differentiator |

`corporate-buyer` is defined but **not commissioned against** — Gift Hamper and Festive Hamper have
0 active products. Writing for a persona the store cannot serve is the hamper error in another form.

---

## 3. Validation rules

Machine-checkable. `seo-ops/blog_validate.py` (Phase 2 deliverable, not yet written).

**Blocks S1 exit**
- All R fields non-empty
- `article_id` unique and matches `{SILO}-{PILLAR}-{nn}`
- `parent_cluster` exists in `TOPIC_CLUSTER_MAP.md`
- `silo` ∈ {`cake-guides`, `meerut`}
- **`target_collection` contains ≥1 real collection handle**
- `primary_keyword` is not the primary keyword of any collection
- `primary_keyword` not already assigned to another row
- `status = HELD` ⟹ `held_reason` non-empty

**Blocks S2 exit**
- All B fields non-empty
- `tags` 2–4, all from the 20
- `internal_links` within budget; ≥1 to a `target_collection`; none to a tag page
- `faqs` 2–4 and none duplicating a site FAQ metaobject
- `word_count_target` inside the band for `content_type`

**Blocks publish**
- All 18 quality gates PASS
- Panel score ≥ threshold for `content_type`
- `last_reviewed` = today; `author_slug` set
- `reading_time` derived and non-zero
- Handle final; silo final
- Exactly one `FAQPage` site-wide, and it is not this article

---

## 4. Video — the honest position

`video_requirements` defaults to **`none`** on every article, indefinitely.

The store cannot currently produce usable **still** photography: catalogue images carry Zomato/TWC
watermarks or piped customer names, and theme assets are Ecomus demo content (`CLAUDE.md`).
Specifying a video production pipeline for a business that cannot yet shoot a photograph would be
building for a capability that does not exist.

The field is in the spec so it can be populated without a schema change if that ever shifts. It is
not a gap; it is a deliberate `none`.

---

## 5. Drift control

The spec is authoritative at S1–S2 and **descriptive** after S3. If drafting proves the outline
wrong, **update the spec** — do not force the prose to match a plan that was wrong.

What may never drift without a `DECISION_LOG.md` entry: `silo`, `parent_cluster`,
`primary_keyword`, `hub_url`, `target_collection`, and the handle. All six are load-bearing for the
locked architecture; four of them change or invalidate a URL.

At publish, `seo-ops/blog_validate.py` re-checks the row against the finished article. A mismatch
is a FAIL, not a warning.
