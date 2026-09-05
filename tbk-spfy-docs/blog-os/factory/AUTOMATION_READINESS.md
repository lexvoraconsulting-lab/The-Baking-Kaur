# AUTOMATION_READINESS.md — Phase 2H

How a future AI agent operates this factory **without changing the architecture**.

---

## 1. The contract

An agent is a **worker inside the pipeline**, never an owner of it.

| An agent MAY | An agent MAY NOT |
|---|---|
| Move an article S1 → S5 | Move an article to `LIVE`. **Publishing is human-only** |
| Draft, revise, restructure | Change `silo`, `parent_cluster`, `primary_keyword`, `hub_url`, `target_collection`, or the handle |
| Run gates and report failures | Override or soften a gate |
| Propose FAQs, links, schema | Create a tag beyond the 20, or a metafield beyond the 5 |
| Read the Admin API | Write to Shopify without `--apply` and a human |
| Update `last_reviewed` **after** re-verifying | Bump `last_reviewed` without re-reading the article |
| Flag an architectural problem | Change the architecture |
| Say "I cannot verify this" | Invent a fact, source, review, rating, licence number or author |

**The single hardest rule:** an agent that cannot verify a claim **removes it and says so**. It
never fills a gap with something plausible. Three removals have already happened on this project
because plausible content shipped.

---

## 2. What is automatable, and what is not

| Stage | Automatable | Why |
|---|:---:|---|
| S1 Commission | **partly** | Keyword clustering and entity mapping: yes. Competitor analysis and SERP validation: **needs SERP access**. The reject decision stays human — it is a business call |
| S2 Blueprint | **yes** | Outlines, link plans, FAQ candidates, schema — all deterministic given a spec |
| S3 Draft | **yes, with a floor** | An agent drafts. **First-party facts must come from a human or the API** — an agent cannot know how our sponge behaves in June |
| S4 Verify | **mostly** | ~11 of 18 gates are already scripted. Fact-checking against the API: yes. Craft claims: human |
| S5 Review | **yes** | The panel is already a rubric. Note the correlated-blind-spot caveat in `AI_REVIEW_SYSTEM.md` §0 |
| S6 Ship | **no** | Publishing is irreversible-ish and outward-facing. Human, always |
| Refresh | **partly** | Detect debt, re-read catalogue facts, propose diffs: yes. Approve: human |

**The boundary is not capability, it is reversibility.** Everything before publish is a file in
git. Publish puts a URL in front of customers and into an index.

---

## 3. The eight requested capabilities

| # | Capability | Ready? | Depends on |
|---|---|:---:|---|
| 1 | Generate drafts | ✅ | `ARTICLE_SPEC` row + blueprint + `CONTENT_TEMPLATES` |
| 2 | Update articles | ✅ | `blog_master.csv` + refresh trigger |
| 3 | Refresh statistics | ⚠️ | Admin API for catalogue facts. **Operational facts need the source docs kept current** |
| 4 | Repair internal links | ✅ | `blog_audit.py` + the link budget |
| 5 | Suggest FAQs | ✅ | Must dedupe against the 43 site metaobjects |
| 6 | Generate schema | ✅ | Template-emitted; the agent supplies `about_refs` |
| 7 | Improve readability | ✅ | G12 thresholds are numeric |
| 8 | Monitor rankings | ❌ | **Blocked on GSC access (Q7).** No amount of agent design substitutes for the data |

Seven of eight are ready the moment the three scripts exist. The eighth is a credential, not an
engineering problem.

---

## 4. What makes this automatable — five properties, already built

The factory was designed so agents need no special accommodation. Each property exists for a
human-facing reason *and* happens to be what an agent requires.

