"""
Enterprise Attribute Language (EAL) v1 - the shared attribute envelope every
future build (EAR, EAD, Master Taxonomy, Knowledge Graph, ...) imports from.
Re-exports the public dataclass/Pydantic surface so downstream modules do
`from ai.eal import EALAttributeRecord` instead of reaching into submodules.
"""
from ai.eal.models import (
    EAL_VERSION,
    EALAttributeRecord,
    EALRelationshipRecord,
    ExternalId,
    HumanVerification,
    Provenance,
    compute_attribute_id,
    compute_relationship_id,
)
from ai.eal.models_pydantic import (
    ExternalIdModel,
    HumanVerificationModel,
    ProvenanceModel,
    EALAttributeRecordModel,
    EALRelationshipRecordModel,
)

__all__ = [
    "EAL_VERSION",
    "EALAttributeRecord",
    "EALRelationshipRecord",
    "ExternalId",
    "HumanVerification",
    "Provenance",
    "compute_attribute_id",
    "compute_relationship_id",
    "ExternalIdModel",
    "HumanVerificationModel",
    "ProvenanceModel",
    "EALAttributeRecordModel",
    "EALRelationshipRecordModel",
]
