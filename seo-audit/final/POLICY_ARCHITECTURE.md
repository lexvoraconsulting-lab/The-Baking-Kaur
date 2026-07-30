# Policy Architecture — One Authoritative Policy System

Generated 2026-07-30, building directly on `POLICY_CONSOLIDATION.md`, `ADDRESS_AUDIT.md`,
`BUSINESS_DECISION_IMPLEMENTATION.md`, `EXECUTIVE_REPORT.md` and `AUDIT_LEDGER.md` (SEO-031 family).
**This is a plan, not an edit.** No live policy wording is changed by this document. Every place a
real legal decision is required carries `<<BUSINESS APPROVAL REQUIRED>>` instead of invented
language — per instruction, nothing below guesses at legal terms.

Two things changed since `POLICY_CONSOLIDATION.md` was written, confirmed by re-querying the live
Admin API for this pass:

- Shopify's `ShopPolicyType` enum has **no Cookie Policy type and no populated Cancellation Policy**
  for this shop (`SUBSCRIPTION_POLICY` exists in the schema but nothing is set) — so "Cookies" and
  "Cancellation" are legitimately *missing* dedicated policies, not just duplicated ones.
- A second, previously-unexamined page, **"Your Privacy Choices"** (`/pages/data-sale-opt-out`,
  **unpublished**), is Shopify's standard CCPA/Global Privacy Control opt-out widget — real,
  functional, cookie/tracking-adjacent, currently switched off. It also carries the same stray
  `<meta charset="utf-8">` copy-paste artifact already found in the Contact Information Shop Policy —
  the same defect pattern in a second place.

## 1. Full policy inventory (all 8 requested topics)

| Topic | Surface(s) found | Live? | Status |
|---|---|---|---|
| **Privacy** | Shop Policy: Privacy policy (`.../policies/28523692201.html`) | Yes | Single copy, Shopify default template, merge fields intact, functioning correctly. **No conflict, no duplicate.** |
| **Cookies** | Folded into the Privacy Policy's "Cookies" section (no separate Shopify policy type exists). Related: "Your Privacy Choices" CCPA/GPC opt-out page, **unpublished**. | Partial | **Missing as a dedicated concern** — acceptable under Shopify's own architecture (cookies are conventionally part of Privacy Policy, not a separate type), but the opt-out mechanism that would fulfil GPC/CCPA obligations is switched off. |
| **Refund** | Custom Page "Refund & Return Policy" (live) · Custom Page "Return, Refund & Replacement Policy" (unpublished draft) · Shop Policy: Refund policy (live) | Yes (2 of 3 surfaces) | **Conflicting.** Live custom page promises refunds under conditions; live Shop Policy says none exist. Draft page has a third, stricter variant. |
| **Return** | Same three surfaces as Refund — "Return" isn't separated from "Refund" anywhere in this store's content. | Yes | Same conflict; no standalone Return policy exists or is needed once Refund is fixed. |
| **Cancellation** | "Cancellations & Changes" section inside the live custom Refund & Return Policy page (12hr window) · contradicted by Shop Policy Terms of Service ("we do not accept cancellations or changes") | Yes (both) | **Conflicting**, and **missing as a dedicated policy** — no Shopify `SUBSCRIPTION_POLICY` is set for this shop. |
| **Shipping** | Shop Policy: Shipping (live, "2-5 hours" / "1 hour issue window") | Yes | Content present but internally unsourced (numbers appear nowhere else on the site) and inconsistent with the Refund policy's own timing windows. No duplicate — only one Shipping Policy surface exists. |
| **Delivery** | Live marketing pages (`cake-delivery-in-meerut`, `midnight-cake-delivery`, `30-minute-cake-delivery-...`) | Yes | Not a legal policy topic in this store's architecture — these are content/marketing pages, correctly separate from the Shipping Policy. Two of them disagree on the served-area list (SEO-035, tracked separately in `DELIVERY_AREA_SPEC.md`) — noted here for completeness, not re-litigated. |
| **Terms** | Custom Page "Terms and Conditions" (live, published, **completely empty body**) · Shop Policy: Terms of service (live, full text, contradicts Refund page, names the business "The Bakery Kaur") | Yes (both) | **Conflicting + one surface is empty.** An indexable, published, contentless legal page is its own defect independent of the duplication question. |
| **Contact Information** | Custom Page "Contact Us" (live) · Shop Policy: Contact Information (live, malformed HTML) | Yes (both) | Wording differs (see `ADDRESS_AUDIT.md`); not a legal-conflict in the same sense as Refund/Terms, but the same "two systems, two answers" pattern. |

## 2. Duplicates, conflicts, broken links, missing pages — summary

- **Duplicate pages**: Refund/Return has three live-or-unpublished surfaces for one topic (custom
  live page, custom draft page, Shop Policy). Terms has two (custom page, Shop Policy). Contact
  Information has two (custom page, Shop Policy).
- **Conflicting wording**: Refund (3-way, see §1), Cancellation (2-way), Terms (2-way, and one side
  is empty so "conflict" understates it — a customer gets no information at all from the custom
  page).
- **Broken links**: none found *within* the policy bodies themselves (they're plain text/paragraphs,
  no anchor tags to check). The previously-found and already-fixed broken `tel:`/WhatsApp links on
  the Contact page (SEO-033) are UX defects on a related page, not inside a policy document itself,
  so not re-counted here.
