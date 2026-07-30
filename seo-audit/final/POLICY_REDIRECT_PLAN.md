# Policy Redirect Plan

Generated 2026-07-30, companion to [POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md). This is a
**plan only** — no redirect, unpublish, or delete is executed by this document. Every action below
depends on the `<<BUSINESS APPROVAL REQUIRED>>` decisions in `POLICY_ARCHITECTURE.md` §3 being made
first; the sequence below assumes they happen in this order because later steps read the canonical
text the earlier steps establish.

## Sequencing (do not skip ahead)

1. Business approves the real Refund/Cancellation/Terms/Shipping wording (the `<<BUSINESS APPROVAL
   REQUIRED>>` items in `POLICY_ARCHITECTURE.md`).
2. Canonical pages get the approved wording (Refund & Return Policy custom page; Shipping, Terms of
   Service, Refund Shop Policies).
3. Only then execute the redirects/unpublish/delete actions below — redirecting before the canonical
   target has final content would send users to a page that's about to change again.

## Redirect map

| # | Source | Type | Target | When | Priority |
|---|---|---|---|---|---|
| 1 | `/pages/return-refund-replacement-policy` (unpublished draft) | 301 redirect | `/pages/refund-return-policy` | After its useful clauses (customised-products-non-returnable language) are merged into the canonical page, per `POLICY_ARCHITECTURE.md` §3 | Low — page is already unpublished, so this only matters if the handle was ever linked externally (e.g. an old email, a QR code, a paid ad). Recommend checking Search Console/analytics for any historical traffic to this handle before deciding the redirect is unnecessary. |
| 2 | `/pages/terms-and-conditions` (live, empty) | **No redirect** — recommend keeping this URL live but populating it, since it's already indexed and may have inbound links/QR codes (this store deliberately defers handle changes for exactly this reason, per `CLAUDE.md`'s "Deliberately deferred" section on handle optimization) | N/A — becomes a short page linking to the Shop Policy Terms of Service URL, or is populated with the approved Terms text directly | After Terms of Service wording is approved (step 1) | Medium — currently the worst state (empty + published + indexed) |
| 3 | Shop Policy Refund (`checkout.shopify.com/.../policies/28553805993.html`) | **Not a redirect target** — Shop Policy URLs aren't theme-editable and can't 301 to a custom page. Instead: **rewrite its body** to match the canonical Refund & Return Policy page exactly, once approved | After step 1 | High — this is the actual conflict, not a URL-structure problem |
| 4 | Shop Policy Terms of Service | Same as #3 — rewrite body, not redirect | After step 1 | High |
| 5 | Shop Policy Shipping | Same as #3 — rewrite body once the real delivery/issue-report windows are confirmed | After step 1 | Medium |
| 6 | Shop Policy Contact Information | Same as #3 — rewrite body: fix the address text (per `ADDRESS_AUDIT.md`'s canonical-address decision) and strip the stray `<meta charset="utf-8">` artifacts | After the address decision in `ADDRESS_AUDIT.md` | Medium |
| 7 | `/pages/data-sale-opt-out` ("Your Privacy Choices") | **No redirect** — this is a functioning, real Shopify feature, currently just unpublished | Publish it only if `<<BUSINESS APPROVAL REQUIRED>>` confirms this store needs CCPA/GPC opt-out support; if published, also strip its stray `<meta charset="utf-8">` artifact | Depends on the business-approval decision in `POLICY_ARCHITECTURE.md` §3 | Low |

## Why Shop Policies aren't redirect targets

Shopify's built-in Shop Policies (`REFUND_POLICY`, `SHIPPING_POLICY`, `TERMS_OF_SERVICE`,
`PRIVACY_POLICY`, `CONTACT_INFORMATION`) are served from `checkout.shopify.com`, not the storefront
domain, and Shopify auto-links them from checkout and (depending on theme) the footer. They can't be
unpublished, deleted, or 301-redirected the way a custom Page can — the only correct fix for a Shop
Policy is editing its body text in Shopify Admin → Settings → Policies to match the canonical
version. This is why rows 3-6 above say "rewrite," not "redirect" — attempting to redirect them isn't
a real option, and treating them as one would misstate the actual implementation work.

## What's explicitly NOT in this plan

- No numeric refund/cancellation/shipping window is proposed as correct — every wording change
  above depends on a `<<BUSINESS APPROVAL REQUIRED>>` decision made first, tracked in
  `POLICY_ARCHITECTURE.md`.
- No handle changes to any currently-live, indexed URL (`/pages/terms-and-conditions`,
  `/pages/refund-return-policy`) — consistent with this project's standing deferred-handle-
  optimization policy (`CLAUDE.md`), which treats live URL changes as high-risk relative to their
  SEO upside unless there's a specific reason (there isn't one here).
- No automatic execution — this is the plan for a human (or a future, explicitly-approved
  implementation pass) to act on once the legal wording is signed off.

## Related

[POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md), [POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md),
[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md), [../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md) (SEO-031, SEO-034).
