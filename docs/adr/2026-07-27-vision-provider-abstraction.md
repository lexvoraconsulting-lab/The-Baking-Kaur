# ADR 0003: Vision Provider Abstraction

Date: 2026-07-27

## Status

Accepted

## Context

The first working AI artifact in this repo, `ai/vision/python/test_vision.py`, hardcoded a local
Ollama URL, model name, and image path in one 86-line script. It proved the vision-model loop
(image in, text description out) end-to-end, but coupled "call a vision model" to "which vision
model" — swapping backends meant editing code, not configuration.

The platform's stated direction requires supporting multiple vision providers over time (local
Ollama models today; Google Gemini, OpenAI GPT-5 Vision, and Claude are named future targets) with
no vendor lock-in. The prompt/schema content that will eventually drive structured extraction
(`ai/vision/prompts/extractor_v1.md`, `ai/vision/schemas/*.json`) does not exist yet — those files
are intentionally empty this phase, so no output-parsing contract is decided here either.

## Decision

Introduce a small provider abstraction, sized to the one concrete backend that exists today:

- `VisionProvider` (abstract base class, `ai/vision/python/providers.py`) defines a single method:
  `analyze(image_bytes, prompt, *, timeout) -> str`.
- `OllamaProvider(VisionProvider)` implements it with the existing base64-encode + HTTP POST logic,
  moved verbatim from the original script.
- `get_provider(cfg)` is a plain factory function (not a class-based registry) dispatching on
  `cfg["provider"]["name"]`. Adding Google/OpenAI/Claude later is one new class + one new branch.
- Configuration lives in `ai/vision/config/vision.json` — plain JSON (stdlib `json`, no PyYAML or
  tomllib dependency), matching the `.json` schema files already in this tree. One loader function,
  `load_config()`, with no validation library.
- `ai/vision/python/pipeline.py` orchestrates image/prompt loading and the provider call.
  `test_vision.py` becomes a thin CLI: load config, run pipeline, print result — no business logic.

No folders are created for future platform modules (knowledge graph, vector DB, search, Shopify
sync, marketing, JARVIS, ERP) — those have no code yet and are tracked as prose in
`docs/AI/Roadmap.md` only.

## Consequences

- Adding a new vision backend requires zero changes to `pipeline.py` or `test_vision.py` — only a
  new `VisionProvider` subclass, a new `get_provider` branch, and a config value.
- `analyze()` returns raw text (`str`), matching current behavior — it does not yet return
  structured/validated JSON, since the schema file that would define that contract is still an
  empty placeholder. Extending the return contract is deferred to the phase that authors
  `tbk_image_schema_v1.json`.
- `pipeline.py` falls back to an inline prompt when `extractor_v1.md` is empty, so the smoke test
  keeps working through this content-authoring gap; the fallback is marked for removal once the
  prompt file is authored (see `docs/AI/VisionPipeline.md`).
- Config is JSON, consistent with the schema files already in `ai/vision/schemas/` — no new
  third-party dependency was introduced.

## Notes

This ADR is the sole decision record for the Vision Engine's Phase 1 architecture, per this
repo's "one decision, one document" standing principle (CLAUDE.md). `docs/AI/Architecture.md`,
`FolderStructure.md`, `VisionPipeline.md`, `Configuration.md`, and `Roadmap.md` describe the
resulting system for day-to-day reference; they do not re-decide it.
