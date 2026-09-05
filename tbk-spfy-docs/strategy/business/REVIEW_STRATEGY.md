# REVIEW_STRATEGY.md — The Baking Kaur

Governs **every** review, rating, testimonial and star that appears anywhere on the storefront, in any phase, forever. Pairs with `SCHEMA_MASTER.md` (markup), `SEO_GEO_MASTER_PLAN.md` (search/AI), `BRAND_VOICE.md` (tone).

**This document exists because the storefront was found publishing fabricated reviews.** See §8.

---

## 0. The one rule

> **If it cannot be traced to a real customer at a verifiable public URL, it does not go on the website.**

No exceptions, no "temporary" placeholders, no "just for the launch", no demo content left in. Every other rule here is a consequence of this one.

**Never fabricate, and never approximate:** review text · reviewer names · ratings · review counts · AggregateRating · dates · "verified" badges.

---

## 1. Review sources

Approved sources, in client-ratified priority order (2026-07-16):

| # | Source | Status | Integration | Notes |
|---|---|---|---|---|
| **1** | **Google Business Profile** | ✅ **RATIFIED PRIMARY SOURCE** (client, 2026-07-16) | ❌ no Shopify sync | Reviews must be **transcribed by hand** into `testimonial` metaobjects, each with a public `source_url`. Highest trust: customers can click through and verify. |
| **2** | **Judge.me** | ✅ approved | app + own widget | Collects **verified-buyer** reviews post-purchase. If adopted, its own widget/metafields become the source of truth and this section defers to it. |
| **3** | **Loox** | ✅ approved | app + own widget | Photo reviews. Same deferral rule as Judge.me. |
| **4** | **Shopify Product Reviews** | ✅ approved | native metafield `spr.reviews` | Legacy/basic. |
| **5** | **Zomato** | ⚠️ approved **only if legally displayable** | ❌ none | **Do not transcribe until someone confirms Zomato's terms permit off-platform reproduction.** Approval is conditional; the condition has not been checked. Treat as blocked. |

**Primary source ratified 2026-07-16: Google Business Profile.** S5 is designed around it — transcribe each genuine Google review into a `testimonial` entry with its public `source_url`, verify against the source (§3), and the section activates automatically. Judge.me/Loox remain approved fallbacks and would supersede transcription if adopted.

**Currently installed: none.** Verified 2026-07-16 — no Judge.me, Loox, Shopify Product Reviews, Okendo, Stamped or Yotpo metafields exist on the store. **There is presently zero genuine review data**, which is why S5 renders nothing.

**Anything not on this list is not a source.** Screenshots, WhatsApp messages, staff recollection, "we know customers love it", and the agency's imagination are **not** sources.

---

## 2. Review governance — the data model

Genuine reviews live in the **`testimonial` metaobject** ("Verified Review", created 2026-07-16, `gid://shopify/MetaobjectDefinition/13988495529`). **Admin → Content → Metaobjects → Verified Review.**

| Field | Type | Required | Governance |
|---|---|---|---|
| `author` | text | ✅ | Exactly as published at the source. Never invent, never embellish, never "tidy". |
| `body` | multi-line text | ✅ | **Verbatim.** Do not rewrite, improve grammar, or trim in a way that changes meaning. |
| `rating` | integer 1–5 | ✅ | As given by the reviewer. Validation enforces 1–5. |
| `source` | text | ✅ | One of the approved sources in §1. |
| `source_url` | url | ✅ | **Public link to the original review. This is the audit trail — no link, no publish.** |
| `review_date` | date | ✅ | As published at the source. |
| `verified` | boolean | ✅ | **Only `true` renders.** See §3. |

**Every field is mandatory by schema.** An entry cannot be saved without its proof link — the data model, not a policy document, is what enforces this.

**Why a metaobject and not section settings:** review text typed into a theme section is indistinguishable from fiction and has no provenance. That is exactly how the fabricated testimonials in §8 came to exist. `sections/home-reviews.liquid` has **no setting capable of holding review text, a name, a rating or a count** — fabrication is impossible by construction, not by good intentions.

---

## 3. Review moderation

**Before ticking `verified`, a human must:**
1. Open `source_url` in a browser.
2. Confirm the **name, text, rating and date** match the entry exactly.
3. Confirm the review is about **The Baking Kaur** and is not a reply, a rating-only entry, or spam.
4. Only then tick **Verified against source**.

**Never tick `verified` on an entry you did not personally open and check.**

