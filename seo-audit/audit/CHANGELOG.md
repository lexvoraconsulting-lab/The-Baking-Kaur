# Audit Changelog

Chronological record of what was actually deployed to the live theme (`151307485353`,
`ae86ba-2a.myshopify.com` / `thebakingkaur.com`), with the deploy-safety evidence for each.

## 2026-07-30 — Sprint 1 re-verification pass (Phase 4): no new implementation

Re-checked Sprint 1's status under the full canonical hierarchy (`business/BUSINESS_MASTER.md` →
`TBK_BRAND_GUIDELINES.md` → `design/*` → `IMPLEMENTATION_BACKLOG.md`). Confirmed the Shopify MCP
connector is still disconnected and no `SHOPIFY_TOKEN` fallback is configured — Sprint 1's remaining
tasks (B1, B2, B4, B5, B6) are unchanged from the last pass, blocked for the same reasons. Re-pulled
B3's 5 previously-corrected files (`bk-local-business.liquid`, `tbk-schema-website.liquid`,
`site-footer.liquid`, `footer.liquid`, `tbk-footer.liquid`) and confirmed all still byte-for-byte live.

**One real finding this pass**: the Shopify CLI briefly failed with a DNS-resolution error
(`getaddrinfo ENOTFOUND accounts.shopify.com`) on first attempt — confirmed transient via direct
`curl` checks (the host resolved normally moments later) and a successful retry. Not a new standing
blocker; noted for the record since it briefly looked like one.

No file changed, no commit made for this entry — see `seo-audit/final/SPRINT_REPORT.md` for full detail.

## 2026-07-31 — R0: restore design-token/component rendering in `layout/theme.liquid`

**Files**: `layout/theme.liquid` only.

**What was broken**: `snippets/tbk-tokens.liquid` (the real `--tbk-*` CSS custom-property system) and
`snippets/tbk-components.liquid` (the real `.tbkx-*` component CSS) were rendered only by
`layout/password.liquid` — confirmed via a repo-wide grep, the only two `render 'tbk-tokens'` /
`render 'tbk-components'` calls anywhere were both in that one file. `layout/theme.liquid`, which
renders every real storefront page, had neither. Three confirmed-live sections
(`sections/tbk-header.liquid`, `sections/site-footer.liquid`, `sections/tbk-announcement-bar.liquid`)
reference `var(--tbk-*)` 177 times combined, all previously resolving to nothing on any real page —
masked entirely by the storefront's own password gate, since anonymous/external checks only ever saw
`password.liquid`. Full detail: `docs/LIQUID_ARCHITECTURE_AUDIT.md` Finding 0.

**Why the fix is safe**: purely additive — two `render` statements added to the existing
`{%- liquid ... -%}` head block, copied from the exact working order already proven correct in
`password.liquid` (immediately after `render 'css-variables'`). No existing render call, CSS value,
or markup was touched. Confirmed zero pre-existing `tbk-tokens`/`tbk-components` calls in
`theme.liquid` before editing — nothing duplicated.

**Deploy safety**: `shopify theme pull --only layout/theme.liquid`, `diff --strip-trailing-cr`
against git HEAD — zero drift confirmed before editing. Pushed via
`shopify theme push --allow-live --only layout/theme.liquid`. Re-pulled and diff-confirmed
byte-for-byte live, both new `render` lines present.

**Verification — Theme Check, full run, before vs. after**:

| Metric | Before | After |
|---|---|---|
| Total offenses | 1,369 | 1,367 (**−2**) |
| Files flagged | 94 | 92 (**−2**) |
| Errors | 1,162 | 1,162 (unchanged — no new errors) |
| Warnings | 207 | 205 (**−2**) |

The exact 2 fewer offenses/files are `tbk-tokens.liquid` and `tbk-components.liquid`'s
`OrphanedSnippet` findings — both completely absent from the new report (confirmed via grep, zero
mentions of either name), proving Theme Check now sees them as reachable. `layout/theme.liquid`
itself carries zero findings. No regression.

