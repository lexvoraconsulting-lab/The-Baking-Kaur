"""
Dynamic Visual Structure Discovery - models.

Implements docs/80_Dynamic_Structure_Discovery/SPECIFICATION.md sections 7.2
and 7.3. This package holds PROPOSALS and their EVIDENCE. It defines no
attribute, owns no vocabulary, and stores no canonical value.

WHY A SEPARATE PACKAGE RATHER THAN FIELDS ON ai.taxonomy
  ai.taxonomy's entries deliberately carry no confidence and no provenance -
  they are the canonical meaning layer, not records ABOUT an entity. That is
  correct, and it is exactly why the evidence for a proposed structure has
  nowhere to live there (spec gap G2). Adding confidence/provenance to frozen
  Build-005 models to solve this would corrupt the layer that is right.

WHY Evidence EMBEDS ai.eal.models.Provenance RATHER THAN RESTATING IT
  Provenance already carries provider/model/model_version/prompt_version/
  schema_version/taxonomy_version/extracted_at - every field a proposal needs.
  A second provenance shape would be the duplicate-system failure ECP-100 14
  found this repository has so far avoided everywhere.

WHY status IS NOT ai.taxonomy.EntryStatus
  EntryStatus is ["active", "deprecated"] - it has no "proposed" value
  (spec gap G1), and widening it touches frozen Build-005 code behind gate
  AR-007. ProposalStatus is this package's own lifecycle and never leaks into
  a taxonomy record. Nothing here writes to ai.taxonomy.
"""
from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from ai.eal.models import Provenance
from ai.structure_discovery.ids import compute_proposal_id

STRUCTURE_DISCOVERY_VERSION = "1.0"

MatchState = Literal[
    "matched",           # resolved to an active taxonomy element
    "matched_synonym",   # resolved via Term.synonyms
    "ambiguous",         # more than one active element fits -> review, never guess
    "unmatched",         # observed, nothing fits -> drives a proposal
    "not_applicable",    # pairs with value_state "null"
    "undetermined",      # pairs with value_state "unknown"
]

ProposalKind = Literal[
    "attribute",          # -> EAR entry, status "draft" (mechanism already exists)
    "term",               # -> Term, status "proposed"
    "vocabulary",
    "attribute_group",
    "category",
    "relationship",
    "relationship_type",  # widens a frozen Literal: ADR + gate required
    "entity_type",        # widens a frozen Literal: ADR + gate required
]

ProposalStatus = Literal[
    "observed",   # seen once, below the promotion threshold
    "candidate",  # deduped, occurrence_count above threshold
    "validated",  # passed all four validation dimensions - still NOT canonical
    "approved",   # human-approved; promotion executed
    "rejected",   # human-rejected; retained, never deleted
    "merged",     # duplicate of an existing element; superseded_by is set
    "deferred",
]

# Kinds whose promotion would widen a Literal inside a frozen package.
# Recorded and reviewable; never auto-promotable. Spec section 5.3.
FROZEN_LITERAL_KINDS = ("relationship_type", "entity_type")


@dataclass(frozen=True)
class Evidence:
    """Why this proposal exists. The genuinely new record in this package."""
    image_id: str
    observation_id: str
    raw_fragment: str          # the model's own words, verbatim, never paraphrased
    provenance: Provenance
    region: dict | None = None


@dataclass(frozen=True)
class StructureProposal:
    proposal_kind: ProposalKind
    canonical_name: str        # normalized slug - the dedupe key
    label: str
    status: ProposalStatus = "observed"
    proposal_id: str = ""
    parent_reference: str | None = None       # target vocabulary_id / group_id / EAR-NNNNNN
    suggested_data_type: str | None = None    # ai.eal DataType, reused
    suggested_vocabulary: str | None = None
    confidence: float | None = None
    occurrence_count: int = 1
    first_seen: str = ""
    last_seen: str = ""
    evidence: tuple[Evidence, ...] = ()
    validation_issues: tuple[Any, ...] = ()
    why_unmatched: str | None = None
    superseded_by: str | None = None
    taxonomy_version: str = ""                # the version this was proposed AGAINST
    promoted_to: str | None = None            # the real ID created on approval
    requires_gate: bool = False               # True for FROZEN_LITERAL_KINDS
    likely_duplicate_of: str | None = None    # an existing active element with the same name

    def __post_init__(self):
        if not self.proposal_id:
            object.__setattr__(
                self, "proposal_id",
                compute_proposal_id(self.proposal_kind, self.canonical_name),
            )
        if self.proposal_kind in FROZEN_LITERAL_KINDS and not self.requires_gate:
            object.__setattr__(self, "requires_gate", True)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class MatchedAttribute:
    """A resolved observation, carrying enough to build an ai.eal record."""
    group: str
    group_id: str
    attribute: str
    attribute_id: str
    value: Any
    value_state: str
    match_state: MatchState
    data_type: str
    vocabulary: str | None = None
    term_id: str | None = None
    normalized_value: Any = None
    confidence: float | None = None
    evidence: str | None = None
    observation_id: str = ""
    entity_type: str = "image"
    region: dict | None = None


@dataclass(frozen=True)
class DiscoveryResult:
    """One image's complete outcome. Records and proposals travel together -
    a partial match never suppresses the rest of the extraction."""
    image_id: str
    observation_id: str
    taxonomy_version: str
    matched: tuple[MatchedAttribute, ...] = ()
    proposals: tuple[StructureProposal, ...] = ()
    match_states: dict = field(default_factory=dict)
    unparsed: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "image_id": self.image_id,
            "observation_id": self.observation_id,
            "taxonomy_version": self.taxonomy_version,
            "matched": [asdict(m) for m in self.matched],
            "proposals": [p.to_dict() for p in self.proposals],
            "match_states": dict(self.match_states),
            "unparsed": list(self.unparsed),
        }
