#!/usr/bin/env python3
"""
Self-check for config loading, the provider factory, and image-id
determinism - no network calls.

USAGE
  python -m ai.vision.python.test_config_providers
"""
from ai.vision.python.config import load_config
from ai.vision.python.pipeline import compute_image_id
from ai.vision.python.providers import OllamaProvider, get_provider


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


if __name__ == "__main__":
    test_load_config()
    test_get_provider_returns_ollama()
    test_get_provider_rejects_unknown()
    test_compute_image_id_is_deterministic()
    print("OK")
