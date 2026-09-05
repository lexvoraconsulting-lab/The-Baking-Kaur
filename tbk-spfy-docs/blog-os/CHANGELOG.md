# CHANGELOG.md â€” Blog OS

---

## [2.1.0] â€” 2026-07-24 â€” ðŸ”’ **ARCHITECTURE LOCKED**

### Store changes
**None.** Still read-only.

### Gate run
The 15 completion conditions were run as a gate, not a formality.
**Pass 1: 9 pass, 4 fail, 2 partial.** Fixes applied. **Pass 2: 15/15. Locked.**

### New evidence â€” verified product counts

Active-product counts by type were verified for the first time. They contradicted assumptions
carried through v1 and v2.

| Finding | Impact |
|---|---|
| **602 active, not 651** (588 draft, 45 archived) | Corrected in 8 documents |
| **Theme Cake = 400 (66% of catalogue)** | CG-P1 promoted to highest-priority pillar, +3 clusters |
| **Anniversary 83, Wedding 68 â€” no pillar** | CG-P7, CG-P8 added: 151 active products had no coverage |
| **Gift/Festive Hamper = 0 active** | Hamper pillar **withheld** â€” blocked on inventory, not photography |
| **Bento Cake = 0 active** | CG-2d held |

### Failures fixed

| Condition | Failure | Fix |
|---|---|---|
| 5 Â· commercial destination | 5 pillars had a page hub and no commercial destination; ME-P2 pointed only at About Us | Hub and commercial destination are now separate required fields |
| 6 Â· collection support | 26 of 35 collections had no designated supporting content | `COLLECTION_CONTENT_MAP.md` â€” all 35, with retire/repair verdicts where support is not the answer |
| 7 Â· product support | 151 active products across the #2 and #3 types had no pillar | CG-P7 + CG-P8; 100% of active products now covered by type |
| 13 Â· editorial standards | Fragments across three files; nothing on verification, images or sign-off | `EDITORIAL_STANDARDS.md` |
| 14 Â· templates | Named but not specified | `TEMPLATE_SPEC.md` |
| 3 & 4 Â· duplicate intent | Architecture clean, store not | Locked as âœ… architecture / â›” pending Phase 0 (D-039) |

### Added
`COMPLETION_AUDIT.md` Â· `COLLECTION_CONTENT_MAP.md` Â· `EDITORIAL_STANDARDS.md` Â· `TEMPLATE_SPEC.md`

### Updated
`BLOG_ARCHITECTURE.md` (lock header, Â§8 hub/destination) Â· `TOPIC_CLUSTER_MAP.md` (11 pillars,
76 launch) Â· `BLOG_OS_ROADMAP.md` (re-sequenced, ~25 weeks) Â· `DECISION_LOG.md` (D-033â€¦D-039) Â·
plus the 602/588/45 correction across `CURRENT_STATE.md`, `BLOG_AUDIT.md`,
`CONTENT_GAP_ANALYSIS.md`, `DESIGN_REVIEW.md`, `ENTITY_RELATIONSHIP_MAP.md`,
`FINAL_PHASE1_REPORT.md`.

### Numbers

| | v2.0 | v2.1 |
|---|---:|---:|
| Pillars | 9 | **11** |
| Launch articles | 62 | **71** (65 publishable, 6 held) |
| Timeline to Gate 4 | ~21 wks | **~24 wks** |
| Ceiling | ~250 | ~250 (unchanged) |

### Scores

| Score | Value |
|---|---|
| Store State | **33 / 100** â€” unchanged; moves only when Phase 0 executes |
| Design Quality | **93 / 100** â€” unchanged; v2.1 closed completeness gaps, not design defects |

**Status: architecture locked. Next action is implementation, not design.**

---

## [2.0.0] â€” 2026-07-24 â€” Adversarial design review and redesign

### Store changes
**None.** Still read-only. No product, collection, page, blog, menu, redirect, metafield,
metaobject or theme file was created, modified or deleted.

### Added
- `DESIGN_REVIEW.md` â€” 42 findings (6 fatal, 12 serious) against v1, the redesign, and a
  **Design Quality Score** rubric.
- `MEASUREMENT_PLAN.md` â€” KPIs, UTM convention, WhatsApp source tokens, AI-visibility panel,
  kill criteria. v1 had no measurement of any kind.

### Rewritten to v2
`BLOG_ARCHITECTURE.md` Â· `BLOG_TAXONOMY.md` Â· `TOPIC_CLUSTER_MAP.md` Â·
`INTERNAL_LINKING_BLUEPRINT.md` Â· `BLOG_OS_ROADMAP.md` Â· `FINAL_PHASE1_REPORT.md`

### Updated
`ENTITY_RELATIONSHIP_MAP.md` (Â§2â€“Â§6) Â· `CONTENT_GAP_ANALYSIS.md` (C7, C8, H13â€“H16 added;
L1/L2 removed as errors; L4 promoted) Â· `DECISION_LOG.md` (D-016â€¦D-032, five reversals) Â·
`BLOG_AUDIT.md` (scoring-scope note)

### Unchanged
`CURRENT_STATE.md` â€” an observation of the store, not a design artifact. Nothing in the review
invalidated it.

### Corrections to v1 â€” errors of fact

