"""
Enterprise Master Taxonomy (Build-005) - import.

WHY
  One function, both formats - a catalog file has four top-level keys
  (categories, attribute_groups, vocabularies, terms), in either JSON or
  YAML. Mirrors ai.ear.loader's _read()/load_registry() pattern exactly.
"""
import json
from pathlib import Path

import yaml

from ai.taxonomy.catalog import TaxonomyCatalog
from ai.taxonomy.models_pydantic import (
    AttributeGroupModel,
    CategoryModel,
    TermModel,
    VocabularyModel,
)


def _read(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if path.suffix in (".yaml", ".yml") else json.loads(text)


def load_catalog(path: str | Path) -> TaxonomyCatalog:
    data = _read(Path(path))
    categories = [CategoryModel(**raw) for raw in data.get("categories", [])]
    attribute_groups = [AttributeGroupModel(**raw) for raw in data.get("attribute_groups", [])]
    vocabularies = [VocabularyModel(**raw) for raw in data.get("vocabularies", [])]
    terms = [TermModel(**raw) for raw in data.get("terms", [])]
    return TaxonomyCatalog(categories, attribute_groups, vocabularies, terms)
