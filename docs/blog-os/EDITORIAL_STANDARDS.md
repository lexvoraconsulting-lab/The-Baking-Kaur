# EDITORIAL_STANDARDS.md

**Satisfies completion condition 13.** Voice and copy rules are **not** duplicated here — they live
in `BRAND_VOICE.md` and `COPY_GUIDELINES.md` at the repo root. This file covers what those do not:
verification, structure, images, and the publish gate.

---

## 1. Non-negotiables

Violating any of these blocks publication. No exceptions, no "just this once".

| Rule | Why |
|---|---|
| **No claim without a source.** No rating, review count, certification, award, delivery promise or superlative that cannot be pointed at | Standing project rule. It has already caused three removals |
| **No invented facts.** No GTINs, MPNs, barcodes, licence numbers, reviews, or persona | `CLAUDE.md` |
| **No "best", "top", "leading", "#1"** unless attributed to a named third party with a link | The shop meta description already carries an unverified "best bakery"; do not add more |
| **No delivery promise the store cannot keep.** Slot claims come from `SERVICE_AREA_ZONE_MAP.md` / `PROPOSED_DELIVERY_CONFIG.md`, never from the writer | A missed promise costs more than the traffic earns |
| **No locality article without a locality-specific fact** — a real window, a real fee band | Without it, it is a doorway page |
| **No competitor named** in comparisons | Nothing to gain; real risk |
| **Prices are ranges with a "from", never exact** unless read from the live product | Prices change; articles do not |

---

## 2. Verification

Every factual statement falls into one of three buckets, and each has a required source.

| Bucket | Source of truth | Example |
|---|---|---|
| **Catalogue fact** — sizes, flavours, price floors, lead times | Admin API, read at writing time | "available in 1 kg, 1.5 kg and 2 kg" |
| **Operational fact** — delivery windows, fees, cut-offs, minimum order | `SERVICE_AREA_ZONE_MAP.md`, `PROPOSED_DELIVERY_CONFIG.md` | "order before 4 PM for evening delivery" |
| **Craft claim** — technique, storage life, ingredient behaviour | The studio. Ask; do not infer | "eggless sponge holds structure because…" |

**If a fact cannot be placed in a bucket, it does not go in the article.** Writing around a gap is
acceptable; guessing is not.

Catalogue facts are re-checked at every refresh. An article quoting a price floor that has moved is
worse than one that never quoted it.

---

## 3. Structure

Required on every article (4). From `BLOG_ARCHITECTURE.md` §7 — reduced from v1's ten, because
enforced uniformity across hundreds of pages is itself a Helpful-Content risk.

1. **H1** matching the primary intent.
2. **A direct answer within the first 60 words.** Answer the title before doing anything else.
3. **Byline** — a named `Person` once available; `Organization` in the interim.
4. **`Last reviewed: {date}`**, visible, bound to `custom.last_reviewed` and to `dateModified`.

Recommended, used where they genuinely help — not on a schedule: key-facts list, question-shaped
subheadings, first-party evidence, comparison table, conversion module.

**Deliberate variation is required.** If three consecutive articles in a cluster open the same way,
rewrite one. Formulaic output is the failure mode this section exists to prevent.

### Length by type

| Type | Words |
|---|---|
| Pillar `P` | 1,800–3,000 |
| Cluster `C` | 900–1,600 |
| Local `LO` | 700–1,200 |
| Seasonal `S` | 800–1,500 |

Under the floor: it is a section of another article, not an article. Over the ceiling: it is two.

---

## 4. Metadata

| Element | Rule |
|---|---|
| `<title>` | ≤60 chars, primary keyword front-loaded, no brand suffix, no superlative |
| H1 | may differ from `<title>`; must read as human |
| Meta description | 140–158 chars, **must contain a concrete specific** — a number, lead time, price floor or locality — not a restatement of the title |
| Handle | lowercase-hyphenated, 4–7 words, never repeats the blog handle, no dates, **immutable after publish** |
| Silo | **immutable after publish** — moving blogs changes the URL |
| Tags | 2–4, from the 20 in `BLOG_TAXONOMY.md` §3 |

