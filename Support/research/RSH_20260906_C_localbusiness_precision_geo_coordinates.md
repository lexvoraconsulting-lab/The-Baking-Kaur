<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/research-dark.svg">
  <img alt="Research" src="../../skills/ThemeStyleOps/assets/banners/lexvora/research-light.svg" width="100%">
</picture>

# Research — LocalBusiness Precision Geo Coordinates & NAP Authority (`RSH_20260906_C`)

> **Parent:** [`research-master.md`](./research-master.md) · **Status:** `Exploring` · **Date:** 2026-09-06
> **From concept:** [`CON004`](../concept-design/CON004_Verified_Trust_Framework_Fssai_Entity_Concept.md) (reverse: research spawned by an open question)

## Question

What are the exact latitude/longitude coordinates and NAP (Name, Address, Phone) parameters required to anchor The Baking Kaur in Google's Local Knowledge Graph and dominate Meerut local pack rankings?

## Current Baseline

The snippet `theme_files/snippets/bk-local-business.liquid` currently carries approximate fallback coordinates for Thapar Nagar, Meerut. Historical documentation suffered from fragmented NAP entries across five separate files before the Phase 7.0 reconciliation.

## Findings

1. **Entity Reconciliation:** Canonical NAP is established as:
   - **Name:** The Baking Kaur
   - **Address:** Thapar Nagar, Meerut, Uttar Pradesh 250001, India
   - **Telephone:** `+91 91055 57077`
   - **Market Area:** Meerut City + 15 km delivery radius
2. **Schema Properties:** Injecting `@type: ["Bakery", "LocalBusiness"]` with nested `geo: {"@type": "GeoCoordinates", "latitude": 28.9845, "longitude": 77.7064}` and `servesCuisine: "100% Eggless Bakery"` matches Google Search and GEO entity specifications.
3. **FSSAI Alignment:** Adding the verified 14-digit FSSAI licence as an identifier in the JSON-LD schema (`identifier: {"@type": "PropertyValue", "name": "FSSAI", "value": "<NUMBER>"}`) strengthens commercial credibility.

## Open Questions

1. Should the kitchen address or customer pickup counter address be declared as the primary schema pin?

## Proposed Promotion

Feeds [`CON004`](../concept-design/CON004_Verified_Trust_Framework_Fssai_Entity_Concept.md) and deployment of `snippets/bk-local-business.liquid` to the Shopify live theme.

