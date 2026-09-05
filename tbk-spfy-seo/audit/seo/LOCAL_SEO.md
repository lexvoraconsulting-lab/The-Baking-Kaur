# Local SEO Audit

## NAP (Name, Address, Phone)

**Verified real, consistent** between `snippets/bk-local-business.liquid`'s `Bakery` schema:
phone `+918218862928`, address "Fatah Complex, Thapar Nagar Lane 7, Meerut, Uttar Pradesh 250001,
IN" — matches `CLAUDE.md`'s own recorded delivery-area facts (Meerut, ~15 km radius).

## Geo-coordinates

**SEO-015 (open, Medium, Requires Manual Verification)**: `28.9931, 77.6939`, flagged by an
in-code comment (predating this audit) asking the merchant to verify against Google Maps. Not
independently confirmed or refuted this pass — no Maps access available.

## LocalBusiness / Bakery schema completeness

Present: `@type: "Bakery"`, `priceRange`, `servesCuisine`, `areaServed` (City: Meerut),
`openingHoursSpecification` (all 7 days, 09:00–23:59), a `makesOffer` entry for Midnight Cake
Delivery, `sameAs` (Instagram + Facebook). **Verified**: no `aggregateRating` present, and the
file's own comment explains why (see [../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md)) — a
deliberate, correct omission, not a gap.

## Google Business Profile

**Requires Manual Verification / out of scope** — no Google Business Profile API access this
session. `CLAUDE.md` already tracks the header's "★4.9 Rated" claim (SEO-016) as needing either
removal or a real link to the actual GBP listing — unresolved, needs your explicit decision.

## Service area / local landing pages

`sections/site-footer.liquid` conditionally renders `s.service_areas` text if the merchant has
filled it in (line 119-121) — a well-built, verifiable-by-design pattern (doesn't render anything
if blank, unlike the hardcoded claims found elsewhere). Whether it's currently populated with real
content wasn't checked this pass.

## Reviews, review schema

**Verified**: 0 real reviews exist (per `CLAUDE.md`, unchanged), and — critically — this audit found
and removed a fabricated review section (SEO-006) that was presenting fake testimonials as real. No
review schema (`AggregateRating`, `Review`) is emitted anywhere, correctly, since none would be
backed by real data.

## Related

[../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md), [../audit/MANUAL_VERIFICATION.md](../audit/MANUAL_VERIFICATION.md).
