# EAD — Mapping Guide

## `shopify_mapping` / `erp_mapping`

Both reuse `ai.eal.models_pydantic.ExternalIdModel` directly — the exact `system`/`id_type`/`value`
shape [External_ID_Standard.md](../20_Attribute_Language/External_ID_Standard.md) already defines
for EAL's own `external_ids` field. EAD does not invent a second join mechanism; it reuses EAL's,
scoped one level up (per-attribute *guidance* about the mapping, not the per-record join itself,
which still lives on the `EALAttributeRecord`).

```json
"shopify_mapping": { "system": "shopify", "id_type": "metafield", "value": "custom.primary_colour" }
```

(See [`EAR-000001` in `examples/definitions.json`](../../ai/ead/examples/definitions.json).)

Either field is `null` when an attribute isn't (yet) distributed to that system — e.g. a `draft` or
`deprecated`/`retired` attribute (see [`EAR-000002`, `EAR-000004`, `EAR-000005`]
(../../ai/ead/examples/definitions.json)).

## `knowledge_graph_reference`

An opaque, nullable pointer. The Knowledge Graph (Build-005) doesn't exist yet — every current
example leaves this `null`, the same deferred-pointer pattern EAR already used for its own
`definition_reference` before this build existed
([EAR_SPECIFICATION.md](../40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md)).

## Who actually writes to Shopify/ERP

**Build-003 (this build) writes nowhere.** `shopify_mapping`/`erp_mapping` are guidance consumed by
Build-004 (Enterprise Attribute Distribution) — the only code with write access to either external system
([Enterprise Program Roadmap](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 13/14). This mirrors EAR's own boundary: a registry/definitions layer describes, a
distribution layer acts.

## `mapping_guidance` vs. the concrete mapping fields

`mapping_guidance` is prose context (e.g. "used for kitchen recipe colour matching") that explains
*why* a mapping exists; `shopify_mapping`/`erp_mapping` are the concrete, machine-usable join
values Build-004 reads. Neither replaces the other — prose for a human reviewer, structured data
for the distribution code.

## Related Standards

[External_ID_Standard.md](../20_Attribute_Language/External_ID_Standard.md),
[Definition_Model.md](Definition_Model.md), Enterprise Program Roadmap Sections 07 (Build-004), 13,
14.