---

## 5. Images

| Rule | Detail |
|---|---|
| **Original photography only** | No stock, no Ecomus demo assets, no scraped images |
| **No watermarked catalogue images** | Existing assets carry Zomato/TWC watermarks or piped customer names — unusable in editorial |
| **No customer image without written permission** | Including images already on product pages |
| Filename | `{subject}-{silo}-the-baking-kaur.webp` |
| Alt text | Descriptive sentence naming the subject. Never empty, never stuffed |
| Format / size | WebP, ≤200 KB, longest edge 1600 px |
| Lead image | Required on pillars; optional on clusters |
| Pinterest assets | 2:3 vertical, and they point at **products/collections, not articles** |

**Most of this silo is image-gated.** Until a studio shoot happens, prefer text-only articles over
padding with unusable assets — that constraint is why `cake-ideas` was deleted rather than deferred.

---

## 6. Links

From `INTERNAL_LINKING_BLUEPRINT.md`. Restated because it is a publish-gate item.

- 1 up (hub) · ≤2 lateral (same pillar) · ≤3 down to collections · ≤3 down to products ·
  ≤1 cross-silo (pillar only).
- **At least one link to a commercial destination.** A pillar whose hub is a page must still reach
  a collection (`COLLECTION_CONTENT_MAP.md` §3).
- Never the collection's exact primary keyword as anchor.
- Never link a tag page from body copy.
- ~1 link per 150 words.

---

## 7. Publish gate

Every item, every article. Failing one blocks publication.

**Content**
- [ ] Title ≤60, no superlative, keyword front-loaded
- [ ] Direct answer in the first 60 words
- [ ] Every fact traced to a bucket (§2)
- [ ] No unsourced claim, no invented fact, no unkeepable promise
- [ ] Length inside the band for its type
- [ ] Does not open like the last two articles in its cluster

**Structure & links**
- [ ] `cluster_id` set; exactly one parent
- [ ] `hub_url` set; 1 up-link present
- [ ] **≥1 link to a commercial destination**
- [ ] Link budget respected; no tag-page links
- [ ] 2–4 tags from the controlled vocabulary

**Technical**
- [ ] 5 metafields populated (`BLOG_TAXONOMY.md` §5)
- [ ] `about_refs` set → `Article.about` / `mentions` resolve
- [ ] `last_reviewed` set; visible on page; `dateModified` reflects it
- [ ] Schema validates; **exactly one `FAQPage` on the site**, and it is not this page
- [ ] Handle final — it cannot change after this
- [ ] Silo final — it cannot change after this
- [ ] Images original, alt text present, WebP, ≤200 KB
- [ ] WhatsApp CTA carries its source token (`MEASUREMENT_PLAN.md` §4)

**Sign-off:** one named reviewer, not the writer. On a 2-staff Basic plan that is the owner. If the
writer and reviewer are the same person, the article waits 24 hours before publication — a delay is
a weaker check than a second pair of eyes, but it is a real one.

---

## 8. Refresh

| Type | Cycle |
|---|---|
| Pillar | 12 months |
| Cluster | 24 months |
| Local | 12 months |
| Seasonal | **Annual, in place, at the same URL** |

**A refresh is a re-verification, not a date bump.** Re-check every catalogue and operational fact
against source, then update `last_reviewed`. Changing the date without re-reading the article is a
freshness lie, and it is exactly what the broken `dateModified` bug already does by accident.

**Year-suffixed URLs are prohibited.** `diwali-hamper-ideas-2027` never exists.

**Refresh debt is a stop condition:** if more than 20% of published articles are past their refresh
date for two consecutive months, new production halts until it clears
(`MEASUREMENT_PLAN.md` §7). That rule is what keeps the library inside the capacity envelope in
`BLOG_ARCHITECTURE.md` §6.
