# EAL — Human Verification Standard

## Rule

Every Attribute Record carries a `human_verification` object
(`ai/eal/models.py::HumanVerification`):

```python
status: "unverified" | "pending_review" | "verified" | "rejected" | "corrected"
reviewer_id: str | None
reviewed_at: str | None
original_value: Any   # set only when status == "corrected" — the pre-correction value
```

This is the concrete record behind [VIG-007](../00_Governance/VIG-007-Quality-Standard.md)'s
verification gate and [Validation.md](../10_Taxonomy/Validation.md)'s confidence-thresholding /
Human Review path.

## State meanings

| Status | Meaning |
|---|---|
| `unverified` | Default. No review has happened. |
| `pending_review` | Flagged for human review (e.g. low confidence, or a consistency conflict per [Validation.md](../10_Taxonomy/Validation.md)). |
| `verified` | A human confirmed the value as correct. |
| `rejected` | A human determined the value is wrong, with no replacement supplied yet. |
| `corrected` | A human supplied a replacement value; `original_value` preserves what the AI produced, satisfying [VIG-003](../00_Governance/VIG-003-Data-Principles.md)'s immutable-source-data spirit even for corrections — nothing is silently overwritten without a trace. |

## Related Standards

[VIG-007](../00_Governance/VIG-007-Quality-Standard.md),
[Validation_Standard.md](Validation_Standard.md),
[Confidence_Standard.md](Confidence_Standard.md).