**Selection rules — what may be excluded, and what may not:**
- ✅ You **may** choose which genuine reviews to feature (curation is normal merchandising).
- 🚫 You **may not** edit a review's wording to make it more positive.
- 🚫 You **may not** display a rating that contradicts the source.
- 🚫 You **may not** imply the featured set represents the overall rating — see §5.

**Removal:** if a reviewer deletes or edits their review at the source, the entry must be updated or removed. **Re-verification cadence: every 6 months**, or immediately if a reviewer complains. A review displayed after its author removed it is a live liability.

**Right of reply:** never publish a customer's full name beyond what the source already shows publicly, and never add a photo, location or order detail the source did not publish.

---

## 4. Schema rules

**The homepage reviews section emits NO structured data. Deliberately.**

| Schema | Where | Allowed? |
|---|---|---|
| `AggregateRating` on `Bakery` / `LocalBusiness` / `Organization` | anywhere | 🚫 **NEVER** — see §5 |
| `Review` on `Bakery` / `LocalBusiness` / `Organization` | anywhere | 🚫 **NEVER** — self-serving (§5) |
| `AggregateRating` / `Review` on **`Product`** | PDP only | ⚠️ **Only** from a genuine product-review source (Judge.me / Loox / SPR) with reviews **visible on that same page**. Not currently possible — no source installed. |
| Any rating in `ItemList` (S4 bestsellers) | homepage | 🚫 not without a real per-product source |

**The `Product` schema on PDPs currently carries no `aggregateRating` — verified 2026-07-16. Keep it that way** until a real product-review source exists.

**GEO / AI-search note:** AI assistants (AI Overviews, ChatGPT, Gemini, Perplexity) read the **visible text of the page**, not only the markup. Genuine reviews rendered as real HTML earn AI-search visibility **with no schema at all**. Emitting no markup costs nothing in GEO — and fabricated markup would poison the entity data these systems build about the business.

---

## 5. AggregateRating rules

**🚫 The storefront does not emit AggregateRating. At all. Anywhere.**

Three independent reasons, each sufficient on its own:

1. **Google forbids self-serving ratings for LocalBusiness/Organization.** Google's review-snippet guidelines exclude ratings a business collects, curates or marks up about itself from rich-result eligibility for `LocalBusiness` and `Organization`. A hardcoded rating in the Bakery schema is not merely ineligible — it is the shape of markup that earns a manual action for spammy structured data.
2. **A featured subset is not an aggregate.** If 3 hand-picked 5★ reviews are displayed, computing `AggregateRating` from those 3 would declare the business is rated 5.0 — a number no data supports. **Never compute an aggregate from the displayed subset.** This is a subtle, easy, and very common way to lie with true data.
3. **Genuine Google ratings do not need our markup.** The real Google rating already surfaces in Google's own knowledge panel and Maps. Re-declaring it in our own markup adds no visibility and imports all the risk.

**If AggregateRating is ever proposed again**, all of the following must be true first — and it must be re-checked against Google's then-current guidelines, not against this document:
- it describes a **`Product`**, never the business;
- it is **computed from a real review source**, never typed in;
- every counted review is **visible on the same page**;
- the count and value **match the source exactly** at render time.

**A visible claim is still a claim.** Writing "4.8 on Google" in copy — with no markup — is a factual assertion. It requires a real, current figure and a link customers can check. Do not state a rating you cannot prove today, and do not let a once-true number go stale.

---

## 5b. Brand milestones are NOT review data  *(client decision 2026-07-16)*

**"20,000+ celebrations" is a brand milestone and a trust signal. It is not a review claim.**

| Permitted | Prohibited |
|---|---|
| ✅ Stating it as a milestone in trust copy ("20,000+ celebrations") | 🚫 Presenting it as a **review count** ("20,000+ reviews") |
| ✅ Treating it as a trust signal | 🚫 Feeding it into **`AggregateRating.reviewCount`** — in any schema, anywhere |
| | 🚫 Pairing it with a star rating so it reads as a rating basis |
| | 🚫 Implying 20,000 people rated the bakery |

**Why the distinction is load-bearing.** A count of *customers served* and a count of *ratings received* are different facts. Merging them — "4.8 ★ from 20,000+ customers" — manufactures a rating basis out of an operational statistic. That is precisely the shape of the removed `4.8 / 500` markup (§8): a real-sounding number with nothing behind it. The prohibition stands **even though the milestone itself may be true**.

**Substantiation.** The figure is the client's own and is currently **unverified**. Client decision 2026-07-16: *if it cannot be substantiated, replace it with a verified milestone* — e.g. an order count from Shopify, or years in operation. Both are checkable; neither requires a review.
**Standing rule:** a milestone must be replaceable with a real number, never quietly retired into vagueness ("thousands of happy customers"). Vagueness is what an unsubstantiated claim decays into.

