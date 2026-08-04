"""
Enterprise Attribute Intelligence Engine (Build-303) - normalization.

WHY THIS WRAPS ai.taxonomy INSTEAD OF DEFINING ITS OWN SYNONYM TABLE
  A synonym table is a controlled vocabulary - ai.taxonomy.Term already IS
  that (label + synonyms, scoped to a Vocabulary), and Relationship_Model.md
  is explicit that new vocabulary belongs there, "never invented ad hoc
  inline." AttributeNormalizer.normalize() is the exact matching rule
  ai.product_intelligence.resolvers.TaxonomyResolver already implements
  inline (attr.value == term.label or attr.value in term.synonyms) -
  extracted here as a standalone, reusable function for this package and any
  future caller.

WHY ai.product_intelligence.resolvers.TaxonomyResolver WAS NOT RETROFITTED
  TO CALL THIS FUNCTION
  ai.attribute_intelligence.integration (this sprint) reads FROM
  ai.product_intelligence (its ProductAggregate/ProductReadModel) - making
  ai.product_intelligence import back from ai.attribute_intelligence would
  create a real circular package dependency (product_intelligence ->
  attribute_intelligence -> product_intelligence), not just a style
  inconsistency. The five duplicated lines of matching logic are the
  correct, deliberate trade-off against that cycle - see ADR
  2026-08-02-attribute-intelligence-engine.md.
"""
from ai.taxonomy.catalog import TaxonomyCatalog
from ai.taxonomy.models_pydantic import TermModel, VocabularyModel


def normalize_against_vocabulary(
    catalog: TaxonomyCatalog, vocabulary_id_or_name: str, raw_value: str,
) -> TermModel | None:
    """Matches raw_value against every Term's label/synonyms within the
    named/identified Vocabulary. Returns None (not a guess) when nothing
    matches - normalization never invents a canonical value that isn't
    already a real, controlled Term."""
    for vocabulary in catalog.vocabularies:
        if vocabulary_id_or_name not in (vocabulary.vocabulary_id, vocabulary.name):
            continue
        for term in catalog.terms_in_vocabulary(vocabulary.vocabulary_id):
            if raw_value == term.label or raw_value in term.synonyms:
                return term
    return None


def normalize_against_any_vocabulary(catalog: TaxonomyCatalog, raw_value: str) -> TermModel | None:
    """Same matching rule, searched across every Vocabulary in the catalog -
    useful when the caller doesn't already know which Vocabulary a raw value
    belongs to (e.g. a free-text tag with no namespace prefix)."""
    for vocabulary in catalog.vocabularies:
        term = normalize_against_vocabulary(catalog, vocabulary.vocabulary_id, raw_value)
        if term is not None:
            return term
    return None


class AttributeNormalizer:
    """A thin, DI-friendly wrapper over the two functions above - most
    callers want an instance bound to one TaxonomyCatalog, not to pass the
    catalog on every call."""

    def __init__(self, catalog: TaxonomyCatalog):
        self._catalog = catalog

    def normalize(self, raw_value: str, vocabulary_id_or_name: str | None = None) -> TermModel | None:
        if vocabulary_id_or_name is not None:
            return normalize_against_vocabulary(self._catalog, vocabulary_id_or_name, raw_value)
        return normalize_against_any_vocabulary(self._catalog, raw_value)
