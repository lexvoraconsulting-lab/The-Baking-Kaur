# QUALITY_GATES.md — Phase 2D

**18 gates. Every gate PASS/FAIL. Any FAIL blocks the article.**

No gate is a judgement call — each has a stated measurement. Where a gate needs a human, the human
is answering a closed question, not forming an impression.

**Auto** = scripted by `seo-ops/blog_gates.py` (Phase 3 deliverable). **Manual** = operator, ≤2 min.

| # | Gate | Mode | Runs at |
|---|---|---|---|
| 1–4 | Technical SEO, On-page SEO, Schema, Internal Linking | Auto | S4 |
| 5–7 | Local SEO, GEO, Trust | Mixed | S4 |
| 8–11 | Helpful Content, E-E-A-T, Originality, Completeness | Manual | S4 |
| 12–14 | Readability, Grammar, Brand Voice | Mixed | S4 |
| 15–16 | External References, Accessibility | Auto | S4 |
| 17–18 | Performance, Conversion | Auto | S4 |

---

## G1 · Technical SEO — Auto

| Check | PASS |
|---|---|
| `<title>` length | ≤60 characters |
| Title contains primary keyword | yes |
| Meta description length | 140–158 characters |
| Meta description contains a concrete specific | a number, lead time, price band or locality present |
| Handle | 4–7 words, lowercase-hyphenated, no date, does not repeat the blog handle |
| H1 count | exactly 1 |
| Heading order | no skipped levels (no H2 → H4) |
| Canonical | self-referential |
| Indexability | article is indexable; **its tag pages are not** |
| Image weight | every image WebP, ≤200 KB |

**FAIL if any row fails.** All ten are mechanical; none requires reading the article.

## G2 · On-page SEO — Auto

| Check | PASS |
|---|---|
| Primary keyword in first 60 words | yes, naturally |
| Primary keyword density | 0.4%–1.8% (below = accidental; above = stuffing) |
| Secondary keywords present | ≥3 of the 3–6 in spec |
| Semantic terms present | ≥6 of the 8–15 in spec |
| Word count | inside the band for `content_type` |
| **Primary keyword is not any collection's primary keyword** | **hard fail** |
| No keyword in spec assigned to another live article | hard fail |

The last two are the cannibalization firewall. They are why this gate is scripted rather than eyeballed.

## G3 · Schema — Auto

| Check | PASS |
|---|---|
| `Article` emitted with `author`, `publisher`, `isPartOf`, `datePublished`, `dateModified` | yes |
| `dateModified` == `custom.last_reviewed` | yes — **never `published_at`** |
| `BreadcrumbList` correct for the article URL | yes |
| `about` / `mentions` resolve to live Product/Collection `@id`s | yes, no 404 |
| **`FAQPage` count across the whole site** | **exactly 1, and it is `/pages/faqs`** |
| Deprecated types | **no `HowTo`, no `speakable`, no per-article `FAQPage`** |
| `aggregateRating` / `review` | **absent** — hard fail if present from any non-verified source |
| Rich Results Test | no errors |

## G4 · Internal Linking — Auto

| Check | PASS |
|---|---|
| Up-links | exactly 1, to `hub_url` |
| Lateral links | ≤2, same pillar only |
| Collection links | ≤3 |
| Product links | ≤3 |
| Cross-silo links | ≤1, and to a **pillar** |
| **≥1 link to a `target_collection`** | **hard fail if absent** (locked condition 5) |
| Link density | ≤1 per 150 words |
| Tag-page links in body | **zero** |
| Duplicate targets | no target linked twice |
| Anchor text | not the exact primary keyword of the linked collection |
| Broken links | zero (HEAD check all) |

## G5 · Local SEO — Mixed

Applies to `meerut` silo articles; partially to `cake-guides`.

| Check | PASS |
|---|---|
| Locality named (LO type) | ≥1 real locality from the verified zone list |
| **Locality-specific fact present** | **a real delivery window or fee band. Absent → hard fail** |
| Delivery claims traceable | to `SERVICE_AREA_ZONE_MAP.md` / `PROPOSED_DELIVERY_CONFIG.md` |
| NAP consistency | any address/phone matches the `Bakery` schema byte-for-byte |
| No unfulfillable promise | no slot the store cannot serve |

**The second row is the doorway-page firewall.** A locality article with no locality-specific fact
is a doorway page, and this gate is the only thing standing between volume pressure and one.

## G6 · GEO / AI retrieval — Mixed

| Check | PASS |
|---|---|
| Direct answer within first 60 words | present, self-contained, quotable without surrounding context |
| Answer survives extraction | reads correctly when lifted out of the page — read it aloud alone |
| Question-shaped subheadings | 2–4 |
| First-party specifics | ≥3 concrete facts (lead time, price band, size, process detail) |
| Critical facts in text | no key fact expressed **only** in an image or table cell |
| Entity mentions | ≥2 from `ENTITY_RELATIONSHIP_MAP.md` §4 |
| One idea per paragraph | yes |

## G7 · Trust — Manual

| Check | PASS |
|---|---|
| No unsourced claim | every claim in a verification bucket |
| No superlative | no "best/top/leading/#1" without an attributed source |
| No invented fact | no rating, review, licence number, award, GTIN |
| No fabricated author | byline is real, or `Organization` |
| Prices | stated as ranges with "from", or read live |
| Promises | nothing the store cannot deliver today |

