# EAR — Validation

## What is enforced today

| Check | Enforced by | Runnable proof |
|---|---|---|
| `eal_reference` matches EAL's canonical-path grammar | `EARAttributeEntryModel._eal_reference_must_match_grammar` (imports `ai.eal.models_pydantic.CANONICAL_PATH_PATTERN`) | Any malformed `eal_reference` fails on load |
| `namespace` agrees with `eal_reference` | `_namespace_matches_eal_reference` | [`test_namespace_must_match_eal_reference`](../../ai/ear/test_ear.py) |
| `datatype` is one of EAL's 11 canonical types | Pydantic `Literal` type, reused from `ai.eal` | [`test_invalid_datatype_rejected`](../../ai/ear/test_ear.py) |
| `deprecated_in` set iff `status` in (`deprecated`, `retired`) | `_deprecated_in_matches_status` | [`test_deprecated_status_requires_deprecated_in`](../../ai/ear/test_ear.py) |
| No duplicate `attribute_id` across a Registry | `ai/ear/validation.py::validate_registry` | [`test_duplicate_attribute_id_rejected`](../../ai/ear/test_ear.py) |
| No duplicate `(namespace, canonical_name)` across a Registry | `validate_registry` | [`test_duplicate_namespace_name_rejected`](../../ai/ear/test_ear.py) |
| `attribute_id` matches `^EAR-\d{6}$` | `ai/ear/ids.py::is_valid_attribute_id`, checked in `validate_registry` | [`test_example_attribute_ids_are_valid_format`](../../ai/ear/test_ear.py) |
| `registry_uuid` is deterministic from `eal_reference` | `ai/ear/ids.py::compute_registry_uuid` | [`test_registry_uuid_is_deterministic`](../../ai/ear/test_ear.py), and every example's stored value is cross-checked against a fresh recomputation — [`test_example_registry_uuids_match_computed`](../../ai/ear/test_ear.py), closing the exact drift-detection gap [AR-004](../20_Attribute_Language/Architecture_Review_AR004.md) found and fixed for EAL |
| Missing required field | Pydantic's own required-field check | [`test_missing_required_field_rejected`](../../ai/ear/test_ear.py) |
| Import/export round-trips without data loss | `ai/ear/loader.py` + `ai/ear/exporter.py` | [`test_export_then_reload_round_trips`](../../ai/ear/test_ear.py) |

## What is deliberately not yet enforced

Same category of deferral EAL's own `Validation_Standard.md` already established — a live registry
would be needed to validate against, and none exists yet:

1. **`taxonomy_references` resolving to real Sprint 2.1/2.2 taxonomy content.** Sprint 2.2 (Build-005
   per the [Enterprise Program Roadmap](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md))
   hasn't authored real Category/Attribute Group/Vocabulary content yet — `taxonomy_references`
   stays an opaque `list[str]` until it does.
2. **`definition_reference` resolving to a real Build-003 (EAD) definition.** EAD doesn't exist yet
   — this field stays `null` on every current example.
3. **`validation_profile` resolving to a real, named ruleset.** No ruleset registry exists yet;
   stored as an opaque string, defaulting to `"default"`.

Inventing enforcement for any of the three above now, with nothing real to validate against, would
violate [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4 — the same
reasoning EAL's own Validation_Standard.md already applies to its own deferred items.

## Related Standards

[EAL's Validation_Standard.md](../20_Attribute_Language/Validation_Standard.md) (the pattern this
follows), [Registry_Model.md](Registry_Model.md), [Namespace_Guide.md](Namespace_Guide.md).
