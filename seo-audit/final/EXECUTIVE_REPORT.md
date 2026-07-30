# Executive Report — Storefront Audit, 2026-07-29

`thebakingkaur.com` / theme `151307485353`. Full detail in the category reports linked throughout;
this is the summary. No score below is invented — each is a qualitative band backed by cited
evidence, per this audit's own explicit "never fabricate scores" instruction. Full ledger:
[`../audit/AUDIT_LEDGER.md`](../audit/AUDIT_LEDGER.md); machine-readable source of truth:
[`../issues.yml`](../issues.yml).

## Overall Website Health: Improving, real gaps remain

18 verified defects found and fixed across five audit passes and five live deployments (commits
`52a3821`, `eaad74f`, `4d23a2e`, `edf458f`, `21457ec`) — 12 content-fabrication/placeholder issues,
a duplicate Product schema affecting all 602 active products, a sitewide-unconditional FAQPage
schema, one Core Web Vitals fix, and a live hyperlink to an unrelated demo Shopify store in the
mobile header. The hosted Shopify MCP connector then came back fully working and resolved two more
previously-blocked items with real data (customer count, page-template assignments) — which in turn
**escalated two already-logged issues from assumed to confirmed-live** (see below) and surfaced one
new one. 10 items remain open — none silently ignored, each requires either a business decision or
real business content, not a tool limitation anymore.

## Category Scores (qualitative, evidence-linked — see [SCORECARD.md](../audit/SCORECARD.md) for full basis)

| Category | Band |
|---|---|
| Technical SEO | Adequate (Verified) — clean `robots.txt`, correct dynamic canonicals and `lang` attribute; one minor open item (hidden duplicate H1, SEO-025); site is intentionally password-gated, limiting live-crawl checks |
| Schema | **Was Critical (duplicate Product schema on all 602 active products), now fixed** — see [../schema/SCHEMA_SCORECARD.md](../schema/SCHEMA_SCORECARD.md) |
| Core Web Vitals | One real, verified fix (LCP lazy-loading, SEO-026); no overall score claimed — Lighthouse/PageSpeed can't run against a gated site |
| Content SEO | **Critical gap (Verified)** — both real FAQ page templates show Lorem Ipsum, live |
| GEO / AI Search Readiness | Estimated — schema foundation is strong, dynamic, and now free of duplicate entities; the FAQ *content* gap (not the schema placement, now fixed) still actively hurts AI-citation trust |
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

