# BLOG_OS_ROADMAP.md

**v2.1 — LOCKED.** Re-sequenced after `DESIGN_REVIEW.md`; pillar count and ordering updated after
`COMPLETION_AUDIT.md` (11 pillars, CG-P1 promoted to first on 66% catalogue share). Key changes
from v1: an off-site track added (F-21), effort estimates made credible (S-17), the launch set cut
from 97 to 71 (F-16), and fast-returning work moved ahead of slow-returning work (S-24).

**Nothing here is authorised.** Phase 1 is read-only and ends at approval.

---

## Sequencing principle — fastest return first

v1 sequenced by dependency alone and put ~97 new articles — the slowest-returning asset on an
unknown-authority domain — ahead of everything. v2 orders by **time-to-return**:

| Work | Returns in |
|---|---|
| Schema repairs, GBP link, nav | **days–weeks** |
| Off-site entity track (GBP, directories, NAP) | **weeks** |
| Collection enrichment (pages that already rank) | **weeks** |
| New articles | **months** |

---

## Phase 0 — Prerequisites (~11 days) · **BLOCKING**

### 0.1 Structured-data repairs (1.5 d) — no client input, no dependencies

| Task | File |
|---|---|
| **Delete** the hardcoded `FAQPage` | `layout/theme.liquid:68` |
| Add Google Business Profile to `sameAs` | `snippets/bk-local-business.liquid` |
| Reconcile `Organization` + `Bakery` into one `@id` node | `bk-local-business` + `tbk-schema-website` |
| `dateModified` → `custom.last_reviewed`, fallback `updated_at` | `snippets/tbk-schema-article.liquid` |
| Add `Service` nodes (midnight, same-day, custom design, corporate) | `bk-local-business.liquid` |
| `noindex, follow` on tag pages incl. `+` combinations | blog templates |
| `robots.txt.liquid` — explicit **allow** for GPTBot, ClaudeBot, PerplexityBot, CCBot, Google-Extended | new |

Deploy per `CLAUDE.md`: pull-and-diff first, single-file push to theme `#151307485353`, verify with
`?preview_theme_id=` and a cache-buster.

### 0.2 Collection consolidation (3 d) — data only, no deploy

**Mandatory pre-step (new in v2 — `DESIGN_REVIEW.md` M-09):** dump all 820 redirects and check
whether any already target the four handles about to be redirected. **Flatten, never chain.**

| Action |
|---|
| Keep `/collections/cakes` as the single `TYPE~Cake` canonical (985) |
| Retire `cake-delivery-meerut`, `midnight-cake-delivery`, `midnight-cake-delivery-meerut`, `same-day-cake-delivery-meerut` → 301 to `/collections/cakes`; delivery *intent* moves to the pages layer |
| Fix or retire `best-selling-products` + `newest-products` (self-cancelling rules returning all 1,235 incl. 588 drafts) |
| Rename/repair `showstopper-wedding-cake` — handle, title, rule and SEO currently describe four different things |
| Replace `wedding-cakes` rule `TITLE contains "wed"` → `TYPE = Wedding Cake` |
| Resolve `flowers-cake-combos` (1 product) and `for-her` (1 product): stock or `noindex` |

⚠ Four 301s on live URLs. Audit printed QR codes, paid-ad destinations and GSC top pages first —
the same discipline `CLAUDE.md` applies to handle optimization.

### 0.3 Page consolidation (2 d)

Merge `delivery-information` + `midnight-surprise-delivery` drafts into the two live delivery
pages, then delete · publish `freshness-guarantee` and `corporate-gifting-solutions` · fold
`why-choose-the-baking-kaur` into `/pages/about-us` · convert `cake-customization-guide` into
pillar `CG-P1` · retire `/pages/theme-cakes` → `/collections/designer-theme-cakes` · consolidate
the hamper page family behind `/pages/gift-hampers` · delete the duplicate refund policy ·
delete `theme-cake-1`, `rewind-menu-backup-page` · fill the four empty published page bodies.

### 0.4 Navigation repair (1 d)

Fill `explore-cakes`, `meerut-delivery`, `quick-links` per `INTERNAL_LINKING_BLUEPRINT.md` §7. Add
the blog to `main-menu`. Resolve the two contact destinations.

