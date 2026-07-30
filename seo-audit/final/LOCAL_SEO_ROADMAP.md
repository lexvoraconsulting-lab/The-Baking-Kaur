# Local SEO Roadmap — Meerut

Generated 2026-07-30. Builds directly on this session's real findings (`ADDRESS_AUDIT.md`,
`DELIVERY_AREA_SPEC.md`, `EEAT_REPORT.md`) — this is a prioritized plan, not new content or code.
Standing context: the storefront is intentionally password-gated pre-launch (per project memory), so
none of this reaches Google until the gate lifts — sequence accordingly.

## Priority 0 — fix before anything new ships

These are prerequisites; building new local-SEO content on top of them would just propagate the
existing inconsistencies further.

1. **Resolve the address/coordinate conflict** (`ADDRESS_AUDIT.md`) — a single confirmed address and
   a fresh Google Maps pin-drop, applied consistently across all schema, footer, and page copy.
   Blocks: an accurate Local Pack listing, an accurate Google Business Profile match, and any new
   Service Area page (§2 below) that would otherwise just add a *fifth* address wording.
2. **Resolve the delivery-area-list conflict** (`DELIVERY_AREA_SPEC.md` §2) — one confirmed list of
   serviceable localities. Blocks: Service Area pages, internal linking anchor text, and the LocalBusiness
   `areaServed` schema (currently just "Meerut" city-level, not neighborhood-level).
3. **Google Business Profile consistency check** — once the address/hours are confirmed internally
   (P0.1), compare against the real GBP listing (this session has no GBP access; needs the business
   or a browser session with the login). NAP (Name/Address/Phone) must match exactly between the site
   and GBP — right now the site alone has 4 address wordings, so it cannot yet be said to match GBP
   even in principle.

## Priority 1 — once P0 is resolved

4. **Repurpose the unpublished Store Locator page** into a real Delivery Areas page using
   `DELIVERY_AREA_SPEC.md` as the content source. Keep it unpublished until the P0 conflicts are
   settled — publishing it with either of the two conflicting area lists just live-ships the
   conflict on a dedicated, more-visible page.
5. **Expand `LocalBusiness`/`Bakery` schema's `areaServed`** from the current single "Meerut" city
   entity to the confirmed neighborhood list (once P0.2 settles it) — this is the schema-level
   equivalent of the content work in item 4, and should ship together with it, not independently.
6. **Service Area pages** for the top 2-3 confirmed localities (e.g. a dedicated page per major
   service area, if the business wants neighborhood-level landing pages) — deliberately not scoped
   further here since it depends on which localities P0.2 confirms as real, and how many the business
   wants dedicated pages for. This is a content-investment decision, sized once P0.2 lands.

## Priority 2 — internal linking

7. **Cross-link the existing real delivery pages to each other consistently.** They already link
   somewhat (e.g. `midnight-cake-delivery` → `surprise-hampers-meerut`; `30-minute-...` →
   `midnight-cake-delivery` and `gift-hampers`) but not uniformly — `cake-delivery-in-meerut` (the
   most general page) doesn't link to the FAQ page, and none of the delivery pages link to
   `100-percent-eggless-bakery` from their body copy even though eggless is a core differentiator
   mentioned on all of them. Low-effort, no new content needed — just adding existing real URLs as
   links within already-published copy.
8. **Link the new FAQ page (SEO-013, shipped this session) from the delivery/hamper pages** — right
   now nothing links to `/pages/frequently-asked-questions-faqs` except the header, so it's an island
   relative to the topically-relevant pages that would benefit from cross-linking into it.

## Priority 3 — once the storefront password gate lifts

9. **Re-run Core Web Vitals / Search Console checks** — meaningless while gated (per project memory);
   don't schedule this until launch is confirmed.
10. **Submit/verify sitemap.xml** — previously found 404 (SEO-019), very likely a symptom of the
    password gate per existing project notes; re-check once gated status changes, not before.

## What this roadmap deliberately does not include

No new page count targets, no keyword-volume estimates, no backlink strategy — none of that data is
available to this session, and inventing plausible-sounding numbers would violate this audit's own
"no unverifiable claims" standard just as much as a fabricated rating would.

## Related

[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md), [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md),
[CONTENT_PLAN.md](CONTENT_PLAN.md), [../seo/LOCAL_SEO.md](../seo/LOCAL_SEO.md) (prior local-SEO
audit detail).
