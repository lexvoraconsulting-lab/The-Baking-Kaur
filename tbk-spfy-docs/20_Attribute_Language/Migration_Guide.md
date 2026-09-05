# EAL — Migration Guide: Vision Engine → EAL

## Scope

How today's Vision Engine output ([`docs/AI/VisionPipeline.md`](../AI/VisionPipeline.md),
`ai/vision/python/pipeline.py`'s `VisionResult`) maps onto an `EALAttributeRecord`, **without
changing the Vision Engine itself**. This is a mapping document, not a migration script — Build-001
ships no code that touches `ai/vision/`.

## Field mapping

| `VisionResult` field (today) | EAL field | Notes |
|---|---|---|
| `image_id` (`TBK_IMAGE_ID`, from `compute_image_id`) | `entity_id` | Same content-hash identifier scheme — [Identifier_Strategy.md](Identifier_Strategy.md) reuses it, doesn't replace it. |
| `schema_version` | `provenance.schema_version` | Direct copy. |
| `taxonomy_version` | `provenance.taxonomy_version` | Direct copy. |
| `provider` | `provenance.provider` | Direct copy (today: `"ollama"`). |
| `model` | `provenance.model` | Direct copy (today: e.g. `"qwen2.5vl:3b"`). |
| raw text `response` | *(not yet mapped)* | See "What's not solved yet" below. |
| *(none today)* | `entity_type: "image"` | Every current Vision Engine run analyzes a whole image, never yet a Region or Object — see [docs/10_Taxonomy/Entity_Model.md](../10_Taxonomy/Entity_Model.md). |

## What's not solved yet: raw text → structured Attribute Records

The Vision Engine's `provider.analyze()` call returns unstructured model text today —
[VisionPipeline.md](../AI/VisionPipeline.md) documents `extractor_v1.md` as an intentionally empty
prompt placeholder, with the real structured-output parsing step (`Observation` → candidate
Attribute) explicitly deferred to Sprint 2.3+
([docs/10_Taxonomy/Roadmap.md](../10_Taxonomy/Roadmap.md)). EAL defines the *target* shape that
step will populate (one `EALAttributeRecord` per extracted attribute, per
[`vision_output_example.json`](../../ai/eal/examples/vision_output_example.json)) — it does not
implement the extraction/parsing itself, since there is no real taxonomy or prompt to parse against
yet.

## Why this is safe to author now, before that parsing step exists

Per [VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) and the pattern already used for
`TBK_IMAGE_ID` ([VisionPipeline.md](../AI/VisionPipeline.md)): introducing the identity/versioning
scheme *before* volume exists is materially cheaper than retrofitting it after. EAL is the same bet
one layer up — the wire format is ready the moment Sprint 2.3 needs to emit it, with zero rework of
this document required.

## Related Standards

[docs/AI/VisionPipeline.md](../AI/VisionPipeline.md), [docs/AI/Roadmap.md](../AI/Roadmap.md),
[docs/10_Taxonomy/Roadmap.md](../10_Taxonomy/Roadmap.md) (Sprint 2.3+),
[Identifier_Strategy.md](Identifier_Strategy.md), [Provenance_Standard.md](Provenance_Standard.md).
