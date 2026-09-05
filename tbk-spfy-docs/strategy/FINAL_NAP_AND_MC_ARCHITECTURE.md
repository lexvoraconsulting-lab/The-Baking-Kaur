# FINAL NAP + MERCHANT CENTER ARCHITECTURE — FOR APPROVAL
## The Baking Kaur · 2026-07-19 · READ-ONLY, nothing changed

---

# PART 1 — AUTHORITATIVE GBP: RESOLVED

**There is exactly ONE Google Business Profile. The earlier "two entries" concern was a false
alarm** — Merchant Center surfaced the same profile twice (once by listing, once by owning
account email). **No duplicate exists. Nothing to merge or delete.**

Verified in Google Business Profile Manager:

| Field | Value |
|---|---|
| Businesses on account | **1 business · 100% verified** |
| Shop code | **GOOBK1** |
| Status | **Verified** ✅ |
| Address | Fateh Complex 390/1, Opposite Ice Factory, Near Hemkund Car Accessories Lane Number 7, Thapar Nagar, Meerut, Uttar Pradesh **250001** |
| Reviews | Genuine and recent — multiple 5★, most recent ~3 weeks ago |
| Operating profile | Active. Sample review: *"I had a last-minute request, and they went above and beyond to make it happen."* |

**This is unambiguously the authoritative profile:** single listing, Google-verified, real
customer reviews, correct address, and it already carries your confirmed `250001` and `Fateh`.

> Because Google has **physically verified** this address, GBP — not Shopify — is the correct
> source of truth for the address.

---

# PART 2 — CANONICAL NAP (FOR YOUR APPROVAL)

```
Name    : The Baking Kaur

Address : Fateh Complex, 390/1
          Opposite Ice Factory, Near Hemkund Car Accessories
          Lane Number 7, Thapar Nagar
          Meerut, Uttar Pradesh 250001
          India

Phone   : +91 82188 62928
Email   : thebakingkaur@gmail.com
Website : https://thebakingkaur.com
```

Derived from the Google-verified GBP record, with your confirmations (`250001`, `Fateh`) applied.

## Per-surface change list

| # | Surface | Current | Change to | Risk |
|---|---|---|---|---|
| 1 | **Shopify location** address | zip **250002** | **250001** | 🟢 Low — **this is the LIA blocker** |
| 2 | Shopify location `address1` | "Thapar Nagar Gali Number 7 Lajpat Bazaar Thapar Nagar" (duplicates "Thapar Nagar") | "Fateh Complex, 390/1" | 🟢 Low |
| 3 | Shopify location `address2` | "Fateh Complex, 390/1, Lane Number 7, opposite Ice Factory," | "Opposite Ice Factory, Lane Number 7, Thapar Nagar" | 🟢 Low |
| 4 | Shopify **billing** address | 250001 ✅, but same field-order issue | align format | 🟢 Low |
| 5 | Website footer (`site-footer.liquid`) | "**Fatah** Complex, Thapar Nagar Lane 7, Meerut, Uttar Pradesh 250001" | canonical address | 🟢 Low |
| 6 | LocalBusiness schema (`bk-local-business.liquid`) | `streetAddress: "Fatah Complex, Thapar Nagar Lane 7"`, `postalCode: "250001"` | canonical `streetAddress`, postcode already correct | 🟢 Low |
| 7 | Phone formatting | `+918218862928` / `+91 8218862928` / `+91-8218862928` | `+91 82188 62928` (keep `wa.me/918218862928`) | 🟢 Cosmetic |
| 8 | **GBP address** | already canonical ✅ | **no change** | — |

**Only item 1 is functionally required** — it unblocks the LIA address match. Items 2–7 are
entity-consistency improvements for local SEO.

## GBP business name — recommended change

| | |
|---|---|
| Current | `The Baking Kaur \| Premium Bakery and Cake Shop \|Best bakery in meerut \| Best cakes in meerut` |
| Genuine real-world name | **The Baking Kaur** |

Per your instruction ("fix only if it differs from our genuine real-world business name") — **it
does differ.** Everything after "The Baking Kaur" is category descriptor plus keywords, not part
of your trading name. Google's guideline is that the name field must contain the real-world
business name only.

**Recommendation: change to `The Baking Kaur`.**

⚠️ **Honest risk disclosure — your call, not mine:**
- Keyword-stuffed names sometimes *do* rank better short-term. Removing keywords may cause a
  temporary local-pack dip.
- Editing the name can trigger **re-verification**, during which the listing may be less visible.
- However, the current name is a **suspension risk**, and suspension is far harder to reverse
  than a ranking dip.

I recommend the change, but I will not touch it without your explicit go-ahead.

---

# PART 3 — MERCHANT CENTER FEED ARCHITECTURE

