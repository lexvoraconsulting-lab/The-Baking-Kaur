# CONTENT_GAP_ANALYSIS.md — Gaps, priority, impact

**v2.0.** Re-graded after `DESIGN_REVIEW.md`. Changes: four gaps added that v1 did not see
(off-site corroboration, AI-crawler posture, entity disambiguation, measurement), `speakable`
removed as an error, and email capture promoted Low → High.

Current website vs. the architecture in `BLOG_ARCHITECTURE.md` v2.
Effort is in working days for one operator with Admin API + theme access.

Impact scales: **Business** (revenue proximity) · **SEO** (organic search) · **GEO** (AI answer
engines) — each High / Med / Low.

---

## CRITICAL — blocks everything downstream

| # | Gap | Business | SEO | GEO | Effort |
|---|---|---|---|---|---|
| C1 | **5 collections resolve from the identical rule `TYPE CONTAINS "Cake"` to the identical 985 products** (`cakes`, `cake-delivery-meerut`, `midnight-cake-delivery`, `midnight-cake-delivery-meerut`, `same-day-cake-delivery-meerut`) | High | **High** | Med | 2 |
| C2 | **Site-wide hardcoded `FAQPage` in `theme.liquid:68`**, in `<head>`, on 1,300+ URLs | Low | **High** | **High** | 0.5 |
| C3 | **Delivery intent spread across 8+ URLs**; hamper intent across 6; theme-cake across 3 | High | **High** | Med | 3 |
| C4 | **No author `Person` entity anywhere on the site**; `Article.author` = `Organization` | Med | Med | **High** | 1 *(+client)* |
| C5 | **`best-selling-products` and `newest-products` carry self-cancelling rules** and return all 1,235 products including 588 drafts | Med | **High** | Low | 0.5 |
| C6 | **Blog is orphaned from all navigation**; no menu links `/blogs/*` | High | **High** | Med | 0.5 |
| **C7** | **No off-site corroboration.** GBP unclaimed in schema; no Zomato/Swiggy/JustDial/directory NAP consistency. For a local business this is where AI citation actually comes from | **High** | **High** | **High** | 1.5 |
| **C8** | **No measurement layer at all** — no KPI, no attribution, no baseline. The primary CTA is one fixed `wa.me` link, so every enquiry is indistinguishable | **High** | Med | Low | 1 |

**C1/C3 are the gate.** Publishing ME-P1, CI-P5 or CI-P2 into the current URL set adds
competitors to an already-split query. Sequenced as Phase 0 in `BLOG_OS_ROADMAP.md`.

**C2 detail.** The block declares the same six-plus questions on the homepage, every product,
every collection and every future article. Two failure modes: Google sees one FAQ set claimed by
1,300 URLs (structured-data spam exposure), and every article that emits its own correct
`FAQPage` emits a second one on the same URL. Deleting it is half a day and unblocks the entire
GEO track.

---

## HIGH

| # | Gap | Business | SEO | GEO | Effort |
|---|---|---|---|---|---|
| H1 | **Zero educational content.** The only teaching on the site is two boilerplate Q&As repeated on 602 products | Med | **High** | **High** | 15 |
| H2 | **43 Q&A metaobjects rendered nowhere**, while the FAQ page body is empty | Med | **High** | **High** | 2 |
| H3 | **Google Business Profile absent from `sameAs`** — the primary local entity link | **High** | **High** | **High** | 0.25 |
| H4 | **`dateModified` = `published_at`** — freshness signal permanently wrong | Low | **High** | Med | 0.25 |
| H5 | **No locality landing targets.** Meerut localities are named inside one collection description and nowhere else; `meerut-delivery` menu is empty | **High** | **High** | Med | 6 |
| H6 | **Ten published pages orphaned from navigation**, incl. `100-percent-eggless-bakery` — the brand's strongest differentiator | **High** | **High** | Med | 1 |
| H7 | **Zero internal links in 1,235 product descriptions** | Med | **High** | Low | 3 |
| H8 | **No pillar content of any kind.** 17 pillars planned, 0 exist | **High** | **High** | **High** | 25 |
| H9 | **Two unreconciled org-class schema nodes** (`Organization` with `@id` + IG; `Bakery` no `@id` + IG/FB) | Low | Med | **High** | 0.5 |
| H10 | **0 verified reviews.** Judge.me installed, returning `0` on every product; 1 `testimonial` metaobject | **High** | Med | **High** | *client* |
| H11 | **FSSAI "approved" claimed with no licence number** | Med | Low | **High** | 0.25 *(+client)* |
| H12 | **Blog templates bound to three non-existent handles** (`blog-categories`, `blog-default`, `list`) + a comments block against a comments-CLOSED blog | Low | Med | Low | 0.5 |
| **H13** | **Thin collection descriptions on ~20 occasion/format/theme collections** — the pages that should own inspiration intent | **High** | **High** | Med | 4 |
| **H14** | **AI-crawler posture is an accident, not a decision.** No `robots.txt.liquid`; GPTBot/ClaudeBot/PerplexityBot/Google-Extended access undeclared | Low | Low | **High** | 0.25 |
| **H15** | **Entity disambiguation.** "Kaur" is a near-universal name; 2 `sameAs` links cannot resolve this business against many similarly-named home bakeries | Med | Med | **High** | *(in C7)* |
| **H16** | **No email capture.** On a domain whose SEO payoff is months away, an owned list — with occasion dates, for a celebration business — is the only near-term return the blog can produce | **High** | Low | Low | 1 |

**H1 is the largest pure-upside item in the audit.** The expertise exists in the studio; it is
unwritten, not unknown. Nothing about it is blocked.

