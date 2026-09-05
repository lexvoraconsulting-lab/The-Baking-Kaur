# EAR — Registry Model

## What a Registry is

`ai/ear/registry.py::Registry` holds the whole collection of `EARAttributeEntryModel` entries in
memory, keyed for lookup by both identifiers a caller might have (`attribute_id` or
`eal_reference`). A `Registry` object that exists is guaranteed internally consistent — its
constructor runs [`validate_registry`](Validation.md) before building its lookup indexes, so a
`Registry` is never a partially-checked collection.

## Uniqueness invariants

Enforced by `ai/ear/validation.py::validate_registry` at construction time, over the whole
collection at once (per-entry shape is already enforced by `EARAttributeEntryModel`'s own
validators before an entry ever reaches a `Registry` — see
[EAL's Namespace_Model.md](../20_Attribute_Language/Namespace_Model.md) for the equivalent
per-entry pattern this mirrors):

1. **No two entries share an `attribute_id`.** Each `EAR-NNNNNN` identifies exactly one attribute.
2. **No two entries share a `(namespace, canonical_name)` pair.** A namespace-scoped name must
   resolve to exactly one attribute — two different attributes both named `primary_colour` under
   `domain.bakery` would make `canonical_name` ambiguous within its own namespace.

Both are runnable assertions:
[`test_duplicate_attribute_id_rejected`](../../ai/ear/test_ear.py),
[`test_duplicate_namespace_name_rejected`](../../ai/ear/test_ear.py).

## Why duplicate `attribute_id` and duplicate `(namespace, canonical_name)` are different checks

An `attribute_id` collision is an allocator bug (two entries claiming the same sequential slot). A
`(namespace, canonical_name)` collision is a naming bug (two genuinely different attribute
identities registered under the same human-readable name) — the two can occur independently, so
catching one does not imply catching the other.

## Query surface

`ai/ear/api.py` exposes the read-only questions EAR is meant to answer:
`attribute_exists`, `get_attribute`, `get_by_eal_reference`, `by_namespace`, `by_owner`, `by_tag`.
Every function reads from an already-validated `Registry` — none of them perform I/O or resolve
against a real taxonomy or EAD content, since neither exists yet (see [Validation.md](Validation.md)).

## Related Standards

[Validation.md](Validation.md), [Namespace_Guide.md](Namespace_Guide.md),
[EAR_SPECIFICATION.md](EAR_SPECIFICATION.md).
