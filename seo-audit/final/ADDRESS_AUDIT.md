# Address, Phone, Hours &amp; Coordinate Audit (SEO-015 / SEO-029)

Generated 2026-07-30. Every occurrence below was read directly from either the live theme (via
`shopify theme pull` / repo grep, cross-checked against a live pull) or the Shopify Admin API
(GraphQL). Nothing here is invented — where sources disagree, both are quoted verbatim and flagged.
No canonical value is chosen in this document; that is a business decision (see **Recommendation**).

## 1. Street address — 4 distinct wordings, live simultaneously

| # | Source | Live? | Exact text |
|---|---|---|---|
| A | **Shopify Admin — shop billing address** (merchant record of truth) | N/A (admin only) | `address1`: "Thapar Nagar Gali Number 7 Lajpat Bazaar Thapar Nagar" · `address2`: "Fateh Complex, 390/1, Lane Number 7, opposite Ice Factory," · Meerut, Uttar Pradesh 250001 |
| B | Shopify built-in **Contact Information legal policy** (`checkout.shopify.com/.../policies/28523757737.html`) | **Live, public** | "The Baking kaur, Fateh complex, Thapar Nagar Gali no 7, Meerut city, Pincode :250001" (contains stray `<meta charset="utf-8">` tags mid-paragraph — a copy-paste artifact, not just a wording issue) |
| C | `snippets/bk-local-business.liquid` (Bakery JSON-LD, renders on every page) | **Live** | `streetAddress`: "**Fatah** Complex, Thapar Nagar Lane 7" — note the typo, "Fatah" not "Fateh" |
| D | `sections/site-footer.liquid` (confirmed live footer via `footer-group.json`) | **Live** | "**Fatah** Complex, Thapar Nagar Lane 7, Meerut, Uttar Pradesh 250001" — same typo as C |
| D2 | `sections/footer.liquid`, `sections/tbk-footer.liquid` (not confirmed live, but present in repo) | Unconfirmed | "**Fatah** Complex, Thapar Nagar Lane 7, Meerut – 250001" — same typo |
| E | `templates/page.contact-2.json` (live Contact page — map embed, contact list, on-page FAQ, ×3 occurrences) | **Live** | "**Fateh** Complex, Thapar Nagar – Lane No. 7, Meerut, Uttar Pradesh – 250001" — correct spelling here |
| F | Custom "Refund & Return Policy" page body (live, Admin API Page) | **Live** | "390/1, Lane Number 7, Thapar Nagar, Meerut, Uttar Pradesh 250001" — no "Fateh/Fatah Complex" at all, different structure entirely |
| G | Header `note_mobile` (header-e-commerce.liquid / header-menu-bottom blocks) | **Not live** — both blocks are `"disabled": true` in `header-group.json` | Same wording as F |
| H | `snippets/tbk-schema-website.liquid` (Organization JSON-LD, renders on every page) | **Live** | **No `streetAddress` field at all** — only locality/region/postal/country |

**Finding**: three live surfaces (B, C/D, E) each spell the building name differently ("Fateh" vs
"Fatah"), and a fourth live surface (F, the Refund & Return Policy page) uses a completely different
address structure ("390/1, Lane Number 7" first) that matches nothing else live except the two
disabled header blocks. The Shopify Admin billing address (A) — arguably the single most
authoritative record, since it's what the merchant entered into their own account — matches neither
exactly: it has both "Lajpat Bazaar" (appears nowhere else) and "390/1... opposite Ice Factory"
(the detail F has but nowhere else does). This reads as the same real address transcribed
independently at least four times, never copy-pasted from one canonical source.

## 2. Geo-coordinates — two different points, ~600m apart

| Source | Latitude | Longitude |
|---|---|---|
| Shopify Admin billing address (authoritative merchant record) | 28.9897017 | 77.7044604 |
| `snippets/bk-local-business.liquid` (live Bakery JSON-LD) | 28.9931 | 77.6939 |

The file itself already carries an in-code warning (`⚠ Verify the geo latitude/longitude from
Google Maps for your exact shop pin`) predating this audit — so this was already flagged as
unverified, not something newly discovered. What this audit adds: the Shopify Admin record has its
own real coordinates, and they don't match the ones in the live schema. The ~600 m gap is enough to
misplace the pin on Google's Local Pack / Maps result for "cake shop near me" searches.
`snippets/tbk-schema-website.liquid`'s Organization schema has no geo block at all to cross-check
against.

