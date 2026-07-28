# Development Environment Setup

Canonical bootstrap for this repository's Python code (`ai/eal`, `ai/ear`, `ai/ead`,
`ai/attribute_distribution`, `ai/vision`). `requirements.txt` at the repo root is the canonical
dependency list — install from it, don't hand-install packages ad hoc.

## Bootstrap

```bash
# from the repo root
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Verify the environment

```bash
python -c "import pydantic, yaml, requests; print('OK')"

python -m ai.eal.test_eal
python -m ai.ear.test_ear
python -m ai.ead.test_ead
python -m ai.vision.python.test_config_providers
```

Every command above should print `OK` and exit 0, with no network access required — these are all
offline self-checks (see each module's own `test_*.py` module docstring).

## Running the Vision Engine

```bash
python -m ai.vision.python.test_vision
```

This one **does** need a real Ollama server reachable at the URL in `ai/vision/config/vision.json`
(default `http://localhost:11434`) — it is the only command here with an external runtime
dependency. If Ollama isn't running, this hangs/fails at "Sending image to provider..." — that's
expected and is not an environment problem; every command in the "Verify" section above runs fully
offline and is the actual gate for confirming the Python environment itself is sound.

## What's in `requirements.txt` and why

| Package | Used by | Why |
|---|---|---|
| `pydantic` | `ai/eal`, `ai/ear`, `ai/ead`, `ai/attribute_distribution` | Runtime validation + JSON Schema generation for every module's `models_pydantic.py` |
| `PyYAML` | same modules' `loader.py`/`exporter.py`/`test_*.py` | YAML example files alongside JSON ones |
| `requests` | `ai/vision/python/providers.py` | `OllamaProvider`'s HTTP client (ADR 0003) |

No other third-party dependency exists anywhere in this codebase — everything else is Python
standard library. Do not add a new dependency for what a few lines of stdlib can do
(`docs/CODING_STANDARDS.md`).
