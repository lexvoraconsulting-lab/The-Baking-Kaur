# Component Library

**Canonical hierarchy**: `business/BUSINESS_MASTER.md` → `business/TBK_BRAND_GUIDELINES.md` →
`DESIGN_SYSTEM.md` → this document. Documents every real, currently-live component this pass could
confirm, plus components that exist as files but are **not confirmed wired to a live section** —
labeled explicitly, never conflated. No new component is proposed here; this is inventory, not design.

---

## Header

**File**: `sections/tbk-header.liquid`. **Live**: yes, via `tbk_header_main` block in
`sections/header-group.json`. Single burger-triggered drawer navigation used for **both** mobile and
desktop (confirmed via the file's own header comment: "Desktop: [Burger \| Logo]... Mobile: [Burger \|
Logo...]") — there is no separate horizontal desktop nav bar. Renders `linklists[s.main_menu]`
(currently `main-menu`, per `header-group.json`'s stored setting). Nested menu items render as native
`<details>/<summary>` disclosures inside the drawer — real, accessible, no JS-only accordion. As of
2026-07-30 (Sprint 2), `main-menu` includes a "Categories" item with 6 real collection children
(Birthday, Anniversary, Diwali Hampers, Theme Cakes, Hampers, Wedding). A second menu (`header`, 6
real collection links) and a disabled two-tier bottom-nav block (`header_menu_bottom_hulkapps_backup`)
exist but are **not live** — do not treat them as the current header state.

## Footer

**File**: `sections/site-footer.liquid`. **Live**: yes, confirmed via `footer-group.json`. Hardcodes
its own links rather than rendering the (unused) `footer` linklist. Real, current known defects (per
`BUSINESS_MASTER.md` §9/§13, both blocked on B1/B2): Refund link falls through to the uncorrected Shop
Policy; Terms link (2 occurrences, one unconditional) points at the still-empty custom Terms page.
FAQ is currently absent from the footer link set. Two other footer files exist —
`sections/footer.liquid` and `sections/tbk-footer.liquid` — **not confirmed live**; both were updated
for address consistency (B3) defensively, but `site-footer.liquid` is the one that actually renders.

## Hero

**File**: `sections/hero-image.liquid` (confirmed to exist; not deeply re-audited this pass beyond
confirming the file). Per `BUSINESS_MASTER.md`/`CLAUDE.md`: the live homepage hero currently uses a
**temporary product shot**, not commissioned photography — this is a content/asset gap, not a
component defect. See `DESIGN_SYSTEM.md`'s Photography note in `TBK_BRAND_GUIDELINES.md` §2.

## Cards

Base primitive: `.tbkx-card` (`snippets/tbk-components.liquid`) — see `DESIGN_SYSTEM.md`. All
specific card types below (Product, Collection) should extend this base rather than define a parallel
card shell.

## Product Card

**File**: likely rendered within `sections/main-collection.liquid` or a dedicated card snippet — **not
deeply audited this pass**; confirmed the collection listing renders through `main-collection.liquid`.
`DESIGN APPROVAL REQUIRED` / follow-up audit needed before treating any specific product-card markup
as canonical. Known, already-fixed constraint that applies regardless of exact markup: the first
gallery/product image on any listing must not be lazy-loaded if it's a likely LCP element (SEO-026,
already fixed for the live default template).

## Collection Card

Rendered via `sections/main-collection.liquid`. Real content constraint (not a markup detail): 7 of
the site's 36 collections are near-duplicates of each other and 2 show an unfiltered full catalogue
with no real curation (`BUSINESS_MASTER.md` §11, B5, unresolved) — any new collection-card feature
(e.g. a "Best Seller" ribbon) must not be wired to those 2 non-curating collections until B5 resolves,
or it will display a meaningless badge on the entire catalogue.

## Trust Badges

