# MEASUREMENT_FRAMEWORK.md — Phase 2G

Per-article KPIs. Extends `../MEASUREMENT_PLAN.md` (programme level) — this file is the
article-level instrument.

---

## 0. The blocking dependency, restated

**No GSC or Analytics access exists in this session** (`Q7`, `DECISION_LOG.md`). Eight of the 13
requested metrics are unobtainable without it.

**Nothing publishes before the baseline is captured** (`BLOG_OS_ROADMAP.md` Gate 1). Publishing
first and instrumenting later means the first months are permanently unmeasurable.

---

## 1. The 13 requested metrics — what is actually obtainable

| # | Metric | Source | Available today | Effort |
|---|---|---|:---:|---|
| 1 | Traffic | GSC clicks / Shopify Analytics | ❌ needs Q7 | free once granted |
| 2 | Rankings | GSC avg position | ❌ needs Q7 | free |
| 3 | CTR | GSC | ❌ needs Q7 | free |
| 4 | Conversions | **WhatsApp source token** + email captures | ✅ **yes** | manual tally |
| 5 | Revenue | Shopify Analytics landing-page report | ❌ needs Q7 | free |
| 6 | Internal link flow | `blog_audit.py` | ✅ **yes** | script |
| 7 | Scroll depth | GA4 event | ❌ needs Q7 | free, needs setup |
| 8 | Time on page | GA4 | ❌ needs Q7 | free |
| 9 | Bounce rate | GA4 | ❌ needs Q7 | **deprioritise — see §4** |
| 10 | AI visibility | **manual prompt panel** | ✅ **yes** | 30 min/month |
| 11 | Featured snippets | GSC position 0 proxy | ❌ needs Q7 | free |
| 12 | AI Overview visibility | manual panel | ✅ **yes** | in #10 |
| 13 | Topical authority | **derived, §5** | ✅ **yes** | script |

**Four of thirteen are measurable today**, and one of those four (#4) is the only one that touches
revenue. That is the argument for Q7 in one line.

---

## 2. `blog_kpis.csv` — one row per article per month

Kept **separate** from `blog_master.csv`: one is state (one row per article, mutable), the other is
history (append-only, never edited).

```
month, article_id, url,
impressions, clicks, ctr, avg_position,            # GSC
sessions, avg_time_on_page, scroll_50, scroll_90,  # GA4
whatsapp_enquiries, email_captures,                # manual tally + form
collection_clicks,                                 # UTM
inbound_links, refresh_due,                        # blog_audit.py
ai_mentions, ai_citations,                         # manual panel
notes
```

Append-only. **A KPI row is never edited after the month closes** — a corrected history is not a
history.

---

## 3. Per-article KPI targets

Targets are set at S6 against `content_type` and `priority`, then reviewed at 90 and 180 days.

| Horizon | Pillar | Cluster | Local |
|---|---|---|---|
| **30 d** | indexed; ≥1 impression | indexed | indexed |
| **90 d** | avg position <40; ≥1 collection click | avg position <50 | ≥1 impression on a locality term |
| **180 d** | avg position <20; ≥1 attributed enquiry | avg position <35 | ≥1 attributed enquiry |
| **365 d** | top 10 on primary keyword; **does not outrank its hub** | top 20 | ranks for the locality term |

**"Does not outrank its hub" is a target, not an aspiration.** An article outranking its hub
collection is a defect (D-002); at 365 days it is measured and, if it happens, the anchors are
fixed within 30 days (`../MEASUREMENT_PLAN.md` §7).

**Not every article will hit these, and that is expected.** The kill criteria exist for the case
where most do not.

---

## 4. Two metrics deliberately deprioritised

**Bounce rate (#9).** For an informational article, a high bounce rate is frequently *success* —
the reader got the answer and left. Optimising against it pushes toward artificially fragmenting
content across pages. Recorded if GA4 is connected; **never used as a quality signal.**

**Time on page (#8).** Same distortion in the other direction: a longer read is not a better one.
Directionally useful in aggregate per cluster; meaningless per article.

Both are recorded because they were requested. Neither drives a decision. Saying so here prevents
someone optimising the wrong thing in six months.

---

## 5. Topical authority contribution — how it is actually derived

There is no supplied "topical authority" metric. Anything sold as one is a vendor composite.
Ours is derived from things that can be counted:

```
cluster_completeness  = published_in_cluster / planned_in_cluster
internal_cohesion     = articles with >=2 inbound links from the same cluster / published
entity_coverage       = distinct entities covered / entities mapped for the silo
ranking_breadth       = distinct queries with an impression, per cluster   [needs Q7]
citation_rate         = AI panel prompts returning a citation / prompts run

authority_index (per pillar) = mean of the available components, 0-1
```

Reported **per pillar**, never per article — authority is a property of a cluster.

**Trend is the signal, not the level.** An index of 0.4 rising is healthier than 0.6 flat.

---

## 6. Attribution — the two things that work without analytics

### WhatsApp source tokens
Every CTA carries the `cluster_id`, so the source arrives inside the chat message.

```
wa.me/918218862928?text=Hi%2C%20I%20read%20your%20guide%20on%20cake%20sizes%20%5Bcg-p2%5D
```

Tallied weekly from the inbox, five minutes. **This is the only revenue-adjacent measurement
available today**, and it needs no plan upgrade, no app and no code beyond the href.

Depends on `Q9` — someone must actually do the tally.

### UTM on internal blog → collection links
`?utm_source=blog&utm_medium=internal&utm_campaign={article_id}` — makes article→catalogue flow
visible in Shopify Analytics without GA4.

**Only on blog → collection links.** Never on nav, never on collection → blog, never cross-domain.
Over-tagging pollutes the session data it is meant to clarify.

---

## 7. AI visibility panel

Same six prompts monthly, same engines, logged. Full prompt set in `../MEASUREMENT_PLAN.md` §5.

Per run, per prompt: mentioned Y/N · cited with a link Y/N · which URL · what claim was attributed.

Prompts 4 and 5 are non-local and non-branded — they test whether `cake-guides` earns retrieval on
knowledge alone, which is the one thing on-site content can prove by itself.

Automated LLM rank-tracking tools are not used. They are unreliable, and a manual panel of six
prompts is 30 minutes with a result you can actually inspect.

---

## 8. Review cadence

| Cadence | Review | Output |
|---|---|---|
| Weekly | WhatsApp tokens; publishing rate | 2 numbers |
| Monthly | `blog_audit.py` (orphans, refresh debt, tags); AI panel; GBP insights | append to `blog_kpis.csv` |
| Quarterly | GSC by silo; cannibalization sweep; per-pillar authority index | one page |
| Annually | Seasonal set refreshed in place; kill criteria re-checked | decision |

---

## 9. Kill criteria — live from Phase 3

From `../MEASUREMENT_PLAN.md` §7, restated because they are the point of measuring at all:

- **After 11 pillars + 6 months:** no growth in non-brand blog impressions **and** no AI panel
  citation → **stop cluster production.** Reinvest in the off-site entity track and collection
  enrichment, which return faster and cost less.
- **Any article outranking its hub collection** on a transactional query → fix anchors within
  30 days or de-optimise the article.
- **Refresh debt >20% for two consecutive months** → **halt new production** until it clears.

A programme without a stopping rule is a sunk cost with a content calendar.
