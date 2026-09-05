# Schema Changelog

Schema-scoped subset of [`../audit/CHANGELOG.md`](../audit/CHANGELOG.md) — deploy-safety evidence
specifically for schema.org/JSON-LD changes. The prior two commits (`52a3821`, `eaad74f`) were
content-fabrication fixes, not schema changes; this is the first entry.

## 2026-07-30 — Commit `4d23a2e`: remove duplicate Product schema, gate sitewide FAQPage, fix sameAs

**Files**: `snippets/tbk-schema-website.liquid`, `snippets/structured-data.liquid`,
`sections/main-product-premium-v2.liquid`, `sections/main-product-premium.liquid`,
`layout/theme.liquid`.

**Issues closed**: SEO-020, SEO-023, SEO-024.

**Discovery method**: `grep -rhoE '"@type":\s*"[^"]+"' sections/*.liquid snippets/*.liquid layout/*.liquid | sort -u`
— enumerating every `@type` actually emitted anywhere in the theme, not just the files already known
from the first schema pass, surfaced `Offer`/`Brand`/`MerchantReturnPolicy`/`OfferShippingDetails`
in product section files and `FAQPage`/`Question`/`Answer` in `layout/theme.liquid` — none of which
the first pass had traced to their source files.

**Deploy safety**: `shopify theme pull --only <file>` into a scratch path for all 5 files → diff
`--strip-trailing-cr` against `git show HEAD:<path>`. Four files: zero drift. `layout/theme.liquid`:
real drift found (two `render` calls in git, absent live) — reconciled by adopting the live version
as the new local baseline *before* applying the FAQPage-gate edit, so the eventual push carried
exactly one intentional change to that file. Edited all 5 → `shopify theme push --allow-live --only
<file>` for all 5 in one push → re-pulled → diffed against the edited local copies → confirmed
byte-for-byte live for all 5 before committing.

## Related

[../issues.yml](../issues.yml), [SCHEMA_AUDIT.md](SCHEMA_AUDIT.md), [../audit/CHANGELOG.md](../audit/CHANGELOG.md).