**Not done this pass, per explicit scope**: R1 (removing the confirmed-dead `-hulkapps-backup`
files) and every later phase in `docs/LIQUID_ARCHITECTURE_AUDIT.md`'s plan — R0 only.

## 2026-07-31 — R1: remove 10 confirmed-dead `-hulkapps-backup` files

**Files removed**: `sections/cart-drawer-hulkapps-backup.liquid`,
`sections/header-e-commerce-hulkapps-backup.liquid`, `sections/header-inline-hulkapps-backup.liquid`,
`sections/main-cart-hulkapps-backup.liquid`, `sections/main-gift-cart-hulkapps-backup.liquid`,
`snippets/cart-checkbox-hulkapps-backup.liquid`, `snippets/cart-complementary-hulkapps-backup.liquid`,
`snippets/cart-shipping-bar-hulkapps-backup.liquid`, `snippets/item-cart-hulkapps-backup.liquid`,
`snippets/item-cart-page-hulkapps-backup.liquid` — 3,319 lines total. Full rationale per file already
documented in `docs/LIQUID_ARCHITECTURE_AUDIT.md` Finding 1, re-verified fresh immediately before
deletion (all 10 still showed zero references via a repo-wide grep across every `*-group.json`/
`templates/*.json`, and the 5 snippets were independently confirmed by Theme Check's own
`OrphanedSnippet` detector).

**Explicitly excluded from this pass**: `snippets/rewind_menu_backup_do_not_delete.liquid` (filename
is a literal do-not-delete instruction) and `sections/header-menu-bottom-hulkapps-backup.liquid`
(referenced once, as a `disabled: true` block in `header-group.json` — live-but-inactive
configuration, not orphaned code; deferred to R2, a separate decision).

**Real, unrelated drift found and deliberately routed around**: a full-theme pull (all 365 files)
before deletion, diffed against git HEAD, surfaced 3 pre-existing drifts unrelated to this task:
`layout/password.liquid` and `sections/tbk-header.liquid` (live already renders `tbk-tokens` in
places local git didn't have — `tbk-header.liquid`'s copy in particular means the header's 145
`var(--tbk-*)` references were likely already resolving correctly on real pages even before R0,
independent of R0's fix) and `sections/main-password.liquid` (live has a real WhatsApp/Call-Now
button block entirely absent from local git). An unscoped `theme push` (Shopify CLI's default
behavior deletes remote files not present locally) would have silently pushed local's version of all
three over live, adding unintended content to `password.liquid` and **deleting the live WhatsApp/Call
feature from `main-password.liquid`**. Deployed via `theme push --only <path>` named explicitly for
each of the 10 files instead, avoiding an unscoped sync entirely.

**Deploy safety**: deleted the 10 files locally, pushed with 10 explicit `--only` flags (not an
unscoped push), then a full-theme re-pull confirmed: all 10 gone remotely; all 3 unrelated drifted
files unchanged (`main-password.liquid` still has its WhatsApp/Call block; `tbk-header.liquid` still
has its inline `tbk-tokens` render; `password.liquid`'s drift unchanged). A separate repo-wide grep
post-deletion confirmed zero dangling references to any of the 10 removed files.

**Verification — Theme Check, two independent runs, both identical**:

| Metric | Before R1 (post-R0) | After R1 |
|---|---|---|
| Files inspected | 365 | 355 (**−10**, exactly the removed files) |
| Total offenses | 1,367 | 1,362 (**−5**) |
| Files flagged | 92 | 87 (**−5**) |
| Errors | 1,162 | 1,162 (unchanged — no new errors) |
| Warnings | 205 | 200 (**−5**) |

No regression. R2 through R7 not started, per explicit scope.

## 2026-07-31 — R2: investigate `header-menu-bottom-hulkapps-backup.liquid`, decision: KEEP

**Files changed**: none — documentation only.

**Task**: R1 explicitly excluded this file from the confirmed-dead cleanup, since (unlike the 10
files removed there) it has a real reference. This pass investigated it fully to reach a disposition.

**Evidence gathered**:
- Repo-wide grep for `header-menu-bottom-hulkapps-backup` / `header_menu_bottom_hulkapps_backup`
  across every `.liquid`/`.json` file: the **only** occurrences anywhere are in
  `sections/header-group.json` — a block definition
  (`"header_menu_bottom_hulkapps_backup_kgkQBL": { "type": "header-menu-bottom-hulkapps-backup", ...
  "disabled": true, ... }`, lines 180-246) and its entry in the group's `"order"` array (line 253).
- The block's own settings: `main_menu: "header"` (the orphaned 6-collection linklist — its purpose
  already superseded, since R0/Sprint 2 already merged those 6 collections into the *active*
  `main-menu`) and a `note_mobile` field carrying the pre-B3 stale address format.
