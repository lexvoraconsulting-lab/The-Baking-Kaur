# Schema Validation Checklist

What's been validated by direct code inspection this session, versus what still needs an external
validator (Google Rich Results Test, Schema Markup Validator) once the storefront is publicly
reachable. The password gate (SEO-022) blocks every external-tool row below — none of them are
guessed at or assumed passing.

## Validated by code inspection (Verified)

| Check | Result | How |
|---|---|---|
| JSON syntax (structural) | Pass | Every block manually read; braces/brackets balanced, no orphaned Liquid tags after edits (checked explicitly after each edit this pass) |
| No duplicate `Product` entity per page | **Pass, as of `4d23a2e`** | SEO-023 fixed — traced every product template's rendering path |
| No fabricated `AggregateRating`/`Review` | Pass | Confirmed absent theme-wide; native filter can't fabricate them (no review data exists to draw from) |
| `FAQPage` matches visible page content | **Pass, as of `4d23a2e`** (schema placement) / **Fail** (content) | SEO-024 fixed the sitewide-rendering violation; the two real FAQ pages still show Lorem Ipsum (SEO-013, open) so schema-content mismatch persists there specifically |
| Entity relationships (`@id` cross-references) | Partial | See [ENTITY_GRAPH.md](ENTITY_GRAPH.md) — `Organization`/`WebSite` link correctly; `Bakery` entity doesn't share an `@id` with `Organization` |
| Deprecated schema.org properties | None found | No deprecated property names encountered in any reviewed block |

## Requires an external validator (Requires Manual Verification — site is password-gated)

| Check | Tool needed | Blocked by |
|---|---|---|
| Google Rich Results Test eligibility (per page type) | [Google Rich Results Test](https://search.google.com/test/rich-results) | Storefront password gate — the tool needs a publicly fetchable URL |
| Schema Markup Validator (schema.org compliance) | [validator.schema.org](https://validator.schema.org) | Same |
| Merchant Center feed compatibility | Google Merchant Center | Same, plus requires an actual Merchant Center account connection this session doesn't have |
| Real rendered JSON-LD matches the Liquid source (no runtime templating bug) | Any live page view | Same |

## How to close these out

The moment the password gate lifts (SEO-022), re-run this checklist against at least: the homepage,
one product on each of the 4 product templates (default, premium, hampers-template, tbk), one
collection page, one blog article, and both FAQ pages — that combination exercises every schema type
in [SCHEMA_AUDIT.md](SCHEMA_AUDIT.md)'s enumeration at least once.

## Related

[SCHEMA_AUDIT.md](SCHEMA_AUDIT.md), [RICH_RESULTS_REPORT.md](RICH_RESULTS_REPORT.md).