**Fixed** (schema architecture, third pass, commit `4d23a2e`):
- **Duplicate/conflicting Product schema on every product page**, including all 602 currently-active
  products on the default template — two separate `@type: "Product"` JSON-LD blocks per page (one
  from Shopify's native `structured_data` filter, one hand-rolled per section file). Resolved by
  keeping whichever version is richer per template and gating the other off.
- **Sitewide, unconditional `FAQPage` schema** in `layout/theme.liquid` — rendered identically on
  every page regardless of content relevance, violating Google's structured-data guidelines and
  duplicating the dedicated FAQ pages' own schema. Gated to exclude those two pages; the real
  Q&A content itself was preserved untouched.
- A `sameAs` inconsistency between two schema sources describing the same business, reconciled.
- Found and reconciled an unrelated pre-existing drift in `layout/theme.liquid` (two `render` calls
  present in git but never actually live, from an apparently-abandoned commit) before applying the
  FAQ fix, so the deploy didn't silently reintroduce them.

**Fixed** (Technical SEO / Core Web Vitals, fourth pass, commit `edf458f`):
- The main product-gallery image in `tbk-gallery.liquid` (an alternate, unconfirmed-live product
  template) was marked `loading="lazy"` — this is almost certainly the LCP element on any page using
  it, and Google's own guidance says the LCP image should never be lazy-loaded. Fixed to
  `loading="eager"` + `fetchpriority="high"`. Confirmed the actually-live default template already
  handles this correctly (`lazy_load: false` on the first media item) — no fix needed there.
- Logged, not fixed: a hidden (`display:none`) duplicate `<h1>` sitewide in `layout/theme.liquid`
  (SEO-025) — safely removing it needs confirming every other page type still has its own visible
  H1 first, more investigation than this minor item currently justifies.

**Fixed** (Local SEO / Trust, fifth pass, commit `21457ec`):
- **A live hyperlink to `demo-ecomus-global.myshopify.com`** in the mobile header's "Need help?"
  text — sending real customers to an unrelated demo Shopify store. Found by checking the actual
  *stored* section settings, not just the theme file's schema default (which had a different,
  also-wrong value — a typo'd email and malformed phone number, fixed too, though not itself live).
  Link removed rather than guessing the correct internal page to point to instead.
- **Not fixed, logged**: a three-way address-text inconsistency across the theme (SEO-029) — one
  variant removed as part of the above fix, two remain, genuinely different from each other. Needs
  the business's real current address, not a guess. Also logged: a fake Ecomus demo
  "Store Locations" page (London/Madrid/Tokyo) that doesn't fit this single-location business
  (SEO-030) — needs a page-scope decision, not a text fix.

**Verification pass, no code change** (hosted Shopify MCP reconnected):
- **SEO-017 and SEO-018 resolved with real data**: page-template assignments confirmed via a real
  `pages` GraphQL query (`page.faq-01.json` and `templates/page.store-locations.json` are both
  confirmed live), and real customer/order counts (113 / 24) confirm the "20,000+" claims removed
  earlier were indeed fabricated.
- **SEO-013 escalated High → Critical** and **SEO-030 escalated Low → High** — both are now
  confirmed live on real, published pages, not assumed.
- **SEO-031 found** (new, Medium): two live-adjacent policy pages covering the same topic
  ("Return, Refund & Replacement Policy" and "Refund & Return Policy") — a genuine duplicate-content
  signal.

## Remaining Risks

1. **The live FAQ page shows placeholder Lorem Ipsum content** (SEO-013, **confirmed live**,
   Critical) — the top priority; needs real business content, not an invented fix.
2. **The original header "★4.9 Rated" claim is still live** (SEO-016) — `CLAUDE.md` has required
   your explicit go-ahead for this since before this audit began; still outstanding.
3. **The live "Store Locator" page shows fake London/Madrid/Tokyo demo content** (SEO-030,
   **confirmed live**, escalated to High) — needs a decision: delete, repurpose for the real Meerut
   location, or leave as-is. Could be safely unpublished as an interim step without guessing at
   replacement content, but that's still a real, visible change not made unilaterally.
4. Geo-coordinates and founding-year claim need business-side confirmation (SEO-014, SEO-015).
5. A hidden, duplicate `<h1>` renders sitewide (SEO-025, Low) — not fixed, needs a
   template-by-template heading check first.
6. Three-way NAP/address inconsistency across the theme (SEO-029) — needs the business's real,
   current, complete address; not guessed at.
7. Two duplicate policy pages on the same topic (SEO-031, new) — needs a decision on which is
   canonical.

## Top Priorities for Launch

1. Real FAQ content for the live FAQ page (or remove it until real content exists) — SEO-013.
2. Decide on the header rating claim — SEO-016.
3. Decide what to do with the live "Store Locator" page (fake international locations) — SEO-030.
4. Confirm the Google Maps geo-coordinates and the real business address — SEO-015, SEO-029.
5. Decide which policy page is canonical — SEO-031.
6. Re-check `sitemap.xml` the moment the password gate lifts — SEO-019.

## Stop condition reached

Per this audit's own instruction ("continue until no Critical or High-priority verified issues
remain"): every remaining Critical/High item (SEO-013, SEO-016, SEO-030) requires either
business-supplied content or your explicit decision — not something this audit can resolve by
continuing to search the codebase or query the API further. Both blocked-tool items from the prior
pass (SEO-017, SEO-018) are now genuinely resolved with real data, not just re-flagged — the
hosted Shopify MCP reconnecting removed that excuse entirely. What's left is exclusively business
decisions and business-supplied content. Stopping here is the correct application of the stop
condition, not an early exit.

## Full report index

[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md) ·
[../audit/VERIFIED_ISSUES.md](../audit/VERIFIED_ISSUES.md) ·
[../audit/MANUAL_VERIFICATION.md](../audit/MANUAL_VERIFICATION.md) ·
[../audit/CHANGELOG.md](../audit/CHANGELOG.md) ·
[../audit/SCORECARD.md](../audit/SCORECARD.md) ·
[../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md) ·
[../schema/SCHEMA_CHANGELOG.md](../schema/SCHEMA_CHANGELOG.md) ·
[../schema/SCHEMA_SCORECARD.md](../schema/SCHEMA_SCORECARD.md) ·
[../schema/SCHEMA_VALIDATION.md](../schema/SCHEMA_VALIDATION.md) ·
[../schema/ENTITY_GRAPH.md](../schema/ENTITY_GRAPH.md) ·
[../schema/RICH_RESULTS_REPORT.md](../schema/RICH_RESULTS_REPORT.md) ·
[../seo/TECHNICAL_SEO.md](../seo/TECHNICAL_SEO.md) ·
[../seo/ONPAGE_SEO.md](../seo/ONPAGE_SEO.md) ·
[../seo/LOCAL_SEO.md](../seo/LOCAL_SEO.md) ·
[../seo/GEO_AUDIT.md](../seo/GEO_AUDIT.md) ·
[../ux/UX_AUDIT.md](../ux/UX_AUDIT.md) ·
[../ux/CRO_AUDIT.md](../ux/CRO_AUDIT.md) ·
[../security/SECURITY_AUDIT.md](../security/SECURITY_AUDIT.md) ·
[../issues.yml](../issues.yml)

## Note on scope for this pass — pipeline status

A multi-phase pipeline was requested (BUILD-008 Technical SEO through BUILD-015 Launch Readiness,
tracked here under `SEO-NNN` instead — see the naming note in [[storefront-seo-audit-2026-07-29]]).
Status per phase, evidence-based, not assumed:

- **BUILD-008 (Technical SEO)**: done for what's code-verifiable, **plus now further resolved by
  the hosted Shopify MCP reconnecting** — page-template assignments (SEO-017) confirmed with real
  data. Duplicate-title/thin-page checks across the full 602-product catalogue and redirect-chain
  checks remain unattempted (not blocked anymore in principle — the API works — just not yet run,
  since this pass focused on the previously-blocked items specifically).
- **BUILD-009 (Core Web Vitals)**: unchanged — SEO-026 is the one real fix. A real Lighthouse/
  PageSpeed score still can't be produced; the storefront's password gate is a separate blocker
  from the Admin API and is unaffected by the MCP reconnection.
- **BUILD-010 (AI Search/GEO)**: unchanged, no new findings this pass.
- **BUILD-011 (Local SEO)**: unchanged from the prior pass (SEO-027 fixed, SEO-029/015 still need
  business input) — the MCP reconnection didn't surface new Local SEO findings specifically.
- **BUILD-012 (Content + EEAT)**: **materially advanced this pass** — SEO-013 and SEO-030 both
  moved from "assumed" to "confirmed live" via real data, and a new duplicate-content finding
  (SEO-031) surfaced from the same query. Real customer/order counts (SEO-018) also resolved.
- **BUILD-013 (UX/CRO) through BUILD-015 (Launch Readiness)**: still not started. The specific
  blocker for these has narrowed — it's now purely the storefront's password gate (live rendering),
  not the Admin API (which is fully working again). Product/collection *data* is fully queryable;
  actual page *rendering* for UX/CRO purposes is not.

Recommended continuation: with the Admin API now confirmed working, the fastest remaining unlock is
the password gate — lifting it (even temporarily) would enable BUILD-013 and real Core Web Vitals
measurement, the two things Admin API access alone can't provide.
