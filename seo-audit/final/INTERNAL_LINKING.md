# Internal Linking Architecture

Generated 2026-07-30, BUILD-020. Consolidates and extends `LOCAL_SEO_ROADMAP.md` §7/§8's already-
identified gaps into a full link map covering every content type in this BUILD's scope. This is a
plan — no page body or menu is edited here. Every link named below points at a URL confirmed live or
already specified elsewhere in this document set; nothing invents a new page's existence.

## 1. Principle

Link by real topical relevance, not by template convenience. This site's content is already
genuinely topically rich (delivery pages, eggless page, hamper page, FAQ) but almost entirely
unlinked to each other — each page was written and published in isolation. The fix is near-zero-cost:
adding existing real URLs into already-published copy, not writing new content.

## 2. Hub-and-spoke map

### Delivery cluster — IMPLEMENTED 2026-07-30

- **Hub**: `/pages/cake-delivery-in-meerut` — now links to `/pages/frequently-asked-questions-faqs`
  (added, via `pageUpdate`) in addition to its existing links to `/pages/midnight-cake-delivery`,
  `/pages/30-minute-cake-delivery-in-meerut-...`, and `/pages/100-percent-eggless-bakery` (all
  confirmed already present, unchanged).
- **Future hub**: `/pages/delivery-areas-in-meerut` (once built, per `DELIVERY_AREA_SPEC.md`) becomes
  the parent of all three delivery-mode pages above — they should link back up to it once it exists
  — **still open, blocked on Sprint 1**.

### Eggless page — IMPLEMENTED 2026-07-30

`/pages/100-percent-eggless-bakery` now links to `/pages/frequently-asked-questions-faqs` (added, via
`pageUpdate`), in addition to its existing links to the collections and to the same-day/midnight
delivery pages. Its own on-page FAQ section (6 real Q&A) was left as-is, not merged into the main FAQ
page — both are real, non-fabricated content, and merging them was out of this task's mechanical-link
scope.

### FAQ page — IMPLEMENTED 2026-07-30

Per `LOCAL_SEO_ROADMAP.md` §8: the FAQ page (`templates/page.faq-01.json` and its unused twin
`page.faq-02.json`) now links out to its 3 most relevant topic pages, added inline within the
existing Q&A content rather than in the section-divider headings (checked `sections/accordion.liquid`
first — divider "title" blocks render as plain `<h5>` text with no existing link precedent in this
file, so links were added within accordion-item answer text instead, matching the FAQ's own existing
pattern of linking to the Refund & Return Policy page from prose): the Delivery Q&A links to
`/pages/cake-delivery-in-meerut`, the Eggless Q&A to `/pages/100-percent-eggless-bakery`, the Hampers
Q&A to `/pages/gift-hampers`. Deployed live, verified byte-for-byte via a post-push pull/diff.

### Hampers cluster — cross-linking IMPLEMENTED 2026-07-30

- **Hub**: `/pages/gift-hampers` — added a new "Explore by Occasion" section linking to all 3
  location-specific siblings. "Related Collections" (task 2.8) — **implemented 2026-07-30**: converted
  all 6 items (Birthday Cakes, Anniversary Cakes, Designer Cakes, Wedding Cakes, Flowers & Cake
  Combos, Midnight Delivery) from plain text to real links to their matching live collections.
- Its three location-specific siblings (`/pages/customised-hampers-meerut`,
  `/pages/festive-hampers-meerut`, `/pages/surprise-hampers-meerut`) — **verified this pass that none
  linked to the hub or each other**, then fixed: each now links to the Gift Hampers hub and to the
  other two siblings (not itself), added within each page's existing closing paragraph.
- Festival hampers: once/if additional festival collections are built (see §12 in
  `WEBSITE_ARCHITECTURE.md`), each should link to `/pages/festive-hampers-meerut` and vice versa —
  still open, not part of this pass (no new festival collections exist yet).

### Collections ↔ Delivery/Policy (currently zero links either direction)

Per `CONTENT_PLAN.md`'s Collections brief: each core collection (Birthday, Anniversary, Wedding,
Designer & Theme, Hampers) should link to its single most relevant delivery page from its
description — Birthday → same-day delivery, Wedding → the venue-setup FAQ answer (once a Wedding
Cakes page exists, see §3 below), Hampers → Gift Hampers page (if the collection and page aren't
already cross-linked; not confirmed this pass).

### Wedding cluster (mostly to be built, not yet linked because most of it doesn't exist as a page yet)

Real facts currently live in two disconnected places: `/pages/about-us` ("bespoke wedding cakes,"
"luxury wedding cakes in Meerut") and the sitewide FAQ schema in `layout/theme.liquid` (the venue-
setup answer). If the optional Wedding Cakes page from `CONTENT_PLAN.md`/`SITE_TREE.md` is built, it
becomes the hub: linked from `/collections/wedding-cakes`, from About Us, and linking out to the
Wedding collection and to Contact (for venue-setup inquiries, since no dedicated venue-radius data
exists — per `DELIVERY_AREA_SPEC.md` §6).

### Corporate cluster (same situation — real facts scattered, hub not yet populated)

`/pages/gift-hampers`'s "Corporate Gifting Solutions" section is the only place this content
currently lives. Once `/pages/corporate-gifting-solutions` is populated (per `CONTENT_PLAN.md`'s open
questions), it becomes the hub, linked from Gift Hampers and vice versa.

### Policy cluster

Fully specified already in `POLICY_REDIRECT_PLAN.md` — the canonical Refund/Terms pages should be
linked consistently from the footer, the quick-links menu, and the FAQ's Payment/Refunds section
(the FAQ page already links to `/pages/refund-return-policy` twice, added this session — once the
canonical decision in `POLICY_ARCHITECTURE.md` is made, verify this still points at the right URL).

## 3. Orphan pages (zero inbound internal links found this pass)

- `/pages/photo-cakes`, `/pages/theme-cakes` — real, published pages with no confirmed inbound link
  from their matching collections (`photo-cakes`, `designer-theme-cakes`). Recommend linking each
  collection description to its matching content page.
- `/pages/data-sale-opt-out` — orphan by design while unpublished; once/if published per
  `POLICY_ARCHITECTURE.md`, link it from the footer/quick-links menu (already specified in
  `NAVIGATION.md` §2/§4).

## 4. What this document does not do

No page copy is rewritten to add these links — that's an implementation task for whichever future
pass has "no coding" lifted. This document specifies the target link graph only.

## Related

[SITE_TREE.md](SITE_TREE.md), [NAVIGATION.md](NAVIGATION.md), [URL_STRUCTURE.md](URL_STRUCTURE.md),
[LOCAL_SEO_ROADMAP.md](LOCAL_SEO_ROADMAP.md), [CONTENT_PLAN.md](CONTENT_PLAN.md).
