# Attribute Intelligence Engine — Confidence (Build-303)

`ai.attribute_intelligence.confidence` — see [ATTRIBUTE_ENGINE.md](ATTRIBUTE_ENGINE.md) for the
full architecture.

## Two numbers, not one: `confidence` and source trust

`AttributeObservation.confidence` is what the *source itself* reports (a Vision model's own
certainty, a fixed 1.0 for a direct Shopify tag read, a human's implicit certainty for a manual
entry). `DEFAULT_SOURCE_TRUST` is a *separate*, business-policy ranking of which kind of source
should win when two observations disagree on value, independent of either one's self-reported
confidence:

```python
DEFAULT_SOURCE_TRUST = {
    "manual": 100, "knowledge_graph": 80, "vision": 60, "genome": 60,
    "shopify": 50, "merchant": 40, "seo": 30, "inference": 10,
}
```

A Vision call at 0.99 confidence does not beat a Manual correction at 0.50 confidence — a human
correction is definitionally more authoritative than an AI guess, regardless of how certain the AI
claims to be. This ranking is documented and overridable
(`AttributeConfidenceEngine(source_trust={...})`), the same "illustrative, config-driven, not a
measured fact" posture `ai.pricing`'s rate-card config files already established.

## `resolve_best()` — three outcomes

| `ResolutionMethod` | When |
|---|---|
| `single_source` | Only one observation exists, OR every observation agrees on value (multiple sources confirming the same fact is not a conflict) |
| `highest_trust` | Observations disagree, and the winning source outranks the runner-up |
| `highest_confidence` | Observations disagree, sources tie in trust — the higher `confidence` value breaks the tie |
| `unresolved` | Reserved for a future case with no observations at all — `resolve_best([])` raises `ValueError` today rather than silently returning this |

## Why `inference` ranks lowest

An inferred observation (see [ATTRIBUTE_INFERENCE.md](ATTRIBUTE_INFERENCE.md)) is evidence one step
further removed from direct observation than whatever it was derived from. Ranking it below every
real source means a genuine, independently-sourced observation always overrides an inferred guess
when they disagree — inference only wins when nothing else has an opinion.