| Error | Correction |
|---|---|
| Per-article `FAQPage` presented as an SEO deliverable | FAQ rich results have been unavailable to commercial sites since Aug 2023. Removed |
| `HowTo` content type built around `HowTo` schema | `HowTo` rich results are deprecated. Type deleted |
| `speakable` listed as an opportunity | Google-News-only. Removed |
| Per-silo article templates | `Article.templateSuffix` is per-article and not inherited from `Blog.templateSuffix`. One template, branching on `blog.handle` |
| `noindex, follow` tag pages "pass equity" | Long-term `noindex` is eventually treated as `nofollow`. No equity claim |
| Tag surface sized at 208 pages | Shopify also generates `/tagged/{a}+{b}` â€” combinatorial |
| Productâ†”blog loop "structurally impossible" | Impossible in HTML; available in schema via `Article.about`/`mentions` |
| Basic plan never considered | No Shopify Flow â†’ 12 required metafields Ã— 900 articles was unworkable. Cut to 5 |

### Redesign summary

| | v1 | v2 |
|---|---|---|
| Silos | 4 | **2** |
| Inspiration content | 450-article `cake-ideas` silo | **35 enriched collection descriptions** |
| Pillars / launch / ceiling | 17 / 97 / 920 | **9 / 62 / ~250** |
| Article templates | 4 suffixes | **1** |
| Required metafields | 12 | **5** |
| Tags | 52 | **20** |
| GEO | on-site only | **on-site + off-site entity track** |
| Measurement | none | **full plan** |
| Timeline to launch set | 46 days (not credible) | **~21 weeks** at 4 articles/week |

### Scores

| Score | Value | Note |
|---|---|---|
| **Store State** | **33 / 100** | Unchanged. Measures the live store; moves only when Phase 0 executes |
| **Design Quality** | **40 â†’ 93 / 100** | Measures the blueprint. Derivation in `DESIGN_REVIEW.md` |

---

Changes to **the Blog OS design documents**. The store's own changelog is the root
`CHANGELOG.md`; nothing in this phase touched the store.

---

## [1.0.0] â€” 2026-07-24 â€” Phase 1: Discovery & Content Architecture

### Store changes
**None.** Phase 1 was read-only, as specified. No product, collection, page, blog, menu, redirect,
metafield, metaobject or theme file was created, modified or deleted.

### Verification performed (read-only)

| Source | What was read |
|---|---|
| Admin GraphQL | `shop`, `blogs`, `pages` (3 pages of results), `collections` (2 pages, all 35), `products` (3 ACTIVE samples, full field set), `menus` (all 9), `productTypes`, `productTags`, `metaobjectDefinitions`, `metaobjects(shopify--qa-pair)` (25 of 43), `urlRedirectsCount` |
| Local theme | `layout/theme.liquid`, `templates/{blog,blog.list,article}.json`, `snippets/tbk-schema-{article,breadcrumb,website}.liquid`, `snippets/bk-local-business.liquid`, directory listings for `templates/`, `sections/`, `snippets/` |
| Repo | root `*.md` inventory, `docs/`, `tasks/` |

### Added â€” `docs/blog-os/`

| File | Contents |
|---|---|
| `CURRENT_STATE.md` | Verified inventory of blog, products, collections, pages, menus, schema, metaobjects |
| `BLOG_AUDIT.md` | 16 areas scored 1â€“10 with evidence; 34/100 composite |
| `BLOG_ARCHITECTURE.md` | Four-silo intent-based design; platform constraints; taxonomy, schema, multi-city, quality gates |
| `BLOG_TAXONOMY.md` | Silos, subcategories, 52-tag capped vocabulary, prohibited tags, 12 article metafields, naming rules |
| `TOPIC_CLUSTER_MAP.md` | 17 pillars, 97 launch articles, per-pillar cannibalization check |
| `CONTENT_GAP_ANALYSIS.md` | 6 Critical, 12 High, 15 Medium, 7 Low gaps with Business/SEO/GEO impact and effort |
| `ENTITY_RELATIONSHIP_MAP.md` | Current and target digital twin, knowledge graph, journey map, AI retrieval model |
| `INTERNAL_LINKING_BLUEPRINT.md` | Hub-and-spoke model, link budgets, anchor policy, nav changes, anti-patterns |
| `BLOG_OS_ROADMAP.md` | Phases 0â€“6 with exit gates, ~86 days to Gate 4 |
| `DECISION_LOG.md` | 15 decisions with rationale and rejected alternatives; 6 open client questions |
| `CHANGELOG.md` | This file |
| `FINAL_PHASE1_REPORT.md` | Executive summary, findings, scores, next phase |

### Key findings recorded

- The blog layer is **empty** (1 blog, 0 articles) â€” greenfield, not remediation.
- Five collections resolve from the identical smart rule to the identical 985 products.
- A hardcoded `FAQPage` ships in `<head>` on every URL of the store.
- 43 Q&A metaobjects exist and are rendered nowhere; the FAQ page body is empty.
- Ten published pages and the blog itself are orphaned from all navigation.
- No `Person`/author entity exists anywhere on the site.
- Three blog-template bindings point at handles that do not exist.
- The `<title>`/H1 mismatch on `motu-patlu-designer-birthday-cake-meerut` recorded in `CLAUDE.md`
  is **not present in the current API data** â€” the roadmap item may already be closed; re-verify
  the rendered page.

### Deferred to Phase 2+

Article writing Â· theme deployment Â· collection consolidation Â· redirects Â· schema repairs Â·
metaobject rendering Â· navigation changes Â· author entity Â· the orphan-audit script.

### Not done, and why

| Item | Reason |
|---|---|
| Rendered-HTML verification of live pages | Would require fetching the storefront; Phase 1 scope is the Admin API and local source |
| Google Search Console / Analytics data | Not connected to this session |
| Google Business Profile review inventory | Not accessible; needed for the reviews unblock |
| Remaining 18 of 43 Q&A metaobjects | 25 sampled; the quality pattern was consistent and the editorial pass is Phase 0.5 work |
| Full 1,235-product SEO sweep | 3 ACTIVE products sampled in full; catalogue-wide sweep is an existing `seo-ops/` task, not a Blog OS deliverable |

