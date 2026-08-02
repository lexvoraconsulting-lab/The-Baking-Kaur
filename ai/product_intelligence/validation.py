"""
Enterprise Product Intelligence Engine v1 - Product Validation Service.

WHY THIS IS BUSINESS-RULE VALIDATION, NOT SCHEMA VALIDATION
  Every field on ProductAggregate already came from an upstream system that
  validated its own shape (EAL/EAR/EAD/Taxonomy/Pricing all validate at
  their own boundary). What's missing - and what this service actually
  checks - is cross-slice, product-level correctness: does this aggregate
  hang together as one coherent product, not whether any single field is
  well-formed.

WHY MISSING SLICES ARE WARNINGS, NOT ERRORS
  A Pending pricing slice or an empty Collection slice is often *honest*,
  not broken - CLAUDE.md itself documents that Shopify `tags` is queried
  nowhere yet, so every CollectionSlice is empty today by design, not by
  bug. Only genuinely product-breaking conditions (no identity, no metadata
  at all) are errors; the rest are warnings a caller can act on or ignore.
"""
from dataclasses import dataclass

from ai.product_intelligence.models import ProductAggregate, ProductValidationResult, ValidationIssue


@dataclass(frozen=True)
class ProductValidationService:
    """Stateless - validate() is a pure function of the aggregate it's
    given. No constructor dependencies, unlike the resolvers, since
    business-rule validation needs nothing external to reason about."""

    def validate(self, aggregate: ProductAggregate, validated_at: str) -> ProductValidationResult:
        issues: list[ValidationIssue] = []
        issues.extend(self._check_identity(aggregate))
        issues.extend(self._check_metadata(aggregate))
        issues.extend(self._check_attributes(aggregate))
        issues.extend(self._check_taxonomy(aggregate))
        issues.extend(self._check_collections(aggregate))
        issues.extend(self._check_pricing(aggregate))
        issues.extend(self._check_entity_links(aggregate))

        is_valid = not any(issue.severity == "error" for issue in issues)
        return ProductValidationResult(
            product_intelligence_id=aggregate.identity.product_intelligence_id,
            is_valid=is_valid,
            validated_at=validated_at,
            issues=tuple(issues),
        )

    @staticmethod
    def _check_identity(aggregate: ProductAggregate) -> list[ValidationIssue]:
        if not aggregate.identity.handle:
            return [ValidationIssue(
                code="missing_handle", severity="error",
                message="ProductIdentity has no handle", field="identity.handle",
            )]
        return []

    @staticmethod
    def _check_metadata(aggregate: ProductAggregate) -> list[ValidationIssue]:
        if aggregate.metadata.title is None and aggregate.metadata.status is None:
            return [ValidationIssue(
                code="metadata_unresolved", severity="error",
                message="MetadataSlice is entirely empty - the metadata resolver may not be wired",
                field="metadata",
            )]
        return []

    @staticmethod
    def _check_attributes(aggregate: ProductAggregate) -> list[ValidationIssue]:
        if not aggregate.attributes.attributes:
            return [ValidationIssue(
                code="no_attributes_resolved", severity="warning",
                message="No EAL attributes resolved for this product's linked entities",
                field="attributes",
            )]
        return []

    @staticmethod
    def _check_taxonomy(aggregate: ProductAggregate) -> list[ValidationIssue]:
        if not aggregate.taxonomy.categories and not aggregate.taxonomy.terms:
            return [ValidationIssue(
                code="no_taxonomy_resolved", severity="warning",
                message="No taxonomy categories or terms resolved for this product",
                field="taxonomy",
            )]
        return []

    @staticmethod
    def _check_collections(aggregate: ProductAggregate) -> list[ValidationIssue]:
        if not aggregate.collections.tags:
            return [ValidationIssue(
                code="no_tags_resolved", severity="warning",
                message="No Shopify tags resolved - expected until a live CollectionResolverPort is wired in",
                field="collections",
            )]
        return []

    @staticmethod
    def _check_pricing(aggregate: ProductAggregate) -> list[ValidationIssue]:
        cost = aggregate.pricing.cost_result
        if cost is None:
            return [ValidationIssue(
                code="pricing_unresolved", severity="warning",
                message="PricingSlice has no cost result at all",
                field="pricing",
            )]
        if cost.status == "pending_calculation":
            return [ValidationIssue(
                code="pricing_pending", severity="warning",
                message=cost.reason or "pricing is pending, not calculated",
                field="pricing",
            )]
        return []

    @staticmethod
    def _check_entity_links(aggregate: ProductAggregate) -> list[ValidationIssue]:
        seen = set()
        issues = []
        for link in aggregate.entity_links:
            key = (link.eal_entity_id, link.relationship)
            if key in seen:
                issues.append(ValidationIssue(
                    code="duplicate_entity_link", severity="warning",
                    message=f"entity_id={link.eal_entity_id!r} linked twice with relationship={link.relationship!r}",
                    field="entity_links",
                ))
            seen.add(key)
        return issues