**Real, already-corrected pattern**: `sections/site-footer.liquid` conditionally renders
`service_areas` and `fssai_text` settings **only if the merchant has filled them in** — a safe,
already-established pattern (`ux/UX_AUDIT.md`'s finding) that any new trust badge should follow:
render nothing rather than a placeholder/fabricated value. **Do not add a new trust badge for
FSSAI/GST/rating/review-count claims** — none of those have a real value yet
(`BUSINESS_MASTER.md` §1/§10). Thirteen fabricated trust-badge instances have already been found and
removed from this codebase across this project's history — do not reintroduce the pattern.

## FAQ

**File**: `sections/accordion.liquid` (real, live, renders `templates/page.faq-01.json`'s 19-topic
content as of 2026-07-30). Title-divider blocks render as `<h5>`; question/answer pairs render as
`<details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">` — real,
schema-integrated Microdata, no separate JSON-LD needed for this page. A parallel `other_content`
block type renders a "still have a question?" CTA with configurable button links. New FAQ content
should always use this existing section/block structure — do not build a new FAQ component.

## Gallery

**Files**: `snippets/tbk-gallery.liquid` (used by the `tbk` product template — real, already-fixed
lazy-loading defect, SEO-026), `sections/image-gallery.liquid` / `image-gallery-manual.liquid` (exist;
not deeply audited this pass). The **actually-live default product template**
(`templates/product.json`, all 602 active products) uses `product-media.liquid`
with `lazy_load: false` already correctly set on the first media item — confirmed correct, no action
needed there.

## CTA

No single dedicated "CTA" section/snippet was found as a named component — CTAs are composed from
`{% render 'tbk-button' %}` (see `DESIGN_SYSTEM.md`/`TBK_BRAND_GUIDELINES.md` §2) placed within
whichever section needs one (e.g. the FAQ's `other_content` block's `solid_btn_label`/
`solid_btn_link` fields). Treat "CTA" as a usage pattern of the Button component, not a separate one.

## Testimonials / Reviews

**Governing document**: `REVIEW_STRATEGY.md` (repo root) — a complete, pre-existing governance
document for this exact component; read it in full before touching anything review-related, it is
more authoritative than this entry. Key real facts it establishes:

- The real, live component is `sections/home-reviews.liquid` — **intentionally FROZEN v1.0, renders
  nothing**, because there are 0 verified reviews. This is correct, specified behavior, not a defect.
- Real reviews live in a `testimonial` **metaobject** (`gid://shopify/MetaobjectDefinition/13988495529`),
  every field mandatory including a public `source_url` — fabrication is structurally impossible, not
  just discouraged, because the metaobject has no field that could hold an unsourced claim.
- Approved sources in priority order: Google Business Profile (ratified primary, 2026-07-16) →
  Judge.me → Loox → Shopify Product Reviews → Zomato (conditionally blocked, terms unconfirmed).
  **A real Google Business Profile listing for this business was located this project**
  (`BUSINESS_MASTER.md` §5) — this is a concrete, real path to activating this section that didn't
  exist before.
- `AggregateRating`/`Review` schema is **never** emitted on the `Bakery`/`Organization`/`LocalBusiness`
  entity, under any circumstance — three independent reasons documented in `REVIEW_STRATEGY.md` §5.
- Separate, **not-confirmed-live** files exist in the repo (`sections/testimonials.liquid`,
  `testimonials-2.liquid`, `testimonials-3.liquid`, `testimonial-before-after.liquid`) — do not assume
  any of these are the real component; `home-reviews.liquid` is the one `REVIEW_STRATEGY.md` names as
  canonical and frozen.

## Announcement Bar

**Files**: `sections/tbk-announcement-bar.liquid` (real `tbk-announcement-bar` type, referenced in
`header-group.json`) and `sections/announcement-bar.liquid` (a second, generic version — its
instance in `header-group.json` was `disabled: true` as of the last direct check). Do not assume the
generic version is live without re-checking `header-group.json`'s current `disabled` flags first — a
disabled-flag check has already been the deciding factor in several real findings on this project.

## Drawer

**File**: `sections/cart-drawer.liquid` (`hdt-` component family — `<hdt-cart-drawer>` custom
element, `hdt-mini-cart` classes). Separate from the header's own mobile navigation drawer
(`tbk-header.liquid`'s `.tbk-drawer-nav`, `tbk-` family) — **two independently-built drawer patterns
coexist**, one for cart, one for navigation. Do not merge them without a deliberate design decision;
document any future unification as its own change, not an incidental side effect of touching either.

## Search

**Files**: `sections/main-search.liquid` (search results page), `snippets/hdt_predictive-search.liquid`
/ `hdt_predictive-search2.liquid` (live-as-you-type dropdown — two versions exist, not confirmed which
if either is currently wired; do not assume). `hdt-` component family throughout.

## Filters

Not confirmed as a distinct, separately-named component this pass — likely composed within
`main-collection.liquid`/`toolbar-mobile.liquid`. **Follow-up audit needed** before documenting
filter-specific markup/behavior as canonical.

## Variant Picker

Rendered within the live product template (`main-product-premium-v2.liquid`, confirmed as the
protected default template per `CLAUDE.md` — **product page changes require explicit sign-off; no
visual/UX/flow/CSS/JS changes without deliberate approval**, this rule overrides anything else in this
document for that one template).

## Price

Related file: `sections/price_tables.liquid` exists; product-page pricing itself renders within the
protected product template — same golden-rule constraint as Variant Picker above.

## Reviews

See **Testimonials / Reviews** above — one entry, not duplicated, since this project's real component
(`home-reviews.liquid`) and governance (`REVIEW_STRATEGY.md`) treat them as the same system, not two
separate ones.

## Breadcrumb

**Schema-only, no visible UI component found.** `snippets/tbk-schema-breadcrumb.liquid` emits a
`BreadcrumbList` JSON-LD block (fully dynamic across product/collection/article/page types,
`schema/SCHEMA_AUDIT.md`'s own finding: "verified correct, no issues found") — this is structured
data for search engines, not a rendered on-page breadcrumb trail. If a **visible** breadcrumb UI is
ever wanted, that is new component work, not something already built —
**`DESIGN APPROVAL REQUIRED`**.

---

## What this document does not do

No component is built, modified, or removed by this document. Several entries above explicitly flag
"not deeply audited this pass" or "follow-up audit needed" rather than asserting confidence this
pass's evidence doesn't support — treat those as open items, not settled documentation.

## Related

[../business/BUSINESS_MASTER.md](../business/BUSINESS_MASTER.md),
[../business/TBK_BRAND_GUIDELINES.md](../business/TBK_BRAND_GUIDELINES.md),
[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md), [../REVIEW_STRATEGY.md](../REVIEW_STRATEGY.md),
[CONTENT_SYSTEM.md](CONTENT_SYSTEM.md), [COPY_GUIDELINES.md](COPY_GUIDELINES.md).
