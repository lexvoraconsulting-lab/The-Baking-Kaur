"""
Dynamic Visual Structure Discovery.

Spec: docs/80_Dynamic_Structure_Discovery/SPECIFICATION.md
Governed by: docs/adr/2026-08-20-n8n-python-system-of-record.md (ADR 0011)

This package lets the platform record a visual observation it has no taxonomy
home for, as an evidence-backed proposal, instead of discarding it or forcing
it into an approximate field. It never writes to ai.taxonomy or ai.ear.
"""
from ai.structure_discovery.ids import compute_observation_id, compute_proposal_id, slugify
from ai.structure_discovery.matcher import ObservationMatcher
from ai.structure_discovery.models import (
    FROZEN_LITERAL_KINDS,
    STRUCTURE_DISCOVERY_VERSION,
    DiscoveryResult,
    Evidence,
    MatchedAttribute,
    MatchState,
    ProposalKind,
    ProposalStatus,
    StructureProposal,
)
from ai.structure_discovery.proposer import build_discovery_result, propose_from_unmatched

__all__ = [
    "STRUCTURE_DISCOVERY_VERSION", "FROZEN_LITERAL_KINDS",
    "MatchState", "ProposalKind", "ProposalStatus",
    "Evidence", "StructureProposal", "MatchedAttribute", "DiscoveryResult",
    "ObservationMatcher", "propose_from_unmatched", "build_discovery_result",
    "compute_proposal_id", "compute_observation_id", "slugify",
]
