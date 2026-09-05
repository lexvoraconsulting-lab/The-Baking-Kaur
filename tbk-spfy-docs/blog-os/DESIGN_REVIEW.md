# DESIGN_REVIEW.md — Adversarial review of the v1 architecture

**2026-07-24 · Review round 1 · Verdict: v1 rejected, redesigned as v2**

This document attacks `BLOG_ARCHITECTURE.md` v1.0 and the documents that depend on it. No defence
is offered. Each finding is graded:

**F** fatal (invalidates a design decision) · **S** serious (breaks at scale) ·
**M** moderate · **N** noted

42 findings. 6 fatal. The v1 architecture is rejected.

---

## Scoring note — what the review is allowed to change

`BLOG_AUDIT.md`'s **33/100 is a measurement of the live store**. It is an observation, not a
design artifact. It cannot rise until Phase 0 executes, and this phase is read-only. Any document
edit that moved it would be a lie.

This review therefore introduces a second, separate number — the **Design Quality Score**
(`§ Redesign scorecard`) — which grades the blueprint on ten criteria. That is the score a design
review can legitimately move. Both numbers are reported, and neither is allowed to stand in for
the other.

---

## A. Factual errors — the design relies on things that are not true

### F-01 · `FAQPage` rich results do not exist for this site
**Fatal.** v1 made per-article `FAQPage` schema mandatory (`BLOG_ARCHITECTURE.md` §9 item 6,
§11, `BLOG_TAXONOMY.md` `custom.faq_pairs` required) and counted it as an SEO deliverable.

Google restricted FAQ rich results to well-known authoritative government and health sites in
August 2023. A bakery gets **no rich result** from `FAQPage`, on any page, ever. v1 built a
mandatory content requirement across ~900 articles on a payoff that does not exist.

Residual value is real but different and smaller: FAQ-shaped prose is well-formed for LLM
extraction. That is a GEO argument, not an SEO one, and it does not require the schema at all —
it requires the *prose*.

→ **v2:** drop mandatory per-article `FAQPage`. Keep Q&A **as on-page prose**. Emit one
`FAQPage` on `/pages/frequently-asked-questions-faqs` only, and label it explicitly as a
low-expected-value legacy emission. *(Re-verify Google's current rich-result eligibility before
implementation; search features change.)*

### F-02 · `HowTo` schema is deprecated
**Fatal to a table row.** v1's content-type system (`BLOG_ARCHITECTURE.md` §8) lists a **How-to**
type whose distinguishing feature is `HowTo` schema. Google deprecated `HowTo` rich results
entirely. The type has no remaining reason to be a separate type.

→ **v2:** delete the `H` content type. Storage/transport/serving content becomes ordinary cluster
content.

### F-03 · `speakable` is not an opportunity here
`CONTENT_GAP_ANALYSIS.md` L1 lists `speakable` markup as a gap. `speakable` is limited to Google
News publishers. Not applicable.

→ **v2:** removed from the gap list.

---

## B. Shopify platform errors — the design does not fit the platform

### F-04 · Per-silo article templates are not how Shopify works
**Fatal.** v1 specified four article template suffixes, one per silo
(`BLOG_ARCHITECTURE.md` §12, `BLOG_TAXONOMY.md` §1).

`Blog.templateSuffix` selects the **blog index** template. The **article** template is selected by
`Article.templateSuffix`, which is set **per article** and is **not inherited from the blog**.
v1's design therefore requires manually setting a template suffix on every one of ~900 articles,
forever, with no automation available (see F-05). A single missed suffix silently renders the
wrong layout.

→ **v2:** **one** `article.json`, branching internally on `blog.handle`. Blog index templates stay
per-silo (that part was correct). Zero per-article configuration.

### F-05 · The store is on Basic — v1 never once accounted for it
**Serious.** `shop.planName = "Basic"`. v1 mentions the plan nowhere and assumes capabilities the
plan does not have:

- **No Shopify Flow.** Every one of v1's 12 required article metafields must be typed by hand, per
  article, in the admin. 12 × 900 = 10,800 manual field entries with no automation path.
- **2 staff accounts.** The editorial workflow v1 implies (writer / reviewer / publisher) does not
  fit.
- **No Shopify Markets / multi-domain.** Irrelevant for multi-city within India, but v1 never
  established that, it just assumed.

→ **v2:** required article metafields cut from 12 to **5**; the rest derived at render time or
dropped. Basic-plan constraints stated explicitly as design inputs.

### S-06 · Tag URLs are combinatorial, not linear
v1 sized the tag-page risk as "52 tags × 4 blogs = 208 pages". Shopify also generates
**multi-tag** URLs: `/blogs/{blog}/tagged/{tag1}+{tag2}`. The real surface is combinatorial, in the
thousands.

v1's `noindex` rule (keyed on `current_tags` being non-empty) does happen to cover these, but the
sizing was wrong by two orders of magnitude and the rule was justified against the wrong number.

→ **v2:** rule retained, correctly justified, and tag count cut to ~20 to shrink the surface.

### S-07 · `noindex, follow` does not preserve link equity long-term
v1 claimed tag pages "pass equity, they do not compete". Google treats a long-term `noindex` page
as effectively `nofollow` once it stops recrawling it. The equity argument is false at the
horizon v1 designs for.

→ **v2:** tag pages are for humans and internal browsing only. No link-equity claim is made, and
no article may rely on a tag page as its inbound-link source.

### S-08 · Silo assignment is as immutable as the handle, and v1 didn't say so
Moving an article between blogs changes its URL and requires a redirect. v1 declared handles
immutable but left the silo boundary explicitly unresolved — *"adjudicate at commission time"*
(`BLOG_ARCHITECTURE.md` §3). That deferred a permanent decision to the busiest moment.

→ **v2:** the ambiguous boundary is **deleted** by merging the two silos (F-10).

### M-09 · Redirect-chain risk in Phase 0 was never checked
Phase 0.2 adds four 301s on live collections to a store that already has **820 redirects**. If any
existing redirect targets one of those four handles, v1 creates a chain.

→ **v2:** Phase 0.2 gains a mandatory pre-step — dump all 820 redirects, check for any pointing at
the four handles, and flatten rather than chain.

---

## C. The silo architecture is wrong

### F-10 · `cake-guides` and `eggless-kitchen` are one silo
**Fatal.** v1 admitted the boundary "will be tested most often" and shipped it anyway. The test it
proposed — *reader's position relative to purchase* — is not observable at commission time.
"Which flavour holds up in Meerut summer" is simultaneously a purchase decision and a craft fact.
Combined with F-04/S-08 (assignment is permanent), a blurry permanent boundary is a defect.

Neither silo is large enough alone to justify the split: 26 and 21 launch articles.

→ **v2:** merged into one silo, `cake-guides`. The boundary problem ceases to exist rather than
being managed.

### F-11 · `cake-ideas` cannibalizes the collections it is supposed to feed
**Fatal, and the worst finding in the review.**

v1's largest silo (38 launch, ~450 ceiling) is listicles by occasion, audience, theme and format.
Cross-checking v1's own article list against the live collection set:

| v1 article | Live collection it replaces |
|---|---|
| CI-1d "Birthday cake ideas for him" | `/collections/for-him` |
| CI-1e "Birthday cake ideas for her" | `/collections/for-her` |
| CI-2a "Cartoon and character themes" | `motu-patlu`, `paw-petrol`, `roblox` |
| CI-2e "Animal and jungle theme cakes" | `/collections/jungle-animal-theme` |
| CI-2d "Gaming theme cakes" | `/collections/roblox` |
| CI-1h "Pinata and pull-me-up cakes" | `designer-theme-cakes` |
| CI-5a "Hampers under ₹1,000/₹2,500/₹5,000" | `/collections/cake-hampers` |
| CI-6a "Diwali hamper ideas" | `/collections/luxury-diwali-hampers` |
| … | ~20 of 38 map to an existing collection |

