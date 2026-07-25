# DECISION_LOG.md — Blog OS

Architectural decisions with rationale and rejected alternatives. One decision, one entry
(per the `CLAUDE.md` standing principle). Nothing here has been executed.

---

### D-001 · Four blogs as intent-based silos
**2026-07-24 · Accepted**

Four Shopify blogs — `cake-guides`, `cake-ideas`, `eggless-kitchen`, `meerut` — cut on **search
intent**, not subject.

*Why:* Shopify's URL is fixed at `/blogs/{blog}/{article}`. The blog handle is the only hierarchy
level available, so silos must be blogs. Cutting on subject ("birthday", "wedding", "hampers")
would collide immediately — those already exist as collections, product types, tags and pages.
Cutting on intent cannot collide with the catalogue by construction, because the catalogue owns
transactional intent and nothing else.

*Rejected:* **One blog, tags as categories** — a 1,000-article index paginates ~111 deep and gives
a crawler no silo signal; tag pages would have to be indexed to substitute, creating exactly the
thin index this design forbids. **8–12 blogs** — fragments authority, multiplies template
maintenance, and forces judgement calls at every commission.

---

### D-002 · Collections and pages are the hubs; articles are never hubs
**2026-07-24 · Accepted**

Every cluster's hub is a collection or page. Pillars link **up** to it.

*Why:* the blog's job is to feed the catalogue. If pillars are hubs, authority accrues to
`/blogs/*` and the pages that can take an order stay where they are. Making the money page the hub
turns every cluster into a funnel.

*Consequence:* an article that outranks its hub is a **defect**, not a win. Anchor-text policy
(`INTERNAL_LINKING_BLUEPRINT.md` §4) exists to prevent it.

---

### D-003 · Tags are facets, and every tag page is `noindex, follow`
**2026-07-24 · Accepted**

52-tag cap, four prefixed namespaces, 2–4 tags per article, no new tag without a retirement.

*Why:* Shopify auto-generates `/blogs/{blog}/tagged/{tag}`. 52 tags × 4 blogs = up to 208
auto-generated thin pages competing with the pillars they were meant to support. `follow` keeps
the equity flowing; `noindex` keeps them out of the index. Setting this before article one is
trivial; after 200 are indexed it is a recovery project.

*The cap is the real decision.* Uncapped vocabularies are how blogs reach 300 tags and zero
navigability. A cap forces the retirement conversation.

---

### D-004 · No `/blogs/answers/` atomic-Q&A silo
**2026-07-24 · Rejected**

A fifth silo of one-question-per-URL articles was designed for AI Overviews and cut.

*Why:* it duplicates the 43 existing Q&A metaobjects and the FAQ page; each article would be
100–200 words, i.e. exactly the thin content already scoring 3/10 in the audit; and atomic answers
cannibalize the pillars that should answer the same question with more context.

*Instead:* GEO is served by a mandatory 40–60 word **answer-first block** and 2–4 unique Q&As
**inside** every substantive article. Extractability without the thin-page cost.

---

### D-005 · Collection consolidation is a hard prerequisite, not a parallel track
**2026-07-24 · Accepted**

No article publishes into the delivery, hamper or theme-cake intent space until Phase 0 completes.

*Why:* five collections resolve from the identical rule `TYPE CONTAINS "Cake"` to the identical
985 products. Adding blog content to that adds a sixth, seventh and eighth competitor for one
query. The three highest-value pillars in the plan (`ME-P1`, `CI-P5`, `CI-P2`) are precisely the
three that collide — the store's most valuable intents are the ones most fragmented, which is why
this sequencing is not negotiable.

---

### D-006 · Delete the site-wide hardcoded `FAQPage`
**2026-07-24 · Accepted**

`layout/theme.liquid:68` emits a hardcoded `FAQPage` in `<head>` on every URL.

*Why:* one FAQ set claimed by 1,300+ URLs is structured-data spam exposure, and every article
emitting its own correct `FAQPage` would emit a second on the same page. Half a day of work
blocking the entire GEO track.

*Replacement:* one `FAQPage` on `/pages/frequently-asked-questions-faqs` sourced from the 43
metaobjects, plus per-article `FAQPage` from `custom.faq_pairs`.

---

### D-007 · A named `Person` author entity is required, and may not be invented
**2026-07-24 · Accepted — client-blocked**

Every article's `Article.author` resolves to `#person-{slug}` with a real page, photo and bio.

*Why:* `Organization` as author is the weakest available E-E-A-T signal, and for a *studio* brand
whose product is craft it is also a wasted differentiator. A named baker who has made 1,235 cake
designs is the experience signal; it is currently unclaimed.

