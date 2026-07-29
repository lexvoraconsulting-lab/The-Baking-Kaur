# Executive Report — Storefront Audit, 2026-07-29

`thebakingkaur.com` / theme `151307485353`. Full detail in the category reports linked throughout;
this is the summary. No score below is invented — each is a qualitative band backed by cited
evidence, per this audit's own explicit "never fabricate scores" instruction. Full ledger:
[`../audit/AUDIT_LEDGER.md`](../audit/AUDIT_LEDGER.md); machine-readable source of truth:
[`../issues.yml`](../issues.yml).

## Overall Website Health: Improving, real gaps remain

12 verified content-fabrication and placeholder defects found and fixed across two audit passes and
two live deployments (commits `52a3821`, `eaad74f`). 10 more identified and logged as open — none
silently ignored, each requires either a business decision, real business content, or a
currently-disconnected tool to close out.

## Category Scores (qualitative, evidence-linked — see [SCORECARD.md](../audit/SCORECARD.md) for full basis)

| Category | Band |
|---|---|
| Technical SEO | Adequate (Verified) — clean `robots.txt`, correct dynamic canonicals; site is intentionally password-gated, limiting live-crawl checks |
| Content SEO | **Critical gap (Verified)** — both real FAQ page templates show Lorem Ipsum, live |
| GEO / AI Search Readiness | Estimated — schema foundation is strong and dynamic; FAQ gap actively hurts AI-citation trust |
| Local SEO | Adequate, one unverified input (geo-coordinates) |
| UX / CRO | Not assessable this pass — site gated, no live render available |
| Security | Adequate within the narrow scope reviewed — not a full security audit |
| EEAT | Was Critical, now substantially improved — 12 fabrication instances removed (more than `CLAUDE.md` alone had tracked); still 0 real reviews, no FSSAI number (both already known, client-blocked) |

## What changed this session

**Removed** (never replaced with a different invented claim — deleted outright, per the
verifiability-over-persuasion standard already established for this project):
- Six instances of fabricated "Google Rated"/"Top Rated" claims across the active product template,
  an alternate product template, and both product templates' footer.
- An entire fabricated "Customer Reviews" section with four invented customer names and quotes —
  the single most serious finding, a repeat of a violation already documented as "permanently
  closed."
- Three more unsourced "20,000+ Customers" count claims found by a second, broader sweep — including
  one on the **actually-live** footer (`site-footer.liquid`), after discovering the first footer fix
  (`tbk-footer.liquid`) had targeted a file not wired into the live theme at all.

**Fixed** (replaced with real, verified information):
- A page-builder app's leftover placeholder email (`EComposer@example.com`) across three templates,
  replaced with the shop's real, verified email.

## Remaining Risks

1. **Both FAQ page templates show placeholder Lorem Ipsum content, live** (SEO-013) — the top
   priority; needs real business content, not an invented fix.
2. **The original header "★4.9 Rated" claim is still live** (SEO-016) — `CLAUDE.md` has required
   your explicit go-ahead for this since before this audit began; still outstanding.
3. Geo-coordinates, founding-year claim, and real customer-count all need a business-side
   confirmation before they can be fully closed out (SEO-014, 015, 018).
4. Shopify Admin API access disconnected mid-session — several "is this actually live" questions
   (SEO-017) need it reconnected to answer definitively.

## Top Priorities for Launch

1. Real FAQ content (or remove the FAQ pages until it exists) — SEO-013.
2. Decide on the header rating claim — SEO-016.
3. Confirm the Google Maps geo-coordinates — SEO-015.
4. Reconnect Admin API, re-verify template-assignment and real customer-count questions before
   concluding the site is launch-ready — SEO-017, SEO-018.
5. Re-check `sitemap.xml` the moment the password gate lifts — SEO-019.

## Stop condition reached

Per this audit's own instruction ("continue until no Critical or High-priority verified issues
remain"): every remaining Critical/High item (SEO-013, SEO-016) requires either business-supplied
content or your explicit decision — not something this audit can resolve by continuing to search
the codebase. Stopping here is the correct application of that stop condition, not an early exit.

## Full report index

[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md) ·
[../audit/VERIFIED_ISSUES.md](../audit/VERIFIED_ISSUES.md) ·
[../audit/MANUAL_VERIFICATION.md](../audit/MANUAL_VERIFICATION.md) ·
[../audit/CHANGELOG.md](../audit/CHANGELOG.md) ·
[../audit/SCORECARD.md](../audit/SCORECARD.md) ·
[../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md) ·
[../seo/TECHNICAL_SEO.md](../seo/TECHNICAL_SEO.md) ·
[../seo/ONPAGE_SEO.md](../seo/ONPAGE_SEO.md) ·
[../seo/LOCAL_SEO.md](../seo/LOCAL_SEO.md) ·
[../seo/GEO_AUDIT.md](../seo/GEO_AUDIT.md) ·
[../ux/UX_AUDIT.md](../ux/UX_AUDIT.md) ·
[../ux/CRO_AUDIT.md](../ux/CRO_AUDIT.md) ·
[../security/SECURITY_AUDIT.md](../security/SECURITY_AUDIT.md) ·
[../issues.yml](../issues.yml)
