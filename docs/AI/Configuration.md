# AI Vision Engine — Configuration

`ai/vision/config/vision.json`:

```json
{
  "provider": {
    "name": "ollama",
    "model": "qwen2.5vl:3b",
    "url": "http://localhost:11434/api/generate",
    "timeout": 300
  },
  "schema_version": "v1",
  "taxonomy_version": "v1",
  "prompt_file": "ai/vision/prompts/extractor_v1.md",
  "schema_file": "ai/vision/schemas/tbk_image_schema_v1.json",
  "image_path": "ai/vision/images/1.png"
}
```

| Field | Meaning |
|---|---|
| `provider.name` | Which `VisionProvider` to construct (`get_provider` dispatches on this). Today only `"ollama"` is implemented. |
| `provider.model` | Model name passed to the provider. |
| `provider.url` | Provider API endpoint. |
| `provider.timeout` | Request timeout in seconds. |
| `schema_version` | Which `tbk_image_schema_v*.json` version this run's output is meant to conform to. Carried on every `VisionResult` now so nothing has to be retrofitted once structured-output parsing actually validates against it. |
| `taxonomy_version` | Same idea, for `taxonomy_v*.json`. |
| `prompt_file` | Path (relative to repo root) to the extraction prompt. Falls back to an inline prompt while this file is an empty placeholder — see [VisionPipeline.md](VisionPipeline.md). |
| `schema_file` | Path to the expected output schema. Not yet consumed by the pipeline (no structured-output parsing exists this phase) — reserved for when schema content is authored. |
| `image_path` | Path to the image to analyze. |

Both version fields are required keys, not optional — `config.py` raises `KeyError` if either is
missing, matching its "no silent defaults" stance for anything that must exist to run.

## Secrets: environment variables only, never in vision.json

`vision.json` is a tracked file in this repo. Ollama needs no credential, so this hasn't mattered
yet — it will the moment a cloud provider (Google Gemini, OpenAI, Claude, Azure OpenAI) is added,
since each requires an API key. That key must be read from an environment variable inside the new
provider class (`os.environ.get("GOOGLE_API_KEY")`, etc.) — the same pattern `seo-ops/` already
uses for `SHOPIFY_TOKEN`. Never add an `api_key` field to `vision.json` itself. If a config needs
to *name* which environment variable to read (e.g. to support multiple accounts), store the
variable's name as a string (`"api_key_env": "GOOGLE_API_KEY"`), never the key's value.

This section implements [VIG-007 (Quality Standard)](../00_Governance/VIG-007-Quality-Standard.md);
the versioning fields above implement [VIG-005 (Versioning Standard)](../00_Governance/VIG-005-Versioning-Standard.md).

## Why JSON, not YAML or TOML

No third-party config-format dependency exists anywhere in this repo, and there's no
requirements.txt to add one to. `ai/vision/schemas/` already uses `.json` for the taxonomy and
image schema files sitting in the same tree — using JSON for config too means one format, not
two, in this folder. `tomllib` is stdlib (Python 3.11+) but buys nothing over `json.load` for six
known keys, and this repo has no existing TOML usage to match.

## Adding a second environment or provider

Point `--config` at a different JSON file for a different environment. To add a new provider
(Google/OpenAI/Claude), add a new `VisionProvider` subclass in `providers.py`, a new branch in
`get_provider()`, and set `provider.name` to match — no changes to `pipeline.py` or
`test_vision.py`.
