"""
Dynamic Visual Structure Discovery - turning unmatched observations into
evidence-backed proposals.

WHY A PROPOSAL IS NEVER WRITTEN TO ai.taxonomy OR ai.ear HERE
  Spec invariant 1: no proposal is ever auto-promoted, at any confidence, at
  any occurrence count. This module produces records; promotion is a separate,
  human-gated step (spec section 4.2 APPROVE -> REGISTER) that does not exist
  yet and is deliberately not stubbed in - a stub that writes would be the one
  bug this whole design exists to prevent.

WHY AN UNMATCHED *OBSERVATION* ALSO BECOMES A PROPOSAL
  matcher.match() returns "unmatched" for two different situations: the model
  named a group/attribute the taxonomy does not have, and the model gave a
  value no Term covers. Both are taxonomy gaps and both must survive - spec
  invariant 4, "an observation is never forced into a wrong field".
"""
from dataclasses import replace

from ai.eal.models import Provenance
from ai.structure_discovery.ids import compute_observation_id, slugify
from ai.structure_discovery.models import (
    DiscoveryResult,
    Evidence,
    StructureProposal,
)

# What kind of structure an unmatched observation implies, when the model did
# not say. Conservative on purpose: proposing a whole new attribute_group is a
# much larger claim than proposing one term, so an unknown case defaults to the
# smaller one and lets a reviewer widen it.
_DEFAULT_KIND = "term"
_VALID_KINDS = {
    "attribute", "term", "vocabulary", "attribute_group",
    "category", "relationship", "relationship_type", "entity_type",
}


def _provenance_from(result) -> Provenance:
    """Reuse ai.eal.models.Provenance verbatim. Not a second provenance shape."""
    return Provenance(
        provider=result.provider or "unknown",
        model=result.model or "unknown",
        schema_version=result.schema_version,
        taxonomy_version=result.taxonomy_version,
        extracted_at=result.extracted_at or "",
        model_version=result.model_version,
        prompt_version=result.prompt_version,
    )


def propose_from_unmatched(unmatched, *, result, observation_id: str) -> StructureProposal:
    """One UnmatchedObservation (the model's own second channel) -> proposal."""
    kind = unmatched.suggested_kind if unmatched.suggested_kind in _VALID_KINDS else _DEFAULT_KIND
    label = unmatched.suggested_label or unmatched.observed
    return StructureProposal(
        proposal_kind=kind,
        canonical_name=slugify(label),
        label=label,
        confidence=unmatched.confidence,
        why_unmatched=unmatched.why_unmatched,
        parent_reference=unmatched.closest_attribute or unmatched.closest_group,
        taxonomy_version=result.taxonomy_version,
        first_seen=result.extracted_at or "",
        last_seen=result.extracted_at or "",
        evidence=(Evidence(
            image_id=result.image_id,
            observation_id=observation_id,
            raw_fragment=unmatched.observed,
            provenance=_provenance_from(result),
            region=unmatched.region,
        ),),
    )


def _propose_from_failed_match(observation, reason: str, *, result, observation_id: str) -> StructureProposal:
    """An observation the model believed was in-taxonomy but which does not
    resolve. The model's own words are the evidence; `reason` is the matcher's."""
    is_value_gap = "vocabulary" in reason
    label = str(observation.value) if is_value_gap else observation.attribute
    return StructureProposal(
        proposal_kind="term" if is_value_gap else "attribute",
        canonical_name=slugify(label),
        label=label,
        confidence=observation.confidence,
        why_unmatched=reason,
        parent_reference=observation.attribute if is_value_gap else observation.group,
        suggested_data_type=observation.data_type,
        suggested_vocabulary=observation.vocabulary,
        taxonomy_version=result.taxonomy_version,
        first_seen=result.extracted_at or "",
        last_seen=result.extracted_at or "",
        evidence=(Evidence(
            image_id=result.image_id,
            observation_id=observation_id,
            raw_fragment=observation.evidence or f"{observation.attribute}={observation.value!r}",
            provenance=_provenance_from(result),
            region=observation.region,
        ),),
    )


