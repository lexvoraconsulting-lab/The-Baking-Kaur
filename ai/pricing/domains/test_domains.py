#!/usr/bin/env python3
"""
Self-check for the Enterprise Pricing Intelligence Engine's domain extension
points - no network calls.

USAGE
  python -m ai.pricing.domains.test_domains
"""
from ai.pricing.domains.corporate_pricing import (
    CorporatePricingContext,
    CorporateRateTier,
    TieredCorporateRateStrategy,
)
from ai.pricing.domains.ai_quote_generation import NotImplementedQuoteGenerator
from ai.pricing.domains.customization import CustomizationContext, UnconfiguredCustomizationCostStrategy
from ai.pricing.domains.delivery import DeliveryContext, DistanceBand, TieredDistanceDeliveryStrategy
from ai.pricing.domains.erp_integration import (
    NotConnectedERPPort,
    calculated_cost_to_erp_fields,
)
from ai.pricing.domains.packaging import PackagingContext, UnconfiguredPackagingCostStrategy
from ai.pricing.domains.recipe_costing import (
    Ingredient,
    RecipeCostContext,
    UnconfiguredRecipeCostStrategy,
)
from ai.pricing.models import CostResult
from ai.pricing.domains.discounts_promotions import (
    BuyXGetYFreeStrategy,
    DiscountContext,
    FlatAmountDiscountStrategy,
    PercentageDiscountStrategy,
    TieredVolumeDiscountStrategy,
    VolumeTier,
)


def test_percentage_discount():
    result = PercentageDiscountStrategy(percentage=10).apply(DiscountContext(base_amount=100.0))
    assert result.status == "calculated"
    assert result.total_cost == 90.0
    assert result.breakdown == {"original": 100.0, "discount": -10.0}


def test_percentage_discount_rejects_out_of_range():
    try:
        PercentageDiscountStrategy(percentage=150)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_flat_amount_discount_never_goes_negative():
    result = FlatAmountDiscountStrategy(amount=1000.0).apply(DiscountContext(base_amount=50.0))
    assert result.total_cost == 0.0, "a discount larger than the base amount must floor at 0"
    assert result.breakdown["discount"] == -50.0, "the discount actually applied, not the requested amount"


def test_tiered_volume_discount_picks_best_qualifying_tier():
    strategy = TieredVolumeDiscountStrategy(tiers=(VolumeTier(10, 5), VolumeTier(50, 10)))
    below_any_tier = strategy.apply(DiscountContext(base_amount=100.0, quantity=5))
    assert below_any_tier.total_cost == 100.0

    mid_tier = strategy.apply(DiscountContext(base_amount=100.0, quantity=20))
    assert mid_tier.total_cost == 95.0

    top_tier = strategy.apply(DiscountContext(base_amount=100.0, quantity=60))
    assert top_tier.total_cost == 90.0, "60 qualifies for both tiers - the higher percentage must win"


def test_buy_x_get_y_free():
    strategy = BuyXGetYFreeStrategy(buy=3, get_free=1)
    # 8 units at $10 each = $80 base; group size is 3 paid + 1 free = 4, and
    # 8 // 4 = 2 complete groups fit -> 2 free units.
    result = strategy.apply(DiscountContext(base_amount=80.0, quantity=8))
    assert result.breakdown["discount"] == -20.0
    assert result.total_cost == 60.0

    # 5 units: only 1 complete group of 4 fits (the 5th unit is a leftover,
    # not enough to earn a second free unit) -> exactly 1 free unit.
    partial = strategy.apply(DiscountContext(base_amount=50.0, quantity=5))
    assert partial.breakdown["discount"] == -10.0


def test_discount_context_rejects_invalid_input():
    try:
        DiscountContext(base_amount=-1)
        assert False, "expected ValueError"
    except ValueError:
        pass
    try:
        DiscountContext(base_amount=10, quantity=0)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_corporate_pricing_returns_pending_for_unknown_account():
    strategy = TieredCorporateRateStrategy(rates_by_account={})
    result = strategy.calculate(CorporatePricingContext(account_id="unknown", quantity=10))
    assert result.status == "pending_calculation"
    assert result.reason is not None


def test_corporate_pricing_applies_best_qualifying_tier():
    strategy = TieredCorporateRateStrategy(rates_by_account={
        "acct-1": (CorporateRateTier(50, 8.5), CorporateRateTier(200, 7.0)),
    })
    below_min = strategy.calculate(CorporatePricingContext(account_id="acct-1", quantity=10))
    assert below_min.status == "pending_calculation", "10 doesn't meet even the lowest tier (50)"

    mid = strategy.calculate(CorporatePricingContext(account_id="acct-1", quantity=100))
    assert mid.status == "calculated"
    assert mid.total_cost == 850.0  # 100 * 8.5

    top = strategy.calculate(CorporatePricingContext(account_id="acct-1", quantity=500))
    assert top.total_cost == 3500.0  # 500 * 7.0 - the better negotiated rate wins


