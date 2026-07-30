# Audit Changelog

Chronological record of what was actually deployed to the live theme (`151307485353`,
`ae86ba-2a.myshopify.com` / `thebakingkaur.com`), with the deploy-safety evidence for each.

## 2026-07-29 — Commit `52a3821`: remove fabricated ratings and fake customer reviews

**Files**: `sections/main-product-premium-v2.liquid`, `sections/main-product.liquid`,
`sections/main-product-premium.liquid`, `sections/tbk-footer.liquid`, `sections/tbk-product.liquid`.

**Issues closed**: SEO-001 through SEO-006.

**Deploy safety**:
1. `shopify theme pull --only <file>` for each file, into a scratch path.
2. `diff --strip-trailing-cr` against `git show HEAD:<path>` — zero real drift (the CLI's
   line-endings differ from git's checkout, which a plain `diff` misreports as 100% divergence;
   `--strip-trailing-cr` is required for an accurate check).
3. Edited locally, `shopify theme push --allow-live --only <file>` for all 5 files.
4. Re-pulled post-push, diffed against the edited local copies — byte-for-byte match confirmed for
   all 5 files before considering the change live.

## 2026-07-29 — Commit `eaad74f`: remove remaining unverified count claims, fix placeholder contact email

**Files**: `sections/main-product-premium-v2.liquid` (second edit), `sections/site-footer.liquid`,
`templates/page.contact-1.json`, `templates/page.contact-2.json`, `templates/page.our-store.json`.

**Issues closed**: SEO-007, SEO-008, SEO-009, SEO-010, SEO-011, SEO-012.

**Key correction this pass**: `sections/tbk-footer.liquid` (fixed in `52a3821`) turned out not to be
the live footer — `sections/footer-group.json` wires in `site-footer.liquid` instead. The real live
footer still carried the unsourced count claim; fixed here.

**Deploy safety**: identical pull → diff (zero drift) → push `--allow-live` → re-pull → diff-confirm
cycle as above, run against all 5 files in this commit.

## 2026-07-30 — Commit `4d23a2e`: remove duplicate Product schema, gate sitewide FAQPage, fix sameAs

**Files**: `snippets/tbk-schema-website.liquid`, `snippets/structured-data.liquid`,
`sections/main-product-premium-v2.liquid`, `sections/main-product-premium.liquid`,
`layout/theme.liquid`.

**Issues closed**: SEO-020, SEO-023, SEO-024.

**Drift found and reconciled before editing**: `layout/theme.liquid` had diverged from git
independent of this fix — two `render` calls added in commit `011f9be` were absent from the live
theme. Synced local to live truth for this file, then applied only the intended FAQPage-gate edit
on top, so the push carried exactly one change to this file, not an unrelated reintroduction.

**Deploy safety**: identical pull → diff (drift found + reconciled for `theme.liquid`, zero drift on
the other 4) → edit → push `--allow-live` → re-pull → diff-confirm cycle as prior commits, run
against all 5 files.

## 2026-07-30 — Commit `edf458f`: stop lazy-loading the main product gallery image

**Files**: `snippets/tbk-gallery.liquid`.

**Issues closed**: SEO-026 (Core Web Vitals). Also logged, not fixed: SEO-025 (Technical SEO, Low —
a hidden duplicate `<h1>` in `layout/theme.liquid`, needs template-by-template heading verification
before a safe removal).

**Discovery method**: `grep -rc "loading=\"lazy\""` across every section/snippet, then manually
checked whether the *first* image in each product gallery was included in that lazy-loading net —
Google's own guidance is that the LCP image should never be lazy-loaded. Found one real instance
(`tbk-gallery.liquid`, used by the "tbk" product template) and confirmed the actually-live default
template (`product-media.liquid`, all 602 active products) already handles this correctly via a
`lazy_load: false` parameter on the first media item — no fix needed there.

