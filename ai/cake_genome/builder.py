"""
TBK Cake Genome - assembly and the Design Identity Lock.

WHY THE GENOME OWNS NO DATA
  Same discipline as ai.product_intelligence (ADR 0008): every value here is
  resolved from a DiscoveryResult produced upstream, assembled in memory, and
  never independently persisted by this package. VIG-003 Principle 2 - no
  second, competing system of record.

WHY THE LOCK HASHES ONLY RESOLVED ATTRIBUTES
  The brief: "Do not invent hidden surfaces." A design fingerprint that
  included guessed geometry or an inferred palette would produce confident
  matches for cakes that do not look alike. Only taxonomy-resolved,
  value_state == "present" facts enter the hash; everything observed but
  unresolved is carried alongside in `unresolved`, visible and unhashed.
"""
import hashlib
import json
from dataclasses import asdict

from ai.cake_genome.models import (
    CAKE_GENOME_VERSION,
    DERIVED_SECTIONS,
    SECTION_ALIASES,
    CakeGenome,
    DesignIdentityLock,
    GenomeAttribute,
)

_COLOUR_GROUP = "Colour"
# Below this, an attribute is reported as uncertain rather than trusted.
# ponytail: one global threshold. Validation.md specifies PER-GROUP thresholds;
# that belongs in Build-006 (the Validation Engine), which owns thresholding.
# Upgrade path: read per-group values from EAD confidence_expectations.
UNCERTAIN_BELOW = 0.60


def _to_genome_attribute(matched) -> GenomeAttribute:
    return GenomeAttribute(
        attribute=matched.attribute,
        value=matched.value,
        normalized_value=matched.normalized_value,
        value_state=matched.value_state,
        match_state=matched.match_state,
        confidence=matched.confidence,
        evidence=matched.evidence,
        data_type=matched.data_type,
        vocabulary=matched.vocabulary,
        term_id=matched.term_id,
    )


def _build_sections(discovery) -> tuple[dict, tuple]:
    """Group resolved attributes under the requested section names, via the
    documented SECTION_ALIASES mapping onto real Attribute Groups."""
    by_group: dict[str, list] = {}
    for matched in discovery.matched:
        by_group.setdefault(matched.group, []).append(_to_genome_attribute(matched))

    sections, unrepresented = {}, []
    aliased_groups = {g for groups in SECTION_ALIASES.values() for g in groups}
    for section, groups in SECTION_ALIASES.items():
        if section in DERIVED_SECTIONS:
            continue
        if not groups:
            unrepresented.append({
                "section": section,
                "reason": "no Attribute Group in bakery_v1.json backs this section",
            })
            continue
        attributes = [a for g in groups for a in by_group.get(g, [])]
        if attributes:
            sections[section] = {
                "backed_by_groups": list(groups),
                "attributes": [a.__dict__ for a in attributes],
            }
        else:
            unrepresented.append({
                "section": section,
                "reason": f"groups {list(groups)} exist but produced no observation for this image",
            })

    # A matched attribute whose Attribute Group no section alias covers would
    # otherwise vanish from the genome entirely - silent loss, and exactly what
    # this pipeline exists to prevent. Observed live: Writing.visible_text
    # resolved correctly but had no home. Surfaced, not dropped.
    orphaned = {
        group: attrs for group, attrs in by_group.items() if group not in aliased_groups
    }
    if orphaned:
        sections["other_observed_groups"] = {
            "backed_by_groups": sorted(orphaned),
            "note": "resolved attributes whose Attribute Group no section alias maps; "
                    "SECTION_ALIASES needs a mapping for these",
            "attributes": [a.__dict__ for attrs in orphaned.values() for a in attrs],
        }
    return sections, tuple(unrepresented)


def _palette(discovery) -> tuple:
    return tuple(
        m.normalized_value for m in discovery.matched
        if m.group == _COLOUR_GROUP and m.value_state == "present" and m.normalized_value
    )


def find_value_conflicts(discovery) -> dict:
    """Two different values for the SAME attribute on the same image.

    Validation.md's consistency dimension: "A contradiction blocks automatic
    promotion and routes to Human Review rather than silently picking one
    value." Observed live on qwen2.5vl:3b, which reported visible_text twice
    ("HAPPY BIRTHDAY" and "We love you, Dad") - both real, both on the cake.
    Keying a fingerprint dict on attribute name would have kept whichever came
    last, which is silent data loss dressed up as a clean result.
    """
    seen: dict[str, list] = {}
    for m in discovery.matched:
        if m.value_state == "present" and m.normalized_value not in (None, ""):
            seen.setdefault(m.attribute, []).append(m.normalized_value)
    return {a: v for a, v in seen.items() if len({str(x) for x in v}) > 1}