Built only on confirmed values. **No India-wide or UP-wide promise.**

## 3.1 Where the feed is actually blocked — recap

```
Shopify → Google & YouTube channel ....... Active ✅
       → OAuth thebakingkaur@gmail.com ... correct ✅
       → MC account 5552376763 ........... correct ✅
       → Product sync toggle ............. ON ✅
       → PRODUCTS SUBMITTED .............. 0 ❌  ← blocked
       → Shipping rates in Shopify ....... NONE ❌ ← root cause
MC API (30d): accounts.get 41 · liasettings.get 30 · liasettings.getaccessiblegmbaccounts 31
              products.* .................. ZERO
```

## 3.2 Recommended architecture

| Layer | Configuration | Rationale |
|---|---|---|
| **Shopify checkout** | Local Delivery on the Meerut location, scoped to your genuine service area | Structurally cannot advertise outside Meerut |
| **Shopify pickup** | Leave as-is (4-hour) ✅ | Already working |
| **Shopify General profile** | Leave **empty** | Any zone here becomes a country-level promise |
| **Google channel shipping** | Set to **Manual** | Google's documented route for custom shipping |
| **Merchant Center shipping** | Service scoped to **Meerut postal codes only** | Accurate; no false promise |
| **Local Inventory (LIA)** | Complete **after** >10 products are approved | Documented prerequisite chain |

## 3.3 Service area — awaiting your definition

Your footer already declares:
> *Thapar Nagar, Shastri Nagar, Sadar Bazaar, Civil Lines, Pallavpuram, Ganga Nagar & nearby areas*

**🟡 I need this as concrete postcodes or a radius.** I will not convert *"& nearby areas"* into a
delivery boundary myself — that is a serviceability decision, and inventing it is exactly what you
instructed me not to do.

## 3.4 Delivery pricing — deferred at your instruction

Not assumed. You will confirm separately. Evidence on file: **₹100 on 7 orders, ₹0 on 4**, with
₹100 used as recently as Feb 2026.

## 3.5 Perishable vs shippable

| Group | Count | Treatment |
|---|---:|---|
| Perishable cakes and cake-containing hampers | **607 active** | Meerut local delivery only |
| Genuinely shippable non-perishables | **0 verified** | none exist today |

⚠️ **Open question — the pan-India hamper claim.** Your live FAQ states *"pan-India hamper delivery
on request."* Per your instruction I have neither removed nor retained it pending verification.
**I cannot verify this from available data** — no fulfilled order outside Meerut/Delhi exists, and
the catalogue hampers contain fresh cake. **Only you can confirm** whether a genuinely shippable
hamper product exists or is planned. Until then, MC will be configured Meerut-only.

## 3.6 Execution order

| # | Action | Who | Blocking? |
|---:|---|---|---|
| 1 | Approve the canonical NAP above | **You** | — |
| 2 | Fix Shopify **location** postcode → 250001 | You or me | **Yes — LIA blocker** |
| 3 | Align website footer + schema address | Me (theme edit) | No |
| 4 | Confirm service area postcodes/radius | **You** | **Yes** |
| 5 | Confirm delivery charge | **You** | **Yes** |
| 6 | Configure Local Delivery | **You** | **Yes — restores checkout** |
| 7 | Set Google channel shipping → Manual | **You** | Yes |
| 8 | Create Meerut-scoped MC shipping service | **You** | Yes |
| 9 | Verify products submitted > 0 | **Me, read-only** | — |
| 10 | Decide on GBP name change | **You** | No |
| 11 | Complete LIA once >10 approved | **You** | No |

## 3.7 Verification I will run (read-only)

| # | Check | Now | Target |
|---:|---|---|---|
| 1 | `deliveryProfiles.zoneCountryCount` / local delivery | 0 / none | configured |
| 2 | Checkout offers delivery | pickup only | delivery + pickup |
| 3 | Shopify channel product total | **0** | ~607 |
| 4 | MC API `products.*` calls | **zero** | present |
| 5 | MC data sources | "Local Feed Partnership" (0) | Shopify source with count |
| 6 | **MC products submitted** | **0** | **> 0** ← P0 success |

---

# WHAT I NEED FROM YOU NOW

1. ✅ **Approve the canonical NAP** in Part 2
2. 🟡 **GBP name** — change to "The Baking Kaur"? (recommended, with the risks stated)
3. 🟡 **Service area** — postcodes or radius
4. 🟡 **Delivery charge** — you said you'd confirm separately
5. 🟡 **Pan-India hampers** — does a genuinely shippable hamper exist?

On approval of (1) I can immediately fix the Shopify location postcode — a one-field change that
clears the LIA address-match blocker — and align the website/schema address. Items 3–5 gate the
Merchant Center work.
