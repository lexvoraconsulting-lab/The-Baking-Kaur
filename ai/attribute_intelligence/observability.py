"""
Enterprise Attribute Intelligence Engine (Build-303) - observability.

WHY A COVERAGE REPORT PLUS A SEPARATE DRIFT FUNCTION, NOT ONE MEGA-REPORT
  Coverage (unknown/missing/low-confidence/conflicts/validation errors) is a
  property of ONE SubjectAttributeProfile snapshot. Drift is inherently
  comparative (this profile vs. a previous one) - conflating the two into
  one function would force every coverage call to also supply a "previous"
  profile it may not have. Both are pure functions of already-computed
  profiles, mirroring ai.knowledge.observability.compute_health_report's
  "pure function over a snapshot" shape.
"""
import logging
from abc import ABC
from dataclasses import dataclass

from ai.attribute_intelligence.models import SubjectAttributeProfile

_logger = logging.getLogger("ai.attribute_intelligence")


class AttributeIntelligenceObserver(ABC):
    def on_profile_resolved(self, profile: SubjectAttributeProfile) -> None:
        pass

    def on_conflict(self, subject_id: str, registry_reference: str) -> None:
        pass

    def on_validation_error(self, subject_id: str, message: str) -> None:
        pass


class NullObserver(AttributeIntelligenceObserver):
    """The default - see ai.pricing.observability.NullObserver's rationale."""


class LoggingObserver(AttributeIntelligenceObserver):
    def on_profile_resolved(self, profile: SubjectAttributeProfile) -> None:
        _logger.info(
            "attribute_intelligence.resolved subject=%s attributes=%d conflicts=%d",
            profile.subject_id, len(profile.attributes), len(profile.conflicts),
        )

    def on_conflict(self, subject_id: str, registry_reference: str) -> None:
        _logger.warning("attribute_intelligence.conflict subject=%s attribute=%s", subject_id, registry_reference)

    def on_validation_error(self, subject_id: str, message: str) -> None:
        _logger.warning("attribute_intelligence.validation_error subject=%s message=%s", subject_id, message)


@dataclass(frozen=True)
class CoverageReport:
    subject_id: str
    expected_count: int
    covered_registry_references: tuple[str, ...]
    missing_registry_references: tuple[str, ...]
    unknown_registry_references: tuple[str, ...]
    low_confidence_registry_references: tuple[str, ...]
    conflict_count: int
    validation_error_count: int
    inference_quality: float | None

    @property
    def completeness(self) -> float:
        if self.expected_count == 0:
            return 1.0
        return len(self.covered_registry_references) / self.expected_count


def compute_coverage_report(
    profile: SubjectAttributeProfile, expected_registry_references: list[str],
    low_confidence_threshold: float = 0.5,
) -> CoverageReport:
    expected = set(expected_registry_references)
    covered = set(profile.attributes.keys())

    low_confidence = tuple(sorted(
        ref for ref, resolved in profile.attributes.items()
        if resolved.confidence is not None and resolved.confidence < low_confidence_threshold
    ))

    inferred_total = 0
    inferred_won = 0
    for resolved in profile.attributes.values():
        was_offered_by_inference = any(obs.source == "inference" for obs in resolved.observations)
        if was_offered_by_inference:
            inferred_total += 1
            if resolved.source == "inference":
                inferred_won += 1

    return CoverageReport(
        subject_id=profile.subject_id,
        expected_count=len(expected),
        covered_registry_references=tuple(sorted(covered)),
        missing_registry_references=tuple(sorted(expected - covered)),
        unknown_registry_references=tuple(sorted(covered - expected)) if expected else (),
        low_confidence_registry_references=low_confidence,
        conflict_count=len(profile.conflicts),
        validation_error_count=sum(1 for i in profile.validation_issues if i.severity == "error"),
        inference_quality=(inferred_won / inferred_total) if inferred_total else None,
    )


def compute_drift(
    previous: SubjectAttributeProfile, current: SubjectAttributeProfile,
) -> dict[str, tuple[object, object]]:
    """registry_reference -> (previous_value, new_value) for every attribute
    whose resolved value changed between two profiles for the same
    subject."""
    drifted = {}
    for registry_reference, resolved in current.attributes.items():
        previous_resolved = previous.attributes.get(registry_reference)
        previous_value = previous_resolved.value if previous_resolved else None
        if previous_resolved is None or previous_value != resolved.value:
            drifted[registry_reference] = (previous_value, resolved.value)
    return drifted
