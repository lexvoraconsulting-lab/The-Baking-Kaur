#!/usr/bin/env python3
"""
The Baking Kaur - Vision Engine smoke test.

WHY
  Manual CLI check that the configured vision provider (model/URL/image) is
  reachable and returns a sensible description. Not a pipeline runner, not a
  batch tool - one image, one prompt, print the response.

USAGE
  Run as a module from the repo root (this package uses absolute imports,
  so it must be run with -m, not as a bare script path):
    python -m ai.vision.python.test_vision
    python -m ai.vision.python.test_vision --config path/to/other.json
"""
import argparse

from ai.vision.python.config import load_config
from ai.vision.python.pipeline import run_vision_pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="ai/vision/config/vision.json")
    args = parser.parse_args()

    cfg = load_config(args.config)

    print(f"Loading image: {cfg['image_path']}")
    print("Sending image to provider...")
    result = run_vision_pipeline(cfg)

    print(f"Image ID: {result.image_id}")
    print("\n========================")
    print("MODEL RESPONSE")
    print("========================\n")
    print(result.response)
    print(f"\nTokens: {result.token_usage.input_tokens} in / {result.token_usage.output_tokens} out")
    if result.cost.status == "calculated":
        print(f"Cost: {result.cost.total_cost} {result.cost.currency}")
    else:
        print(f"Cost: pending ({result.cost.reason})")


if __name__ == "__main__":
    main()