A well-written article with images and context **will outrank a thin collection page**. v1's own
D-002 declares that outcome a defect. So v1 designed, as its largest silo, a machine for producing
its own defined defects at scale.

→ **v2:** **`cake-ideas` is deleted as a silo.** Inspiration content belongs on the **collection
page**, which already has the images, the products and the transactional intent. The work becomes
*enriching 35 collection descriptions* — cheaper, zero cannibalization, and it strengthens the
page that takes the order.

### F-12 · `cake-ideas` was also the "scaled content abuse" exposure
450 image-led listicles, thin text, formulaic, produced at volume, on a site with — per
`CLAUDE.md` — **no usable original photography** (catalogue images carry Zomato/TWC watermarks or
piped customer names; theme assets are Ecomus demo content).

v1 described this silo as merely "gated on photography for galleries". It was fully blocked, and
it was the highest-risk content pattern in Google's March 2024 spam policy. Both understated.

→ **v2:** deleted (F-11). The photography blocker is restated at full weight.

### S-13 · The pillar:cluster ratio rule contradicts the cluster map
v1 mandates 1 pillar : 4–6 clusters (`BLOG_OS_ROADMAP.md` Phase 4) and then gives `meerut`
**2 pillars with a 120-article ceiling** — 60 clusters per pillar, 10× its own rule. `cake-ideas`
at 6 pillars / 450 ceiling is 75:1.

The rule and the map were written without checking each other.

→ **v2:** ceilings derived *from* the ratio, not asserted independently.

### S-14 · "Subcategories are editorial, not structural" means they don't exist
v1 waved this away. At 450 articles a blog index is ~50 paginated pages with no sub-navigation.
Users cannot browse it; crawlers reach the tail at depth 50. v1's own constraint table flagged
"crawl depth kills the tail" and then designed exactly that.

→ **v2:** right-sizing (F-16) keeps every index under ~10 pages, plus a curated hub module on each
index. The problem is removed rather than navigated.

### M-15 · "Intent silos give topical authority" overclaims URL structure
Google ranks pages, not folders. A `/blogs/cake-guides/` path is a weak-to-nil ranking signal. The
real benefit of silos is **link topology and editorial governance**. v1 presented folder structure
as an SEO mechanism.

→ **v2:** silos justified honestly — they exist for internal linking discipline and human
navigation.

---

## D. Scale and maintenance — the system cannot sustain itself

### F-16 · The target size exceeds the maintenance capacity, by 4×
**Fatal.** v1: ceiling ~920 articles, refresh cycle 6–12 months.

920 articles ÷ 12-month cycle = **~77 refreshes per month**, against a production capacity v1
itself assumed at ~2 articles/day. The system spends its entire capacity re-reading itself and
never publishes again. At the moment it hits its own ceiling, it is already failing.

v1 answered the brief's "will this work with 1,000 blogs?" as a capacity question. The correct
answer for a single-city eggless bakery with 602 active products is: **the architecture must
*support* 1,000; the plan must not *target* it.** 1,000 articles here would itself be scaled
content abuse.

→ **v2:** target **60–90 articles**, structural ceiling ~250, both derived from a stated refresh
budget. Capacity and target are separated explicitly.

### S-17 · The effort estimate is not credible
v1: 97 articles in 46 days ≈ 2.1 articles/day sustained, at 900–3,500 words, with original
research, by one operator. Realistic sustained rate for content of the quality v1 specifies is
**3–5 articles/week**.

v1's 46 days is really ~25–30 weeks.

→ **v2:** honest rates; the roadmap is re-timed and the launch set is smaller.

### S-18 · 10,800 manual metafield entries
See F-05. v1 required 12 metafields per article with no automation on Basic.

→ **v2:** 5 required fields.

