"""
Enterprise Attribute Intelligence Engine v1 (Build-303) - the multi-source
attribute reconciliation layer under ai.product_intelligence and
ai.knowledge: normalizes, validates, infers, scores, resolves, and tracks
the history of every product attribute, across Shopify/Vision/Manual/
Merchant/SEO/Knowledge-Graph/Genome sources, without owning an attribute
catalog of its own. See docs/ATTRIBUTE_ENGINE.md.
"""
from ai.attribute_intelligence.confidence import (
    DEFAULT_SOURCE_TRUST, AttributeConfidenceEngine, RankedObservation,
)
from ai.attribute_intelligence.conflicts import AttributeConflictResolver
from ai.attribute_intelligence.exporter import export_profile
from ai.attribute_intelligence.extensions import (
    GenomeAttributeSourcePort, MerchantAttributeSourcePort, NotConnectedGenomeAttributeSource,
    NotConnectedMerchantAttributeSource,
)
from ai.attribute_intelligence.history import AttributeHistoryLog
from ai.attribute_intelligence.ids import compute_observation_id, compute_resolution_id
from ai.attribute_intelligence.inference import (
    AttributeInferenceEngine, InferenceRule, TaxonomyRelationshipInferenceRule,
)
from ai.attribute_intelligence.integration import observations_from_eal, observations_from_tags
from ai.attribute_intelligence.models import (
    ATTRIBUTE_INTELLIGENCE_VERSION, AttributeHistoryEntry, AttributeObservation, ConflictRecord,
    ResolvedAttribute, SubjectAttributeProfile, ValidationIssue,
)
from ai.attribute_intelligence.normalizer import (
    AttributeNormalizer, normalize_against_any_vocabulary, normalize_against_vocabulary,
)
from ai.attribute_intelligence.observability import (
    AttributeIntelligenceObserver, CoverageReport, LoggingObserver, NullObserver,
    compute_coverage_report, compute_drift,
)
from ai.attribute_intelligence.search import AttributeSearchService
from ai.attribute_intelligence.service import AttributeIntelligenceService
from ai.attribute_intelligence.validator import AttributeValidator

__all__ = [
    "ATTRIBUTE_INTELLIGENCE_VERSION",
    "DEFAULT_SOURCE_TRUST",
    "AttributeConfidenceEngine",
    "AttributeConflictResolver",
    "AttributeHistoryEntry",
    "AttributeHistoryLog",
    "AttributeInferenceEngine",
    "AttributeIntelligenceObserver",
    "AttributeIntelligenceService",
    "AttributeNormalizer",
    "AttributeObservation",
    "AttributeSearchService",
    "AttributeValidator",
    "ConflictRecord",
    "CoverageReport",
    "GenomeAttributeSourcePort",
    "InferenceRule",
    "LoggingObserver",
    "MerchantAttributeSourcePort",
    "NotConnectedGenomeAttributeSource",
    "NotConnectedMerchantAttributeSource",
    "NullObserver",
    "RankedObservation",
    "ResolvedAttribute",
    "SubjectAttributeProfile",
    "TaxonomyRelationshipInferenceRule",
    "ValidationIssue",
    "compute_coverage_report",
    "compute_drift",
    "compute_observation_id",
    "compute_resolution_id",
    "export_profile",
    "normalize_against_any_vocabulary",
    "normalize_against_vocabulary",
    "observations_from_eal",
    "observations_from_tags",
]
