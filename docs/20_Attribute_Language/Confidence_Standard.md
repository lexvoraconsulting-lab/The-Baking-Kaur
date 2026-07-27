# EAL — Confidence Standard

## Rule

`confidence: float | None`, range `[0.0, 1.0]`, enforced by `Field(ge=0.0, le=1.0)` in
[`ai/eal/models_pydantic.py`](../../ai/eal/models_pydantic.py). By convention it is required
(non-`None`) whenever a record's origin is AI-derived — this is the field behind
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md) Principle 1 — **but Build-001 does not yet
mechanically enforce "AI-derived implies confidence is set"** as a cross-field validator; only the
range check is live today. Flagged as a Minor finding in
[Architecture_Review_AR004.md](Architecture_Review_AR004.md).

`confidence` is `None` when `value_state` is `unknown` or `null` (nothing to be confident about) or
when the value came from a human correction rather than an AI extraction (see
[Human_Verification_Standard.md](Human_Verification_Standard.md) — a `corrected` record's
confidence is meaningless once a human has overridden it).

## Example

```json
{ "value": "white", "value_state": "present", "confidence": 0.82 }
```

vs.

```json
{ "value": null, "value_state": "unknown", "confidence": null }
```

(Both from [`api_payload_example.json`](../../ai/eal/examples/api_payload_example.json).)

## Related Standards

[VIG-007](../00_Governance/VIG-007-Quality-Standard.md),
[Null_and_Unknown_Standard.md](Null_and_Unknown_Standard.md),
[Validation_Standard.md](Validation_Standard.md) (confidence thresholding feeds the
Sprint 2.1 verification-gate logic).
