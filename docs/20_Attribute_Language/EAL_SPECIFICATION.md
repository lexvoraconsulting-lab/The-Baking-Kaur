# Enterprise Attribute Language (EAL) v1 — Specification

## What EAL is

A wire format — not a database, not a service — for one fact: *this entity has this attribute, with
this value, produced this way, verified to this degree*. Every future module (Vision AI, Knowledge
Graph, Shopify sync, ERP sync, Search, Embeddings, JARVIS) reads and writes this same shape instead
of each inventing its own. EAL does not replace [Sprint 2.1's Entity/Attribute
Group/Relationship Model](../10_Taxonomy/Architecture.md) — it serializes that logical model into a
concrete, validated envelope two systems can actually exchange.

## Two record types

```
EALAttributeRecord     one fact about one entity
EALRelationshipRecord  one typed edge between two entities
```

Both are defined twice, deliberately: as plain dataclasses in
[`ai/eal/models.py`](../../ai/eal/models.py) (the human/IDE-facing shape, zero dependencies) and as
Pydantic models in [`ai/eal/models_pydantic.py`](../../ai/eal/models_pydantic.py) (runtime
validation + JSON Schema generation). See those files' module docstrings for why the split exists
rather than generating one from the other.

## Attribute Record — field-by-field

```
canonical_path      "eal.<namespace>.<group>.<attribute>" — Attribute_Path_Syntax.md
attribute_id        opaque, content-hash of canonical_path — Identifier_Strategy.md
eal_version         "1.0" — this document's version
namespace            "core" | "domain.<name>" — Namespace_Model.md
group               schema-level grouping (mirrors Sprint 2.1 Attribute Group)
entity_id           TBK_*_ID this attribute describes — Identifier_Strategy.md, VIG-006
entity_type         "image" | "region" | "object"
value               the actual value, or None — Null_and_Unknown_Standard.md
value_state         "present" | "null" | "unknown" — Null_and_Unknown_Standard.md
data_type           one of 11 canonical types — Data_Type_Standard.md
unit                required for physical measurements — Units_Standard.md
vocabulary          required when data_type == "enum" — Enum_Standard.md
confidence          float 0.0-1.0 or None — Confidence_Standard.md
provenance          who/what produced this — Provenance_Standard.md
human_verification  review lifecycle — Human_Verification_Standard.md
external_ids        join points to Shopify/ERP/etc — External_ID_Standard.md
```

## Relationship Record — field-by-field

```
relationship_id  opaque, content-hash of source_id|type|target_id — Identifier_Strategy.md
eal_version      "1.0"
type             a Controlled Vocabulary term (ON, NEAR, PART_OF, ...) — Relationship_Naming.md
source_id        TBK_*_ID of the edge's origin entity
target_id        TBK_*_ID of the edge's destination entity
confidence       float 0.0-1.0 or None — Confidence_Standard.md
provenance       who/what produced this — Provenance_Standard.md
```

## Diagram: one Attribute Record flowing through the platform

```
Vision Engine (ai/vision) ──produces──▶ EALAttributeRecord ──serialized as──▶ JSON / YAML
                                              │
                                              ├─▶ Knowledge Graph node/edge (via external_ids)
                                              ├─▶ Shopify metafield  (via external_ids: shopify)
                                              ├─▶ ERP attribute code (via external_ids: erp)
                                              └─▶ Embedding metadata (data_type: vector)
```

The record itself never changes shape based on its destination — see
[Migration_Guide.md](Migration_Guide.md) and [Examples.md](Examples.md) for each of these concretely.

## Folder structure

```
ai/eal/
  __init__.py               public re-exports
  models.py                 dataclasses (canonical field reference)
  models_pydantic.py        Pydantic models (validation, JSON Schema generation)
  test_eal.py               self-check: regenerates schemas, validates every example
  schemas/                  generated JSON Schema — never hand-edited, see test_eal.py
    eal_attribute.schema.json
    eal_relationship.schema.json
  examples/                 one example per real consumer, validated by test_eal.py
    vision_output_example.json
    api_payload_example.json
    shopify_mapping_example.yaml
    erp_mapping_example.yaml
    knowledge_graph_node_example.json
    embedding_metadata_example.json

docs/20_Attribute_Language/  this specification (prose, no implementation)
```

## What EAL deliberately does not do

- Does not define real Category/Attribute/Vocabulary content — that's Sprint 2.2's Master Taxonomy,
  which EAL records point at via `group`/`vocabulary`, not duplicate.
- Does not choose a physical datastore for the Knowledge Graph — an ADR-level decision per
  [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md), unaffected by this wire format.
- Does not implement a Vocabulary registry, a Master Taxonomy validator, or a unit-conversion
  service — each is named as a future consumer in the relevant standard document, not built here.

## Related Standards

Implements [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) (module boundaries),
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) (`eal_version`),
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md) (`attribute_id`/`relationship_id`),
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md) (confidence/provenance/verification), and
serializes [Sprint 2.1](../10_Taxonomy/Architecture.md)'s logical model. See
[README.md](README.md) for the full document index.