*Constraint:* no persona, no stock photo, no invented name. Consistent with the standing rule that
has already caused three removals. Articles ship with an Organization byline until the client
provides the identity, then are retro-updated.

---

### D-008 · Seasonal articles are refreshed in place; year-suffixed URLs are prohibited
**2026-07-24 · Accepted**

`/blogs/cake-ideas/diwali-hamper-ideas` is written once and updated each year.
`diwali-hamper-ideas-2027` is banned.

*Why:* year-suffixed seasonal content is the single largest long-run source of cannibalization in
retail blogs — by year five, five URLs compete for one query and four are stale. It also depends on
a working `dateModified`, which is why D-010 is a prerequisite.

---

### D-009 · Parameterise the city variable before city one
**2026-07-24 · Accepted**

`areaServed`, delivery radius, minimum order, locality list and phone become metafield-driven in
Phase 2 — before any second city, and before the Meerut silo is fully built.

*Why:* two days now, a re-platforming job after 100 Meerut articles. The stated requirement is
multi-city expansion *without major architectural change*; that requirement is only met if the city
is data. Today it is a literal in ~28 collection SEO strings, ~8 page handles and the `Bakery`
schema.

---

### D-010 · `dateModified` must come from `custom.last_reviewed`
**2026-07-24 · Accepted**

`tbk-schema-article.liquid` currently sets `dateModified` to `article.published_at`, which can
never change.

*Why:* freshness is a ranking and citation signal; a permanently-wrong one makes updated articles
look stale forever. Fall back to `article.updated_at`, never to `published_at`. The same value
renders visibly as `Last reviewed:` — an honest date, not a rolling fake.

---

### D-011 · No `Recipe` schema
**2026-07-24 · Rejected**

`eggless-kitchen` will discuss technique; it will not publish recipes with `Recipe` markup.

*Why:* `Recipe` invites a rich result that answers the query **without a click**, and the studio's
commercial interest is in selling a cake, not teaching someone to bake one. Technique articles
build authority; recipes give away the product and compete in a saturated vertical against
dedicated food publishers. `HowTo` on storage/transport/serving is used instead — it supports the
purchase rather than replacing it.

---

### D-012 · Named IP is referenced descriptively; collections own the branded query
**2026-07-24 · Accepted**

Motu Patlu, PAW Patrol, Roblox, Barbie etc. are mentioned inside articles and linked down to their
collections. No article *titles* target a trademarked term.

*Why:* the collection is the correct canonical owner of a transactional branded query and already
ranks; and editorial pages carry a different trademark-exposure profile from product listings.
Descriptive reference plus a down-link captures the value without the risk.

---

### D-013 · The product page stays a link sink
**2026-07-24 · Accepted**

No related-articles module on the product page. The blog↔catalogue loop closes via collection
descriptions instead.

*Why:* `main-product-premium-v2.liquid` is a protected module (`CLAUDE.md`). Collection
`descriptionHtml` is data, editable through the Admin API with no theme deploy, and carries the
reverse edge adequately.

*Cost, stated plainly:* product pages accumulate authority and pass none onward. Accepted, not
worked around. If the protection is ever relaxed for invisible edits, this is the highest-value
addition available.

---

### D-014 · Blog OS documentation lives in `docs/blog-os/`, not the repo root
**2026-07-24 · Accepted**

*Why:* `MD_FILE_INVENTORY.md` already documents root `*.md` sprawl, and `CLAUDE.md` names
"one decision, one document" as a standing principle after the five-file Jul-19 NAP cluster.
Twelve more root files would repeat exactly that.

---

### D-015 · The existing `news` blog is retained but excluded
**2026-07-24 · Accepted**

`news` (0 articles) stays, reserved for genuine announcements, linked from nowhere.

*Why:* deleting it is a needless risk for zero gain. Excluding it from navigation prevents it
becoming the default dumping ground for anything that fails a silo charter — which is what would
otherwise happen by article 50.

---

---
---

# v2 decisions — post-design-review

`DESIGN_REVIEW.md` rejected v1 with 6 fatal findings. The following supersede or add to the above.
**Reversals are marked.**

---

### D-016 · Four silos → two · **REVERSES D-001**
**Accepted.** `eggless-kitchen` merged into `cake-guides`; `cake-ideas` deleted entirely.

*Why:* the `cake-guides`/`eggless-kitchen` boundary was ambiguous **and** permanent — moving an
article between blogs changes its URL. v1 deferred the call to "commission time", which is the
worst moment to make an irreversible decision. Merging deletes the problem rather than managing it.

