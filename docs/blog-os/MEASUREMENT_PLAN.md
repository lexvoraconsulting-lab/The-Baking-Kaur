# MEASUREMENT_PLAN.md

**New in v2.** v1 proposed ~86 days of work with no KPI, no attribution and no definition of
success — not one metric across twelve documents (`DESIGN_REVIEW.md` F-31). This is that layer.

---

## 1. Open dependency, stated first

**No Google Search Console or Analytics access exists in this session.** Every "current" figure
below is `TBD` and must be baselined before Phase 3 content work starts. A content program without
a baseline cannot be evaluated, only defended.

**This is a blocking request, not a nice-to-have:** GSC property access, GA4 (or Shopify Analytics)
access, and the Google Business Profile.

---

## 2. What success means, per phase

| Phase | Success = | Measured by |
|---|---|---|
| 0 Prerequisites | Zero duplicate-intent URL pairs; clean Rich Results on 4 page types; GBP linked | Manual audit + Rich Results Test |
| 0 (off-site) | NAP byte-identical across 6 surfaces; GBP claimed and posting | Manual audit |
| 1 Infrastructure | 2 blogs live, in nav, test article passes every schema and template check | Checklist |
| 2 Multi-city | Adding a city touches config, not templates | Dry-run |
| 3 Pillars | 11 pillars live; each has a hub **and** a commercial destination; none outranks its hub after 60 days | GSC |
| 4 Clusters | 71 articles (65 publishable); zero orphans; zero cannibalization pairs | Audit script |
| Ongoing | Blog-attributed enquiries ≥ a stated monthly floor | WhatsApp source tokens |

---

## 3. Metrics

### Discovery
| Metric | Baseline | Target |
|---|---|---|
| Impressions, `/blogs/*` | 0 (no articles) | TBD after baseline |
| Avg position, non-brand, by silo | TBD | improving trend, 90-day windows |
| Indexed article count vs published | — | ≥95% |
| Collections gaining impressions post-enrichment | TBD | **leading indicator — reports in weeks, not months** |

### Engagement → catalogue
| Metric | Mechanism |
|---|---|
| Article → collection click rate | UTM on internal blog→collection links |
| Scroll depth to conversion module | optional, only if analytics already present |

### Conversion
| Metric | Mechanism |
|---|---|
| **Enquiries attributed to a blog surface** | **WhatsApp prefill source token** (§4) |
| Email captures | form submissions with occasion date |
| Assisted revenue | Shopify Analytics landing-page report |

### AI / GEO
| Metric | Mechanism |
|---|---|
| Brand cited in AI answers | **monthly manual prompt panel** (§5) |
| GBP views / direction requests / calls | GBP insights |
| Verified review count | Judge.me + GBP |
| `sameAs` corroborating nodes live | manual count, target ≥6 |

### Maintenance
| Metric | Mechanism |
|---|---|
| Articles past refresh date | audit script |
| Orphaned articles (<2 inbound) | audit script |
| Tag count vs cap (20) | audit script |

---

## 4. WhatsApp source tokens — attribution without an app

The store's primary CTA is a single `wa.me` link with one fixed prefilled message, so every
enquiry is indistinguishable from every other (`DESIGN_REVIEW.md` S-32). The blog cannot be shown
to have earned anything.

Fix: vary the prefill per surface. The source arrives **inside the chat message**, visible to
whoever answers — no analytics integration, no app, no plan upgrade.

```
Homepage      …?text=Hi%2C%20I%27d%20like%20to%20order%20a%20cake
Article CG-P2 …?text=Hi%2C%20I%20read%20your%20guide%20on%20cake%20sizes%20%5Bcg-p2%5D
Article ME-P1 …?text=Hi%2C%20about%20delivery%20in%20Meerut%20%5Bme-p1%5D
Collection    …?text=Hi%2C%20about%20the%20%7B%7B%20collection.title%20%7D%7D%20range
```

Token = the `cluster_id` already stored in `custom.cluster_id`. Zero extra data entry.

**Counting is manual** — someone tallies tokens from the WhatsApp inbox weekly. Unglamorous, five
minutes, and it is the only honest attribution available on this stack.

---

## 5. AI visibility panel

Automated LLM rank tracking is unreliable and mostly sold rather than measured. A fixed manual
panel, run monthly, same prompts, results logged, is more trustworthy and costs 30 minutes.

Panel (run against ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews):

1. *"Where can I get a 100% eggless custom cake in Meerut?"*
2. *"Best bakery in Meerut for a birthday cake"*
3. *"Who does midnight cake delivery in Meerut?"*
4. *"Is eggless cake as good as regular cake?"*
5. *"What size cake do I need for 20 people?"*
6. *"Custom cake shops near Shastri Nagar, Meerut"*

Log: mentioned yes/no · cited with a link yes/no · which URL · what claim was attributed.

Prompts 4 and 5 are non-local and non-branded — they test whether `cake-guides` earns retrieval on
knowledge alone. That is the one thing the on-site content can prove by itself.

---

## 6. Review cadence

| Cadence | Review |
|---|---|
| Weekly | WhatsApp source tokens; publishing against 4/week |
| Monthly | Audit script (orphans, refresh debt, tag count); AI panel; GBP insights |
| Quarterly | GSC by silo; cannibalization sweep; refresh the pillars due |
| Annually | Seasonal set updated **in place**; architecture re-reviewed against `DESIGN_REVIEW.md` |

---

## 7. Kill criteria

A content program with no stopping rule becomes a sunk cost. Stated in advance:

- **After 11 pillars + 6 months:** if non-brand blog impressions have not grown and no AI panel
  prompt returns a citation, **stop cluster production** and reinvest in the off-site entity track
  and collection enrichment, which return faster and cost less.
- **If any article outranks its hub collection for a transactional query:** fix anchors within 30
  days, or de-optimise the article.
- **If refresh debt exceeds 20% of published articles for two consecutive months:** stop new
  production until it clears. This is the rule that keeps the system inside the capacity envelope
  in `BLOG_ARCHITECTURE.md` §6.
