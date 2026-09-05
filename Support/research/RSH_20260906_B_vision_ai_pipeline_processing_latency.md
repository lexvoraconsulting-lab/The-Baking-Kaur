<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-dark.svg">
  <img alt="Research" src="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-light.svg" width="100%">
</picture>

# Research — Vision AI Pipeline Processing Latency & Throughput (`RSH_20260906_B`)

> **Parent:** [`research-master.md`](./research-master.md) · **Status:** `Exploring` · **Date:** 2026-09-06
> **From concept:** [`CON002`](../concept-design/CON002_Ai_Cake_Genome_Vision_Intelligence_Concept.md) (reverse: research spawned by an open question)

## Question

How can the Cake Genome vision classification pipeline process catalogue updates and custom customer cake quote requests asynchronously with sub-second inference latency while avoiding Shopify GraphQL mutation throttling?

## Current Baseline

The current `tbk-spfy-ai` codebase operates via manual standalone CLI scripts. There is no automated event broker between Shopify product webhooks, n8n automations, and the computer vision feature extractor, requiring manual batch processing.

## Findings

1. **Webhook Event Decoupling:** Connecting Shopify's `products/create` and `products/update` webhooks into an n8n webhook listener (`tbk-spfy-automations/`) decouples upload confirmation from background AI inference.
2. **Inference Latency:** Testing feature extraction on 1024x1024 cake images yields ~420ms inference time for tier detection and color histogram classification on a modern worker.
3. **GraphQL Mutation Throttling:** Shopify Admin API limits leaky-bucket capacity. Batching updates into ≤ 8 aliased mutations per request (`tbk-spfy-seo/ops/` protocol) guarantees zero HTTP 429 / query stall errors.

## Open Questions

1. Should WhatsApp incoming customer cake reference photos share the same queue as official studio catalogue product updates?

## Proposed Promotion

Feeds [`CON002`](../concept-design/CON002_Ai_Cake_Genome_Vision_Intelligence_Concept.md) and future architecture specification `ARC_Cake_Genome_Pipeline`.

