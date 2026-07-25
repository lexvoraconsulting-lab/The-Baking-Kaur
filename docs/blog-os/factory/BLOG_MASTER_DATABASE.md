# BLOG_MASTER_DATABASE.md — Phase 2C

**The source of truth for the blog operation.**

---

## 1. Storage format — recommendation and reasoning

### Recommended: **one git-tracked CSV** — `docs/blog-os/factory/blog_master.csv`

Plus the Shopify Admin API as the authority for *published* state. Two stores, one boundary, no
overlap:

| Authority for | Lives in | Because |
|---|---|---|
| Planning, pipeline state, everything pre-publish | `blog_master.csv` | Shopify has no place to put it |
| Published article content and the 5 render-time metafields | **Shopify** | It is already the source of truth; duplicating it guarantees drift |

The CSV never mirrors article body text. It holds the spec, the state, and the KPI pointers.

### Why CSV

| Property | Why it decides it |
|---|---|
| **Diffable in git** | A spec change shows up in a commit diff. Reviewable, revertible, attributable. This is the single biggest argument |
| **Editable without a tool** | Opens in Excel or Sheets. The operator is a baker, not a DBA |
| **Already the house pattern** | Every `seo-ops/` script is dry-run → CSV → `--apply`. Zero new conventions, zero new dependencies |
| **Trivially machine-readable** | `csv` from the stdlib. No ORM, no migration, no schema versioning |
| **Right-sized** | 76 rows now, ~250 at ceiling. A query engine for 250 rows is ceremony |
| **Survives the operator** | A plain file needs no account, no subscription, no login |

### Why not the alternatives

| Rejected | Reason |
|---|---|
| **SQLite** | Not diffable — the file is a binary blob, so git shows "changed" and nothing else. Needs a tool to edit. Buys indexing and joins that 250 rows never need. Would be right at ~10,000 rows |
| **Markdown table** | Breaks on commas and quotes in prose fields (`content_goal`, `faqs`, anchor text). Unsortable, unfilterable at 250 rows. Fine for 20 |
| **Airtable / Notion** | Another subscription, another auth, another sync surface. Lives outside git so it cannot be reviewed with the code that reads it. Best UI here, worst durability |
| **Google Sheets** | Same off-git problem, but free and multi-editor. **The one legitimate alternative** — see §6 |
| **Shopify metafields as primary** | 31 fields × 250 articles = 7,750 hand entries with no Flow on Basic. Precisely the failure `DESIGN_REVIEW.md` F-05 rejected |
| **JSON / YAML** | Diffs cleanly, but no operator will hand-edit 250 nested records, and it loses spreadsheet editing for nothing gained |

### The honest trade

CSV has **no referential integrity, no types, and no concurrent editing.** Two people editing it
simultaneously will clobber each other.

On a **2-seat Basic plan with one operator**, none of those costs is real today. All three become
real at roughly 3+ editors — which is the migration trigger in §6, stated in advance so the
decision is made deliberately rather than after a lost afternoon.

---

## 2. Schema

One row per article. Columns are the 31 `ARTICLE_SPEC.md` fields plus 9 operational columns.

```
article_id, status, held_reason, priority, version, owner,
business_goal, content_goal, search_intent, buying_stage, persona,
silo, parent_cluster, child_cluster, content_type, template,
hub_url, target_collection, target_products, primary_cta, secondary_cta,
primary_keyword, secondary_keywords, semantic_keywords, entities, tags,
faqs, internal_links, external_references, image_requirements, video_requirements,
schema_type, word_count_target, reading_time, review_frequency, last_reviewed, author_slug,
-- operational --
working_title, shopify_handle, shopify_article_id, published_at, next_review_due,
gate_status, panel_score, kpi_baseline_date, notes
```

**Conventions**
- List fields are **pipe-separated** (`a|b|c`) — commas appear inside prose fields.
- Dates are ISO `YYYY-MM-DD`.
- Empty ≠ zero. An empty `panel_score` means "not reviewed", not "scored 0".
- `shopify_article_id` is blank until publish and is the join key to the live store.

---

## 3. The eight operations it must support

| Operation | How |
|---|---|
| **Planning** | Filter `status=BACKLOG`, sort by `priority`. Commission the top 8 monthly |
| **Approval** | `status` transitions are the approval record. Git history is the audit trail — who, when, what changed |
| **Writing** | `status=BLUEPRINT` is the writer's queue |
| **Review** | `status=VERIFIED` is the reviewer's queue; `panel_score` and `gate_status` record the outcome |
| **Publishing** | `status=APPROVED` is the publish queue. On publish, write `shopify_article_id`, `published_at`, `next_review_due` |
| **Measurement** | `kpi_baseline_date` links to `blog_kpis.csv` (`MEASUREMENT_FRAMEWORK.md`). Kept separate — one row per article per month there, one row per article here |
| **Refreshing** | `next_review_due < today` → `REFRESH_DUE`. Re-enters at S4 |
| **Archiving** | `status=ARCHIVED` + a note. Rows are **never deleted** — a deleted row loses the record of why a URL exists |

---

## 4. Seed state

`blog_master.csv` is created in this phase, seeded with all **76 planned articles** from
`TOPIC_CLUSTER_MAP.md` — 11 pillars and 65 clusters.

Seeded now: `article_id`, `status`, `held_reason`, `priority`, `silo`, `parent_cluster`,
`content_type`, `working_title`, `hub_url`, `target_collection`, `review_frequency`, `owner`.

Filled at commission (S1) and blueprint (S2): everything else. A seeded row is a **`BACKLOG`
placeholder, not a commissioned article** — it has not passed the commissioning test and may still
be rejected.

**6 rows seed as `HELD`** with a stated reason: CG-6h (photography), ME-1c–1f (delivery-data),
CG-2d (inventory).

---

## 5. Tooling

Three scripts, `seo-ops/` conventions throughout — **dry-run by default, CSV out, `--apply` to
commit.** None is written yet; all three are Phase 3 deliverables.

| Script | Does |
|---|---|
| `blog_validate.py` | Runs §3 of `ARTICLE_SPEC.md` over every row. Exit non-zero on any blocking failure. **Runs in CI on every commit that touches the CSV** |
| `blog_sync.py` | Reconciles CSV ↔ Shopify. Reports rows whose `shopify_article_id` is missing/stale, live articles absent from the CSV, and metafield drift on the 5 locked fields |
| `blog_audit.py` | The orphan + refresh audit owed since `INTERNAL_LINKING_BLUEPRINT.md` §9. Inbound-link counts, refresh debt, tag-count vs the cap of 20 |

`blog_validate.py` in CI is what makes the CSV behave like a database: the constraints live in the
validator instead of the storage engine, and they are enforced on every change rather than
remembered.

---

## 6. Migration triggers

Named in advance so the decision is deliberate.

| Trigger | Move to |
|---|---|
| **3+ concurrent editors** | Google Sheets (keep a CSV export committed weekly, so git remains the audit trail) |
| **>500 rows** | SQLite + a thin CLI. Indexing starts to matter; diffability starts not to |
| **Multi-city, 3+ cities** | Add a `city` column first. Only split files if a single file becomes unreviewable |
| **Real editorial workflow needed** (assignments, deadlines, notifications) | A project tool — but note that means the team grew, which means the Basic-plan constraint that shaped all of this has also changed |

Until one of those fires, **the CSV is the right answer and adding anything else is cost without
benefit.**