def _merge(existing: StructureProposal, incoming: StructureProposal) -> StructureProposal:
    """Dedupe by (kind, canonical_name), mirroring tbk_unmapped_attributes'
    occurrence_count semantics. Evidence accumulates; nothing is replaced."""
    return StructureProposal(
        proposal_kind=existing.proposal_kind,
        canonical_name=existing.canonical_name,
        label=existing.label,
        status=existing.status,
        parent_reference=existing.parent_reference or incoming.parent_reference,
        suggested_data_type=existing.suggested_data_type or incoming.suggested_data_type,
        suggested_vocabulary=existing.suggested_vocabulary or incoming.suggested_vocabulary,
        confidence=max(
            [c for c in (existing.confidence, incoming.confidence) if c is not None] or [None],
        ) if (existing.confidence is not None or incoming.confidence is not None) else None,
        occurrence_count=existing.occurrence_count + incoming.occurrence_count,
        first_seen=existing.first_seen or incoming.first_seen,
        last_seen=incoming.last_seen or existing.last_seen,
        evidence=existing.evidence + incoming.evidence,
        why_unmatched=existing.why_unmatched or incoming.why_unmatched,
        taxonomy_version=existing.taxonomy_version,
    )


def _flag_existing_duplicates(proposals, catalog) -> list:
    """Mark a proposal whose name already exists in the ACTIVE taxonomy.

    A weak model reliably proposes things that already exist - observed live:
    qwen2.5vl:3b proposed a new attribute_group "Theme" while the Theme group
    was in the digest it had been given. The proposal is still recorded (never
    discarded - spec invariant 2), but flagged so a reviewer sees "this is
    probably already Theme" instead of triaging it from scratch.

    This does NOT auto-merge. Setting status to "merged" is a review decision
    (spec section 8), not something matching may do on its own.
    """
    from ai.structure_discovery.matcher import _fold

    existing = {}
    for group in catalog.attribute_groups:
        if group.status == "active":
            existing[_fold(group.name)] = group.group_id
    for attribute in catalog.attributes:
        if attribute.status == "active":
            existing.setdefault(_fold(attribute.name), attribute.attribute_id)
    for term in catalog.terms:
        if term.status == "active":
            existing.setdefault(_fold(term.label), term.term_id)
            for synonym in term.synonyms:
                existing.setdefault(_fold(synonym), term.term_id)

    flagged = []
    for proposal in proposals:
        match = existing.get(_fold(proposal.label))
        flagged.append(
            replace(proposal, likely_duplicate_of=match) if match else proposal
        )
    return flagged


def build_discovery_result(result, matcher, catalog=None) -> DiscoveryResult:
    """The whole matching + proposing pass for one extraction.

    Every observation lands in exactly one of two places and none is dropped -
    this is the invariant the function exists to guarantee.
    """
    observation_id = compute_observation_id(result.image_id, result.extracted_at or "")
    matched, match_states = [], {}
    proposals: dict[tuple[str, str], StructureProposal] = {}

    def add(proposal: StructureProposal) -> None:
        key = (proposal.proposal_kind, proposal.canonical_name)
        proposals[key] = _merge(proposals[key], proposal) if key in proposals else proposal

    for observation in result.observations:
        state, attribute, reason = matcher.match(observation)
        match_states[f"{observation.group}.{observation.attribute}"] = state
        if attribute is not None:
            matched.append(attribute)
        else:
            add(_propose_from_failed_match(
                observation, reason or "unmatched", result=result, observation_id=observation_id,
            ))

    for unmatched in result.unmatched:
        add(propose_from_unmatched(unmatched, result=result, observation_id=observation_id))

    final = list(proposals.values())
    if catalog is not None:
        final = _flag_existing_duplicates(final, catalog)

    return DiscoveryResult(
        image_id=result.image_id,
        observation_id=observation_id,
        taxonomy_version=result.taxonomy_version,
        matched=tuple(matched),
        proposals=tuple(final),
        match_states=match_states,
        unparsed=result.unparsed,
    )
