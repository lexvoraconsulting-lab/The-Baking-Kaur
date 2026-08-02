#!/usr/bin/env python3
"""
Self-check for config loading, the provider factory, image-id determinism,
and end-to-end token-usage/cost wiring through run_vision_pipeline - no
network calls (a stub VisionProvider stands in for OllamaProvider).

USAGE
  python -m ai.vision.python.test_config_providers
"""
import tempfile
from pathlib import Path

from ai.vision.python import pipeline as pipeline_module
from ai.vision.python.config import load_config
from ai.vision.python.pipeline import compute_image_id, run_vision_pipeline
from ai.vision.python.providers import OllamaProvider, ProviderResponse, VisionProvider, get_provider


def test_load_config():
    cfg = load_config()
    assert "provider" in cfg
    assert cfg["provider"]["name"] == "ollama"
    assert "schema_version" in cfg
    assert "taxonomy_version" in cfg


def test_get_provider_returns_ollama():
    cfg = {"provider": {"name": "ollama", "url": "http://x", "model": "m"}}
    provider = get_provider(cfg)
    assert isinstance(provider, OllamaProvider)


def test_get_provider_rejects_unknown():
    cfg = {"provider": {"name": "does-not-exist"}}
    try:
        get_provider(cfg)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_compute_image_id_is_deterministic():
    a = compute_image_id(b"same bytes")
    b = compute_image_id(b"same bytes")
    c = compute_image_id(b"different bytes")
    assert a == b
    assert a != c
    assert a.startswith("TBK-")


class _StubProvider(VisionProvider):
    """Deterministic stand-in for OllamaProvider - proves the pipeline wires
    a provider's token counts into TokenUsage/CostResult without needing a
    live Ollama server."""

    def analyze(self, image_bytes: bytes, prompt: str, *, timeout: int) -> ProviderResponse:
        return ProviderResponse(text="a fake cake description", input_tokens=123, output_tokens=45)


def test_pipeline_wires_token_usage_and_cost(monkeypatch):
    monkeypatch.setattr(pipeline_module, "get_provider", lambda cfg: _StubProvider())

    with tempfile.TemporaryDirectory() as tmp:
        prompt_path = Path(tmp) / "prompt.md"
        prompt_path.write_text("describe the cake")
        image_path = Path(__file__).resolve().parents[1] / "images" / "1.png"

        cfg = {
            "image_path": str(image_path),
            "prompt_file": str(prompt_path),
            "schema_version": "v1",
            "taxonomy_version": "v1",
            "provider": {"name": "ollama", "model": "qwen2.5vl:3b", "url": "http://x", "timeout": 5},
        }
        result = run_vision_pipeline(cfg)

    assert result.response == "a fake cake description"
    assert result.token_usage.input_tokens == 123
    assert result.token_usage.output_tokens == 45
    assert result.token_usage.provider == "ollama"
    # ollama.json prices this model at $0 - a real calculated cost, not Pending.
    assert result.cost.status == "calculated"
    assert result.cost.total_cost == 0.0


def test_pipeline_records_pending_cost_for_unpriced_model_without_failing(monkeypatch):
    monkeypatch.setattr(pipeline_module, "get_provider", lambda cfg: _StubProvider())

    with tempfile.TemporaryDirectory() as tmp:
        prompt_path = Path(tmp) / "prompt.md"
        prompt_path.write_text("describe the cake")
        image_path = Path(__file__).resolve().parents[1] / "images" / "1.png"

        cfg = {
            "image_path": str(image_path),
            "prompt_file": str(prompt_path),
            "schema_version": "v1",
            "taxonomy_version": "v1",
            "provider": {"name": "ollama", "model": "a-model-with-no-rate-card", "url": "http://x", "timeout": 5},
        }
        result = run_vision_pipeline(cfg)  # must not raise

    assert result.response == "a fake cake description"
    assert result.token_usage.input_tokens == 123, "usage recorded even though pricing is unavailable"
    assert result.cost.status == "pending_calculation"
    assert result.cost.reason is not None


if __name__ == "__main__":
    test_load_config()
    test_get_provider_returns_ollama()
    test_get_provider_rejects_unknown()
    test_compute_image_id_is_deterministic()

    class _Monkeypatch:
        def setattr(self, obj, name, value):
            setattr(obj, name, value)

    test_pipeline_wires_token_usage_and_cost(_Monkeypatch())
    test_pipeline_records_pending_cost_for_unpriced_model_without_failing(_Monkeypatch())
    print("OK")
