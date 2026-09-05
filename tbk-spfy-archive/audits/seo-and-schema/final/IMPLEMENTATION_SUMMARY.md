# Implementation Summary — Sprint 1 Blockers (B1-B6)

Generated 2026-07-30. Reports what was actually implemented against the six approved business
decisions (`BUSINESS_DECISION_GUIDE.md`). **This is a status report, not new planning** — every
recommendation it references was already approved; nothing new is proposed here.

## Headline: a tool outage limited this pass to one blocker

Partway through this implementation phase, **the Shopify MCP connector disconnected**, and this
environment has no fallback — `seo-ops/`'s existing direct-API path needs a `SHOPIFY_TOKEN`
environment variable, confirmed unset (`env | grep -i shopify` returned nothing Shopify-related; no
`.env` file exists). This blocks every operation that isn't a theme-file change: Shop Policy edits,
Page body edits, collection publish/unpublish, and menu changes are all unreachable right now.

Cross-referencing this against B1-B6:

| Blocker | Status this pass | Why |
|---|---|---|
| **B1** (refund/terms policy rewrite) | **Not implemented** | Shop Policies are edited only via Shopify Admin → Settings → Policies — never reachable by theme deploy, and now unreachable by the MCP path either. |
| **B2** (empty Terms page) | **Not implemented** | Admin-API-only (Page body), and gated on B1 regardless. |
| **B3** (address/geo unification) | **Partially implemented** | Its theme-file portion (5 files) doesn't need Admin API — completed and deployed. Its Admin-only portion (Refund policy page body, Shop Policy Contact Information) is blocked, same as B1. |
| **B4** (delivery-area list) | **Not implemented** | The approved decision was to *go confirm* a real list against logistics data — no concrete list was supplied alongside the approval. Executing this would mean guessing, which this project has refused to do throughout. |
| **B5** (duplicate collection cluster) | **Not implemented** | Needs actual merchandising picks (which collections, if any, to keep) — not supplied — and Admin API for execution either way. |
| **B6** (Store Locator fate) | **Not implemented** | Explicitly sequenced to start only after B4 — B4 didn't land, so B6 doesn't either. |

