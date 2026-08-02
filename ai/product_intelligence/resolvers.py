"""
Enterprise Product Intelligence Engine v1 - resolvers.

WHY ONE MODULE FOR FIVE RESOLVERS
  Each resolver is a small, single-purpose adapter (join existing data into
  one slice of ProductAggregate) - five tiny classes, not five packages. If
  any one grows real complexity later, it can move to its own module then
  (see ai/vision/python/providers.py's own VIG-002 rationale for the same
  "no subpackage until there's a real second tenant" reasoning).

REAL (OFFLINE) VS LIVE (DI) RESOLVERS
  AttributeResolver, TaxonomyResolver, and PricingResolver wrap pure-Python
  packages (ai.eal/ai.ear/ai.ead, ai.taxonomy, ai.pricing) - fully real,
  fully testable with no network. CollectionResolver and MetadataAggregator
  need live Shopify data that no offline fixture can provide; both are typed
  against a small Protocol port and shipped with a fake implementation for
  tests. A default live implementation (Shopify tags/SEO fields, via
  ai.pricing.shopify_gql's proven CLI/token dual-path) is future work, not
  built here - CLAUDE.md confirms Shopify `tags` is queried nowhere in this
  repo today, so there is no existing call site to reuse yet.

WHY THE ATTRIBUTE JOIN NEEDS entity_links, NOT A LIVE INDEX
  ECP-100 found no product_id -> eal_entity_id index exists anywhere. This
  resolver does not invent one - it accepts the join (ProductEntityLink
  records) as an explicit input, the same "caller supplies what it knows,
  resolver never guesses" shape as every other DI boundary in this engine.
"""
from typing import Protocol

from ai.attribute_distribution.models import DistributionRecord
from ai.ead.definitions import DefinitionSet
from ai.ead.models_pydantic import EADDefinitionModel
from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.ear.registry import Registry
from ai.eal.models import EALAttributeRecord
from ai.pricing.models import CostResult
from ai.pricing.service import PricingService
from ai.taxonomy.catalog import TaxonomyCatalog

from ai.product_intelligence.models import (
    AttributeSlice, CollectionSlice, MetadataSlice, PricingSlice,
    ProductEntityLink, ProductIdentity, TaxonomySlice,
)


def _matches_vocabulary(vocabulary_id_or_name: str, catalog_vocab) -> bool:
    return vocabulary_id_or_name in (catalog_vocab.vocabulary_id, catalog_vocab.name)


class AttributeResolver:
    """Joins EAL records -> EAR entries -> EAD definitions for a product,
    via its ProductEntityLink set. eal_records is DI'd (a flat list any
    caller assembles from wherever its EAL records currently live - no such
    single store exists yet, per Build-008's not-started status)."""

    def __init__(self, ear_registry: Registry, ead_definitions: DefinitionSet,
                 eal_records: list[EALAttributeRecord]):
        self._ear = ear_registry
        self._ead = ead_definitions
        self._eal_by_entity_id: dict[str, list[EALAttributeRecord]] = {}
        for record in eal_records:
            self._eal_by_entity_id.setdefault(record.entity_id, []).append(record)

    def resolve(self, entity_links: list[ProductEntityLink]) -> AttributeSlice:
        entity_ids = tuple(sorted({link.eal_entity_id for link in entity_links}))
        attributes: list[EALAttributeRecord] = []
        for entity_id in entity_ids:
            attributes.extend(self._eal_by_entity_id.get(entity_id, []))
        return AttributeSlice(attributes=tuple(attributes), source_entity_ids=entity_ids)

    def registry_entry_for(self, eal_reference: str) -> EARAttributeEntryModel | None:
        return self._ear.get(eal_reference=eal_reference)

    def definition_for(self, registry_reference: str) -> EADDefinitionModel | None:
        return self._ead.get(registry_reference)


class TaxonomyResolver:
    """Joins EAL attribute values -> Taxonomy Terms via the attribute's own
    `vocabulary` field (a controlled-vocabulary id or name) and the value
    itself (matched against a Term's label or synonyms) - the real join
    EAL/Taxonomy already share, not a guessed one. Relationships attached to
    a matched Term (e.g. term -> category) are included via
    TaxonomyCatalog.relationships_for, which is only ever as complete as
    what the catalog already records - this resolver never fabricates a
    relationship the catalog doesn't have."""

    def __init__(self, catalog: TaxonomyCatalog):
        self._catalog = catalog

    def resolve(self, attributes: AttributeSlice) -> TaxonomySlice:
        matched_terms = {}
        for attr in attributes.attributes:
            if not attr.vocabulary or attr.value is None:
                continue
            for vocab in self._catalog.vocabularies:
                if not _matches_vocabulary(attr.vocabulary, vocab):
                    continue
                for term in self._catalog.terms_in_vocabulary(vocab.vocabulary_id):
                    if attr.value == term.label or attr.value in term.synonyms:
                        matched_terms[term.term_id] = term

        relationships = {}
        for term_id in matched_terms:
            for rel in self._catalog.relationships_for("term", term_id):
                relationships[rel.relationship_id] = rel

        category_ids = {r.subject_id for r in relationships.values() if r.subject_type == "category"}
        category_ids |= {r.object_id for r in relationships.values() if r.object_type == "category"}
        categories = tuple(
            c for c in (self._catalog.get_category(cid) for cid in sorted(category_ids)) if c
        )
        return TaxonomySlice(
            categories=categories,
            terms=tuple(matched_terms[tid] for tid in sorted(matched_terms)),
            relationships=tuple(relationships.values()),
        )


class PricingResolver:
    """Wraps ai.pricing.PricingService - never recomputes cost logic itself.
    Returns CostResult.pending() (not a failure) when no distribution/cost
    record exists for this product yet, matching this engine's system-wide
    Pending-not-failing rule."""

    def __init__(self, pricing_service: PricingService):
        self._pricing_service = pricing_service

    def resolve(self, distribution_records: list[DistributionRecord]) -> PricingSlice:
        for record in distribution_records:
            if record.status in ("success", "dry_run") and record.value is not None:
                return PricingSlice(cost_result=CostResult(
                    status="calculated", total_cost=float(record.value),
                    breakdown={}, reason=None,
                ))
        return PricingSlice(cost_result=CostResult.pending(
            "no successful distribution record carries a priced value for this product yet"
        ))


class CollectionResolverPort(Protocol):
    """Live Shopify `tags`/collection membership - Protocol, not an ABC,
    since the only implementations that will ever exist are a fake (tests)
    and a future thin wrapper over the Shopify Admin API; no shared base
    behaviour to inherit."""

    def fetch(self, identity: ProductIdentity) -> CollectionSlice: ...


class MetadataResolverPort(Protocol):
    """Live Shopify title/status/productType/seo{title,description}."""

    def fetch(self, identity: ProductIdentity) -> MetadataSlice: ...


class FakeCollectionResolver:
    """Test/offline double - constructor-injected fixed data, never a live call."""

    def __init__(self, by_gid: dict[str, CollectionSlice] | None = None):
        self._by_gid = by_gid or {}

    def fetch(self, identity: ProductIdentity) -> CollectionSlice:
        return self._by_gid.get(identity.shopify_product_gid, CollectionSlice())


class FakeMetadataResolver:
    """Test/offline double - constructor-injected fixed data, never a live call."""

    def __init__(self, by_gid: dict[str, MetadataSlice] | None = None):
        self._by_gid = by_gid or {}

    def fetch(self, identity: ProductIdentity) -> MetadataSlice:
        return self._by_gid.get(identity.shopify_product_gid, MetadataSlice())
