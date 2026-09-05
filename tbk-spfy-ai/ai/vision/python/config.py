"""
Vision pipeline config loader.

WHY
  Nothing in this repo hardcodes model names, URLs, or paths per CLAUDE.md's
  configuration guidance. One function, plain JSON (stdlib only - no PyYAML/
  tomllib dependency to add for 6 known keys, and this folder already uses
  .json for the schema files next to it).

ENVIRONMENT OVERRIDES (OLLAMA_BASE_URL / OLLAMA_MODEL)
  The inference runtime is NOT the machine this repository is edited on. The
  same code runs against a local Ollama during development and against the
  deployment host's Ollama in production, and the difference must not be a
  code change or a tracked-file edit.

  vision.json therefore keeps a localhost default and NEVER contains a remote
  host. Deployment supplies:

      OLLAMA_BASE_URL=http://127.0.0.1:11434
      OLLAMA_MODEL=qwen3.5:4b

  Both values are read here, at the single point every caller already flows
  through (providers.get_provider, pipeline.run_vision_pipeline and
  cake_genome.run_phase1 all read cfg["provider"][...] and nothing else).

WHY 127.0.0.1 IS THE CORRECT VALUE IN BOTH PLACES
  On the deployment host the pipeline runs beside Ollama, so 127.0.0.1 is
  literally correct and port 11434 stays unexposed. For local development the
  same value is correct through an SSH tunnel:

      ssh -N -L 11434:127.0.0.1:11434 <user>@<host>

  One config, two environments, no public endpoint and no credential in a
  tracked file. This mirrors the SHOPIFY_TOKEN convention seo-ops already
  uses, and Configuration.md's existing rule: secrets and environment-specific
  values come from the environment, never from vision.json.
"""
import json
import os
from pathlib import Path

ENV_BASE_URL = "OLLAMA_BASE_URL"
ENV_MODEL = "OLLAMA_MODEL"

# Ollama's generate endpoint. OLLAMA_BASE_URL is a BASE (scheme://host:port),
# matching `curl $OLLAMA_BASE_URL/api/tags` usage; the path is appended here so
# no caller has to know it and no environment has to repeat it.
_GENERATE_PATH = "/api/generate"


def apply_env_overrides(cfg: dict) -> dict:
    """Overlay OLLAMA_BASE_URL / OLLAMA_MODEL onto a loaded config.

    Returns a new dict - the caller's config is never mutated in place, so a
    test or a second load is unaffected by a previous call. An unset variable
    leaves the file value untouched; an empty one is treated as unset rather
    than as a request to blank a required field.
    """
    provider = dict(cfg.get("provider") or {})
    base_url = (os.environ.get(ENV_BASE_URL) or "").strip()
    model = (os.environ.get(ENV_MODEL) or "").strip()

    if base_url:
        provider["url"] = base_url.rstrip("/") + _GENERATE_PATH
        provider["url_source"] = ENV_BASE_URL
    if model:
        provider["model"] = model
        provider["model_source"] = ENV_MODEL

    merged = dict(cfg)
    merged["provider"] = provider
    return merged


def load_config(path: str | Path = "ai/vision/config/vision.json") -> dict:
    """Read and return the vision pipeline config. Raises FileNotFoundError /
    json.JSONDecodeError on bad input - no silent defaults for a config file
    that must exist to run anything.

    Environment overrides are applied after the file is read, so a deployment
    never has to edit (or accidentally commit) a host-specific vision.json.
    """
    with open(path) as f:
        return apply_env_overrides(json.load(f))


def describe_runtime(cfg: dict) -> str:
    """One line naming the endpoint and model actually in use, and where each
    came from. Printed by the runner so a run's target is never ambiguous in a
    log - the failure mode this prevents is a 'passing' regression that
    silently hit the wrong host or the wrong model."""
    provider = cfg.get("provider") or {}
    url_src = provider.get("url_source", "vision.json")
    model_src = provider.get("model_source", "vision.json")
    return (f"{provider.get('url')} [{url_src}] "
            f"model={provider.get('model')} [{model_src}]")
