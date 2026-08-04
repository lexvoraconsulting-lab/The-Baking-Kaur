# Attribute Intelligence Engine — Normalization (Build-303)

`ai.attribute_intelligence.normalizer` — see [ATTRIBUTE_ENGINE.md](ATTRIBUTE_ENGINE.md) for the
full architecture.

## The mechanism: controlled-vocabulary matching, not string heuristics

Phase 3 asked for "Birthday Cake / Birthday Cakes / Birthday / Birthday Theme → Birthday". This is
exactly what `ai.taxonomy.Term.label` + `Term.synonyms` already model (a canonical label plus its
known aliases, scoped to a Vocabulary) — `Relationship_Model.md` is explicit that new vocabulary
"is added the same way a new vocabulary Term is added... never invented ad hoc inline." This
package adds no separate synonym table; it matches against the one that already exists.

```python
from ai.attribute_intelligence.normalizer import AttributeNormalizer

normalizer = AttributeNormalizer(taxonomy_catalog)
term = normalizer.normalize("Crimson", vocabulary_id_or_name="Colour Name")
# term.label == "Red" - "Crimson" was already a synonym of the real "Red" Term
```

`normalize_against_vocabulary` scopes the search to one Vocabulary (fast, precise, when the caller
already knows which controlled list a raw value should map to). `normalize_against_any_vocabulary`
searches every Vocabulary in the catalog — useful for a free-text tag with no namespace hint.

## Why unmatched values return `None`, never a guess

`ai.attribute_intelligence` follows the platform-wide "never fabricate" rule exactly like every
other module: if `raw_value` doesn't match any Term's label or synonym, normalization returns
`None`. A caller decides what to do with an unmatched value (flag it for curation, keep the raw
string, discard it) — this package never invents a canonical value that isn't a real, controlled
Term.

## Where this is used

`AttributeIntelligenceService` does not call the normalizer directly on every observation today —
normalization is exposed as a standalone, reusable tool for callers assembling `AttributeObservation`s
from raw strings (e.g. a future Shopify-tag adapter that needs to map a free-text tag to a
controlled value before constructing an observation). `integration.observations_from_tags` already
receives pre-namespaced tag values and doesn't need it for the current worked example; a future
adapter for unstructured text would.

## Why `ai.product_intelligence.resolvers.TaxonomyResolver` keeps its own copy of this logic

See [ADR 0010](adr/2026-08-02-attribute-intelligence-engine.md) point 4 — retrofitting it to call
this normalizer would create a circular package dependency
(`product_intelligence -> attribute_intelligence -> product_intelligence`, since this package's
`integration.py` reads FROM `ai.product_intelligence`). The five duplicated lines are the
documented, deliberate trade-off.