- `shopify theme check` flags this file with only a minor `HardcodedRoutes` warning — **not**
  `OrphanedSnippet` or any unused-code category, confirming Theme Check itself recognizes it as
  referenced, not dead.
- Shopify's standard section-group behavior: a block with `disabled: true` is skipped at render time
  — confirmed this block causes no live rendering, no error, and no customer-facing effect today.

**Classification**: Disabled, Legacy, Referenced (not orphaned), Not required (its function is
already served elsewhere), **not safely removable as a simple file deletion** — its `.liquid` file is
referenced by a live block/order entry in `header-group.json`, the same file that defines the
currently-active header. Removing the file alone would leave a dangling section-type reference in an
active, shared configuration file. Removing it correctly would require also editing the
block/order entries out of `header-group.json` — a materially bigger, riskier change than R1's clean
deletions, on the file most sensitive to a mistake right now (it also carries R0/Sprint 2's live
header changes).

**Decision: KEEP.** The block is already fully inert (disabled, no render, no error) — leaving it
carries zero live risk. Removing it would require a live edit to `header-group.json` for a purely
cosmetic benefit. Not worth the risk-to-benefit ratio for this pass. If a future pass wants to remove
it, the correct sequence is: (1) delete the `header_menu_bottom_hulkapps_backup_kgkQBL` block object
and its `order` entry from `header-group.json`, verified via the same pull→diff→push→re-pull cycle
used throughout this project, (2) confirm no other block references the same section type, (3) only
then delete `sections/header-menu-bottom-hulkapps-backup.liquid` itself.

**Verification**: `git status` confirmed clean (no file touched) both before and after this
investigation; Theme Check re-run showed no change from R1's post-cleanup baseline.

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
live `get-shop-info` test — see `docs/setup/SHOPIFY_MCP_CAPABILITIES.md`). Used it to resolve two
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

## 2026-07-31 — R3: exhaustive product-template census (audit only, no files removed)

**Files**: `docs/TEMPLATE_CENSUS.md` (new). No theme file changed.

**What was done**: paginated the entire 1,235-product catalogue (`sortKey: ID`, cursor pagination,
250/page) for `templateSuffix`, superseding Finding 2's ~100-product sample from the Phase 5 audit.
Confirmed `template_suffix:` is not a real Shopify search filter (empirically — a filtered query
silently returns the full unfiltered count — and via `search_docs_chunks`, absent from the
documented field list), so exhaustive pagination was the only reliable method.

**Result** (sums to exactly 1,235, cross-checked against `productsCount` before and after):
default `product.json` (`null`/`""`) — 1,228; `product.premium.json` — 3; `product.hampers-template.json`
— 4; `product.tbk.json` — 0; `product.only_config.json` — 0 (by design, see below).

**Zero-usage templates verified twice each, per the required standard**:
- `product.only_config.json` is **not orphaned** — it's Shopify's alternate-template mechanism for
  quick-view/quick-add modals, gated on `template == 'product.only_config'` in
  `sections/main-quick-view.liquid`, `sections/main-quick-add.liquid`, and `layout/theme.liquid`,
  and reached via `assets/global.min.js`'s `view=only_config` query-string convention — a path the
  `templateSuffix` census cannot and isn't meant to detect. Not a cleanup candidate.
