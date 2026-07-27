# EAL — External ID Standard

## Rule

Every Attribute Record carries `external_ids: list[ExternalId]`
(`ai/eal/models.py::ExternalId`):

```python
system: str    # e.g. "shopify", "erp"
id_type: str    # e.g. "metafield", "sku_attribute_code"
value: str       # the external system's own identifier/key
```

This is the *only* place an external system's identity enters an EAL record. `canonical_path`,
`attribute_id`, `group`, and every other field are Shopify/ERP/CRM-agnostic by construction — see
[VIG-004](../00_Governance/VIG-004-AI-Principles.md) Principle 1 (providers, and by extension
downstream systems, are interchangeable and non-load-bearing for the language itself).

## Why a list, not a single field

One EAL Attribute Record can join to more than one external system at once — a colour attribute
might be a Shopify metafield *and* an ERP SKU attribute code simultaneously, with neither system
aware of the other. A single `external_id` field would force a choice between them; the list lets
both mappings coexist on the one record that's actually true.

## Example: the same attribute, two external systems

```yaml
# shopify_mapping_example.yaml
external_ids:
  - system: shopify
    id_type: metafield
    value: "custom.primary_colour"
```

```yaml
# erp_mapping_example.yaml
external_ids:
  - system: erp
    id_type: sku_attribute_code
    value: "COLOUR_PRIMARY"
```

Both files wrap the *same* `attribute_id: EAL-fa3c900429a739de` — proving one EAL record maps to
many downstream systems without EAL itself knowing about any of them. See
[Examples.md](Examples.md).

## What EAL does NOT do

EAL does not validate that a `system` value is one of a known set, or that a `value` is a real,
live Shopify/ERP identifier — that's each integration's own responsibility at write time.
`external_ids` is a join table entry, not a foreign-key-checked reference.

## Related Standards

[VIG-004](../00_Governance/VIG-004-AI-Principles.md),
[Relationship_Model.md](../10_Taxonomy/Relationship_Model.md) (Image/Object → Business Entity is the
taxonomy-level version of this same join), [Migration_Guide.md](Migration_Guide.md).
