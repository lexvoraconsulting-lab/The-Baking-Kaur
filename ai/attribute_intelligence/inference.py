"""
Enterprise Attribute Intelligence Engine (Build-303) - rule-based inference.

WHY THIS IS NOT ai.knowledge.inference
  ai.knowledge.InferenceChainRunner walks a declared predicate sequence
  across GRAPH NODES (Product -> Category -> ... -> Delivery), one hop at a
  time. This module infers NEW ATTRIBUTE OBSERVATIONS from EXISTING ones for
  the SAME subject (e.g. "Occasion=birthday, and Taxonomy already records
  birthday PAIRS_WITH a Theme term, so propose Theme=<that term> as a
  candidate") - a different domain object (observations, not graph nodes)
  and a different mechanism (attribute propagation, not multi-hop
  traversal). Complementary, not duplicative; a future integration could
  feed one's output into the other, not built this sprint.

WHY EVERY INFERRED OBSERVATION GETS REDUCED CONFIDENCE AND source="inference"
  An inferred value is evidence one step further removed from direct
  observation than the fact it was derived from - VIG-007's confidence
  discipline requires that distinction be visible, not laundered away by
  reusing the original observation's confidence. AttributeConfidenceEngine's
  DEFAULT_SOURCE_TRUST already ranks "inference" lowest for exactly this
  reason - a real, independently-sourced observation always outranks an
  inferred one when they disagree.

WHY NO ML
  Build-303 Phase 4 is explicit: "No ML. Rule-based inference only." Every
  InferenceRule here is a plain function over already-real data (a Taxonomy
  Relationship that genuinely exists in the catalog) - it proposes nothing
  a human curator didn't already encode as a Relationship.
"""
from typing import Protocol

from ai.attribute_intelligence.models import AttributeObservation
from ai.taxonomy.catalog import TaxonomyCatalog


class InferenceRule(Protocol):
    def infer(self, observations: list[AttributeObservation]) -> list[AttributeObservation]: ...


class TaxonomyRelationshipInferenceRule:
    """For every observation whose value matches a Taxonomy Term, follows
    every Relationship attached to that Term and - where the related Term's
    Vocabulary is mapped to a known EAR attribute via
    vocabulary_to_registry_reference - proposes an observation for that
    attribute. vocabulary_to_registry_reference is DI'd rather than
    auto-derived: EAR's own taxonomy_references field is a looser, free-text
    reference (e.g. "bakery.colour"), not a reliable vocabulary_id join, so
    this rule asks the caller for the mapping it actually has rather than
    guessing one."""

    def __init__(
        self, catalog: TaxonomyCatalog, vocabulary_to_registry_reference: dict[str, str],
        confidence_penalty: float = 0.5, observed_at: str = "",
    ):
        self._catalog = catalog
        self._vocabulary_to_registry_reference = vocabulary_to_registry_reference
        self._confidence_penalty = confidence_penalty
        self._observed_at = observed_at

    def infer(self, observations: list[AttributeObservation]) -> list[AttributeObservation]:
        inferred: list[AttributeObservation] = []
        for obs in observations:
            term = self._match_term(obs.value)
            if term is None:
                continue
            for relationship in self._catalog.relationships_for("term", term.term_id):
                other_id = relationship.object_id if relationship.subject_id == term.term_id else relationship.subject_id
                other_type = relationship.object_type if relationship.subject_id == term.term_id else relationship.subject_type
                if other_type != "term":
                    continue
                other_term = self._catalog.get_term(other_id)
                if other_term is None:
                    continue
                registry_reference = self._vocabulary_to_registry_reference.get(other_term.vocabulary_id)
                if registry_reference is None:
                    continue
                inferred.append(AttributeObservation(
                    registry_reference=registry_reference, subject_id=obs.subject_id,
                    source="inference", value=other_term.label,
                    confidence=(obs.confidence or 0.5) * self._confidence_penalty,
                    observed_at=self._observed_at or obs.observed_at,
                    notes=f"inferred via {relationship.relationship_type} from {obs.registry_reference}={obs.value!r}",
                ))
        return inferred

    def _match_term(self, value):
        for term in self._catalog.terms:
            if value == term.label or value in term.synonyms:
                return term
        return None


class AttributeInferenceEngine:
    def __init__(self, rules: list[InferenceRule]):
        self._rules = rules

    def infer(self, observations: list[AttributeObservation]) -> list[AttributeObservation]:
        inferred: list[AttributeObservation] = []
        for rule in self._rules:
            inferred.extend(rule.infer(observations))
        return inferred