- `product.tbk.json` / `sections/tbk-product.liquid` has zero assignments and, unlike
  `only_config`, no alternate-view wiring anywhere in the theme. Its own header comment describes
  manual single-product assignment that evidence shows never happened. Marked **SAFE TO REMOVE**
  in the census doc, with one residual caveat (installed-app references aren't inspectable from
  this environment) — **not removed this phase**, per R3's explicit audit-only scope.

**Verification**: `git status` clean except the new doc; Theme Check re-run for a fresh baseline
(no theme file touched, so no regression is possible by construction). Full detail, matrix, and
reference-check evidence: `docs/TEMPLATE_CENSUS.md`.

## 2026-07-31 — R3.5: remove `templates/product.tbk.json` (the one file R3 proved safe)

**Files**: `templates/product.tbk.json` only (deleted). `sections/tbk-product.liquid` deliberately
left in place — out of scope for this phase.

**Before, re-verified from scratch** (not reused from R3): fresh full pagination of all 1,235
products (`sortKey: ID`, cursor pagination, 250/page, 5 pages) — 0 `templateSuffix: "tbk"`
assignments, matching R3 exactly (1,228 default / 3 `premium` / 4 `hampers-template` / 0 `tbk`).
Catalogue totals unchanged (1,235 total, 602/588/45 active/draft/archived split) — no concurrent
edits. Grep re-confirmed: no `view=tbk` or `template == 'product.tbk'` gate anywhere (unlike
`only_config`, which has real alternate-view wiring); no other template/section references
`tbk-product`; `assets/base.css`'s `.tbk-product-*` classes are a naming convention shared with
`main-product-premium.liquid`/`-v2.liquid`, not a dependency on this template file specifically.
App-level references remain unverifiable from this environment (disclosed caveat, not a blocker —
no evidence of app usage found).

**Why safe to remove**: zero live product assignments (exhaustive, twice-verified), zero alternate
rendering path, zero references from any other theme file. `templates/product.tbk.json` only
declares which section (`tbk-product`) to render for an assigned product — with the assignment
never made, the JSON file itself has no function.

**Deploy safety**: `shopify theme pull --only templates/product.tbk.json` + `diff --strip-trailing-cr`
against local — zero drift confirmed before deleting. Deleted locally, then
`shopify theme push --allow-live --only templates/product.tbk.json --force` (scoped, not an
unscoped sync — same deliberate pattern as R1). Re-pulled `templates/product*.json` afterward:
confirmed `product.tbk.json` gone live; the other 4 product templates
(`product.json`, `product.premium.json`, `product.hampers-template.json`, `product.only_config.json`)
unchanged.

**After — Theme Check**: 354 files inspected (was 355 in R3, exactly -1) — 1,362 offenses across 87
files, 1,162 errors, 200 warnings, identical to R3's baseline. No new offense introduced; the
removed file itself carried none.

**Not removed this phase**: `sections/tbk-product.liquid` — explicitly out of scope per this
phase's instruction ("remove ONLY templates/product.tbk.json"). Its own future disposition (R4+)
depends on the still-unverifiable app-reference check.

## 2026-07-31 — R4: orphan snippet verification & risk classification (audit only)

**Files**: `docs/ORPHAN_SNIPPET_AUDIT.md` (new). No theme file changed.

