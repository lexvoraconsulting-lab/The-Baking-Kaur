"""
Enterprise Attribute Intelligence Engine (Build-303) - the canonical service.

WHY THIS CLASS IS "THE" AttributeResolver
  Phase 7 named eight services (AttributeResolver, AttributeNormalizer,
  AttributeValidator, AttributeInference, AttributeConfidence,
  AttributeHistory, AttributeSearch, AttributeExporter). Seven already exist
  as their own focused classes/functions (normalizer.py, validator.py,
  inference.py, confidence.py, history.py, search.py, exporter.py) -
  AttributeIntelligenceService.resolve() IS the resolver: the orchestrator
  that wires the other seven together into one canonical call, exactly the
  role ProductIntelligenceService and KnowledgeGraphService already played
  for their own sprints. Naming it "Service" rather than "AttributeResolver"
  keeps this repo's established top-level-orchestrator naming convention
  consistent across all three engines.
"""
from ai.attribute_intelligence.confidence import AttributeConfidenceEngine
from ai.attribute_intelligence.conflicts import AttributeConflictResolver
from ai.attribute_intelligence.history import AttributeHistoryLog
from ai.attribute_intelligence.inference import AttributeInferenceEngine
from ai.attribute_intelligence.models import AttributeObservation, ResolvedAttribute, SubjectAttributeProfile
from ai.attribute_intelligence.normalizer import AttributeNormalizer
from ai.attribute_intelligence.observability import AttributeIntelligenceObserver, NullObserver
from ai.attribute_intelligence.validator import AttributeValidator
from ai.ead.definitions import DefinitionSet
from ai.taxonomy.catalog import TaxonomyCatalog


class AttributeIntelligenceService:
    def __init__(
        self,
        taxonomy_catalog: TaxonomyCatalog,
        ead_definitions: DefinitionSet | None = None,
        normalizer: AttributeNormalizer | None = None,
        validator: AttributeValidator | None = None,
        inference_engine: AttributeInferenceEngine | None = None,
        confidence_engine: AttributeConfidenceEngine | None = None,
        conflict_resolver: AttributeConflictResolver | None = None,
        history_log: AttributeHistoryLog | None = None,
        observer: AttributeIntelligenceObserver | None = None,
    ):
        self._definitions = ead_definitions
        self._normalizer = normalizer or AttributeNormalizer(taxonomy_catalog)
        self._validator = validator or AttributeValidator()
        self._inference_engine = inference_engine or AttributeInferenceEngine(rules=[])
        self._confidence_engine = confidence_engine or AttributeConfidenceEngine()
        self._conflict_resolver = conflict_resolver or AttributeConflictResolver(self._confidence_engine)
        self._history_log = history_log or AttributeHistoryLog()
        self._observer = observer or NullObserver()
        self._previous_profiles: dict[str, SubjectAttributeProfile] = {}

    def resolve(
        self, subject_id: str, observations: list[AttributeObservation], resolved_at: str,
    ) -> SubjectAttributeProfile:
        inferred = self._inference_engine.infer(observations)
        all_observations = list(observations) + inferred

        validation_issues = []
        for obs in all_observations:
            definition = self._definitions.get(obs.registry_reference) if self._definitions else None
            issues = self._validator.validate(obs, definition)
            validation_issues.extend(issues)
            for issue in issues:
                if issue.severity == "error":
                    self._observer.on_validation_error(subject_id, issue.message)

        groups = self._conflict_resolver.group_by_attribute(all_observations)
        resolved_attributes: dict[str, ResolvedAttribute] = {}
        conflicts = []
        for (registry_reference, subj), group in groups.items():
            winner, conflict = self._conflict_resolver.resolve(group)
            resolved = ResolvedAttribute(
                registry_reference=registry_reference, subject_id=subj,
                value=winner.value, confidence=winner.confidence, source=winner.source,
                resolved_at=resolved_at,
                resolution_method=conflict.resolution_method if conflict else "single_source",
                observations=tuple(group), conflict=conflict,
            )
            resolved_attributes[registry_reference] = resolved
            if conflict:
                conflicts.append(conflict)
                self._observer.on_conflict(subj, registry_reference)

        profile = SubjectAttributeProfile(
            subject_id=subject_id, resolved_at=resolved_at,
            attributes=resolved_attributes, validation_issues=tuple(validation_issues),
            conflicts=tuple(conflicts),
        )

        previous = self._previous_profiles.get(subject_id)
        for registry_reference, resolved in resolved_attributes.items():
            previous_resolved = previous.attributes.get(registry_reference) if previous else None
            if previous_resolved is None or previous_resolved.value != resolved.value:
                self._history_log.record_transition(previous_resolved, resolved)
        self._previous_profiles[subject_id] = profile

        self._observer.on_profile_resolved(profile)
        return profile
