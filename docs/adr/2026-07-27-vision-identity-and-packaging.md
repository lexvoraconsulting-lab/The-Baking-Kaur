# ADR 0004: Vision Engine Identity, Versioning, and Packaging Hardening

Date: 2026-07-27

## Status

Accepted

## Context

`docs/AI/ARCHITECTURE_REVIEW_AR001.md` reviewed the Phase 1 Vision Engine (ADR 0003) as a sound
foundation — **GO** — but flagged three gaps worth closing before other modules (Shopify AI, an
embeddings pipeline, a Knowledge Graph, JARVIS-style orchestration) start depending on this one:

1. `ai/vision/python/` is a directory of scripts, not an importable package — its bare imports
   (`from providers import get_provider`) only resolve because Python auto-adds a running script's
   own directory to `sys.path`. No other module in the repo could import this one.
2. No per-image identifier exists. Every future module the roadmap names needs a stable key to
   join its output back to a specific image; retrofitting one after volume exists is materially
   harder than adding it now, while exactly one image is in play.
3. Nothing documents that provider secrets (future Gemini/OpenAI/Claude/Azure API keys) must come
   from environment variables rather than the committed `vision.json` — no secret exists yet
   (Ollama is unauthenticated), so this is free to close before it becomes a real mistake.

## Decision

- **Packaging**: `ai/`, `ai/vision/`, and `ai/vision/python/` each get an empty `__init__.py`,
  making `ai.vision.python` a real, importable package. Internal imports switch to package-
  qualified form (`from ai.vision.python.providers import get_provider`). The CLI is now invoked as
  `python -m ai.vision.python.test_vision` from the repo root, not as a bare script path.
- **Identity**: `compute_image_id(image_bytes) -> str` (`ai/vision/python/pipeline.py`) derives
  `TBK_IMAGE_ID` from a SHA-256 content hash (`"TBK-" + hexdigest[:16]`), not a random UUID or a
  stateful counter. Reprocessing the same image file always yields the same ID, with no registry
  or database required to guarantee that. `run_vision_pipeline`'s return type changes from a bare
  `str` to a frozen `VisionResult` dataclass carrying `image_id`, `image_path`, `schema_version`,
  `taxonomy_version`, `provider_name`, `model`, and `response` together.
- **Versioning**: `vision.json` gains required `schema_version`/`taxonomy_version` fields (both
  `"v1"` today, matching the existing `_v1` schema/taxonomy filenames), read straight through with
  no defensive default — consistent with `config.py`'s existing "no silent defaults" stance.
- **Secrets convention**: documented in `docs/AI/Configuration.md` — provider API keys are read
  from environment variables inside the provider class, matching `seo-ops/`'s existing
  `os.environ.get("SHOPIFY_TOKEN")` pattern, and are never written into `vision.json`.

## Consequences

- Any future module elsewhere in the repo can `from ai.vision.python.pipeline import
  run_vision_pipeline` without `sys.path` workarounds.
- Every `VisionResult` now carries a stable, deterministic image identity and the schema/taxonomy
  version it was produced against — nothing has to be reconstructed or backfilled onto past
  extractions once structured-output parsing and persistence are built in a later phase.
- No cloud-provider API key can accidentally end up committed to git via the established config
  pattern, because the pattern for where a key lives was decided before the first key existed.
- These changes are additive to the Phase 1 design (ADR 0003) — no provider logic, config-format
  choice, or module boundary from that ADR was revisited or reversed.

## Notes

This ADR responds to `docs/AI/ARCHITECTURE_REVIEW_AR001.md` §13 (Required Changes 13.1–13.3) in
full. It does not implement §14/§15 (Recommended/Nice-to-have improvements — logging, retries,
provenance records, multi-environment config) or any Phase 2 capability (batch runner, second
provider, structured-output parsing, persistence, embeddings) — those remain future work per
`docs/AI/Roadmap.md`.