def build_design_identity_lock(discovery, *, prompt_version=None) -> DesignIdentityLock:
    """Deterministic fingerprint of the observable design."""
    conflicts = find_value_conflicts(discovery)
    # A conflicted attribute is EXCLUDED from the fingerprint rather than
    # resolved by guessing. It stays visible in `unresolved` and in the
    # genome's uncertain_attributes, awaiting review.
    locked = {
        m.attribute: m.normalized_value
        for m in discovery.matched
        if m.value_state == "present" and m.normalized_value not in (None, "")
        and m.attribute not in conflicts
    }
    relationships = tuple(sorted(
        f"{r}" for r in ()  # relationships are extracted but not yet taxonomy-resolved; see caveats
    ))
    populated = [m for m in discovery.matched if m.value_state == "present"]
    resolved = [m for m in populated if m.match_state in ("matched", "matched_synonym")]
    completeness = round(len(resolved) / len(populated), 4) if populated else 0.0

    payload = json.dumps(
        {"attributes": dict(sorted(locked.items())), "relationships": list(relationships)},
        sort_keys=True, ensure_ascii=False,
    )
    caveats = []
    if conflicts:
        caveats.append(
            "excluded from the fingerprint as contradictory: "
            + "; ".join(f"{a} = {sorted({str(x) for x in v})}" for a, v in conflicts.items()),
        )
    if not locked:
        caveats.append("no attribute resolved - this lock cannot identify a design")
    if discovery.proposals:
        caveats.append(
            f"{len(discovery.proposals)} observed feature(s) are not yet nameable in the taxonomy "
            "and are therefore NOT part of the fingerprint",
        )
    caveats.append(
        "relationships are extracted but not taxonomy-resolved in Phase 1; they are excluded "
        "from the hash rather than hashed unvalidated",
    )

    return DesignIdentityLock(
        lock_id="LOCK-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20],
        image_id=discovery.image_id,
        locked_attributes=dict(sorted(locked.items())),
        locked_relationships=relationships,
        palette=_palette(discovery),
        unresolved=tuple(p.label for p in discovery.proposals)
                   + tuple(f"{a} (conflicting values)" for a in conflicts),
        completeness=completeness,
        taxonomy_version=discovery.taxonomy_version,
        prompt_version=prompt_version,
        caveats=tuple(caveats),
    )


def build_cake_genome(discovery, extraction) -> CakeGenome:
    """DiscoveryResult + ExtractionResult -> CakeGenome. Pure assembly."""
    sections, unrepresented = _build_sections(discovery)

    present = [m for m in discovery.matched if m.value_state == "present"]
    scored = [m.confidence for m in present if m.confidence is not None]
    confidence = {
        "mean_attribute_confidence": round(sum(scored) / len(scored), 4) if scored else None,
        "attributes_present": len(present),
        "attributes_scored": len(scored),
        "attributes_unscored": len(present) - len(scored),
        "resolution_rate": round(
            len([m for m in present if m.match_state in ("matched", "matched_synonym")])
            / len(present), 4,
        ) if present else 0.0,
        "proposals_raised": len(discovery.proposals),
    }

    conflicts = find_value_conflicts(discovery)
    uncertain = tuple(
        {
            "attribute": attribute,
            "reason": "conflicting values reported for the same attribute on this image; "
                      "Validation.md routes contradictions to review, never to a guess",
            "values": sorted({str(v) for v in values}),
            "confidence": None,
            "evidence": None,
        }
        for attribute, values in conflicts.items()
    ) + tuple(
        {
            "attribute": m.attribute,
            "reason": (
                "value_state is 'unknown' - applies but not determined"
                if m.value_state == "unknown" else
                f"confidence {m.confidence} below {UNCERTAIN_BELOW}"
            ),
            "confidence": m.confidence,
            "evidence": m.evidence,
        }
        for m in discovery.matched
        if m.value_state == "unknown"
        or (m.confidence is not None and m.confidence < UNCERTAIN_BELOW)
    )

    # A distinctive feature is something the taxonomy could NOT name - by
    # definition the parts of this cake that make it unlike the vocabulary's
    # idea of a cake. Proposals are exactly that set.
    distinctive = tuple(
        {"feature": p.label, "why": p.why_unmatched, "confidence": p.confidence,
         "proposal_id": p.proposal_id, "status": p.status}
        for p in discovery.proposals
    )

    search_tags = tuple(sorted({
        str(m.normalized_value).lower()
        for m in present if m.normalized_value not in (None, "")
    }))

    return CakeGenome(
        genome_version=CAKE_GENOME_VERSION,
        image_id=discovery.image_id,
        observation_id=discovery.observation_id,
        taxonomy_version=discovery.taxonomy_version,
        schema_version=extraction.schema_version,
        provenance={
            "provider": extraction.provider,
            "model": extraction.model,
            "model_version": extraction.model_version,
            "prompt_version": extraction.prompt_version,
            "schema_version": extraction.schema_version,
            "taxonomy_version": extraction.taxonomy_version,
            "extracted_at": extraction.extracted_at,
            "extraction_version": extraction.extraction_version,
            "parse_ok": extraction.parse_ok,
        },
        sections=sections,
        design_identity_lock=build_design_identity_lock(
            discovery, prompt_version=extraction.prompt_version,
        ),
        confidence=confidence,
        uncertain_attributes=uncertain,
        distinctive_features=distinctive,
        visual_search_tags=search_tags,
        unrepresented_sections=unrepresented,
        candidate_discoveries=tuple(p.to_dict() for p in discovery.proposals),
        # Leaked output is preserved here and NOWHERE else - not in sections,
        # not in the lock, not in candidate_discoveries. Diagnostics only.
        diagnostics={
            "prompt_leakage": [asdict(r) for r in extraction.leaked],
            "prompt_leakage_count": len(extraction.leaked),
            "unparsed_count": len(extraction.unparsed),
            "parse_ok": extraction.parse_ok,
        },
        verification_status="unverified",
    )
