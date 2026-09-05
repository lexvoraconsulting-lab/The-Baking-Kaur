# Attribute Intelligence Engine — Validation (Build-303)

`ai.attribute_intelligence.validator.AttributeValidator` — see
[ATTRIBUTE_ENGINE.md](ATTRIBUTE_ENGINE.md) for the full architecture.

## Every rule reuses an existing `ai.ead` field — none is new

| `ValidationIssue.code` | Severity | Rule |
|---|---|---|
| `missing_confidence` | warning | `observation.confidence is None` — VIG-007 Principle 1 requires a confidence score before promotion; a missing one is flagged, not silently accepted |
| `no_definition` | warning | No `EADDefinitionModel` found for `registry_reference` — allowed_values/minimum_confidence can't be checked; the caller is told why, not left guessing |
| `value_not_allowed` | error | `definition.allowed_values is not None` and `observation.value` isn't in it |
| `below_minimum_confidence` | warning | `observation.confidence < definition.confidence_expectations.minimum_confidence` |

## Why `value_not_allowed` is an error but everything else is a warning

An out-of-vocabulary value is a real correctness problem for a `Literal`-typed attribute — passing
it downstream would violate the EAD Definition's own contract. A missing confidence, a missing
definition, or a below-threshold confidence are all real signals worth surfacing, but none of them
makes the *value itself* wrong — they describe how much to trust it, which
`AttributeConfidenceEngine`'s ranking already accounts for. This mirrors
`ai.product_intelligence.validation`'s identical error/warning split (see that package's own docs).

## How validation composes with resolution

`AttributeIntelligenceService.resolve()` validates every observation (winners and losers alike)
BEFORE conflict resolution runs — a `value_not_allowed` error on a losing observation is still
recorded in `SubjectAttributeProfile.validation_issues`, even though that observation never becomes
the `ResolvedAttribute`. Validation issues are never silently dropped just because an observation
lost a conflict.
