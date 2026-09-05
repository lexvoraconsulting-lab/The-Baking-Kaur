# CONTENT_FACTORY.md — Phase 2A

**The production pipeline.** Architecture is locked as **BLOG_OS v1.0** (= `BLOG_ARCHITECTURE.md`
v2.1). Nothing here changes it.

---

## 0. The constraint this factory is built for

Every design choice below follows from four facts established in Phase 1:

| Fact | Consequence for the factory |
|---|---|
| **1 operator**, Basic plan, **2 staff seats** | No multi-role hand-offs. Roles are hats, not people |
| **No Shopify Flow** | No workflow automation inside Shopify. State lives in a file |
| **4 articles/week sustainable** | ~20 operator-touches/week is the entire budget |
| **76 launch articles, ~250 ceiling** | The system must be boring at 250 rows, not clever at 20 |

A factory that costs more to operate than the writing it governs is not a factory.

---

## 1. The 26 checks → 6 stages

The requested pipeline lists 26 steps. **All 26 are preserved.** They are grouped into 6 stages,
because a stage is a *state transition an operator performs* and 26 of those per article is
~2,000 hand-offs for the launch set.

```
  S1 COMMISSION  →  S2 BLUEPRINT  →  S3 DRAFT  →  S4 VERIFY  →  S5 REVIEW  →  S6 SHIP & OPERATE
       spec           structure       writing      machine       human +        publish, measure,
                                                    checks        panel          refresh
```

| Stage | Requested steps absorbed | Output | Status |
|---|---|---|---|
| **S1 Commission** | Topic · Intent Analysis · Entity Analysis · Competitor Analysis · Keyword Cluster · Search Intent Validation · Collection Mapping · Product Mapping | A complete `ARTICLE_SPEC` row | `SPEC` |
| **S2 Blueprint** | Outline Generation · Internal Linking Plan · FAQ Generation · Schema Plan · Image Requirements · Video Requirements | H2/H3 skeleton + link + media plan | `BLUEPRINT` |
| **S3 Draft** | Draft · SEO Optimization · GEO Optimization · AI Retrieval Optimization | Finished prose | `DRAFT` |
| **S4 Verify** | Fact Checking · EEAT Validation · (18 Quality Gates) | Gate report, all PASS | `VERIFIED` |
| **S5 Review** | Editorial Review · Brand Review · AI Review · Final QA | Panel scores ≥ threshold | `APPROVED` |
| **S6 Ship & Operate** | Ready For Publishing · Performance Tracking · Refresh Cycle | Live article + KPI row | `LIVE` → `REFRESH_DUE` |

### Two deliberate departures from the diagram

**1. Optimization is not a stage.** The diagram places SEO, GEO and AI-retrieval optimization
*after* drafting. Optimizing prose after it is written is precisely how formulaic,
retrofitted-for-search content gets made — the pattern Google's helpful-content system targets and
the one `DESIGN_REVIEW.md` M-26 already flagged in our own v1 anatomy.

They move upstream: **structure** decisions (what gets answered, in what order, what links where)
happen in S2; **language** decisions happen while writing in S3. S4 then *verifies* they were done
— it does not *apply* them.

**2. Fact-checking runs before review, not after drafting only.** A reviewer scoring an article
whose facts have not been checked is scoring fiction. S4 is machine-checkable gates and source
verification; S5 is judgement. Never the reverse.

---

## 2. Stage detail

### S1 · COMMISSION → `SPEC`

**Purpose:** decide whether the article should exist at all. This is the cheapest place to kill
one, and the only place where killing one is free.

