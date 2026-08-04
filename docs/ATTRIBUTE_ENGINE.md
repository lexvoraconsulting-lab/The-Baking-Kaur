# Enterprise Attribute Intelligence Engine — Overview (Build-303)

`ai/attribute_intelligence/` is the multi-source attribute reconciliation layer sitting under
`ai.product_intelligence` and `ai.knowledge`: given several candidate values for the same attribute
on the same subject, from different sources, it normalizes, validates, infers, scores, resolves ONE
winning value, and tracks the history of every change — without owning an attribute catalog of its
own. See [ADR 0010](adr/2026-08-02-attribute-intelligence-engine.md) for the full scoping decision.

## The hard requirement this design is built around

**This package resolves VALUES for attributes `ai.ear`/`ai.ead` already define — it never defines a
new attribute catalog, never duplicates Taxonomy, Product Intelligence, or Knowledge Graph.**
Every `AttributeObservation.registry_reference` is a real `ai.ear` attribute_id (`EAR-NNNNNN`).

## Package layout

```
ai/attribute_intelligence/
  models.py           AttributeObservation, ResolvedAttribute, ConflictRecord,
                       AttributeHistoryEntry, ValidationIssue, SubjectAttributeProfile
  ids.py                compute_observation_id() / compute_resolution_id() - uuid5, distinct
                       namespace UUIDs
  normalizer.py           AttributeNormalizer - wraps ai.taxonomy Term.label/.synonyms matching
  validator.py               AttributeValidator - wraps ai.ead allowed_values/confidence_expectations
  confidence.py                 AttributeConfidenceEngine - source-trust + confidence ranking
  conflicts.py                    AttributeConflictResolver - N-source conflict detection,
                                 generalizing ai.attribute_distribution.conflicts' 1-vs-1 shape
  inference.py                      AttributeInferenceEngine + TaxonomyRelationshipInferenceRule -
                                 rule-based only, no ML
  history.py                          AttributeHistoryLog - JSONL append, mirrors
                                 ai.pricing.audit.AuditEngine exactly
  search.py                             AttributeSearchService - composes ai.ear.api + ai.taxonomy
  exporter.py                             export_profile() - plain-dict snapshot, not a Shopify/
                                 ERP write (that stays ai.attribute_distribution's job)
  integration.py                            observations_from_eal() / observations_from_tags() -
                                 real adapters over ai.product_intelligence
  extensions.py                               MerchantAttributeSourcePort /
                                 GenomeAttributeSourcePort - NotConnected, no backing system exists
  observability.py                              AttributeIntelligenceObserver + CoverageReport +
                                 compute_drift()
  service.py                                      AttributeIntelligenceService - the one
                                 canonical entrypoint
  test_attribute_intelligence.py                    self-check
  test_integration.py                                 self-check
```

## Dependency graph

```
                    ┌────────────────────────────┐
                    │  AttributeIntelligenceService │   <- the ONE canonical entrypoint
                    └───────────────┬────────────────┘
      ┌──────────────┬──────────────┼──────────────┬───────────────┬───────────────┐
      ▼              ▼              ▼               ▼               ▼               ▼
AttributeNormalizer AttributeValidator AttributeInferenceEngine AttributeConfidenceEngine AttributeConflictResolver AttributeHistoryLog
      │                   │                  │                        │                     (composes Confidence)      │
      ▼                   ▼                  ▼                                                                          ▼
ai.taxonomy.        ai.ead.Definition   ai.taxonomy Relationship                                                  ai/logs/attribute_
TaxonomyCatalog        Set (allowed_       (rule-based, no ML)                                                    history.jsonl
                       values, min_
                       confidence)

integration.py (real, one-directional): reads ai.product_intelligence.ProductAggregate/
ProductReadModel + ai.ear.Registry - NEVER the reverse (would create a circular dependency,
see ADR 0010 point 4).

extensions.py: MerchantAttributeSourcePort / GenomeAttributeSourcePort - NOT wired into
AttributeIntelligenceService this sprint, no real backing system exists.
```

