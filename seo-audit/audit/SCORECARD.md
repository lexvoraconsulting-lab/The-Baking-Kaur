# Scorecard

No numeric scores are fabricated here. Per this repo's standing principle (`CLAUDE.md`:
"verifiability beats persuasion") and this audit's own explicit instruction ("never fabricate
findings or scores"), each category is a qualitative band with the specific evidence behind it —
not an invented 1-10 or percentage figure with no defensible basis.

| Category | Band | Basis |
|---|---|---|
| **Overall Website Health** | Improving, real gaps remain | 15 verified defects found and fixed across 3 audit passes (fabrication/placeholder content, plus duplicate/misplaced schema); 8 more identified and logged, open |
| **Technical SEO** | Adequate (Verified), one context caveat | Canonical tags, viewport meta, conditional meta description all correctly dynamic in `layout/theme.liquid`; `robots.txt` clean, no crawl traps. Whole site is intentionally password-gated (SEO-022, confirmed by the business, not a defect) — most live-crawl checks aren't meaningful until that lifts |
| **Schema** | **Was Critical (duplicate Product on all 602 active products), now fixed (Verified)** | SEO-023 (duplicate/conflicting Product schema, all active products), SEO-024 (sitewide unconditional FAQPage), SEO-020 (sameAs inconsistency) all resolved this pass — see [../schema/SCHEMA_SCORECARD.md](../schema/SCHEMA_SCORECARD.md) for per-entity detail |
| **Content SEO** | **Critical gap (Verified)** | Both real FAQ page templates show Lorem Ipsum placeholder text live (SEO-013) — an FAQ page with gibberish is actively worse than no FAQ page |
| **GEO / AI Search Readiness** | Estimated — structurally sound, content-limited | Schema (WebSite/Organization/Breadcrumb/CollectionPage/Article/Product, see [../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md)) is well-built, dynamic, and — as of this pass — free of duplicate/conflicting entities. `FAQPage` schema on the two dedicated FAQ pages still wraps placeholder content (SEO-013, unresolved) — actively hurts AI-citation trust until real content lands; the *sitewide, unconditional* copy of this same schema (SEO-024) is now fixed and no longer a separate duplication risk |
| **Local SEO** | Adequate, one unverified input | Real `LocalBusiness`/`Bakery` schema present with genuine phone/address; geo-coordinates explicitly flagged in-code as unverified (SEO-015) |
| **UX / CRO** | Not assessable this pass | Storefront is password-gated; no live page render available to test against real users |
| **Security** | Adequate (Verified, within scope reviewed) | HTTPS via Shopify default; no exposed credentials, no mixed-content pattern found in the files reviewed this pass — full audit not run (see [../security/SECURITY_AUDIT.md](../security/SECURITY_AUDIT.md) for exact scope) |
| **EEAT** | Was Critical, now substantially improved | 12 fabricated trust-signal instances removed this session — a materially larger problem than `CLAUDE.md` alone had tracked (it knew of 1, this audit found 12). Still 0 real reviews and no FSSAI licence number, both already tracked as client-blocked in `CLAUDE.md`, not new findings |

## What would change this scorecard

- SEO-013 resolved (real FAQ content) → Content SEO and GEO Readiness bands both improve materially.
- SEO-016 resolved (header rating claim decision) → EEAT closes its last known open fabrication.
- Password gate lifted → Technical SEO, UX/CRO become assessable against real live pages.
- Admin API reconnected → SEO-017/018 resolve, confirming exact liveness/urgency of several already-fixed items.
- SEO-021 resolved (Shopify Liquid `article` object's real update-timestamp property confirmed or refuted).

## Related

[AUDIT_LEDGER.md](AUDIT_LEDGER.md), [../final/EXECUTIVE_REPORT.md](../final/EXECUTIVE_REPORT.md).
