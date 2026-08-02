# Enterprise Collection Architecture (Phase 7.9)

**Documentation only. No production changes.** No collection was created, merged, redirected,
deleted, or renamed; no handle changed; no navigation touched. This designs the permanent target
architecture and how to get there safely — it stops at documentation and waits for approval before
any implementation phase begins.

**Historical audits are evidence, not constraints.** `docs/COLLECTION_STRATEGY_EVIDENCE_REPORT.md`
(Phase 7.8) catalogued four prior, mutually contradictory collection audits (2026-07-16 through
07-30) and reconciled them against live data. This document doesn't re-litigate that reconciliation
— it starts fresh from the current live store (36 collections, 1,235 products, re-queried
2026-08-01) and from the business facts established across this entire engagement (100% eggless,
Meerut-only delivery, no reviews, no GTIN/MPN, password-gated site, Merchant Center submitting 0
products today). Where a historical proposal happens to match what this design independently
arrives at, that's noted as corroboration, not inherited authority.

---

## Part 1 — Enterprise Collection Architecture

### 1. The taxonomy: three axes, not a flat list

The store's own product data already implies three independent axes — this isn't invented, it's
recovered from the 36 collections that exist today and the product-type values already in use
(`Birthday Cake`, `Anniversary Cake`, `Wedding Cake`, `Designer Cake`, `Theme Cake`, plus hamper and
photo lines):

| Axis | Role | Example values | Cardinality today |
|---|---|---|---|
| **Occasion** | Primary — what the purchase is *for* | Birthday, Anniversary, Wedding, Baby Shower/Gender Reveal, Corporate/Achievement, Festival (Diwali), Gifting/Hampers | 6-8 |
| **Theme/Character** | Secondary — what the design *looks like* | Unicorn, Motu Patlu, Cricket, K-Pop, Jungle Animal, Teddy, Butterfly, Chartered Accountant, Roblox, PAW Patrol, Bow/Ribbon, Baby Girl, Gender Reveal | 13+ today, unbounded over time |
| **Flavor** | Tertiary — what it *tastes like* | Chocolate, Vanilla, Red Velvet, Strawberry, Butterscotch, Lotus Biscoff, Fruit Cocktail, Chocolate Mousse | ~9, filter-only, never a collection (already correctly ratified — see §5) |

A 4th, thinner axis — **Recipient** (For Him, For Her) — exists today at 11 and 1 products
respectively. At this volume it's a filter value on the Occasion axis, not an independent
collection tier (see §5).

**Why this axis set, not a different one**: it matches how the business itself already organizes —
occasion collections are what's actually wired into live navigation and carry the real SEO
title/description work already done catalogue-wide (Phase 7.2/7.4); themes are what the 13
character-based collections already represent, just not integrated with occasion; flavor is
already a variant/tag dimension, never a collection, in the live data. This design formalizes what's
half-built, rather than replacing it.

### 2. Permanent collection hierarchy

```
Cakes (root, non-canonical index — see §16)
├── Birthday Cakes                      [PRIMARY, occasion]
├── Anniversary Cakes                   [PRIMARY, occasion]
├── Wedding Cakes                       [PRIMARY, occasion]
├── Baby Shower & Gender Reveal Cakes   [PRIMARY, occasion — new, consolidates Baby Girl + boy-or-girl-cake]
├── Corporate & Achievement Cakes       [PRIMARY, occasion — new, consolidates Chartered Accountant + future corporate lines]
├── Designer & Custom Cakes             [PRIMARY, occasion — consolidates today's Designer & Theme Cakes + Custom Cakes Meerut cluster]
├── Photo Cakes                         [PRIMARY, occasion/format hybrid — kept as today, real distinct format]
├── Festival Hampers                    [PRIMARY, gifting — Diwali today, extensible to future festivals]
└── Cake Hampers & Gifting              [PRIMARY, gifting — hampers, flowers & cake combos]

Theme collections (SECONDARY tier — cross-linked from occasion, not siblings of it)
├── Unicorn, Motu Patlu, Cricket, K-Pop, Jungle Animal, Teddy, Butterfly,
│   Roblox, PAW Patrol, Bow/Ribbon, Winter Strawberry [seasonal]
└── (unbounded — new themes join this tier automatically, see §17)

Utility / non-curating (own tier — never conflated with the two above)
├── Best Selling Products   [needs a real rule — see Part 4]
└── Newest Products         [needs a real rule — see Part 4]
```

