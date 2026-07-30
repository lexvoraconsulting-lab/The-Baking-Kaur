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

## Related

[AUDIT_LEDGER.md](AUDIT_LEDGER.md), [VERIFIED_ISSUES.md](VERIFIED_ISSUES.md).
