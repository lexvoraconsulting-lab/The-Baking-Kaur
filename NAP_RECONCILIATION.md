# NAP & DELIVERY RECONCILIATION — FOR APPROVAL
## The Baking Kaur · 2026-07-19 · READ-ONLY, nothing changed

Sources interrogated: Shopify Admin API (shop billing + location), theme source, live rendered
website, live LocalBusiness + FAQ schema, Merchant Center linked services, 15 historical orders.

---

## CONFLICT 1 — POSTCODE · 🔴 SHOPIFY CONTRADICTS ITSELF

| Source | Postcode |
|---|---|
| Shopify **billing address** | **250001** |
| Shopify **location address** | **250002** |
| Website footer (rendered live) | **250001** |
| LocalBusiness schema (live) | **250001** |
| Theme source (14 occurrences) | **250001** |
| Theme source (1 occurrence) | 250002 |
| GBP (via Merchant Center) | not displayed |
| Fulfilled orders | both 250001 and 250002 seen |

**Evidence favours 250001 — 4 sources to 1.** The lone outlier is the Shopify *location* record,
which is precisely the field Google's LIA address-match check reads.

**🟡 RECOMMENDED SOURCE OF TRUTH: `250001`** — pending your confirmation of the physical premises.

---

## CONFLICT 2 — STREET NAME SPELLING · 🟠

| Spelling | Where | Count |
|---|---|---|
| **"Fatah** Complex" | website footer, LocalBusiness schema | 6 |
| **"Fateh** Complex" | Shopify billing, Shopify location, GBP | 5 |

Customer-facing surfaces say **Fatah**; official records say **Fateh**.

**🟡 WHICH IS CORRECT?** Google matches GBP against Shopify — currently both say "Fateh", so LIA
may pass, but your website disagrees with both, which weakens entity consistency for local SEO.

---

## CONFLICT 3 — ADDRESS FORMAT · 🟠

| Source | Rendering |
|---|---|
| Shopify (billing + location) | "Thapar Nagar Gali Number 7 Lajpat Bazaar Thapar Nagar" + "Fateh Complex, 390/1, Lane Number 7, opposite Ice Factory," |
| Website / schema | "Fatah Complex, Thapar Nagar Lane 7" |
| GBP | "Fateh Complex 390/1, Opposite Ice Factory, Near Hemkund Car Accessories Lane Number 7, Thapar Nagar" |

Three different formats of the same premises. Note Shopify duplicates "Thapar Nagar" within
`address1`, and only GBP mentions "Near Hemkund Car Accessories".

**🟡 PROPOSED CANONICAL NAP** (for your approval — adjust freely):

```
Name    : The Baking Kaur
Address : Fateh Complex, 390/1, Lane Number 7,
          Opposite Ice Factory, Thapar Nagar,
          Meerut, Uttar Pradesh 250001, India
Phone   : +91 82188 62928
Email   : thebakingkaur@gmail.com
```

To be applied identically to: Shopify billing · Shopify location · GBP · footer · LocalBusiness
schema.

---

## PHONE · ✅ NO CONFLICT

`8218862928` consistent everywhere. Only formatting varies (`+918218862928`, `+91 8218862928`,
`+91-8218862928`, `wa.me/918218862928`).

**🟡 Recommend standardising display as `+91 82188 62928`**, keeping `wa.me/918218862928` for the
WhatsApp link. Cosmetic only.

---

## CONFLICT 4 — AUTHORITATIVE GBP · 🔴 TWO ENTRIES LINKED

Merchant Center → Apps and services lists **two** Google Business Profile links:

| # | Identifier shown |
|---|---|
| 1 | "The Baking Kaur \| Premium Bakery and Cake Shop \|Best bakery in meerut \| Best cakes in meerut" — Fateh Complex 390/1, Opposite Ice Factory, Near Hemkund Car Accessories Lane Number 7, Thapar Nagar, Meerut, Uttar Pradesh, India |
| 2 | `thebakingkaur@gmail.com` |

Entry 1 carries the full address and a keyword-stuffed business name. Entry 2 shows only an email
and may be the same profile surfaced via its owning account, or a genuine duplicate.

**I cannot determine which is authoritative from Merchant Center alone** — it does not expose GBP
listing IDs here.

