"""
Enterprise Attribute Intelligence Engine (Build-303) - validation.

WHY THIS WRAPS ai.ead's EADDefinitionModel, NOT A NEW RULE SET
  allowed_values and confidence_expectations.minimum_confidence already
  exist on every EAD Definition - VIG-007's confidence/provenance
  requirements are already the law this whole platform follows.
  AttributeValidator applies those existing per-attribute rules to an
  AttributeObservation; it defines no new validation vocabulary.
"""
from ai.attribute_intelligence.models import AttributeObservation, ValidationIssue
from ai.ead.models_pydantic import EADDefinitionModel


class AttributeValidator:
    def validate(self, observation: AttributeObservation, definition: EADDefinitionModel | None) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []

        if observation.confidence is None:
            issues.append(ValidationIssue(
                code="missing_confidence", severity="warning",
                message=f"observation {observation.observation_id} has no confidence score (VIG-007 Principle 1)",
            ))

        if definition is None:
            issues.append(ValidationIssue(
                code="no_definition", severity="warning",
                message=f"no EAD Definition found for {observation.registry_reference!r} - cannot check allowed_values or minimum_confidence",
            ))
            return issues

        if definition.allowed_values is not None and observation.value not in definition.allowed_values:
            issues.append(ValidationIssue(
                code="value_not_allowed", severity="error",
                message=f"value {observation.value!r} is not in {definition.registry_reference}'s allowed_values {definition.allowed_values}",
            ))

        minimum = definition.confidence_expectations.minimum_confidence
        if observation.confidence is not None and observation.confidence < minimum:
            issues.append(ValidationIssue(
                code="below_minimum_confidence", severity="warning",
                message=f"confidence {observation.confidence} is below {definition.registry_reference}'s minimum_confidence {minimum}",
            ))

        return issues