**Deploy safety**: pulled live copy, diffed against last commit (zero drift), pushed
`--allow-live`, re-pulled and confirmed byte-for-byte live.

## 2026-07-30 — Commit `21457ec`: remove demo-store link, typo'd email/phone in mobile header note

**Files**: `sections/header-e-commerce.liquid`, `sections/header-group.json`.

**Issues closed**: SEO-027 (High), SEO-028 (Medium). Also logged, not fixed: SEO-029 (Medium — a
3-way address inconsistency, needs the real current address from the business), SEO-030 (Low — a
fake demo store-locations page, needs a page-scope decision).

**Discovery method**: cross-checking every phone-number occurrence (`grep -rn` for the known real
number) surfaced a file with a *typo'd* email/phone in its schema default — checking whether that
default was actually live (it wasn't; `header-group.json`'s stored settings override it) led to
inspecting the real stored value directly, which turned up a live hyperlink to
`demo-ecomus-global.myshopify.com` — a materially more serious, separate finding than the one that
prompted the check. Lesson: a file's schema `"default"` value is not evidence of what's actually
live; the stored section-group JSON is the only source of truth for that.

**Deploy safety**: pulled live copies of both files, diffed against last commit (zero drift),
pushed `--allow-live`, re-pulled and confirmed byte-for-byte live.

## 2026-07-30 — Verification pass (no code change): hosted Shopify MCP reconnected, real data resolves SEO-017/018

The hosted `claude.ai Shopify` MCP connector came back fully working (28 tools, confirmed via a
live `get-shop-info` test — see `setup/SHOPIFY_MCP_CAPABILITIES.md`). Used it to resolve two
previously-blocked items with real data instead of guesses:

- **SEO-017 resolved**: `{ pages(first: 30) { edges { node { title handle templateSuffix
  isPublished } } } }` confirmed exactly which page templates are actually live —
  `page.contact-2.json` (Contact Us, live), `page.faq-01.json` (FAQ, live),
  `templates/page.store-locations.json` (Store Locator, live). `page.contact-1.json` and
  `page.faq-02.json` are confirmed unused.
- **SEO-018 resolved**: `{ customersCount { count } ordersCount(query: "") { count } }` → 113
  customers, 24 orders — confirms the "20,000+ Happy Customers" claims removed in SEO-007/008/009
  were indeed fabricated.
- **SEO-013 escalated** High → Critical (the Lorem Ipsum FAQ content is confirmed live, not
  hypothetical).
- **SEO-030 escalated** Low → High (the fake Ecomus store-locations page is confirmed live).
- **SEO-031 found** (new, Medium): two live-adjacent policy pages on the same topic
  ("Return, Refund & Replacement Policy" and "Refund & Return Policy") — a genuine duplicate-content
  signal, surfaced by the same page query.

No code was changed this pass — every remaining open item (SEO-013, SEO-016, SEO-029, SEO-030,
SEO-031) needs either real business content or a business decision, not a mechanical fix.

## 2026-07-30 — Live data action: unpublished the fake Store Locator page (SEO-030, user-approved)

Presented the confirmed-live SEO-030 finding directly and asked how to handle it. User chose to
unpublish it as an interim step. Executed via the hosted Shopify MCP:

```graphql
mutation($id: ID!, $page: PageUpdateInput!) {
  pageUpdate(id: $id, page: $page) { page { id title isPublished } userErrors { field message } }
}
```
against `gid://shopify/Page/110839595177`, `{isPublished: false}` — zero `userErrors`. Re-verified
with a fresh `page(id: ...)` read: `isPublished: false` confirmed live.

**Status: Mitigated, not Resolved** — the page and its fake London/Madrid/Tokyo content still
exist, just no longer publicly reachable. The underlying decision (delete the page, repurpose it
for the real Meerut location, or leave it unpublished permanently) is still open.

## Verification queries used (reusable — Admin API confirmed working again as of 2026-07-30)