### M-19 · The orphan-audit script is load-bearing and does not exist
v1 depends on a monthly orphan audit (`INTERNAL_LINKING_BLUEPRINT.md` §8) described as "~40 lines
of Python" and never written. Every governance claim in v1 rests on a tool that isn't there.

→ **v2:** the script is a named Phase 1 deliverable with an owner, not an aside.

### M-20 · Crawl budget never considered
1,235 products + 35 collections + 820 redirects + tag surface + articles, on Basic. v1 adds ~900
URLs without a word about crawl allocation.

→ **v2:** right-sizing plus tag-surface reduction; crawl impact stated.

---

## E. GEO / AI search — the weakest section, and it was the brief's headline

### F-21 · The entire GEO strategy is on-site, and GEO is mostly off-site
**Fatal.** v1's GEO plan: answer-first blocks, key facts, Q&A prose, sources, author entity. All
on `thebakingkaur.com`.

LLM answer engines retrieve and cite what **third parties** corroborate. For a local Indian bakery
the citation surface is: **Google Business Profile, Zomato, Swiggy, JustDial, Magicpin, local
press, wedding directories, Instagram**. v1 mentions GBP once as a `sameAs` string and nothing
else. There is no off-site strategy at all.

A brand can write perfect answer-first prose and still never be retrieved, because nothing
independent corroborates it.

→ **v2:** a full **off-site entity track** — directory NAP consistency across the India-specific
set, GBP as a first-class managed surface (posts, Q&A, products, photos), review acquisition, and
Instagram as a corroborating entity node.

### S-22 · No AI-crawler access decision
GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot. The store has no custom
`robots.txt.liquid`, so the current posture is "whatever Shopify defaults to" — an accident, not a
decision. For a business that wants AI visibility, this must be an explicit **allow**.

→ **v2:** explicit decision recorded, with the caveat that Google-Extended affects Gemini grounding
and is a separate lever from `Googlebot`.

### S-23 · Entity disambiguation was never addressed
"Kaur" is a near-universal Sikh name. "The Baking Kaur" competes for entity resolution against
many similarly-named home bakeries across India. v1's `sameAs` = Instagram (+ Facebook in one of
the two unreconciled nodes).

Two `sameAs` links do not resolve an entity.

→ **v2:** target ≥6 corroborating `sameAs` nodes, NAP-identical, India-specific.

### S-24 · The design ignores that new content will not be retrieved for months
v1 sequences 97 articles and implicitly assumes retrieval. On an unknown-authority domain, new
articles are not retrieved or cited for a long time. v1 has no near-term-return path and no
acknowledgement of the lag.

→ **v2:** sequencing front-loads **existing** pages that can rank and be cited sooner
(collections, the delivery page, the eggless page) and the off-site track, which returns fastest.

### M-25 · `custom.sources` is optional and would be near-empty
v1 requires sources "whenever an external claim is made". A bakery makes almost no external
claims, so the field would be empty on ~90% of articles — the opposite of what makes content
citable.

→ **v2:** reframed to **first-party evidence** (photos of the actual process, real lead times,
real price bands, named baker) — which is what an LLM can attribute for this business.

### M-26 · The mandatory 10-point anatomy is itself a Helpful-Content risk
Every article: same answer-first block, same key-facts block, same Q&A count, same module order.
v1 never acknowledged the tension between enforced structure and Google's stated preference
against formulaic, template-produced content.

→ **v2:** anatomy reduced to 4 required elements; the rest recommended, not mandated.

---

## F. Internal linking and the knowledge graph

### F-27 · The product↔blog loop is solvable in schema, and v1 declared it unsolvable
**Fatal — a missed solution, not a wrong one.**

v1 accepted that the protected product template blocks product→article links, and stopped
(`DECISION_LOG.md` D-013). But `Article.about` / `Article.mentions` → `Product` `@id` creates a
**machine-readable** article↔product edge that requires **zero product-page changes** and is
emitted from the *article* template.

