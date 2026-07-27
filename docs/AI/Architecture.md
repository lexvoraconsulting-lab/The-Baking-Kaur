# AI Vision Engine — Architecture

## Why this exists

The vision engine started as a single hardcoded script (`test_vision.py`) that called one local
Ollama model. It proved the concept — an image in, a text description out — but welded the
"mechanism" (which vision backend, which model, which URL) to the "content" (the prompt) in one
file. Nothing could change without editing code.

This phase introduces a provider abstraction so a second or third vision backend (Google Gemini,
OpenAI GPT-5 Vision, Claude, future local models) can be added later without touching any call
site — only by adding a new provider class and a config value.

## Shape

```
config (vision.json) → providers (VisionProvider / OllamaProvider / get_provider) → pipeline (run_vision_pipeline) → CLI (test_vision.py)
```

- **config** — one JSON file, one loader function. No hardcoded model/URL/paths anywhere.
- **providers** — `VisionProvider` is the abstract interface (`analyze(image_bytes, prompt, timeout) -> str`).
  `OllamaProvider` is the only concrete implementation today. `get_provider(cfg)` is a plain
  factory function that dispatches on `cfg["provider"]["name"]`.
- **pipeline** — orchestrates: load image, load prompt (with a documented fallback while the real
  prompt file is still an empty placeholder), call the configured provider, return its raw text.
- **CLI** — `test_vision.py` is a thin entrypoint: load config, run pipeline, print. No business
  logic lives here anymore.

## Non-goals (Phase 1)

This phase does not build a knowledge graph, vector search, batch processing, structured/validated
output, or any Shopify/marketing/JARVIS/ERP integration. Those are named in
[Roadmap.md](Roadmap.md) as future phases, not scaffolded as folders — there is no code for them
yet, and creating empty directories for them now would be speculative structure with no
responsibility to hold.

## Decision record

The actual architecture decision (why a provider abstraction, why JSON config, why a thin CLI) is
recorded in `docs/adr/2026-07-27-vision-provider-abstraction.md`, per this repo's "one decision,
one document" convention (see `docs/adr/` for prior ADRs). This document explains the resulting
system; it does not re-decide it.
