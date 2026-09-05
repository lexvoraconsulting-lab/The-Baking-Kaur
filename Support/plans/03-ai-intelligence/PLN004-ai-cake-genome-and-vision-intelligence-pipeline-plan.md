# Plan — AI Cake Genome and Vision Intelligence Pipeline (`CGV`)

> **Parent:** [`../plans-master.md`](../plans-master.md) · **Code:** `CGV`
> **Status:** Active · **Owner:** AI & Automation Team

## Sources and Traceability

| S.No. | Code | Source record | Plan role | Status |
| ---: | --- | --- | --- | --- |
| 1 | `RUL` | [`../../rules.md`](../../rules.md) | Binding constraints and governance | Current |
| 2 | `CON` | [`../../concept-design/CON002_Ai_Cake_Genome_Vision_Intelligence_Concept.md`](../../concept-design/CON002_Ai_Cake_Genome_Vision_Intelligence_Concept.md) | AI Cake Genome and vision intelligence pipeline specification | Current |

## Statistics

`TL = PD + IP + CD`. From task markers below.

| S.No. | Plan Scope | TL | PD | IP | CD |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `CGV` direct tasks | 6 | 6 | 0 | 0 |
| 2 | Total | **6** | **6** | **0** | **0** |

## Context

Integrate the Python-based Cake Genome vision feature extractor with Shopify webhooks and n8n orchestration to automatically classify cake tiers, icing styles, color palettes, and celebratory occasions, writing standardized metafields via safe batched GraphQL mutations (≤ 8–10 mutations).

## 01. AI Pipeline Tasks

- [ ] `CGV-01.01` Benchmark Cake Genome feature extraction models in `tbk-spfy-ai/ai/cake_genome/` against sample catalog images.
- [ ] `CGV-01.02` Define standardized Shopify Metafield definitions for `custom.cake_theme`, `custom.tier_count`, and `custom.flavor_profile`.
- [ ] `CGV-01.03` Configure n8n webhook workflow (`tbk-spfy-automations/`) to trigger vision processing upon product image upload.
- [ ] `CGV-01.04` Build GraphQL mutation client in `tbk-spfy-seo/ops/` enforcing ≤ 8 aliased mutations per batch.
- [ ] `CGV-01.05` Implement automated pre-commit validation preventing occasion misclassifications.
- [ ] `CGV-01.06` Run end-to-end sandbox test on 5 draft products and verify metafield updates in Shopify Admin.

## Footer Navigation

Parent: [`../plans-master.md`](../plans-master.md) · Plans Master: [`../plans-master.md`](../plans-master.md)