### 0.5 FAQ activation (2 d)

Editorial pass over the 43 `shopify--qa-pair` metaobjects (fix `"he Baking Kaur"`, the lowercase
starts, the truncated answer). Render on `/pages/frequently-asked-questions-faqs`. Emit **one**
`FAQPage` there — labelled low-expected-value, since FAQ rich results are unavailable to
commercial sites (`DESIGN_REVIEW.md` F-01). The same corpus seeds **GBP Q&A** in Phase 0.6, which
is where it will actually earn. Delete the empty `weights` / `weightr` definitions.

### 0.6 Off-site entity track (1.5 d + ongoing) — **new in v2**

| Task |
|---|
| Claim/verify **Google Business Profile**; NAP byte-identical to the `Bakery` schema |
| Seed GBP Q&A from the 43 metaobjects; add products; add real photos |
| NAP consistency: Zomato, Swiggy, JustDial, Magicpin, Instagram bio |
| List on Meerut wedding directories (WedMeGood, ShaadiSaga) |
| Collect ≥6 corroborating `sameAs` URLs → feed back into 0.1 |

**This is the highest-return work in the entire roadmap and v1 did not contain it.** For a local
business, LLM answer engines cite what third parties corroborate — not what the site says about
itself (`DESIGN_REVIEW.md` F-21).

> **Gate 0 →** No two live URLs answer one query. No `FAQPage` outside `/pages/faqs`. GBP claimed
> and in `sameAs`. ≥6 corroborating nodes, NAP-identical. Zero orphaned published pages. Rich
> Results clean on homepage / product / collection / page.

---

## Phase 1 — Collection enrichment + infrastructure (~7 days)

**Enrichment runs first** — it improves pages that already rank and reports in weeks.

### 1.1 Enrich 35 collection descriptions (4 d) — data only, no deploy
150–350 words of buying context each, ≤4 links (1 up, 1–2 sibling, 1 to a guide where one exists).
This is what replaced v1's 450-article `cake-ideas` silo.

### 1.2 Blog infrastructure (3 d)

| Task |
|---|
| Create blogs `cake-guides`, `meerut` |
| Create the **5** article metafield definitions |
| Create the `blog-categories` link list |
| Rebind sidebars off `blog-default` / `list` |
| Remove the comments block from `article.json` |
| **One** `article.json` branching on `blog.handle`; two index templates via `Blog.templateSuffix` |
| New `tbk-schema-blog.liquid`; add `about`/`mentions` to the article schema |
| Seed the 20 tags |
| **Write the orphan/refresh audit script** (`INTERNAL_LINKING_BLUEPRINT.md` §9) — a deliverable, not an aside |
| Verify `social-meta-tags` emits `og:type=article`; verify articles appear in theme search |
| Baseline GSC + Analytics (`MEASUREMENT_PLAN.md` §1) |

> **Gate 1 →** Both blogs live and in nav. One test article per silo passes: schema clean, exactly
> one `FAQPage` sitewide, tag page `noindex`, breadcrumb correct, `dateModified` from
> `last_reviewed`, `about`/`mentions` resolving. Audit script runs. Baseline captured.

---

## Phase 2 — Multi-city readiness (2 d) · **before city one**

Convert `areaServed`, delivery radius, minimum order, locality list and phone from literals to
metafields. Two days now; a re-platforming job after 90 Meerut articles.

> **Gate 2 →** Adding a city touches configuration, not templates.

---

## Phase 3 — Pillars (11 articles, ~5 weeks)

Order by catalogue share and blocker. **CG-P1 moves to the front in v2.1**: Theme Cake is
**400 of 602 active products — 66% of the catalogue.**