**What was done**: reviewed all 17 files in scope (Finding 3's 14 real orphan-snippet candidates +
Finding 4's 3 zero-reference numbered-variant sections), re-verifying every one via direct
`render`/`include`/section-type grep rather than trusting Theme Check's `OrphanedSnippet` label.

**Critical methodology finding — Theme Check's orphan detector is unreliable in both directions**:
- **4 files falsely flagged orphaned, actually live**: `product-form-bundle.liquid`,
  `product-form-bundle2.liquid`, `product_tabs.liquid` (all 3 rendered by all 3 product templates,
  including the default, protected `main-product-premium-v2.liquid` used by 1,228/1,235 products),
  and `cake-addons.liquid` (rendered by 2 of 3 product templates). All 4 reclassified **ACTIVE** —
  none touched.
- **1 file falsely counted as referenced, actually dead**: `shine-trust.liquid` is called via
  `layout/theme.liquid:201`'s `{% include 'shine-trust.liquid' %}` — passing the snippet name
  *with* the `.liquid` extension, which Liquid resolves to the non-existent
  `snippets/shine-trust.liquid.liquid`. The include silently fails; the 78KB snippet has never
  rendered. Independently corroborated by a pre-existing, already-documented, never-resolved
  finding: `SEO_AUDIT_LEDGER.md`'s **P2-26** (2026-07-18, `MissingTemplate`, "OWNER INPUT REQUIRED
  (decide on/off)").

**Fabrication-risk review** (explicit focus: reviews, ratings, trust badges, testimonials,
counters, customer numbers, awards, schema): **none found** in any of the 17 files.
`shine-trust.liquid` is CSS-only bundle/"sold out" widget styling, no claims. `testimonials-2.liquid`
/ `testimonials-3.liquid` carry `"disabled_on": {"groups": ["*"]}` (Shopify-level lockout) and only
generic Ecomus fashion-demo placeholder copy, never added to any live section group. Two bonus,
directly relevant discoveries surfaced while tracing the newly-reclassified-ACTIVE
`product_tabs.liquid`: its live `tab_review` case renders `hdt-pr-single-review.liquid`, which is
empty (0 bytes) — so the review tab is inert even when configured; and `hdt-pr-card-rating.liquid`
(rendered by ~19 live card components, gated on `settings.show_rating: true`) is entirely a
documentation comment listing third-party review-app integration instructions — it renders nothing.
Both confirm zero fabricated or real rating content currently reaches the storefront, consistent
with `REVIEW_STRATEGY.md`.

**Classification result**: 4 ACTIVE (not touched) · 2 MANUAL REVIEW (`bk-datetime.liquid` — a real,
bespoke, brand-styled delivery date/time-slot feature with a documented but unimplemented
integration plan; `shine-trust.liquid` — pre-existing unresolved on/off decision) · 11 SAFE TO
REMOVE (confirmed zero references, zero fabrication risk, zero business decision needed) — **none
removed this phase**, per audit-only scope.

**Verification**: `git status` clean except the new doc; Theme Check re-run for a fresh baseline
(no theme file touched, so no regression is possible by construction). Full matrix, evidence, and
recommended cleanup order: `docs/ORPHAN_SNIPPET_AUDIT.md`.

## 2026-07-31 — R5: remove the 11 verified-safe orphan snippets

**Files**: 11 files removed (8 snippets, 3 sections). `bk-datetime.liquid` and `shine-trust.liquid`
(R4's 2 manual-review items) deliberately left untouched.

```
snippets/hdt-pr-single-rating.liquid   snippets/delivery-date.liquid
snippets/meta-tags.liquid              snippets/type.liquid
snippets/product-btns.liquid           snippets/product-thumbnail.liquid
snippets/choose_style.liquid           snippets/lookbook-card-product.liquid
sections/testimonials-2.liquid         sections/testimonials-3.liquid
sections/video-2.liquid
```

**Before, re-verified independently a second time** (not reused from R4): fresh repo-wide grep for
`render`/`include`/section-type references to all 11 files — zero hits on every one, confirming
R4's finding still holds. `meta-tags.liquid` reconfirmed a duplicate of the live
`social-meta-tags.liquid`; `testimonials-2.liquid`/`testimonials-3.liquid`/`video-2.liquid`
reconfirmed carrying `"disabled_on": {"groups": ["*"]}` with only generic Ecomus demo content.

**Deploy safety**: `shopify theme pull --only <11 paths>` + `diff --strip-trailing-cr` against
local for each file — zero drift confirmed on all 11 before deleting. Deleted locally, then
`shopify theme push --allow-live --only <11 paths> --force` (scoped, not an unscoped sync — same
deliberate pattern as R1/R3.5). Re-pulled the full `snippets/`/`sections/` directories afterward:
confirmed all 11 gone live; confirmed `bk-datetime.liquid` and `shine-trust.liquid` byte-for-byte
unchanged.

**After — Theme Check**: 343 files inspected (was 354, exactly −11) — 1,351 offenses across 80
files, 1,162 errors (unchanged), 189 warnings (was 200, exactly −11 — each removed file carried
exactly one `OrphanedSnippet` warning). No new offense introduced; no regression.

**Repository grep, post-removal**: no remaining `render`/`include` call anywhere references any of
the 11 removed files — no broken includes.

**Not removed this phase**: `bk-datetime.liquid` (real, unfinished, brand-styled feature — needs a
product decision) and `shine-trust.liquid` (pre-existing, unresolved on/off decision, `SEO_AUDIT_LEDGER.md`
P2-26) — both explicitly out of scope per this phase's instruction.

## 2026-07-31 — R6: repair the one verified missing-asset reference

**Files**: `assets/no-image.svg` (new — a plain, generic gray placeholder icon; no business claims,
no fabrication risk).

**Full scan performed** (Theme Check JSON output, parsed programmatically): 8 `MissingAsset`
findings total, 1 `MissingTemplate`, 3 `UnknownFilter`, 3 `DuplicateRenderSnippetArguments`, 1
`ValidJSON`. Each was independently triaged against R6's "deterministic, low-risk, fully verified,
asset/reference only" mandate:

| Finding | Verdict | Why |
|---|---|---|
| `assets/no-image.svg` missing, referenced by `snippets/tbk-gallery.liquid:7` | **Repaired** | Deterministic, purely additive, zero fabrication risk. This is the audit's own Finding 6, explicitly reserved for R6. |
| 6× `MissingAsset` under `design_handoff_shopify_product/theme_files/` | Not touched | Non-live reference/handoff folder, outside the theme's actual root (`sections/`, `snippets/`, `templates/`, `assets/`, `layout/`, `config/`) — Finding 5, already established out of scope for this whole refactor plan. |
| `MissingTemplate`: `layout/theme.liquid:200`'s broken `{% include 'shine-trust.liquid' %}` | Not touched | Pre-existing, unresolved business decision (`SEO_AUDIT_LEDGER.md` P2-26; R4/R5 manual-review item) — fixing it visibly changes every page (78KB of CSS turns on), not a deterministic/low-risk repair. |
| 3× `UnknownFilter 'limit'` in `sections/tbk-product.liquid` | Not touched | A Liquid logic bug, not an asset/reference issue — out of R6's scope. Also moot: `tbk-product.liquid` has had zero live rendering path since R3.5 removed its only assigning template (`product.tbk.json`), confirmed via grep (`"type": "tbk-product"` appears nowhere in any live template/section-group). |
| 3× `DuplicateRenderSnippetArguments` in `sections/main-list-collections.liquid` (a live file) | Not touched | Redundant-but-not-broken render argument — a code-quality issue, not a missing/broken reference; "do not refactor unrelated code" per this phase's instruction. |
| `ValidJSON` in `locales/en.default.schema.json:4957` | Not touched | A locale/schema-labels structural issue — explicitly excluded ("do not modify schema content... copy"). |

**Deploy safety**: pulled to confirm the asset was genuinely absent live, added the file locally,
pushed via a scoped `--only assets/no-image.svg` push, re-pulled and diff-confirmed byte-identical.

**After — Theme Check**: 343 files (unchanged — a new asset isn't a liquid/json file counted the
same way), 1,350 offenses (was 1,351, −1) across 80 files, 1,161 errors (was 1,162, −1, exactly the
resolved `MissingAsset`), 189 warnings (unchanged). No new offense introduced.

**Repository grep**: `assets/no-image.svg` now resolves correctly wherever referenced;
`snippets/tbk-gallery.liquid`'s `{{ 'no-image.svg' | asset_url }}` now points at a real file. No
other broken `render`/`include`/`asset_url`/`image_url`/`file_url` reference remains in scope.

## Related

[AUDIT_LEDGER.md](AUDIT_LEDGER.md), [VERIFIED_ISSUES.md](VERIFIED_ISSUES.md).
