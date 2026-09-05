# EAL — Namespace Model

## Rule

Two namespace forms only: `core` (platform-level, applies to every domain, defined once — never
extended per-domain) and `domain.<name>` (domain-level, one subtree per industry). This is the
direct serialization of Sprint 2.1's two-tier Attribute Group split
([Attribute_Group_Architecture.md](../10_Taxonomy/Attribute_Group_Architecture.md)) into the wire
format — EAL does not introduce a third tier or redefine the split.

## Enforcement

`EALAttributeRecordModel._namespace_matches_path` in
[`ai/eal/models_pydantic.py`](../../ai/eal/models_pydantic.py) derives the expected `namespace`
value from `canonical_path` and rejects any record where the two disagree — a record cannot claim
`namespace: "core"` while its path says `eal.domain.bakery....`, or vice versa.

## Examples

| `canonical_path` | `namespace` |
|---|---|
| `eal.core.confidence.score` | `core` |
| `eal.domain.bakery.colour.primary` | `domain.bakery` |
| `eal.domain.flowers.stem_count.value` | `domain.flowers` (future domain, same rule, zero code changes) |

## Related Standards

Implements [VIG-001](../00_Governance/VIG-001-Platform-Principles.md),
[VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4 (additive-only growth —
adding `domain.flowers` never touches `core` or `domain.bakery`). See
[Attribute_Path_Syntax.md](Attribute_Path_Syntax.md) for the path grammar this maps onto.
