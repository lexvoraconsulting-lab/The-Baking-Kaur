"""
Enterprise Attribute Intelligence Engine (Build-303) - Attribute Exporter.

WHY A PLAIN DICT, NOT A SHOPIFY/ERP WRITE
  Writing a resolved value out to a downstream system is
  ai.attribute_distribution's job (DistributionRecord, the Shopify/ERP
  adapters) - reimplementing that here would be exactly the "duplicated
  service" this sprint's own principles forbid. export_profile() produces a
  plain, JSON-safe snapshot of what THIS package resolved; a caller wiring
  it into ai.attribute_distribution would pass registry_reference + value
  (already present in DistributionRecord's own shape) into that package's
  existing resolve_distribution(), not through a new write path here.
"""
from typing import Any

from ai.attribute_intelligence.models import SubjectAttributeProfile


def export_profile(profile: SubjectAttributeProfile) -> dict[str, Any]:
    return {
        "subject_id": profile.subject_id,
        "resolved_at": profile.resolved_at,
        "attributes": {
            registry_reference: {
                "value": resolved.value,
                "confidence": resolved.confidence,
                "source": resolved.source,
                "resolution_method": resolved.resolution_method,
                "has_conflict": resolved.conflict is not None,
            }
            for registry_reference, resolved in profile.attributes.items()
        },
        "validation_issue_count": len(profile.validation_issues),
        "conflict_count": len(profile.conflicts),
    }
