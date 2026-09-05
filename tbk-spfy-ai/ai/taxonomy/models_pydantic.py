"""
Enterprise Master Taxonomy (Build-005) - Pydantic models.

WHY
  Runtime validation and JSON Schema generation for the four entities defined
  in ai.taxonomy.models. Field shapes kept in lockstep by hand (checked by
  ai/taxonomy/test_taxonomy.py), mirroring ai.ear's dataclass/Pydantic split.

USAGE
  python -m ai.taxonomy.test_taxonomy   # validates every example + regenerates schemas
"""
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from ai.eal.models_pydantic import ExternalIdModel  # reused, not redefined
from ai.taxonomy.ids import (
    ENTITY_TYPE_ID_PATTERNS,
    is_valid_attribute_id,
    is_valid_category_id,
    is_valid_group_id,
    is_valid_relationship_id,
    is_valid_term_id,
    is_valid_vocabulary_id,
)

TaxonomyEntityTypeLiteral = Literal["category", "attribute_group", "attribute", "vocabulary", "term"]

# Deliberately excludes SEARCH_ALIAS/SHOPIFY_TAG/ERP_REFERENCE/VISION_LABEL/SEO_KEYWORD/
# GOOGLE_MERCHANT_LABEL - see ai.taxonomy.models.RelationshipType's docstring.
RelationshipTypeLiteral = Literal[
    "IS_A", "PART_OF", "BELONGS_TO", "USES", "RELATED_TO",
    "PAIRS_WITH", "CONTRASTS_WITH", "COMPLEMENTS", "AVAILABLE_IN", "SUITABLE_FOR",
]

TAXONOMY_VERSION = "1.0"

# Same values as ai.eal.models.DataType - inlined for Pydantic per ai.ear.models_pydantic's own
# precedent (DataTypeLiteral), not imported, so this module has no import-time dependency loop risk.
DataTypeLiteral = Literal[
    "string", "integer", "float", "boolean", "enum",
    "date", "datetime", "array", "object", "vector", "reference",
]


class CategoryModel(BaseModel):
    category_id: str
    domain: str
    name: str
    parent_id: str | None = None
    attribute_group_ids: list[str] = Field(default_factory=list)
    status: Literal["active", "deprecated"] = "active"
    taxonomy_version: str = TAXONOMY_VERSION

    @model_validator(mode="after")
    def _category_id_must_be_valid(self):
        if not is_valid_category_id(self.category_id):
            raise ValueError(f"category_id {self.category_id!r} does not match ^TAX-CAT-\\d{{6}}$")
        return self

    @model_validator(mode="after")
    def _attribute_group_ids_must_be_valid(self):
        for gid in self.attribute_group_ids:
            if not is_valid_group_id(gid):
                raise ValueError(f"attribute_group_ids contains invalid group_id {gid!r}")
        return self


class AttributeGroupModel(BaseModel):
    group_id: str
    name: str
    tier: Literal["platform", "domain"]
    ear_namespace: str | None = None
    version: str = "v1"
    status: Literal["active", "deprecated"] = "active"
    taxonomy_version: str = TAXONOMY_VERSION

    @model_validator(mode="after")
    def _group_id_must_be_valid(self):
        if not is_valid_group_id(self.group_id):
            raise ValueError(f"group_id {self.group_id!r} does not match ^TAX-GRP-\\d{{6}}$")
        return self


class VocabularyModel(BaseModel):
    vocabulary_id: str
    name: str
    scope: Literal["global", "domain"]
    domain: str | None = None
    version: str = "v1"
    status: Literal["active", "deprecated"] = "active"
    taxonomy_version: str = TAXONOMY_VERSION

    @model_validator(mode="after")
    def _vocabulary_id_must_be_valid(self):
        if not is_valid_vocabulary_id(self.vocabulary_id):
            raise ValueError(f"vocabulary_id {self.vocabulary_id!r} does not match ^TAX-VOC-\\d{{6}}$")
        return self

    @model_validator(mode="after")
    def _domain_required_iff_scope_is_domain(self):
        needs_domain = self.scope == "domain"
        has_domain = self.domain is not None
        if needs_domain != has_domain:
            raise ValueError(
                f"scope={self.scope!r} and domain={self.domain!r} are inconsistent - domain is "
                f"required if and only if scope is 'domain'"
            )
        return self


