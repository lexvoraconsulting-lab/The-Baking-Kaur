# AI Vision Engine — Roadmap

## Phase 1 (this work)

- Provider abstraction (`VisionProvider` / `OllamaProvider` / `get_provider`).
- Config-driven pipeline (`config/vision.json`, no hardcoded model/URL/paths).
- `test_vision.py` reduced to a thin CLI entrypoint; all business logic moved into
  `config.py` / `providers.py` / `pipeline.py`.
- `.gitignore` guard so future sample images aren't silently accumulated in git.

## Phase 2+ (not built yet — content and capability work)

- Author real content for `ai/vision/prompts/extractor_v1.md`,
  `ai/vision/schemas/taxonomy_v1.json`, and `ai/vision/schemas/tbk_image_schema_v1.json`.
- Parse the provider's response into structured JSON validated against the schema, instead of
  returning raw text.
- Additional `VisionProvider` implementations: `GoogleProvider` (Gemini), `OpenAIProvider`
  (GPT-5 Vision), `ClaudeProvider`.
- A batch pipeline that runs the vision extraction over the full product catalogue rather than
  one image at a time.
- `docs/AI/PROJECT_CONSTITUTION.md` gets authored once the platform's guiding principles are
  finalized.

## Explicitly deferred — documented here, not scaffolded as folders

The long-term "TBK Intelligence Platform" ambition includes a Product Genome, Knowledge Graph,
vector search, Shopify sync automation, marketing automation, a JARVIS-style orchestration layer,
and ERP integration. None of these have any code today. Per this repo's own architecture
guidance ("do NOT create empty folders without justification"), no `knowledge_graph/`,
`vector_db/`, `search/`, `shopify/`, `marketing/`, `jarvis/`, or `erp/` folders exist yet — they
are named here as future direction only, and will be scaffolded when a phase actually implements
the first piece of one.
