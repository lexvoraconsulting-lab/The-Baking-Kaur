# Content System

**Canonical hierarchy**: `business/BUSINESS_MASTER.md` → `business/TBK_BRAND_GUIDELINES.md` →
`DESIGN_SYSTEM.md`/`COMPONENT_LIBRARY.md` → this document. This document documents page-level
**structure** (what sections exist, in what order, sourced from what components); it does not repeat
`TBK_BRAND_GUIDELINES.md` §3's content-standards rules — read that first.

---

## Homepage Structure

Per the already-approved slot architecture (`WEBSITE_ARCHITECTURE.md` §5, not re-derived here):

1. Hero (`sections/hero-image.liquid`) — currently a temporary product shot, real photography pending.
2. Verifiable differentiators strip — must only state facts traceable to `BUSINESS_MASTER.md`.
3. Occasion entry points — the same 6 collections now live in the header's "Categories" dropdown
   (Sprint 2, task 2.1); homepage and header should share one link set, not two independently
   maintained ones.
4. Hampers cross-sell → `/pages/gift-hampers`.
5. Trust section (`sections/home-reviews.liquid`) — **frozen, renders nothing** until a real,
   verified review lands (see `COMPONENT_LIBRARY.md`'s Testimonials entry / `REVIEW_STRATEGY.md`).
   Do not fill this slot with a placeholder claim.
6. FAQ teaser — 2-3 real questions from the live FAQ page, linking through to it.
7. Footer (`sections/site-footer.liquid`).

## Collection Structure

Short intro copy (not "walls of text," per `CLAUDE.md`'s already-completed trim pass) → product grid
(`main-collection.liquid`, Product Card component) → optional cross-link to the single most relevant
delivery/content page (`INTERNAL_LINKING.md`'s Collections cluster, approved, partially implemented).
**Before adding a new collection**, check `BUSINESS_MASTER.md` §11 — 7 near-duplicate collections and
2 non-curating utility collections are a known, unresolved issue (B5); don't add an 8th near-duplicate.

## Product Structure

Governed by the **protected default product template**
(`sections/main-product-premium-v2.liquid`) — per `CLAUDE.md`'s golden rule, **no visual/UX/flow/CSS/
JS change without deliberate, explicit sign-off**, regardless of anything else in this document set.
Only invisible edits (structured data, analytics, accessibility, performance) are permitted, and only
deliberately. SEO title/description follow the real, migrated template
(`"{Name} - Eggless | Meerut"`, `TBK_BRAND_GUIDELINES.md` §4).

## Blog Structure

**`BUSINESS APPROVAL REQUIRED`** — a Shopify blog object ("News") exists but is unused and unlinked
(`BUSINESS_MASTER.md`, corrected from an earlier "no blog exists" statement). No structure to
document until the business decides whether to use it (`CONTENT_PLAN.md`'s open question).

## Landing Pages

Real, established anatomy (observed across `cake-delivery-in-meerut`, `midnight-cake-delivery`,
`30-minute-cake-delivery-...`, the hamper cluster, and the eggless page): an H2 intro → 2-4 H2/H3
topic sections with real specifics → a small on-page FAQ (3-6 Q&A) → a "Why Choose"/differentiators
list → a closing cross-link paragraph to related pages/collections. New landing pages should follow
this same real anatomy rather than a from-scratch structure.

## FAQs

19-topic, title-divider-grouped accordion structure, fully documented in `TBK_BRAND_GUIDELINES.md` §3
and `COMPONENT_LIBRARY.md`'s FAQ entry — not repeated here. **Do not** create a second, separately-
structured FAQ page; extend the existing one.

## Policies

**Do not draft new policy structure or wording** until B1 (`BUSINESS_MASTER.md` §9) resolves — the
live refund/terms sources currently contradict each other. Once resolved, the canonical structure
(per the approved custom "Refund & Return Policy" page) is: intro → Cancellations & Changes →
Damaged/Incorrect/Quality Issues → Non-Returnable by Nature → Refund Method & Timeline → Allergies →
Contact Us. Reuse this structure for the corrected Shop Policies rather than inventing a new one.

## Email

**`BUSINESS APPROVAL REQUIRED`** — no email template or transactional-copy structure exists in any
reviewed document.

## WhatsApp

Real, live pattern: `https://wa.me/918218862928?text={url-encoded, page-specific greeting}`. Structure
observed: greeting names the business + states intent specific to the page it's linked from (e.g. "I
want to order a custom cake" on general pages, vs. hamper-specific phrasing on hamper pages). New
WhatsApp links should follow this same specific-to-context pattern, not a single generic message
reused everywhere.

## Social (Instagram)

Handle confirmed real (`BUSINESS_MASTER.md` §14). **`BUSINESS APPROVAL REQUIRED`** for any content
calendar, caption structure, or hashtag system — none exists in any reviewed document.

---

## What this document does not do

No page is built, restructured, or published by this document. Every structure described is either
already real and live (Homepage slots, FAQ, landing-page anatomy, WhatsApp pattern) or explicitly
marked as requiring a business decision that hasn't been made (Blog, Email, Social calendar).

## Related

[../business/BUSINESS_MASTER.md](../business/BUSINESS_MASTER.md),
[../business/TBK_BRAND_GUIDELINES.md](../business/TBK_BRAND_GUIDELINES.md),
[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md), [COMPONENT_LIBRARY.md](COMPONENT_LIBRARY.md),
[COPY_GUIDELINES.md](COPY_GUIDELINES.md),
[../seo-audit/final/CONTENT_PLAN.md](../seo-audit/final/CONTENT_PLAN.md).
