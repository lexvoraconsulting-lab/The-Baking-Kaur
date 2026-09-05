<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-dark.svg">
  <img alt="Concept Design" src="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-light.svg" width="100%">
</picture>

# Concept — AI Cake Genome & Vision Intelligence Pipeline (`CON002`)

> **Parent:** [`concept-design-master.md`](./concept-design-master.md) · **Status:** `Planned` · **Date:** 2026-09-06
> **Cross-cut:** none
> **Decision:** [`DEC_Pending`](../decisions/decisions-master.md) · **Fed Plan:** [`CGV`](../plans/03-ai-intelligence/PLN004-ai-cake-genome-and-vision-intelligence-pipeline-plan.md)

---

## 1. Problem

The repository contains extensive machine learning and vision intelligence assets in `tbk-spfy-ai/` and `tbk-spfy-automations/`, but these engines are currently operated in silos. Cataloguing the store's ~1,235 products has historically suffered from manual tagging drift (e.g., the previously resolved defect where 70 theme cakes were mislabelled with "anniversary" occasions in their descriptions).

## 2. Concept

Formally link the Python Cake Genome intelligence engine to the Shopify Admin GraphQL API:
- **Vision Classification:** Automatically extract visual features from cake product images (tier height, icing finish, dominant color scheme, celebratory theme, design motifs).
- **Taxonomy Normalization:** Map visual attributes into standardized Shopify Metafields (`custom.cake_theme`, `custom.tier_count`, `custom.eggless_certification`, `custom.flavor_profile`).
- **Mutation Safety:** Batch generated updates via the `tbk-spfy-seo/ops/` architecture strictly keeping mutations ≤ 8–10 per request to respect Shopify rate limits.
- **Workflow Automation:** Connect new product uploads to an n8n webhook pipeline (`tbk-spfy-automations/`) for automated attribute enrichment before human review.

## 3. Ideas Backlog

| S.No. | Idea | Notes |
| ---: | --- | --- |
| 1 | Automated Visual Attribute Extraction | Classify tier count, color palette, and occasion directly from catalogue photography. |
| 2 | Taxonomy Synchronization Service | Map detected attributes to Shopify Metaobjects and product tags automatically. |
| 3 | Misclassification Guardrails | Pre-commit validation preventing occasion contradictions (e.g., kids theme vs anniversary). |
| 4 | Custom Cake Quote Vision Estimator | Customer image uploads on WhatsApp routed through n8n to provide ballpark pricing estimates. |

## 4. Scope

- **In Scope:** `tbk-spfy-ai` models, `tbk-spfy-seo/ops` GraphQL update scripts, n8n webhook configurations in `tbk-spfy-automations/`.
- **Out of Scope:** Client-side in-browser machine learning (all vision processing is asynchronous server-side).

## 5. Open Questions

1. Should production vision inference run on a local dedicated GPU worker or via cloud deployment using `microsoft-foundry`?
2. How should the pipeline handle watermarked supplier images (e.g., Zomato/TWC marks) during attribute detection?

## 6. Promotion Path

`CON002` -> Decision -> Architecture / Rules -> Plan -> Worklog.

## Footer

Parent: [`concept-design-master.md`](./concept-design-master.md) ·
Decisions: [`../decisions/decisions-master.md`](../decisions/decisions-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