No circular dependencies: `ai.eal`, `ai.ear`, `ai.ead`, `ai.taxonomy`, `ai.attribute_distribution`,
and `ai.product_intelligence` are all dependency-graph leaves w.r.t. `ai.attribute_intelligence` -
none of them imports anything from it (verified both by inspection and by the fact that importing
this package succeeds at all).

## How a profile resolves (real join logic)

```
observations: list[AttributeObservation]  (from integration.py adapters + any caller-supplied ones)
      │
      ├─► AttributeInferenceEngine.infer(observations) -> extra, reduced-confidence,
      │        source="inference" observations (rule-based, e.g. via a real Taxonomy Relationship)
      │
      ├─► AttributeValidator.validate(obs, ead_definition) for every observation
      │        -> ValidationIssue[] (missing_confidence / no_definition / value_not_allowed /
      │           below_minimum_confidence)
      │
      ├─► group by (registry_reference, subject_id)
      │        AttributeConflictResolver.resolve(group) -> (winning observation, ConflictRecord|None)
      │             internally: AttributeConfidenceEngine.resolve_best() ranks by
      │             (source_trust, confidence) - manual/knowledge_graph outrank vision/shopify/
      │             merchant/seo, inference ranks lowest
      │
      ├─► AttributeHistoryLog.record_transition(previous, new) - only when the value actually changed
      │
      └─► SubjectAttributeProfile { attributes: {registry_reference: ResolvedAttribute},
                                     validation_issues, conflicts }
```

## Public interfaces

- `AttributeIntelligenceService(taxonomy_catalog, ead_definitions=None, ...)`
  - `.resolve(subject_id, observations, resolved_at) -> SubjectAttributeProfile`
- `AttributeNormalizer(catalog).normalize(raw_value, vocabulary_id_or_name=None) -> TermModel | None`
- `AttributeValidator().validate(observation, definition) -> list[ValidationIssue]`
- `AttributeConfidenceEngine().resolve_best(observations) -> (AttributeObservation, ResolutionMethod)`
- `AttributeConflictResolver().resolve(observations) -> (AttributeObservation, ConflictRecord | None)`
- `AttributeInferenceEngine(rules).infer(observations) -> list[AttributeObservation]`
- `AttributeHistoryLog().record_transition(previous, new) -> AttributeHistoryEntry`
- `AttributeSearchService(ear_registry, taxonomy_catalog)` — `.find_attributes_by_namespace/owner/tag`, `.find_terms_by_label_substring`
- `export_profile(profile) -> dict`
- `observations_from_eal(aggregate, ear_registry, observed_at)` / `observations_from_tags(read_model, mapping, observed_at)`
- `compute_coverage_report(profile, expected_registry_references) -> CoverageReport`
- `compute_drift(previous_profile, current_profile) -> dict`

## Validation checklist (Build-303's own success criteria)

- **Never duplicate data / taxonomy / Product Intelligence / Knowledge Graph** — every source of
  truth is read, never re-derived; `TaxonomyResolver`'s inline matching is duplicated by five lines
  only where retrofitting would create a circular dependency (ADR 0010 point 4), and that trade-off
  is documented, not hidden.
- **Every attribute supports Identity/Value/Confidence/Version/Source/Timestamp/Validation/
  Relationship/Observability** — `AttributeObservation`/`ResolvedAttribute` carry all nine
  (`registry_reference`+`observation_id`/`resolution_id` = identity, `value`, `confidence`,
  `ATTRIBUTE_INTELLIGENCE_VERSION`, `source`, `observed_at`/`resolved_at`, validator output,
  `conflict`/`observations`, the observer hooks).
- **Dependency injection only** — every service takes its collaborators via constructor params with
  sensible defaults, the same pattern `ai.pricing.PricingService` established.
- **No ML in inference** — `inference.py`'s only rule (`TaxonomyRelationshipInferenceRule`) walks a
  real, already-recorded Taxonomy Relationship; nothing is learned or predicted.
