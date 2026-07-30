# Policy Consolidation Audit (SEO-031)

Generated 2026-07-30. Covers every Privacy/Refund/Shipping/Terms/Returns/Cancellation surface found
live. **No page or policy is deleted, merged, or edited by this document** — per instruction, this is
analysis and a canonical/duplicate/redirect recommendation only, for a human decision.

## The headline finding: two independent policy systems, actively contradicting each other

Shopify stores legal policy content in two unrelated places, and this store has real, live, differing
content in both:

1. **Custom Pages** (Shopify Admin → Pages), rendered via the theme.
2. **Shop Policies** (Shopify Admin → Settings → Policies), Shopify's built-in legal-page system,
   served at `checkout.shopify.com/<shop_id>/policies/<policy_id>.html` and usually linked from
   checkout/footer automatically.

Both are live and public right now. **They say opposite things about whether refunds exist.**

### Refund / Return policy — direct contradiction

| Surface | Type | Live? | Says |
|---|---|---|---|
| "Refund & Return Policy" (`/pages/refund-return-policy`) | Custom Page | **Yes, published** | Cancel/modify up to **12 hours before** delivery for full refund/credit; damaged/wrong/quality issues → contact **within 4 hours**, replacement or partial/full refund at discretion; approved refunds in **5–7 business days** |
| "Return, Refund & Replacement Policy" (`/pages/return-refund-replacement-policy`) | Custom Page | **No — unpublished** | Refund/replacement for wrong/damaged/missing item, quality issue reported **within 2 hours**; cancellation before production starts |
| Shop Policy: **Refund policy** | Built-in legal policy | **Yes, live**, `checkout.shopify.com/66799304873/policies/28553805993.html` | *"1. No Refunds or Replacements: All orders are final. We do not offer refunds or replacements once an order is placed... 2. Quality Issues: Report... within 2 hours... but no refunds or replacements will be given."* Business name given as **"The Bakery Kaur"** (wrong). |
| Shop Policy: **Terms of service** | Built-in legal policy | **Yes, live** | *"Order Confirmation: Once you place an order, it is considered final. We do not accept cancellations or changes... We do not offer refunds or replacements."* Also "The Bakery Kaur." |

Three live, public documents make three different promises about the same question ("can I get a
refund?"): yes-with-conditions (12hr/4hr/5-7 days), yes-with-conditions but stricter (2hr), and
flatly no. A customer who reads the Refund & Return Policy page before ordering and then reads the
Shop Policy linked at checkout would reasonably conclude the store is misrepresenting one of them.
This is a legal/trust exposure, not just a duplicate-content SEO issue — **resolving which policy is
actually true is a business decision, not something this audit will pick for you.**

### Shipping policy

| Surface | Live? | Says |
|---|---|---|
| Shop Policy: **Shipping** | Yes, live | "We deliver in Meerut, typically within 2-5 hours... Delivery Issues: Contact us... within **1 hour** of receiving your order" — again "The Bakery Kaur" |
| Live delivery pages (`cake-delivery-in-meerut`, `midnight-cake-delivery`, `30-minute-...`) | Yes, live | Same-day/midnight/express framing, no numeric "2-5 hours" claim, no "1 hour" issue-report window |

A fourth, separate numeric window (1 hour) that appears nowhere else and isn't consistent with the
Refund policy's 4-hour or 2-hour windows.

### Terms and Conditions

| Surface | Live? | Says |
|---|---|---|
| Custom Page "Terms and Conditions" (`/pages/terms-and-conditions`) | **Yes, published** | **Body is completely empty** — a live, indexable page with a `<title>` and no content at all |
| Shop Policy: **Terms of service** | Yes, live | Full text present (see above), contradicts the Refund page |

The published custom Terms page having zero body content is itself a defect independent of the
duplication question — a customer or Google crawler visiting `/pages/terms-and-conditions` finds
nothing.

### Privacy policy

Only one live copy found: the Shop Policy (built-in), which is Shopify's own default template with
merge fields (`{{ shop_name }}`, `{{ email }}`, `{{ address }}`) intact and rendering correctly — no
custom Privacy Policy Page exists to duplicate it. **No issue here.**

### Contact information

Two live copies with different wording (see [ADDRESS_AUDIT.md](ADDRESS_AUDIT.md) for the full
address-text comparison): the Contact page and the Shop Policy "Contact Information" page (which also
has embedded `<meta charset="utf-8">` HTML artifacts from a copy-paste).

## Canonical / duplicate / redirect recommendation

This audit does **not** choose which policy text is correct — that's a business decision, since the
Refund/Terms/Shipping conflict is about actual customer rights, not just wording. It does recommend
the *mechanism* for fixing it once the business decides:

1. **Pick one system as canonical.** Recommend the custom Pages, since they're the ones with
   real, specific, currently-reasonable terms (12hr cancellation, 4hr issue window, 5-7 day refund) —
   the Shop Policies read like unedited defaults/generated boilerplate (wrong business name in 3 of
   4, a flat "no refunds ever" stance that seems inconsistent with the rest of the site's tone).
2. **Once the real terms are confirmed by the business**, update the Shop Policies (Settings →
   Policies in Shopify Admin, not a theme file — out of this session's write scope) to match the
   custom Pages exactly, including fixing "The Bakery Kaur" → "The Baking Kaur" in all three.
3. **Unpublish, don't delete**, the draft "Return, Refund & Replacement Policy" custom page (it's
   already unpublished) — keep it only if there's a plan to merge its useful clauses (e.g. its
   explicit "customised/personalised products are non-returnable" clause, which the published page
   states less directly) into the canonical page, then delete once merged.
4. **Write real content for the empty "Terms and Conditions" custom page**, or unpublish it until
   real terms exist — an empty, indexable, published legal page is worse than no page.
5. **Redirect candidates**: once a single canonical Refund/Return URL is confirmed, 301 the
   unpublished draft's handle (`/pages/return-refund-replacement-policy`) to the canonical one, in
   case it was ever linked externally (it currently isn't published, so this is low urgency, but
   costs nothing once the canonical is settled).

## What this document does NOT recommend

No automatic deletion, no automatic merge, no automatic edit to either Shop Policy (those require
Shopify Admin access outside this session's Admin-API scope for policy text, and more importantly
require the business to confirm the actual refund/cancellation terms first). The one clearly
mechanical, no-judgment-required fix — the malformed HTML in the Contact Information Shop Policy — is
noted but not applied here since Shop Policies aren't reachable via the theme deploy path used this
session.

## Related

[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md), [EEAT_REPORT.md](EEAT_REPORT.md),
[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md) (SEO-031).
