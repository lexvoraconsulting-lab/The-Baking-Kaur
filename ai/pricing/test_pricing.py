#!/usr/bin/env python3
"""
Self-check for the Enterprise Pricing Service v1.

WHY
  Regenerates ai/pricing/schemas/*.schema.json from the Pydantic models (so
  the committed schema files can never drift from the code that defines
  them), validates every ai/pricing/config/*.json file against
  PricingConfigFileModel, then exercises the repository/strategy/service/
  audit flow end to end - including the two hard requirements this module
  exists to satisfy: token usage is always recorded even when pricing is
  unavailable, and the Audit Engine never imports pricing-configuration code.

USAGE
  python -m ai.pricing.test_pricing
"""
import ast
import json
import tempfile
from pathlib import Path

from ai.pricing.audit import AuditEngine
from ai.pricing.ids import compute_audit_id, compute_pricing_id
from ai.pricing.models import PriceComponent, PricingRecord, TokenUsage
from ai.pricing.models_pydantic import PricingConfigFileModel
from ai.pricing.repository import FileConfigPricingRepository
from ai.pricing.service import PricingService
from ai.pricing.strategy import StandardTokenCostStrategy

PRICING_DIR = Path(__file__).parent
CONFIG_DIR = PRICING_DIR / "config"
SCHEMAS_DIR = PRICING_DIR / "schemas"


def regenerate_schemas():
    SCHEMAS_DIR.mkdir(exist_ok=True)
    (SCHEMAS_DIR / "pricing_config.schema.json").write_text(
        json.dumps(PricingConfigFileModel.model_json_schema(), indent=2) + "\n"
    )


def test_every_config_file_validates():
    files = sorted(CONFIG_DIR.glob("*.json"))
    assert files, "no pricing config files found"
    for path in files:
        raw = json.loads(path.read_text(encoding="utf-8"))
        model = PricingConfigFileModel(**raw)
        assert model.provider == path.stem, f"{path.name}: provider field must match filename"
        assert model.records, f"{path.name}: at least one pricing record expected"


def test_pricing_id_is_deterministic():
    a = compute_pricing_id("openai", "gpt-4o", "example-2026-01", "2026-01-01")
    b = compute_pricing_id("openai", "gpt-4o", "example-2026-01", "2026-01-01")
    c = compute_pricing_id("openai", "gpt-4o", "example-2026-02", "2026-02-01")
    assert a == b
    assert a != c


def test_price_component_cost_for():
    per_million = PriceComponent(unit_price=10.0, unit="per_1m_tokens")
    assert per_million.cost_for(1_000_000) == 10.0
    assert per_million.cost_for(500_000) == 5.0
    per_token = PriceComponent(unit_price=0.001, unit="per_token")
    assert round(per_token.cost_for(10), 6) == 0.01


def test_repository_resolves_latest_by_default():
    repo = FileConfigPricingRepository(CONFIG_DIR)
    record = repo.get_pricing("openai", "gpt-4o")
    assert record is not None
    assert record.provider == "openai" and record.model == "gpt-4o"
    assert record.pricing_id  # populated by _record_from_dict, not blank


def test_repository_resolves_as_of_date():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "acme.json").write_text(json.dumps({
            "provider": "acme",
            "records": [
                {"provider": "acme", "model": "m1", "version": "v1", "effective_date": "2026-01-01",
                 "currency": "USD", "input_price": {"unit_price": 1.0}, "output_price": {"unit_price": 2.0}},
                {"provider": "acme", "model": "m1", "version": "v2", "effective_date": "2026-06-01",
                 "currency": "USD", "input_price": {"unit_price": 5.0}, "output_price": {"unit_price": 10.0}},
            ],
        }))
        repo = FileConfigPricingRepository(tmp_path)
        early = repo.get_pricing("acme", "m1", as_of="2026-03-01")
        assert early.version == "v1", "must resolve the rate active at the as-of date, not the latest"
        late = repo.get_pricing("acme", "m1", as_of="2026-12-01")
        assert late.version == "v2"
        missing = repo.get_pricing("acme", "does-not-exist")
        assert missing is None


def test_repository_missing_provider_returns_none_not_error():
    repo = FileConfigPricingRepository(CONFIG_DIR)
    assert repo.get_pricing("no-such-provider", "no-such-model") is None


def test_standard_strategy_calculates_multi_category():
    pricing = PricingRecord(
        provider="acme", model="m1", version="v1", effective_date="2026-01-01", currency="USD",
        input_price=PriceComponent(unit_price=1.0), output_price=PriceComponent(unit_price=2.0),
        categories={"cached": PriceComponent(unit_price=0.5)},
        pricing_id="test-id",
    )
    usage = TokenUsage(
        provider="acme", model="m1", input_tokens=1_000_000, output_tokens=500_000,
        cached_tokens=200_000, recorded_at="2026-01-15T00:00:00Z",
    )
    result = StandardTokenCostStrategy().calculate(usage, pricing)
    assert result.status == "calculated"
    assert result.breakdown["input"] == 1.0
    assert result.breakdown["output"] == 1.0
    assert result.breakdown["cached"] == 0.1
    assert round(result.total_cost, 4) == 2.1
    assert result.pricing_id == "test-id"
    assert result.pricing_version == "v1"


