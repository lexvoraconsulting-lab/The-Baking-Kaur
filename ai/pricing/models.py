"""
Enterprise Pricing Service v1 - plain dataclass models.

WHY
  Same split as ai.eal: this module is the IDE/human-facing shape with no
  third-party dependency; ai.pricing.models_pydantic mirrors it for runtime
  validation of pricing config files and JSON Schema generation. See
  docs/AI/PricingService.md.

DESIGN NOTE - why TokenUsage and CostResult are separate types
  The request that drives this module ("token usage must always be recorded
  ... cost calculation must be separated from token collection") is a real
  constraint, not a style preference: a provider call can fail to price (an
  unknown model, a missing config file, a future modality with no rate card
  yet) without that ever being allowed to fail the call itself or lose the
  usage data. Keeping TokenUsage capture and CostResult calculation as two
  independently-constructible types is what makes "record usage now,
  calculate cost later or never" possible - a merged UsageAndCost type would
  force cost to exist (even as null-filled) the moment usage is captured.
"""
from dataclasses import dataclass, field
from typing import Literal

PRICING_MODEL_VERSION = "1.0"

# unit_price is always expressed per this many tokens - per-token float pricing
# on numbers like $0.0000006 loses precision and is unreadable in config files;
# every real provider rate card (OpenAI, Anthropic, Google) publishes per-1M.
PriceUnit = Literal["per_token", "per_1k_tokens", "per_1m_tokens"]

CostStatus = Literal["calculated", "pending_calculation"]

# Fixed set of token categories this module has direct support for today.
# Not a hard ceiling - TokenUsage.other_tokens and PricingRecord.categories are
# open dicts precisely so a new modality doesn't require a schema change (see
# "future modalities" in the module docstring) - this Literal documents which
# categories the *built-in* strategy treats as first-class, not which
# categories are ever allowed to exist.
TokenCategory = Literal[
    "input", "output", "cached", "reasoning", "image", "embedding",
]


@dataclass(frozen=True)
class PriceComponent:
    """One category's unit price - the atom every PricingRecord is built from."""
    unit_price: float
    unit: PriceUnit = "per_1m_tokens"

    def cost_for(self, token_count: int) -> float:
        divisor = {"per_token": 1, "per_1k_tokens": 1_000, "per_1m_tokens": 1_000_000}[self.unit]
        return (token_count / divisor) * self.unit_price


@dataclass(frozen=True)
class TokenUsage:
    """Captured verbatim from a provider response - never derived, never guessed.
    Always constructible even when nothing is known about pricing yet."""
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    recorded_at: str
    cached_tokens: int = 0
    reasoning_tokens: int = 0
    image_tokens: int = 0
    embedding_tokens: int = 0
    # Open extension point for a modality this module doesn't name yet (e.g.
    # "video_tokens", "audio_seconds") - added without touching this dataclass.
    other_tokens: dict[str, int] = field(default_factory=dict)
    request_id: str | None = None

    def category_counts(self) -> dict[str, int]:
        """All non-zero token categories, input/output always included even at 0."""
        counts = {
            "input": self.input_tokens,
            "output": self.output_tokens,
        }
        for name, value in (
            ("cached", self.cached_tokens),
            ("reasoning", self.reasoning_tokens),
            ("image", self.image_tokens),
            ("embedding", self.embedding_tokens),
        ):
            if value:
                counts[name] = value
        for name, value in self.other_tokens.items():
            if value:
                counts[name] = value
        return counts


@dataclass(frozen=True)
class PricingRecord:
    """One versioned, dated rate card entry. provider+model+version+effective_date
    is the natural key - see ai.pricing.ids.compute_pricing_id."""
    provider: str
    model: str
    version: str
    effective_date: str
    currency: str
    input_price: PriceComponent
    output_price: PriceComponent
    categories: dict[str, PriceComponent] = field(default_factory=dict)
    pricing_id: str = ""

    def price_for(self, category: str) -> PriceComponent | None:
        if category == "input":
            return self.input_price
        if category == "output":
            return self.output_price
        return self.categories.get(category)


@dataclass(frozen=True)
class CostResult:
    """Either a real calculated cost, or an explicit, non-failing Pending state.
    pricing_version is copied onto every audit record at execution time even if
    the underlying config file is edited or deleted later - that's what makes
    the audit trail historically accurate regardless of config drift."""
    status: CostStatus
    currency: str | None = None
    total_cost: float | None = None
    breakdown: dict[str, float] = field(default_factory=dict)
    pricing_id: str | None = None
    pricing_version: str | None = None
    reason: str | None = None

    @staticmethod
    def pending(reason: str) -> "CostResult":
        return CostResult(status="pending_calculation", reason=reason)


@dataclass(frozen=True)
class ExecutionAuditRecord:
    """What the Audit Engine persists. Constructed from a TokenUsage (always
    present) and a CostResult (which may itself be Pending) - the audit
    record's own shape doesn't change based on whether pricing succeeded."""
    audit_id: str
    usage: TokenUsage
    cost: CostResult
    recorded_at: str
    pricing_model_version: str = PRICING_MODEL_VERSION
