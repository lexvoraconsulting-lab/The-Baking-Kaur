# EAR — Versioning

## Two versioning layers

**Registry-format version** — `ear_version` (currently `"1.0"`), the version of the EAR wire format
itself (the field list, the validation rules). Bumped only when the format changes, per
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md)'s explicit-immutable-version rule —
mirrors `EAL_VERSION` in [EAL](../20_Attribute_Language/EAL_SPECIFICATION.md).

**Per-attribute lifecycle version** — `version`, `introduced_in`, `deprecated_in`, tracking one
attribute's own history: which schema/taxonomy version introduced it, and (if applicable) which
version deprecated it. This is new to EAR — EAL records a single fact's shape; EAR is the first
module tracking an attribute's *lifecycle* across versions.

## Sequential `v1`/`v2` convention

Per-attribute version fields follow VIG-005's sequential `v1`/`v2`... convention for content
artifacts (not the governance library's own `Version: 1.0` amendment style, which VIG-005
explicitly excludes itself from). `introduced_in` is always required; `deprecated_in` is required
if and only if `status` is `"deprecated"` or `"retired"` — enforced by
`EARAttributeEntryModel._deprecated_in_matches_status`, see [Validation.md](Validation.md).

## Status lifecycle

```
draft -> active -> deprecated -> retired
```

Not a strictly enforced state machine in Build-002 (an entry could in principle move `active` ->
`draft` if authored that way) — only the `deprecated_in` consistency rule above is mechanically
enforced. A stricter transition-order validator is a candidate for a future Build if a real
authoring workflow needs one; not built ahead of that need
([VIG-001](../00_Governance/VIG-001-Platform-Principles.md) Principle 4).

## Related Standards

[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md),
[EAL's identifier/versioning precedent](../20_Attribute_Language/Identifier_Strategy.md),
[Validation.md](Validation.md).
