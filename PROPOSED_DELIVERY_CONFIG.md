# PROPOSED SHIPPING & DELIVERY CONFIGURATION — FOR APPROVAL
## The Baking Kaur · Meerut-first local bakery · 2026-07-19

**Nothing has been changed.** This is a draft for your review.

Fields marked **🟢 EVIDENCE** are derived from your live store data.
Fields marked **🟡 YOUR DECISION** need your input — I will not invent prices or a service area.

---

## ⚠️ FIRST — A PREMISE CORRECTION

Your brief refers to "the 14 potentially shippable/non-perishable products."
**There are zero.** I verified all 13 individually earlier and every one is a cake:

| Supposedly shippable | Actually |
|---|---|
| `b75`–`b83`, `b176`, `teddy-rainbow…` (10) | **Teddy-themed CAKES** — my classifier matched "teddy" in a cake title |
| `ch249` | **Candlelight Wedding CAKE** — matched "candle" |
| `hamper13/14/23` | **Cake + flower + balloon combo boxes** — contain fresh cake |
| The 14th (`shopify-flow`) | A Shopify Flow system artefact, not a product |

**All 607 active products are perishable and Meerut-local.** No separate shippable profile is
needed, and building one would be designing for products that do not exist. If you later add
genuinely shelf-stable lines (boxed cookies, packaged chocolates), a second profile becomes
worthwhile — the structure is sketched in §8 for that future case only.

---

## 1. YOUR ACTUAL DELIVERY MODEL — 🟢 EVIDENCE

Extracted from `snippets/tbk-buy-box.liquid` (live theme):

Every product captures, as required line-item properties:
- `properties[Delivery Date]` — a date picker
- `properties[Time Slot]` — a required select with exactly these options:

| Slot |
|---|
| 9 AM – 12 PM |
| 12 PM – 3 PM |
| 3 PM – 6 PM |
| 6 PM – 9 PM |
| **Midnight** |

From `snippets/bk-local-business.liquid`:
- `areaServed`: City = **Meerut**
- `openingHoursSpecification`: **7 days, 09:00–23:59**
- `makesOffer`: **"Midnight Cake Delivery"**, areaServed Meerut
- `geo`: 28.9931, 77.6939

**Key architectural insight:** delivery date and slot are captured as **line-item properties at
add-to-cart**, entirely decoupled from Shopify shipping rates. So the rate structure does **not**
need to encode slots — the slot is already captured separately. This considerably simplifies the
configuration and means a single local-delivery rate can serve all five slots.

---

## 2. RECOMMENDED SHOPIFY ARCHITECTURE

```
Settings → Shipping and delivery
│
├── LOCAL DELIVERY  ◄── THE FIX. Restores checkout.
│   └── Location: The Baking Kaur (Meerut 250002)
│       ├── Delivery area: postcode list (§3)
│       ├── Rate: §4
│       └── Order notes: delivery date + slot already captured on the product page
│
├── LOCAL PICKUP  ◄── already configured, leave alone
│   └── The Baking Kaur · 4-hour pickup · ✅ working
│
└── GENERAL PROFILE  ◄── leave with NO zones
    └── Deliberately empty. See §6 for why.
```

**Why Local Delivery and not a shipping zone:** a shipping zone is defined by country/region and
would advertise delivery to all of India or all of Uttar Pradesh. Local Delivery is defined by
**postcode or radius from your store** and only appears for customers inside it. That matches
reality and cannot over-promise.

---

## 3. MEERUT SERVICE AREA — 🟡 YOUR DECISION

**I will not invent your delivery area.** What I can evidence:

| Source | Postcode |
|---|---|
| Shopify location address | **250002** |
| LocalBusiness schema | **250001** |
| Fulfilled orders | 250001, 250002 |
| Rejected/unfulfilled orders | 110049 (Delhi), 560005 (Bangalore), 370210 (Gujarat), 201301 (Noida) |

Meerut spans roughly **250001–250005** plus outlying codes. **Please confirm which you deliver to:**

```
[ ] 250001   Thapar Nagar / Lajpat Bazaar / city centre
[ ] 250002   Shastri Nagar / your store location
[ ] 250003   ...
[ ] 250004   ...
[ ] 250005   ...
[ ] other: ______________
```

