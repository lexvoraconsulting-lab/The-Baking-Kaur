# CHANGELOG — The Baking Kaur Enterprise Transformation

Living record of every file changed: what, why, and how to roll back.
Format per entry: **File · Reason · Business · SEO · Performance · Risk · Rollback.**

Rollback baseline for the whole transformation: branch `phase-a/production-safety`, commit **`2aeff64`** ("Phase A baseline snapshot"). `git checkout 2aeff64 -- <path>` restores any single file; `git reset --hard 2aeff64` restores everything.

---

## Phase A — Production Safety & Cleanup  *(staged in repo, not yet deployed)*

### A1. Rollback baseline
- **File:** (git) branch `phase-a/production-safety` @ `2aeff64`
- **Reason:** capture full working tree before any change.
- **Business/SEO/Perf:** none (safety only). **Risk:** none.
- **Rollback:** n/a — this *is* the rollback point.

### A2. Dead-code removal (10 files)
- **Files removed:**
  `sections/cart-drawer-hulkapps-backup.liquid`, `sections/header-e-commerce-hulkapps-backup.liquid`, `sections/header-inline-hulkapps-backup.liquid`, `sections/main-cart-hulkapps-backup.liquid`, `sections/main-gift-cart-hulkapps-backup.liquid`, `snippets/cart-checkbox-hulkapps-backup.liquid`, `snippets/cart-complementary-hulkapps-backup.liquid`, `snippets/cart-shipping-bar-hulkapps-backup.liquid`, `snippets/item-cart-hulkapps-backup.liquid`, `snippets/item-cart-page-hulkapps-backup.liquid`
- **Reason:** orphaned HulkApps migration backups — verified **0 references** across all `.liquid`/`.json`.
- **Business:** cleaner, faster-to-maintain theme; less editor confusion. **SEO:** none. **Perf:** none at runtime (unreferenced); smaller theme package.
- **Risk:** ○ very low (proven unreferenced). **Rollback:** `git checkout 2aeff64 -- <path>`.

### A3. Duplicate schema removal — conflicting Bakery entity
- **File:** `layout/theme.liquid`
- **Reason:** an inline `Bakery` JSON-LD block duplicated `snippets/bk-local-business.liquid` **with conflicting geo (28.9845,77.7064 vs 28.9931,77.6939) and hours (21:00 vs 23:59)**. Removed the inline block; `bk-local-business` is now the single Bakery source.
- **Business:** consistent business info to Google/AI. **SEO:** high-positive — removes a conflicting duplicate LocalBusiness entity. **GEO:** cleaner entity graph. **Perf:** minor (less inline JSON).
- **Risk:** ○ low (one entity remains). **Rollback:** `git checkout 2aeff64 -- layout/theme.liquid`. **Validate:** Rich Results Test on deploy.

### A4. Duplicate schema removal — WebSite & BreadcrumbList
- **File:** `snippets/structured-data.liquid`
- **Reason:** emitted a 2nd `WebSite` (dup of `tbk-schema-website.liquid`) and a 2nd `BreadcrumbList` (dup of `tbk-schema-breadcrumb.liquid`). Rewrote to keep ONLY Shopify-native `Product`/`Article` schema (its unique, valuable contribution).
- **Business:** correct rich results. **SEO:** high-positive — removes duplicate WebSite + Breadcrumb; **preserves native Product schema**. **GEO:** single canonical entities. **Perf:** minor.
- **Risk:** ◐ medium (schema surface). **Rollback:** `git checkout 2aeff64 -- snippets/structured-data.liquid`. **Validate:** Rich Results Test on Home/Product/Collection/Article before promote.

### Canonical schema sources after Phase A
| Entity | Source |
|---|---|
| Organization + WebSite | `snippets/tbk-schema-website.liquid` |
| Bakery / LocalBusiness | `snippets/bk-local-business.liquid` |
| BreadcrumbList | `snippets/tbk-schema-breadcrumb.liquid` |
| Product / Article (native) | `snippets/structured-data.liquid` |
| FAQPage | inline in `theme.liquid` *(placement flagged — see SEO plan)* |

