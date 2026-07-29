"""
Enterprise Master Taxonomy (Build-005) - the TaxonomyCatalog container.

WHY
  Holds all four entity collections in memory, keyed for O(1) lookup by ID -
  the same design EAR's Registry uses, chosen for the same reason: this
  catalog is expected to reach 500+ Attribute Groups and 10,000+ Controlled
  Vocabulary Terms (per Build-005's stated scale target), where a linear scan
  per lookup would not hold up. Runs validate_catalog() at construction, so a
  TaxonomyCatalog that exists is guaranteed internally consistent, never a
  partially-checked one. See docs/70_Enterprise_Master_Taxonomy/TAXONOMY_SPECIFICATION.md.
"""
from ai.taxonomy.models_pydantic import (
    AttributeGroupModel,
    CategoryModel,
    TermModel,
    VocabularyModel,
)
from ai.taxonomy.validation import validate_catalog


class TaxonomyCatalog:
    def __init__(
        self,
        categories: list[CategoryModel],
        attribute_groups: list[AttributeGroupModel],
        vocabularies: list[VocabularyModel],
        terms: list[TermModel],
    ):
        validate_catalog(categories, attribute_groups, vocabularies, terms)
        self._categories = {c.category_id: c for c in categories}
        self._attribute_groups = {g.group_id: g for g in attribute_groups}
        self._vocabularies = {v.vocabulary_id: v for v in vocabularies}
        self._terms = {t.term_id: t for t in terms}

    def __len__(self) -> int:
        return len(self._categories) + len(self._attribute_groups) + len(self._vocabularies) + len(self._terms)

    def get_category(self, category_id: str) -> CategoryModel | None:
        return self._categories.get(category_id)

    def get_attribute_group(self, group_id: str) -> AttributeGroupModel | None:
        return self._attribute_groups.get(group_id)

    def get_vocabulary(self, vocabulary_id: str) -> VocabularyModel | None:
        return self._vocabularies.get(vocabulary_id)

    def get_term(self, term_id: str) -> TermModel | None:
        return self._terms.get(term_id)

    def terms_in_vocabulary(self, vocabulary_id: str) -> list[TermModel]:
        return [t for t in self._terms.values() if t.vocabulary_id == vocabulary_id]

    def children_of(self, category_id: str) -> list[CategoryModel]:
        return [c for c in self._categories.values() if c.parent_id == category_id]

    @property
    def categories(self) -> list[CategoryModel]:
        return list(self._categories.values())

    @property
    def attribute_groups(self) -> list[AttributeGroupModel]:
        return list(self._attribute_groups.values())

    @property
    def vocabularies(self) -> list[VocabularyModel]:
        return list(self._vocabularies.values())

    @property
    def terms(self) -> list[TermModel]:
        return list(self._terms.values())
