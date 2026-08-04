# Attribute Intelligence Engine — Attribute Model (Build-303)

`ai.attribute_intelligence.models` — see [ATTRIBUTE_ENGINE.md](ATTRIBUTE_ENGINE.md) for the full
architecture.

## `AttributeObservation` — one candidate value, from one source

| Field | Meaning |
|---|---|
| `registry_reference` | A real `ai.ear` `attribute_id` (`EAR-NNNNNN`) — this package defines no attributes of its own |
| `subject_id` | Any entity's identifier (a Shopify GID today) — this package doesn't care what kind of thing it is |
| `source` | `"shopify" \| "vision" \| "manual" \| "merchant" \| "seo" \| "knowledge_graph" \| "genome" \| "inference"` |
| `value` | The candidate value (`Any`) |
| `confidence` | `float \| None`, per VIG-007 |
| `observed_at` | Caller-supplied timestamp — this package makes no wall-clock calls itself |
| `observation_id` | `compute_observation_id(registry_reference, subject_id, source, observed_at)` — deterministic uuid5 |

## `ResolvedAttribute` — the winning value for one attribute on one subject

Carries `value`/`confidence`/`source` (the winner's), `resolution_method`
(`"single_source" | "highest_trust" | "highest_confidence" | "unresolved"`), the FULL
`observations` tuple (every candidate, winner and losers alike — see
[ATTRIBUTE_ENGINE.md](ATTRIBUTE_ENGINE.md)'s "never silently overwrite" rationale), and an optional
`conflict: ConflictRecord | None`.

## `ConflictRecord` — produced whenever 2+ sources disagree on value

`competing_observations` (every one, not just the loser), `resolved_observation_id` (which one
won), `resolution_method`. Never replaces or discards a losing `AttributeObservation`.

## `AttributeHistoryEntry` — one append-only transition

`previous_value -> new_value`, tied to the `resolution_id` that produced the transition. See
[ai/logs/attribute_history.jsonl](../ai/logs) (created on first write) and
`ai.attribute_intelligence.history.AttributeHistoryLog`.

## `SubjectAttributeProfile` — the per-subject output of `AttributeIntelligenceService.resolve()`

`attributes: dict[registry_reference, ResolvedAttribute]` + `validation_issues` +
`conflicts` — the complete, queryable result of one resolution pass.

## The nine required properties (Build-303 Phase 2), and where each lives

| Property | Where |
|---|---|
| Identity | `registry_reference` + `subject_id` (+ `observation_id`/`resolution_id`) |
| Value | `AttributeObservation.value` / `ResolvedAttribute.value` |
| Confidence | `.confidence` on both |
| Version | `ATTRIBUTE_INTELLIGENCE_VERSION` on `ResolvedAttribute` |
| Source | `.source` on both |
| Timestamp | `.observed_at` / `.resolved_at` |
| Validation | `ValidationIssue` (validator.py) |
| Relationship | `ConflictRecord.competing_observations`; `AttributeInferenceEngine`'s Taxonomy-Relationship-derived observations |
| Observability | `AttributeIntelligenceObserver` hooks + `CoverageReport` (observability.py) |

## Why Phase 2's ~30 example attributes aren't 30 registered EAR entries

They illustrate the *kind* of attribute this model handles (scored, categorical, and confidence
attributes alike) — not a data-entry list for this sprint. Registering real `EAR`/`EAD` entries for
Primary Occasion, Luxury Score, etc. is EAR/EAD's own governance process (content curation), not an
engineering task; see [ADR 0010](adr/2026-08-02-attribute-intelligence-engine.md) point 10 and
[ATTRIBUTE_ROADMAP.md](ATTRIBUTE_ROADMAP.md).
