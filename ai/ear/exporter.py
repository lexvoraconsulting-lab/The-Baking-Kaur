"""
Enterprise Attribute Registry (EAR) v1 - export.

WHY
  The write-side counterpart to loader.py, plus JSON Schema regeneration -
  regenerate_schema() writes ai/ear/schemas/ear.schema.json from
  EARAttributeEntryModel so the committed schema file can never drift from
  the code that defines it, the same guarantee ai/eal/test_eal.py provides
  for EAL's schemas.
"""
import json
from pathlib import Path

import yaml

from ai.ear.models_pydantic import EARAttributeEntryModel
from ai.ear.registry import Registry

EAR_DIR = Path(__file__).parent
SCHEMAS_DIR = EAR_DIR / "schemas"


def regenerate_schema() -> None:
    SCHEMAS_DIR.mkdir(exist_ok=True)
    (SCHEMAS_DIR / "ear.schema.json").write_text(
        json.dumps(EARAttributeEntryModel.model_json_schema(), indent=2) + "\n"
    )


def export_registry(registry: Registry, path: str | Path) -> None:
    path = Path(path)
    data = {"attributes": [json.loads(e.model_dump_json()) for e in registry.entries]}
    if path.suffix in (".yaml", ".yml"):
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    else:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
