"""
Enterprise Attribute Definitions (EAD) v1 - import.

WHY
  Mirrors ai/ear/loader.py exactly - one function, both formats, a
  definitions file is a list of entries under a "definitions" key.
"""
import json
from pathlib import Path

import yaml

from ai.ead.definitions import DefinitionSet
from ai.ead.models_pydantic import EADDefinitionModel


def _read(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if path.suffix in (".yaml", ".yml") else json.loads(text)


def load_definitions(path: str | Path) -> DefinitionSet:
    data = _read(Path(path))
    definitions = [EADDefinitionModel(**raw) for raw in data["definitions"]]
    return DefinitionSet(definitions)