**Alternative — radius instead of postcodes.** Shopify supports "deliver within X km of the
store". Given order #1016 arrived with city "meerut" but postcode **201301** (that is Noida),
a radius is more forgiving of customer typos. Trade-off:

| | Postcode list | Radius |
|---|---|---|
| Precision | exact | approximate |
| Handles typos | no | yes |
| Effort | list them once | set one number |

**My recommendation: radius, 15 km from the store**, unless you have specific areas you refuse.
🟡 Confirm the distance.

---

## 4. DELIVERY RATE STRUCTURE — 🟡 YOUR DECISION

Your own history — 🟢 EVIDENCE from live orders:

| Period | Rate name | Price |
|---|---|---|
| Aug 2024 | "12:00 PM To 4:00 PM" | ₹0 |
| Oct 2024 – Feb 2026 | "Delivery Charge" | **₹100** |
| Sep 2025 | "Standard 1 Cake Delivery Rate" | **₹100** |
| Dec 2025 – Jul 2026 | "The Baking Kaur" | **₹0** |

You most recently charged **₹0**. Proposed structure:

| Option | Rate name | Price | Notes |
|---|---|---|---|
| **A — simplest, matches your latest** | Local Delivery – Meerut | **₹0** | one rate, all slots |
| **B — matches your longest-running** | Local Delivery – Meerut | **₹100** | one rate, all slots |
| **C — free over threshold** | Local Delivery – Meerut | **₹0** over ₹X, else ₹100 | 🟡 set X |
| **D — midnight surcharge** | Standard ₹0 + Midnight ₹Y | | ⚠️ see caveat |

⚠️ **Caveat on D:** the midnight slot is chosen on the **product page** as a line-item property,
*before* checkout. Shopify shipping rates cannot read line-item properties, so a midnight
surcharge **cannot** be applied automatically as a shipping rate. It would need a separate
product/add-on or an app. **Not recommended for this pass.**

**My recommendation: Option A (₹0)** — it matches your current practice, is the simplest thing
that unblocks checkout, and can be changed any time.

---

## 5. GOOGLE & YOUTUBE CHANNEL CONFIGURATION

| Setting | Set to | Why |
|---|---|---|
| Shipping settings | **Manual** | Google's documented path for *"advanced or customized shipping settings"*. Prevents country-level auto-import. |
| Product sync | Leave **On** | already correct |
| Merchant Center account | Leave **5552376763** | already correct |
| Google account | Leave `thebakingkaur@gmail.com` | already correct |

Path: Shopify → Google & YouTube → Settings → Product feed → *Additional settings to sync with
Google Merchant Center*.

---

## 6. MERCHANT CENTER SHIPPING CONFIGURATION

Configure **directly in Merchant Center**, not via Shopify import.

Two documented constraints make auto-import unsuitable:
> *"Only shipping rates in your **General** shipping profile can sync to Google Merchant Center.
> If you use custom shipping profiles, then rates will sync incorrectly … and cause errors."*

Auto-import is organised at **country level** — it cannot express "Meerut only" without
promising all of India.

**Proposed MC service:**

| Field | Value |
|---|---|
| Service name | Meerut Local Delivery |
| Country | India |
| **Region** | **Meerut postal codes only** (MC → Shipping → Regions → create a postal-code group) |
| Rate | match §4 |
| Delivery time | 🟡 your standard lead time, e.g. same-day if ordered before 6 PM |

Products then show as deliverable **only within Meerut** — accurate, and no false national promise.

---

## 7. THE 593 PERISHABLE PRODUCTS

No special handling required. All 607 active products use the same configuration:
Local Delivery (Meerut) + Local Pickup, with MC shipping scoped to Meerut. They are a single
homogeneous group.

---

## 8. FUTURE — GENUINELY SHIPPABLE PRODUCTS (none exist today)

Do **not** build this now. If you later add shelf-stable lines:

1. Create a **custom** profile "Shippable – Non-Perishable"
2. Assign only those products
3. Add a real India zone with courier rates
4. In MC, create a **second** shipping service covering India, and use a
   `shipping_label` / custom label to bind it to those products only