- **Missing pages**: a dedicated Cancellation Policy (SEO-031 family — cancellation terms currently
  live only as a subsection of Refund & Return, contradicted by Terms of Service); a functioning
  Cookie consent/opt-out surface (the CCPA opt-out page exists but is unpublished).
- **Unused pages**: the draft "Return, Refund & Replacement Policy" custom page (unpublished, real
  content, some of it not present elsewhere — see §3).
- **Recurring technical defect**: the stray `<meta charset="utf-8">` copy-paste artifact appears in
  **two** Shop Policy bodies now (Contact Information, previously found; "Your Privacy Choices,"
  found this pass) — this looks like a systemic pattern from whatever tool or workflow originally
  populated these, not two independent one-off mistakes.

## 3. Canonical recommendation — one page per policy

| Policy | Recommended canonical location | Action on the others |
|---|---|---|
| **Privacy** | Shop Policy: Privacy policy (keep as-is — already correct, no other surface exists) | No action needed |
| **Cookies** | Fold into the Privacy Policy (Shopify's own convention; no separate page needed) | Decide whether to publish "Your Privacy Choices" — `<<BUSINESS APPROVAL REQUIRED>>`: confirm whether this store serves customers in jurisdictions where CCPA/GPC opt-out must be offered |
| **Refund + Return** | Custom Page "Refund & Return Policy" (`/pages/refund-return-policy`) — recommended over the Shop Policy because it already has specific, reasonable, currently-live terms rather than boilerplate | 1) `<<BUSINESS APPROVAL REQUIRED>>`: confirm the exact terms (12hr cancellation / 4hr issue window / 5–7 day refund) are the real, intended policy — this document does not assume they are just because they're better-written than the alternative. 2) Once approved, the Shop Policy: Refund policy body must be rewritten to match exactly — `<<BUSINESS APPROVAL REQUIRED>>` for the final wording, since it's a legal document. 3) Merge into the canonical page any clause from the unpublished draft that isn't already covered — specifically its explicit "customised/personalised products and flowers/hampers are non-returnable" language, which the live page states less directly — `<<BUSINESS APPROVAL REQUIRED>>` for the merged wording. 4) Unpublish (already done) → delete the draft page once merged. |
| **Cancellation** | Fold into the same canonical Refund & Return Policy page, under its existing "Cancellations & Changes" heading — no separate page needed | The Shop Policy: Terms of service currently says the opposite ("we do not accept cancellations or changes") — `<<BUSINESS APPROVAL REQUIRED>>`: Terms of Service must be reworded to defer to the Refund & Return Policy rather than contradict it |
| **Shipping** | Shop Policy: Shipping (keep this as the canonical legal-terms location — no custom Shipping Policy page exists to compete with it) | `<<BUSINESS APPROVAL REQUIRED>>`: confirm the real delivery-time window and issue-report window — the current "2-5 hours" / "1 hour" figures are unsourced anywhere else and don't match the Refund policy's 4-hour window |
| **Delivery** (marketing/content, not legal) | Existing live pages (`cake-delivery-in-meerut` as the hub, linking to `midnight-cake-delivery` and the 30-minute page) — correctly kept separate from the Shipping Policy | No canonical-page change needed here; the area-list conflict between these pages and the footer (SEO-035) is tracked in `DELIVERY_AREA_SPEC.md`, not duplicated in this document |
| **Terms** | Shop Policy: Terms of service (recommended over the custom page, since it's the one Shopify surfaces automatically at checkout and it's the one with actual content) | 1) `<<BUSINESS APPROVAL REQUIRED>>`: real Terms of Service wording (current text says "The Bakery Kaur," contradicts the Refund policy, and needs the cancellation fix above). 2) The custom "Terms and Conditions" page currently live with an empty body must not stay that way — either populate it with a short pointer + link to the Shop Policy Terms URL (a content decision, not a legal one, so this document *can* specify that pattern), or unpublish it. No legal wording is invented for this page either way. |
| **Contact Information** | Custom "Contact Us" page (`/pages/contact`) — recommended over the Shop Policy since it's the one a human visitor actually lands on, and it's the one already being kept accurate (SEO-033 fixed its broken links this session) | Shop Policy: Contact Information needs its address text reconciled per `ADDRESS_AUDIT.md`'s recommendation (business confirms one address first) and its malformed HTML (stray `<meta charset="utf-8">` tags) removed — mechanical fix, no `<<BUSINESS APPROVAL REQUIRED>>` needed for the HTML cleanup itself, only for which address text to insert |

## 4. What this document does not do

No page is edited, unpublished, deleted, or redirected by this document — it is the plan. No legal
clause is drafted on the business's behalf; every place a real decision or real wording is required
carries `<<BUSINESS APPROVAL REQUIRED>>` rather than a guess. Implementation sequencing and concrete
redirect mappings are in [POLICY_REDIRECT_PLAN.md](POLICY_REDIRECT_PLAN.md).

## Related

[POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md), [ADDRESS_AUDIT.md](ADDRESS_AUDIT.md),
[BUSINESS_DECISION_IMPLEMENTATION.md](BUSINESS_DECISION_IMPLEMENTATION.md),
[POLICY_REDIRECT_PLAN.md](POLICY_REDIRECT_PLAN.md), [../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md) (SEO-031, SEO-034).
