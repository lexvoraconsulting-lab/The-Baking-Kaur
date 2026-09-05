# Attribute Intelligence Engine — Inference (Build-303)

`ai.attribute_intelligence.inference` — see [ATTRIBUTE_ENGINE.md](ATTRIBUTE_ENGINE.md) for the full
architecture. Explicitly rule-based, no ML, per Build-303 Phase 4.

## Why this is not `ai.knowledge.InferenceChainRunner`

| | `ai.knowledge.InferenceChainRunner` | `ai.attribute_intelligence.AttributeInferenceEngine` |
|---|---|---|
| Operates on | Graph nodes/edges | Attribute observations |
| Mechanism | Walks a declared predicate sequence, one hop at a time | Propagates from an existing observation to a NEW candidate observation via a real Taxonomy Relationship |
| Output | A path of `KnowledgeNode`s | New `AttributeObservation`s, `source="inference"`, reduced confidence |

Complementary, not duplicative — a future integration could feed one's output into the other; not
built this sprint.

## `TaxonomyRelationshipInferenceRule` — the one rule shipped this sprint

For an observation whose value matches a Taxonomy Term, follows every real Relationship attached to
that Term. Where the related Term's Vocabulary is mapped (by the caller) to a known `EAR`
attribute, proposes a new observation for that attribute:

```python
rule = TaxonomyRelationshipInferenceRule(
    catalog, vocabulary_to_registry_reference={"TAX-VOC-000099": "EAR-000099"},
)
engine = AttributeInferenceEngine(rules=[rule])
inferred = engine.infer([colour_observation])
# colour "Red" PAIRS_WITH style "Bold" (a real Relationship) ->
# inferred == [AttributeObservation(registry_reference="EAR-000099", value="Bold",
#              source="inference", confidence=colour_observation.confidence * 0.5)]
```

`vocabulary_to_registry_reference` is always caller-supplied, never auto-derived — `ai.ear`'s own
`taxonomy_references` field is a looser, free-text reference (e.g. `"bakery.colour"`), not a
reliable Vocabulary-to-attribute join, so guessing one would risk a wrong inference presented as
real. No inference happens where the mapping is missing.

## Why every inferred observation gets `confidence_penalty` applied

An inferred value is real evidence — it comes from a genuine, already-recorded Taxonomy
Relationship — but it is one step further removed from direct observation. VIG-007's confidence
discipline requires that distinction stay visible in the number, not be laundered away by reusing
the source observation's original confidence unchanged. The default penalty is `0.5`
(`inferred.confidence = source.confidence * 0.5`), constructor-overridable.

## Why the real `ai/taxonomy/examples/catalog.json` fixture produces zero inferences

That fixture has 0 relationships recorded (confirmed during Build-302's own discovery). This
sprint's inference tests build a small, explicitly-labeled example catalog with one real
`PAIRS_WITH` relationship to prove the *mechanism* works — this is mechanism testing, not a claim
that live inference produces results against today's real taxonomy content.
