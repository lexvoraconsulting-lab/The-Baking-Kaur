# Image Taxonomy — Validation Strategy

Sprint 2.1. Defines how a candidate Attribute is checked before it becomes a Genome Attribute — the
concrete validation logic sitting inside
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md)'s verification gate.

## Four validation dimensions

1. **Structural validation** — does the candidate Attribute's value conform to its Attribute
   definition's expected type (string, number, enum) and, where one exists, resolve to a
   [Controlled Vocabulary](Controlled_Vocabulary.md) Term? A value that doesn't fit its Attribute's
   type is rejected before it reaches the confidence/review stage at all.
2. **Confidence thresholding** — does the Attribute's confidence score clear the bar required for
   automatic promotion to a Genome Attribute, or does it require Human Review
   ([VIG-007](../00_Governance/VIG-007-Quality-Standard.md) Principle 5)? The threshold is a
   per-Attribute-Group configuration value, not a single global number — a "Colour" Attribute's
   auto-promotion bar and a customer-facing "Occasion" claim's bar are not required to be the same,
   since VIG-007 already states risk-proportionate review is acceptable.
3. **Consistency validation** — does this candidate Attribute contradict another already-verified
   Genome Attribute on the same entity (e.g. `shape: round` and `shape: square` on the same Object)?
   A contradiction blocks automatic promotion and routes to Human Review rather than silently
   picking one value.
4. **Completeness validation** — for a given Category, are the Attribute Groups
   ([Attribute_Group_Architecture.md](Attribute_Group_Architecture.md)) that Category requires
   actually populated? This is a data-quality signal (what's missing), not a blocker — an Image
   with incomplete Attributes is still valid; completeness validation surfaces gaps for the Roadmap
   rather than rejecting data.

## Not every group exercises all four dimensions equally

The four dimensions apply with different weight depending on the Attribute Group. A classification
value (e.g. `shape: round`, in the Geometry group) meaningfully exercises all four — it can be
structurally wrong, low-confidence, contradicted, or missing. A raw embedding vector (Embeddings
group, see [Attribute_Group_Architecture.md](Attribute_Group_Architecture.md)) has no natural
"contradiction" with another embedding and no classification-style confidence score — for that
group, structural validation (correct dimensionality, correct model/version tag) is the primary
check; confidence and consistency validation are not meaningful in the same sense and should not be
forced onto it just for uniformity.

## What validation does NOT do

Validation never fabricates a value to satisfy completeness, and never silently resolves a
consistency conflict by guessing — both would violate
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md) Principle 3 (no fabricated attributes,
ever). An incomplete or conflicting record is left incomplete/conflicting and flagged, not patched.

## Where validation sits in the pipeline

```
AI Observation → parse → candidate Attribute
                              │
                    [1. Structural validation]
                              │
                    [2. Confidence thresholding] ──fails──> Human Review
                              │ passes                           │
                    [3. Consistency validation] ──conflicts──────┤
                              │ passes                           │
                         Genome Attribute <──── reviewed/approved ┘
```

## Related Standards

Implements [VIG-007](../00_Governance/VIG-007-Quality-Standard.md) in full for the taxonomy domain.
Cross-references [Controlled_Vocabulary.md](Controlled_Vocabulary.md) (structural validation
target) and [Attribute_Group_Architecture.md](Attribute_Group_Architecture.md) (per-group
confidence thresholds).
