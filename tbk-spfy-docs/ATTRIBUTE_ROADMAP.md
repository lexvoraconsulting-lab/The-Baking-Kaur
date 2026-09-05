# Attribute Intelligence Engine — Roadmap (Build-303)

What Build-303 did not build, in priority order. None of this is started; nothing here should be
read as committed or scheduled.

## 1. Real EAR/EAD content for Phase 2's illustrative attribute list

Primary Occasion, Theme, Style, Luxury Score, Wedding Score, etc. need real `ai.ear`/`ai.ead`
entries (canonical name, namespace, owner, allowed_values, confidence_expectations) before this
engine can resolve them for real. Content curation, not engineering — belongs to EAR/EAD's own
governance process, not this sprint.

## 2. Wire `AttributeIntelligenceService.resolve()` into a live pipeline

Today it's called with caller-assembled observation lists in tests. A real pipeline would call
`integration.observations_from_eal`/`observations_from_tags` against a live
`ai.product_intelligence.ProductIntelligenceService` result, on a real schedule or on-demand.

## 3. Feed `ResolvedAttribute` into `ai.attribute_distribution`

This package resolves a value; writing it to Shopify/ERP is `ai.attribute_distribution`'s job. The
natural next step is a thin adapter: `ResolvedAttribute` → `DistributionRecord`
(`registry_reference`, `value`, `human_verification_status` derived from `source`/`resolution_method`)
— not built this sprint, see [ADR 0010](adr/2026-08-02-attribute-intelligence-engine.md) point 6.

## 4. Knowledge Graph integration

A `ResolvedAttribute` is a natural `KnowledgeEdge` source (e.g. Product `HAS_COLOR` a resolved
Colour value) — today `ai.knowledge.ProductGraphResolver` derives colour/style edges directly from
`ai.product_intelligence`'s taxonomy match, bypassing this engine entirely. Once this engine is
live-wired (item 2), `ai.knowledge` could consume its `ResolvedAttribute`s instead — a genuine
quality improvement (conflict-aware, multi-source) over today's single-source taxonomy match, not
built this sprint.

## 5. Real Merchant and Genome sources

`MerchantAttributeSourcePort`/`GenomeAttributeSourcePort` (extensions.py) become real the moment
their backing systems exist — same status as `ai.knowledge.extensions`'s equivalent ports.

## 6. Caching / incremental resolution

Every `resolve()` call re-runs inference, validation, and conflict resolution from scratch.
`AttributeIntelligenceService` already tracks `_previous_profiles` in memory for history purposes;
a real deployment would need to decide a persistence/caching strategy once call volume exists to
justify one — premature to build against zero real callers.

## 7. Drift-based alerting

`observability.compute_drift()` is a pure function today, called manually. A real deployment would
wire it into `AttributeIntelligenceObserver.on_profile_resolved` to alert when a high-confidence,
previously-stable attribute suddenly changes value — not built this sprint (no alerting
infrastructure exists anywhere in this repo's `ai/` layer to wire it into).

## 8. A free-text normalization adapter

`AttributeNormalizer` is ready for a caller with raw, unstructured text (a customer review, a
product description) to normalize against a Vocabulary — no such adapter exists yet; today's only
integration (`integration.observations_from_tags`) already receives pre-namespaced values.
