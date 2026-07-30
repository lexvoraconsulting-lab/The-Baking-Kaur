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

### Delivery cluster (already mostly linked, per `LOCAL_SEO_ROADMAP.md` §7 — gaps only, not repeated)

- **Hub**: `/pages/cake-delivery-in-meerut` (the most general delivery page)
  - Missing links → `/pages/frequently-asked-questions-faqs`, `/pages/100-percent-eggless-bakery`
  - Existing links → `/pages/midnight-cake-delivery`, `/pages/30-minute-cake-delivery-in-meerut-...` (already present, confirmed)
- **Future hub**: `/pages/delivery-areas-in-meerut` (once built, per `DELIVERY_AREA_SPEC.md`) becomes
  the parent of all three delivery-mode pages above — they should link back up to it once it exists

### Eggless page (currently an island)

`/pages/100-percent-eggless-bakery` is linked *from* the delivery-in-Meerut page's "Why Choose"
section already, but does not itself link *out* to anything beyond its own collection list. Add:
→ `/pages/frequently-asked-questions-faqs` (its own FAQ section duplicates 3 questions already on
the new FAQ page — link instead of duplicating, once the FAQ page's eggless section is confirmed to
cover the same ground; if kept separate, at minimum cross-link both directions).

### FAQ page (currently only reachable via the header)

Per `LOCAL_SEO_ROADMAP.md` §8: link **to** the FAQ page from every delivery/hamper/eggless page (5
pages) and **from** the FAQ page's existing "Still have a question?" block, which already links to
Contact — add a link to the most relevant topic page per FAQ section (e.g. the Delivery section
links to `/pages/cake-delivery-in-meerut`, the Eggless section to `/pages/100-percent-eggless-bakery`,
the Hampers section to `/pages/gift-hampers`).

### Hampers cluster

- **Hub**: `/pages/gift-hampers` (the richest page on the site) already lists related collections by
  name but not as links — convert "Related Collections" (Birthday Cakes, Anniversary Cakes, Designer
  Cakes, Wedding Cakes, Flowers & Cake Combos, Midnight Delivery) from plain text to real hyperlinks
  to the matching live collections.
- Its three location-specific siblings (`/pages/customised-hampers-meerut`,
  `/pages/festive-hampers-meerut`, `/pages/surprise-hampers-meerut`) should link back to the hub and
  to each other — not verified whether they currently do; flag for a content-pass check before this
  BUILD's next phase.
- Festival hampers: once/if additional festival collections are built (see §12 in
  `WEBSITE_ARCHITECTURE.md`), each should link to `/pages/festive-hampers-meerut` and vice versa.

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
