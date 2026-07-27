# ai/vision/images/

Local sample images for manual vision-model smoke testing only (`test_vision.py`).

This is not a production dataset store. Production image datasets will live outside
git (NAS, cloud/object storage) and be referenced by path via `ai/vision/config/vision.json` —
not committed to this repo.

The 3 existing sample images (`1.png`, `2.png`, `3.png`) stay tracked. New images dropped
in this folder are gitignored by default (see repo root `.gitignore`).