---

## 6. Google compliance

- **No fabricated reviews.** Beyond SEO, fabricated reviews attributed to invented individuals are a consumer-protection matter — India's CCPA guidelines on fake reviews, and equivalents elsewhere. This is a legal exposure, not a ranking risk.
- **No incentivised reviews presented as organic.** If a review was ever solicited with a discount or freebie, that must be disclosed — or the review not used.
- **No self-serving LocalBusiness ratings** (§5).
- **Markup must match visible content.** Never mark up a review that a customer cannot see on that page.
- **`rel="nofollow noopener ugc"`** on every outbound link to a review source — implemented in `home-reviews.liquid`. `ugc` correctly labels user-generated content; `nofollow` prevents passing authority to a third-party profile.
- **No review gating** (soliciting only happy customers, or filtering negatives before they're published). If Judge.me or Loox is adopted, **do not enable review gating** — Google treats it as deceptive.

---

## 7. AI search compliance (GEO)

- **Real reviews are strong AI signals; fabricated ones are poison.** AI systems cross-reference claims against Google, Zomato, Maps and social. A homepage claiming reviews that exist nowhere else creates a **contradiction** in the entity graph — which is worse than silence, because it undermines every other claim on the site.
- **Consistency across sources is the asset.** The rating shown on-site must match Google exactly. A mismatch is a trust signal *against* the business.
- **Visible text is enough.** See §4 — no markup is required for AI visibility.
- **Never let AI-search ambition drive fabrication.** "It would help us rank for *is The Baking Kaur good*" is not a reason to invent a review. The honest answer to a thin review profile is to **collect more real reviews**, not to author them.

---

## 8. Incident record — fabricated reviews found live (2026-07-16)

**Found:** the production homepage was publishing **4 fabricated testimonials attributed to named individuals** (Aisha Patel, Ravi Sharma, Neha Verma, Amit Verma), plus a **hardcoded `AggregateRating` of 4.8 / 500 reviews** in the `Bakery` schema — rendered from `snippets/bk-local-business.liquid` in `<head>`, and therefore present on **every page of the site**, not just the homepage.

**Origin:** unreplaced Ecomus theme demo content. Two independent tells: the reviews praised **almond croissants, breads, cinnamon rolls and coffee** — a butter-and-egg café menu, for a 100% eggless cake bakery that delivers — and one contained a *complaint* ("they close a bit early"), which no business writes into its own testimonials. The `4.8/500` was backed by no data whatsoever.

**Fixed (client-approved, verified on production):** fabricated blocks deleted from `templates/index.json`; section disabled and gracefully hidden (no orphan heading, no orphan schema); `aggregateRating` removed from `bk-local-business.liquid` with a permanent guard comment; a theme-editor-only placeholder reads *"Waiting for verified review source."*

**Lessons encoded, not just noted:**
1. **Demo content is a live liability from day one** — it is written to look plausible, so it survives review. Audit every theme section for demo text before launch.
2. **Provenance must be structural.** The fix is not "don't type fake reviews" — it is a data model where a review **cannot be saved without a public proof link**, and a section with **no field capable of holding review text**.
3. **Schema in `<head>` is sitewide.** A single fabricated snippet contaminated all ~1,200 pages. Head-rendered schema deserves the highest scrutiny.
4. **A rating found in a theme is not data.** If nobody can name where a number came from, it is fabricated until proven otherwise.

---

## 9. Status & activation path

**Current state:** `sections/home-reviews.liquid` is **FROZEN v1.0** and live-safe, rendering **nothing** — because there are **0 verified reviews**. This is the correct, specified behaviour, not a defect.

**To activate — in order:**
1. Choose a source (§1). **Google Business Profile is Priority 1**; Judge.me is the strongest long-term option because it produces *verified-buyer* reviews continuously without transcription.
2. If transcribing: create one `testimonial` entry per review, complete every field, open each `source_url`, then tick `verified` (§3).
3. The section appears **automatically** at the first verified entry. No code change, no deploy.
4. **Do not add AggregateRating** (§5).
5. If Judge.me/Loox is installed instead, this section defers to the app's own widget — retire it rather than run two review systems.

**Backlog:** *"Collect genuine reviews"* — the real fix for a thin review profile is more real reviews. A bakery with 20,000+ claimed celebrations should have no difficulty; it has simply never asked.

_v1.1 — 2026-07-16. Google Business Profile ratified as primary source; brand-milestone rule added (§5b). v1.0 — created after fabricated reviews were found live and removed. Governs all review content in every phase._