class RelationshipModel(BaseModel):
    relationship_id: str
    subject_type: TaxonomyEntityTypeLiteral
    subject_id: str
    relationship_type: RelationshipTypeLiteral
    object_type: TaxonomyEntityTypeLiteral
    object_id: str
    status: Literal["active", "deprecated"] = "active"
    taxonomy_version: str = TAXONOMY_VERSION

    @model_validator(mode="after")
    def _relationship_id_must_be_valid(self):
        if not is_valid_relationship_id(self.relationship_id):
            raise ValueError(f"relationship_id {self.relationship_id!r} does not match ^TAX-REL-\\d{{6}}$")
        return self

    @model_validator(mode="after")
    def _subject_id_must_match_subject_type(self):
        pattern = ENTITY_TYPE_ID_PATTERNS[self.subject_type]
        if not pattern.match(self.subject_id):
            raise ValueError(f"subject_id {self.subject_id!r} does not match the ID format for subject_type {self.subject_type!r}")
        return self

    @model_validator(mode="after")
    def _object_id_must_match_object_type(self):
        pattern = ENTITY_TYPE_ID_PATTERNS[self.object_type]
        if not pattern.match(self.object_id):
            raise ValueError(f"object_id {self.object_id!r} does not match the ID format for object_type {self.object_type!r}")
        return self

    @model_validator(mode="after")
    def _no_self_loop(self):
        if self.subject_type == self.object_type and self.subject_id == self.object_id:
            raise ValueError(f"relationship {self.relationship_id!r} is a self-loop ({self.subject_id!r} -> itself)")
        return self


class TaxonomyAttributeModel(BaseModel):
    attribute_id: str
    group_id: str
    name: str
    data_type: DataTypeLiteral
    vocabulary_id: str | None = None
    ear_namespace: str | None = None
    status: Literal["active", "deprecated"] = "active"
    taxonomy_version: str = TAXONOMY_VERSION

    @model_validator(mode="after")
    def _attribute_id_must_be_valid(self):
        if not is_valid_attribute_id(self.attribute_id):
            raise ValueError(f"attribute_id {self.attribute_id!r} does not match ^TAX-ATTR-\\d{{6}}$")
        return self

    @model_validator(mode="after")
    def _group_id_must_be_valid(self):
        if not is_valid_group_id(self.group_id):
            raise ValueError(f"group_id {self.group_id!r} does not match ^TAX-GRP-\\d{{6}}$")
        return self

    @model_validator(mode="after")
    def _vocabulary_id_must_be_valid_if_set(self):
        if self.vocabulary_id is not None and not is_valid_vocabulary_id(self.vocabulary_id):
            raise ValueError(f"vocabulary_id {self.vocabulary_id!r} does not match ^TAX-VOC-\\d{{6}}$")
        return self

    @model_validator(mode="after")
    def _enum_datatype_requires_vocabulary(self):
        if self.data_type == "enum" and self.vocabulary_id is None:
            raise ValueError("data_type='enum' requires a vocabulary_id to resolve values against")
        return self


class TermModel(BaseModel):
    term_id: str
    vocabulary_id: str
    label: str
    synonyms: list[str] = Field(default_factory=list)
    parent_term_id: str | None = None
    status: Literal["active", "deprecated"] = "active"
    superseded_by: str | None = None
    external_ids: list[ExternalIdModel] = Field(default_factory=list)
    taxonomy_version: str = TAXONOMY_VERSION

    @model_validator(mode="after")
    def _term_id_must_be_valid(self):
        if not is_valid_term_id(self.term_id):
            raise ValueError(f"term_id {self.term_id!r} does not match ^TAX-TERM-\\d{{6}}$")
        return self

    @model_validator(mode="after")
    def _vocabulary_id_must_be_valid(self):
        if not is_valid_vocabulary_id(self.vocabulary_id):
            raise ValueError(f"vocabulary_id {self.vocabulary_id!r} does not match ^TAX-VOC-\\d{{6}}$")
        return self

    @model_validator(mode="after")
    def _superseded_by_required_iff_deprecated(self):
        is_deprecated = self.status == "deprecated"
        has_superseded_by = self.superseded_by is not None
        if is_deprecated != has_superseded_by:
            raise ValueError(
                f"status={self.status!r} and superseded_by={self.superseded_by!r} are "
                f"inconsistent - superseded_by is required if and only if status is 'deprecated' "
                f"(per docs/10_Taxonomy/Controlled_Vocabulary.md: 'where a replacement exists' - "
                f"a Term with no replacement yet stays 'active' until one exists)"
            )
        return self
