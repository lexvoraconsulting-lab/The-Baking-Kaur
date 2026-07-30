# Scorecard

No numeric scores are fabricated here. Per this repo's standing principle (`CLAUDE.md`:
"verifiability beats persuasion") and this audit's own explicit instruction ("never fabricate
findings or scores"), each category is a qualitative band with the specific evidence behind it —
not an invented 1-10 or percentage figure with no defensible basis.

| Category | Band | Basis |
|---|---|---|
| **Overall Website Health** | Improving, real gaps remain | 24 verified defects found and fixed across 6 audit passes; 2 previously-blocked items resolved with real Admin API data rather than fixed; 8 more identified and logged, open, each needing a business decision or business input |
| **Technical SEO** | Adequate (Verified), one context caveat, one minor open item | Canonical tags, viewport meta, conditional meta description, `lang` attribute all correctly dynamic; `robots.txt` clean, no crawl traps. Whole site is intentionally password-gated (SEO-022, not a defect) — most live-crawl checks aren't meaningful until that lifts. One minor open item: a hidden duplicate `<h1>` sitewide (SEO-025, Low) |
| **Core Web Vitals** | One real fix made (Verified), rest not measurable | LCP-image lazy-loading bug found and fixed (SEO-026) via code inspection; the default live template was already correct. No Lighthouse/PageSpeed score exists or is claimed — the password gate blocks real measurement |
| **Schema** | **Was Critical (duplicate Product on all 602 active products), now fixed (Verified)** | SEO-023 (duplicate/conflicting Product schema, all active products), SEO-024 (sitewide unconditional FAQPage), SEO-020 (sameAs inconsistency) all resolved — see [../schema/SCHEMA_SCORECARD.md](../schema/SCHEMA_SCORECARD.md) for per-entity detail |
| **Content SEO** | **Was Critical, materially improved (Verified)** | SEO-013 fixed: the live FAQ page's Lorem Ipsum replaced with 19 topics of real, evidence-based content. Remaining open: a fake Ecomus "Store Locator" page, unpublished not deleted (SEO-030, replacement spec ready — [../final/DELIVERY_AREA_SPEC.md](../final/DELIVERY_AREA_SPEC.md)); an empty live "Terms and Conditions" page (SEO-034); a fabricated "20,000+ celebrations" claim found on a live Page body and fixed (SEO-032) |
| **GEO / AI Search Readiness** | Improving — FAQ content gap closed | The live FAQ page's `FAQPage` schema now wraps 19 real Q&A pairs instead of placeholder text (SEO-013) — no new schema code was needed, since `sections/accordion.liquid` already emits per-item Microdata dynamically. Schema itself (WebSite/Organization/Breadcrumb/CollectionPage/Article/Product) remains well-built and free of duplicate/conflicting entities |
| **Local SEO** | Adequate schema, real NAP-consistency gap, now fully quantified | Real `LocalBusiness`/`Bakery` schema present. Full address audit this pass ([../final/ADDRESS_AUDIT.md](../final/ADDRESS_AUDIT.md)) found **4 distinct address wordings and 2 different geo-coordinate pairs (~600m apart)** live simultaneously (SEO-015, SEO-029, SEO-036), plus two conflicting delivery-area lists (SEO-035) and a 1-hour opening-time discrepancy — all need one business-confirmed answer, not guessed here |
| **UX / CRO** | Not assessable sitewide; one real fix made | Storefront is password-gated, so no live page render is available for broad user testing. One concrete fix landed anyway: the live Contact page's `tel:`/WhatsApp links were silently broken (missing the phone number in both `href`s) — fixed and deployed (SEO-033) |
| **Security** | Adequate (Verified, within scope reviewed) | HTTPS via Shopify default; no exposed credentials, no mixed-content pattern found in the files reviewed this pass — full audit not run (see [../security/SECURITY_AUDIT.md](../security/SECURITY_AUDIT.md) for exact scope) |
| **EEAT** | Was Critical, now substantially improved, one new legal-conflict finding | 12 fabricated trust-signal instances removed in prior passes, a 13th ("20,000+ celebrations," SEO-032) found and fixed this pass. The header rating claim (SEO-016) was confirmed already-fixed, not newly fabricated. New, more serious finding: live Refund/Terms policies materially contradict each other on real customer rights (SEO-031, escalated Medium→Critical — [../final/POLICY_CONSOLIDATION.md](../final/POLICY_CONSOLIDATION.md)), and 3 of 4 built-in Shop Policies name the business "The Bakery Kaur" (wrong). Still 0 real reviews, no FSSAI licence number, no named founder, no GST number surfaced — all catalogued in [../final/EEAT_REPORT.md](../final/EEAT_REPORT.md), all business-blocked, not new defects this pass except where noted |

## What would change this scorecard

- SEO-031 resolved (business confirms real refund/cancellation terms, Shop Policies corrected to
  match and to fix the wrong business name) → EEAT and Content SEO both improve materially; this is
  now the single highest-value remaining item.
- SEO-015/029/036 resolved (one confirmed address + fresh geo pin, applied everywhere) → Local SEO
  closes its NAP-consistency gap entirely.
- SEO-035 resolved (one confirmed delivery-area list) → unblocks a real Delivery Areas page
  (SEO-030's replacement spec) and an `areaServed` schema upgrade.
- SEO-034 resolved (real Terms content or unpublish) → closes the last known empty-legal-page gap.
- Password gate lifted → Technical SEO, UX/CRO become assessable against real live pages.
- SEO-021 resolved (Shopify Liquid `article` object's real update-timestamp property confirmed or refuted).

## Related

[AUDIT_LEDGER.md](AUDIT_LEDGER.md), [../final/EXECUTIVE_REPORT.md](../final/EXECUTIVE_REPORT.md).
