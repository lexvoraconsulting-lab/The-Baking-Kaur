# BLOG_TAXONOMY.md — Controlled vocabulary

**v2.0.** Supersedes v1.0. Changes forced by `DESIGN_REVIEW.md`: F-04 (one article template),
F-05 (12 → 5 metafields), S-06/S-07 (tag surface), F-10/F-11 (4 → 2 silos), N-41 (52 → 20 tags).

---

## 1. Silos

| Handle | Name | Charter | Index template | City-scoped |
|---|---|---|---|---|
| `cake-guides` | Cake Guides | *Helps you decide, or explains how it works — true in any city.* | `blog.guides.json` | no |
| `meerut` | Meerut | *Only true in this city.* | `blog.city.json` | **yes** |
| `news` | News | *Dated announcements only.* Linked from nowhere. | default | no |

**One article template** — `article.json`, branching internally on `blog.handle`.
`Article.templateSuffix` is per-article and not inherited, so per-silo article templates would
mean configuring ~250 articles by hand (`DESIGN_REVIEW.md` F-04). Blog *index* templates are set
via `Blog.templateSuffix` and are safe.

### The boundary rule

> **Does the answer change if the city changes?**
> Yes → `meerut`. No → `cake-guides`.

Observable at commission time. Replaces v1's "reader's position relative to purchase", which was
not (`DESIGN_REVIEW.md` F-10). This matters because moving an article between blogs changes its
URL — **silo assignment is permanent**.

Worked examples:
- *"Midnight delivery: how it works"* → answer changes by city → **`meerut`**
- *"Which flavours hold up in summer heat"* → true anywhere → **`cake-guides`**
- *"What size cake for 20 guests"* → **`cake-guides`**
- *"Delivery to Pallavpuram"* → **`meerut`**

---

## 2. Subcategories

Editorial groupings, surfaced as a curated module on each blog index. Not URLs.

**`cake-guides`** — Choosing & sizing · Flavours · Cost & lead time · Custom design ·
Eggless & dietary · Keeping & serving · Inside the studio

**`meerut`** — Delivery & timing · Localities · Venues & events · City calendar

At ~160 and ~90 articles these indexes run ~14 and ~8 paginated pages. v1's 450-article silo ran
~38 pages with no sub-navigation and an uncrawlable tail (`DESIGN_REVIEW.md` S-14).

---

## 3. Tags — 20 maximum

Cut from 52. v1 sized its vocabulary for 920 articles; the target is ~250
(`DESIGN_REVIEW.md` N-41, F-16).

**Tags are for human browsing and related-content modules. They carry no link equity** — a
long-term `noindex` page is eventually treated as `nofollow` (`DESIGN_REVIEW.md` S-07). No article
may depend on a tag page as an inbound-link source.

### `occ-` Occasion (8)
`occ-birthday` · `occ-anniversary` · `occ-wedding` · `occ-baby` · `occ-diwali` · `occ-rakhi` ·
`occ-christmas-new-year` · `occ-corporate`

### `topic-` Subject (8)
`topic-sizing` · `topic-flavour` · `topic-cost` · `topic-custom-design` · `topic-eggless` ·
`topic-storage` · `topic-delivery` · `topic-studio`

### `loc-` Locality — **`meerut` silo only** (4 in use, extend only from verified zone data)
`loc-civil-lines` · `loc-shastri-nagar` · `loc-pallavpuram` · `loc-garh-road`

**Total: 20.** 2–4 tags per article. No new tag without retiring one.

### Tag page handling
`noindex, follow` on every `/blogs/*/tagged/*` URL — **including the `+`-combination forms**, which
make the surface combinatorial rather than the 208 pages v1 estimated
(`DESIGN_REVIEW.md` S-06). Implementation keys on `current_tags` being non-empty, which covers
both forms.

---

## 4. Prohibited tags

| Prohibited | Why |
|---|---|
| Any tag matching a collection handle (`unicorn`, `teddy`, `roblox`, `motu-patlu`, `butterfly`…) | Cannibalizes a live transactional URL |
| Format tags (`fmt-*` in v1) | Every format already **is** a collection. v1's `fmt-` namespace duplicated the catalogue |
| Audience tags (`aud-*` in v1) | Same — `for-him`, `for-her` are collections |
| Any city outside the `meerut` silo | Doorway pages |
| `best-*`, `top-*`, `cheap-*`, `premium-*` | Unverifiable claims frozen into URLs |
| Year tags | Breaks in-place seasonal refresh |
| `news`, `blog`, `misc`, `general` | Zero facet value; tag rot |
| Unprefixed tags | Prefix is what keeps the vocabulary auditable |
| Product tags | Separate vocabulary — 18 uncontrolled strings with inconsistent casing |

v1's `fmt-` and `aud-` namespaces (20 tags) are deleted outright. Both duplicated collections that
already exist, which is the same error as `cake-ideas` at the tag layer.

---

## 5. Article metafields — 5 required

Cut from 12. The store is on **Basic — no Shopify Flow**, so every field is typed by hand. v1
required 12 × ~900 = 10,800 manual entries (`DESIGN_REVIEW.md` F-05).

| Namespace.key | Type | Purpose |
|---|---|---|
| `custom.last_reviewed` | date | Drives `dateModified` **and** the visible on-page date. The fix for the `published_at` bug |
| `custom.cluster_id` | single_line_text | Parent pillar, e.g. `CG-P2`. Powers cluster-scoped related articles |
| `custom.hub_url` | url | The single up-link |
| `custom.about_refs` | list.mixed_reference | Product/Collection `@id`s for `Article.about` / `mentions` — the schema edge that closes the product loop |
| `custom.author_slug` | single_line_text | Resolves `Article.author` |

**Dropped and how they are handled instead:** `content_type`, `intent` → derivable from
`cluster_id` and blog handle. `answer_first`, `key_facts`, `faq_pairs` → **written into the body**,
where they belong; storing prose in metafields was overhead with no payoff once per-article
`FAQPage` was dropped (F-01). `sources` → inline links. `city` → derivable from blog handle.
`related_collections` → merged into `about_refs`.

---

## 6. Naming rules

| Element | Rule |
|---|---|
| Article handle | lowercase-hyphenated, 4–7 words, never repeats the blog handle, no dates, **immutable after publish** |
| City in handle | `meerut` silo only |
| `<title>` | ≤60 chars, primary keyword front-loaded, no brand suffix, **no superlatives** |
| H1 | may differ from `<title>`; must read as human |
| Meta description | 140–158 chars, must contain a concrete specific — a number, lead time, price floor or locality |
| Tag | prefixed, lowercase-hyphenated, from §3 only |
| Image filename | `{subject}-{silo}-the-baking-kaur.webp` |
| Image alt | descriptive sentence; never empty; never keyword-stuffed |
| **Silo assignment** | **immutable after publish** — moving blogs changes the URL |
