"""
Self-check: python -m ai.structure_discovery.test_structure_discovery

Asserts the invariants docs/80_Dynamic_Structure_Discovery/SPECIFICATION.md
section 9 states. No framework, no fixtures - the pattern ai.eal.test_eal,
ai.ear.test_ear and ai.taxonomy.test_taxonomy already use.
"""
from ai.structure_discovery import ObservationMatcher, build_discovery_result
from ai.vision.python.extraction import RawObservation, parse_extraction
from ai.vision.python.taxonomy_digest import load_canonical_catalog

CATALOG = load_canonical_catalog()
MATCHER = ObservationMatcher(CATALOG)


def _extract(payload: str):
    return parse_extraction(
        payload, image_id="TBK-0000000000000001", taxonomy_version="1.0",
        schema_version="v1", prompt_version="test", provider="test", model="test",
        extracted_at="2026-08-20T00:00:00Z",
    )


def test_exact_and_synonym_match():
    state, attr, _ = MATCHER.match(RawObservation("Colour", "primary_colour", "White", "present", 0.9))
    assert state == "matched" and attr.normalized_value == "White", state
    # Case folding is input canonicalization, not a looser rule.
    state, attr, _ = MATCHER.match(RawObservation("colour", "PRIMARY_COLOUR", "  white ", "present", 0.9))
    assert state == "matched" and attr.normalized_value == "White", state
    state, attr, _ = MATCHER.match(RawObservation("Colour", "primary_colour", "Blush Gold", "present", 0.7))
    assert state == "matched_synonym" and attr.normalized_value == "Rose Gold", attr.normalized_value


def test_null_and_unknown_are_distinct():
    state, attr, _ = MATCHER.match(RawObservation("Writing", "visible_text", None, "null"))
    assert state == "not_applicable" and attr.value_state == "null", state
    state, attr, _ = MATCHER.match(RawObservation("Tier", "tier_count", None, "unknown"))
    assert state == "undetermined" and attr.value_state == "unknown", state


def test_unknown_group_and_unknown_value_both_unmatched():
    state, attr, reason = MATCHER.match(RawObservation("Sparkle", "glitter", "high", "present", 0.5))
    assert state == "unmatched" and attr is None and "Sparkle" in reason, reason
    state, attr, reason = MATCHER.match(RawObservation("Colour", "primary_colour", "ultraviolet", "present", 0.5))
    assert state == "unmatched" and attr is None and "vocabulary" in reason, reason


def test_no_observation_is_ever_discarded():
    """Spec invariant 4: every observation lands in exactly one of two places."""
    result = _extract(
        '{"observations":['
        '{"group":"Colour","attribute":"primary_colour","value":"White","value_state":"present","confidence":0.9},'
        '{"group":"Nonexistent","attribute":"whatever","value":"x","value_state":"present","confidence":0.5}],'
        '"unmatched":[{"observed":"a thing","why_unmatched":"nothing fits","suggested_kind":"term","suggested_label":"Thing"}]}'
    )
    discovery = build_discovery_result(result, MATCHER)
    assert len(discovery.matched) + len(discovery.proposals) == 3, (
        len(discovery.matched), len(discovery.proposals))


def test_proposals_never_advance_past_observed():
    """Spec invariant 1: no proposal is ever auto-promoted, at any confidence."""
    result = _extract(
        '{"observations":[],"unmatched":[{"observed":"x","why_unmatched":"y",'
        '"suggested_kind":"term","suggested_label":"X","confidence":1.0}]}'
    )
    discovery = build_discovery_result(result, MATCHER)
    assert all(p.status == "observed" and p.promoted_to is None for p in discovery.proposals)


def test_frozen_literal_kinds_require_a_gate():
    """Spec section 5.3: widening EntityType/RelationshipType needs an ADR."""
    result = _extract(
        '{"observations":[],"unmatched":[{"observed":"a new kind of thing","why_unmatched":"n/a",'
        '"suggested_kind":"entity_type","suggested_label":"Assembly"}]}'
    )
    proposal = build_discovery_result(result, MATCHER).proposals[0]
    assert proposal.requires_gate is True, proposal


def test_dedupe_accumulates_evidence():
    result = _extract(
        '{"observations":[],"unmatched":['
        '{"observed":"lace collar A","why_unmatched":"a","suggested_kind":"term","suggested_label":"Lace Collar"},'
        '{"observed":"lace collar B","why_unmatched":"b","suggested_kind":"term","suggested_label":"Lace Collar"}]}'
    )
    proposals = build_discovery_result(result, MATCHER).proposals
    assert len(proposals) == 1 and proposals[0].occurrence_count == 2, proposals
    assert len(proposals[0].evidence) == 2, "evidence must accumulate, never replace"


def test_parse_failure_is_data_not_an_exception():
    result = _extract("I'm sorry, I cannot analyse this image.")
    assert result.parse_ok is False and result.unparsed, result
    assert build_discovery_result(result, MATCHER).matched == ()


def test_confidence_dropped_when_value_absent():
    """Confidence_Standard.md: nothing to be confident about."""
    result = _extract(
        '{"observations":[{"group":"Tier","attribute":"tier_count","value":null,'
        '"value_state":"unknown","confidence":0.9}],"unmatched":[]}'
    )
    assert result.observations[0].confidence is None


def test_proposed_entries_are_invisible_to_matching():
    """Spec invariant 3. ai.taxonomy has no 'proposed' status yet (gap G1), so
    this asserts the filter that will enforce it: only active is matchable."""
    inactive = [t for t in CATALOG.terms if t.status != "active"]
    for term in inactive:
        state, _, _ = MATCHER.match(
            RawObservation("Colour", "primary_colour", term.label, "present", 0.9))
        assert state == "unmatched", f"non-active term {term.label} was matched"


def demo():
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {name}")
    print("ai.structure_discovery self-check passed")


if __name__ == "__main__":
    demo()