Silo count should equal the number of intents the business can serve with first-party knowledge.
For a single-city eggless cake studio that is two.

---

### D-017 · `cake-ideas` deleted; inspiration content moves to collection descriptions
**Accepted. The most consequential v2 change.**

20 of v1's 38 `cake-ideas` launch articles mapped onto a live collection (`for-him`, `for-her`,
`roblox`, `jungle-animal-theme`, `cake-hampers`, `luxury-diwali-hampers`…). A well-written article
outranks a thin collection page — which D-002 defines as a **defect**. v1's largest silo was a
machine for producing its own defined defect at scale.

It was also the highest-risk content pattern available (450 formulaic image-led listicles) on a
store with **no usable original photography**.

*Instead:* enrich 35 collection descriptions. ~4 days, no theme deploy (`descriptionHtml` is data),
zero cannibalization, and it strengthens the page that takes the order. It also supplies the
collection→blog reverse edge.

---

### D-018 · One article template, branching on `blog.handle` · **REVERSES the v1 template plan**
**Accepted.** `Article.templateSuffix` is **per-article and not inherited** from
`Blog.templateSuffix`. v1's four per-silo article templates would require manual configuration on
every article forever, with no Flow automation on Basic. Blog *index* templates remain per-silo —
that part was correct.

---

### D-019 · Required article metafields: 12 → 5
**Accepted.** The store is on **Basic — no Shopify Flow.** v1 required 12 fields × ~900 articles =
10,800 manual entries. Prose fields (`answer_first`, `key_facts`, `faq_pairs`) belong in the body,
not in metafields; `intent`, `content_type` and `city` are derivable.

---

### D-020 · No per-article `FAQPage` · **REVERSES D-006's article half**
**Accepted.** Google restricted FAQ rich results to authoritative government and health sites in
August 2023. A bakery gets **no rich result**, on any page. v1 made a mandatory content
requirement across ~900 articles on a payoff that does not exist.

Q&A prose is retained — it serves LLM extraction, and that value comes from the writing, not the
markup. One `FAQPage` remains on `/pages/faqs`, labelled low-expected-value. The deletion of the
**site-wide** hardcoded block (D-006) stands unchanged.

*Re-verify Google's current rich-result eligibility before implementation.*

---

### D-021 · `HowTo` content type deleted
**Accepted.** Google deprecated `HowTo` rich results. The type's only distinguishing feature was
its schema. Storage/transport/serving content becomes ordinary cluster content.

---

### D-022 · `Article.about` / `mentions` → Product `@id` · **REVERSES D-013's conclusion**
**Accepted. A missed solution, not a wrong one.**

v1 concluded the product↔blog loop was unclosable because the product template is protected, and
wrote a decision record accepting it. The loop is unclosable in **HTML**; it is fully available in
**schema**, emitted from the *article* template, touching no product file.

A machine-readable article↔product edge is precisely what AI retrieval traverses. v1 gave up on
the edge that most mattered for the brief's stated goal.

D-013's HTML conclusion stands: the product page remains an HTML link sink.

---

### D-023 · GEO requires an off-site track
**Accepted. The largest hole in v1.**

v1's entire GEO strategy was on-site prose. LLM answer engines cite local businesses that
**third parties corroborate** — GBP, Zomato, Swiggy, JustDial, Magicpin, Instagram, wedding
directories, local press. v1 mentioned GBP once, as a `sameAs` string.

Target: **≥6 corroborating `sameAs` nodes, NAP byte-identical.** "Kaur" is a near-universal name;
two links cannot resolve this business against many similarly-named home bakeries.

1.5 days, returns in weeks, and it is now the second item in the roadmap.

---

### D-024 · Explicitly allow AI crawlers
**Accepted.** No `robots.txt.liquid` exists, so the current posture is Shopify's default — an
accident, not a decision. Explicit **allow** for GPTBot, ClaudeBot, PerplexityBot, CCBot and
Google-Extended. Note `Google-Extended` governs Gemini grounding independently of `Googlebot`.

---

### D-025 · Target ~250 articles, not 920
**Accepted.** v1's ceiling was **4× its own maintenance capacity**: 920 articles on a 12-month
refresh cycle is ~77 refreshes/month against a capacity of ~16 articles/month. At the moment v1
reached its ceiling it was already failing.

**The architecture supports 1,000+; the plan deliberately does not target it.** For a single-city
bakery with 602 active products, 1,000 articles would itself be the scaled-content pattern Google's
spam policy targets. Capacity and target are different questions.

