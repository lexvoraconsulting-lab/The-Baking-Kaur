"""
Enterprise Master Taxonomy (Build-005) - plain dataclass models.

WHY
  Human/IDE-facing shape, independent of any validation library - mirrors
  ai.eal.models / ai.ear.models's split. ai.taxonomy.models_pydantic carries
  runtime validation for the same fields. See
  docs/70_Enterprise_Master_Taxonomy/TAXONOMY_SPECIFICATION.md.

WHAT THIS PACKAGE IS
  The real, authored content of the taxonomy architecture Sprint 2.1
  (docs/10_Taxonomy/) designed: Category tree, Attribute Group registry,
  Controlled Vocabularies and their Terms. It is a knowledge layer, not a
  framework layer - it does not redefine EAR's attribute registry, EAD's
  definitions, or Build-004's distribution engine; it supplies the content
  those already-built engines were designed to consume (EAR's
  taxonomy_references, EAD's allowed_values/knowledge_graph_reference).
"""
from dataclasses import dataclass, field
from typing import Literal

from ai.eal.models import DataType  # reused, not redefined

TAXONOMY_VERSION = "1.0"

GroupTier = Literal["platform", "domain"]
EntryStatus = Literal["active", "deprecated"]


@dataclass(frozen=True)
class Category:
    category_id: str
    domain: str
    name: str
    parent_id: str | None = None
    attribute_group_ids: list[str] = field(default_factory=list)
    status: EntryStatus = "active"
    taxonomy_version: str = TAXONOMY_VERSION


@dataclass(frozen=True)
class AttributeGroup:
    group_id: str
    name: str
    tier: GroupTier
    ear_namespace: str | None = None
    version: str = "v1"
    status: EntryStatus = "active"
    taxonomy_version: str = TAXONOMY_VERSION


@dataclass(frozen=True)
class Vocabulary:
    vocabulary_id: str
    name: str
    scope: Literal["global", "domain"]
    domain: str | None = None
    version: str = "v1"
    status: EntryStatus = "active"
    taxonomy_version: str = TAXONOMY_VERSION


@dataclass(frozen=True)
class TaxonomyAttribute:
    attribute_id: str
    group_id: str
    name: str
    data_type: DataType
    vocabulary_id: str | None = None
    ear_namespace: str | None = None
    status: EntryStatus = "active"
    taxonomy_version: str = TAXONOMY_VERSION


@dataclass(frozen=True)
class Term:
    term_id: str
    vocabulary_id: str
    label: str
    synonyms: list[str] = field(default_factory=list)
    parent_term_id: str | None = None
    status: EntryStatus = "active"
    superseded_by: str | None = None
    external_ids: list = field(default_factory=list)  # list[ai.eal.models.ExternalId]
    taxonomy_version: str = TAXONOMY_VERSION
