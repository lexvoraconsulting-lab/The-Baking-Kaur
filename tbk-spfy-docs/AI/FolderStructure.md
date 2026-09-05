# AI Vision Engine — Folder Structure

```
ai/vision/
  python/
    config.py                    load_config(path) -> dict
    providers.py                  VisionProvider ABC + OllamaProvider + get_provider() factory
    pipeline.py                    run_vision_pipeline(cfg) -> str, orchestrates image+prompt+provider
    test_vision.py                  thin CLI entrypoint (load config -> run pipeline -> print)
    test_config_providers.py         self-check, no network calls
  config/
    vision.json                      provider name/model/url/timeout, prompt_file, schema_file, image_path
  prompts/
    extractor_v1.md                   empty placeholder — content authored in a later phase
  schemas/
    taxonomy_v1.json                   empty placeholder
    tbk_image_schema_v1.json            empty placeholder
  images/
    1.png, 2.png, 3.png                  tracked sample images for local smoke testing
    README.md                             scope note (not a dataset store)
```

## Why prompts/ and schemas/ are separate from python/

The prompt text and the output schema are *content* — what to ask the model and what shape the
answer should take. They change independently of the *mechanism* (how to call a vision model).
Keeping them in their own folders means authoring that content later touches zero Python code.

## Why images/ isn't a dataset store

`ai/vision/images/` holds a handful of sample photos for manually verifying the pipeline still
works — not a place to accumulate a product catalogue's worth of images. See
[images/README.md](../../ai/vision/images/README.md). Production datasets are referenced by path
via `config/vision.json`, not committed to git — enforced by the `.gitignore` rule that allowlists
only the 3 existing samples.

## Why no `providers/` package yet

`providers.py` holds one abstract class, one concrete implementation, and one factory function —
a single file, not a subpackage. A `providers/` package is only justified once a second concrete
provider (Google/OpenAI/Claude) actually exists; splitting now would be a folder with no second
tenant.

This layout applies [VIG-002 (Architecture Principles)](../00_Governance/VIG-002-Architecture-Principles.md)
Principle 4 (structure in proportion to actual responsibilities).