Per instruction ("stop immediately if a new business decision is required"): B4 and B5 aren't blocked
by a *new* decision, but they were approved as *processes* ("go confirm the real list," "review which
collections to keep"), not as ready-to-execute concrete values — proceeding without the actual data
would be inventing it. Stopping here for those two rather than guessing.

## Files changed

- `snippets/bk-local-business.liquid` — corrected `streetAddress` (fixed "Fatah" → "Fateh" typo,
  full address) and `geo` coordinates; updated the in-code sourcing comment.
- `snippets/tbk-schema-website.liquid` — added a `streetAddress`/`geo` block it previously lacked
  entirely, closing a known Organization/Bakery schema-coverage gap.
- `sections/site-footer.liquid` — corrected the `address` setting's default value.
- `sections/footer.liquid` — corrected the hardcoded address text next to a real Google Maps link.
- `sections/tbk-footer.liquid` — corrected the hardcoded address text (2 occurrences).
- `seo-audit/issues.yml` — SEO-015, SEO-029, SEO-036 statuses updated to Partial with full detail.
- `seo-audit/audit/AUDIT_LEDGER.md` — table rows updated; B1-B6 status table added.
- `seo-audit/audit/CHANGELOG.md` — full before/why/implementation/after entry for B3.

No product page, no protected module, and no file outside the address/geo scope was touched.

## Commits

1. `137ea7d` — `fix(local-seo): unify address and geo-coordinates across theme (B3 partial, SEO-015/029/036)`

Only one commit was possible this pass, since B3 was the only blocker with executable work. B1, B2,
B4, B5, B6 have no corresponding commit — nothing was changed for them.

## Verification performed

- **Before editing**: `shopify theme pull` on all 5 target files, `diff --strip-trailing-cr` against
  git HEAD — confirmed zero pre-existing drift before any edit.
- **New evidence check**: resolved a real, previously-unexamined Google Maps share link found in
  `sections/footer.liquid` (`https://maps.app.goo.gl/LmD25vZFZYQL3TTd6`) via `WebFetch` — it redirects
  to a genuine Google Business Profile listing for this exact business, whose address text
  independently corroborates the Shopify Admin billing address used for this change. Attempted to
  extract its exact coordinates (direct fetch, and a CID-based URL converted from the place ID's hex
  value via `printf "%d\n" 0x...`) — both attempts failed because Google Maps place pages are
  JS-rendered and not accessible to a static fetch; this is a genuine tooling limit, documented rather
  than papered over.
- **After editing**: `shopify theme push --allow-live`, then re-pulled and `diff --strip-trailing-cr`
  — confirmed byte-for-byte live on all 5 files.
- **Theme Check**: run across the full theme after the push — 1,369 offenses across 94 files,
  identical to the pre-existing baseline established earlier this project; zero offenses in any of
  the 5 touched files (confirmed via grep) — no regression introduced.
- **Environment check**: confirmed the Shopify MCP's absence and the lack of a `SHOPIFY_TOKEN`
  fallback before concluding B1/B2/B4(execution)/B5/B6 were genuinely blocked, not just skipped.

## SEO impact

**B3 (implemented)**: Medium-High. Address/geo-coordinate consistency across schema and footer
surfaces is a real Local Pack ranking input; this pass eliminates the ~600 m coordinate discrepancy
between the two live schema sources and removes a spelling-typo'd address variant from 5 surfaces.
Two surfaces (Refund policy page, Shop Policy Contact Information) remain inconsistent until the
Admin-API-only portion completes — full NAP consistency is not yet achieved.

**B1/B2/B4/B5/B6 (not implemented)**: no change from prior state — the live legal-policy
contradiction (B1), empty Terms page (B2), delivery-area-list conflict (B4), duplicate-collection
cluster (B5), and Store Locator's fate (B6) all remain exactly as documented in
`SPRINT1_BLOCKERS.md`/`BUSINESS_DECISION_GUIDE.md`.

## UX impact

**B3**: customers checking the address across the footer or viewing page source now see one
consistent, correctly-spelled address instead of a typo'd variant in most places — a small but real
trust/credibility improvement. No visible layout change (address text length changed slightly but the
surrounding UI is unaffected).

**Everything else**: unchanged — the live policy contradiction, empty Terms page, and inconsistent
delivery-area claims remain live exactly as before.

## Risk

- **B3's implementation risk**: low. Text/schema-value changes only, verified byte-for-byte live,
  zero Theme Check regressions.
- **B3's residual risk**: the address used is the Shopify Admin billing address, corroborated by a
  real (if coordinate-unverifiable) Google Business Profile listing — a strong but not
  human-visually-confirmed source. A follow-up visual check against the real signage/lease is still
  recommended, as `ADDRESS_AUDIT.md` originally noted.
- **Risk of NOT implementing B1**: unchanged and highest-priority — the live refund/terms policy
  contradiction continues to carry real legal/trust exposure until Admin API access is restored and
  the rewrite executes.
- **Risk of NOT implementing B4/B5**: unchanged — continued local-SEO inconsistency (B4) and
  duplicate-content dilution (B5), neither worsened nor improved by this pass.

## Manual QA checklist

For B3 (before considering it fully closed):
- [ ] Visit `thebakingkaur.com` (or the preview-theme URL) and inspect the footer on at least one
      page — confirm the address reads correctly and matches across all footer variants in use.
- [ ] View page source on the homepage and a product page — confirm the `Bakery` (`bk-local-business`)
      and `Organization` (`tbk-schema-website`) JSON-LD blocks both show the same `streetAddress` and
      `geo` coordinates.
- [ ] Run the updated address/coordinates through Google's Rich Results Test to confirm both schema
      blocks parse without new errors.
- [ ] Have someone with local knowledge of the shop visually confirm the Google Maps pin at
      (28.9897017, 77.7044604) actually sits on/near the real storefront — this pass could not do
      that confirmation itself.
- [ ] Once Shopify Admin API access is restored (MCP reconnect, or a `SHOPIFY_TOKEN` provided), apply
      the same address correction to the Refund & Return Policy page body and the Shop Policy Contact
      Information body to close out SEO-029 fully.

Before resuming B1/B2/B4/B5/B6:
- [ ] Confirm Shopify Admin API access is restored (reconnect the MCP connector, or set
      `SHOPIFY_STORE`/`SHOPIFY_TOKEN` for the `seo-ops/` scripts' direct-API path).
- [ ] Supply the actual confirmed delivery-area locality list for B4 (not a re-pick between the two
      existing conflicting lists — a genuinely confirmed one, per the approved recommendation).
- [ ] Supply the actual merchandising decision for B5 — which (if any) of the 7 near-duplicate
      collections should stay live.

## Related

[SPRINT1_BLOCKERS.md](SPRINT1_BLOCKERS.md), [BUSINESS_DECISION_GUIDE.md](BUSINESS_DECISION_GUIDE.md),
[../audit/CHANGELOG.md](../audit/CHANGELOG.md), [../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md),
[../issues.yml](../issues.yml).
