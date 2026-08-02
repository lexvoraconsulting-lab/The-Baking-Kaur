"""
Enterprise Pricing Service v1 - identifier strategy.

WHY CONTENT-HASH, NOT SEQUENTIAL
  Pricing records live in flat config files anyone can edit and are not
  allocated by one central process, the same "many uncoordinated producers"
  situation as ai.eal (see ai.eal.ids' rationale) rather than ai.ear's single-
  registry case - two people independently adding the same
  (provider, model, version, effective_date) rate-card entry in two branches
  should get the same pricing_id with zero coordination. Distinct namespace
  UUID from every other module's, so a pricing_id can never collide with an
  attribute_id/registry_uuid/definition_id/distribution_id even given the
  same input string.
"""
import uuid

PRICING_NAMESPACE_UUID = uuid.UUID("7c3e9f2a-1b6d-4c8e-a3f5-2d9b6e4c1a80")

AUDIT_NAMESPACE_UUID = uuid.UUID("4a1d8b6e-2f3c-4e9a-b7d1-6c8a3f5e2b90")


def compute_pricing_id(provider: str, model: str, version: str, effective_date: str) -> str:
    key = f"{provider}|{model}|{version}|{effective_date}"
    return str(uuid.uuid5(PRICING_NAMESPACE_UUID, key))


def compute_audit_id(usage_provider: str, usage_model: str, recorded_at: str,
                      input_tokens: int, output_tokens: int, request_id: str | None) -> str:
    """Deterministic if the exact same execution is replayed (useful for
    idempotent re-recording); request_id, when the provider supplies one,
    makes two genuinely distinct calls with identical token counts distinct
    audit entries instead of colliding."""
    key = f"{usage_provider}|{usage_model}|{recorded_at}|{input_tokens}|{output_tokens}|{request_id or ''}"
    return str(uuid.uuid5(AUDIT_NAMESPACE_UUID, key))