**🟡 YOU MUST CONFIRM.** Open [business.google.com](https://business.google.com) as
`thebakingkaur@gmail.com` and report how many verified listings exist for this address.

⚠️ **Separate issue — the GBP business name is keyword-stuffed:**
`"The Baking Kaur | Premium Bakery and Cake Shop |Best bakery in meerut | Best cakes in meerut"`
This violates Google Business Profile naming guidelines (name must be the real-world business
name only) and is a common cause of suspension or hard-to-reverse ranking penalties. **Recommend
changing to `The Baking Kaur`** — but that is a decision with local-ranking consequences, so
flagging rather than advising blind action.

---

## CONFLICT 5 — DELIVERY PRICING · 🔴 NO AUTHORITATIVE VALUE EXISTS

You told me not to assume ₹0. Correct — here is everything the data actually shows:

| Period | Rate name on order | Charged |
|---|---|---|
| Aug 2024 | "12:00 PM To 4:00 PM" | ₹0 |
| Oct 2024 | "Delivery Charge" | **₹100** |
| Jul 2025 | "Delivery Charge" | **₹100** |
| Sep 2025 | "Delivery Charge" ×2, "Standard 1 Cake Delivery Rate" ×2 | **₹100** |
| Dec 2025 | "The Baking Kaur" | ₹0 |
| Feb 2026 | "Delivery Charge" | **₹100** |
| Jul 2026 (#1023, most recent) | "The Baking Kaur" | ₹0 |

**₹100 appears on 7 orders; ₹0 on 4.** The two rate names alternate rather than replace each
other — ₹100 "Delivery Charge" was used as recently as **Feb 2026**, *after* the ₹0
"The Baking Kaur" rate first appeared in Dec 2025.

Additional searches found **no** authoritative statement:
- No delivery price stated anywhere in theme copy
- No free-shipping threshold configured (`cart-shipping-bar` requires a `shipping_amount` argument that is not set)
- Shipping policy page contains no pricing
- FAQ schema mentions delivery availability but never a charge

**Conclusion: I cannot determine your intended delivery price. 🟡 YOU MUST SPECIFY IT.**
The plausible reading is that both rates coexisted — possibly ₹0 for some orders/areas and ₹100
for others — but that is inference, not evidence.

---

## CONFLICT 6 — "PAN-INDIA HAMPER DELIVERY" · 🔴 LIVE CLAIM CONTRADICTS THE LOCAL MODEL

Your live FAQ schema states:

> **"Do you deliver gift hampers?"** — *"Yes, we offer budget, premium and luxury gift hampers in
> Meerut **and pan-India hamper delivery on request**."*

This directly conflicts with:
- The Meerut-only model you have instructed me to build
- Order evidence: Bangalore (#1012) and Gujarat (#1010) were **accepted and never fulfilled**
- My verified finding that the catalogue hampers (`hamper13/14/23`) contain **fresh cake**

**🟡 DECISION REQUIRED:**

| Option | Consequence |
|---|---|
| **A. Remove the pan-India claim** | Website matches reality. Recommended if you cannot ship nationally. |
| **B. Keep it, but honour it** | Requires genuinely shelf-stable hampers, courier rates, and a second shipping profile. None exist today. |

**Do not configure Merchant Center around pan-India** either way — MC shipping must describe only
what you can actually fulfil.

---

## SERVICE AREA · 🟢 EVIDENCE FOUND

Your footer already declares the service area:

> *"Same-day & midnight cake delivery across Meerut — **Thapar Nagar, Shastri Nagar, Sadar Bazaar,
> Civil Lines, Pallavpuram, Ganga Nagar** & nearby areas."*

And the buy box offers these slots on every product:
`9 AM–12 PM` · `12 PM–3 PM` · `3 PM–6 PM` · `6 PM–9 PM` · **`Midnight`**
Opening hours in schema: **7 days, 09:00–23:59**.

**🟡 CONFIRM:** are those six localities the complete delivery area, and what does "& nearby
areas" mean concretely — a distance, or specific additional localities? I will not translate a
marketing phrase into a delivery boundary on your behalf.

---

## SUMMARY — DECISIONS I NEED BEFORE ANY CHANGE

| # | Question | Evidence-based lean |
|---|---|---|
| 1 | Postcode — 250001 or 250002? | **250001** (4 sources vs 1) |
| 2 | "Fatah" or "Fateh" Complex? | **Fateh** (Shopify + GBP) — but website says Fatah |
| 3 | Approve the canonical NAP block above? | — |
| 4 | Which GBP is authoritative? | cannot determine — **you must check** |
| 5 | Fix the keyword-stuffed GBP name? | recommend yes; ranking implications |
| 6 | **Delivery price — ₹0, ₹100, or tiered?** | **no authoritative value exists** |
| 7 | Keep or remove the pan-India hamper claim? | remove unless genuinely fulfillable |
| 8 | Is the 6-locality list the full service area? | — |

Once 1–8 are settled I will produce the final Shopify Local Delivery + Merchant Center
configuration built strictly on confirmed values, with **no** Uttar-Pradesh-wide or India-wide
fallback.

---

## NOTE ON THE EARLIER "UP-WIDE ZONE" FALLBACK

I previously floated a Uttar-Pradesh-wide zone as a contingency if products would not sync.
**Per your instruction, that is withdrawn.** If the Google & YouTube app refuses to submit
products without a shipping rate, the correct response is to configure Merchant Center shipping
manually for the real Meerut area — not to widen the promise to make a tool cooperate.
