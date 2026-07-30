# Delivery Areas in Meerut — Replacement Specification (SEO-030)

Generated 2026-07-30. This is a **content specification**, not new theme code or a new live page.
Per instruction: the fake "Store Locator" page (`templates/page.store-locations.json`,
London/Madrid/Tokyo demo content) stays unpublished, is not deleted, and is a candidate for
repurposing later using this spec — this document is that repurposing plan, grounded entirely in
real, already-published site content and previously-verified project facts (see
`CLAUDE.md` → "Local delivery"). Nothing below is invented; where a requested topic has no real
source, that's stated explicitly rather than filled in.

## 1. Service radius (verified, `CLAUDE.md`)

- **~15 km radius** from the Meerut studio.
- **₹350 minimum order** for delivery.
- **Distance-based delivery fees** — Merchant Center shipping is set to Manual, decoupled from
  Shopify shipping profiles (per `CLAUDE.md`), so exact fee tiers aren't in the theme/Admin data
  this session can read; confirm current fee bands with the business before publishing specific
  numbers beyond the ₹350 minimum.

## 2. Named delivery areas — two live lists, not identical

| Source | Areas listed |
|---|---|
| Live "Cake Delivery in Meerut" page (`/pages/cake-delivery-in-meerut`) | Thapar Nagar, Shastri Nagar, **Ganga Nagar**, **Partapur**, **Jagriti Vihar** and nearby localities |
| Live footer `service_areas` setting (`sections/site-footer.liquid`, confirmed live) | Thapar Nagar, Shastri Nagar, **Sadar Bazaar**, **Civil Lines**, **Pallavpuram**, Ganga Nagar & nearby areas |

Both are real, both are live, and they don't match past the first two entries. A future Delivery
Areas page should use **one** confirmed list — recommend the business confirm the true full list of
serviceable localities once, and both surfaces get updated together (see
[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md) for the same "two lists disagree" pattern applied to the
address itself).

## 3. Same-Day Delivery (verified — real, live page content)

Source: `/pages/cake-delivery-in-meerut`, `/pages/30-minute-cake-delivery-in-meerut-...`.

- Order online, receive freshly prepared cakes "within hours."
- Available for "most designs ordered within cut-off time" — the live copy does not state a
  specific cut-off hour; do not invent one for a future page without confirming it with the business.

## 4. Midnight Delivery (verified — real, live page content, `/pages/midnight-cake-delivery`)

- Choose a midnight slot at checkout; cake is baked fresh same-day and delivered around midnight.
- Advance booking recommended for designer/tiered cakes.
- Available across the site's Meerut delivery zones (same "confirm your area" caveat as §2).

## 5. Express / 30-Minute Delivery (verified — real, live page content)

Source: `/pages/30-minute-cake-delivery-in-meerut-premium-reliable-service`.

- Selected ready-to-go birthday/celebration cake designs only — not the full catalogue.
- **Selected areas of Meerut only** — narrower than the general same-day/midnight zones; the live
  copy repeatedly says "terms and conditions apply" without stating which areas qualify. A real
  Delivery Areas page should state the actual qualifying zone list once the business confirms it —
  currently unconfirmed anywhere in the data this session could read.

## 6. Wedding Venue Delivery (verified — real, sitewide FAQ content already live)

Source: `layout/theme.liquid`'s sitewide FAQPage JSON-LD (already live, already fact-checked, not
new): *"Yes, we provide custom wedding cakes with flexible on-site setup depending on the venue and
client requirement."* This confirms on-site/venue setup is a real, offered service — no specific
venue list, radius, or setup fee is stated anywhere in the data available this session; do not invent
one.

## 7. Corporate Delivery (verified — real, live Gift Hampers page content)

Source: `/pages/gift-hampers`. Under "Same-Day & Surprise Delivery": Home Delivery, **Office
Delivery**, **Venue Delivery**, Customized Surprise Experiences. Under "Corporate Gifting Solutions":
employee appreciation hampers, festive gifting boxes, client gifting, event gifting packages "tailored
to business requirements." No specific corporate delivery radius, minimum order size, or lead-time
is stated anywhere found — flag for the business if a dedicated Corporate Delivery section is built.

Note: the dedicated "Corporate Gifting Solutions" page (`/pages/corporate-gifting-solutions`) exists
in Admin but is **unpublished with an empty body** — it's a stub, not a source of any real facts yet.

## What this spec deliberately leaves open

- The single, confirmed delivery-area list (§2's conflict).
- Same-day order cut-off time (§3).
- Which specific localities qualify for 30-minute express delivery (§5).
- Any wedding-venue-specific radius or setup fee (§6).
- Corporate/bulk delivery minimums or lead times (§7).

None of these are guessed here. If/when the fake Store Locator page is repurposed into a real
Delivery Areas page, these five gaps are exactly what's needed from the business before publishing —
everything else in this spec is already real, live, verifiable copy that can be reused directly.

## Related

[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md), [LOCAL_SEO_ROADMAP.md](LOCAL_SEO_ROADMAP.md),
[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md) (SEO-030).