This is a **two-tier hierarchy with cross-links**, not a deep tree: Occasion collections are the
primary navigable structure (this is what "hierarchy" should mean in Shopify's flat collection
model); Theme collections are a second, cross-cutting tier that every occasion collection links to
and can be filtered by. Shopify collections cannot literally nest (confirmed during Phase 7.8 — no
native parent/child relationship exists on the platform), so "hierarchy" here is implemented via
consistent internal linking + faceted filtering, not URL nesting. See §3.

### 3. Parent/child relationships (as data, not as URLs)

Shopify has no native collection nesting, so "parent/child" is modeled two ways simultaneously,
matching how the platform actually supports it:

1. **Metafield-declared relationship** — each Theme collection carries a
   `custom.parent_occasion` reference metafield pointing at its primary Occasion collection(s) (a
   theme can belong to more than one occasion — e.g. Unicorn spans Birthday and Baby Shower). This
   is queryable data, drives the "part of" breadcrumb (§7) and related-collections modules (§8),
   and costs nothing at read time.
2. **Faceted filter, not a separate URL, for high-volume overlap** — a customer browsing
   `/collections/birthday-cakes` can filter by theme (`?filter.p.tag=theme_unicorn`) without ever
   leaving the Birthday Cakes collection. The theme's own standalone collection page
   (`/collections/unicorn`) continues to exist in parallel for long-tail SEO capture ("unicorn cake
   Meerut" as its own query) — these are not either/or, they're the same product set exposed two
   ways for two different search intents, with canonicalization handling the overlap (§16).

Utility collections (Best Selling, Newest) have no parent — they're cross-cutting views over the
whole catalogue by definition and shouldn't be nested under any occasion.

### 4. Smart collection strategy

**Root cause of today's problems, restated as a design constraint**: every broken or duplicate rule
found in Phase 7.8 was a **title-substring or type-substring match** (`TITLE contains "wed"`, `TYPE
contains "Cake"`, a self-cancelling `contains X AND not-contains X` pair). Substring matching
against free-text fields is inherently fragile — it can't distinguish "Wedding Cake" from "Wednesday
Surprise Cake," and it can't express "belongs to exactly these occasions" cleanly. **The permanent
fix is structural, not a smarter substring pattern**: every smart collection should rule on
**controlled-vocabulary fields only** — `product_type` (exact match, from the fixed vocabulary in
§17) and **standardized tags** (`occasion:birthday`, `theme:unicorn`, `flavor:chocolate`,
`recipient:him`), never `TITLE contains`.

| Collection tier | Rule basis | Example |
|---|---|---|
| Occasion (primary) | `product_type = X` OR `tag = occasion:X` (products can carry a secondary occasion tag without changing their primary type) | `Birthday Cakes`: `product_type = "Birthday Cake"` |
| Theme (secondary) | `tag = theme:X` | `Unicorn`: `tag = "theme:unicorn"` |
| Utility | A real, non-tautological rule — e.g. `tag = "bestseller"` (a tag applied by a scheduled process reading actual order data, not by title text) for Best Selling; `sort: created_at DESC` with no filter rule at all (not a smart-collection *rule*, just a manual collection's sort order) for Newest | See Part 4 for the concrete repair |
| Gifting | `product_type = "Hamper"` or a dedicated `Cake Hamper` / `Gift Hamper` type | Cake Hampers |

**Why smart over manual for the primary tier**: this is the actual lever that satisfies "optimize
for the next 10,000 products" — a smart collection ruled on `product_type`/tags means every future
product joins the correct collection automatically at creation time, with zero manual
collection-membership work. Today's Occasion collections (Birthday, Anniversary, etc.) are
currently **manual** — every one of the ~2,000+ products added since launch had to be manually
added to a collection. That's the single highest-leverage change in this entire document.

### 5. Manual collection strategy

Manual collections are the right tool only for genuinely curated, non-rule-expressible sets:

- **Festival Hampers** (seasonal, hand-picked per festival — Diwali today, others later) — a human
  decides what's "this year's Diwali hamper," not a rule.
- **Homepage/campaign features** (if/when built) — hand-curated by definition.
- **Best Selling**, if the business prefers a merchandiser's judgment call over a data-driven tag
  (a legitimate choice — Part 4 covers both options).

Everything else should be smart. Manual collections are the thing that silently drifted out of
sync in this store already (today's Birthday/Anniversary/Wedding collections are manual, meaning
every product needed a human to remember to add it) — that's exactly the failure mode this
architecture is designed to close.

---

## Part 2 — Information Architecture Blueprint

### 6. Navigation hierarchy (target)

```
HOME  |  CAKES ▾  |  HAMPERS & GIFTING ▾  |  DELIVERY ▾  |  ABOUT US  |  CONTACT US
       │            │                      │
       │            ├─ Cake Hampers        ├─ Same-Day Delivery       (page)
       ├─ Birthday   ├─ Festival Hampers    ├─ Midnight Delivery       (page)
       ├─ Anniversary└─ Flowers & Cake Combo└─ Delivery in Meerut      (page)
       ├─ Wedding
       ├─ Baby Shower & Gender Reveal
       ├─ Corporate & Achievement
       ├─ Designer & Custom
       ├─ Photo Cakes
       └─ Shop by Theme ▸ (Unicorn, Motu Patlu, Cricket, ...)
```

This is a **direct, low-risk extension of what's already live and working** — the current
`main-menu`'s "Categories" dropdown already correctly lists 6 occasion collections (verified live in
Phase 7.8). The target adds the 3 missing occasion pillars (Baby Shower/Gender Reveal, Corporate,
Photo Cakes), a "Shop by Theme" sub-menu surfacing the 13 theme collections (today completely
absent from navigation — 0 of them are in any live menu), and a "Delivery" menu using the
`meerut-delivery` menu resource that Phase 7.8 confirmed already exists, already has real
page content, and is simply not wired to a visible section today.

**Customer Experience**: closes the biggest navigation gap found in this whole investigation — 30
of 36 collections are currently reachable by URL only, not by browsing. **SEO**: every newly-linked
collection gains a crawlable, discoverable internal link (currently 0 for the theme tier).
**Risk**: none to existing traffic — this only *adds* menu items, doesn't remove or redirect
anything. **Rollback**: revert the menu item additions; zero data impact.

### 7. Breadcrumb architecture

```
Home / Cakes / Birthday Cakes / Unicorn Birthday Cake (product)
Home / Cakes / Birthday Cakes / Unicorn (theme collection, when reached via the theme path)
Home / Hampers & Gifting / Cake Hampers
```

Breadcrumb parent is resolved via the same `custom.parent_occasion` metafield relationship from §3:
a product's breadcrumb walks Occasion → the product itself; a theme collection's breadcrumb uses
its declared parent occasion (if a theme spans two occasions, use the one the customer actually
arrived via — session referrer, not a hardcoded default — falling back to the theme's primary
declared parent for direct/organic entry). This matches
`docs/MERCHANDISING_GUIDE.md`'s already-ratified priority order (Occasion > Theme > Flavor) — kept,
not redesigned. **SEO**: `BreadcrumbList` structured data (already implemented site-wide per
`snippets/tbk-schema-breadcrumb.liquid`, confirmed live in earlier phases) gets accurate,
occasion-anchored paths instead of guessing. **AEO/AI Search**: a clean, single-parent breadcrumb
is exactly the kind of unambiguous entity-relationship signal knowledge-graph extraction favors.

### 8. Internal linking architecture

Three link types, all currently near-zero (Phase 7.1's `docs/INTERNAL_LINKING_AUDIT.md` explicitly
flagged this as unaudited and unbuilt):

1. **Occasion → Theme** (downward): every occasion collection's description links to its 3-5
   most relevant theme collections ("Looking for a specific theme? Unicorn · Jungle Animal ·
   Teddy..."). Mirrors the one incidental example already found live (the `Cakes` collection body
   links to 4 sibling occasion collections) — extend that pattern deliberately rather than by
   accident.
2. **Theme → Occasion** (upward): every theme collection's description states its parent
   occasion(s) and links back ("Part of our Birthday Cakes range").
3. **Collection ↔ Delivery pages**: every occasion collection links to the relevant delivery pages
   (same-day, midnight) and vice versa — `seo-audit/final/INTERNAL_LINKING.md` (Phase 7.1)
   explicitly found **zero** links either direction today.

**Automation opportunity**: this is templatable, not bespoke per collection — a single Liquid
snippet (`snippets/related-collections.liquid`, new) reads the `parent_occasion`/theme metafield
relationships and renders the correct links automatically, so a newly created theme collection gets
correct cross-links with zero manual authoring, the same principle as §4's automatic classification.

### 9. AI Search entity hierarchy

```
Organization: The Baking Kaur
  └─ LocalBusiness (Bakery), Meerut, ~15km service radius
       └─ ProductGroup: Birthday Cakes  (schema.org ProductGroup, one per Occasion collection)
            └─ Product: {individual cake}
                 └─ (theme, flavor as additionalProperty / variesBy, not separate entities)
```

Each Occasion collection becomes one `ProductGroup` entity — a clean, singular "thing" per customer
intent, rather than today's 5 near-duplicate URLs all claiming to be "cakes in Meerut" (the exact
problem Phase 7.8 flagged as the store's clearest current duplicate-content risk). Theme and flavor
are **properties of products within a group**, not separate top-level entities — this avoids
manufacturing dozens of thin, competing entities for what's really one product line viewed through
different filters.

**Explicit, honest caveat carried forward from Phase 7.8**: `docs/AI_SEARCH_READINESS.md` found the
storefront **entirely password-gated** — no AI crawler (GPTBot, ClaudeBot, Google-Extended,
PerplexityBot) can index anything today. Every recommendation in this section is architecturally
correct and ready, and has **zero live effect until the password gate lifts** (a separate,
already-tracked business decision this document doesn't reopen).

### 10. GEO hierarchy

Same entity model as §9, read through a *local* lens: `LocalBusiness` is the anchor entity for all
"cake delivery in Meerut" / "cake shop near me" style generative-engine queries, with each Occasion
`ProductGroup` as a sub-entity answering "what kind of cake." The **service pages** (same-day,
midnight delivery — §6, §15) are the GEO-relevant surface for delivery-logistics queries
specifically, kept deliberately separate from product collections (a delivery-speed query and a
product-type query are different search intents and should resolve to different, non-competing
URLs — this is the architectural fix for the whole 5-collection duplicate cluster, generalized).
Same password-gate caveat as §9 applies.

### 11. AEO hierarchy

Answer-engine relevance here means: does a single URL cleanly answer one question. Today's
duplicate cluster fails this (5 URLs all trying to answer "cakes in Meerut" with the same list).
Target state: each Occasion collection answers "what {occasion} cakes are available," each Theme
collection answers "what {theme} cakes are available," each delivery page answers "how does
{delivery type} work" — one clear question per URL, matching `docs/AEO_READINESS.md`'s own scoring
criterion (FAQ infrastructure exists at 3/5; this collection-level clarity is the missing structural
half of that score, not a content gap). FAQPage schema (already correctly scoped to genuine FAQ
pages only, per Phase 7.4's removal of the mismatched global block) should be considered for the
delivery pages specifically, since "how does midnight delivery work" is a natural FAQ-shaped query
— a future content decision, not proposed as implemented here.

### 12. Merchant Center category mapping

Categorization here is **product-level**, not collection-level — confirmed in Phase 7.8:
`mm-google-shopping.custom_product = true` is already set on all active products (no GTIN/MPN
exists for made-to-order cakes, a correct, already-ratified decision — not reopened here). The
architectural gap this document closes: **`google_product_category` should be derived from
`product_type`**, the same controlled vocabulary driving collection membership (§4), so every future
product gets correct Shopping categorization automatically instead of needing manual entry.

| `product_type` | Target Google product category path |
|---|---|
| Birthday Cake, Anniversary Cake, Wedding Cake, Designer Cake, Theme Cake, Photo Cake | Food, Beverages & Tobacco > Food Items > Baked Goods > Cakes |
| Hamper / Cake Hamper | Food, Beverages & Tobacco > Food Items > Gift Baskets *(or the closest confirmed node — see caveat)* |

**Deliberate caveat, per this project's "never invent" rule**: exact numeric Google taxonomy IDs
are not fabricated here — Google's product taxonomy file changes periodically, and inventing a
specific ID without checking it against the live taxonomy would risk shipping a wrong category
silently. The *path* above is accurate to Google's public taxonomy structure as of this
engagement's knowledge; **the exact ID should be confirmed against Google's current taxonomy file
at implementation time**, a 5-minute lookup, not a design decision.

**Current live impact**: Merchant Center is submitting **0 products today** (confirmed in
`FINAL_NAP_AND_MC_ARCHITECTURE.md` and re-flagged in Phase 7.8) — this mapping has no live Shopping
listing to affect yet; it's groundwork for when the feed goes live, not an urgent fix.

### 13. Google Shopping mapping

Same mapping as §12 — Shopping and Merchant Center categorization are the same underlying field in
the modern Shopify/Google integration (there's no separate "Shopping-only" taxonomy to design).
Noted as its own numbered item per the request, but architecturally it is §12, not a second system.

### 14. Filters and faceted navigation

Given the axis model in §1, faceted navigation on every Occasion collection should expose exactly
three filters, matching the three real axes and nothing else:

- **Theme** (tag-based, `theme:*`) — lets a Birthday Cakes visitor narrow to Unicorn without
  leaving the collection or needing to know the theme collection exists separately.
- **Flavor** (tag or variant-option based, `flavor:*`) — never promoted to its own collection
  (§1), always a filter, matching the already-correct pattern for this axis today.
- **Price** (native Shopify range filter) — already standard, no design change needed.

**Explicit non-recommendation**: do not add a "Recipient" (For Him/For Her) top-level filter at
current volume (11 + 1 products) — with `theme:*` tagging in place, a `recipient:him`/`recipient:her`
tag is trivial to add as a *value within* the theme filter facet rather than a whole separate UI
control, avoiding building filter infrastructure for a 12-product edge case.

### 15. URL strategy

**No handle changes are proposed or implied by this document** — `CLAUDE.md`'s own standing
principle ("Never rename a handle... changes live URLs, can silently kill printed QR codes... needs
the full 8-step checklist") governs any actual handle change, and that process is explicitly
deferred elsewhere, unchanged by this design.

Target URL shape (already the live pattern for every collection that matters — this formalizes,
doesn't change it):

- Occasion: `/collections/{occasion}-cakes` (e.g. `/collections/birthday-cakes` — already correct,
  live, untouched).
- Theme: `/collections/{theme}` (e.g. `/collections/unicorn` — already correct, live, untouched).
- Gifting: `/collections/{gift-type}` (e.g. `/collections/cake-hampers` — already correct).
- Delivery/service intent: `/pages/{service}-cake-delivery-meerut` — **not** `/collections/*`. This
  is the one structural correction this document makes versus today's live state: the 5-collection
  duplicate cluster exists specifically because delivery-speed intent was modeled as a collection
  URL. The `meerut-delivery` pages already live at this correct URL shape (confirmed in Phase 7.8) —
  the fix is architectural recognition + eventual migration (Part 6), not a new URL pattern to
  invent.

### 16. Canonical strategy

- Every Occasion and Theme collection **self-canonicalizes** — each represents a genuinely distinct
  entity/intent (confirmed by `seo-audit/final/WEBSITE_ARCHITECTURE.md`'s finding that the 13 theme
  collections are "real, distinct," not filtered duplicates of each other).
- A product that belongs to both an Occasion and a Theme collection (e.g. a Unicorn cake reachable
  via both `/collections/birthday-cakes` and `/collections/unicorn`) canonicalizes its **product**
  page to itself regardless of entry collection (standard, already correct Shopify behavior — not a
  design change).
- The 5-collection duplicate cluster is the one deliberate **exception** to self-canonicalization:
  until the migration in Part 6 resolves which 1-2 survive, the non-surviving collections should
  canonicalize to the survivor rather than each self-canonicalizing — this is a canonical-tag change,
  reversible, lower-risk than a redirect, and exactly the kind of "reusable, safe" intermediate step
  this document is allowed to recommend even though it can't implement it.
- The `Cakes` root/index collection is **non-canonical by design** — it's a navigation aid
  (§2's tree root), not meant to compete in search against the Occasion collections that actually
  carry unique, hand-written copy.

### 17. Automation rules — how future products classify themselves

This is the load-bearing section for "optimize for the next 10,000 products," not an afterthought:

1. **Controlled vocabulary, enforced at creation.** `product_type` is restricted to a fixed list
   (Birthday Cake, Anniversary Cake, Wedding Cake, Designer Cake, Theme Cake, Photo Cake, Cake
   Hamper, Festival Hamper) — the same list §4's smart-collection rules key on. No free-text
   product types.
2. **Standardized tag namespace, applied at creation**: `occasion:{value}`, `theme:{value}`,
   `flavor:{value}`, and optionally `recipient:{value}`. One occasion tag required; theme and
   flavor optional/multi-valued; recipient optional.
3. **A lightweight, reusable classification script** — `seo-ops/classify_product.py` (proposed, not
   built in this pass): follows this project's own established convention exactly (dry-run by
   default, review CSV, `--apply`, ≤8-batch mutations, same pattern as `fix_seo_snippets.py` and
   `fix_mojibake.py`). Its job: audit every product against the controlled vocabulary + tag
   namespace, flag any product missing a required occasion tag or carrying a non-vocabulary
   `product_type`, and (only on `--apply`, only for unambiguous cases — e.g. a product titled
   "Unicorn Birthday Cake" missing its `theme:unicorn` tag) backfill the obvious tags. Ambiguous
   cases (a product type that doesn't map cleanly, same "never guess" boundary as every prior
   phase) get flagged for review, not guessed at.
4. **New-theme onboarding is then zero-config**: because Theme collections are smart (§4, ruled on
   `tag = theme:X`) and the internal-linking snippet (§8) reads the same tag data, adding a 14th
   theme collection means: create the collection, set its smart rule to the new tag, tag the
   relevant products. No manual product-adding, no manual cross-link authoring, no navigation
   rebuild beyond adding one "Shop by Theme" menu entry.

**This is the concrete "build systems, not fixes" deliverable**: every other recommendation in this
document (hierarchy, breadcrumbs, linking, filters) *depends* on this automation layer existing —
without it, the target architecture would decay back into today's state (manual collections
drifting out of sync) the moment product #1,236 is created.

---

## Part 3 — Automation Blueprint (consolidated)

| Component | What it automates | Reuses |
|---|---|---|
| Controlled `product_type` vocabulary | Which primary Occasion collection a product joins | Shopify's native product field — zero new tooling |
| `occasion:*` / `theme:*` / `flavor:*` / `recipient:*` tags | Theme collection membership, filter facets, breadcrumb parent resolution | Shopify's native tag field |
| Smart collection rules keyed on type/tags | Collection membership itself | Native Shopify smart collections — replaces today's fragile substring rules |
| `seo-ops/classify_product.py` (proposed) | Auditing/backfilling tags on existing and newly imported products | This project's own established dry-run/CSV/`--apply`/batched-mutation convention (`fix_seo_snippets.py`, `fix_mojibake.py`, `fix_description_occasion.py`) |
| `snippets/related-collections.liquid` (proposed) | Occasion↔Theme cross-linking, delivery-page linking | Metafield relationship data from §3, rendered once, works for every current and future collection |
| `custom.parent_occasion` metafield | Breadcrumb parent, related-collections, theme-collection "part of" copy | Shopify's native metafield system |
| `google_product_category` derived from `product_type` | Merchant Center / Shopping categorization | Same controlled vocabulary as collection membership — one source of truth, not two |

---

## Part 4 — Execution Roadmap

Phased so each phase is independently valuable and independently reversible — no phase depends on
a later phase succeeding, and every phase after Phase 0 depends only on Phase 0's data model
existing, not on any specific collection decision.

**Phase 0 — Data model (no visible change)**: define the controlled `product_type` vocabulary and
tag namespace; build and dry-run `classify_product.py` against the full catalogue; review the
audit CSV. Nothing is applied to Shopify in this phase beyond the read-only audit.

**Phase 1 — Backfill (data only, no visible change)**: apply the tag backfill for unambiguous
cases only (per §17.3); hand off ambiguous cases for a merchandising decision, same as every prior
phase's governance.

**Phase 2 — Smart-collection conversion (per-collection, reversible)**: convert Occasion
collections from manual to smart, one at a time, verifying product membership matches the prior
manual list before and after each conversion (a direct, cheap regression check).

**Phase 3 — Cross-linking (theme-only content change)**: build and deploy
`related-collections.liquid`; populate `parent_occasion` metafields for existing theme collections.

**Phase 4 — Navigation (additive only)**: add the missing occasion pillars and the "Shop by Theme"
menu to `main-menu`; wire the `meerut-delivery` menu to a visible section. Nothing existing is
removed at this phase.

**Phase 5 — Duplicate-cluster resolution (highest risk, business-gated)**: exactly the
already-scoped Phase 7.8 recommendation — GSC/QR/paid-ad audit first, then a business decision on
which 1-2 of the 5-collection cluster survive, then canonical-tag changes (§16) before any redirect
is even considered.

**Phase 6 — Merchant Center mapping**: wire `google_product_category` derivation once the feed is
ready to go live (currently 0 products submitted — no urgency, but the mapping should exist before
the feed launches, not be retrofitted after).

## Part 5 — Priority Matrix

| Item | Customer/SEO value | Effort | Risk | Priority |
|---|---|---|---|---|
| Phase 0-1 (data model + backfill) | Foundational — everything else depends on it | Medium (new script, but follows an established pattern) | Very low (dry-run/CSV first, same governance as every prior phase) | **P0** |
| Phase 2 (manual → smart) | High (closes the "future products need manual work" gap) | Low per collection | Low (reversible, verifiable via membership diff) | **P0** |
| Phase 4 (navigation additions) | High (closes the 30-of-36-collections-orphaned gap) | Low | Very low (additive only) | **P1** |
| Phase 3 (cross-linking) | Medium-high (SEO + AEO structural clarity) | Medium (one new snippet + metafield population) | Very low | **P1** |
| Phase 6 (Merchant Center mapping) | Low today (0 products live), high once feed launches | Low | None (no live feed yet) | **P2** (do before feed launch, not urgently) |
| Phase 5 (duplicate cluster) | High value, but gated on a business decision + external audit this document cannot perform | Medium | **Highest** (live URLs, possible QR/ad impact) | **P2 — sequenced last on purpose**, not because it's unimportant |

## Part 6 — Migration Strategy

- **Every phase above is additive or reversible until Phase 5.** Phases 0-4 either add new data
  (tags, metafields) that nothing currently depends on, or add navigation/linking that doesn't
  remove anything existing — rollback for any of them is "stop/revert the specific change," with no
  cascading effect on other phases.
- **Phase 2's smart-collection conversion has a built-in verification gate**: capture each
  collection's current manual product list before converting; after converting, diff against the
  smart rule's actual membership; any discrepancy blocks moving to the next collection until
  resolved. This directly prevents a repeat of this store's own history (an undocumented rule
  conversion in Phase 7.8's audit #2 is exactly how the 5-collection duplicate cluster was created
  in the first place).
- **Phase 5 is the only phase this document does not consider safe to greenlight from documentation
  alone** — it requires external data (GSC, ad platforms, QR code inventory) this repo-and-API-only
  investigation cannot produce, plus an explicit business decision on which collections survive.
  Everything in Phases 0-4 can proceed independently of Phase 5 ever happening.

## Part 7 — Verification Checklist

- [ ] Phase 0: `classify_product.py` dry-run CSV reviewed; every product has exactly one
      `product_type` from the controlled vocabulary or is explicitly flagged for review.
- [ ] Phase 1: tag backfill applied only to unambiguous cases; ambiguous list handed off, not
      guessed at; spot-check a sample of newly-tagged products live.
- [ ] Phase 2: for each converted collection, smart-rule membership count matches (or knowingly
      differs from, with a stated reason) the prior manual membership count.
- [ ] Phase 3: `related-collections.liquid` renders correct, non-broken links on a sample of
      Occasion and Theme collections; no orphaned metafield references.
- [ ] Phase 4: new navigation items resolve to live, correct URLs; existing navigation items
      unchanged; Theme Check clean (matching this project's standing deploy-safety gate).
- [ ] Phase 5 (if/when authorized): GSC/QR/paid-ad audit completed and documented *before* any
      canonical or redirect change; business decision on cluster survivors documented; each change
      verified live via pull/diff before/after, matching this project's established deploy cycle.
- [ ] Phase 6: `google_product_category` values spot-checked against Google's current taxonomy file
      before the Merchant Center feed goes live.

---

## Related

[docs/COLLECTION_STRATEGY_EVIDENCE_REPORT.md](COLLECTION_STRATEGY_EVIDENCE_REPORT.md) (the
historical-evidence reconciliation this design treats as input, not authority),
[CATALOG_ARCHITECTURE.md](../CATALOG_ARCHITECTURE.md), [INFORMATION_ARCHITECTURE.md](../INFORMATION_ARCHITECTURE.md),
[docs/MERCHANDISING_GUIDE.md](MERCHANDISING_GUIDE.md), [docs/AI_SEARCH_READINESS.md](AI_SEARCH_READINESS.md),
[docs/AEO_READINESS.md](AEO_READINESS.md), [docs/GEO_READINESS.md](GEO_READINESS.md),
[FINAL_NAP_AND_MC_ARCHITECTURE.md](../FINAL_NAP_AND_MC_ARCHITECTURE.md), `CLAUDE.md` (handle-change
governance, product-page protection, "never invent" rules — all carried forward unchanged).