| Step | What actually happens | Kill condition |
|---|---|---|
| Topic | Pull the next item from `blog_master.csv` by priority | — |
| **Commissioning test 1** | Does a collection or page already serve this query? | **Yes → REJECT.** It is collection copy, not an article |
| **Commissioning test 2** | Does the answer change if the city changes? | Yes → `meerut`. No → `cake-guides` |
| Intent analysis | Classify: decision / understanding / local | Ambiguous → reject, split, or re-scope |
| Entity analysis | Which entities does this touch? (`ENTITY_RELATIONSHIP_MAP.md` §4) | No entity → probably not a topic |
| Competitor analysis | Top 5 SERP results; what do they *not* answer? | Nothing to add → **REJECT** |
| Keyword cluster | 1 primary, 3–6 secondary, 8–15 semantic | Primary already owned by our own URL → reject |
| Search intent validation | Does the SERP show informational results? | SERP is all product/collection pages → **REJECT**, transactional |
| Collection mapping | Assign `target_collection` | — |
| Product mapping | 1–3 illustrative products → `about_refs` | — |
| **Commercial destination** | ≥1 collection this article links down to | **None → REJECT** (locked condition 5) |

**Reject is the expected outcome for a meaningful share of commissions.** A factory that never
rejects is a conveyor belt.

Two of the requested steps — competitor analysis and search-intent validation — **require SERP
access this environment does not have** (`Q7` in `DECISION_LOG.md`). Until GSC and manual SERP
checks are available, they are performed by the operator by hand, in a browser, and recorded as a
one-line note. They are not skipped and not simulated.

### S2 · BLUEPRINT → `BLUEPRINT`

**Purpose:** make every structural decision before a word of prose is written, so the writer
writes prose instead of scaffolding.

Produces, in one document:
- **Outline** — H1, the direct answer (≤60 words), H2/H3 skeleton, one idea per section.
- **Internal linking plan** — the exact URLs: 1 up · ≤2 lateral · ≤3 collection · ≤3 product ·
  ≤1 cross-silo. Plus the anchor text for each, checked against the anchor policy.
- **FAQ plan** — 2–4 questions **as prose subheadings**, not schema. Per-article `FAQPage` was
  removed in v2 (no rich result for commercial sites). Questions must be ones the article
  genuinely answers, and must not duplicate the 43 site FAQ metaobjects.
- **Schema plan** — for 95% of articles this is one line: *"`Article` + `BreadcrumbList` +
  `about`/`mentions`, emitted by the template."* Deviations require a reason.
- **Image requirements** — subject, count, alt text intent. Original photography only.
- **Video requirements** — **`none` by default.** The store cannot currently produce still
  photography (`CLAUDE.md` blocker); designing a video pipeline for it would be building for a
  capability that does not exist. The field exists in the spec so it can be filled later.

### S3 · DRAFT → `DRAFT`

Write it. The blueprint is the brief; deviating from the blueprint is allowed and expected — if the
writing reveals the outline was wrong, **fix the blueprint, don't force the prose.**

Optimization happens *here*, as writing decisions:
- **SEO** — primary keyword in H1, title, first 60 words, naturally. Secondaries where they fit.
  Never forced.
- **GEO** — the direct answer is self-contained and quotable without surrounding context.
  First-party specifics (real lead times, real price bands) over adjectives.
- **AI retrieval** — question-shaped subheadings; one idea per paragraph; no critical fact
  expressed only in an image or a table cell.

**Anti-formula rule:** if the last two articles in this cluster open the same way, this one opens
differently. Enforced at S5, decided at S3.

### S4 · VERIFY → `VERIFIED`

**Machine-first.** Everything scriptable is scripted; only what needs a human gets one.

1. **Fact check.** Every factual claim assigned to a bucket (`EDITORIAL_STANDARDS.md` §2):
   catalogue fact → re-read from the Admin API at check time; operational fact → cite the source
   doc; craft claim → confirmed by the studio. **Unbucketable claim → cut it.**
2. **E-E-A-T validation.** Byline resolves · first-party evidence present · no unsourced claim ·
   no superlative.
3. **18 Quality Gates** (`QUALITY_GATES.md`). Every gate PASS/FAIL, ~11 of 18 scriptable.

Any FAIL returns the article to S3 with the specific gate named. Not "needs work".

### S5 · REVIEW → `APPROVED`

`AI_REVIEW_SYSTEM.md`. Tiered — a 12-reviewer panel on every article is not affordable at 4/week
and, more importantly, not *useful*: the marginal reviewer stops finding things.

