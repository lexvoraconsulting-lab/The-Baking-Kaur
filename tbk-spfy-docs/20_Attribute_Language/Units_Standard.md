# EAL — Units Standard

## Rule

Any attribute whose value is a physical measurement carries an explicit `unit` field
(`ai/eal/models.py`'s `EALAttributeRecord.unit: str | None`). No attribute's magnitude is ever
interpreted without one — a bare `value: 15` with no `unit` is meaningless and must not be produced.

## Canonical units (v1)

Build-001 does not yet enforce a controlled unit vocabulary (no measurement-typed attribute exists
in any Build-001 example) — this is intentionally deferred, not an oversight, since inventing unit
codes with nothing yet using them would violate
[VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4. When the first
measurement attribute is authored (Sprint 2.2+), its unit values become entries in a `unit` name
Controlled Vocabulary, following the exact same mechanism as [Enum_Standard.md](Enum_Standard.md) —
`unit` is conceptually an enum field, just one that hasn't been populated yet.

## Conversion policy (forward-looking)

When units are populated: a schema declares one canonical unit per attribute; a value supplied in a
different unit is converted to the canonical unit before storage, with the original unit recorded
in `provenance` (extending [Provenance_Standard.md](Provenance_Standard.md)) — never stored
ambiguously in two possible units under one field.

## Related Standards

[Data_Type_Standard.md](Data_Type_Standard.md), [Enum_Standard.md](Enum_Standard.md).
