# Website Architecture — Production Build (BUILD-020)

Generated 2026-07-30. Role: this document designs the final website architecture for The Baking
Kaur, building strictly on evidence already established across every prior report (`EXECUTIVE_REPORT.md`,
`AUDIT_LEDGER.md`, `POLICY_CONSOLIDATION.md`/`POLICY_ARCHITECTURE.md`, `ADDRESS_AUDIT.md`,
`DELIVERY_AREA_SPEC.md`, `EEAT_REPORT.md`, `LOCAL_SEO_ROADMAP.md`, `CONTENT_PLAN.md`). Nothing below
repeats those findings in depth — each section cites the relevant prior work and adds the
architectural decision on top of it. **No code is written. No page, menu, or collection is created,
edited, published, or deleted.** Every place a real business fact or legal/visual decision is needed
carries `<<BUSINESS APPROVAL REQUIRED>>` rather than a guess.

Four areas have their own dedicated companion document, since they need tabular/tree detail this
narrative document would otherwise have to duplicate: [SITE_TREE.md](SITE_TREE.md) (§1),
[NAVIGATION.md](NAVIGATION.md) (§2), [URL_STRUCTURE.md](URL_STRUCTURE.md) (§3),
[INTERNAL_LINKING.md](INTERNAL_LINKING.md) (§4). This document summarizes each briefly and gives full
treatment to §5–§12, which have no dedicated document yet.

## 1. Website hierarchy

Full current-state and target-state tree in [SITE_TREE.md](SITE_TREE.md). Headline decision this
BUILD makes: **the site already has more real, usable structure than is switched on.** Six menus
exist; three are empty shells (`explore-cakes`, `quick-links`, `meerut-delivery`) apparently created
for a navigation redesign that never shipped, and a fourth (`header`, with real content — all 6
primary collections) is wired only to a disabled section block. The architecture in this document
turns on and organizes what already exists before proposing anything new.

## 2. Navigation

Full detail in [NAVIGATION.md](NAVIGATION.md). Headline decisions: wire the live header to the six
real collection links already sitting unused in the `header` menu; fix the footer's Refund/Terms
link targets, which currently point at the wrong side of the SEO-031 policy conflict and at the empty
Terms page (SEO-034) respectively; populate the empty `meerut-delivery` menu as the real home for
Delivery Area navigation (§9).

## 3. URL architecture

Full detail in [URL_STRUCTURE.md](URL_STRUCTURE.md). Headline decision: every new URL this BUILD
proposes follows a pattern the site already uses successfully (`/pages/{topic}-in-meerut`,
`/collections/{festival}-hampers`) — no new convention is invented. No existing handle is renamed,
per `CLAUDE.md`'s standing deferred-handle-optimization decision. The 7 near-duplicate "Meerut"
collections (all ~986 products) are flagged as the collection-level equivalent of the SEO-031 policy
duplication, needing the same kind of business decision, not resolved here.

## 4. Internal linking

Full detail in [INTERNAL_LINKING.md](INTERNAL_LINKING.md). Headline decision: this site's content is
already topically rich but almost entirely unlinked — the fix across every cluster (delivery, eggless,
hampers, FAQ, wedding, corporate) is adding existing real URLs into already-published copy, near-zero
content cost.

## 5. Homepage architecture

Per `CONTENT_PLAN.md`'s Homepage brief (not repeated in full): the hero is currently a temporary
product shot and S8 Trust is gated on FSSAI number or real reviews, both already tracked in
`CLAUDE.md` as client-blocked. Architecturally, the homepage should be structured as:

