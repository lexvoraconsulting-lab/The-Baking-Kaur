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
    is_valid_category_id,
    is_valid_group_id,
    is_valid_term_id,
    is_valid_vocabulary_id,
)

TAXONOMY_VERSION = "1.0"


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