**H3 is the highest impact-per-hour item in the entire document** — one URL added to one array.

---

## MEDIUM

| # | Gap | Business | SEO | GEO | Effort |
|---|---|---|---|---|---|
| M1 | Four published pages with empty bodies (`contact`, `store-locator`, `frequently-asked-questions-faqs`, `terms-and-conditions`) | Med | Med | Low | 2 |
| M2 | Six finished-title empty drafts occupying blog intent — resolved on paper in `BLOG_ARCHITECTURE.md` §4, not yet executed | Low | Med | Low | 2 |
| M3 | `showstopper-wedding-cake`: handle, title, rule and SEO copy describe four different things | Med | Med | Low | 0.5 |
| M4 | `wedding-cakes` matches the substring **`wed`** — set is untrustworthy | Med | Med | Low | 0.5 |
| M5 | `flowers-cake-combos` (1 product) and `for-her` (1 product) are indexable with full SEO metadata and no inventory | Med | Med | Low | 1 |
| M6 | Identical two-Q&A boilerplate on ~602 product descriptions | Low | Med | Med | 2 |
| M7 | Feed category mismatch: `mm-google-shopping` 2194 vs `mc-facebook` 8271 on the same product | Med | Low | Low | 1 |
| M8 | Three empty menus (`explore-cakes`, `quick-links`, `meerut-delivery`) | Med | Med | Low | 0.5 |
| M9 | Two contact destinations (`/pages/contact` vs `/policies/contact-information`) | Low | Low | Low | 0.25 |
| M10 | Duplicate refund policy (`refund-return-policy` live + `return-refund-replacement-policy` draft) | Low | Med | Low | 0.25 |
| M11 | No `Blog` / `ItemList` schema on blog index | Low | Med | Med | 0.5 |
| M12 | Tag pages will be indexable by default; no custom `robots.txt.liquid` | Low | **High** | Low | 0.5 |
| M13 | Product tags: 18 uncontrolled strings, inconsistent casing and plurality | Low | Low | Low | 1 |
| M14 | Empty duplicate metaobject definitions `weights`, `weightr` (0 entries each) | Low | Low | Low | 0.25 |
| M15 | Shop meta description opens *"the best bakery and cake shop in Meerut"* — unverifiable superlative in store metadata | Low | Low | Med | 0.25 |

**M12 is cheap and time-sensitive:** 52 tags × 4 blogs = up to 208 auto-generated thin pages.
Setting `noindex, follow` *before* the first article is trivial; after 200 are indexed it is a
recovery project.

---

## LOW

| # | Gap | Effort |
|---|---|---|
| ~~L1~~ | ~~No `speakable` markup~~ — **removed, was an error.** `speakable` is Google-News-only and does not apply (`DESIGN_REVIEW.md` F-03) | — |
| ~~L2~~ | ~~No `HowTo` schema~~ — **removed, was an error.** `HowTo` rich results are deprecated (`DESIGN_REVIEW.md` F-02) | — |
| L3 | Blog comments disabled — fine, but the UI block still ships | *(in H12)* |
| ~~L4~~ | ~~No newsletter capture~~ — **promoted to H16** | — |
| L5 | No related-collection module on article template | 1 |
| L6 | `rewind-menu-backup-page` and `theme-cake-1` are dead pages | 0.25 |
| L7 | No `ItemList` on collection pages | 0.5 |
| L8 | No `Service` entities — 4 real services modelled as one stub `makesOffer` | 0.5 |
| L9 | Pinterest unused — and when used, should point at **products/collections**, not articles | *(gated on photography)* |

---

## Client-blocked — do not build placeholders

Consistent with the standing rule in `CLAUDE.md`.

| Blocker | Needed | Unblocks |
|---|---|---|
| **Author identity** | Name, title, photo, bio, one external profile URL | C4, the entire E-E-A-T layer, every article byline, `EK-P4` |
| **Verified reviews** | 3+ real reviews (Judge.me is installed; transcribing GBP reviews with `source_url` is the fast path) | H10, any `aggregateRating`, S5 Social Proof |
| **FSSAI licence number** | The number | H11, S8 Trust |
| **Photography** | One studio shoot | `EK-P4` studio pillar, `cake-ideas` galleries, hero |
| **Google Business Profile URL** | The canonical GBP link | H3 — *most likely already obtainable without the client* |

**Under no circumstance** should an author persona, a review, or a licence number be invented to
unblock a deliverable. Three removals have already resulted from this rule.

---

## Prioritised sequence — ordered by time-to-return, not by dependency alone

1. **C2, C5, H3, H4, H14, M12, L8** — ~2 days, no client input, all pure gain. Returns in weeks.
2. **C7, H15** — off-site entity track: GBP, directories, NAP. ~1.5 days. **Highest return in the
   document, and v1 did not contain it.**
3. **C1, C3, M3, M4** — consolidation. The gate. ~6 days.
4. **C6, H6, M8** — navigation and orphan repair. ~1 day.
5. **H13** — enrich 35 collection descriptions. ~4 days, no deploy. Improves pages that
   **already rank**; this replaced v1's 450-article ideas silo.
6. **H2, M1** — wire the 43 Q&A metaobjects into the FAQ page *and* into GBP Q&A. ~2 days.
7. **H12, C8, H16** — blog infrastructure, measurement layer, email capture. ~3 days.
8. **H8, H1, H5** — write. 71 articles, ~18 weeks at a sustainable 4/week.
9. **C4, H10, H11** — as the client unblocks.

Steps 1–2 total **3.5 days, need no client input, and return faster than anything else here.**
They are worth authorising independently of the rest.

Full sequencing with gates: `BLOG_OS_ROADMAP.md`.
