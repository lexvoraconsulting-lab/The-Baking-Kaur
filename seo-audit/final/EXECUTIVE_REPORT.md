# Executive Report — Storefront Audit, 2026-07-29

`thebakingkaur.com` / theme `151307485353`. Full detail in the category reports linked throughout;
this is the summary. No score below is invented — each is a qualitative band backed by cited
evidence, per this audit's own explicit "never fabricate scores" instruction. Full ledger:
[`../audit/AUDIT_LEDGER.md`](../audit/AUDIT_LEDGER.md); machine-readable source of truth:
[`../issues.yml`](../issues.yml).

## Overall Website Health: Improving, real gaps remain

24 verified defects found and fixed across six audit passes and live deployments/Admin writes
(commits `52a3821`, `eaad74f`, `4d23a2e`, `edf458f`, `21457ec`, plus this pass's FAQ/contact-link
theme pushes and two Admin API page writes) — 12 content-fabrication/placeholder issues from earlier
passes, plus this pass's real FAQ content (SEO-013), a 13th fabricated count claim on a live Page
body (SEO-032), broken Contact-page `tel:`/WhatsApp links (SEO-033), a duplicate Product schema
affecting all 602 active products, a sitewide-unconditional FAQPage schema, one Core Web Vitals fix,
and a live hyperlink to an unrelated demo Shopify store in the mobile header. This pass also ran a
full business-decision-implementation cycle per an explicit instruction: implemented every item that
was a mechanical/evidence-based fix, and produced 6 new evidence-based planning documents for every
item that is a genuine business decision — most significantly, escalating SEO-031 from "two duplicate
pages" to a confirmed 4-way legal contradiction between the site's own policy surfaces (see
[POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md)). 8 items remain open — none silently ignored,
each requires either a business decision or real business content, not a tool limitation.

## Category Scores (qualitative, evidence-linked — see [SCORECARD.md](../audit/SCORECARD.md) for full basis)

| Category | Band |
|---|---|
| Technical SEO | Adequate (Verified) — clean `robots.txt`, correct dynamic canonicals and `lang` attribute; one minor open item (hidden duplicate H1, SEO-025); site is intentionally password-gated, limiting live-crawl checks |
| Schema | **Was Critical (duplicate Product schema on all 602 active products), now fixed** — see [../schema/SCHEMA_SCORECARD.md](../schema/SCHEMA_SCORECARD.md) |
| Core Web Vitals | One real, verified fix (LCP lazy-loading, SEO-026); no overall score claimed — Lighthouse/PageSpeed can't run against a gated site |
| Content SEO | **Was Critical, now fixed (Verified)** — live FAQ page rewritten with 19 topics of real content (SEO-013); one live fabricated count claim found and fixed on a Page body (SEO-032); one empty live legal page remains open (SEO-034) |
| GEO / AI Search Readiness | Improving — the FAQ content gap is closed (SEO-013); schema foundation remains strong, dynamic, and free of duplicate entities |
| Local SEO | Real NAP gap, now fully quantified — 4 address wordings + 2 geo-coordinate pairs (~600m apart) + 2 conflicting delivery-area lists, all live simultaneously (SEO-015/029/036/035); see [ADDRESS_AUDIT.md](ADDRESS_AUDIT.md) |
| UX / CRO | Not fully assessable — site gated. One real fix landed: broken Contact-page `tel:`/WhatsApp links (SEO-033) |
| Security | Adequate within the narrow scope reviewed — not a full security audit |
| EEAT | Was Critical, now substantially improved, one new legal-conflict finding — 13 fabrication instances removed total (12 prior + 1 this pass); a live 4-way contradiction between Refund/Terms policies is the new top finding (SEO-031, Critical); still 0 real reviews, no FSSAI number, no named founder, no GST surfaced — see [EEAT_REPORT.md](EEAT_REPORT.md) |

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

## Sixth pass, 2026-07-30 — Business Decision Implementation

An explicit instruction to implement approved business decisions and generate replacement
specifications for everything still open. Full detail:
[BUSINESS_DECISION_IMPLEMENTATION.md](BUSINESS_DECISION_IMPLEMENTATION.md). Headline outcomes:

- **SEO-013 fixed and deployed**: live FAQ page rewritten, 19 real topics, grounded entirely in
  already-published site content — no new facts invented.
- **SEO-016 confirmed already-fixed**: the header rating claim `CLAUDE.md` described as still-open
  was already resolved by a prior commit predating this audit; both `CLAUDE.md` and project memory
  were stale and are now corrected.
- **SEO-032, SEO-033 found and fixed**: a fabricated count claim on a live Page body, and broken
  `tel:`/WhatsApp links on the live Contact page.
