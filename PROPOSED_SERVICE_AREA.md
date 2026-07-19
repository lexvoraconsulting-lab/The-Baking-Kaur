# PROPOSED DELIVERY SERVICE AREA — FOR APPROVAL
## The Baking Kaur · 2026-07-19 · Nothing configured

Built from: your own website's declared localities · Meerut district government PIN code table ·
your confirmation that Modinagar is served · order history.

---

## KEY FINDING — A RADIUS WOULD NOT WORK, AND NEITHER WOULD THE SIX LOCALITIES

Two facts from the authoritative data change the model:

**1. Pallavpuram — already in your own declared service area — is PIN `250110`, not `2500xx`.**
Your footer lists Pallavpuram among the areas you serve. Its postcode sits outside the Meerut
city core block. So your real coverage was already broader than "Meerut city" before Modinagar
entered the picture.

**2. Modinagar (`201204`) is in Ghaziabad district, not Meerut district** — roughly 25–30 km down
the Delhi Road (NH-58). A radius centred on your shop would either exclude Modinagar or sweep in
large areas of Ghaziabad and Baghpat you may not serve.

**Conclusion: an explicit postcode list is the correct model.** It is precise, auditable, and
cannot over-promise. I am proposing tiers below — you confirm which tiers are genuinely
serviceable.

---

## VERIFIED REFERENCE DATA

### Meerut district PIN codes — 🟢 source: [meerut.nic.in](https://meerut.nic.in/std-pin-codes/)

| Area | PIN |
|---|---|
| Meerut Cantt · Abu Lane · Begum Bagh · Incholi · Meerut University | **250001** |
| Meerut City · Gandhi Ashram · Meerut Tehsil | **250002** |
| Meerut Kuchery | **250003** |
| Medical College | **250004** |
| **Pallavpuram** | **250110** |
| Kithore | 250104 |
| Mawana | 250401 |

Meerut district has **25 unique PIN codes across 270 post offices** — so the list above is the
published summary, not the complete district.

### Modinagar — 🟢 confirmed by you

| Area | PIN | District |
|---|---|---|
| Modinagar (incl. Painga, Patla, Saunda, Shahjahanpur, Sikri Kalan, Sikri Khurd) | **201204** | Ghaziabad |

---

## PROPOSED TIERS — 🟡 YOUR CONFIRMATION REQUIRED

### TIER A — Meerut city core · **recommend INCLUDE**

| PIN | Covers | Basis |
|---|---|---|
| **250001** | Meerut Cantt, Abu Lane, Begum Bagh, Sadar Bazaar, Civil Lines, Thapar Nagar area, Meerut University | Your shop's own PIN; fulfilled orders |
| **250002** | Meerut City, Gandhi Ashram, Meerut Tehsil | Fulfilled orders |
| **250003** | Meerut Kuchery | Contiguous city core |
| **250004** | Medical College | Contiguous city core |

☐ Confirm Tier A

### TIER B — declared localities outside the core · **recommend INCLUDE**

| PIN | Covers | Basis |
|---|---|---|
| **250110** | **Pallavpuram** | Named in your own footer as a served area |

☐ Confirm Tier B

### TIER C — Modinagar · **you confirmed**

| PIN | Covers |
|---|---|
| **201204** | Modinagar and villages under that post office |

☐ Confirm Tier C

### TIER D — the Meerut ↔ Modinagar corridor · 🟡 **I CANNOT DETERMINE THIS**

Modinagar is ~25–30 km from Meerut along NH-58. Settlements lie between (Partapur, Mohiuddinpur,
Kharkhauda and others). **If you deliver to Modinagar, you likely pass through these — but I will
not assume you stop for them.**

☐ **Do you deliver to points between Meerut and Modinagar?**
  If yes, please name them and I will look up the exact PINs.

### TIER E — wider Meerut district · 🟡 **NOT PROPOSED**

Kithore (250104), Mawana (250401), Sardhana and the remaining ~19 district PINs.

☐ **Do you deliver to any of these?** Not included unless you say so.

### EXPLICITLY EXCLUDED

Everything else — all other Ghaziabad PINs, Noida (**201301** — note order #1016 arrived with
city "meerut" but this Noida PIN), Delhi, and the rest of Uttar Pradesh and India.

**No UP-wide or India-wide promise will be created.**

---

## SHASTRI NAGAR AND GANGA NAGAR — 🟡 PIN UNCONFIRMED

Two of your six declared localities do **not** appear in the district government table:

| Locality | PIN | Status |
|---|---|---|
| Shastri Nagar | ? | likely 250004 or 250005 — **not verified** |
| Ganga Nagar | ? | likely 250001 or 250002 — **not verified** |

Both are within Meerut city, so Tier A probably covers them — but I am flagging rather than
assuming. **Please confirm** if either sits outside 250001–250004.

---

## PROPOSED CONFIGURATION SHAPE (once tiers are confirmed)

### Shopify — Local Delivery on the Meerut location
```
Delivery area : explicit PIN list from confirmed tiers
                e.g. 250001, 250002, 250003, 250004, 250110, 201204
Rate          : 🟡 PENDING — you are confirming pricing policy separately
Method        : Local Delivery (NOT a shipping zone)
```
Local Delivery is defined by **postcode**, so it structurally cannot advertise beyond the list.

### Merchant Center — shipping service scoped to the same PINs
```
Service name : Meerut & Modinagar Local Delivery
Country      : India
Region       : postal-code group containing ONLY the confirmed PINs
Rate         : 🟡 PENDING
Delivery time: 🟡 PENDING
```
Google supports postal-code region groups, so the MC promise will mirror the Shopify list exactly.

⚠️ **One consequence to be aware of:** with shipping scoped to these PINs, your products will show
in Google Shopping as **deliverable only within them**. That is accurate and correct — but it does
mean you will not appear as "available" to a shopper in, say, Delhi. That is the honest trade and
the direct consequence of not making a false national promise.

---

## STILL PENDING — NOT BLOCKING THIS APPROVAL

| Item | Status |
|---|---|
| Delivery charge | 🟡 You are confirming current pricing policy |
| Pan-India hampers | 🟡 You are confirming whether nationwide courier genuinely happens |
| GBP name | 🟡 Untouched pending your decision |

---

## WHAT I NEED

1. ☐ Confirm **Tier A** (250001–250004)
2. ☐ Confirm **Tier B** (250110 Pallavpuram)
3. ☐ Confirm **Tier C** (201204 Modinagar)
4. ☐ **Tier D** — do you deliver between Meerut and Modinagar? Name the places.
5. ☐ **Tier E** — Kithore / Mawana / Sardhana / other district areas — yes or no?
6. ☐ Shastri Nagar and Ganga Nagar — inside 250001–250004, or different PINs?

Once these are settled the Shopify Local Delivery list and the matching Merchant Center
postal-code group are both fully specified and can be entered as soon as pricing is confirmed.