Launch set 97 → **62**. Ceiling 920 → **~250**, derived from a stated refresh budget.

---

### D-026 · Article anatomy: 10 mandatory elements → 4
**Accepted.** Enforced uniformity across hundreds of pages is itself a Helpful-Content risk. v1
never acknowledged the tension between its mandatory 10-point structure and Google's stated
preference against formulaic content. Required: H1, a direct answer within the first 60 words,
byline, visible `Last reviewed`. Everything else is recommended.

---

### D-027 · Tags: 52 → 20; no link-equity claim
**Accepted.** Two reasons. (1) v1 sized its vocabulary for 920 articles. (2) v1's `fmt-` and
`aud-` namespaces duplicated collections that already exist — the `cake-ideas` error at the tag
layer.

Also corrected: v1 claimed `noindex, follow` tag pages "pass equity". A long-term `noindex` page is
eventually treated as `nofollow`. **Tag pages carry no equity** and no article may depend on one
for inbound links. The `noindex` rule itself stands — and the tag surface is **combinatorial**
(`/tagged/{a}+{b}`), not the 208 pages v1 estimated.

---

### D-028 · A measurement layer is part of the architecture
**Accepted.** v1 proposed ~86 days of work with no KPI, no attribution and no definition of
success. Added: `MEASUREMENT_PLAN.md`, per-phase targets, a UTM convention, **WhatsApp prefill
source tokens** (attribution with no app, on a Basic plan), a manual AI-visibility prompt panel,
and **kill criteria** — a content program with no stopping rule becomes a sunk cost.

---

### D-029 · Email capture promoted Low → High
**Accepted.** On a domain whose SEO payoff is months away, an owned list is the only near-term
return the blog can produce — and for a *celebration* business, capturing occasion dates
(birthdays, anniversaries) is the highest-value owned asset available. v1 ranked it L4.

---

### D-030 · Pinterest is a catalogue channel, not a blog channel
**Accepted.** v1 called `cake-ideas` "a Pinterest channel" and specified nothing — no 2:3 vertical
assets, no Rich Pins, no boards — and pointed it at the wrong destination. Pinterest for a cake
studio drives to **product and collection pages**. Gated on photography like everything else
visual.

---

### D-031 · Sequence by time-to-return
**Accepted.** v1 sequenced by dependency and put ~97 new articles — the slowest-returning asset on
an unknown-authority domain — ahead of everything. New content is not retrieved or cited for
months. v2 front-loads schema repairs and the off-site track (weeks), then collection enrichment on
pages that already rank (weeks), then articles (months).

---

### D-032 · Two scores, reported separately
**Accepted.** The 33/100 in `BLOG_AUDIT.md` measures the **live store** and cannot move until
Phase 0 executes. The **Design Quality Score** in `DESIGN_REVIEW.md` measures the **blueprint**.
Neither may stand in for the other, and no document edit may be presented as improving the store.

---

---
---

# v2.1 decisions — post-completion-audit

`COMPLETION_AUDIT.md` ran the 15 completion conditions as a gate. v2.0 failed four and partially
met two. These decisions close them.

---

### D-033 · Hub and commercial destination are separate required fields
**Accepted.** v2.0 conflated them. Five pillars had a page hub and no commercial destination at
all; ME-P2 pointed only at `/pages/about-us`, which takes no orders.

Every pillar and cluster now carries both. A pillar may link up to a page for topical reasons, but
must additionally reach a collection. Enforced at the publish gate, not by intention.

*Why it matters:* completion condition 5 is "every blog has a commercial destination". An article
that cannot reach a page which takes an order is not part of a commercial content system, however
good it is.

---

### D-034 · Two pillars added — wedding and anniversary · **partially reverses D-017**
**Accepted.** Verified active-product counts showed **Anniversary Cake at 83** and **Wedding Cake
at 68** — the #2 and #3 types — with **no pillar between them**.

Deleting `cake-ideas` in v2.0 was correct for the listicles, but it also removed the wedding and
anniversary pillars. That was an over-correction: the *listicles* cannibalized collections; a
*decision* pillar ("how many tiers for how many guests", "choosing by milestone year") does not.

CG-P7 and CG-P8 added. D-017's core holds — inspiration content still lives on collections.

---

### D-035 · No hamper pillar — blocked on inventory, not content
**Accepted.** `cake-hampers` shows 119 products and `luxury-diwali-hampers` 44, but **Gift Hamper
and Festive Hamper both have 0 active products.** Every hamper is DRAFT.

