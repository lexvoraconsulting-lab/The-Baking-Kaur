#!/usr/bin/env python3
"""
Self-check for the Enterprise Attribute Language (EAL) v1.

WHY
  Regenerates ai/eal/schemas/*.schema.json from the Pydantic models (so the
  committed schema files can never drift from the code that defines them),
  then validates every file in ai/eal/examples/ against its model, and
  checks canonical-path grammar and identifier determinism. No network
  calls - pure structural/library validation.

USAGE
  python -m ai.eal.test_eal
"""
import json
from pathlib import Path

import yaml

from ai.eal.models import compute_attribute_id, compute_relationship_id
from ai.eal.models_pydantic import (
    CANONICAL_PATH_PATTERN,
    EALAttributeRecordModel,
    EALRelationshipRecordModel,
)

EAL_DIR = Path(__file__).parent
SCHEMAS_DIR = EAL_DIR / "schemas"
EXAMPLES_DIR = EAL_DIR / "examples"


def regenerate_schemas():
    SCHEMAS_DIR.mkdir(exist_ok=True)
    (SCHEMAS_DIR / "eal_attribute.schema.json").write_text(
        json.dumps(EALAttributeRecordModel.model_json_schema(), indent=2) + "\n"
    )
    (SCHEMAS_DIR / "eal_relationship.schema.json").write_text(
        json.dumps(EALRelationshipRecordModel.model_json_schema(), indent=2) + "\n"
    )


def _load(path: Path) -> dict:
    text = path.read_text()
    return yaml.safe_load(text) if path.suffix == ".yaml" else json.loads(text)


def test_vision_output_example():
    EALAttributeRecordModel(**_load(EXAMPLES_DIR / "vision_output_example.json"))


def test_api_payload_example():
    payload = _load(EXAMPLES_DIR / "api_payload_example.json")
    for attr in payload["attributes"]:
        EALAttributeRecordModel(**attr)


def test_shopify_mapping_example():
    EALAttributeRecordModel(**_load(EXAMPLES_DIR / "shopify_mapping_example.yaml"))


def test_erp_mapping_example():
    EALAttributeRecordModel(**_load(EXAMPLES_DIR / "erp_mapping_example.yaml"))


def test_knowledge_graph_node_example():
    EALRelationshipRecordModel(**_load(EXAMPLES_DIR / "knowledge_graph_node_example.json"))


def test_embedding_metadata_example():
    EALAttributeRecordModel(**_load(EXAMPLES_DIR / "embedding_metadata_example.json"))


def test_canonical_path_grammar():
    assert CANONICAL_PATH_PATTERN.match("eal.core.confidence.score")
    assert CANONICAL_PATH_PATTERN.match("eal.domain.bakery.colour.primary")
    assert not CANONICAL_PATH_PATTERN.match("eal.core.confidence")  # missing attribute segment
    assert not CANONICAL_PATH_PATTERN.match("EAL.core.confidence.score")  # must be lowercase
    assert not CANONICAL_PATH_PATTERN.match("eal.bakery.colour.primary")  # missing domain. prefix


def test_attribute_id_is_deterministic():
    a = compute_attribute_id("eal.domain.bakery.colour.primary")
    b = compute_attribute_id("eal.domain.bakery.colour.primary")
    c = compute_attribute_id("eal.domain.bakery.colour.secondary")
    assert a == b
    assert a != c
    assert a.startswith("EAL-")


def test_relationship_id_is_deterministic():
    a = compute_relationship_id("TBK-OBJ-topper-01", "ON", "TBK-OBJ-cake-01")
    b = compute_relationship_id("TBK-OBJ-topper-01", "ON", "TBK-OBJ-cake-01")
    c = compute_relationship_id("TBK-OBJ-topper-01", "NEAR", "TBK-OBJ-cake-01")
    assert a == b
    assert a != c
    assert a.startswith("EAL-REL-")


def test_example_ids_match_computed_ids():
    attribute_examples = [
        _load(EXAMPLES_DIR / "vision_output_example.json"),
        _load(EXAMPLES_DIR / "shopify_mapping_example.yaml"),
        _load(EXAMPLES_DIR / "erp_mapping_example.yaml"),
        _load(EXAMPLES_DIR / "embedding_metadata_example.json"),
        *_load(EXAMPLES_DIR / "api_payload_example.json")["attributes"],
    ]
    for attr in attribute_examples:
        expected = compute_attribute_id(attr["canonical_path"])
        assert attr["attribute_id"] == expected, (
            f"{attr['canonical_path']!r} has attribute_id {attr['attribute_id']!r}, "
            f"expected {expected!r} - example is stale"
        )

    rel = _load(EXAMPLES_DIR / "knowledge_graph_node_example.json")
    expected = compute_relationship_id(rel["source_id"], rel["type"], rel["target_id"])
    assert rel["relationship_id"] == expected, (
        f"relationship_id {rel['relationship_id']!r} does not match computed {expected!r} - "
        f"example is stale"
    )


def test_value_state_rejects_value_with_null_state():
    bad = _load(EXAMPLES_DIR / "vision_output_example.json")
    bad["value_state"] = "unknown"  # value is still "white" - should be rejected
    try:
        EALAttributeRecordModel(**bad)
        assert False, "expected ValueError for value_state=unknown with a non-null value"
    except ValueError:
        pass


if __name__ == "__main__":
    regenerate_schemas()
    test_vision_output_example()
    test_api_payload_example()
    test_shopify_mapping_example()
    test_erp_mapping_example()
    test_knowledge_graph_node_example()
    test_embedding_metadata_example()
    test_canonical_path_grammar()
    test_attribute_id_is_deterministic()
    test_relationship_id_is_deterministic()
    test_example_ids_match_computed_ids()
    test_value_state_rejects_value_with_null_state()
    print("OK")
