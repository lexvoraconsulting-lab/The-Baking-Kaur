<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/architecture-dark.svg">
  <img alt="Architecture" src="../../skills/ThemeStyleOps/assets/banners/lexvora/architecture-light.svg" width="100%">
</picture>

# ARC_20260906_D — Cake Genome & Vision AI Architecture

> **Date:** 2026-09-06 · **Status:** Current Architecture
> **Related Concepts:** [`CON002`](../concept-design/CON002_Ai_Cake_Genome_Vision_Intelligence_Concept.md)
> **Related Research:** [`RSH_20260906_B`](../research/RSH_20260906_B_vision_ai_pipeline_processing_latency.md)
> **Owning Plan:** [`CGV`](../plans/03-ai-intelligence/PLN004-ai-cake-genome-and-vision-intelligence-pipeline-plan.md)

---

## 1. Pipeline Architecture

```text
[Shopify Product Image Upload]
       |
       v (Webhook)
[n8n Event Broker: tbk-spfy-automations]
       |
       v (Async Job)
[Python Cake Genome Engine: tbk-spfy-ai]
  - Tier Count Detection
  - Palette & Icing Extraction
  - Occasion & Theme Inference
       |
       v (Confidence Scoring & VIG-000 Gate)
[Shopify Admin GraphQL Client: tbk-spfy-seo/ops]
  - Batched Metafield Updates (<= 8 mutations)
```

## 2. Canonical Attributes

| S.No. | Attribute Key | Description | Shopify Metafield Target |
| ---: | --- | --- | --- |
| 1 | `dietary_standard` | 100% Eggless certification | `custom.dietary_standard` |
| 2 | `tier_count` | Number of cake tiers (1, 2, 3+) | `custom.tier_count` |
| 3 | `cake_theme` | Primary decorative theme | `custom.cake_theme` |
| 4 | `celebratory_occasion` | Birthday, Anniversary, Baby Shower | `custom.occasion` |
| 5 | `flavor_profile` | Chocolate, Fruit, Red Velvet, Truffle | `custom.flavor_profile` |