def test_strategy_skips_unpriced_categories_without_failing():
    pricing = PricingRecord(
        provider="acme", model="m1", version="v1", effective_date="2026-01-01", currency="USD",
        input_price=PriceComponent(unit_price=1.0), output_price=PriceComponent(unit_price=2.0),
    )
    usage = TokenUsage(
        provider="acme", model="m1", input_tokens=100, output_tokens=100,
        reasoning_tokens=999_999, recorded_at="2026-01-15T00:00:00Z",
    )
    result = StandardTokenCostStrategy().calculate(usage, pricing)
    assert "reasoning" not in result.breakdown, "no rate on file for reasoning - must be skipped, not guessed"
    assert result.status == "calculated"


def test_service_returns_calculated_when_pricing_exists():
    service = PricingService(repository=FileConfigPricingRepository(CONFIG_DIR))
    usage = TokenUsage(
        provider="ollama", model="qwen2.5vl:3b", input_tokens=500, output_tokens=200,
        recorded_at="2026-01-15T00:00:00Z",
    )
    result = service.calculate_cost(usage)
    assert result.status == "calculated"
    assert result.total_cost == 0.0  # ollama is local/free - a real $0, not a missing rate


def test_service_returns_pending_when_pricing_missing_not_an_exception():
    service = PricingService(repository=FileConfigPricingRepository(CONFIG_DIR))
    usage = TokenUsage(
        provider="totally-unknown-provider", model="totally-unknown-model",
        input_tokens=100, output_tokens=100, recorded_at="2026-01-15T00:00:00Z",
    )
    result = service.calculate_cost(usage)  # must not raise
    assert result.status == "pending_calculation"
    assert result.total_cost is None
    assert result.reason is not None


class _ExplodingRepository:
    def get_pricing(self, provider, model, as_of=None):
        raise RuntimeError("simulated repository failure")


def test_service_survives_repository_exception():
    service = PricingService(repository=_ExplodingRepository())
    usage = TokenUsage(
        provider="x", model="y", input_tokens=1, output_tokens=1,
        recorded_at="2026-01-15T00:00:00Z",
    )
    result = service.calculate_cost(usage)  # must not raise
    assert result.status == "pending_calculation"


def test_audit_engine_always_records_even_when_cost_is_pending():
    with tempfile.TemporaryDirectory() as tmp:
        log_path = Path(tmp) / "audit.jsonl"
        engine = AuditEngine(log_path)
        usage = TokenUsage(
            provider="unknown", model="unknown", input_tokens=10, output_tokens=5,
            recorded_at="2026-01-15T00:00:00Z",
        )
        pending = PricingService(repository=FileConfigPricingRepository(CONFIG_DIR)).calculate_cost(usage)
        record = engine.record(usage, pending)

        assert record.usage.input_tokens == 10, "usage must be recorded regardless of cost status"
        assert record.cost.status == "pending_calculation"
        assert log_path.exists()
        lines = log_path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1
        persisted = json.loads(lines[0])
        assert persisted["usage"]["input_tokens"] == 10
        assert persisted["cost"]["status"] == "pending_calculation"


def test_audit_id_is_deterministic():
    a = compute_audit_id("p", "m", "2026-01-01T00:00:00Z", 10, 5, None)
    b = compute_audit_id("p", "m", "2026-01-01T00:00:00Z", 10, 5, None)
    c = compute_audit_id("p", "m", "2026-01-01T00:00:00Z", 10, 6, None)
    assert a == b
    assert a != c


def test_audit_engine_does_not_import_pricing_configuration_machinery():
    """Structural enforcement of 'the Audit Engine must never depend directly
    on pricing configuration' - parses audit.py's own import statements
    rather than trusting a docstring promise."""
    source = (PRICING_DIR / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)

    forbidden = {"ai.pricing.repository", "ai.pricing.strategy", "ai.pricing.service"}
    leaked = forbidden & imported_modules
    assert not leaked, f"audit.py must not import {leaked} - Audit Engine must not depend on pricing config"


if __name__ == "__main__":
    regenerate_schemas()
    test_every_config_file_validates()
    test_pricing_id_is_deterministic()
    test_price_component_cost_for()
    test_repository_resolves_latest_by_default()
    test_repository_resolves_as_of_date()
    test_repository_missing_provider_returns_none_not_error()
    test_standard_strategy_calculates_multi_category()
    test_strategy_skips_unpriced_categories_without_failing()
    test_service_returns_calculated_when_pricing_exists()
    test_service_returns_pending_when_pricing_missing_not_an_exception()
    test_service_survives_repository_exception()
    test_audit_engine_always_records_even_when_cost_is_pending()
    test_audit_id_is_deterministic()
    test_audit_engine_does_not_import_pricing_configuration_machinery()
    print("OK")