1. Hero (blocked on real photography — `<<BUSINESS APPROVAL REQUIRED>>` / client-blocked, not
   architecture's job to resolve)
2. Verifiable differentiators strip: 100% eggless as standard practice, same-day/midnight delivery,
   made-to-order — every claim here must trace to something already verified in `EEAT_REPORT.md`
3. Occasion entry points → the six primary collections, using the same six links this BUILD is
   already wiring into the header (§2) — the homepage and header should share one link set, not
   maintain two independently
4. Hampers cross-sell → `/pages/gift-hampers`
5. Trust section (S8) → stays gated until FSSAI number or 3 real reviews land, per `EEAT_REPORT.md`;
   architecture reserves the slot, does not fill it with a placeholder claim
6. FAQ teaser → 2-3 real questions from the now-live FAQ page, linking through to it (closes the
   "FAQ is an island" gap from `INTERNAL_LINKING.md` §2 at the highest-traffic page on the site)
7. Footer (per `NAVIGATION.md` §2)

No new homepage copy is drafted here — this is slot architecture, not content.

## 6. Collection architecture

Real inventory: 36 collections total (confirmed via a live Admin API query this pass). Grouped by
real role:

- **Primary occasion collections** (5): Birthday (279), Anniversary (102), Wedding (134),
  Designer & Theme (165), Cake Hampers (119) — these are the real merchandising backbone and need no
  structural change.
- **Theme sub-collections** (13): Baby Girl, Butterfly, Unicorn, Jungle Animal Theme, etc. — real,
  distinct, small (4-28 products each). Shopify collections don't support true nesting, so these
  should be presented as a filtered/grouped view under Designer & Theme Cakes in navigation and on-page
  UI, not as a URL hierarchy change.
- **Small real collections** (4): For Him, For Her, Photo Cakes, Flowers & Cake Combos — keep as-is.
- **Festival collection** (1 so far): Luxury Diwali Hampers — real precedent for §12 below.
- **Non-curating utility collections** (2): "Best Selling Products" and "Newest Products" both show
  exactly 1,235 products — identical to `/collections/all`, meaning neither is actually curating
  anything. `<<BUSINESS APPROVAL REQUIRED>>`: either wire these to real bestseller/newest-arrival
  logic (Shopify supports this natively via smart collection sort rules) or unpublish them — a
  collection claiming to be "Best Selling" while showing the entire, unfiltered catalogue is a small
  trust-signal problem in the same family as the fabricated-count findings in `EEAT_REPORT.md`, even
  though no explicit false claim is stated in words.
- **The 7-collection "Meerut" cluster** (all ~986 products, near-identical): `cakes`,
  `cake-delivery-meerut`, `same-day-cake-delivery-meerut`, `midnight-cake-delivery-meerut`,
  `midnight-cake-delivery`, `custom-cakes-meerut` (617, the one outlier), `kids-birthday-cakes-meerut`.
  This reads as an earlier attempt at collection-level keyword targeting, the same pattern that
  produced the duplicate policy pages and duplicate delivery-area lists elsewhere on this site.
  `<<BUSINESS APPROVAL REQUIRED>>`: recommend picking at most one or two of these to keep live (if
  any serve a real, distinct merchandising purpose) and unpublishing the rest, analogous to how
  `POLICY_ARCHITECTURE.md` recommends one canonical page per policy topic. Not resolved here — this
  is a merchandising/content decision, this document only names the pattern and the recommended
  mechanism.

## 7. Product architecture

Per `CONTENT_PLAN.md`'s Products brief (not repeated): SEO title/description migration is already
done for ~602 active products; the occasion-mismatch fix (`seo-ops/fix_description_occasion.py`) is
the one open item, already tracked, not new architecture work. Product page template itself
(`main-product-premium-v2.liquid`) remains the protected module per `CLAUDE.md` — this document
proposes no change to it. One architectural note worth adding here: `CLAUDE.md` already tracks a
handle typo pattern (`fruit-cocoktail`, `chocolate-moouse`) as deliberately deferred (fixing requires
a metaobject change first, risks deleting variants) — unchanged recommendation, just cross-referenced
here for completeness of the product-architecture picture.

## 8. Blog architecture

**No blog exists** on this storefront — confirmed again this pass (no blog template, no blog page in
the live Admin query). `CONTENT_PLAN.md` already flagged this as unconfirmed with the business.
Architecture, conditional on approval:

- `<<BUSINESS APPROVAL REQUIRED>>`: whether a blog is wanted at all. If the answer is no, this
  section should be struck from the roadmap entirely rather than carried forward as permanent
  unfinished business.
- If approved: standard Shopify blog architecture (`/blogs/{handle}/{article-handle}`, per
  `URL_STRUCTURE.md` §3), one blog object (not per-topic blogs), categorized by tag rather than by
  separate blog objects, linked from the footer and from the most relevant occasion collections
  (e.g. a wedding-planning article linked from `/collections/wedding-cakes`).
- No article topics, cadence, or count are proposed here — that would be inventing a content
  calendar with no business input behind it, the same category of guess this entire audit has
  avoided throughout.

## 9. Delivery Area architecture

Content fully specified in [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md); navigation placement in
[NAVIGATION.md](NAVIGATION.md) §3. Architectural summary: one hub page (repurposing the unpublished
Store Locator page, per SEO-030's already-approved "keep unpublished, don't delete" decision) linking
to the three existing real delivery-mode pages (same-day, midnight, express) and, only once SEO-035's
area-list conflict resolves, to per-locality pages. The `meerut-delivery` menu (currently an empty
shell) is the intended navigational home — reusing existing infrastructure rather than creating new.

## 10. Wedding architecture

Real facts exist but are scattered across two places (`/pages/about-us`, and the sitewide FAQ's
venue-setup answer in `layout/theme.liquid`) rather than consolidated, per `CONTENT_PLAN.md`.
Architecture: `/collections/wedding-cakes` remains the primary commercial page (134 real products,
no change needed). `<<BUSINESS APPROVAL REQUIRED>>`: whether a dedicated Wedding Cakes content page
is worth building to consolidate the scattered real facts and link out to the collection — this is
an investment decision (is a content page worth it beyond the collection page itself), not something
this architecture can decide unilaterally. If approved, URL pattern and linking already specified in
`URL_STRUCTURE.md` §3 and `INTERNAL_LINKING.md`'s Wedding cluster.

## 11. Corporate architecture

Real facts exist on `/pages/gift-hampers`'s "Corporate Gifting Solutions" section; the dedicated
`/pages/corporate-gifting-solutions` page already exists but is unpublished with an empty body — a
stub, not a gap requiring a new page. Per `CONTENT_PLAN.md`, three real inputs are needed before this
page is populated: minimum order size/lead time, whether GST/invoicing matters for corporate clients
(ties to `EEAT_REPORT.md`'s open GST question), and a real (even anonymized) client example.
Architecture: once populated, this page becomes the hub, cross-linked with Gift Hampers
(`INTERNAL_LINKING.md`'s Corporate cluster) — no new URL needed, the stub already has the right one.

## 12. Festival architecture

Real precedent already exists and works: `/collections/luxury-diwali-hampers` (44 products) plus
`/pages/gift-hampers`'s own festival list (Diwali, Rakhi, Karwa Chauth, Christmas, New Year,
Valentine's Week, Rose Day, Teddy Day, Propose Day, Mother's Day, Father's Day, Women's Day,
Teacher's Day). Architecture: replicate the Diwali pattern — a dedicated collection per festival
that has enough real, distinct product inventory to justify one (`<<BUSINESS APPROVAL REQUIRED>>`:
which festivals clear that bar; this document doesn't invent inventory levels), using the
`/collections/{festival}-hampers` URL pattern already established, each linked from and linking back
to `/pages/festive-hampers-meerut` (`INTERNAL_LINKING.md`'s Hampers cluster). Smaller/seasonal
occasions with too little real inventory for a dedicated collection stay as sections within the
existing Gift Hampers page rather than getting a thin, sparsely-stocked collection of their own.

## What this document does not do

No page, collection, menu, or product is created, edited, published, or deleted. No legal, visual, or
merchandising decision is made on the business's behalf — every such point is marked
`<<BUSINESS APPROVAL REQUIRED>>` and cross-referenced to the specific prior report that already
surfaced the underlying evidence. This is the architecture; implementation is a separate, future,
explicitly-scoped pass.

## Related

[SITE_TREE.md](SITE_TREE.md), [NAVIGATION.md](NAVIGATION.md), [URL_STRUCTURE.md](URL_STRUCTURE.md),
[INTERNAL_LINKING.md](INTERNAL_LINKING.md), [POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md),
[POLICY_REDIRECT_PLAN.md](POLICY_REDIRECT_PLAN.md), [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md),
[CONTENT_PLAN.md](CONTENT_PLAN.md), [LOCAL_SEO_ROADMAP.md](LOCAL_SEO_ROADMAP.md),
[EEAT_REPORT.md](EEAT_REPORT.md), [ADDRESS_AUDIT.md](ADDRESS_AUDIT.md),
[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md), [EXECUTIVE_REPORT.md](EXECUTIVE_REPORT.md).