## 3. Phone number — consistent value, inconsistent formatting only

Every source uses the same 10-digit number, `8218862928`. Formatting varies: `+918218862928`
(schema fields), `+91-8218862928` (header settings), `+91 8218862928` (Admin billing address,
Contact page prose). Not a data conflict — cosmetic only, no action needed beyond picking one format
if a style pass is ever done.

## 4. Email — fully consistent

`thebakingkaur@gmail.com` everywhere checked (Admin `contactEmail`, Contact page, footer, Refund
policy page, all schema files). No discrepancy found.

## 5. Opening hours — two different opening times live at once

| Source | Hours |
|---|---|
| `snippets/bk-local-business.liquid` `openingHoursSpecification` (live, every page) | **09:00–23:59**, all 7 days |
| `templates/page.contact-2.json` live Contact page (prose, ×2 occurrences) | "Open daily from **10:00 AM** to 12:00 Midnight" |

A 1-hour gap between the structured-data opening time (9 AM) and the on-page prose (10 AM). Closing
time is effectively the same (23:59 vs. "12:00 Midnight") once rounding is accounted for, so this is
narrower than the address issue, but it's still a real, live inconsistency between what Google reads
as structured data and what a human reads on the page — exactly the kind of mismatch Google's rich
results guidelines flag.

## 6. Delivery-area list — two different area lists live at once

Documented in full in [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md) §2; noted here because it's the
same class of issue:

- Live "Cake Delivery in Meerut" page: Thapar Nagar, Shastri Nagar, **Ganga Nagar**, **Partapur**,
  **Jagriti Vihar** and nearby localities.
- Live footer `service_areas` setting (`site-footer.liquid`): Thapar Nagar, Shastri Nagar, **Sadar
  Bazaar**, **Civil Lines**, **Pallavpuram**, Ganga Nagar & nearby areas.

Three areas (Sadar Bazaar, Civil Lines, Pallavpuram) appear only in the footer; two (Partapur,
Jagriti Vihar) appear only on the delivery page. Both are live at the same time.

## Organization/LocalBusiness schema coverage gap

`snippets/tbk-schema-website.liquid`'s `Organization` entity (renders sitewide) carries `telephone`
and a partial `PostalAddress` (locality/region/postal/country) but **no `streetAddress` and no
`geo` block**. `snippets/bk-local-business.liquid`'s `Bakery` entity carries the full address and
geo. This isn't a conflict by itself (Google should read the `Bakery` entity for local-pack
purposes), but it means the two schema blocks the site emits are not mirror copies of the same
facts — worth knowing before either one is edited in isolation.

## What this audit does NOT do

Per instruction, no value here is treated as "correct" and pushed live. In particular:

- The Shopify Admin billing address (source #A) is the most likely candidate for canonical, since
  it's the merchant's own account record rather than something typed into a theme file — but it
  itself doesn't exactly match any live on-site text, so confirming it with the business before using
  it as the single source is still necessary.
- The "Fatah" vs "Fateh" spelling needs a business call — a typo fix is safe once the correct
  spelling is confirmed, but which of the four wordings (or a fifth, cleaner one) becomes the
  standard text is not this audit's call to make.

## Recommendation (business decision required)

1. Confirm the single correct address (recommend starting from the Shopify Admin billing address,
   source A, since it's the account of record) and the single correct geo-coordinate pair (recommend
   a fresh Google Maps pin-drop, since neither existing pair is confirmed against the real storefront
   location).
2. Once confirmed, propagate the same text to: `bk-local-business.liquid`, `tbk-schema-website.liquid`
   (add the missing `streetAddress`/`geo`), `site-footer.liquid` default, `footer.liquid`,
   `tbk-footer.liquid`, `page.contact-2.json`, and the Refund & Return Policy page body. This is a
   single coordinated deploy, not five independent ones, to avoid re-introducing drift mid-fix.
3. Decide the real opening hours (9 AM or 10 AM start) and update whichever source is wrong.
4. The Shopify built-in Contact Information policy (source B) needs its malformed HTML
   (stray `<meta charset="utf-8">` tags) cleaned up regardless of which address wording is chosen —
   that's a technical defect, not a business decision, and is being flagged here since it was found
   during this pass, but a Shop Policy body is edited in Shopify Admin → Settings → Policies, not via
   the theme, and is out of this session's write scope.

## Related

[POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md), [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md),
[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md) (SEO-015, SEO-029).
