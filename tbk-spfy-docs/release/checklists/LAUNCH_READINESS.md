# Launch Readiness

**Status: the site is already live** (theme `#151307485353`, password-gated). This document
assesses readiness for *removing the password gate* / full public launch, not a from-scratch
launch — that distinction matters since some "launch readiness" concerns (theme stability, data
integrity) are already satisfied by production operation to date.

## Ready now

- Theme architecture: certified (`docs/FINAL_REPORT.md`)
- Redirects: clean, chains fixed (`docs/CRAWL_REPORT.md`)
- Canonical/robots/sitemap: sound (`docs/TECHNICAL_SEO_AUDIT.md`)
- Product title SEO: 100% compliant, unique (`docs/SHOPIFY_SEO_REPORT.md`)
- No hardcoded secrets, no unsafe code-execution patterns (`docs/SECURITY_AUDIT.md`)
- 1 real XSS vector closed (`docs/SECURITY_AUDIT.md` SEC-002)

## NOT ready — should be resolved before removing the password gate

1. **Meta-description duplication (84% of active products)** — going fully public means Google
   will crawl and index this duplication immediately; better to resolve before unlock than after.
2. **SEC-001 (vendor phone-home)** — going public increases the population of real customers
   whose adjacent store traffic could be affected if this check ever fails/degrades visibly;
   resolve the licensing question before wider exposure, not after.
3. **FSSAI licence number, 0 verified reviews, watermarked catalogue photography** (`CLAUDE.md`'s
   own roadmap) — these are trust-signal gaps that matter more once real public traffic and
   potential customers, not just this engineering program, are looking at the site.

## Can be resolved in parallel with launch, not blocking

- `shine-trust.liquid` decision, `tbk-product.liquid` removal, FAQPage schema restructuring — all
  real but lower-severity than the 3 items above.
- B1–B6 business items already tracked.

## Recommended launch sequence

1. Resolve items 1–3 above (all business decisions, no new engineering discovery needed).
2. Unlock the password gate (or arrange an authenticated pre-launch QA pass).
3. Run real Lighthouse/PSI, Search Console, and Merchant Center verification for the first time.
4. Re-score `docs/PROJECT_SCORECARD.md` with real (not architecture-only) data.
5. Launch.

## Related

[ENTERPRISE_CERTIFICATION.md](ENTERPRISE_CERTIFICATION.md), [PROJECT_SCORECARD.md](PROJECT_SCORECARD.md),
[FINAL_EXECUTIVE_REPORT.md](FINAL_EXECUTIVE_REPORT.md).
