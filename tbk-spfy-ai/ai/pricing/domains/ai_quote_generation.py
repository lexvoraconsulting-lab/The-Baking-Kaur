"""
AI-Assisted Quote Generation - a port interface, no implementation.

WHY THIS IS THE MOST SPECULATIVE EXTENSION POINT IN THIS PACKAGE, AND SAYS SO
  "Generate a customer-facing quote using AI" isn't a pricing-math problem
  like the other domains - it needs a real prompt/business-rules spec (what
  tone, what's negotiable, what must never be offered) that doesn't exist
  yet anywhere in this repo. QuoteGenerationPort defines the shape a future
  implementation would fill (take a costed request, produce a customer-
  facing quote) without pretending an AI-generated quote is a solved problem
  today.

WHAT'S NEEDED TO COMPLETE THIS DOMAIN
  A real specification for what a "quote" contains and how it may vary
  (validity window, negotiability, required disclaimers), plus a chosen
  generation approach (templated from CostResult, or LLM-drafted copy around
  a fixed number this engine already calculated - the latter must never let
  the model invent the number itself, only phrase around a value
  ai.pricing already computed, consistent with this engine's core rule that
  cost calculation is a deterministic strategy, never a guess).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ai.pricing.models import CostResult


@dataclass(frozen=True)
class Quote:
    customer_facing_text: str
    cost: CostResult
    valid_until: str | None = None
    disclaimers: tuple[str, ...] = field(default_factory=tuple)


class QuoteGenerationPort(ABC):
    @abstractmethod
    def generate_quote(self, cost: CostResult, context: dict) -> Quote:
        """cost is always a value this engine already calculated (or a
        Pending result) - a QuoteGenerationPort implementation's job is
        presentation, never re-deriving or adjusting the number itself.
        context is deliberately a plain dict, not a typed dataclass, since
        what a quote needs to reference (occasion, customer name, delivery
        date) is exactly the part of this domain with no spec yet."""


class NotImplementedQuoteGenerator(QuoteGenerationPort):
    """The only concrete implementation until a real quote specification and
    generation approach exist. Fails loudly, the same reasoning as
    erp_integration.NotConnectedERPPort - a caller reaching this class wants
    a feature that hasn't been designed yet, which is a configuration error
    to surface, not a routine Pending-cost case."""

    def generate_quote(self, cost: CostResult, context: dict) -> Quote:
        raise NotImplementedError(
            "No quote generation strategy is configured - see this module's docstring "
            "for what a real implementation needs before it can be written"
        )
