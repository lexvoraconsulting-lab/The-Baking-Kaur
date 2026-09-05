<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-dark.svg">
  <img alt="Concept Design" src="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-light.svg" width="100%">
</picture>

# Concept — Verified Trust Framework & FSSAI Entity Architecture (`CON004`)

> **Parent:** [`concept-design-master.md`](./concept-design-master.md) · **Status:** `Planned` · **Date:** 2026-09-06
> **Cross-cut:** none
> **Decision:** [`DEC_Pending`](../decisions/decisions-master.md) · **Fed Plan:** [`TRST`](../plans/02-operations/PLN002-verified-trust-framework-and-localbusiness-schema-plan.md)

---

## 1. Problem

The storefront currently has zero verified reviews rendered (unverified rating stars and fabricated testimonials were purged under project rules). Furthermore, the storefront displays "FSSAI approved" without an accompanying licence registration number, and the LocalBusiness schema (`bk-local-business.liquid`) has not yet been injected into `<head>` with verified GPS coordinates for Meerut, limiting trust and local SEO/GEO entity authority.

## 2. Concept

Establish an authentic, verifiable Trust and Entity Architecture:
- **Verified Review Integration:** Transcribe genuine Google Business Profile reviews with transparent `source_url` links (fastest path) or integrate Judge.me for automated verified-buyer reviews.
- **FSSAI Licence Entity:** Prominently display the business's official 14-digit FSSAI licence number in the footer and trust strips, establishing compliance and authenticity.
- **Structured Entity Schema:** Render `snippets/bk-local-business.liquid` inside `<head>` of `layout/theme.liquid`, declaring `Bakery`, `LocalBusiness`, geo-coordinates (latitude/longitude), opening hours, and service radius for Google Search and Generative Engine Optimization (GEO).

## 3. Ideas Backlog

| S.No. | Idea | Notes |
| ---: | --- | --- |
| 1 | GBP Review Transcription Strip | Display 3 authentic Google Business Profile customer reviews with direct link to Google Maps listing. |
| 2 | Official FSSAI Badge & Number | Add official FSSAI logo badge with licence number in site footer and trust modules. |
| 3 | LocalBusiness JSON-LD Injection | Deploy `bk-local-business.liquid` with verified Thapar Nagar, Meerut map pin coordinates. |
| 4 | 100% Eggless Certification Badge | Design and embed durable vector badge via `image-to-vector-graphics` certifying pure eggless kitchen. |

## 4. Scope

- **In Scope:** `snippets/bk-local-business.liquid`, footer FSSAI display, authentic review presentation module.
- **Out of Scope:** Any synthetic, scraped, or unverified star ratings (strictly forbidden by `rules.md`).

## 5. Open Questions

1. What is the official 14-digit FSSAI licence registration number for The Baking Kaur?
2. What are the exact Google Maps coordinates for the storefront / kitchen location in Meerut?

## 6. Promotion Path

`CON004` -> Decision -> Architecture / Rules -> Plan -> Worklog.

## Footer

Parent: [`concept-design-master.md`](./concept-design-master.md) ·
Decisions: [`../decisions/decisions-master.md`](../decisions/decisions-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
