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


# --- OLLAMA_BASE_URL / OLLAMA_MODEL environment overrides ------------------

def test_env_overrides_absent_leaves_file_values():
    import os
    from ai.vision.python.config import apply_env_overrides
    for var in ("OLLAMA_BASE_URL", "OLLAMA_MODEL"):
        os.environ.pop(var, None)
    cfg = {"provider": {"name": "ollama", "url": "http://localhost:11434/api/generate",
                        "model": "qwen2.5vl:3b"}}
    out = apply_env_overrides(cfg)
    assert out["provider"]["url"] == "http://localhost:11434/api/generate"
    assert out["provider"]["model"] == "qwen2.5vl:3b"


def test_env_base_url_becomes_generate_endpoint():
    import os
    from ai.vision.python.config import apply_env_overrides
    os.environ["OLLAMA_BASE_URL"] = "http://127.0.0.1:11434"
    os.environ["OLLAMA_MODEL"] = "qwen3.5:4b"
    try:
        out = apply_env_overrides({"provider": {"name": "ollama", "url": "x", "model": "y"}})
        assert out["provider"]["url"] == "http://127.0.0.1:11434/api/generate", out
        assert out["provider"]["model"] == "qwen3.5:4b"
        assert out["provider"]["url_source"] == "OLLAMA_BASE_URL"
        assert out["provider"]["model_source"] == "OLLAMA_MODEL"
    finally:
        os.environ.pop("OLLAMA_BASE_URL", None)
        os.environ.pop("OLLAMA_MODEL", None)


def test_env_base_url_tolerates_trailing_slash():
    import os
    from ai.vision.python.config import apply_env_overrides
    os.environ["OLLAMA_BASE_URL"] = "http://127.0.0.1:11434/"
    try:
        out = apply_env_overrides({"provider": {"url": "x"}})
        assert out["provider"]["url"] == "http://127.0.0.1:11434/api/generate", out
    finally:
        os.environ.pop("OLLAMA_BASE_URL", None)


def test_env_override_does_not_mutate_caller_config():
    import os
    from ai.vision.python.config import apply_env_overrides
    os.environ["OLLAMA_MODEL"] = "qwen3.5:4b"
    try:
        original = {"provider": {"model": "qwen2.5vl:3b"}}
        apply_env_overrides(original)
        assert original["provider"]["model"] == "qwen2.5vl:3b", "caller config was mutated"
    finally:
        os.environ.pop("OLLAMA_MODEL", None)


def test_vision_json_contains_no_remote_host():
    """A tracked config file must never carry a deployment host."""
    import json
    cfg = json.load(open("ai/vision/config/vision.json", encoding="utf-8"))
    url = cfg["provider"]["url"]
    assert "localhost" in url or "127.0.0.1" in url, f"vision.json points at {url}"


# --- D-3 prompt-leakage screening (added 2026-08-20) -------------------------

def test_leak_detector_flags_exact_example_reproduction():
    from ai.vision.python.extraction import detect_prompt_leakage
    template = "Example: {\"observed\": \"a highly reflective poured mirror-glaze finish\"}"
    assert detect_prompt_leakage("a highly reflective poured mirror-glaze finish", template)
    assert detect_prompt_leakage("A Highly Reflective  Poured Mirror-Glaze Finish", template), \
        "casefold/whitespace normalization must still catch a reproduction"


def test_leak_detector_ignores_short_strings():
    """Vocabulary labels appear in the rendered prompt. Flagging them would
    suppress every correct enum value."""
    from ai.vision.python.extraction import detect_prompt_leakage
    template = "Colour Name: Red, Pink, White, Gold, Ivory"
    for label in ("White", "Rose Gold", "no lettering"):
        assert detect_prompt_leakage(label, template) is None, label


def test_leak_detector_screens_template_not_rendered_prompt():
    """The rendered prompt contains the taxonomy digest; the template does not."""
    from ai.vision.python.taxonomy_digest import build_digest, load_canonical_catalog, render_prompt
    from pathlib import Path
    from ai.vision.python.extraction import detect_prompt_leakage
    template = Path("ai/vision/prompts/extractor_v1.md").read_text(encoding="utf-8")
    rendered = render_prompt(template, build_digest(load_canonical_catalog()))
    genuine = "a smooth white buttercream base with a hand-piped shell border around the rim"
    assert detect_prompt_leakage(genuine, template) is None
    assert genuine not in rendered, "test string must not exist in the prompt"


def test_leaked_observation_never_enters_the_stream():
    from pathlib import Path
    from ai.vision.python.extraction import parse_extraction
    template = Path("ai/vision/prompts/extractor_v1.md").read_text(encoding="utf-8")
    leaked = "Every value you emit must be visibly supported by the photograph supplied with this request"
    payload = (
        '{"observations":[],"unmatched":[{"observed":"' + leaked + '",'
        '"why_unmatched":"x","suggested_kind":"term","suggested_label":"Leak"}]}'
    )
    result = parse_extraction(
        payload, image_id="TBK-0000000000000001", taxonomy_version="1.0", schema_version="v1",
        prompt_template=template,
    )
    assert result.unmatched == (), "leaked text must not become an unmatched observation"
    assert len(result.leaked) == 1
    assert result.leaked[0].classification == "prompt_leakage"
    assert result.leaked[0].excluded_from_discovery is True


def test_genuine_unmatched_observation_still_survives():
    """The fix must not suppress real discoveries - the whole point of the
    unmatched channel."""
    from pathlib import Path
    from ai.vision.python.extraction import parse_extraction
    template = Path("ai/vision/prompts/extractor_v1.md").read_text(encoding="utf-8")
    payload = (
        '{"observations":[],"unmatched":[{"observed":"a hand-piped royal icing lace collar '
        'around the upper rim of the middle tier","why_unmatched":"no term covers lace collars",'
        '"suggested_kind":"term","suggested_label":"Lace Collar","confidence":0.74}]}'
    )
    result = parse_extraction(
        payload, image_id="TBK-0000000000000001", taxonomy_version="1.0", schema_version="v1",
        prompt_template=template,
    )
    assert len(result.unmatched) == 1, "a genuine unmatched observation must survive screening"
    assert result.leaked == ()


if __name__ == "__main__":
    _CALLED = {
        "test_load_config", "test_get_provider_returns_ollama",
        "test_get_provider_rejects_unknown", "test_compute_image_id_is_deterministic",
        "test_pipeline_records_usage_when_pricing_unavailable",
    }
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

    # Auto-discover anything defined after this point too. The D-3 leakage
    # tests were originally appended below this block and silently never ran -
    # explicit call lists rot the moment a test is added.
    import inspect
    for _name, _fn in sorted(globals().items()):
        if not (_name.startswith("test_") and callable(_fn)) or _name in _CALLED:
            continue
        if inspect.signature(_fn).parameters:
            continue  # needs a fixture; the explicit block above handles those
        _fn()
        print(f"  ok  {_name}")
    print("ai.vision.python self-check passed")