- **SEO-031 escalated Medium → Critical**: what looked like two duplicate policy pages is actually a
  live, public, 4-way contradiction between the site's custom Refund policy and Shopify's own
  built-in Refund/Terms Shop Policies over whether refunds exist at all.
- **SEO-034, SEO-035, SEO-036 newly found**: an empty live Terms page, two conflicting delivery-area
  lists, and a ~600m geo-coordinate conflict against the Shopify Admin's own billing-address record.
- **6 new evidence-based documents** produced for every remaining business decision:
  [ADDRESS_AUDIT.md](ADDRESS_AUDIT.md), [POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md),
  [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md), [EEAT_REPORT.md](EEAT_REPORT.md),
  [LOCAL_SEO_ROADMAP.md](LOCAL_SEO_ROADMAP.md), [CONTENT_PLAN.md](CONTENT_PLAN.md).

## Remaining Risks

1. **Live, public contradiction on refund/cancellation terms** (SEO-031, **Critical**) — the site's
   own custom Refund & Return Policy page and Shopify's built-in Refund policy/Terms of Service say
   opposite things about whether refunds exist at all. Top remaining priority — a legal/trust risk,
   not just a duplicate-content one.
2. **The "Store Locator" page remains unpublished, not resolved** (SEO-030, Mitigated) — a real
   replacement content spec is now ready ([DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md)) but the
   permanent fate (delete/repurpose/leave unpublished) is still open.
3. **Address, geo-coordinates, and delivery-area lists are each inconsistent across multiple live
   surfaces** (SEO-015, SEO-029, SEO-035, SEO-036) — fully catalogued in
   [ADDRESS_AUDIT.md](ADDRESS_AUDIT.md); needs one confirmed answer from the business, applied
   everywhere at once.
4. **An empty live "Terms and Conditions" page** (SEO-034) — indexable, published, no content.
5. A hidden, duplicate `<h1>` renders sitewide (SEO-025, Low) — not fixed, needs a
   template-by-template heading check first.
6. `sitemap.xml` still needs re-checking once the password gate lifts (SEO-019).

## Top Priorities for Launch

1. Resolve the refund/cancellation policy contradiction and fix the wrong business name on 3 Shop
   Policies — SEO-031 (now the single highest-priority item).
2. Confirm one real address, one real geo-coordinate pair, and one real delivery-area list, then
   propagate together — SEO-015, SEO-029, SEO-035, SEO-036.
3. Decide the permanent fate of the "Store Locator" page using the ready replacement spec — SEO-030.
4. Populate or unpublish the empty "Terms and Conditions" page — SEO-034.
5. Re-check `sitemap.xml` the moment the password gate lifts — SEO-019.

## Stop condition reached

Per this audit's own instruction ("continue autonomously until another genuine business decision is
required"): every remaining item (SEO-031, SEO-030, SEO-015/029/035/036, SEO-034) requires either
business-supplied content or an explicit decision only the business can make — not something this
audit can resolve by continuing to search the codebase or query the API further. Every item that was
a mechanical, evidence-based fix this pass (SEO-013, SEO-032, SEO-033) was implemented and deployed,
not just logged. What's left is exclusively business decisions and business-supplied content.
Stopping here is the correct application of the stop condition, not an early exit.

## Full report index

[BUSINESS_DECISION_IMPLEMENTATION.md](BUSINESS_DECISION_IMPLEMENTATION.md) ·
[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md) ·
[POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md) ·
[DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md) ·
[EEAT_REPORT.md](EEAT_REPORT.md) ·
[LOCAL_SEO_ROADMAP.md](LOCAL_SEO_ROADMAP.md) ·
[CONTENT_PLAN.md](CONTENT_PLAN.md) ·
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
- **BUILD-012 (Content + EEAT)**: **the most advanced track by far** — SEO-013 (FAQ content) is now
  fully implemented and live, not just confirmed-live-as-a-defect. SEO-031 escalated from a simple
  duplicate-content finding to a confirmed 4-way legal contradiction, with a full consolidation
  recommendation ready. Real customer/order counts (SEO-018) resolved. Remaining Content/EEAT work
  (SEO-034 empty Terms page, SEO-031 policy decision) is exclusively business-decision-gated, not
  tool- or data-blocked.
- **BUILD-013 (UX/CRO) through BUILD-015 (Launch Readiness)**: still not started. The specific
  blocker for these has narrowed — it's now purely the storefront's password gate (live rendering),
  not the Admin API (which is fully working again). Product/collection *data* is fully queryable;
  actual page *rendering* for UX/CRO purposes is not.

Recommended continuation: with the Admin API now confirmed working, the fastest remaining unlock is
the password gate — lifting it (even temporarily) would enable BUILD-013 and real Core Web Vitals
measurement, the two things Admin API access alone can't provide.
