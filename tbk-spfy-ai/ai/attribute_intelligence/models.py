"""
Enterprise Attribute Intelligence Engine (Build-303) - plain dataclass models.

WHAT THIS PACKAGE IS
  The multi-source reconciliation layer sitting UNDER ai.product_intelligence
  and ai.knowledge: given several candidate values for the same attribute on
  the same subject, from different sources (Shopify, Vision/EAL, Manual,
  Merchant, SEO, Knowledge Graph, future Genome), it normalizes, validates,
  infers, scores, and resolves ONE winning value per attribute - tracking
  every losing candidate and every version transition, never silently
  overwriting. It owns no attribute catalog of its own: `registry_reference`
  is always a real ai.ear attribute_id (EAR-NNNNNN); this package resolves
  VALUES for attributes EAR/EAD already define, it does not define new ones.

WHY AttributeObservation IS NEW, NOT A REUSE OF EALAttributeRecord
  ai.eal.EALAttributeRecord already carries confidence+provenance, but it is
  scoped to ONE entity_id (an image/region/object) from ONE extraction call -
  it has no concept of "this is one of several competing candidate values
  for the same subject's attribute from different kinds of sources" (Shopify
  tag vs. Vision output vs. a human's manual entry). AttributeObservation
  generalizes that shape across sources without touching ai.eal's frozen
  model; a Vision-sourced observation is trivially constructed FROM an
  EALAttributeRecord (see integration.py), not a competing reimplementation
  of it.

WHY ResolvedAttribute KEEPS EVERY LOSING OBSERVATION, NEVER JUST THE WINNER
  Phase 5's "never silently overwrite" - the same discipline
  ai.attribute_distribution.conflicts already established for one-source-vs-
  downstream conflicts, generalized here to N sources. Discarding the
  runners-up would make a future re-resolution (a new source arrives, a
  source's trust ranking changes) impossible to redo without re-collecting
  every observation from scratch.
"""
from dataclasses import dataclass, field
from typing import Any, Literal

from ai.attribute_intelligence.ids import compute_observation_id, compute_resolution_id

ATTRIBUTE_INTELLIGENCE_VERSION = "1.0"

Source = Literal[
    "shopify", "vision", "manual", "merchant", "seo", "knowledge_graph", "genome", "inference",
]

ResolutionMethod = Literal["single_source", "highest_trust", "highest_confidence", "unresolved"]


@dataclass(frozen=True)
class AttributeObservation:
    """One candidate value for one attribute on one subject, from one
    source. subject_id is deliberately a plain string (a Shopify GID today,
    any future entity's identifier tomorrow) - this package does not care
    what kind of thing the subject is, only that observations about it can
    be compared."""
    registry_reference: str
    subject_id: str
    source: Source
    value: Any
    confidence: float | None
    observed_at: str
    observation_id: str = ""
    notes: str | None = None

    def __post_init__(self):
        if not self.observation_id:
            object.__setattr__(
                self, "observation_id",
                compute_observation_id(self.registry_reference, self.subject_id, self.source, self.observed_at),
            )


@dataclass(frozen=True)
class ConflictRecord:
    """Produced whenever two or more observations for the same
    (registry_reference, subject_id) disagree on value - kept alongside the
    ResolvedAttribute that won, never replacing the losing observations."""
    registry_reference: str
    subject_id: str
    competing_observations: tuple[AttributeObservation, ...]
    resolved_observation_id: str
    resolution_method: ResolutionMethod


@dataclass(frozen=True)
class ResolvedAttribute:
    registry_reference: str
    subject_id: str
    value: Any
    confidence: float | None
    source: Source
    resolved_at: str
    resolution_id: str = ""
    resolution_method: ResolutionMethod = "single_source"
    observations: tuple[AttributeObservation, ...] = ()
    conflict: ConflictRecord | None = None
    version: str = ATTRIBUTE_INTELLIGENCE_VERSION

    def __post_init__(self):
        if not self.resolution_id:
            object.__setattr__(
                self, "resolution_id",
                compute_resolution_id(self.registry_reference, self.subject_id, self.resolved_at),
            )


@dataclass(frozen=True)
class AttributeHistoryEntry:
    """One append-only log line - see history.py. Records a value
    transition, not just a snapshot, so "what did this attribute used to be"
    is answerable without replaying every ResolvedAttribute ever produced."""
    registry_reference: str
    subject_id: str
    previous_value: Any
    new_value: Any
    resolution_id: str
    recorded_at: str


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: Literal["error", "warning"]
    message: str


@dataclass(frozen=True)
class SubjectAttributeProfile:
    """The per-subject output of AttributeIntelligenceService.resolve() -
    every ResolvedAttribute keyed by registry_reference, plus whatever
    validation issues and conflicts surfaced along the way."""
    subject_id: str
    resolved_at: str
    attributes: dict[str, ResolvedAttribute] = field(default_factory=dict)
    validation_issues: tuple[ValidationIssue, ...] = ()
    conflicts: tuple[ConflictRecord, ...] = ()
