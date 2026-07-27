# AR-001: Vision Engine Phase 1 — Architecture Review

Date: 2026-07-27
Reviewers: Principal Software Architect / Principal AI Architect / Enterprise Solution Architect /
Staff Python Engineer / Data Architect / Knowledge Graph Architect / MLOps Architect /
AI Infrastructure Architect / Enterprise Code Reviewer / Technical Product Architect (single
combined pass — see Notes)
Scope reviewed: `ai/vision/python/{config,providers,pipeline,test_vision,test_config_providers}.py`,
`ai/vision/config/vision.json`, `ai/vision/{prompts,schemas,images}/`, `docs/AI/*.md`,
`docs/adr/2026-07-27-vision-provider-abstraction.md`

---

## 1. Executive Summary

Phase 1 delivers exactly what it set out to deliver: a hardcoded, one-file Ollama script has become
a four-module design (`config → providers → pipeline → CLI`) behind a `VisionProvider` interface.
The separation of concerns is real, not decorative — each module has one job, dependencies point
one direction, and no module reaches past its boundary. For what it is scoped to be (a config-driven
single-image smoke test with room for more providers), it is sound.

It is **not**, and was never meant to be, a system ready for 50,000 images, embeddings, a knowledge
graph, or Shopify field generation — none of that exists, and none of it should yet. The risk this
review is looking for is not "is Phase 2 missing" (it is, correctly), but "did Phase 1 make a choice
that will force a rewrite when Phase 2 arrives." On that question: **mostly no**, with two concrete
exceptions detailed below (import portability, missing image identity) that are cheap to fix now and
expensive to retrofit once other modules depend on this one.

**Recommendation: GO.** Phase 1 is approved as the foundation, conditional on the two Required
Changes in §13 landing before Phase 2 cross-module work begins.

---

## 2. Repository Review

- **Folder hierarchy**: `ai/vision/{python,config,prompts,schemas,images}` — flat, one level deep,
  each folder single-purpose. No speculative folders (`knowledge_graph/`, `vector_db/`, etc.) exist,
  which is correct: they have no code and would be empty structure with no tenant.
- **Package structure**: `ai/vision/python/` is a directory of scripts, not a Python package — no
  `__init__.py`, imports are bare (`from providers import get_provider`). This works today because
  Python prepends the running script's own directory to `sys.path`. It will **not** work the moment
  any file outside `ai/vision/python/` needs to import `run_vision_pipeline` or `get_provider` — and
  the stated roadmap (Shopify AI, SEO AI, JARVIS) is entirely built on other modules calling into this
  one. See §13, Required Change 1.
- **Naming conventions**: consistent — `snake_case` modules, `PascalCase` classes, no abbreviations
  that need decoding (`VisionProvider`, `OllamaProvider`, `get_provider`, `load_config`,
  `run_vision_pipeline`).
- **Module boundaries / separation of concerns**: clean. `config.py` knows only about reading JSON.
  `providers.py` knows only about talking to a specific vision backend. `pipeline.py` knows only
  about orchestration order. `test_vision.py` knows only about CLI plumbing. No module imports
  "sideways" or reaches into another's internals.
- **Dependency direction**: strictly `test_vision.py → pipeline.py → providers.py`, and
  `test_vision.py → config.py`. No cycles, no reverse dependencies.
- **Configuration strategy**: single JSON file, no secrets in it today. See §5 for the gap that
  matters once cloud providers arrive.

---

## 3. Vision Engine Review

