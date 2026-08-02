"""
Enterprise Pricing Service v1 - Pydantic models.

WHY
  Runtime validation for pricing config files (ai/pricing/config/*.json) and
  JSON Schema generation, kept in lockstep with ai.pricing.models by hand
  (small surface, checked by ai/pricing/test_pricing.py) - same rationale as
  ai.eal.models_pydantic. Config files are the one place in this module that
  is genuinely external, editable input (a typo'd currency code or a negative
  price should fail loudly at load time, not silently mis-price every call
  that follows), which is exactly what dataclasses don't check for you.

USAGE
  pip install pydantic
  python -m ai.pricing.test_pricing     # validates every config file + example
"""
from typing import Literal

from pydantic import BaseModel, Field, model_validator

PRICING_MODEL_VERSION = "1.0"

_CURRENCY_PATTERN = r"^[A-Z]{3}$"  # ISO 4217, e.g. USD, EUR, INR


class PriceComponentModel(BaseModel):
    unit_price: float = Field(ge=0)
    unit: Literal["per_token", "per_1k_tokens", "per_1m_tokens"] = "per_1m_tokens"


class TokenUsageModel(BaseModel):
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    recorded_at: str = Field(min_length=1)
    cached_tokens: int = Field(default=0, ge=0)
    reasoning_tokens: int = Field(default=0, ge=0)
    image_tokens: int = Field(default=0, ge=0)
    embedding_tokens: int = Field(default=0, ge=0)
    other_tokens: dict[str, int] = Field(default_factory=dict)
    request_id: str | None = None


class PricingRecordModel(BaseModel):
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    version: str = Field(min_length=1)
    effective_date: str = Field(min_length=1)  # ISO date; not datetime-parsed here,
    # the repository layer is where "as-of" comparison logic lives, not the schema.
    currency: str = Field(pattern=_CURRENCY_PATTERN)
    input_price: PriceComponentModel
    output_price: PriceComponentModel
    categories: dict[str, PriceComponentModel] = Field(default_factory=dict)
    pricing_id: str = ""

    @model_validator(mode="after")
    def _no_input_output_in_categories(self) -> "PricingRecordModel":
        # input/output have their own required fields precisely so they can
        # never silently be missing - reserving the names in `categories` too
        # would let a config author "override" one via the optional dict.
        overlap = {"input", "output"} & set(self.categories)
        if overlap:
            raise ValueError(f"categories must not redeclare {overlap} - use input_price/output_price")
        return self


class CostResultModel(BaseModel):
    status: Literal["calculated", "pending_calculation"]
    currency: str | None = Field(default=None, pattern=_CURRENCY_PATTERN)
    total_cost: float | None = Field(default=None, ge=0)
    breakdown: dict[str, float] = Field(default_factory=dict)
    pricing_id: str | None = None
    pricing_version: str | None = None
    reason: str | None = None

    @model_validator(mode="after")
    def _calculated_needs_total(self) -> "CostResultModel":
        if self.status == "calculated" and self.total_cost is None:
            raise ValueError("status=calculated requires total_cost")
        if self.status == "pending_calculation" and self.reason is None:
            raise ValueError("status=pending_calculation requires a reason")
        return self


class ExecutionAuditRecordModel(BaseModel):
    audit_id: str = Field(min_length=1)
    usage: TokenUsageModel
    cost: CostResultModel
    recorded_at: str = Field(min_length=1)
    pricing_model_version: str = PRICING_MODEL_VERSION


class PricingConfigFileModel(BaseModel):
    """One ai/pricing/config/<provider>.json file: every historical + current
    rate-card entry for that provider, across all its models."""
    provider: str = Field(min_length=1)
    records: list[PricingRecordModel]
    # Human-facing provenance, not consumed by the repository loader. Every
    # config file this module ships marks whether its numbers are confirmed
    # against the provider's live pricing page or are illustrative - "never
    # invent" applies to cost figures exactly as much as it does to GTINs or
    # review counts elsewhere in this project.
    source_note: str | None = None