| Property | Where | Why it matters to an agent |
|---|---|---|
| **State in a file, not in someone's head** | `blog_master.csv` | An agent can read the queue, pick work, and record the result |
| **Numeric, closed-question gates** | `QUALITY_GATES.md` | An agent can self-check before asking for review. 11 of 18 need no judgement |
| **Rubric-based review** | `AI_REVIEW_SYSTEM.md` | Reviews are reproducible instead of impressionistic |
| **5 metafields, not 31** | `ARTICLE_SPEC.md` §0 | A small, stable write surface — the only fields an agent ever pushes to Shopify |
| **Dry-run by default** | `seo-ops/` convention | Every agent action is inspectable before it commits |

None of this was added for agents. It is the same discipline that makes the system operable by one
tired human on a Friday — which is the better test.

---

## 5. Job specifications

Each is a scoped task with a defined input, output and refusal condition.

### `draft-article`
**In:** `article_id` with `status=BLUEPRINT`
**Out:** draft markdown; `status=DRAFT`
**Refuse if:** spec incomplete · no `target_collection` · a required fact is unavailable
**Never:** invent a lead time, price, delivery window or craft claim

### `run-gates`
**In:** `article_id` with `status=DRAFT`
**Out:** 18-row PASS/FAIL table with failing lines quoted verbatim
**Never:** mark a gate PASS that it could not evaluate — report `UNKNOWN` and escalate

### `review-panel`
**In:** `article_id` with `status=VERIFIED`
**Out:** panel block per `AI_REVIEW_SYSTEM.md` §4
**Never:** return feedback without a location and a specific change

### `refresh-audit`
**In:** whole CSV, monthly
**Out:** rows past `next_review_due`; orphans (<2 inbound); tag count vs 20; broken links
**Never:** update `last_reviewed` — that is the refresh job's output, after re-verification

### `link-repair`
**In:** an orphan or broken-link report
**Out:** proposed link edits, within budget
**Never:** link a tag page · exceed the budget · use a collection's exact primary keyword as anchor

### `fact-refresh`
**In:** an article due for refresh
**Out:** a diff of catalogue facts (sizes, flavours, price floors) vs the live API
**Never:** change an operational or craft claim — those come from source docs and the studio

---

## 6. Guardrails that must hold before any agent runs

| Guardrail | Status |
|---|---|
| `blog_validate.py` in CI on every CSV commit | **not written** — Phase 3 |
| `blog_gates.py` for the 18 gates | **not written** — Phase 3 |
| `blog_audit.py` for orphans and refresh debt | **not written** — owed since Phase 1 |
| Publishing requires a human `--apply` | ✅ house convention |
| Git history as the audit trail | ✅ |
| Locked-field list enforced by the validator | **not written** |

**No agent should run any job before `blog_validate.py` exists.** Without it the locked fields are
protected by convention alone, and convention is not a control.

---

## 7. The JARVIS-readiness question

A future orchestrating agent needs four things. Three exist:

| Need | State |
|---|---|
| **A machine-readable model of the work** | ✅ `blog_master.csv` + the state machine |
| **Deterministic quality criteria** | ✅ 18 gates, numeric thresholds |
| **A clear authority boundary** | ✅ §1 — and publish is always human |
| **Feedback from reality** | ❌ **blocked on Q7.** Without GSC, an agent optimises against a rubric instead of against outcomes |

The fourth is the important one. **An agent with perfect gates and no outcome data will produce
articles that pass every check and may earn nothing** — and it will do so at scale, confidently.
That is the failure mode this whole document is arranged against, and it is closed by a credential
rather than by more automation.

---

## 8. What must never be automated

| Never | Why |
|---|---|
| **Publishing** | Outward-facing and effectively irreversible once indexed |
| **The commission reject decision** | A business call about what the brand should say |
| **Craft and operational claims** | An agent cannot know how our sponge behaves in a Meerut June |
| **Anything touching the trust layer** | Reviews, ratings, FSSAI, author identity. Three removals already |
| **Architecture changes** | Locked. Requires a `DECISION_LOG.md` entry and a human |
| **`--apply` on any store write** | House rule, and the reason nothing has broken yet |
