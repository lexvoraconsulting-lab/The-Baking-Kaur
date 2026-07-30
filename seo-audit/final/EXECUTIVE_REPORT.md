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
mobile header. 11 more identified and logged as open — none silently ignored, each requires either
a business decision, real business content, or a currently-blocked tool/live-site check to close
out.

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

## Remaining Risks

1. **Both FAQ page templates show placeholder Lorem Ipsum content, live** (SEO-013) — the top
   priority; needs real business content, not an invented fix.
2. **The original header "★4.9 Rated" claim is still live** (SEO-016) — `CLAUDE.md` has required
   your explicit go-ahead for this since before this audit began; still outstanding.
3. Geo-coordinates, founding-year claim, and real customer-count all need a business-side
   confirmation before they can be fully closed out (SEO-014, 015, 018).
4. Shopify Admin API access disconnected mid-session — several "is this actually live" questions
   (SEO-017) need it reconnected to answer definitively.
5. A hidden, duplicate `<h1>` renders sitewide (SEO-025, Low) — not fixed, needs a
   template-by-template heading check first.
6. Three-way NAP/address inconsistency across the theme (SEO-029) — needs the business's real,
   current, complete address; not guessed at.
7. A fake Ecomus demo "Store Locations" page exists (SEO-030) — needs a decision on whether to
   delete, repurpose, or leave as unused dead code.

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

- **BUILD-008 (Technical SEO)**: done for what's code-verifiable — `lang` attribute, canonical
  tags confirmed correct; one real Core Web Vitals fix found and applied (SEO-026, folded in here
  since it surfaced during the same code sweep); one minor item logged, not fixed (SEO-025).
  Duplicate-title/thin-page/redirect-chain checks remain genuinely blocked — they need a live crawl
  or bulk Admin API export, neither available (site gated, MCP disconnected, re-checked this pass).
- **BUILD-009 (Core Web Vitals)**: partially covered by SEO-026 above. A real Lighthouse/PageSpeed
  score cannot be produced — the storefront is password-gated, and no PageSpeed Insights API access
  exists this session. Not claimed as done.
- **BUILD-010 (AI Search/GEO)**: no new repo-based findings beyond what SEO-024 (schema) already
  fixed. Real citation-behavior testing needs live AI-search tools, not attempted.
- **BUILD-011 (Local SEO)**: real, new findings this pass — a live demo-store link removed
  (SEO-027) and a genuine 3-way address inconsistency surfaced (SEO-029, open, needs the business's
  real address). Geo-coordinates (SEO-015) remain unverified.
- **BUILD-012 (Content + EEAT)**: one new finding — a fake Ecomus demo store-locations page
  (SEO-030, open, needs a page-scope decision) — otherwise unchanged from the first audit pass'
  12 fixed fabrication issues.
- **BUILD-013 (UX/CRO) through BUILD-015 (Launch Readiness)**: not started. UX/CRO fundamentally
  needs a live rendered page (site still gated) or Admin API (still disconnected — reconnection was
  attempted again this pass and failed the same way; see [[storefront-seo-audit-2026-07-29]] for
  what's blocked by it). Starting them now without either would mean fabricating findings — not
  done here.

Recommended continuation: reconnect the Shopify Admin API and/or lift the password gate first —
both unblock most of the remaining phases at once, more efficiently than continuing to search for
code-level-only findings in categories that fundamentally need live data.