A hamper pillar would rank for queries the store cannot fulfil. Publish-vs-archive is the client's
merchandising decision (`CLAUDE.md`), so the pillar is drafted and held.

*This blocker was invisible to both v1 and v2.0* — both read collection counts, which include
drafts, and neither checked active inventory. It is now one of the four re-open triggers.

---

### D-036 · CG-P1 is the highest-priority pillar
**Accepted.** **Theme Cake is 400 of 602 active products — 66% of the live catalogue.** v1 filed
it under listicles; v2.0 folded it into one shared "custom ordering" pillar and sequenced it
third.

Three clusters added; moved to first in the Phase 3 order. The plan should be weighted toward what
the business actually sells, and until counts were verified, it was not.

---

### D-037 · "651 active products" was wrong — the figure is 602
**Accepted.** Carried through v1 and v2 as an inference and never verified. Actual:
**602 active / 588 draft / 45 archived = 1,235.** Corrected in every document.

*Why it is logged rather than silently fixed:* it shifted the priority order (D-036), revealed the
hamper blocker (D-035) and exposed two uncovered product types (D-034). An unverified number that
propagates into a plan is a defect, not a typo.

---

### D-038 · Editorial standards and template spec are architecture, not documentation
**Accepted.** Completion conditions 13 and 14 require both to be *finalized*. v2.0 had fragments
scattered across three files — enough to discuss, not enough to build or to enforce.

`EDITORIAL_STANDARDS.md` (verification buckets, image rules, publish gate, refresh discipline) and
`TEMPLATE_SPEC.md` (block order, settings, the three broken-binding repairs, schema amendments)
are now buildable specifications.

---

### D-039 · Conditions 3 and 4 lock as ✅ architecture / ⛔ pending Phase 0
**Accepted.** "No duplicate intent" and "no keyword cannibalization" hold for the architecture and
do **not** hold for the live store — eight URLs on delivery intent, five identical collections.

Marking them ✅ outright would conflate design with execution, the same error the two-score split
exists to prevent (D-032). Marking them ❌ would block a lock on grounds the architecture has
already solved.

They lock as satisfied **by the architecture**, with the store-side fix carried as Phase 0.

---

---

### D-040 · Launch set is 71 articles, not 76 — arithmetic correction
**2026-07-24 · Accepted · post-lock**

Seeding `blog_master.csv` from the itemised per-pillar lists produced **71 rows**, not the 76
asserted in `TOPIC_CLUSTER_MAP.md` v2.1. The subtotals were mis-added: `cake-guides` lists 45
clusters and was summarised as 49; `meerut` totals 18 and was summarised as 19.

**The itemised lists — which the lock actually rests on — are unchanged.** Only the summary
arithmetic was wrong. Corrected to **71 = 53 + 18** (65 publishable, 6 held) across eight
documents; timeline to Gate 4 ~25 → **~24 weeks**.

*Logged rather than silently patched, for the same reason as D-037:* an unverified number that
propagates into a plan is a defect. This one was caught because the CSV was generated from the
lists instead of from the summary — which is an argument for generating counts rather than
typing them, and is now how they are produced.

**No architectural element changed. The lock holds.**

---

## Open questions for the client

| # | Question | Blocks |
|---|---|---|
| Q1 | Who is the named author — name, title, photo, bio, one external profile? | D-007, all bylines, `EK-P4` |
| Q2 | Canonical Google Business Profile URL? | H3 — the highest impact-per-hour fix in the plan |
| Q3 | FSSAI licence number? | `hasCredential`, the "FSSAI approved" claim |
| Q4 | Approve four 301s on live collection URLs? Any printed QR codes or paid ads pointing at them? | Phase 0.2 |
| Q5 | Confirmed delivery windows and fee bands per locality? | ME-1c–1f; without these they are doorway pages and will be held |
| Q6 | Is "the best bakery and cake shop in Meerut" in the shop meta description acceptable, given the no-unverifiable-claims standard? | M15 |
| **Q7** | **Google Search Console + Analytics access?** Without a baseline the program cannot be evaluated, only defended | `MEASUREMENT_PLAN.md` entirely; article topic validation |
| **Q8** | **Which off-site listings already exist and who controls them** — Zomato, Swiggy, JustDial, Magicpin, wedding directories? | D-023, Phase 0.6, the whole GEO track |
| **Q9** | **Who answers WhatsApp, and will they tally source tokens weekly?** Five minutes a week, and it is the only attribution available on this stack | D-028 |
