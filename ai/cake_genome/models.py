"""
TBK Cake Genome - the per-image genome record.

WHAT "CAKE GENOME" MEANS HERE
  Per docs/00_Foundation/GLOSSARY.md, Cake Genome is the Bakery Domain's
  authored taxonomy CONTENT (ai/taxonomy/content/bakery_v1.json). This module
  produces the per-image *instance* of that vocabulary: what one photographed
  cake actually is, expressed in Cake Genome terms. It is not a second
  taxonomy and defines no attribute.

RELATIONSHIP TO Product Genome (ai.product_intelligence)
  Product Genome aggregates a whole SHOPIFY PRODUCT (ADR 0008). CakeGenome
  describes one IMAGE. They join through Image <-> Business Entity, the N:N
  edge Relationship_Model.md specifies and ECP-100 13 recorded as unbuilt.
  That join is NOT made here - no Shopify GID is touched by this package.

WHY SECTIONS ARE DERIVED FROM ATTRIBUTE GROUPS, NOT HARD-CODED
  The requested section list (identity, dimensions, frosting, colors, piping,
  decorations, flowers, fruits, topper, theme, ...) is close to, but not the
  same as, the 30 real Attribute Groups in bakery_v1.json. Hard-coding the
  requested names would create a second, drifting vocabulary - the exact
  failure mode ADR 0011 and the Glossary exist to prevent. Sections are keyed
  on real group names; SECTION_ALIASES documents the mapping for every
  requested name that differs, and requested sections with no backing group
  are reported in `unrepresented_sections` rather than silently omitted.
"""
from dataclasses import asdict, dataclass, field
from typing import Any

CAKE_GENOME_VERSION = "1.0"

# Requested section -> the real Attribute Group(s) in bakery_v1.json that back
# it. Empty tuple = no backing group exists today (surfaced, not hidden).
SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "identity":               ("Classification",),
    "dimensions":             ("Size", "Weight", "Servings", "Tier"),
    "frosting":               ("Cream", "Ganache", "Finish"),
    "colors":                 ("Colour",),
    "piping":                 ("Decoration",),
    "decorations":            ("Decoration",),
    "flowers":                ("Flowers",),
    "fruits":                 (),
    "topper":                 ("Topper",),
    "theme":                  ("Theme",),
    "occasion_intelligence":  ("Occasion",),
    "recipient_tags":         ("Recipient",),
    "relationship_tags":      (),
    "style_tags":             ("Style", "Texture"),
    "visual_search_tags":     (),
    "customer_search_phrases": (),
    "photography_genome":     (),
    "distinctive_features":   (),
    "design_identity_lock":   (),
    "multi_angle_reference":  (),
    "confidence":             (),
    "uncertain_attributes":   (),
}

# Sections assembled from pipeline state rather than from a taxonomy group.
DERIVED_SECTIONS = (
    "distinctive_features", "design_identity_lock", "visual_search_tags",
    "confidence", "uncertain_attributes", "multi_angle_reference",
    "photography_genome", "customer_search_phrases", "relationship_tags",
)


@dataclass(frozen=True)
class GenomeAttribute:
    """One resolved attribute on this image.

    Named for Entity_Model.md's "Genome Attribute", but NOTE the difference:
    that entity is defined as an Attribute that has PASSED the verification
    gate. Nothing here has - verification_status is "unverified" on every
    record this package produces. The gate is Build-006 + human review, and
    neither exists. Treated as a candidate genome, never as verified fact.
    """
    attribute: str
    value: Any
    normalized_value: Any
    value_state: str
    match_state: str
    confidence: float | None
    evidence: str | None
    data_type: str
    vocabulary: str | None = None
    term_id: str | None = None
    verification_status: str = "unverified"


@dataclass(frozen=True)
class DesignIdentityLock:
    """A machine-readable fingerprint of the observable design.

    Purpose (per the Phase 1 brief): let visual search, recommendation,
    multi-angle generation and future image-generation workflows recover the
    same design. Built ONLY from observed, taxonomy-resolved attributes -
    no invented surfaces, no inferred geometry, no hallucinated palette.
    """
    lock_id: str                       # deterministic hash of the locked facts
    image_id: str
    locked_attributes: dict            # attribute -> normalized value
    locked_relationships: tuple = ()
    palette: tuple = ()                # colour terms only, in observed order
    unresolved: tuple = ()             # observed but unmatched - part of the design, not yet nameable
    completeness: float = 0.0          # fraction of populated groups that resolved
    taxonomy_version: str = ""
    prompt_version: str | None = None
    caveats: tuple = ()


@dataclass(frozen=True)
class CakeGenome:
    genome_version: str
    image_id: str
    observation_id: str
    taxonomy_version: str
    schema_version: str
    provenance: dict
    sections: dict = field(default_factory=dict)
    design_identity_lock: DesignIdentityLock | None = None
    confidence: dict = field(default_factory=dict)
    uncertain_attributes: tuple = ()
    distinctive_features: tuple = ()
    visual_search_tags: tuple = ()
    unrepresented_sections: tuple = ()
    candidate_discoveries: tuple = ()
    diagnostics: dict = field(default_factory=dict)
    verification_status: str = "unverified"

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.design_identity_lock is not None:
            data["design_identity_lock"] = asdict(self.design_identity_lock)
        return data
