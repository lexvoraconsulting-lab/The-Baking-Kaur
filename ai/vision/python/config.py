"""
Vision pipeline config loader.

WHY
  Nothing in this repo hardcodes model names, URLs, or paths per CLAUDE.md's
  configuration guidance. One function, plain JSON (stdlib only - no PyYAML/
  tomllib dependency to add for 6 known keys, and this folder already uses
  .json for the schema files next to it).
"""
import json
from pathlib import Path


def load_config(path: str | Path = "ai/vision/config/vision.json") -> dict:
    """Read and return the vision pipeline config. Raises FileNotFoundError /
    json.JSONDecodeError on bad input - no silent defaults for a config file
    that must exist to run anything."""
    with open(path) as f:
        return json.load(f)
