"""
Enterprise Attribute Intelligence Engine (Build-303) - source integration.

WHY THESE TWO FUNCTIONS AND NOTHING ELSE ARE REAL
  Both read data ai.product_intelligence already resolved for real - EAL
  attributes (Vision-sourced, already confidence+provenance-carrying) and
  Shopify tags (already tag-namespace-parsed by
  ai.product_intelligence.ProductReadModel). See extensions.py for why
  Merchant/Genome sources have no real integration this sprint. Knowledge
  Graph and Pricing are deliberately not adapted here either: neither
  produces data shaped like a candidate "attribute value" in the Phase 2
  sense (a graph edge or a cost figure isn't a competing observation of an
  attribute value) - forcing them into AttributeObservation would be a type
  mismatch, not real integration.

WHY registry_reference MAPPINGS ARE ALWAYS CALLER-SUPPLIED, NEVER GUESSED
  ai.ear's own EALAttributeRecord -> EAR join (get_by_eal_reference) is
  real and used directly. But Shopify tag namespaces ("occasion:",
  "theme:", ...) have no equivalent EAR-registered mapping anywhere in this
  repo yet (CLAUDE.md confirms `tags` is queried nowhere) - so
  tag_namespace_to_registry_reference must be supplied by the caller, who
  presumably registered those EAR entries, rather than invented here.
"""
from ai.ear import api as ear_api
from ai.ear.registry import Registry
from ai.product_intelligence.models import ProductAggregate, ProductReadModel

from ai.attribute_intelligence.models import AttributeObservation


def observations_from_eal(
    aggregate: ProductAggregate, ear_registry: Registry, observed_at: str,
) -> list[AttributeObservation]:
    observations = []
    for record in aggregate.attributes.attributes:
        entry = ear_api.get_by_eal_reference(ear_registry, record.canonical_path)
        if entry is None:
            continue
        observations.append(AttributeObservation(
            registry_reference=entry.attribute_id, subject_id=aggregate.identity.shopify_product_gid,
            source="vision", value=record.value, confidence=record.confidence,
            observed_at=observed_at, notes=f"provider={record.provenance.provider}",
        ))
    return observations


def observations_from_tags(
    read_model: ProductReadModel, tag_namespace_to_registry_reference: dict[str, str], observed_at: str,
) -> list[AttributeObservation]:
    observations = []
    for tag in read_model.tags:
        if ":" not in tag:
            continue
        namespace, _, value = tag.partition(":")
        registry_reference = tag_namespace_to_registry_reference.get(namespace)
        if registry_reference is None:
            continue
        observations.append(AttributeObservation(
            registry_reference=registry_reference, subject_id=read_model.shopify_product_gid,
            source="shopify", value=value, confidence=1.0,  # a direct tag read, not an inference - full confidence
            observed_at=observed_at,
        ))
    return observations
