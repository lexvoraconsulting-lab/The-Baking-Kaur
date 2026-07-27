"""
Enterprise Attribute Registry (EAR) v1 - import.

WHY
  One function, both formats - a registry file is a list of entries under an
  "attributes" key, in either JSON or YAML. Mirrors the _load() helper in
  ai/eal/test_eal.py, promoted to production code here since EAR ships
  import/export as a first-class feature, not just a test fixture.
"""
import json
from pathlib import Path

import yaml

from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.ear.registry import Registry


def _read(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if path.suffix in (".yaml", ".yml") else json.loads(text)


def load_registry(path: str | Path) -> Registry:
    data = _read(Path(path))
    entries = [EARAttributeEntryModel(**raw) for raw in data["attributes"]]
    return Registry(entries)