| Article type | Panel |
|---|---|
| Pillar `P` | Full 12-reviewer panel |
| Cluster `C`, Local `LO` | Core 5 |
| Seasonal `S` refresh | Core 3 |

Plus the two human passes the diagram asks for — **Editorial** (does it read well and say something)
and **Brand** (does it sound like us) — which on a 2-seat plan are the same person wearing two hats,
24 hours apart.

### S6 · SHIP & OPERATE → `LIVE`

- Publish checklist (`EDITORIAL_STANDARDS.md` §7) — the last gate before the button.
- Set `last_reviewed`; confirm `dateModified` reflects it.
- Record the baseline KPI row (`MEASUREMENT_FRAMEWORK.md`).
- Schedule the refresh date by type. When it arrives, status → `REFRESH_DUE` and the article
  re-enters at **S4**, not S1 — the commission is still valid, only the facts have aged.

---

## 3. State machine

```
   BACKLOG ──commission──> SPEC ──> BLUEPRINT ──> DRAFT ──> VERIFIED ──> APPROVED ──> LIVE
      │                      │                      ^          │            │          │
      │                      │                      └──fail────┘            │          │
      │                      │                      ^                       │          │
      │                      │                      └────────panel reject───┘          │
      │                      v                                                         │
      └──> REJECTED <────────┘                                          REFRESH_DUE <──┘
                                                                              │
                                                                              └──> S4
   Terminal: LIVE · REJECTED · ARCHIVED
   Blocked:  HELD (reason required: photography | delivery-data | inventory | author | GSC)
```

**`HELD` is a first-class state, not a comment.** Six of the 76 launch articles are held today
(photography, delivery data, bento inventory). A held article with no stated blocker is a bug in
the database.

---

## 4. Throughput

| Stage | Pillar | Cluster |
|---|---:|---:|
| S1 Commission | 90 min | 40 min |
| S2 Blueprint | 90 min | 45 min |
| S3 Draft | 6–9 h | 2.5–4 h |
| S4 Verify | 60 min | 30 min |
| S5 Review | 90 min | 40 min |
| S6 Ship | 30 min | 20 min |
| **Total** | **11–14 h** | **5–7 h** |

At 4 clusters/week ≈ 20–28 h. **That is a full-time role.** If the operator has other duties, the
honest rate is 2/week and the launch set takes ~38 weeks, not ~25.

Stated plainly so the number is chosen rather than discovered.

---

## 5. Batching — where the real leverage is

Doing one article end-to-end is the slowest way to run this. Batch by stage:

| Batch | Cadence | Why |
|---|---|---|
| **Commission 8 at once** | monthly | Cross-checking 8 specs against each other catches cannibalization one-at-a-time review misses |
| **Blueprint 4 at once** | weekly | Internal-link plans are written *between* articles; planning 4 together produces a real link graph |
| **Draft 1 at a time** | daily | Writing does not batch |
| **Verify 4 at once** | weekly | The scripted gates run over a folder as cheaply as over a file |
| **Review 4 at once** | weekly | The panel rubric is loaded once |

Batching cuts the per-article overhead roughly in half without touching draft time.

---

## 6. What the factory refuses to do

| Refusal | Why |
|---|---|
| Publish without a commercial destination | Locked condition 5 |
| Publish a locality article without real delivery data | Doorway page |
| Publish a hamper article | 0 active hamper products — traffic to an empty shelf |
| Emit a second `FAQPage` anywhere | One site-wide, on `/pages/faqs` |
| Invent an author, review, rating, or licence number | Standing rule; three removals already |
| Create a new tag beyond 20 without retiring one | Locked |
| Change an article's handle or silo after publish | Locked — both change the URL |
| Add a metafield beyond the 5 | Locked — no Flow on Basic; hand entry is the cost |
| Touch `main-product-premium-v2.liquid` | Protected module |

**These are enforced in the workflow, not remembered.** A refusal that depends on someone
recalling it is not a control.

---

→ `ARTICLE_SPEC.md` · `CONTENT_WORKFLOW.md` · `QUALITY_GATES.md`
