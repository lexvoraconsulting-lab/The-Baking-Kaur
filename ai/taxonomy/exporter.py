"""
Enterprise Master Taxonomy (Build-005) - export.

WHY
  The write-side counterpart to loader.py, plus JSON Schema regeneration -
  regenerate_schemas() writes ai/taxonomy/schemas/*.schema.json from the four
  Pydantic models so the committed schema files can never drift from the
  code that defines them. Mirrors ai.ear.exporter.
"""
import json
from pathlib import Path

import yaml

from ai.taxonomy.catalog import TaxonomyCatalog
from ai.taxonomy.models_pydantic import (
    AttributeGroupModel,
    CategoryModel,
    RelationshipModel,
    TaxonomyAttributeModel,
    TermModel,
    VocabularyModel,
)

TAXONOMY_DIR = Path(__file__).parent
SCHEMAS_DIR = TAXONOMY_DIR / "schemas"

_SCHEMA_MODELS = {
    "category": CategoryModel,
    "attribute_group": AttributeGroupModel,
    "vocabulary": VocabularyModel,
    "term": TermModel,
    "attribute": TaxonomyAttributeModel,
    "relationship": RelationshipModel,
}


def regenerate_schemas() -> None:
    SCHEMAS_DIR.mkdir(exist_ok=True)
    for name, model in _SCHEMA_MODELS.items():
        (SCHEMAS_DIR / f"{name}.schema.json").write_text(
            json.dumps(model.model_json_schema(), indent=2) + "\n"
        )


def export_catalog(catalog: TaxonomyCatalog, path: str | Path) -> None:
    path = Path(path)
    data = {
        "categories": [json.loads(c.model_dump_json()) for c in catalog.categories],
        "attribute_groups": [json.loads(g.model_dump_json()) for g in catalog.attribute_groups],
        "vocabularies": [json.loads(v.model_dump_json()) for v in catalog.vocabularies],
        "terms": [json.loads(t.model_dump_json()) for t in catalog.terms],
        "attributes": [json.loads(a.model_dump_json()) for a in catalog.attributes],
        "relationships": [json.loads(r.model_dump_json()) for r in catalog.relationships],
    }
    if path.suffix in (".yaml", ".yml"):
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    else:
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
