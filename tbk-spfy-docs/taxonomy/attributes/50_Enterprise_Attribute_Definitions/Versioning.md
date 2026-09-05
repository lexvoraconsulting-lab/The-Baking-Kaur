# EAD — Versioning

## Definition-format version

`ead_version` (currently `"1.0"`) is the version of the EAD wire format itself (the field list, the
validation rules) — bumped only when the format changes, per
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md)'s explicit-immutable-version rule.
Mirrors `EAL_VERSION`/`EAR_VERSION`.

## No separate per-Definition lifecycle version

Unlike EAR, which tracks `version`/`introduced_in`/`deprecated_in` per attribute, EAD does not
duplicate a lifecycle-version field — a Definition's lifecycle state is read from the EAR entry it
describes (`registry_reference` → `EARAttributeEntryModel.status`/`deprecated_in`), not
re-declared here. This is a deliberate non-duplication: EAR is the single source of truth for
*when* an attribute entered or left a lifecycle stage
([EAR's Versioning.md](../40_Enterprise_Attribute_Registry/Versioning.md)); EAD only describes what
that attribute *means*, and its guidance text changes to reflect the referenced EAR entry's current
status (see the `deprecated`/`retired` examples in
[`examples/definitions.json`](../../ai/ead/examples/definitions.json), whose `ai_guidance` fields
explicitly state the lifecycle stance rather than encoding it in a structured field).

## Related Standards

[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md),
[EAR's Versioning.md](../40_Enterprise_Attribute_Registry/Versioning.md),
[Definition_Model.md](Definition_Model.md).
