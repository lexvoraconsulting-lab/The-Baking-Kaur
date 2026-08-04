"""
Enterprise Attribute Intelligence Engine (Build-303) - Attribute Search.

WHY THIS IS A THIN COMPOSITION OVER ai.ear.api, NOT A NEW INDEX
  "Which attributes exist" is EAR's own question (Build-002's stated goal,
  see ai/ear/api.py's docstring) - by_namespace/by_owner/by_tag already
  answer it. AttributeSearchService adds nothing but a single entrypoint
  that also reaches into ai.taxonomy for vocabulary-term search, so a
  caller doesn't need to know which of the two registries a search term
  belongs to.
"""
from dataclasses import dataclass

from ai.ear import api as ear_api
from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.ear.registry import Registry
from ai.taxonomy.catalog import TaxonomyCatalog
from ai.taxonomy.models_pydantic import TermModel


@dataclass
class AttributeSearchService:
    ear_registry: Registry
    taxonomy_catalog: TaxonomyCatalog

    def find_attributes_by_namespace(self, namespace: str) -> list[EARAttributeEntryModel]:
        return ear_api.by_namespace(self.ear_registry, namespace)

    def find_attributes_by_owner(self, owner: str) -> list[EARAttributeEntryModel]:
        return ear_api.by_owner(self.ear_registry, owner)

    def find_attributes_by_tag(self, tag: str) -> list[EARAttributeEntryModel]:
        return ear_api.by_tag(self.ear_registry, tag)

    def find_terms_by_label_substring(self, substring: str) -> list[TermModel]:
        lowered = substring.lower()
        return [t for t in self.taxonomy_catalog.terms if lowered in t.label.lower()]
