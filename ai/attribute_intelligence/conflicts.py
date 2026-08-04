"""
Enterprise Attribute Intelligence Engine (Build-303) - conflict resolution.

WHY THIS GENERALIZES ai.attribute_distribution.conflicts RATHER THAN IMPORTING IT
  ai.attribute_distribution.conflicts.detect_conflict compares exactly ONE
  resolved value against ONE downstream system's current value - a
  one-vs-one shape. This module's job is N-vs-N: several sources may each
  hold a different candidate value for the same attribute before any of
  them is "the" resolved value yet. The two are complementary, not
  duplicative: this package could produce the resolved value that later
  becomes the input ai.attribute_distribution checks against a downstream
  system - but that wiring is future work (see docs/ATTRIBUTE_ROADMAP.md),
  not built this sprint, and the two conflict shapes are different enough
  that importing one into the other would be a type mismatch, not reuse.
"""
from collections import defaultdict

from ai.attribute_intelligence.confidence import AttributeConfidenceEngine
from ai.attribute_intelligence.models import AttributeObservation, ConflictRecord


class AttributeConflictResolver:
    def __init__(self, confidence_engine: AttributeConfidenceEngine | None = None):
        self._confidence_engine = confidence_engine or AttributeConfidenceEngine()

    def resolve(
        self, observations: list[AttributeObservation],
    ) -> tuple[AttributeObservation, ConflictRecord | None]:
        """observations must all share the same (registry_reference,
        subject_id) - the caller (service.py) is responsible for grouping;
        this function does not silently mix unrelated attributes."""
        winner, method = self._confidence_engine.resolve_best(observations)
        distinct_values = {obs.value for obs in observations}
        if len(distinct_values) <= 1:
            return winner, None  # every observation agrees - not a conflict, never discarded either

        conflict = ConflictRecord(
            registry_reference=observations[0].registry_reference,
            subject_id=observations[0].subject_id,
            competing_observations=tuple(observations),
            resolved_observation_id=winner.observation_id,
            resolution_method=method,
        )
        return winner, conflict

    @staticmethod
    def group_by_attribute(
        observations: list[AttributeObservation],
    ) -> dict[tuple[str, str], list[AttributeObservation]]:
        groups: dict[tuple[str, str], list[AttributeObservation]] = defaultdict(list)
        for obs in observations:
            groups[(obs.registry_reference, obs.subject_id)].append(obs)
        return dict(groups)
