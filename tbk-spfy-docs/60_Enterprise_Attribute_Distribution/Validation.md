# Enterprise Attribute Distribution — Validation

## What is enforced today

| Check | Enforced by | Runnable proof |
|---|---|---|
| `registry_reference` matches EAR's `^EAR-\d{6}$` format | `DistributionRecordModel._registry_reference_must_be_valid_ear_id` (imports `ai.ear.ids.is_valid_attribute_id`) | [`test_invalid_registry_reference_format_rejected`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| `confidence` in `[0.0, 1.0]` | Pydantic `Field(ge=0.0, le=1.0)` | [`test_confidence_out_of_range_rejected`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| `external_id` required iff `status` in (`dry_run`, `success`) | `_external_id_required_when_resolved` | [`test_external_id_required_when_dry_run_or_success`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| `notes` required iff `status` in (`failed`, `conflict`), forbidden otherwise | `_notes_required_iff_failed_or_conflict` | [`test_notes_required_when_status_failed_or_conflict`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| `distribution_id` deterministic from `(registry_reference, target_system)` | `ai/attribute_distribution/ids.py::compute_distribution_id` | [`test_distribution_id_is_deterministic`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| `resolve_distribution()`'s three inputs describe the same attribute | join-integrity check, raises `ValueError` on mismatch | [`test_resolve_join_mismatch_raises`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| `detect_conflict()` only accepts an already-resolved record | requires `status == "dry_run"`, raises `ValueError` otherwise | [`test_detect_conflict_requires_dry_run_status`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| `ERPAdapter.stub_submit()` performs no I/O | signature has no `path`/`url` parameter — structurally incapable | [`test_erp_adapter_performs_no_io`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| Full pipeline composes correctly against real data, both target systems | round-trip test | [`test_round_trip_shopify_and_erp_real_fixtures`](../../ai/attribute_distribution/test_attribute_distribution.py) |
| A flagged conflict is excluded from both adapters | round-trip test | [`test_round_trip_real_conflict_excluded_from_distribution`](../../ai/attribute_distribution/test_attribute_distribution.py) |

## What is deliberately not yet enforced

Same deferral category every prior Build in this platform has already established — a real
downstream system or a real inspected API would be needed to validate against, and neither exists
yet:

1. **Real Shopify payload validation.** No live Shopify Admin API call is made this sprint — the
   dry-run review artifact's shape is not checked against Shopify's actual metafield constraints
   (type, length, etc.). That belongs to whichever future Build implements a real `--apply` path.
2. **Real ERP payload validation.** TBK Kitchen ERP's write API remains uninspected
   ([Enterprise Program Roadmap §13](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md#section-13--erp-integration-strategy),
   Risk R-3) — `ERPAdapter` cannot validate a payload shape that has never been seen.
3. **Real downstream conflict data.** `detect_conflict()`'s `CurrentDownstreamValue` is always
   supplied by the caller in this Build — no code here performs a real read of Shopify's or ERP's
   current value (Risk R-2). The round-trip test (BL-6) proves the *wiring* is correct, not that
   any conflict it will ever flag reflects real downstream state.

Inventing enforcement for any of the above now, with nothing real to validate against, would
violate [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4 — the same
reasoning every prior Build in this platform (EAL, EAR, EAD) already applied to its own deferred
items.

## Related Standards

[EAL's Validation_Standard.md](../20_Attribute_Language/Validation_Standard.md),
[EAR's Validation.md](../40_Enterprise_Attribute_Registry/Validation.md),
[EAD's Validation.md](../50_Enterprise_Attribute_Definitions/Validation.md) — the pattern this
follows. [EAD_SPECIFICATION.md](EAD_SPECIFICATION.md).