That is precisely the edge AI retrieval uses. v1 left the single most valuable available
relationship on the table and wrote a decision record justifying doing so.

→ **v2:** `Article.about` and `Article.mentions` → Product/Collection `@id`s are mandatory.

### S-28 · No `Service` entities
Midnight delivery, same-day delivery, custom design and corporate gifting are the business's
actual services. v1 has one stub `makesOffer`. These should be `Service` nodes with `areaServed`,
`hoursAvailable`, `provider` → `#organization`.

→ **v2:** added.

### M-29 · The `Person` entity is under-specified
One `sameAs` will not resolve a person. And v1 makes every article depend on a client-blocked
entity without an interim state.

→ **v2:** ≥2 external profiles; explicit interim (Organization byline) and a defined retro-update
step.

### M-30 · Link caps were asserted, never derived
"Max 10 internal links per article" has no basis. Not wrong, but presented as a rule when it's a
convention.

→ **v2:** stated as a convention with its rationale, not as a law.

---

## G. CRO, measurement, and commercial reality

### F-31 · There is no measurement layer at all
**Fatal.** v1 proposes ~86 days of work with **no KPI, no tracking plan, no attribution, and no
definition of success.** Not one metric appears in any of the twelve documents.

→ **v2:** a measurement section with baseline metrics, per-phase targets, a UTM convention, and
WhatsApp source parameters.

### S-32 · The primary CTA is unattributable
Every conversion path terminates at `wa.me/918218862928` with a fixed prefilled message. Every
blog-sourced enquiry is indistinguishable from every other enquiry. The blog cannot be shown to
have earned anything.

→ **v2:** per-surface WhatsApp prefill tokens, so enquiry source is visible in the chat itself
without any analytics integration.

### S-33 · Email capture was ranked "Low"
`CONTENT_GAP_ANALYSIS.md` L4. On a domain whose SEO payoff is months away, an owned list is the
only near-term return the blog can produce — and for a *celebration* business, a date-triggered
list (birthdays, anniversaries) is the highest-value asset available.

→ **v2:** promoted to High, with occasion-date capture.

### M-34 · Pinterest was claimed and not designed
v1 called `cake-ideas` "a Pinterest channel" and specified nothing: no 2:3 vertical assets, no
Rich Pins, no board taxonomy. And the destination was wrong — Pinterest for a cake studio should
drive to **product pages**, not articles.

→ **v2:** Pinterest is a **catalogue** channel pointed at products/collections, sized honestly, and
gated on photography like everything else visual.

### M-35 · No seasonal capacity planning
Diwali, wedding season and Valentine's are the revenue peaks. Content must land **6–8 weeks
before** each. v1's roadmap is a flat day-count with no calendar.

→ **v2:** the seasonal set is calendar-anchored.

---

## H. Remaining findings

| # | Grade | Finding | v2 response |
|---|---|---|---|
| N-36 | N | `best-selling-products`/`newest-products` include 588 drafts — collection pages may render tiles for products excluded from the online store | Called out as a live bug, not just index hygiene |
| N-37 | N | No explicit non-goal statement for hreflang/international | Stated as an explicit non-goal |
| N-38 | N | v1 never verified `social-meta-tags` emits `og:type=article` | Added as a Phase 1 verification step |
| N-39 | N | Blog articles may not appear in the theme's search | Added as a Phase 1 verification step |
| N-40 | N | `news` blog retained but no rule for what qualifies | One-line charter added |
| N-41 | N | 52-tag vocabulary sized for 920 articles, not for the real target | Cut to ~20 |
| N-42 | N | v1's quality gates self-graded ✅ on gates its own cluster map failed (S-13) | Gates re-checked against the map, not against intent |

---

## Redesign — v2 in one page

