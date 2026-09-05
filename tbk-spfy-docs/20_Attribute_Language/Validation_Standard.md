# EAL — Validation Standard

## What `ai/eal/models_pydantic.py` actually enforces today

| Check | Enforced by | Runnable proof |
|---|---|---|
| `canonical_path` matches the 4-segment grammar | `_path_must_match_grammar` | [`test_canonical_path_grammar`](../../ai/eal/test_eal.py) |
| `namespace` agrees with `canonical_path` | `_namespace_matches_path` | Implicit in every example test — a mismatch raises on load. |
| `value_state` in (`null`, `unknown`) ⇒ `value is None` | `_value_state_consistency` | [`test_value_state_rejects_value_with_null_state`](../../ai/eal/test_eal.py) |
| `confidence` in `[0.0, 1.0]` when set | `Field(ge=0.0, le=1.0)` | Pydantic's own range check; no dedicated test needed — a violating example would fail to load. |
| `attribute_id`/`relationship_id` are deterministic from their inputs | `compute_attribute_id`/`compute_relationship_id` | [`test_attribute_id_is_deterministic`](../../ai/eal/test_eal.py), [`test_relationship_id_is_deterministic`](../../ai/eal/test_eal.py) |
| Every field's basic type (`str`, `float`, `Literal[...]`, nested model) | Pydantic's standard type coercion/rejection | Every `test_*_example` function — a shape violation raises `ValidationError` on load. |

## What is deliberately not yet enforced (see Architecture_Review_AR004.md)

These are all "Minor, deferred" findings, not oversights — each requires a live registry that
doesn't exist yet in Build-001, and inventing one with nothing to validate against would violate
[VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4 (no speculative
scaffolding):

1. **AI-derived ⇒ `confidence` is set.** Not yet a cross-field validator — see
   [Confidence_Standard.md](Confidence_Standard.md).
2. **`data_type == "enum"` ⇒ `vocabulary` is set.** Not yet a cross-field validator — see
   [Enum_Standard.md](Enum_Standard.md).
3. **`vocabulary`'s declared name resolves to a real Controlled Vocabulary, and `value` is a real
   term in it.** Requires the Sprint 2.2 Master Taxonomy / Vocabulary registry to exist first — see
   [Enum_Standard.md](Enum_Standard.md).
4. **`type` (Relationship Record) resolves to a real relationship-type vocabulary term.** Same
   deferral, see [Relationship_Naming.md](Relationship_Naming.md).
5. **Unit values against a controlled unit vocabulary.** No measurement-typed attribute exists in
   any Build-001 example yet — see [Units_Standard.md](Units_Standard.md).

## How this maps onto Sprint 2.1's Validation dimensions

[Validation.md](../10_Taxonomy/Validation.md) names four validation dimensions at the taxonomy
level (schema conformance, confidence-thresholding, consistency conflicts, human-review gating).
EAL's Pydantic layer is the schema-conformance dimension's concrete implementation for the wire
format; the other three (confidence-thresholding, consistency conflicts, human-review gating) are
downstream consumer logic operating *on* validated EAL records, not EAL validation itself — EAL
guarantees a record is well-formed, not that its value is correct or has been reviewed.

## Related Standards

[Validation.md](../10_Taxonomy/Validation.md) (taxonomy-level validation dimensions),
[Architecture_Review_AR004.md](Architecture_Review_AR004.md) (the review that flagged every
deferred item above), [Confidence_Standard.md](Confidence_Standard.md),
[Enum_Standard.md](Enum_Standard.md), [Null_and_Unknown_Standard.md](Null_and_Unknown_Standard.md).
