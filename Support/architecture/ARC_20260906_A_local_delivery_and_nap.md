<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/architecture-dark.svg">
  <img alt="Architecture" src="../../skills/ThemeStyleOps/assets/banners/lexvora/architecture-light.svg" width="100%">
</picture>

# ARC_20260906_A — Local Delivery and Canonical NAP Architecture

> **Date:** 2026-09-06 · **Status:** Current Architecture
> **Related Concepts:** [`CON003`](../concept-design/CON003_Local_Delivery_Slot_Cart_Architecture_Concept.md), [`CON004`](../concept-design/CON004_Verified_Trust_Framework_Fssai_Entity_Concept.md)
> **Related Research:** [`RSH_20260906_C`](../research/RSH_20260906_C_localbusiness_precision_geo_coordinates.md)
> **Owning Plans:** [`SLOT`](../plans/01-storefront/PLN001-local-delivery-and-time-slot-order-capture-plan.md), [`TRST`](../plans/02-operations/PLN002-verified-trust-framework-and-localbusiness-schema-plan.md)

---

## 1. System Boundary & Canonical Identity

This architecture establishes the single source of truth for The Baking Kaur's physical presence, local delivery boundaries, and Name-Address-Phone (NAP) consistency across Google Business Profile, Google Merchant Center (Local Inventory Ads), Shopify Location, Schema.org structured data, and customer storefront surfaces.

```text
[Verified Google Business Profile: Shop Code GOOBK1]
       |
       +---> [Shopify Physical Location: Fateh Complex, 390/1, PIN: 250001]
       |
       +---> [LocalBusiness Schema: bk-local-business.liquid (Thapar Nagar, Meerut)]
       |
       +---> [Local Delivery Engine: Radius 15 km from Studio, Min Order ₹350]
       |
       +---> [Storefront Footer & Google Merchant Center Manual Shipping Profile]
```

## 2. Authoritative Canonical NAP Specification

| S.No. | Field | Canonical Value | Source Authority |
| ---: | --- | --- | --- |
| 1 | **Brand Name** | `The Baking Kaur` | Trademark & Live Store |
| 2 | **Shop Code** | `GOOBK1` | Verified Google Business Profile |
| 3 | **Street Address Line 1** | `Fateh Complex, 390/1` | Physically Verified Postal Address |
| 4 | **Street Address Line 2** | `Opposite Ice Factory, Near Hemkund Car Accessories, Lane Number 7` | Visual Navigation Landmarks |
| 5 | **Locality / Area** | `Thapar Nagar` | Meerut Urban Local Zone |
| 6 | **City / State / PIN** | `Meerut, Uttar Pradesh 250001` | Official Postal Code (reconciled from 250002) |
| 7 | **Country** | `India` (`IN`) | ISO 3166-1 |
| 8 | **Telephone** | `+91 82188 62928` | Direct Studio Contact |
| 9 | **WhatsApp Support** | `https://wa.me/918218862928` | Customer Ordering Channel |
| 10 | **Primary Email** | `thebakingkaur@gmail.com` | Official Commercial Inquiries |
| 11 | **Canonical Domain** | `https://thebakingkaur.com` | Primary HTTPS Storefront |

## 3. Delivery Radii, Service Zones & Cart Economics

The studio specializes in fresh, fragile artisanal cakes requiring temperature-sensitive direct hand delivery:

| S.No. | Zone Tier | Radial Distance | Minimum Order Value | Shipping Rate Architecture |
| ---: | --- | --- | --- | --- |
| 1 | **Core Studio Zone** | 0 to 5 km | ₹350 | Free or nominal delivery fee |
| 2 | **Greater Meerut Zone** | 5 to 10 km | ₹500 | Standard distance-tiered fee |
| 3 | **Outer Perimeter Zone** | 10 to 15 km | ₹750 | Premium handling fee |
| 4 | **Beyond Perimeter** | > 15 km | N/A | Excluded from local delivery; pickup only |

### Merchant Center Shipping Decoupling
- Google Merchant Center shipping is permanently configured to **Manual Flat/Distance Rates**, decoupled from Shopify internal dynamic shipping profiles to prevent Local Inventory Ads (LIA) synchronization rejection.

## 4. Consequences & Migration Status

1. **Reconciliation Complete:** The historic confusion regarding `250001` vs `250002` is resolved—`250001` is the verified postal code.
2. **Draft Consolidation:** Four superseded exploratory drafts (`PROPOSED_DELIVERY_CONFIG.md`, `NAP_RECONCILIATION.md`, `PROPOSED_SERVICE_AREA.md`, `SERVICE_AREA_ZONE_MAP.md`) are formally archived into `tbk-spfy-archive/superseded-drafts/delivery-geo/`.
3. **Execution Linkage:** Provides the binding delivery constraints for Plan [`SLOT`](../plans/01-storefront/PLN001-local-delivery-and-time-slot-order-capture-plan.md) and Plan [`TRST`](../plans/02-operations/PLN002-verified-trust-framework-and-localbusiness-schema-plan.md).\n