### A6. Restore missing site footer (approved: minimal, production-safe)
- **Files added:** `sections/site-footer.liquid`, `sections/footer-group.json`
- **Reason:** production rendered **no footer** — `theme.liquid` called `sections 'footer-group'` but that group existed on neither repo nor live theme; `footer.liquid` (broken ``` fence, no schema) and `tbk-footer.liquid` (hardcoded, no schema) were orphaned and unusable. Built a minimal, semantic, token-styled footer wired via a new `footer-group.json`.
- **Content (all real):** NAP (`<address>`), `tel:`/`mailto:`, Instagram + WhatsApp, Company/Delivery links to **verified** pages, policies via native `shop.*_policy` (all four resolve), trust strip, copyright. Editable via section settings.
- **Business:** restores trust, navigation, legal-policy access (compliance). **SEO:** footer internal-linking backbone + `SiteNavigationElement`. **GEO:** NAP reinforcement. **Perf:** negligible (scoped CSS, lazy logo).
- **A11y:** `role="contentinfo"`, 3 labelled `<nav>`, `<address>`, visible focus rings, sr-only heading.
- **Risk:** ○ low (additive; no new visual language — uses `tbk-tokens`). **Rollback:** `git rm sections/site-footer.liquid sections/footer-group.json` (or `git checkout 2aeff64`), then footer reverts to prior (absent) state.
- **Note:** premium enterprise footer deferred to Phase E; this is the temporary production-safe restore.

### Phase A validation (on preview theme `colorful-composition` #151370334377)
- Footer renders: `contentinfo`, 3 navs, all links correct, all 4 policies resolve, copyright + NAP present.
- **Schema dedup verified in rendered HTML: Bakery ×1, WebSite ×1, BreadcrumbList ×1** (was ×2 each); native Product schema intact; footer `SiteNavigationElement` present.
- Mobile 375px: single-column stack, **no horizontal overflow**. Brand token bg `#FDFAF8` applied.
- Caught + fixed 2 issues during validation: (1) `url`-type schema settings can't take URL defaults → switched to `text`; (2) `footer-group.json` was rejected on first push because the section it referenced had an invalid schema → re-pushed after fix.
- **Pre-existing issue observed (not introduced):** `tbk-schema-website` throws a Liquid error when `settings.logo` is blank (`image_url` on empty) — flagged for Phase B/F.
- **Deploy state:** staged + validated on preview only. **NOT yet on the live theme** — awaiting approval to promote.

---

## Phase A — DEFERRED (with reasons)
| Item | Why deferred | Owner phase |
|---|---|---|
| **Duplicate Uploadcare load** in `theme.liquid` | Feeds the **protected** PDP reference-image upload; removing a load needs PDP regression testing. | A-2 (post-approval) w/ PDP test |
| **3 whole-document MutationObservers** | Each masks a root cause (sticky bar, `<` arrows, mojibake data). Removing blind reintroduces bugs. | B/H after root-cause |
| **Global FAQPage schema** | Not a duplicate — a placement issue (should be page-scoped). | F/G |
| **Self-asserted AggregateRating** in `bk-local-business` | SEO-quality (needs real review source), not a duplicate. | F |
| **Disabled header backups** in `header-group.json` (`announcement-bar`, `header-e-commerce`, `header-menu-bottom-hulkapps-backup`) | Editing the active header group belongs with header consolidation. | E |
| **`rewind_*` legacy pair** | Marked "do_not_delete"; verify no page uses the template first. | B |

---

## Phase A — PROMOTED TO LIVE (2026-07-14)
Scoped push of `layout/theme.liquid`, `snippets/structured-data.liquid`, `sections/site-footer.liquid`, `sections/footer-group.json` → live theme `Baking Kaur — Draft` (#151307485353, `--allow-live`).
**Verified on live:** footer restored (4 navs, 22 links, 6 policies, NAP, copyright); schema deduped (Bakery/WebSite/Breadcrumb ×1, 0 parse errors); protected PDP intact (premium markers present); collections/search/cart/policies 200; CLS 0; mobile 3-col nav + 2-line trust, no overflow.
**Found (pre-existing, not Phase A):** `tbk-schema-website` Liquid error on blank `settings.logo` (Organization logo field malformed); homepage H1 count = 2; full load ~24.5s.
**Rollback:** `git checkout 2aeff64 -- layout/theme.liquid snippets/structured-data.liquid` + remove footer files, then push to #151307485353.


---

## Phase C1 §2 — Delivery Promise (FROZEN v1.0) — preview only
- **Files:** `sections/home-delivery-promise.liquid` (new), `templates/index.json` (section added as §2, 6 blocks).
- **Reason:** communicate trust immediately below the hero; assembly of the frozen card system (zero new components).
- **Business:** trust + internal linking to delivery/eggless/custom pages. **SEO:** 6 new internal links, semantic list, no H2 pollution, page keeps exactly 1 H1. **GEO:** reinforces same-day/midnight cake delivery in Meerut, eggless, custom designer cakes. **Perf:** zero JS, zero images (inline SVG), CLS 0.
- **Links:** all 6 destinations verified HTTP 200. 4 of the recommended routes 404'd (`same-day-cake-delivery`, `eggless-cakes` collection, `our-promise`, `cake-customization`) → linked to verified pages instead; canonical routes recorded as placeholders (Phase G). `/collections/eggless-cakes` intentionally not created (would duplicate `/collections/all`).
- **Bug fixed in build:** unclosed `{% if count > 0 %}` nested the `{% schema %}` tag → push rejected; fixed + tag-balance check added to validation.
- **Risk:** ○ low (additive, preview only). **Rollback:** `git rm sections/home-delivery-promise.liquid` + remove `home_promise` from `templates/index.json`, or `git checkout 2aeff64 -- templates/index.json`.


---

## Phase C1 §3 — Occasion Navigation (FROZEN v1.0) — preview only
- **Files:** `sections/home-occasions.liquid` (new), `templates/index.json` (added as §3, 6 blocks).
- **Reason:** route visitors to primary commercial intents directly below the trust row.
- **Business:** 6 internal links to revenue pillars + B2B corporate lead-gen. **SEO:** H1→H2→H3 hierarchy, ItemList schema, crawlable canonical destinations. **GEO:** each occasion becomes an entity with an absolute URL (Bakery → category → products). **Perf:** 0 JS, lazy WebP srcset, explicit w/h, CLS 0.
- **Decisions applied:** product counts **OFF** (clean editorial; `show_counts` retained for a later phase); **Corporate Gifting retained** with the approved graceful fallback (image slot ready).
- **Evidence-based exclusions:** Kids / Custom / Same-Day / Midnight — all 0-product collections; delivery already linked from §2.
- **Bugs fixed during build:** (1) unclosed `{% if %}` nested the `{% schema %}` tag; (2) section name exceeded Shopify's 25-char limit; (3) setting label exceeded Shopify's 70-char limit.
- **Finding:** storefront counts != Admin counts — **584/1,235 products are DRAFT** (Hampers shows 8 of 119). Logged as backlog "Publish draft catalogue"; CATALOG_ARCHITECTURE count basis corrected.
- **Risk:** low (additive, preview only). **Rollback:** `git rm sections/home-occasions.liquid` + remove `home_occasions` from `templates/index.json`.


---

## Merchandising Review — draft catalogue classification (2026-07-16) — **audit only, zero changes**
**Nothing was published, archived, edited or deleted.** Read-only GraphQL audit of all 584 drafts + documentation.

### Inventory health
| Total | Active | Draft | Archived | **Publish-ready** |
|---|---|---|---|---|
| **1,235** | **607** (49.1%) | **584** (47.3%) | **44** (3.6%) | **25** (2.0% of catalogue) |

### Draft classification (584, each counted once)
Needs Images **363** (62.2%) · Duplicate **150** (25.7%) · Seasonal **40** (6.8%) · Ready to Publish **25** (4.3%) · Internal/Test **6** (1.0%) · Needs Content **0** (absorbed — every content-gap draft is also image-less) · Discontinued **0** (⚠️ not machine-determinable — needs client judgement).

### Root cause
- **503 of 584 drafts (86%) have zero images** — the single blocker. **0 drafts are priced ₹0**; pricing is healthy.
- **Duplicates are a systematic import artefact:** 75 groups × exactly 2. In **56 groups** the image sits on the legacy short handle (`hamper12`/`ch38`) and the SEO-slug twin has 0 images → **56 twins archivable with no content loss**. 19 groups have 0 images on both copies → need a decision, not a merge.
- **8 drafts carry mojibake titles** (`ch290`, `ch292`–`ch296`, `ch298`) — must not reach the storefront.
- The 25 publish-ready drafts skew **premium Wedding/Anniversary, ₹1,200–₹3,500** — the highest-AOV pillar sitting invisible.

### Collections affected (Admin → shoppable)
Birthday 279→**226** · Anniversary 102→**85** · Wedding 134→**70** · Designer & Theme 165→**78** · **Cake Hampers 119→8** (174 drafts tagged `hampers`; the range is effectively unsellable — the one genuine commercial gap).

### Decisions
- **No bulk publish** — 503 image-less + 8 corrupted-title products would make the storefront worse, not better.
- **Homepage merchandises live, purchasable products only**; sections degrade gracefully on thin inventory (S4 onward).
- **Corporate Gifting card retained** — B2B lead-gen destination, not inventory-dependent.
- Client action sequence recorded: archive 56 duplicate twins → fix 8 titles → review the 25 publish-ready → decide the 6 Addon/Test items → photograph Hampers-first → hold Diwali for the season.

### Docs updated
`CATALOG_ARCHITECTURE.md` §1b (replaces the earlier count-basis note with the full review) · `HOMEPAGE_CONTENT_STRATEGY.md` (new "Merchandising constraint — live inventory only") · this entry.
**Note:** the brief named `CONTENT_STRATEGY.md`; no such file exists — the content source of truth is **`HOMEPAGE_CONTENT_STRATEGY.md`**, which is what was updated.
**Business value:** Trust (no unavailable products shown) · Conversion (publish effort ranked by AOV) · SEO (no thin/corrupted pages indexed) · Maintainability (import defect documented with its fix).


---

## Phase C1 §4 — Bestsellers (BUILT — awaiting review) — preview only
- **Files:** `sections/home-bestsellers.liquid` (new), `templates/index.json` (added as §4, after `home_occasions`).
- **Assembly only:** FROZEN `tbkx-card--product` + `--link/--interactive` + `tbk-button` (secondary) + tokens. **Zero new components.** DOM-verified: **0 legacy `tbk-` classes inside the section**; protected PDP untouched.
- **Reason:** convert on proven demand — the shortest path from homepage to a PDP that already sells.
- **Source:** `best-selling-products` smart collection (`sortOrder: BEST_SELLING`) — real sales data, self-maintaining, zero manual curation.

### ⚠️ Naming conflict flagged for client
The brief lists S4 as **"Featured Collections"**; `HOMEPAGE_SPECIFICATION.md`'s canonical order sequences **Bestsellers** here. **Built Bestsellers** — "Featured Collections" would have duplicated S3 Occasion Navigation exactly (same frozen card, same six destinations), adding a second crawl path to the same URLs and diluting the link graph. S3 = *"what occasion?"*; S4 = *"what do people actually buy?"*. **Needs confirmation.**

### Deliberate omission — no add-to-cart
Spec's §3 row targets `add-to-cart`. **Not built, by design:** the protected PDP owns the customization flow (weight/flavour/message). A homepage ATC would bypass it and ship the wrong cake — a fulfilment failure, not a conversion win. Raise with client if genuinely wanted.

### Merchandising safety (applies the 2026-07-16 review)
- **Live products only by construction** — storefront Liquid cannot see DRAFT products; the 584 drafts are structurally unreachable here.
- **Graceful degradation tested, not asserted** — pointed at a real 0-product collection on preview: section vanished entirely, **no orphan heading, no empty grid, no stray ItemList schema**; other sections unaffected; reverted after the test.
- **`availability` bound to `product.available`**, not hardcoded `InStock` — corrected before final push.

### Business value
**Conversion:** routes homepage traffic to proven revenue PDPs. **SEO:** 8 crawlable links to highest-converting pages; self-re-ranking with demand. **GEO:** ItemList of **Product** entities with price/currency/availability completes `Bakery → category → priced product`, letting AI answer *"how much is a cake at The Baking Kaur?"* with a real number and URL. **Trust:** cannot surface unavailable inventory. **Perf:** 0 JS, lazy WebP srcset, explicit w/h, CLS 0. **Maintainability:** smart-collection sourced, 8 settings, no hardcoded products.

### Validation (preview 151370334377)
4/4 sections render · 8 cards · H1→H2→H3 intact · 1 link/card, 0 nested · **9/9 destinations HTTP 200** · 8/8 images lazy+WebP+explicit w/h+alt · ItemList valid (8 items, absolute URLs) · 0 `<script>` in section · responsive verified 375/624/1280 (2→3→4 cols, ratio 0.80 exact, no overflow) · settings survived push (pull-back verified).

### Bugs avoided during build
(1) **Push-ordering trap** — section pushed first, `index.json` separately, then pulled back to confirm all 8 settings survived. (2) **`index.json` has a Shopify auto-generated `/* */` header** — plain `json.load` fails; header preserved on rewrite. (3) Naive tag-balance regex mis-flagged schema placement (`{%-` vs `{%` dashes) — re-verified correctly.

- **Risk:** low (additive, preview only). **Rollback:** `git rm sections/home-bestsellers.liquid` + remove `home_bestsellers` from `templates/index.json`.
- **Finding logged:** 3 of the top 8 bestsellers use legacy handles (`b158`, `b155`, `hamper13`) → backlog "Rehandle legacy-slug bestsellers" (needs 301s).


---

## Phase C1 §4 — Bestsellers **FROZEN v1.0** (2026-07-16)
- **Approved by client and frozen.** `sections/home-bestsellers.liquid` + `templates/index.json` (§4). No S4 changes without explicit unfreeze.
- Recorded in `HOMEPAGE_SPECIFICATION.md` as **Version 1.0 — FROZEN**.

### 🚫 Client directive — no handle renames during Homepage development
The S4 finding (3 of the top 8 bestsellers on legacy handles `b158`, `b155`, `hamper13`) is **deferred in full**. All three resolve HTTP 200 — nothing is broken, and S4 links to them exactly as they are.
Escalated from a backlog task to a standalone project: **SEO MIGRATION – Product Handle Optimization** (`PROJECT_ROADMAP.md`), with 8 mandatory steps — handle mapping · 301 redirect plan · internal link update · **QR code audit** · Google indexing verification · sitemap update · canonical validation · Search Console monitoring.
**Standing rule recorded for S5–S9:** sections link to handles exactly as they exist; never rename, never hardcode a prettier URL.
**Why the QR audit can veto a rename:** a printed QR code encodes a URL permanently — it cannot be reissued once it's on a cake box. That URL must resolve forever, which makes some handles effectively un-renameable regardless of SEO value.

### Docs updated
`HOMEPAGE_SPECIFICATION.md` (S4 → FROZEN v1.0) · `PROJECT_ROADMAP.md` (SEO Migration project replaces the rehandle stub) · `SEO_GEO_MASTER_PLAN.md` (handle-rename freeze rule for S5–S9) · `HOMEPAGE_CONTENT_STRATEGY.md` (URL & handle rule) · this entry.


---

## 🔴 INCIDENT + FIX — fabricated reviews removed from production (2026-07-16)
**Client-approved, executed on the LIVE theme (151307485353), verified on the public storefront.**

### What was live
- **4 fabricated testimonials attributed to named individuals** — Aisha Patel, Ravi Sharma, Neha Verma, Amit Verma — on the production homepage, section `testimonials_dhWXwb`, **not disabled**.
- A **hardcoded `"aggregateRating": {"ratingValue":"4.8","reviewCount":"500"}`** in the `Bakery` JSON-LD from `snippets/bk-local-business.liquid`. That snippet renders in `<head>`, so the unverifiable rating was on **every page of the site (~1,200 URLs)**, not just the homepage.

### How it was identified
Unreplaced **Ecomus theme demo content**. Two independent tells: the reviews praised **almond croissants, breads, cinnamon rolls and coffee** — a butter-and-egg café menu, for a 100% eggless cake bakery that delivers — and one contained a *complaint* ("the only downside is that they close a bit early"), which no business writes into its own testimonials. The 4.8/500 was backed by no data at all.

### Fixed
- Fabricated blocks **deleted** from `templates/index.json` (not merely hidden — the names and text no longer exist in the theme).
- Section **disabled** → gracefully hidden: **no orphan heading, no orphan schema**.
- `aggregateRating` **removed** from `bk-local-business.liquid`; all legitimate Bakery data preserved (name, address, geo, hours, telephone, sameAs); **permanent guard comment** added explaining why it must never return.
- Theme-editor-only placeholder: *"Waiting for verified review source."*

### Verified on production (fresh session, preview cookie cleared)
Fabricated names/text **gone** · `hdt-testimonials` **not rendered** · `aggregateRating`/`ratingValue`/`reviewCount` **gone sitewide** · no orphan heading · placeholder **not** leaked to customers · Bakery schema intact and parsing · **unapproved homepage (S1–S5) still NOT on live** — live `index.json` was patched surgically via pull→patch→push, never from the repo copy.

### Process note — a false negative I nearly reported
An early verification appeared to show the fix had failed. Two causes, both mine: (1) the browser tab still held a `preview_theme_id` cookie, so I was inspecting **preview**, not live — and the cookie is per-domain, so a "fresh tab" inherited it; (2) my grep for `aggregateRating` matched **my own guard comment**. Both were caught by checking the authoritative source — pulling the file back from the live theme and parsing the emitted JSON body — rather than trusting a string match on rendered HTML. **Lesson: verify against the artefact, not the rendering, and confirm which theme you are actually looking at.**

---

## Phase C1 §5 — Social Proof / Reviews **FROZEN v1.0** (2026-07-16) — genuine data only
- **Files:** `sections/home-reviews.liquid` (new), `templates/index.json` (§5), `REVIEW_STRATEGY.md` (new).
- **Assembly only:** FROZEN `tbkx-card--review` + `tbk-button` + tokens. **Zero new components.** PDP untouched.
- **New data model:** `testimonial` metaobject — **"Verified Review"** (`gid://shopify/MetaobjectDefinition/13988495529`). Fields, **all mandatory**: author · body · rating (1–5) · source · **source_url (public proof link)** · review_date · **verified**.

### Frozen rendering NOTHING — correct, not a defect
**0 verified reviews exist**; no approved source is installed (verified: no Judge.me, Loox, Shopify Product Reviews, Okendo, Stamped, Yotpo). Section renders nothing to customers and **activates automatically** on the first verified entry — no code change, no deploy.

### Fabrication impossible by construction
The section has **no setting capable of holding review text, a name, a rating or a count**. An entry **cannot be saved without a public proof link**. Only `verified == true` renders. This is the structural answer to the incident above: the old section stored review text in theme settings — indistinguishable from fiction, no provenance.

### 🚫 Emits NO structured data — deliberately
No `Review`, no `AggregateRating`. Google disallows **self-serving** ratings for `LocalBusiness`/`Organization`; **re-adding it would be wrong even with genuine data**. Computing an aggregate from a hand-picked subset would also declare a rating no data supports. **GEO is unaffected** — AI assistants read visible text, so real reviews earn AI visibility with zero markup.

### Validation (preview 151370334377)
**Empty state:** wrapper renders **0 bytes** — no heading, cards, or schema; placeholder not leaked; S1–S4 unaffected.
**Populated state:** tested with disposable, unmistakably-non-review entries, then deleted. Verified entry rendered; **unverified entry did NOT leak** (the core guarantee); stars rendered ★★★★☆ / `aria-label="4 out of 5"` from a seeded rating of **4** — proving data-driven, not hardcoded; `rel="nofollow noopener ugc"` on source links; H2→H3 intact; 0 JS; no schema. **Cleanup verified** — storefront back to clean empty state.

### Docs
**`REVIEW_STRATEGY.md` created** — sources · governance · moderation · schema rules · AggregateRating rules · Google compliance · AI-search compliance · incident record. Also updated: `HOMEPAGE_SPECIFICATION.md` (S5 frozen), `HOMEPAGE_CONTENT_STRATEGY.md` (§8 rewritten, rating hero removed, review copy rule), `SEO_GEO_MASTER_PLAN.md`, `SCHEMA_MASTER.md`, `PROJECT_ROADMAP.md` (Collect genuine reviews).
- **Risk:** low (renders nothing). **Rollback:** `git rm sections/home-reviews.liquid` + remove `home_reviews` from `templates/index.json`.


---

## Client decisions recorded (2026-07-16)
**1 · Google Business Profile ratified as PRIMARY review source.** S5 is designed around it: transcribe genuine Google reviews into `testimonial` entries with public `source_url`, verify against source, section activates automatically. Judge.me/Loox remain approved fallbacks. Prohibitions restated and unchanged: never fabricate review text, counts, ratings or AggregateRating; hide gracefully when verified reviews are insufficient. `REVIEW_STRATEGY.md` §1.

**2 · "20,000+ celebrations" = brand milestone, NOT review data.** May be stated as a trust signal; may **never** be exposed as a review count, fed into `AggregateRating.reviewCount`, or paired with stars so it reads as a rating basis. Rationale recorded: customers-served and ratings-received are different facts, and merging them manufactures a rating basis from an operational statistic — the same shape as the removed 4.8/500, and prohibited **even though the milestone may be true**. Currently unverified; if unsubstantiable, replace with a verified milestone (Shopify order count, years in operation) — never soften into vagueness. `REVIEW_STRATEGY.md` §5b.

**3 · SEO CONTENT FIX – Product Titles & Encoding** — new backlog project. Encoding cleanup · title/H1 consistency · search snippet optimization · **preserve URLs** · no homepage dependency. Kept strictly separate from **SEO MIGRATION – Product Handle Optimization**: title fixes are safe and reversible, handle changes need 301s and a QR audit. Records that the store's **#1 bestseller** currently shows a `<title>` naming a *different cake* (`Celestial Charm Cake ÃÂÃÂ¢??…`) against an H1 of `Motu Patlu Designer Birthday Cake` — a live, revenue-facing defect, higher priority than the 8 corrupted drafts because customers see it in Google today. Does not block homepage development.


---

## Phase C1 §6 — Craft Story **FROZEN v1.0** (2026-07-16)
- **Files:** `sections/home-craft-story.liquid` (new), `templates/index.json` (§6).
- **Assembly only:** FROZEN `tbk-button` (primary + ghost) + tokens. **Zero new components** — the 5/7 editorial split is section-scoped layout, same precedent as S1/S3/S4. PDP untouched.
- **Copy:** `HOMEPAGE_CONTENT_STRATEGY.md` §5 verbatim — "100% eggless. 100% handcrafted." / "Baked fresh after you order — never from a shelf."

### Trust points are a plain list, not `tbkx-card--trust` — deliberate
S2 already owns the trust-card pattern. Reusing cards here would duplicate a component's **job** and put two competing trust blocks on one page. The reuse rule forbids duplicate components; this extends it to duplicate **uses**.

### 🚫 No image shipped — and no stock asset used
The theme's stock images (`p1`/`p2`/`c1`/`c2`/`h1`/`h2`/`g1`) are **Ecomus demo content — the same source as the fabricated testimonials removed today**. Shipping one as this bakery's craft would be the identical mistake in a new costume. Catalogue photos are also unusable (Zomato watermarks, TWC branding, customers' piped names). **Section renders text-only, centred, max 72ch — no broken layout, no placeholder.** Image is an optional setting; addable later with no code change. Backlogged into **Flagship Hero Photoshoot**.

### 🚫 Emits NO structured data — deliberately
Prose is not a list or Q&A; there is no honest schema type for it. Inventing `FAQPage` for non-Q&A prose is exactly the "markup that doesn't match visible content" pattern this project has been removing. GEO unaffected — AI reads visible text.

### Validation (preview 151370334377)
**Text-only (shipped):** renders; `--noimg` single column; H2-only (no orphan H3); both CTAs **HTTP 200** (`/pages/about-us`, `/pages/freshness-guarantee`); buttons resolve to frozen `tbkx-btn--primary`/`--ghost`; 0 JS; no schema; S1–S5 unaffected.
**With-image (tested then reverted):** desktop split **0.714 = exactly 5/7**; `format=webp` in `src` + `srcset` (500/750/1100w); `loading="lazy"`; **CLS 0 proven structurally** — browser reserved ratio 1.500 from the width/height attributes *before* load, matching rendered ratio exactly. Revert verified.
**Mobile 375px:** 1 column, no overflow, CTA tap targets 48px (≥44), trust points wrap cleanly.

### New backlog
**Craft & studio photography** (folds into Flagship Hero Photoshoot) · **Substantiate the FSSAI claim** — a licence number is public, legally required to display, and converts an unverifiable adjective into checkable proof. Minutes of effort; Trust + GEO value. Not blocking.
- **Risk:** low (additive, preview only). **Rollback:** `git rm sections/home-craft-story.liquid` + remove `home_craft` from `templates/index.json`.


---

## Phase C1 §5–§7 — Homepage Assembly + Custom Cake CTA + Explore **FROZEN v1.0** (2026-07-16) — preview only
Completed the homepage to the **client-ratified conversion-first order** (2026-07-16):
`Hero → Delivery Promise → Occasion Navigation → Best Sellers → Reviews (only if verified) → Custom Cake CTA → Explore → Footer`.

### Three parts
1. **Retired 19 legacy sections** — duplicates of S2/S3/S4, an autoplay marquee (forbidden by the design rules), a carousel mis-headed "Best Seller" that actually showed designer-theme-cakes, and thin custom-liquid blocks.
2. **S7a Custom Cake CTA** (`sections/home-custom-cake-cta.liquid`) — the single custom-cake conversion point; FROZEN `tbk-button` primary + whatsapp; canonical WhatsApp only.
3. **S7b Explore Collections** (`sections/home-explore.liquid`) — theme-axis long-tail discovery; FROZEN `tbkx-pills`; merchandising-safe (skips thin collections).

### ⚠️ Two process failures caught and corrected (recorded honestly)
1. **Reported a push as successful when it had failed.** I truncated the CLI JSON with `head -c 50`, which cut off the `"errors"` key. The push had actually been **rejected**: `order: must have a maximum of 25` — Shopify caps JSON templates at 25 sections, and disabling doesn't free a slot. **Fix:** removed (not disabled) the 19 legacy sections, archived them to `docs/retired-homepage-sections-2026-07-16.json`, and re-pushed. **Lesson: never truncate a push result; grep it for `"errors"`.** All subsequent pushes check for the errors key explicitly.
2. **WhatsApp URL 404'd** — `... | append: s.whatsapp_text | url_encode` made Liquid encode the whole URL, not just the text param, so the href resolved against our own origin. Fixed by encoding the text into its own variable first. Re-verified well-formed.

### Live safety
**The live site was never touched by this phase.** All work is on preview theme 151370334377; live still runs the previous homepage. Nothing was deleted from the store — retired sections are archived and in git history.

### Validation (preview 151370334377)
Rendered order DOM-verified; 0 legacy rendering; footer present; `home_reviews` correctly invisible; both new sections H2-only, 0 JS, no schema; 13/13 internal links HTTP 200; canonical WhatsApp, no legacy number; 11/14 theme pills shown (3 skipped by the live-count filter); mobile 375px clean (no overflow, 56px CTAs, 44px pills).

### Docs
`HOMEPAGE_SPECIFICATION.md` (S7 frozen, ratified order replaces the original 9-section sequence), `docs/retired-homepage-sections-2026-07-16.json` (new archive), this entry.
- **Risk:** low (preview only). **Rollback:** restore `templates/index.json` from git; `git rm` the two new sections.