| Component | Assessment |
|---|---|
| `providers.py` | ABC + one concrete class + a factory function. SOLID-compliant: `OllamaProvider` can be replaced or extended without modifying callers (Open/Closed); the interface is one method, so no class is forced to implement behavior it doesn't need (Interface Segregation). |
| `pipeline.py` | Orchestration only — no HTTP calls, no config parsing leak from `config.py`. The empty-prompt fallback is explicit and commented (`ponytail:` marker), not a silent behavior change. |
| `config.py` | One function, stdlib-only. No validation library — acceptable at 6 known keys; will need a real schema check (or at minimum a required-keys assertion) once the number of providers/fields grows past what a `KeyError` explains clearly. |
| `vision.json` | Flat, readable, no nesting beyond one level. Does not yet anticipate multi-environment or per-provider secrets (see §5). |
| `test_vision.py` | Thin as required — argparse, load, run, print. Zero business logic. |
| `test_config_providers.py` | Covers the one branching piece of logic that exists (`get_provider`'s dispatch) plus config shape. Does not cover `pipeline._load_prompt`'s fallback branch — minor gap, not blocking. |
| Error handling | `FileNotFoundError` on missing image, `ValueError` on unknown provider, `response.raise_for_status()` on HTTP failure — all fail loudly and specifically, no silent swallowing. Appropriate for a CLI tool; insufficient for a batch/production runner (no retry, no partial-failure handling) — correctly out of scope until a batch runner exists. |
| Logging | `print()` only, matching the `seo-ops/` convention. Fine for a single-image CLI; will need real leveled logging the moment a batch pipeline processes hundreds of images, so failures are attributable to a specific image, not lost in stdout. |
| Dependency injection | Not present, not needed — `get_provider(cfg)` is a factory, which is the right amount of indirection for 1–4 providers. A full DI container would be an unrequested abstraction at this scale. |
| Testing | Assert-based, no framework, matches repo convention. Appropriately minimal — this is not a gap, it's the right amount of test for the amount of logic that exists. |

---

## 4. AI Provider Review — "Adding Gemini should require one class, one config entry, nothing else"

**Verified true for the mechanism, not yet true for secrets.**

Adding `GoogleProvider(VisionProvider)`:
- ✅ One new class in `providers.py`.
- ✅ One new `elif name == "google":` branch in `get_provider`.
- ✅ One new `provider.name` value in `vision.json`.
- ⚠️ **Gap**: Gemini/OpenAI/Claude/Azure all require an API key. `vision.json` is a committed file
  (tracked in git). If a future engineer follows the existing pattern and puts
  `"api_key": "sk-..."` directly into `vision.json`, that key ships to git history permanently.
  Ollama needed no such field, so this gap is invisible today — it will not be invisible the day
  someone adds the second provider under time pressure.
- **Fix is additive, not a redesign**: document now (before Gemini/OpenAI/Claude land) that provider
  secrets are read from environment variables — matching the exact pattern `seo-ops/` already uses
  (`os.environ.get("SHOPIFY_TOKEN")`) — never placed in `vision.json`. See §13, Required Change 2.

**Google Gemini readiness specifically**: yes, mechanically ready. `VisionProvider.analyze()`'s
signature (`image_bytes: bytes, prompt: str, timeout: int → str`) maps cleanly onto Gemini's
`generate_content([image, prompt])` call shape — no interface change needed, only a new class whose
internals build a Gemini request instead of an Ollama one.

---

## 5. Configuration Review

- No secrets exist yet (Ollama is unauthenticated localhost), so there is no live vulnerability —
  but there is also no documented convention steering the next contributor away from creating one.
- Single environment, single file. No `--env` concept, no per-environment override layering. Not
  needed yet (one deployment target: local Ollama) but worth naming as a Phase 2 concern once a
  second environment (e.g. a cloud provider used in CI vs. local Ollama used in dev) exists.
- JSON over YAML/TOML was the right call for zero-dependency stdlib config at this size (see ADR
  0003) — do not revisit this unless the config genuinely needs comments or multi-document
  structure, neither of which is true today.

---

## 6. Data Architecture Review

- Current data flow: one image path (string) → one raw text response (string). No identifier
  survives the round-trip.
- **Gap**: `docs/AI/PROJECT_CONSTITUTION.md`'s stated principle (per the original mission brief)
  is "every image receives a `TBK_IMAGE_ID`." No such identifier is assigned, generated, or threaded
  through `pipeline.py` today. This is the single most important data-architecture gap relative to
  the 5-year vision: a Knowledge Graph, embeddings store, and Shopify sync all need a stable key to
  join vision output back to a specific product image. Retrofitting an ID after thousands of images
  have been processed without one means either reprocessing or fragile path-based matching later.
  See §13, Required Change 3.
- Provenance/versioning: nothing records which prompt version, schema version, or model version
  produced a given response. Not urgent while there is exactly one prompt (empty) and one model —
  becomes necessary the moment `extractor_v1.md` gets a `v2`, so a past extraction can be traced to
  the prompt that generated it. Flagged as a Recommended Improvement (§14), not required now.

---

## 7. Cake Genome Readiness

Not built, and correctly not built — the schema (`tbk_image_schema_v1.json`) is an intentional empty
placeholder this phase. What's worth confirming is whether today's *shape* blocks tomorrow's content:

- **Structured JSON output**: `analyze()` returns `str`. When the extractor prompt is authored to
  request JSON, parsing happens in `pipeline.py` (or a new module above it) — not inside
  `providers.py`. This is the correct boundary: providers stay "dumb pipes" to a model, and schema
  interpretation lives above them. No redesign needed, only addition.
- **Versioned schemas**: filename already carries `_v1` (`taxonomy_v1.json`, `tbk_image_schema_v1.json`,
  `extractor_v1.md`) — a `_v2` can sit alongside without touching code, only a config value change.
  Sound.
- **Confidence scores / human verification / provenance**: none of this has a home yet, because
  there is no structured output yet to attach them to. Not a defect — a dependency ordering. Will
  need a small "extraction record" shape (image id, schema version, raw output, parsed output,
  confidence, verified-by) once structured output exists. Recommended Improvement, not required now.
- **Embeddings / similarity search**: entirely absent, correctly so — nothing upstream (structured
  attributes) exists yet to embed.

---

## 8. Knowledge Graph Readiness

The current data flow (image path in, text out, printed to stdout) has no persistence layer at all —
nothing is written anywhere. This is fine for a smoke test and is not a defect of Phase 1. It does
mean the Knowledge Graph has literally nothing to read from yet. The dependency chain is: **image
identity (§6) → structured output (§7) → persistence → graph ingestion** — Phase 1 correctly stops
before any of that, having built the first thing (a working extraction call) that everything else
depends on.

---

## 9. Shopify Readiness

Same answer as §8: no persistence, no structured fields, so nothing exists yet to map to Shopify's
`title`/`seo.title`/`alt text`/tags. Correctly out of scope — the mission explicitly says do not
implement this. Nothing in the current design blocks it later: whatever eventually parses structured
JSON out of the vision response can just as easily emit a dict shaped for Shopify's fields as for a
knowledge graph node. No premature coupling to Shopify exists in `providers.py`/`pipeline.py` today
(good — the ADR 0002 principle of keeping mechanism domain-agnostic is being honored here too, just
in Python instead of Liquid).

---

## 10. Enterprise Readiness

| Area | Status | Verdict |
|---|---|---|
| Configuration | Single JSON file, no secrets handling documented | Adequate for Phase 1; gap flagged §5/§13 |
| Secrets | None exist yet | No live issue; convention needed before first cloud provider |
| Environment variables | Not used yet (no secrets to hold) | Fine — nothing to configure this way today |
| Logging | `print()` only | Adequate for CLI; insufficient for batch/production (expected, deferred) |
| Testing | Assert-based, no framework | Matches repo convention; right-sized for current logic |
| Packaging | No `pyproject.toml`/`setup.py` anywhere in repo | Not urgent alone; compounds with the import-portability gap (§13) |
| CI/CD | None exists for Python anywhere in repo | Out of scope for Phase 1; note for Phase 2 once a batch runner exists to actually gate |
| Git workflow | Clean — `.gitignore` guards future image sprawl, docs/ADR follow existing repo conventions | Good |
| Dependency management | `requests` is the only third-party dependency, undeclared (matches `seo-ops/` convention of no requirements.txt) | Acceptable at 1 dependency; revisit once Google/OpenAI/Claude SDKs are added (3-4 new dependencies is where "no requirements file" starts to hurt) |
| Error recovery | Fail-fast, no retries | Correct for a manual CLI smoke test; required before batch/production use |
| Monitoring | None | Not applicable yet — nothing is running unattended |

---

## 11. Scalability Review

| Volume | Verdict |
|---|---|
| 1 image (today) | Works as-is. |
| 1,200 images | Works if run in a loop calling `run_vision_pipeline` per image — but nothing today provides that loop; `test_vision.py` handles exactly one image per invocation. Needs a thin batch-runner script (iterate a directory or a list of paths, call the existing pipeline per item). This is additive — it does not change `providers.py`, `pipeline.py`, or the `VisionProvider` interface. |
| 50,000 images | The additive batch runner from the row above will be too slow run serially with `timeout=300`-second HTTP calls. Needs concurrency (a thread pool or async HTTP) at the batch-runner layer, plus real logging (per-image success/failure, not stdout prints) and retry/backoff for transient failures. Still does not require changing the provider interface — `VisionProvider.analyze()` can remain a synchronous per-item call wrapped by a concurrent orchestrator above it. |
| Millions of images | Needs the above plus a persistence layer (results can't live in stdout), likely a job queue rather than a single long-running script, and almost certainly a hosted/batched provider API rather than one request per image to a local Ollama instance. This is squarely Phase 2+/3+ territory — nothing about it is blocked by today's design, but nothing about it exists yet either. |

**Bottom line**: the provider/pipeline boundary was drawn correctly — scaling is a matter of adding a
concurrent batch orchestrator *around* `run_vision_pipeline`, not rewriting it. The two things that
would be genuinely painful to retrofit at 50,000+ images are the two flagged as Required Changes: a
stable image identity (§6) and an importable package structure (§13) so a batch runner living
elsewhere in the repo can actually call this code.

---

## 12. Risks

1. **Import portability** (High, cheap to fix, expensive to defer) — see §13.1.
2. **No image identity** (High, cheap to fix now, expensive once volume grows) — see §13.2.
3. **Secrets-in-config convention undocumented** (Medium, zero cost to document now, real cost if a
   real API key gets committed) — see §13.3.
4. **No dependency manifest** (Low today, compounds as more provider SDKs are added) — recommended,
   not required, at 1 dependency.
5. **`get_provider`'s `if/elif` chain** (Low) — fine through 4-5 providers; becomes a minor readability
   tax past that. Convert to a `dict` registry only when it actually gets long, not preemptively.

---

## 13. Required Changes (before Phase 2 cross-module work begins)

**13.1 — Make `ai/vision/python/` importable as a package.**
Today's bare imports (`from providers import get_provider`) only resolve because Python auto-adds
the running script's own directory to `sys.path`. Any future module elsewhere in the repo (a
Shopify sync script, a batch runner, JARVIS) that tries `from ai.vision.python.pipeline import
run_vision_pipeline` will fail. Fix: add `ai/vision/python/__init__.py` (and `ai/vision/__init__.py`,
`ai/__init__.py`) and switch internal imports to package-qualified form
(`from ai.vision.python.providers import get_provider`), with `test_vision.py` still runnable via
`python -m ai.vision.python.test_vision` from the repo root. This is a mechanical, low-risk change
that costs nothing today and blocks nothing — it only prevents a guaranteed breakage the day a
second module needs this one.

**13.2 — Introduce a stable per-image identifier.**
Add an `image_id` (or `TBK_IMAGE_ID`, matching the original mission's naming) generated or assigned
alongside `image_path`, threaded through `run_vision_pipeline`'s return value (e.g. return
`{"image_id": ..., "response": ...}` instead of a bare `str`, or a small dataclass). This is the one
change to `pipeline.py`'s return contract worth making before real volume arrives — retrofitting an
identity scheme after thousands of un-keyed extractions exist is materially harder than adding it now.

**13.3 — Document the secrets convention before adding the first cloud provider.**
One paragraph in `docs/AI/Configuration.md`: provider API keys are read from environment variables
(matching `seo-ops/`'s `os.environ.get("SHOPIFY_TOKEN")` pattern), never placed in `vision.json`.
Zero code changes needed today (no provider needs a key yet) — this is purely closing the door
before someone walks through it under deadline pressure.

---

## 14. Recommended Improvements (do when the triggering condition arrives, not now)

- Real leveled logging (`logging` module) — when a batch runner is built.
- Retry/backoff on provider HTTP calls — when a batch runner is built.
- Extraction provenance record (prompt version, schema version, model version, timestamp) — when
  structured output parsing is built.
- A dependency manifest (`requirements.txt` or `pyproject.toml`) — when a second/third provider SDK
  is added and "note it in the docstring" stops being enough to track transitively.
- Config schema validation beyond `KeyError` — if/when the config grows past ~10 keys or gains
  nested per-provider blocks.

## 15. Nice-to-have Improvements (no clear trigger yet — track, don't schedule)

- Multi-environment config layering (`--env staging` style overrides).
- `dict`-based provider registry instead of `if/elif` (cosmetic past 4-5 providers).
- Unit test for `pipeline._load_prompt`'s empty-file fallback branch.

---

## 16. Scores

| Score | Value | Basis |
|---|---|---|
| Architecture Score | **7/10** | Clean SRP/SOLID separation, correct dependency direction, no premature abstraction beyond what was asked. Held below 8-9 by the import-portability and missing-image-identity gaps, both of which are real but cheap to close. |
| Production Readiness Score | **3/10** | Appropriately low — this is a CLI smoke test, not a service. No logging, retries, persistence, or monitoring exist, none of which were in scope for Phase 1. This score should stay low until a batch/production runner is actually built; it is not a criticism of Phase 1's stated goal. |
| Future Scalability Score | **7/10** | The provider/pipeline boundary will not need to be redesigned for additional providers, structured output, or concurrent batch execution — those are additive. The two Required Changes are the only load-bearing gaps between today's design and the 5-year vision; both are fixable without touching what already works. |

---

## 17. Go / No-Go Recommendation

**GO.** Phase 1 is approved as the architectural foundation for the Vision Engine.

Land Required Changes 13.1–13.3 (package structure, image identity, secrets convention doc) before
starting any Phase 2 work that has another module import this one or add a second provider. All
three are small, additive, and do not touch the working Ollama path.

### Prioritised Phase 2 execution order

1. **13.1 + 13.2 + 13.3** (this review's Required Changes) — foundation hardening, no new features.
2. **Batch runner** — iterate a directory of images through the existing `run_vision_pipeline`,
   sequentially first (prove correctness), concurrency only once sequential works.
3. **Author `extractor_v1.md` v1 content** and switch the prompt fallback off — now that there's a
   batch runner worth pointing a real prompt at.
4. **Structured output parsing** against `tbk_image_schema_v1.json` (once that schema is authored) —
   `analyze()` keeps returning raw text; a new parsing layer above `pipeline.py` turns it into
   validated structured data.
5. **Second provider** (Gemini or OpenAI) — proves the abstraction holds under a real second
   implementation, not just in theory.
6. Everything past this point (embeddings, Knowledge Graph, Shopify field generation, JARVIS) has a
   real prerequisite chain through 1-5 above and should not be started before they land.

---

## Notes

This review was performed as a single integrated pass rather than as separate independent reviewer
outputs — the codebase at this stage (5 Python modules, 1 config file, ~150 lines total) does not
have enough surface area to produce materially different findings across ten separate personas; a
combined review avoids manufacturing disagreement where none exists. If the platform later reaches a
scale where genuinely conflicting tradeoffs emerge across these disciplines (e.g. Data Architecture
wanting a schema-first approach vs. MLOps wanting fast iteration), a split review becomes worth the
overhead. It is not yet.
