"""
Enterprise Attribute Language (EAL) v1 - plain dataclass models.

WHY
  Human/IDE-facing shape of the EAL envelope, independent of any validation
  library. ai.eal.models_pydantic mirrors these fields for runtime validation
  and JSON Schema generation - this module has no third-party dependency.
  See docs/20_Attribute_Language/EAL_SPECIFICATION.md.
"""
import hashlib
from dataclasses import dataclass, field
from typing import Any, Literal

EAL_VERSION = "1.0"

EntityType = Literal["image", "region", "object"]
ValueState = Literal["present", "null", "unknown"]
DataType = Literal[
    "string", "integer", "float", "boolean", "enum",
    "date", "datetime", "array", "object", "vector", "reference",
]
VerificationStatus = Literal[
    "unverified", "pending_review", "verified", "rejected", "corrected",
]


def compute_attribute_id(canonical_path: str) -> str:
    """Opaque, deterministic identifier derived from a canonical path (same
    content-hash pattern as ai.vision.python.pipeline.compute_image_id) -
    renaming a path later never breaks a stored reference to this ID."""
    return "EAL-" + hashlib.sha256(canonical_path.encode("utf-8")).hexdigest()[:16]


def compute_relationship_id(source_id: str, relationship_type: str, target_id: str) -> str:
    key = f"{source_id}|{relationship_type}|{target_id}"
    return "EAL-REL-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class ExternalId:
    system: str
    id_type: str
    value: str


@dataclass(frozen=True)
class Provenance:
    provider: str
    model: str
    schema_version: str
    taxonomy_version: str
    extracted_at: str
    model_version: str | None = None
    prompt_version: str | None = None


@dataclass(frozen=True)
class HumanVerification:
    status: VerificationStatus = "unverified"
    reviewer_id: str | None = None
    reviewed_at: str | None = None
    original_value: Any = None


@dataclass(frozen=True)
class EALAttributeRecord:
    canonical_path: str
    namespace: str
    group: str
    entity_id: str
    entity_type: EntityType
    value: Any
    value_state: ValueState
    data_type: DataType
    provenance: Provenance
    attribute_id: str = ""
    eal_version: str = EAL_VERSION
    unit: str | None = None
    vocabulary: str | None = None
    confidence: float | None = None
    human_verification: HumanVerification = field(default_factory=HumanVerification)
    external_ids: list[ExternalId] = field(default_factory=list)

    def __post_init__(self):
        if not self.attribute_id:
            object.__setattr__(self, "attribute_id", compute_attribute_id(self.canonical_path))


@dataclass(frozen=True)
class EALRelationshipRecord:
    type: str
    source_id: str
    target_id: str
    provenance: Provenance
    relationship_id: str = ""
    eal_version: str = EAL_VERSION
    confidence: float | None = None

    def __post_init__(self):
        if not self.relationship_id:
            object.__setattr__(
                self,
                "relationship_id",
                compute_relationship_id(self.source_id, self.type, self.target_id),
            )
