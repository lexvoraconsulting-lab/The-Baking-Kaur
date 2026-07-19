# SERVICE AREA ZONE MAP — FINAL PROPOSAL
## The Baking Kaur · 2026-07-19 · Awaiting approval, nothing configured

Geography verified against the Meerut district government PIN table and India Post area data.
No radius. No UP-wide or India-wide promise.

---

## THE MAP

Your service area is **not a circle** — it runs north to Pallavpuram/Modipuram and south down the
Delhi Road (NH-58) corridor to Modinagar, roughly 30 km end to end. Three zones:

### ZONE 1 — MEERUT CORE
Your shop sits here. Shortest drive, densest demand.

| PIN | Post office / covers |
|---|---|
| **250001** | Meerut Cantt · Abu Lane · Begum Bagh · Meerut University · **Sadar Bazaar** · **Civil Lines** · **Thapar Nagar** *(your shop)* |
| **250002** | Meerut City · Gandhi Ashram · Meerut Tehsil · Lajpat Bazaar |
| **250003** | Meerut Kuchery |
| **250004** | Medical College · **Shastri Nagar** *(likely)* |

Covers 4 of the 6 localities your footer already advertises.

### ZONE 2 — GREATER MEERUT / OUTSKIRTS
Still Meerut district, outside the core block.

| PIN | Post office / covers | Direction |
|---|---|---|
| **250110** | **Pallavpuram** · Modipuram | North |
| **250103** | **Partapur** · I.E. Partapur | South, on Delhi Road |

Pallavpuram is already named in your footer. Partapur sits on the road you must take to reach
Modinagar.

### ZONE 3 — EXTENDED / MODINAGAR CORRIDOR
Down NH-58, crossing into Ghaziabad district.

| PIN | Post office / covers | District | Approx. distance |
|---|---|---|---|
| **250205** | Mohiuddinpur | Meerut | ~15 km south |
| **201204** | **Modinagar** · Painga · Patla · Saunda · Shahjahanpur · Sikri Kalan · Sikri Khurd | Ghaziabad | ~25–30 km south |

You confirmed Modinagar. Mohiuddinpur lies directly between it and Partapur on the same road.

---

## PROPOSED FULL LIST

```
Zone 1 (core)      : 250001, 250002, 250003, 250004
Zone 2 (outskirts) : 250110, 250103
Zone 3 (extended)  : 250205, 201204
```

**8 postcodes.** Everything else excluded — including all other Ghaziabad PINs, Noida (201301),
Delhi, and the remainder of Uttar Pradesh and India.

---

## NOT INCLUDED — say the word if any should be

| PIN | Area | Why excluded |
|---|---|---|
| 250104 | Kithore | ~30 km **east**, opposite direction to Modinagar |
| 250401 | Mawana | ~25 km **north-east** |
| 250406 | Kharkhari | outlying |
| — | Sardhana | ~20 km north-west |
| — | remaining ~17 Meerut district PINs | Meerut district has 25 PINs / 270 post offices; only the serviceable ones are proposed |

---

## UNVERIFIED — please confirm

| Locality | Assumed PIN | Confidence |
|---|---|---|
| **Shastri Nagar** | 250004 | Medium — in your footer, not in the government table |
| **Ganga Nagar** | 250001 or 250002 | Low — in your footer, not in the government table |

Both are inside Meerut city, so Zone 1 very likely covers them. Flagging rather than assuming.

---

## HOW THIS MAPS TO CONFIGURATION

### Shopify — Local Delivery on the Meerut location
```
Method       : Local Delivery (NOT a shipping zone)
Delivery area: the 8 postcodes above
Rate         : PENDING your pricing decision
```
Local Delivery is postcode-bound, so it structurally cannot advertise beyond the list.

### Merchant Center — shipping service scoped identically
```
Service  : Meerut & Modinagar Local Delivery
Country  : India
Region   : postal-code group = the same 8 postcodes
Rate     : mirrors Shopify
Lead time: PENDING
```

The two lists must match exactly, or Google will advertise availability you cannot honour.

---

## ONE STRUCTURAL QUESTION THIS RAISES

Zone 1 is ~2–5 km from your shop. Zone 3 is ~25–30 km. **Shopify Local Delivery supports either a
single flat rate for the whole area, or separate rates per postcode group.**

If you charge the same to deliver 3 km and 30 km, one flat rate is simplest. If Modinagar costs
more to serve, we should configure Zone 1/2 and Zone 3 as two rates. **This is decision 2 below.**
