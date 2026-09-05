"""
Recipe Costing - an interface-only extension point.

WHY NO CONCRETE COST IMPLEMENTATION SHIPS HERE
  Costing a recipe requires real per-ingredient unit costs (flour per kg,
  eggless binder per litre, ...) that don't exist anywhere in this
  repository - CLAUDE.md's own "never invent" rule (no fabricated GTINs,
  reviews, or delivery promises) applies exactly as much to a cost figure
  presented as real. UnconfiguredRecipeCostStrategy is a real, working,
  tested class - it just always answers Pending until someone supplies an
  ingredient cost table, at which point a RealIngredientCostStrategy (not
  written here) implements the same RecipeCostStrategy contract and every
  caller is unaffected.

WHAT'S NEEDED TO COMPLETE THIS DOMAIN
  A per-ingredient unit cost table (ingredient name/unit -> cost), sourced
  from real supplier invoices or a POS/inventory system - not something an
  engineering pass can supply on its own.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ai.pricing.models import CostResult


@dataclass(frozen=True)
class Ingredient:
    name: str
    quantity: float
    unit: str  # e.g. "g", "kg", "ml", "unit"

    def __post_init__(self):
        if not self.name:
            raise ValueError("name must be non-empty")
        if self.quantity <= 0:
            raise ValueError(f"quantity must be > 0, got {self.quantity}")
        if not self.unit:
            raise ValueError("unit must be non-empty")


@dataclass(frozen=True)
class RecipeCostContext:
    recipe_name: str
    ingredients: tuple[Ingredient, ...] = field(default_factory=tuple)
    currency: str = "USD"

    def __post_init__(self):
        if not self.recipe_name:
            raise ValueError("recipe_name must be non-empty")


class RecipeCostStrategy(ABC):
    @abstractmethod
    def calculate(self, context: RecipeCostContext) -> CostResult:
        """Never raises - returns CostResult.pending(...) for any recipe or
        ingredient it has no real cost data for."""


class UnconfiguredRecipeCostStrategy(RecipeCostStrategy):
    """The default until a real ingredient cost table exists. Always Pending
    - never guesses at a per-ingredient cost."""

    def calculate(self, context: RecipeCostContext) -> CostResult:
        return CostResult.pending(
            f"no ingredient cost data configured for recipe={context.recipe_name!r} "
            f"({len(context.ingredients)} ingredient(s))"
        )
