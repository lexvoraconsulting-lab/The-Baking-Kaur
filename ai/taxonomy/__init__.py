"""
Enterprise Master Taxonomy (Build-005), Workstream TAX. Re-exports the public
surface so downstream modules do `from ai.taxonomy import TaxonomyCatalog`
instead of reaching into submodules. Authors the real content EAR's
taxonomy_references and EAD's allowed_values/knowledge_graph_reference were
built to point at - see docs/70_Enterprise_Master_Taxonomy/TAXONOMY_SPECIFICATION.md.
"""
from ai.taxonomy.models import (
    TAXONOMY_VERSION,
    AttributeGroup,
    Category,
    TaxonomyAttribute,
    Term,
    Vocabulary,
)
from ai.taxonomy.models_pydantic import (
    AttributeGroupModel,
    CategoryModel,
    TaxonomyAttributeModel,
    TermModel,
    VocabularyModel,
)
from ai.taxonomy.ids import (
    allocate_attribute_id,
    allocate_category_id,
    allocate_group_id,
    allocate_term_id,
    allocate_vocabulary_id,
    is_valid_attribute_id,
    is_valid_category_id,
    is_valid_group_id,
    is_valid_term_id,
    is_valid_vocabulary_id,
)
from ai.taxonomy.catalog import TaxonomyCatalog
from ai.taxonomy.loader import load_catalog
from ai.taxonomy.exporter import export_catalog, regenerate_schemas

__all__ = [
    "TAXONOMY_VERSION",
    "Category",
    "AttributeGroup",
    "Vocabulary",
    "Term",
    "TaxonomyAttribute",
    "CategoryModel",
    "AttributeGroupModel",
    "VocabularyModel",
    "TermModel",
    "TaxonomyAttributeModel",
    "allocate_category_id",
    "allocate_group_id",
    "allocate_vocabulary_id",
    "allocate_term_id",
    "allocate_attribute_id",
    "is_valid_category_id",
    "is_valid_group_id",
    "is_valid_vocabulary_id",
    "is_valid_term_id",
    "is_valid_attribute_id",
    "TaxonomyCatalog",
    "load_catalog",
    "export_catalog",
    "regenerate_schemas",
]
