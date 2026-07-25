# AI_REVIEW_SYSTEM.md — Phase 2E

**Stage S5.** Runs only on articles that already passed all 18 quality gates. A panel reviewing
unverified facts is scoring fiction.

---

## 0. What this system honestly is — and is not

**It is** a structured multi-perspective critique, run to a fixed rubric, that catches problems a
single read misses.

**It is not** twelve independent reviewers. One model simulating twelve roles has **correlated
blind spots** — if it is wrong about what Google rewards, it is wrong in all twelve voices at once,
and the consensus will look like agreement rather than a shared error.

Three consequences, built in rather than disclaimed:

1. **Reviewers are rubric-driven, not vibe-driven.** Each answers specific closed questions. The
   value is in the checklist, not the persona.
2. **The Customer reviewer outranks the rest on a tie.** It is the only one grounded in something
   real rather than in a model of an algorithm.
3. **A perfect panel score means nothing on its own.** It is a floor, not evidence. Real evidence
   is in `MEASUREMENT_FRAMEWORK.md`.

---

## 1. Tiering

12 reviewers on every article is unaffordable at 4/week and, past a point, unhelpful — the marginal
reviewer stops finding anything.

| Type | Panel | Reviewers |
|---|---|---|
| **Pillar `P`** | Full 12 | all |
| **Cluster `C`** | Core 5 | Helpful Content · AI Overviews · Technical SEO · Brand · Customer |
| **Local `LO`** | Core 5 + Local SEO | ″ + Local |
| **Seasonal `S`** refresh | Core 3 | Helpful Content · Brand · Customer |

---

## 2. The panel

Each reviewer scores **/10** and returns **actionable feedback** — a specific line and a specific
change. "Could be stronger" is a void review and is re-run.

### R1 · Google Helpful Content
*Was this made for people, or for search?*
- Does it answer the title question completely?
- Information not in the top 3 SERP results — named specifically?
- Written from experience, or summarised from other pages?
- Any section present only to hold a keyword?
- Would it exist if search engines did not?

**Auto-fail:** any section that exists only for a keyword.

### R2 · Google AI Overviews
*Can a passage be lifted and shown as an answer?*
- Is the first-60-words answer self-contained out of context?
- Are subheadings phrased as real questions?
- Any critical fact only in an image or table cell?
- Is the claim attributable to a resolvable entity?

**Auto-fail:** the answer does not survive extraction.

### R3 · ChatGPT Search
*Would I cite this?*
- Is the source identifiable and specific?
- Is there first-party information unavailable elsewhere?
- Is it current, with a real `dateModified`?
- Is anything overstated relative to what is proven?

### R4 · Gemini
*Does this resolve into the knowledge graph?*
- Do entity mentions match the site's own entity set?
- Do `about`/`mentions` point at real Product/Collection nodes?
- Is the business entity disambiguated from other "Kaur" bakeries?
- Do local claims match the `Bakery` node?

### R5 · Claude
*Is this honest?*
- Any claim that cannot be substantiated?
- Are limits and trade-offs stated, or only benefits?
- Does the confidence match the evidence?
- Would a reader be misled by anything, including by omission?

**Auto-fail:** any claim that survives into the draft without a verification bucket.

### R6 · Perplexity
*Is it citable and corroborated?*
- Is there a specific, quotable fact rather than general advice?
- Would an external source corroborate it?
- Is it structured for excerpting — short paragraphs, clear claims?

### R7 · Technical SEO
*Re-checks G1–G4 by reading rather than parsing.* Title/H1 relationship, heading logic, link
placement in context, schema appropriateness, keyword placement that reads naturally.

### R8 · Local SEO *(LO only)*
Locality named naturally, not stuffed · a real locality-specific fact · NAP consistent · no
unfulfillable delivery promise · genuinely useful **to someone in Meerut**.

### R9 · UX
Scannable? · paragraph length? · does the structure match how someone actually reads this? ·
mobile-first (most traffic is phone) · is the next step obvious?

### R10 · CRO
Is the CTA in the right place for the buying stage? · one CTA or several competing? · does the
article build enough confidence to act? · does the WhatsApp link carry its source token? · is the
email capture worth the reader's address?

### R11 · Brand Manager
Against `BRAND_VOICE.md`. Would the owner say this aloud to a customer? · warm and specific, not
breathless? · honest about variation and lead times? · does it sound like the studio or like an
agency?

### R12 · Customer
**The tie-breaker.** Simulated as a named persona from `ARTICLE_SPEC.md` §2.
- Did I get the answer I came for?
- Is anything still unclear?
- Do I trust these people more than before reading?
- Would I message them now?
- Is there anything that makes me trust them *less*?

**The last question finds more than the other eleven reviewers combined.** An overclaim, a stock
photo, a promise that sounds too good — those read as risk to a customer and as "optimised" to
everyone else on the panel.

---

## 3. Thresholds

| Type | Min average | Min any single | Auto-fails |
|---|---:|---:|---|
| Pillar `P` | **8.0** | 7 | 0 |
| Cluster `C` | **7.5** | 6 | 0 |
| Local `LO` | **7.5** | 6 | 0 |
| Seasonal `S` | **7.0** | 6 | 0 |

**Any auto-fail blocks regardless of average.** A 9.5 average with one auto-fail is a fail.

| Outcome | Action |
|---|---|
| Threshold met, no auto-fail | → `APPROVED` |
| 1–2 reviewers below minimum | Fix the named lines, re-run **those reviewers only** |
| ≥3 below minimum | Return to **S3**. The draft is the problem |
| Any auto-fail | Return to S3 with the auto-fail quoted verbatim |
| Same reviewer fails 3 articles running | **Stop.** The template or the brief is wrong — fix the system |

---

## 4. Output format

One block per article, appended to `docs/blog-os/factory/reviews/{article_id}.md`:

```
ARTICLE: CG-P2-01 · v1.0 · panel: core-5 · date: YYYY-MM-DD

R1  Helpful Content   8  Serving numbers are ours, not generic. §"1kg" repeats §"500g" — merge.
R2  AI Overviews      7  Opening answer depends on the H1 to make sense. Rewrite standalone.
R7  Technical SEO     9  —
R11 Brand             8  "Perfect for any celebration" is agency filler. Cut or make specific.
R12 Customer          6  Still don't know what to do for 15 people — the table jumps 10 to 20.

AVERAGE 7.6  ·  MIN 6  ·  AUTO-FAILS 0  ·  VERDICT: REVISE (R2, R12)
```

Every line names a location and a change. That is the whole standard.

---

## 5. Cost

| Panel | Reviewers | Operator time |
|---|---:|---:|
| Full 12 (pillar) | 12 | ~90 min |
| Core 5 (cluster) | 5 | ~40 min |
| Core 3 (seasonal) | 3 | ~20 min |

Batch 4 clusters weekly: the rubric loads once, ~2 hours for the batch.

---

## 6. What the panel cannot tell you

Stated so it is not quietly forgotten:

- **Whether the article will rank.** It has no SERP access and no GSC data.
- **Whether anyone searches for this.** Demand validation is `Q7`, still open.
- **Whether an LLM will actually cite it.** That is measured monthly in
  `MEASUREMENT_FRAMEWORK.md` §5, against real prompts.
- **Whether the facts are true.** That was S4's job and must already be done.

The panel raises the floor on quality. It does not predict outcomes, and a document that implied
otherwise would be selling the same false comfort as a hardcoded 4.9-star rating.
