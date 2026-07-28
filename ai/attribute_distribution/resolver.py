"""
Enterprise Attribute Distribution v1 (Build-004) - mapping resolution.

WHY
  BL-2: given one EAL attribute record, its EAR registry entry, and its EAD
  definition, resolve the concrete write payload for a target system. This
  is a pure function - no HTTP, no Shopify/ERP calls, no database, no file
  writes, no AI calls, no retries. It validates inputs, resolves a mapping,
  applies the Risk R-9 verification gate, and returns a DistributionRecordModel
  describing the outcome (dry_run or failed) - it never causes an external
  side effect itself. See
  docs/60_Enterprise_Attribute_Distribution/EAD_SPECIFICATION.md.

VERIFICATION GATE (Risk R-9, this module's one real policy decision)
  Shopify is treated as customer-facing: distribution requires
  human_verification.status in ("verified", "corrected"). ERP is treated as
  internal/low-stakes: distribution is allowed regardless of verification
  status. Flagged explicitly here since the roadmap only states the general
  principle ("customer-facing fields need review"), not which systems count
  as which - this is the concrete rule this Build encodes.
"""
from ai.ead.models_pydantic import EADDefinitionModel
from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.eal.models_pydantic import EALAttributeRecordModel

from ai.attribute_distribution.ids import compute_distribution_id
from ai.attribute_distribution.models_pydantic import DistributionRecordModel

_SHOPIFY_REQUIRES_VERIFICATION = ("verified", "corrected")


def resolve_distribution(
    eal_record: EALAttributeRecordModel,
    ear_entry: EARAttributeEntryModel,
    ead_definition: EADDefinitionModel,
    target_system: str,
) -> DistributionRecordModel:
    if ear_entry.eal_reference != eal_record.canonical_path:
        raise ValueError(
            f"ear_entry.eal_reference {ear_entry.eal_reference!r} does not match "
            f"eal_record.canonical_path {eal_record.canonical_path!r} - inputs do not "
            f"describe the same attribute"
        )
    if ead_definition.registry_reference != ear_entry.attribute_id:
        raise ValueError(
            f"ead_definition.registry_reference {ead_definition.registry_reference!r} "
            f"does not match ear_entry.attribute_id {ear_entry.attribute_id!r} - inputs "
            f"do not describe the same attribute"
        )

    distribution_id = compute_distribution_id(ear_entry.attribute_id, target_system)
    verification_status = eal_record.human_verification.status

    mapping = (
        ead_definition.shopify_mapping if target_system == "shopify" else ead_definition.erp_mapping
    )
    if mapping is None:
        return DistributionRecordModel(
            registry_reference=ear_entry.attribute_id,
            target_system=target_system,
            value=eal_record.value,
            human_verification_status=verification_status,
            external_id=None,
            distribution_id=distribution_id,
            confidence=eal_record.confidence,
            status="failed",
            notes=f"no {target_system} mapping defined for {ear_entry.attribute_id}",
        )

    if target_system == "shopify" and verification_status not in _SHOPIFY_REQUIRES_VERIFICATION:
        return DistributionRecordModel(
            registry_reference=ear_entry.attribute_id,
            target_system=target_system,
            value=eal_record.value,
            human_verification_status=verification_status,
            external_id=None,
            distribution_id=distribution_id,
            confidence=eal_record.confidence,
            status="failed",
            notes=(
                f"blocked: Shopify distribution requires human_verification.status in "
                f"{_SHOPIFY_REQUIRES_VERIFICATION}, got {verification_status!r}"
            ),
        )

    return DistributionRecordModel(
        registry_reference=ear_entry.attribute_id,
        target_system=target_system,
        value=eal_record.value,
        human_verification_status=verification_status,
        external_id=mapping,
        distribution_id=distribution_id,
        confidence=eal_record.confidence,
        status="dry_run",
    )
