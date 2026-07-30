# Business Decision Implementation — 2026-07-30

Implements the approved-decisions instruction: SEO-013 (FAQ), SEO-016 (ratings), SEO-030 (Store
Locator replacement spec), SEO-015/SEO-029 (address audit), SEO-031 (policy consolidation), plus
EEAT, Local SEO, and Content planning deliverables. Continued autonomously per instruction until
every remaining item resolved into either a real fix or a documented business decision.

## Files changed

**Deployed live (theme push, pull → diff → edit → push → re-pull → diff-confirm each time):**

- `templates/page.faq-01.json` — full rewrite, Lorem Ipsum → 19 real FAQ topics (SEO-013).
- `templates/page.faq-02.json` — same content, kept in sync (unused, no live page assigned).
- `templates/page.contact-2.json` — fixed broken `tel:`/WhatsApp `href`s (SEO-033).

**Live Admin API write (Page body, not a theme file):**

- Page `gid://shopify/Page/116138016937` ("100% Eggless Bakery in Meerut") — removed a fabricated
  "20,000+ celebrations" count claim (SEO-032).

**Documentation (this repo, not deployed to the storefront):**

- `CLAUDE.md` — corrected roadmap item #2 (header rating), which was stale.
- `C:\Users\DELL\.claude\projects\...\memory\storefront-seo-audit-2026-07-29.md` — same correction.
- `seo-audit/issues.yml` — SEO-013, SEO-016 statuses corrected to Fixed; SEO-030, SEO-031 updated
  with new evidence; SEO-032 through SEO-036 added (new findings).
- `seo-audit/audit/AUDIT_LEDGER.md`, `CHANGELOG.md`, `SCORECARD.md` — updated to reflect the above.
- `seo-audit/final/EXECUTIVE_REPORT.md` — updated with this pass's summary.
- **New**: `seo-audit/final/ADDRESS_AUDIT.md`, `POLICY_CONSOLIDATION.md`, `DELIVERY_AREA_SPEC.md`,
  `EEAT_REPORT.md`, `LOCAL_SEO_ROADMAP.md`, `CONTENT_PLAN.md`.

## Issues closed

| ID | What | How |
|---|---|---|
| SEO-013 | Live FAQ page Lorem Ipsum | Rewritten with 19 real, evidence-based topics; no new schema code needed (existing Microdata in `accordion.liquid` handles it) |
| SEO-016 | Header "★4.9 Rated" claim | Confirmed already-fixed by a prior commit (`36e1b0c`), predating this audit; `CLAUDE.md`/memory corrected, not a new fix |
| SEO-032 | Fabricated "20,000+ celebrations" on a live Page | Rewritten via Admin API, verified against real customer/order counts |
| SEO-033 | Broken `tel:`/WhatsApp links on live Contact page | Fixed hrefs to the real, already-verified phone number |

## Issues escalated or newly found (documented, not silently resolved)

| ID | What | Status |
|---|---|---|
| SEO-031 | Escalated Medium → Critical: 4-way live contradiction between the custom Refund policy and Shopify's built-in Refund/Terms Shop Policies, plus wrong business name on 3 of 4 built-in policies | Open — business decision required |
| SEO-034 | New: live "Terms and Conditions" page has a completely empty body | Open — business decision required |
| SEO-035 | New: two different live delivery-area lists (footer vs. delivery page) agree on only 2 of 5 named localities | Open — business input required |
| SEO-036 | New: LocalBusiness schema geo-coordinates vs. Shopify Admin's own billing-address coordinates, ~600m apart | Open — business/verification input required |
| SEO-030 | Replacement content spec now ready (`DELIVERY_AREA_SPEC.md`); page stays unpublished, not deleted, per instruction | Open — permanent-fate decision still needed |
| SEO-015 / SEO-029 | Full audit completed — 4 address wordings, 2 coordinate pairs, 1-hour opening-time gap, all catalogued in `ADDRESS_AUDIT.md` | Open — business confirmation required |

## Remaining manual inputs needed from the business

1. **Which refund/cancellation terms are actually true** (12hr/4hr/5-7day vs. "all orders final") —
   the single highest-priority open item; also requires editing Shop Policies in Shopify Admin →
   Settings → Policies (outside this session's write scope) once decided.
2. **The single correct street address and a fresh Google Maps pin-drop** — recommend starting from
   the Shopify Admin billing address as the most likely source of truth, then confirming.
3. **The single correct list of serviceable Meerut localities.**
4. **Real Terms and Conditions content**, or a decision to unpublish that page until it exists.
5. **The Store Locator page's permanent fate** — delete, repurpose using the ready spec, or leave
   unpublished indefinitely.
6. Previously-tracked, still open: FSSAI licence number, GST number (if applicable), whether to name
   a founder publicly, real customer reviews (3 needed to activate the built Social Proof section),
   professional photography (hero + product catalogue).

## Risks

- **Legal/trust risk (SEO-031)**: a live, public policy contradiction about actual refund rights is
  the most serious open item in this entire audit — higher risk than any prior fabricated-rating
  finding, since it concerns enforceable customer rights, not just marketing claims.
- **NAP inconsistency (SEO-015/029/035/036)**: actively hurts Local Pack ranking and could misdirect
  customers/delivery partners until resolved.
- **Empty legal page (SEO-034)**: a published, indexable page with no content is a minor but real
  legal-completeness gap.
- No risk from this session's own changes: every live deploy/write was pull→diff→push/write→re-pull→
  diff-confirmed before being considered done, per this project's established deploy-safety pattern.

## Recommended next BUILD

**BUILD-013 equivalent**: resolve SEO-031 (the policy contradiction) first — it's the highest-
severity open item and the one most likely to cause real customer harm or a support dispute if left
live. Second: a single coordinated address/coordinate/delivery-area confirmation and propagation
pass (SEO-015/029/035/036), since all four are the same underlying "which source is true" question
applied to different fields. Everything else (SEO-030's permanent fate, SEO-034's content, the
already-tracked photography/reviews/FSSAI/GST items) can follow once those two are settled.

## Related

[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md), [EXECUTIVE_REPORT.md](EXECUTIVE_REPORT.md),
[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md), [POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md),
[DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md), [EEAT_REPORT.md](EEAT_REPORT.md),
[LOCAL_SEO_ROADMAP.md](LOCAL_SEO_ROADMAP.md), [CONTENT_PLAN.md](CONTENT_PLAN.md).
