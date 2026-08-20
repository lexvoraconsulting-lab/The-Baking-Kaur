"""
Dynamic Visual Structure Discovery - matching an observation to the taxonomy.

WHY THIS WRAPS ai.attribute_intelligence.normalizer RATHER THAN MATCHING ITSELF
  That module already IS this repository's controlled-vocabulary matching rule
  (Term.label / Term.synonyms), extracted from
  ai.product_intelligence.resolvers.TaxonomyResolver for exactly this kind of
  reuse. Writing a third copy would be the duplicate ADR 0010 point 3 exists to
  prevent.

WHY CASE-FOLDING HAPPENS HERE AND NOT THERE
  normalize_against_vocabulary() is exact-match by design ("returns None, not a
  guess"). Real vision output is "White", "white", " White " for the same term,
  so an exact-match-only path would classify nearly every observation as
  unmatched and flood the proposal queue with duplicates of terms that already
  exist. Case/whitespace folding is INPUT CANONICALIZATION applied before the
  canonical rule runs - not a second, looser matching rule, and not a change to
  the frozen rule itself. Anything beyond folding (stemming, fuzzy distance,
  embeddings) would be a real second rule and is deliberately absent.

WHY ONLY status == "active" ENTRIES ARE MATCHED AGAINST
  Spec invariant 3: "proposed" entries are invisible to every consumer. Once
  ai.taxonomy gains a "proposed" EntryStatus (gap G1), this filter is what keeps
  an unapproved proposal from silently becoming matchable.
"""
import re

from ai.attribute_intelligence.normalizer import normalize_against_vocabulary
from ai.structure_discovery.models import MatchedAttribute, MatchState
from ai.taxonomy.catalog import TaxonomyCatalog


def _fold(text) -> str:
    """Case, whitespace AND separator folding: models write "Primary colour"
    where the taxonomy says "primary_colour" (observed live on qwen2.5vl:3b).
    Underscores, hyphens and spaces are treated as the same separator. Still
    input canonicalization - it changes how a value is SPELLED, never which
    values are considered equal in meaning."""
    if text is None:
        return ""
    folded = re.sub(r"[\s_\-]+", " ", str(text).strip().lower())
    return folded.strip()


class ObservationMatcher:
    """Resolves a RawObservation against ACTIVE taxonomy content only."""

    def __init__(self, catalog: TaxonomyCatalog):
        self._catalog = catalog
        self._groups = {
            _fold(g.name): g for g in catalog.attribute_groups if g.status == "active"
        }
        self._attrs_by_group = {}
        for group in catalog.attribute_groups:
            if group.status != "active":
                continue
            self._attrs_by_group[group.group_id] = {
                _fold(a.name): a
                for a in catalog.attributes_in_group(group.group_id)
                if a.status == "active"
            }
        self._vocab_names = {
            v.vocabulary_id: v.name for v in catalog.vocabularies if v.status == "active"
        }

    def match(self, observation) -> tuple[MatchState, MatchedAttribute | None, str | None]:
        """Returns (state, matched_attribute_or_None, reason_when_unmatched).

        The three outcomes map to spec section 6's branches: matched ->
        an EAL record; ambiguous/undetermined/not_applicable -> a record with
        no asserted value; unmatched -> a proposal.
        """
        group = self._groups.get(_fold(observation.group))
        if group is None:
            return "unmatched", None, (
                f"no active attribute group named {observation.group!r} in the taxonomy"
            )

        attribute = self._attrs_by_group.get(group.group_id, {}).get(_fold(observation.attribute))
        if attribute is None:
            return "unmatched", None, (
                f"group {group.name!r} exists but defines no attribute "
                f"{observation.attribute!r}"
            )

        # value_state drives the non-asserting outcomes before any value work.
        if observation.value_state == "null":
            return "not_applicable", self._build(observation, group, attribute,
                                                 "not_applicable", None, None), None
        if observation.value_state == "unknown":
            return "undetermined", self._build(observation, group, attribute,
                                               "undetermined", None, None), None

        # A free-value attribute has nothing to normalize against - the model's
        # value IS the value. Only enum attributes resolve to a Term.
        if not attribute.vocabulary_id:
            return "matched", self._build(observation, group, attribute,
                                          "matched", observation.value, None), None

        raw = _fold(observation.value)
        term = self._match_term(attribute.vocabulary_id, raw)
        if term is None:
            vocab_name = self._vocab_names.get(attribute.vocabulary_id, attribute.vocabulary_id)
            return "unmatched", None, (
                f"{observation.value!r} is not a term or synonym in the "
                f"{vocab_name!r} vocabulary used by {attribute.name!r}"
            )
        state: MatchState = "matched" if _fold(term.label) == raw else "matched_synonym"
        return state, self._build(observation, group, attribute, state, observation.value, term), None

    def _match_term(self, vocabulary_id: str, folded_value: str):
        """Fold both sides, then defer to the canonical exact rule."""
        if not folded_value:
            return None
        for term in self._catalog.terms_in_vocabulary(vocabulary_id):
            if term.status != "active":
                continue
            if _fold(term.label) == folded_value or folded_value in {
                _fold(s) for s in term.synonyms
            }:
                # Re-run the canonical rule on the real label so this path can
                # never resolve something normalize_against_vocabulary would not.
                return normalize_against_vocabulary(
                    self._catalog, vocabulary_id, term.label,
                ) or term
        return None

    def _build(self, observation, group, attribute, state, value, term) -> MatchedAttribute:
        return MatchedAttribute(
            group=group.name,
            group_id=group.group_id,
            attribute=attribute.name,
            attribute_id=attribute.attribute_id,
            value=value,
            value_state=observation.value_state,
            match_state=state,
            data_type=attribute.data_type,
            vocabulary=self._vocab_names.get(attribute.vocabulary_id) if attribute.vocabulary_id else None,
            term_id=term.term_id if term else None,
            normalized_value=term.label if term else value,
            confidence=observation.confidence,
            evidence=observation.evidence,
            entity_type=observation.entity_type,
            region=observation.region,
        )
