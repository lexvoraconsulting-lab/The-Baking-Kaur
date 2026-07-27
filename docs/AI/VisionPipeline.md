# AI Vision Engine — Pipeline Walkthrough

Running `python -m ai.vision.python.test_vision` from the repo root does the following (this
package uses absolute imports, so it's run as a module with `-m`, not as a bare script path):

1. `load_config()` reads `ai/vision/config/vision.json` (or the path passed via `--config`).
2. `run_vision_pipeline(cfg)`:
   - Resolves `cfg["image_path"]` and errors with `FileNotFoundError` if it's missing.
   - Loads the prompt from `cfg["prompt_file"]` (`ai/vision/prompts/extractor_v1.md`).
   - **Empty-prompt fallback**: `extractor_v1.md` is an intentionally empty placeholder this
     phase (authoring its real content is out of scope — see the plan's Phase 1 decisions). If
     the file is empty, the pipeline falls back to the original inline cake-description prompt
     that shipped in the first version of `test_vision.py`, so the smoke test keeps working.
     This fallback is marked with a `ponytail:` comment in `pipeline.py` and should be deleted
     once `extractor_v1.md` is actually authored.
   - Calls `get_provider(cfg)` to build the configured `VisionProvider` (today: `OllamaProvider`).
   - Calls `provider.analyze(image_bytes, prompt, timeout=...)` to get the raw text response.
   - Computes `TBK_IMAGE_ID` (`compute_image_id`) and returns a `VisionResult` bundling the image
     ID, image path, `schema_version`/`taxonomy_version`, provider/model, and the response.
3. `test_vision.py` prints the image path, a progress line, the image ID, and the model's
   response.

## TBK_IMAGE_ID is the permanent identifier for every image

`compute_image_id()` (`ai/vision/python/pipeline.py`) hashes the image's bytes
(`"TBK-" + sha256(bytes)[:16]`) rather than assigning a random UUID or a counter — the same image
file always produces the same ID, with no registry or database needed to guarantee that. This ID
is the join key every future module in the platform (embeddings, OCR, vector DB, Shopify sync,
ERP, CRM, JARVIS) is expected to reference back to a specific image. It's introduced now,
deliberately, before any of those modules exist, because retrofitting an identity scheme after
volume has been processed without one is materially harder than carrying it from the start — see
`docs/AI/ARCHITECTURE_REVIEW_AR001.md` §6 and §13.2.

This is the concrete implementation of [VIG-006 (Identifier Standard)](../00_Governance/VIG-006-Identifier-Standard.md);
the `schema_version`/`taxonomy_version` fields implement [VIG-005 (Versioning Standard)](../00_Governance/VIG-005-Versioning-Standard.md).

## Pointing at a different image or model

Nothing in this flow is hardcoded — edit `ai/vision/config/vision.json` (or pass `--config` with
a different file) to change the image, model, URL, timeout, or provider. No code changes needed.