```graphql
# Confirm live store domain
query { shop { name } }  # via get-shop-info tool

# Confirm a collection's real product count and sample template assignments
query($id: ID!) {
  collection(id: $id) {
    products(first: 8) {
      edges { node { id title handle templateSuffix status } }
    }
  }
}

# Confirm a specific product's SEO title/description fields
query($id: ID!) {
  product(id: $id) { title seo { title description } }
}

# Confirm real product-status counts
{
  active: productsCount(query: "status:active") { count }
  draft: productsCount(query: "status:draft") { count }
  archived: productsCount(query: "status:archived") { count }
}
```

## 2026-07-30 — Verification pass (no code change): SEO-016 header rating already resolved live

Pulled the live theme's `sections/tbk-header.liquid` (`shopify theme pull --theme 151307485353
--only sections/tbk-header.liquid`) and its stored `sections/header-group.json` `tbk_header_main`
block, expecting to find and remove the "★ 4.9 Rated" claim CLAUDE.md's roadmap and this project's
own memory both described as still live and awaiting a go-ahead.

Neither the stored block settings nor a `diff --strip-trailing-cr` against local git turned up any
rating/star/Google-review text. Local git history shows a prior commit, `36e1b0c` ("Header: remove
unverified '4.9 Rated' from mobile drawer trust strip"), predating the current HEAD — it appears
this fix was already live before this audit started, and CLAUDE.md's roadmap item was never updated
to reflect it. **No code change made** — issue closed as already-resolved, not newly fixed.

One unrelated pre-existing drift found in the same diff: the live file has `{%- render 'tbk-tokens'
-%}` (design-tokens integration) that local git's copy lacks. Not touched — out of scope for this
check, logged here so a future sync doesn't mistake it for new drift.

**Lesson**: this project's own memory and CLAUDE.md are not infallible sources for "what's still
open" — always re-verify against the live theme before spending effort on a fix, even for an item
previously logged as confirmed-open.

## 2026-07-30 — Business Decision Implementation pass: FAQ content, header verification, 2 new fixes, 6 new documents

Full detail in [../final/BUSINESS_DECISION_IMPLEMENTATION.md](../final/BUSINESS_DECISION_IMPLEMENTATION.md).
Summary:

**Deployed to the live theme / Admin API this pass** (all pull → diff → edit → push/write → re-pull
→ diff-confirm, per this project's standard deploy-safety pattern):

- **SEO-013** (Critical, Fixed): both FAQ templates (`page.faq-01.json`, live; `page.faq-02.json`,
  unused but kept in sync) rewritten from 12× Lorem Ipsum placeholders to 19 topics of real,
  evidence-based FAQ content. No new schema code needed — `sections/accordion.liquid` already emits
  per-item `Question`/`Answer` Microdata dynamically, so real content flows straight into real
  `FAQPage` structured data.
- **SEO-032** (Critical, Fixed): a fabricated "20,000+ celebrations" claim found on the live
  `/pages/100-percent-eggless-bakery` page body (an Admin API Page, not a theme file — a surface the
  original grep-based sweep never covered) — same pattern as SEO-007/008/009, rewritten via
  `pageUpdate` to drop the invented count.
- **SEO-033** (High, Fixed): broken `tel:+91` (no digits) and `wa.me/91` (no number) links on the
  live Contact page, silently non-functional for every visitor — fixed to the real, already-verified
  phone number.

**Verified, not changed** (already correct before this pass, tracker was stale):

- **SEO-016**: the header "★ 4.9 Rated" claim CLAUDE.md and prior memory both described as still-open
  was already fixed live (commit `36e1b0c`, predating this audit). CLAUDE.md's roadmap and this
  project's memory were both corrected to stop chasing a non-existent defect.

**New findings, documented, not auto-resolved** (each requires a business decision or business
input the model must not guess):

- **SEO-031 escalated Medium → Critical**: the "duplicate policy pages" finding is actually a
  4-way contradiction — Shopify's own built-in Refund/Terms Shop Policies say "no refunds ever,"
  directly opposing the live custom Refund & Return Policy page's 12hr/4hr/5-7-day terms. 3 of 4
  built-in policies also say "The Bakery Kaur" (wrong name). Full detail:
  [../final/POLICY_CONSOLIDATION.md](../final/POLICY_CONSOLIDATION.md).
- **SEO-034** (new, High): the live "Terms and Conditions" custom page has a completely empty body.
- **SEO-035** (new, Medium): two different live delivery-area lists (footer vs. delivery page) agree
  on only 2 of 5 named localities.
- **SEO-036** (new, Medium): the LocalBusiness schema's geo-coordinates and the Shopify Admin
  account's own billing-address coordinates are ~600m apart — two real points, not just one
  unverified one.
- **ADDRESS_AUDIT.md**: full catalogue of 8 address-text sources, 4 distinct wordings, one opening-
  hours conflict (9am vs 10am).

**New planning documents** (`seo-audit/final/`): `ADDRESS_AUDIT.md`, `POLICY_CONSOLIDATION.md`,
`DELIVERY_AREA_SPEC.md`, `EEAT_REPORT.md`, `LOCAL_SEO_ROADMAP.md`, `CONTENT_PLAN.md`,
`BUSINESS_DECISION_IMPLEMENTATION.md` — all evidence-based, none invent a business fact, each states
explicitly where real business input is still needed.

## 2026-07-30 — Sprint 2 task 2.1: wire live header navigation to real collections

**Change type**: Shopify Admin navigation-menu content (`menuUpdate` GraphQL mutation) — **no theme
file was edited**, no `shopify theme push` involved.

**Before, verified**: `main-menu` (the menu actually wired to the live header via
`sections/header-group.json`'s `tbk_header_main.main_menu` setting) had 4 items — HOME, ABOUT US,
CONTACT US, and a generic "Categories" link to `/collections`. A second menu, `header`, already
contained real, correctly-ordered links to all 6 primary collections (Birthday, Anniversary, Diwali
Hampers, Theme Cakes, Hampers, Wedding) but was referenced only by a `disabled: true` section block
(`header_menu_bottom_hulkapps_backup_kgkQBL`), so it rendered nowhere live. Confirmed via a fresh
`menus` GraphQL query and a fresh grep of `header-group.json` immediately before making the change.

**Why**: real customers had no direct navigational path from the header to any of the six primary
collections — every visitor had to click through the generic `/collections` index first. This was
`IMPLEMENTATION_BACKLOG.md` task 2.1 / `ARCHITECTURE_VERIFICATION.md` finding A1.

**Decision** (user-selected, since this is a visible layout change requiring sign-off per this
project's standing convention): Option A — merge the collection links into the existing `main-menu`
rather than re-enabling a second navigation row, per explicit user requirements (preserve mobile-first
nav, single row only, use existing menu architecture, preserve accessibility).

**Implementation**: verified `sections/tbk-header.liquid`'s nav rendering first — a single
`nav.links` loop (used for both mobile and desktop; this theme's header uses one burger-triggered
drawer for all breakpoints, confirmed via the file's own header comment) already renders nested
`link.links` as an accessible native `<details>/<summary>` disclosure with zero additional code. This
meant the entire change could be a content-only menu update: converted `main-menu`'s existing
"Categories" item into a parent with 6 real collection children (same titles/order as the orphaned
`header` menu), using `resourceId` (not hardcoded URLs) so each link auto-resolves and stays correct
if a collection's handle ever changes. HOME/ABOUT US/CONTACT US were passed with their existing item
IDs, unchanged.

**After, re-verified**: a fresh `menu` query post-mutation confirmed `userErrors: []` and all 6 child
URLs auto-resolved correctly (`/collections/birthday-cakes`, `/collections/anniversary-cakes`,
`/collections/luxury-diwali-hampers`, `/collections/designer-theme-cakes`, `/collections/cake-hampers`,
`/collections/wedding-cakes`). Ran `shopify theme check` across the full theme afterward: 1,369
pre-existing offenses across 94 files, none in `tbk-header.liquid` or `header-group.json` (confirmed
via grep) — expected, since zero theme files were touched by this change; not a regression.

**Scope discipline**: no other navigation, header functionality, or unrelated site area was touched,
per explicit instruction.

## 2026-07-30 — Sprint 2 task 2.4: remove broken link from `about-us-menu`

**Change type**: Shopify Admin navigation-menu content (`menuUpdate`) — no theme file edited.

**Before, verified**: fresh `menu` query on `about-us-menu` (id `gid://shopify/Menu/230113444009`)
showed 3 items — About Us, Contact Us, and "Store Locations" pointing at
`/pages/store-locator` (`gid://shopify/Page/110839595177`), reconfirmed unpublished this pass.

