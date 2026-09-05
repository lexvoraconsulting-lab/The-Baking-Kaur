<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-dark.svg">
  <img alt="Concept Design" src="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-light.svg" width="100%">
</picture>

# Concept — Storefront Luxury Editorial Redesign (`CON001`)

> **Parent:** [`concept-design-master.md`](./concept-design-master.md) · **Status:** `Planned` · **Date:** 2026-09-06
> **Cross-cut:** none
> **Decision:** [`DEC_Pending`](../decisions/decisions-master.md) · **Fed Plan:** [`HOME`](../plans/01-storefront/PLN003-homepage-editorial-rebuild-s1-s8-plan.md)

---

## 1. Problem

The storefront currently operates on an Ecomus v1.6.1 baseline. While functional, the visual presentation contains remnants of generic multi-purpose e-commerce demo structures. It lacks the cohesive, artisanal, editorial luxury feel expected of a premier 100% eggless cake studio in Meerut. The typography and section cadence need a high-taste elevation governed by `stitch-design-taste` without disturbing the protected product page.

## 2. Concept

Deploy an editorial design language inspired by luxury culinary publications and boutique ateliers:
- **Typography Pairing:** Elegant editorial headings in *Cormorant Garamond* (600/700 weight, italic nuances) anchored by clean, legible interface text in *Manrope* (400/600).
- **Color Discipline:** Preserve the canonical rose (`#7a2147`), soft pill background (`#fff7f8`), and champagne/gold accents defined in `tbk-tokens.liquid`.
- **Generous Pacing:** Elevated vertical rhythm, micro-borders, and tactile subtle shadows rather than harsh drop-shadows or generic card grids.
- **Section Modularity:** Sections S1 through S8 designed as composable OS 2.0 sections with zero jQuery/heavy library overhead (`ponytail` philosophy).

## 3. Ideas Backlog

| S.No. | Idea | Notes |
| ---: | --- | --- |
| 1 | Editorial Hero Canvas (S1) | Full-width or framed split-hero highlighting fresh bespoke cakes with artisanal typography. |
| 2 | Trust & Value Proposition Strip (S2) | "100% Pure Eggless", "Handcrafted in Meerut", "Freshly Baked on Order" visual pills. |
| 3 | Signature Curated Collections (S3) | Curated categories (Bestsellers, Birthday Cakes, Baby Shower, Luxury Hampers) with soft image frames. |
| 4 | Artisanal Craft Story Section (S6) | Editorial brand narrative highlighting ingredient purity and custom cake design philosophy. |

## 4. Scope

- **In Scope:** Homepage sections S1–S8, `tbk-tokens.liquid` refinement, collection banner styling, navigation typography.
- **Out of Scope:** Protected product page (`templates/product.json` and `sections/main-product-premium-v2.liquid`) which is strictly protected against visual/flow changes.

## 5. Open Questions

1. Should typography fonts be self-hosted via Shopify theme assets as `.woff2` to prevent third-party Google Fonts blocking render?
2. Which studio photography assets will replace the current demo product images in the primary hero banner?

## 6. Promotion Path

`CON001` -> Decision -> Architecture / Rules -> Plan -> Worklog.

## Footer

Parent: [`concept-design-master.md`](./concept-design-master.md) ·
Decisions: [`../decisions/decisions-master.md`](../decisions/decisions-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