def test_corporate_rate_tier_rejects_invalid_input():
    try:
        CorporateRateTier(min_quantity=0, unit_price=5.0)
        assert False, "expected ValueError"
    except ValueError:
        pass
    try:
        CorporateRateTier(min_quantity=1, unit_price=-1.0)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_delivery_picks_the_correct_band():
    strategy = TieredDistanceDeliveryStrategy(bands=(
        DistanceBand(5, 30.0), DistanceBand(10, 50.0), DistanceBand(15, 80.0),
    ))
    near = strategy.calculate(DeliveryContext(distance_km=3, order_subtotal=500))
    assert near.status == "calculated" and near.total_cost == 30.0

    mid = strategy.calculate(DeliveryContext(distance_km=8, order_subtotal=500))
    assert mid.total_cost == 50.0

    edge = strategy.calculate(DeliveryContext(distance_km=15, order_subtotal=500))
    assert edge.total_cost == 80.0, "exactly at the band boundary must still match that band"


def test_delivery_beyond_every_band_is_pending_not_guessed():
    strategy = TieredDistanceDeliveryStrategy(bands=(DistanceBand(15, 80.0),))
    result = strategy.calculate(DeliveryContext(distance_km=20, order_subtotal=500))
    assert result.status == "pending_calculation"
    assert result.total_cost is None


def test_delivery_enforces_minimum_order_when_configured():
    strategy = TieredDistanceDeliveryStrategy(
        bands=(DistanceBand(15, 80.0),), minimum_order_subtotal=350.0,
    )
    below_min = strategy.calculate(DeliveryContext(distance_km=5, order_subtotal=200))
    assert below_min.status == "pending_calculation"

    at_min = strategy.calculate(DeliveryContext(distance_km=5, order_subtotal=350))
    assert at_min.status == "calculated"


def test_delivery_context_rejects_negative_values():
    try:
        DeliveryContext(distance_km=-1, order_subtotal=100)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_recipe_costing_unconfigured_returns_pending():
    context = RecipeCostContext(
        recipe_name="Chocolate Truffle Cake",
        ingredients=(Ingredient(name="flour", quantity=500, unit="g"),),
    )
    result = UnconfiguredRecipeCostStrategy().calculate(context)
    assert result.status == "pending_calculation"
    assert result.total_cost is None
    assert "Chocolate Truffle Cake" in result.reason


def test_recipe_ingredient_rejects_invalid_input():
    try:
        Ingredient(name="flour", quantity=0, unit="g")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_packaging_unconfigured_returns_pending():
    context = PackagingContext(box_type="premium-box", size="2kg", add_ons=("ribbon",))
    result = UnconfiguredPackagingCostStrategy().calculate(context)
    assert result.status == "pending_calculation"
    assert "premium-box" in result.reason


def test_customization_unconfigured_returns_pending():
    context = CustomizationContext(message_text="Happy Birthday", photo_print=True)
    result = UnconfiguredCustomizationCostStrategy().calculate(context)
    assert result.status == "pending_calculation"
    assert "message_text" in result.reason and "photo_print" in result.reason


def test_customization_context_rejects_invalid_colour_count():
    try:
        CustomizationContext(colour_count=0)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_erp_port_not_connected_raises_not_implemented():
    port = NotConnectedERPPort()
    try:
        port.push_price(None)
        assert False, "expected NotImplementedError"
    except NotImplementedError:
        pass
    try:
        port.pull_price("openai", "gpt-4o")
        assert False, "expected NotImplementedError"
    except NotImplementedError:
        pass


def test_erp_field_mapping_is_pure_and_generic():
    cost = CostResult(status="calculated", currency="USD", total_cost=1.5, pricing_version="v1")
    fields = calculated_cost_to_erp_fields(cost)
    assert fields == {"status": "calculated", "total_cost": 1.5, "currency": "USD", "pricing_version": "v1"}


def test_ai_quote_generator_not_configured_raises():
    generator = NotImplementedQuoteGenerator()
    cost = CostResult(status="calculated", currency="USD", total_cost=10.0)
    try:
        generator.generate_quote(cost, context={})
        assert False, "expected NotImplementedError"
    except NotImplementedError:
        pass


if __name__ == "__main__":
    test_percentage_discount()
    test_percentage_discount_rejects_out_of_range()
    test_flat_amount_discount_never_goes_negative()
    test_tiered_volume_discount_picks_best_qualifying_tier()
    test_buy_x_get_y_free()
    test_discount_context_rejects_invalid_input()
    test_corporate_pricing_returns_pending_for_unknown_account()
    test_corporate_pricing_applies_best_qualifying_tier()
    test_corporate_rate_tier_rejects_invalid_input()
    test_delivery_picks_the_correct_band()
    test_delivery_beyond_every_band_is_pending_not_guessed()
    test_delivery_enforces_minimum_order_when_configured()
    test_delivery_context_rejects_negative_values()
    test_recipe_costing_unconfigured_returns_pending()
    test_recipe_ingredient_rejects_invalid_input()
    test_packaging_unconfigured_returns_pending()
    test_customization_unconfigured_returns_pending()
    test_customization_context_rejects_invalid_colour_count()
    test_erp_port_not_connected_raises_not_implemented()
    test_erp_field_mapping_is_pure_and_generic()
    test_ai_quote_generator_not_configured_raises()
    print("OK")