**Why**: this menu isn't confirmed wired to any live section, but if it's ever activated, the third
item would 404 — a fake, already-unpublished London/Madrid/Tokyo demo page (SEO-030). Preventive fix,
per `IMPLEMENTATION_BACKLOG.md` task 2.4 / `NAVIGATION.md` §5.

**After, re-verified**: fresh re-query shows 2 items only (About Us, Contact Us), `userErrors: []`.

## 2026-07-30 — Sprint 2 task 2.2 (partial): populate the empty `meerut-delivery` menu

**Change type**: Shopify Admin navigation-menu content (`menuUpdate`) — no theme file edited.

**Before, verified**: fresh `menu` query on `meerut-delivery` (id `gid://shopify/Menu/237291765929`)
confirmed 0 items. Fresh `pages` queries confirmed all 3 target pages exist and are published:
`cake-delivery-in-meerut`, `midnight-cake-delivery`, `30-minute-cake-delivery-in-meerut-premium-reliable-service`.

**Why**: this menu shell exists (apparently created for exactly this purpose, per
`NAVIGATION.md`/`SITE_TREE.md`'s earlier finding) but was never populated. The full Delivery Areas
hub item is blocked on Sprint 1 (SEO-030/SEO-035), but the 3 existing delivery-mode pages need no
business decision to link — a partial implementation, not the full task.

**After, re-verified**: fresh re-query shows 3 items, `userErrors: []`, all URLs resolved correctly.

**Explicitly not done, and explicitly out of Sprint 2 scope**: adding the future Delivery Areas hub
item (blocked on Sprint 1), and surfacing this menu in any live section (a visible layout change of
the same kind task 2.1 required sign-off for — not bundled into this content-only step).

## 2026-07-30 — Sprint 2 task 2.6: add missing FAQ/delivery/eggless cross-links

**Change type**: 2 Admin API `pageUpdate` calls (Page bodies) + 1 theme push (2 template files).

**Before, verified**: fresh `page` queries on `cake-delivery-in-meerut` and
`100-percent-eggless-bakery` confirmed neither linked to `/pages/frequently-asked-questions-faqs`
anywhere in their body, despite both being topically adjacent (each has its own smaller on-page FAQ
section). Fresh theme pull of `page.faq-01.json` confirmed zero drift before editing.

**Why**: `LOCAL_SEO_ROADMAP.md` §8 and `INTERNAL_LINKING.md` both flagged the FAQ page as reachable
only via the header, with no inbound links from the pages most likely to send a reader looking for
more detail. Per `IMPLEMENTATION_BACKLOG.md` task 2.6.

**Implementation**: added one sentence with a link to the FAQ page at the end of each page's existing
on-page mini-FAQ (via `pageUpdate`, no other content changed). For the reverse direction, checked
`sections/accordion.liquid` first to confirm how "title" divider blocks render (plain `<h5>` text, no
existing link precedent) versus how accordion-item answers already handle inline links (the FAQ
page's own Refund/Cancel answers already link to the Refund policy page from prose) — added the 3
topic links (Delivery → `cake-delivery-in-meerut`, Eggless → `100-percent-eggless-bakery`, Hampers →
`gift-hampers`) within the matching Q&A answer text, matching that existing pattern, in both
`page.faq-01.json` (live) and `page.faq-02.json` (unused, kept in sync per this project's established practice).

**After, re-verified**: both `pageUpdate` calls returned `userErrors: []`. Theme push followed the
standard pull → diff (zero drift) → push → re-pull → diff pattern; both files confirmed byte-for-byte
live.

## 2026-07-30 — Sprint 2 task 2.7: cross-link the hamper page cluster

**Change type**: 4 Admin API `pageUpdate` calls (Page bodies) — no theme file involved.

**Before, verified**: fresh `page` queries on all 4 hamper pages (`gift-hampers`,
`customised-hampers-meerut`, `festive-hampers-meerut`, `surprise-hampers-meerut`) confirmed the
`INTERNAL_LINKING.md` finding that was previously marked "not verified": none of the three
location-specific pages linked to the hub (`/pages/gift-hampers`) or to each other, and the hub
itself didn't link to any of the three.

**Why**: per `INTERNAL_LINKING.md`'s Hampers cluster recommendation and `IMPLEMENTATION_BACKLOG.md`
task 2.7 — these four pages cover closely related, non-overlapping ground (general hampers, custom-
built, festival-timed, surprise-timed) but a reader on any one of them had no way to discover the
other three.

**Implementation**: added one sentence with 2 links (to the hub + the two other siblings, not itself)
at the end of each of the 3 location-specific pages' existing closing paragraph. Added a new "Explore
by Occasion" section to the hub page linking to all 3 siblings, placed before the existing "Related
Collections" section (left untouched — see task 2.8 for that separate fix).

**After, re-verified**: all 4 `pageUpdate` calls returned `userErrors: []`; a fresh re-query of all 4
pages confirmed the new links are present and correctly targeted.

## 2026-07-30 — Sprint 2 task 2.8: convert Gift Hampers' "Related Collections" to real links

**Change type**: 1 Admin API `pageUpdate` call (Page body) — no theme file involved.

**Before, verified**: fresh `page` query on `gift-hampers` confirmed its "Related Collections" section
was 6 plain `<li>` text items (Birthday Cakes, Anniversary Cakes, Designer Cakes, Wedding Cakes,
Flowers & Cake Combos, Midnight Delivery) with no `<a>` tags anywhere in that block.

**Why**: the richest, best-built page on the site was sending zero internal link equity to 6 directly
relevant collections. Per `INTERNAL_LINKING.md` and `IMPLEMENTATION_BACKLOG.md` task 2.8.

**Implementation**: wrapped each of the 6 items in an `<a href>` to its matching live collection
(`/collections/birthday-cakes`, `/collections/anniversary-cakes`, `/collections/designer-theme-cakes`,
`/collections/wedding-cakes`, `/collections/flowers-cake-combos`, `/collections/midnight-cake-delivery`)
— text labels unchanged, only wrapped in links. No judgment made here about whether
`midnight-cake-delivery` should remain a distinct collection long-term (that's the Sprint-1-gated
duplicate-cluster decision, out of this task's scope) — linked to whatever collection currently and
correctly matches the existing page text.

**After, re-verified**: `pageUpdate` returned `userErrors: []`; fresh re-query confirms all 6 links present.

## 2026-07-30 — B3 (partial): unify address/geo across 5 theme files (SEO-015/029/036)

**Change type**: 5 theme files, deployed via `shopify theme push` — no Admin API involved (unlike
every prior pass this project, since the Shopify MCP connector disconnected mid-session with no
fallback `SHOPIFY_TOKEN` configured; confirmed via `env | grep -i shopify` and a check of
`seo-ops/`'s existing token-based path, both empty).

**Before, verified**: fresh `shopify theme pull` + `diff --strip-trailing-cr` against git HEAD
confirmed zero drift on all 5 files before editing: `snippets/bk-local-business.liquid` (typo'd
"Fatah Complex," coordinates 28.9931/77.6939), `snippets/tbk-schema-website.liquid` (no
`streetAddress`/`geo` at all), `sections/site-footer.liquid` (schema default, same typo),
`sections/footer.liquid` and `sections/tbk-footer.liquid` (hardcoded, same typo, 3 occurrences total).

**Why**: per the approved B3 decision (`BUSINESS_DECISION_GUIDE.md`) — use the Shopify Admin billing
address as the base text and coordinates, since it's the merchant's own account-of-record.

**Additional real evidence found this pass, not previously known**: `sections/footer.liquid` line 90
contains a real, pre-existing Google Maps share link
(`https://maps.app.goo.gl/LmD25vZFZYQL3TTd6`) that had never been resolved before. Resolving it
(`WebFetch`) revealed a genuine Google Business Profile listing for this exact business — *"The
Baking Kaur | Premium Bakery and Cake Shop..."* — with address text ("Fateh Complex, 390/1, Lane
Number 7, opposite Ice Factory... Thapar Nagar, Lajpat Bazaar, Thapar Nagar, Meerut, Uttar Pradesh
250001") that closely corroborates the Shopify Admin billing address independently. Its exact decimal
coordinates could not be extracted — Google Maps place pages are JS-rendered and neither `WebFetch`
nor a CID-based URL (`google.com/maps?cid=<decimal>`, converted from the place ID's hex) returned
usable coordinate data. This is a real tooling limit, not a decision to skip it.

**Implementation**: `streetAddress` updated to "Fateh Complex, 390/1, Lane Number 7, opposite Ice
Factory, Thapar Nagar Gali Number 7 Lajpat Bazaar Thapar Nagar" (the Admin billing address's `address2`
+ `address1` fields, concatenated as stored, not editorially cleaned up) in both schema files;
coordinates updated to 28.9897017 / 77.7044604 (Admin billing address) in both; `tbk-schema-website.liquid`
gained a `streetAddress`/`geo` block it previously lacked entirely, closing the Organization/Bakery
schema-coverage gap noted in `ADDRESS_AUDIT.md`. The three footer files' address text updated to match
(with reasonable length compression for the two prose/short-label contexts, same underlying facts).
`bk-local-business.liquid`'s in-code warning comment rewritten to record the new source and remaining caveat.

**After, re-verified**: pushed via `shopify theme push --allow-live`; re-pulled and
`diff --strip-trailing-cr` confirmed byte-for-byte live on all 5 files; `shopify theme check` run
across the full theme afterward — 1,369 pre-existing offenses across 94 files, identical count to the
prior baseline, none in the 5 touched files (confirmed via grep) — no regression.

**Not done this pass, blocked**: the Refund & Return Policy page body's address mention and the
Shopify Admin Contact Information Shop Policy both need the same update but are Admin-API-only
surfaces, unreachable without the MCP connector or a configured `SHOPIFY_TOKEN`. A literal
human-confirmed fresh Google Maps pin-drop (this pass's real Maps-listing discovery corroborates the
address text but not exact coordinates) is still recommended as a follow-up.

**B1, B2, B4, B5, B6 status this pass**: not executed. B1/B2 require Admin API (Shop Policy and Page
body edits) — blocked by the same tooling issue. B4 and B5 require actual business
input (a confirmed delivery-area list; specific merchandising picks for the collection cluster) that
wasn't supplied along with the approval — executing either would mean guessing, which this project's
standing rule forbids. B6 is explicitly sequenced after B4. See `IMPLEMENTATION_SUMMARY.md` for full detail.

## Related

[AUDIT_LEDGER.md](AUDIT_LEDGER.md), [VERIFIED_ISSUES.md](VERIFIED_ISSUES.md).
