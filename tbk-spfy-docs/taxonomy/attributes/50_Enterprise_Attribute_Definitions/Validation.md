# EAD — Validation

## What is enforced today

| Check | Enforced by | Runnable proof |
|---|---|---|
| `registry_reference` matches EAR's `^EAR-\d{6}$` format | `EADDefinitionModel._registry_reference_must_be_valid_ear_id` (imports `ai.ear.ids.is_valid_attribute_id`) | [`test_invalid_registry_reference_format_rejected`](../../ai/ead/test_ead.py) |
| No duplicate `registry_reference` across a DefinitionSet | `ai/ead/validation.py::validate_definition_set` | [`test_duplicate_registry_reference_rejected`](../../ai/ead/test_ead.py) |
| `confidence_expectations.minimum_confidence`/`typical_confidence` in `[0.0, 1.0]` | Pydantic `Field(ge=0.0, le=1.0)` | [`test_confidence_out_of_range_rejected`](../../ai/ead/test_ead.py) |
| `typical_confidence` not below `minimum_confidence` | `ConfidenceExpectationsModel._typical_not_below_minimum` | [`test_typical_confidence_below_minimum_rejected`](../../ai/ead/test_ead.py) |
| `examples` has at least one entry | `Field(min_length=1)` | [`test_examples_require_at_least_one_example_value`](../../ai/ead/test_ead.py) |
| Missing required field | Pydantic's own required-field check | [`test_missing_required_field_rejected`](../../ai/ead/test_ead.py) |
| `definition_id` is deterministic from `registry_reference` | `ai/ead/ids.py::compute_definition_id` | [`test_definition_id_is_deterministic`](../../ai/ead/test_ead.py), and every example's stored value is cross-checked against a fresh recomputation — [`test_example_definition_ids_match_computed`](../../ai/ead/test_ead.py) |
| Every example's `registry_reference` resolves against a real, loaded EAR Registry | `ai/ead/api.py::cross_reference_against_registry` | [`test_cross_reference_against_real_ear_registry`](../../ai/ead/test_ead.py) — loads the actual `ai/ear/examples/registry.json` |
| Import/export round-trips without data loss | `ai/ead/loader.py` + `ai/ead/exporter.py` | [`test_export_then_reload_round_trips`](../../ai/ead/test_ead.py) |

## What is deliberately not yet enforced

Same deferral category EAR already established — a live registry/taxonomy would be needed to
validate against, and none exists yet:

1. **`allowed_values` resolving to a real Sprint 2.1/2.2 Controlled Vocabulary.** Sprint 2.2
   (Build-006 per the
   [Enterprise Program Roadmap](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md))
   hasn't authored real vocabulary content yet — `allowed_values` stays an opaque `list[str]`.
2. **`knowledge_graph_reference` resolving to a real Knowledge Graph node.** The Knowledge Graph
   (Build-005) doesn't exist yet — this field stays `null` on every current example.
3. **No validation engine.** Per this build's own Constraints, EAD does not implement the
   Validation Engine (WS-07) — it enforces its own record shape only, not cross-attribute business
   rules or taxonomy-membership checks.

Inventing enforcement for any of the above now, with nothing real to validate against, would
violate [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4 — the same
reasoning EAR's own `Validation.md` already applies to its own deferred items.

## Related Standards

[EAR's Validation.md](../40_Enterprise_Attribute_Registry/Validation.md) (the pattern this follows),
[Definition_Model.md](Definition_Model.md), [Mapping_Guide.md](Mapping_Guide.md).