Keeps the national promise attached solely to products that can honour it.

---

## 9. LOCAL INVENTORY / GBP — 🔴 ADDRESS MISMATCH MUST BE FIXED FIRST

Google requires *"the same address in both Google Business Profile and your Shopify."*
**Three surfaces currently disagree** — 🟢 EVIDENCE:

| Source | Street | Postcode |
|---|---|---|
| Shopify location | "Fateh Complex, 390/1, Lane Number 7, opposite Ice Factory, Thapar Nagar Gali Number 7 Lajpat Bazaar" | **250002** |
| LocalBusiness schema (theme) | "**Fatah** Complex, Thapar Nagar Lane 7" | **250001** |
| GBP (shown in MC) | "Fateh Complex 390/1, Opposite Ice Factory, Near Hemkund Car Accessories Lane Number 7, Thapar Nagar" | not displayed |

Note **"Fateh" vs "Fatah"** and **250002 vs 250001**. 🟡 **Which is correct?** Once you confirm,
all three must be aligned before LIA will complete.

Also: **two Google Business Profile entries** are linked to Merchant Center. 🟡 Confirm which is
authoritative; the duplicate should be unlinked *after* the feed is working.

**LIA prerequisite chain** — 🟢 EVIDENCE from Google's documentation:
```
shipping configured → products sync → >10 products APPROVED → LIA can complete
```
You currently have **0 approved**. LIA "Pending" is downstream of the feed, not the cause of it.

---

## 10. EXECUTION ORDER (on approval)

| # | Action | Where | Who |
|---:|---|---|---|
| 1 | Confirm service area (§3) and rate (§4) | — | **You** |
| 2 | Enable Local Delivery on the Meerut location | Settings → Shipping and delivery | **You** |
| 3 | Verify checkout offers delivery again | Test order | You / me |
| 4 | Set Google channel shipping to **Manual** | Google & YouTube → Settings | **You** |
| 5 | Create Meerut-scoped shipping service in MC | Merchant Center → Shipping | **You** |
| 6 | **Verify product sync fires** | see §11 | **Me — read-only** |
| 7 | Confirm GBP address + postcode, unlink duplicate | GBP / MC | **You** |
| 8 | Once >10 approved, complete LIA | Google & YouTube | **You** |

---

## 11. VERIFICATION — I RUN THESE, READ-ONLY

| # | Check | Now | Expected after |
|---:|---|---|---|
| 1 | Local delivery configured | none | ≥1 method on Meerut location |
| 2 | Checkout offers delivery | pickup only | delivery + pickup |
| 3 | Shopify channel product count | **Total 0** | ~607 → "Under Review" |
| 4 | MC API `products.*` calls | **zero** | `products.insert` / `custombatch` present |
| 5 | MC data sources | "Local Feed Partnership" (0) | Shopify source with count |
| 6 | **MC products submitted** | **0** | **> 0** ← the P0 success criterion |

---

## 12. THE ONE THING I COULD NOT VERIFY

Google's documentation does **not** state whether the Google & YouTube app will submit products
when Shopify has **no shipping rates at all** and channel shipping is set to Manual. It is
possible the app requires *some* rate to exist before it will sync, even in manual mode.

**If step 6 shows products still at 0 after steps 2–5**, the fallback is to add a minimal zone in
the **General** profile — and the honest way to do that without a false promise is a zone
containing **Uttar Pradesh only** (not all India), which at least matches your region. I would
verify and report before recommending it.

Flagging now so it is not a surprise.

---

## SUMMARY OF WHAT I NEED FROM YOU

1. 🟡 **Service area** — postcode list, or radius in km (recommend: 15 km radius)
2. 🟡 **Delivery rate** — Option A (₹0), B (₹100), or C (free over threshold)
3. 🟡 **Correct address + postcode** — 250001 or 250002? "Fateh" or "Fatah"?
4. 🟡 **Which GBP entry** is authoritative
5. 🟡 **Delivery lead time** for the MC service (e.g. same-day if ordered before 6 PM)

Once you confirm, steps 2–5 are yours to enter in Shopify and Merchant Center; I will run the
step-11 verification immediately afterwards and report whether MC products crosses 0.
