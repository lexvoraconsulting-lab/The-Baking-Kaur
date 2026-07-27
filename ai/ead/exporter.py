"""
Enterprise Attribute Definitions (EAD) v1 - export.

WHY
  The write-side counterpart to loader.py, plus JSON Schema regeneration -
  mirrors ai/ear/exporter.py exactly.
"""
import json
from pathlib import Path

import yaml

from ai.ead.definitions import DefinitionSet
from ai.ead.models_pydantic import EADDefinitionModel

EAD_DIR = Path(__file__).parent
SCHEMAS_DIR = EAD_DIR / "schemas"


def regenerate_schema() -> None:
    SCHEMAS_DIR.mkdir(exist_ok=True)
    (SCHEMAS_DIR / "ead.schema.json").write_text(
        json.dumps(EADDefinitionModel.model_json_schema(), indent=2) + "\n"
    )


def export_definitions(definition_set: DefinitionSet, path: str | Path) -> None:
    path = Path(path)
    data = {"definitions": [json.loads(d.model_dump_json()) for d in definition_set.definitions]}
    if path.suffix in (".yaml", ".yml"):
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    else:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