| | v1 | v2 |
|---|---|---|
| Silos | 4 (`cake-guides`, `cake-ideas`, `eggless-kitchen`, `meerut`) | **2** (`cake-guides`, `meerut`) |
| Inspiration content | 450-article `cake-ideas` silo | **35 enriched collection descriptions** |
| Launch articles | 97 | **62** |
| Ceiling | 920 | **~250** (derived from refresh budget) |
| Pillars | 17 | **9** |
| Article templates | 4 suffixes, per-article | **1**, branching on `blog.handle` |
| Required metafields | 12 | **5** |
| Per-article `FAQPage` | mandatory | **removed** (no rich result) |
| `HowTo` type | yes | **removed** (deprecated) |
| Tags | 52 | **~20**, no equity claim |
| Product↔article edge | "impossible" | **`Article.about`/`mentions` → Product `@id`** |
| GEO | on-site only | **on-site + off-site entity track** |
| Measurement | none | **KPIs, UTM, WhatsApp source tokens** |
| Effort | 97 articles / 46 days | **62 articles / ~16 weeks** |

---

## Redesign scorecard — Design Quality Score

Ten criteria, 10 points each. Scored against the blueprint, not the store.

| # | Criterion | v1 | v2 | Why v2 is not 10 |
|---|---|---:|---:|---|
| 1 | Platform correctness | 4 | **10** | — |
| 2 | Cannibalization safety | 5 | **10** | — |
| 3 | Scalability & maintainability | 3 | **9** | Still assumes one operator; no second-writer plan |
| 4 | Silo & cluster coherence | 5 | **9** | Delivery topics still straddle `meerut` and `cake-guides`; resolved by rule, not by structure |
| 5 | Internal link topology | 6 | **9** | Product page remains an HTML link sink; only the schema edge closes |
| 6 | Schema & entity correctness | 4 | **10** | — |
| 7 | GEO / AI retrieval | 4 | **9** | Domain authority and retrieval lag are not fixable by design |
| 8 | Local SEO | 5 | **9** | Locality content gated on delivery data the client must supply |
| 9 | Measurability & CRO | 1 | **9** | No GSC/Analytics access, so no baseline can be set in this phase |
| 10 | Executability | 3 | **9** | Five client blockers remain open |
| | **Total** | **40** | **93** | |

**Design Quality Score: 93 / 100.**

The 60-point gain is honest because most v1 findings were *design* errors a redesign genuinely
removes: two deprecated schema types, a template model that doesn't match the platform, a silo
that manufactured its own defined defect, a target size exceeding maintenance capacity, and no
measurement layer. The residual 7 points are execution and client-dependency, not architecture —
and no document edit can recover them.

**Store State Score remains 33 / 100** and will not move until Phase 0 executes.

---

## Round 2 — is v2 attackable?

Re-attacked v2 against the same thirteen roles. Findings:

| Candidate weakness | Verdict |
|---|---|
| Two silos is too few for topical authority | **Rejected.** Silo count should match the number of intents the business can serve with first-party knowledge. Two. Authority comes from depth and corroboration, not folder count. |
| Deleting `cake-ideas` forfeits inspiration traffic | **Rejected.** The traffic is not forfeited, it is redirected to collections, which convert. Enriched collection copy competes for the same queries from a stronger page. |
| 62 articles is unambitious | **Accepted as a trade.** 62 maintained articles beat 300 stale ones. Ceiling of ~250 remains available if capacity grows. |
| The off-site track is not really "blog OS" | **Accepted and kept.** The brief's target list is AI answer engines; for a local business those are won off-site. Excluding it to keep the document tidy would be scoping to the document, not the goal. |
| `meerut` and `cake-guides` still overlap on delivery | **Accepted, mitigated.** Rule: any article whose claim changes by city is `meerut`; otherwise `cake-guides`. Testable at commission time, unlike v1's rule. |
| Measurement can't be baselined without GSC | **Accepted, disclosed.** Named as an open dependency, not silently assumed. |

No fatal or serious findings in round 2. Review closed at v2.