## G8 · Helpful Content — Manual

Closed questions, not impressions.

| Check | PASS |
|---|---|
| Would a reader finish satisfied, without a second search? | yes |
| Does it contain information not obtainable from the top 3 SERP results? | yes — name it in one line |
| Is it written from experience, not summary? | yes |
| Does it open differently from the last 2 articles in this cluster? | yes |
| Would this exist if search engines did not? | yes |
| Is any section present only to hold a keyword? | **no** |

The last two are the ones that catch the failure mode. Answer honestly or the gate is theatre.

## G9 · E-E-A-T — Manual

| Check | PASS |
|---|---|
| Byline resolves to a real entity | yes |
| First-hand detail present | ≥1 thing only this studio would know |
| Claims attributable | first-party or cited |
| Author entity in schema | `Person` where available, else `Organization` — never blank |
| Business entity resolvable | `#organization` with ≥6 `sameAs` after Phase 0.6 |

## G10 · Originality — Manual

| Check | PASS |
|---|---|
| Not substantially similar to any existing article, page or collection description | yes |
| Not a paraphrase of a competitor page | yes |
| Boilerplate sentences repeated from other articles | **≤2** |
| Images original | yes — no stock, no Ecomus demo, no watermarked catalogue image |

## G11 · Completeness — Manual

| Check | PASS |
|---|---|
| Every H2 in the blueprint addressed, or the blueprint updated | yes |
| Obvious follow-up question answered or linked | yes |
| No "coming soon" / TODO / placeholder | zero |
| All spec fields populated | yes |

## G12 · Readability — Auto

| Check | PASS |
|---|---|
| Flesch Reading Ease | ≥55 |
| Average sentence length | ≤22 words |
| Paragraphs over 5 lines | ≤2 |
| Passive voice | ≤12% of sentences |
| Sentences over 35 words | ≤3 |

Indian English, general consumer audience. 55 is a deliberate floor — below it, extraction quality
drops as well as human comprehension.

## G13 · Grammar — Auto

Zero spelling errors · zero grammar errors · consistent Indian English (`colour`, `personalised`) ·
consistent number and currency formatting (`₹3,000`, `1 kg`) · **no mojibake** — the store already
has a live mojibake defect, so this is checked, not assumed.

## G14 · Brand Voice — Manual

Against `BRAND_VOICE.md` and `COPY_GUIDELINES.md`.

| Check | PASS |
|---|---|
| Reads as the studio, not a content agency | yes |
| Warm, specific, unhurried; not breathless | yes |
| No manufactured urgency ("Order now!!") | yes |
| Honest about limits — variation, lead time, what we can't do | yes |
| Would the owner say this out loud to a customer? | yes |

## G15 · External References — Auto

Every external link resolves 200 · no competitor links · `rel="nofollow"` on commercial
destinations · references dated where a date matters · **no citation to a source that does not
support the claim** (spot-checked, 1 per article).

## G16 · Accessibility — Auto

| Check | PASS |
|---|---|
| Every image has descriptive alt text | yes; decorative images `alt=""` |
| No alt text that is only keywords | yes |
| Heading order logical | no skipped levels |
| Link text meaningful out of context | yes |
| Colour contrast in any inline styling | ≥4.5:1 |
| Tables have headers | yes |

Not negotiable, and not a "nice to have" — this is in the never-simplify list.

## G17 · Performance — Auto

| Check | PASS |
|---|---|
| Total image weight | ≤600 KB per article |
| Every image WebP, longest edge ≤1600 px | yes |
| No render-blocking asset added by the article | yes |
| No inline `<script>` in article body | yes |
| Lighthouse Performance (article URL, mobile) | ≥85 |

## G18 · Conversion — Auto + Manual

| Check | PASS |
|---|---|
| ≥1 CTA present | yes |
| CTA matches `primary_cta` in spec | yes |
| **WhatsApp links carry the `cluster_id` source token** | **yes — else the article is unattributable** |
| Email capture present | yes, with an occasion-date field |
| CTA appropriate to `buying_stage` | decision-stage → collection; early-stage → email/WhatsApp |
| ≤1 conversion module | yes — more reads as pressure and converts worse |

---

## Running the gates

```
python seo-ops/blog_gates.py --article CG-P2-01          # one
python seo-ops/blog_gates.py --status VERIFIED --all     # batch, weekly
```

Dry-run by default, CSV report out, per `docs/CODING_STANDARDS.md`.

**Output is a per-gate PASS/FAIL table plus the failing check verbatim.** A gate report that says
"needs work" is a failed report — the article returns to S3 with the specific line that failed.

**Batch weekly**, 4 articles at a time — the scripted gates run over a folder as cheaply as over a
file (`CONTENT_FACTORY.md` §5).

## Gate escalation

| Situation | Rule |
|---|---|
| Any hard-fail gate | **No override exists.** G2 keyword collision, G3 second `FAQPage`, G4 missing commercial destination, G5 missing locality fact, G7 unsourced claim |
| Soft fail, ≤2 gates | Return to S3, fix, re-run only the failed gates |
| Soft fail, ≥3 gates | Return to **S2** — the blueprint was wrong, not the prose |
| Same gate fails on 3 consecutive articles | **Stop production.** The gate or the template is broken. Fix the system, not the article |

The last rule is the one that keeps this a factory rather than a queue of exceptions.
