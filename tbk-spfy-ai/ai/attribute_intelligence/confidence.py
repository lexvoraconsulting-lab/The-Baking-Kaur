"""
Enterprise Attribute Intelligence Engine (Build-303) - the Confidence Engine.

WHY A SOURCE-TRUST RANKING, NOT JUST THE RAW confidence FIELD
  Two observations can each carry a perfectly valid confidence score and
  still disagree on which source should win when values conflict - a Vision
  call at 0.95 confidence is not automatically more trustworthy than a
  Manual entry at 0.80, because a human correction is definitionally more
  authoritative than an AI guess, regardless of the AI's own self-reported
  certainty. DEFAULT_SOURCE_TRUST encodes that ordering explicitly and
  config-driven (constructor-injected, overridable), the same "illustrative,
  not fabricated fact" posture ai.pricing's config files already established
  - this ranking is a business policy, not a measured metric, and is
  documented as such.
"""
from dataclasses import dataclass, field

from ai.attribute_intelligence.models import AttributeObservation, ResolutionMethod, Source

# Highest number wins. Manual (human-verified) and Knowledge Graph (already-
# reconciled, cross-system data) rank above raw single-source signals;
# inference (this package's own rule-based guesses) ranks lowest since it is
# derived from other observations, never independent evidence.
DEFAULT_SOURCE_TRUST: dict[Source, int] = {
    "manual": 100,
    "knowledge_graph": 80,
    "vision": 60,
    "shopify": 50,
    "merchant": 40,
    "seo": 30,
    "genome": 60,
    "inference": 10,
}


@dataclass(frozen=True)
class RankedObservation:
    observation: AttributeObservation
    trust_score: int


@dataclass
class AttributeConfidenceEngine:
    source_trust: dict[Source, int] = field(default_factory=lambda: dict(DEFAULT_SOURCE_TRUST))

    def rank(self, observations: list[AttributeObservation]) -> list[RankedObservation]:
        ranked = [
            RankedObservation(obs, self.source_trust.get(obs.source, 0))
            for obs in observations
        ]
        ranked.sort(key=lambda r: (r.trust_score, r.observation.confidence or 0.0), reverse=True)
        return ranked

    def resolve_best(
        self, observations: list[AttributeObservation],
    ) -> tuple[AttributeObservation, ResolutionMethod]:
        if not observations:
            raise ValueError("resolve_best() requires at least one observation")
        if len(observations) == 1:
            return observations[0], "single_source"

        ranked = self.rank(observations)
        winner = ranked[0]
        distinct_values = {r.observation.value for r in ranked}
        if len(distinct_values) == 1:
            return winner.observation, "single_source"  # multiple sources agree - not a real conflict

        runner_up = ranked[1]
        if winner.trust_score != runner_up.trust_score:
            return winner.observation, "highest_trust"
        return winner.observation, "highest_confidence"
