# SHOPIFY LOCAL DELIVERY — EXACT SETUP STEPS
## The Baking Kaur · 2026-07-19 · Configure manually in Shopify Admin

Verified against Shopify documentation: **up to 10 delivery zones per location, each with its own
conditional pricing**, postal codes supported as a comma-and-space separated list up to 3,000
characters. Your two-tier structure is natively supported.

---

## BEFORE YOU START

- Do **not** touch Settings → Shipping and delivery → **Shipping** (the General profile). Leave it
  empty. Any zone there becomes a country-level promise.
- You are configuring **Local delivery**, a separate section further down the same page.
- Local pickup is already configured (4-hour) — leave it alone.

---

## STEP 1 — OPEN LOCAL DELIVERY

1. Shopify Admin → **Settings** (bottom-left)
2. **Shipping and delivery**
3. Scroll to the **Local delivery** section
4. Click **The Baking Kaur** (your only location)

---

## STEP 2 — ENABLE IT

5. Turn on **This location offers local delivery**

---

## STEP 3 — CREATE ZONE 1 (₹100)

6. Delivery area method: choose **Postal codes** (not radius)
7. **Zone name:** `Meerut Core and Outskirts`
8. **Postal codes** — paste exactly, comma + space separated:

```
250001, 250002, 250003, 250004, 250103, 250110
```

9. **Delivery price:** `100`
10. **Minimum order price:** leave **blank** (no minimum) — unless you want one
11. Save the zone

**Covers:** Meerut Cantt · Meerut City · Kuchery · Medical College · Partapur · Pallavpuram

---

## STEP 4 — ADD ZONE 2 (₹200)

12. Click **Add delivery zone** (second zone on the same location)
13. **Zone name:** `Extended - Modinagar Corridor`
14. **Postal codes** — paste exactly:

```
250205, 201204
```

15. **Delivery price:** `200`
16. **Minimum order price:** leave blank
17. Save the zone

**Covers:** Mohiuddinpur · Modinagar (incl. Painga, Patla, Saunda, Shahjahanpur, Sikri Kalan,
Sikri Khurd)

---

## STEP 5 — DELIVERY INSTRUCTIONS

18. In the **Delivery instructions / message to customers** field, paste:

```
Same-day delivery is available on selected products, subject to availability and order timing.
Midnight, express 2-4 hour and custom-cake delivery are separate premium services - please
contact us to arrange.
```

This keeps same-day honest and keeps midnight/express **out** of the standard shipping promise,
as instructed.

---

## STEP 6 — SAVE AND CONFIRM

19. **Save**
20. You should now see **two delivery zones** under The Baking Kaur:

| Zone | Postal codes | Price |
|---|---|---|
| Meerut Core and Outskirts | 250001, 250002, 250003, 250004, 250103, 250110 | ₹100 |
| Extended - Modinagar Corridor | 250205, 201204 | ₹200 |

---

## DO NOT DO

| ❌ | Why |
|---|---|
| Add a zone under **Shipping** (General profile) | Smallest unit is a province → UP-wide promise |
| Use a **radius** instead of postal codes | Would sweep in Ghaziabad/Baghpat areas you do not serve |
| Add Kithore, Mawana or Sardhana | Not approved at this stage |
| Set a delivery **guarantee** in the instructions | Same-day is conditional, not guaranteed |

---

## THE 8 APPROVED POSTCODES — REFERENCE

| PIN | Area | Zone | Rate |
|---|---|---|---|
| 250001 | Meerut Cantt · Sadar Bazaar · Civil Lines · Thapar Nagar (your shop) | 1 | ₹100 |
| 250002 | Meerut City · Gandhi Ashram · Lajpat Bazaar | 1 | ₹100 |
| 250003 | Meerut Kuchery | 1 | ₹100 |
| 250004 | Medical College · Shastri Nagar | 1 | ₹100 |
| 250103 | Partapur | 1 | ₹100 |
| 250110 | Pallavpuram · Modipuram | 1 | ₹100 |
| 250205 | Mohiuddinpur | 2 | ₹200 |
| 201204 | Modinagar | 2 | ₹200 |

---

## WHEN YOU CONFIRM COMPLETION, I WILL RUN (all read-only)

| # | Check | Method |
|---|---|---|
| 1 | Local delivery methods now exist | `deliveryProfiles` query |
| 2 | Eligible PIN `250001` gets a delivery option | live checkout probe |
| 3 | Excluded PIN `201301` (Noida) is rejected | live checkout probe |
| 4 | Google & YouTube sync starts | channel product count |
| 5 | MC API shows first `products.*` call | MC API diagnostics |
| 6 | **MC product count 0 → >0** | MC Products |

---

## IF LOCAL DELIVERY DOES NOT SATISFY MERCHANT CENTER

Per your instruction: **no workaround, no broadening.** Local delivery is a Shopify-side
mechanism and Google may not read it as shipping. If products still do not submit after this is
configured, the next step is **manual Merchant Center shipping** — a postal-code region group
containing exactly these same 8 codes, with the same ₹100/₹200 tiers. Google supports
postcode-level regions; the limitation is Shopify's alone.

I will not widen the area or invent a zone to make the tool cooperate.
