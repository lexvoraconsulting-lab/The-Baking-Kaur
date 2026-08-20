"""
TBK Cake Genome - the per-image genome instance.

Assembles a DiscoveryResult (ai.structure_discovery) into a CakeGenome:
sections keyed on real Attribute Groups, a Design Identity Lock over resolved
attributes only, confidence and provenance carried through, and every
unmatched observation preserved as a candidate discovery.

Owns no data. Persists nothing. Verifies nothing.
"""
from ai.cake_genome.builder import build_cake_genome, build_design_identity_lock
from ai.cake_genome.models import (
    CAKE_GENOME_VERSION,
    DERIVED_SECTIONS,
    SECTION_ALIASES,
    CakeGenome,
    DesignIdentityLock,
    GenomeAttribute,
)
from ai.cake_genome.validation import ValidationReport, validate_genome

__all__ = [
    "CAKE_GENOME_VERSION", "SECTION_ALIASES", "DERIVED_SECTIONS",
    "CakeGenome", "DesignIdentityLock", "GenomeAttribute",
    "build_cake_genome", "build_design_identity_lock",
    "validate_genome", "ValidationReport",
]
