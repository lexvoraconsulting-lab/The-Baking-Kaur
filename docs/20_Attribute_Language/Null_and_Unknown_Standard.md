# EAL — Null and Unknown Standard

## Rule: three states, not two

Every EAL Attribute Record carries `value_state: "present" | "null" | "unknown"`
(`ai/eal/models.py`), distinct from `value` itself:

| `value_state` | Meaning | `value` |
|---|---|---|
| `present` | The attribute has a known value. | The actual value. |
| `null` | The attribute **does not apply** to this entity (e.g. `character_name` on a plain cake with no character). | Always `None`. |
| `unknown` | The attribute **applies but hasn't been determined yet** (not extracted, low confidence, awaiting review). | Always `None`. |

Collapsing these into one "no value" state — as a bare optional field would — loses exactly the
distinction a vision pipeline needs: "we know this cake has no topper" (`null`) is a different fact
from "we don't yet know if this cake has a topper" (`unknown`).

## Enforcement

`EALAttributeRecordModel._value_state_consistency` in
[`ai/eal/models_pydantic.py`](../../ai/eal/models_pydantic.py) rejects any record where
`value_state` is `null`/`unknown` but `value` is not `None` — see
[`test_value_state_rejects_value_with_null_state`](../../ai/eal/test_eal.py) and the `unknown`
example in [`api_payload_example.json`](../../ai/eal/examples/api_payload_example.json).

## Related Standards

[Confidence_Standard.md](Confidence_Standard.md) (an `unknown` value never carries a confidence
score — there's nothing to be confident about yet),
[Validation_Standard.md](Validation_Standard.md).