1. **CG-P1** — custom & theme cake ordering. Largest share of the catalogue by far.
2. **CG-P5** (100% eggless) — strongest differentiating asset, zero dependencies.
3. **CG-P2, CG-P3, CG-P4** — sizing, flavour, cost. Genuine white space, nothing blocked.
4. **CG-P8** — anniversary (83 active, #2 type). *(new in v2.1)*
5. **CG-P7** — wedding & event (68 active, #3 type). *(new in v2.1)* Conditional on Phase 0
   reconciling the two wedding collections.
6. **CG-P6** — keeping & craft (CG-6h held for photography).
7. **ME-P2, ME-P3** — celebrating, festive calendar.
8. **ME-P1** — delivery. **Only after Gate 0** clears the 8-URL delivery collision.

> **Gate 3 →** 11 pillars live. Each carries **both** a hub and a commercial destination. **No
> pillar outranks its hub after 60 days** — measured, not assumed.

---

## Phase 4 — Clusters (60 articles, ~15 weeks)

At **4 articles/week** — the honest sustained rate for 900–1,600 words with real research. v1's
2.1/day was not credible (`DESIGN_REVIEW.md` S-17).

Ratio discipline: complete 4–8 clusters under a pillar before starting the next pillar.

**Locality articles (ME-1c–1f) publish only with real delivery-window and fee data.** Without it
they are doorway pages and are held indefinitely. No exceptions under volume pressure.

Seasonal pieces are **calendar-anchored**: live 6–8 weeks before their peak, not when the
day-count reaches them.

> **Gate 4 →** 71 articles (65 publishable; 6 held on photography, delivery data and inventory).
> Zero orphans (≥2 inbound each, tag pages not counted). Zero cannibalization pairs. ≤20 tags.
> Every article carries a hub **and** a commercial destination. Refresh debt under 20%.

---

## Phase 5 — GEO & trust · **client-blocked**

| Task | Blocker |
|---|---|
| `Person` entity + `/pages/authors/{slug}` + retro-byline every article | author identity |
| FSSAI number → `hasCredential` | licence number |
| Judge.me activation; first 3 verified reviews | client |
| Studio photography → CG-6h, collection imagery, Pinterest | one shoot |
| Pinterest: 2:3 assets, Rich Pins, boards — **pointed at products/collections, not articles** | photography |

**Nothing here may be simulated.** No persona, no placeholder licence, no sample review.

> **Gate 5 →** Every article resolves to a named `Person`. `Bakery` carries a real credential. Any
> rating shown is computed from real reviews.

---

## Phase 6 — Maintenance (ongoing)

| Cadence | Task |
|---|---|
| Weekly | WhatsApp source tokens; publishing rate |
| Monthly | Audit script; AI visibility panel; GBP insights |
| Quarterly | GSC by silo; cannibalization sweep; pillar refreshes |
| Annually | Seasonal set updated **in place**; re-run `DESIGN_REVIEW.md` against the architecture |

**Kill criteria are live from Phase 3** (`MEASUREMENT_PLAN.md` §7).

---

## Timeline

| Phase | Duration | Depends on |
|---|---|---|
| 0 Prerequisites | 11 d | — |
| 1 Enrichment + infrastructure | 7 d | Gate 0 |
| 2 Multi-city | 2 d | Gate 1 |
| 3 Pillars | ~5 wks | Gate 2 |
| 4 Clusters | ~15 wks | Gate 3 |
| 5 GEO/trust | 3 d | **client** |
| **Total to Gate 4** | **~24 weeks** | |

v1 claimed ~86 days for a larger scope at an impossible writing rate. v2 is a smaller scope at a
sustainable one.

**Phase 0.1 + 0.6 — 3 days, no client input, highest return in the document — are worth
authorising on their own** regardless of what happens to the rest.

---

## Interaction with the existing roadmap

`CLAUDE.md` holds a separate build track (Phase A validated-not-promoted, then B → C → E). One
shared file: **`layout/theme.liquid`**.

- Phase 0.1 touches `theme.liquid` (FAQPage deletion, robots, Service nodes) — coordinate with the
  Phase A promotion so the two do not race on the live theme.
- Phase 0.4 navigation overlaps the homepage/navigation track (C → E). Do it once.
- Blog OS Phase 0 is almost entirely **data and schema**, matching the `CLAUDE.md` principle:
  *data fixes before theme work — reversible, no deploy, faster to Google.*

Recommended interleave: **Blog OS 0.1 + 0.6 first** (3 days, near-zero risk, highest return), then
promote Phase A, then Blog OS 0.2–0.5.
