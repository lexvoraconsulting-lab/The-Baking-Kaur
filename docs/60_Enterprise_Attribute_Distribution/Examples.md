# Enterprise Attribute Distribution — Examples Walkthrough

## Why this module has no `examples/` directory of its own

Every prior Build (`ai/eal`, `ai/ear`, `ai/ead`) ships its own `examples/` directory of standalone
fixture files. Build-004 deliberately does not — every example it needs already exists as a real,
committed fixture in one of those three modules, and this Build's whole purpose is to compose
*across* them. Duplicating a copy of `ai/eal/examples/shopify_mapping_example.yaml` into a new
`ai/attribute_distribution/examples/` directory would be exactly the kind of duplication this
project's own conventions warn against — one fact, one place.

## The real fixtures this Build's tests load

- **`ai/eal/examples/shopify_mapping_example.yaml`** — the verified colour attribute
  (`eal.domain.bakery.colour.primary`, value `"white"`, `human_verification.status: "verified"`).
  Used by BL-2's success-path tests and BL-6's round-trip test — this is the one attribute that
  passes the Shopify verification gate.
- **`ai/eal/examples/vision_output_example.json`** — the same attribute, unverified
  (`human_verification.status: "unverified"`). Used by BL-2's tests proving Shopify blocks an
  unverified record while ERP allows it.
- **`ai/eal/examples/api_payload_example.json`**'s second attribute — `decoration.type`, draft,
  `value: null`. Used by BL-2's missing-mapping test (`EAR-000002` has no Shopify/ERP mapping yet
  in `ai/ead/examples/definitions.json`).
- **`ai/ear/examples/registry.json`** — loaded via `ai.ear.loader.load_registry` in every test that
  needs a real `EARAttributeEntryModel` to resolve against.
- **`ai/ead/examples/definitions.json`** — loaded via `ai.ead.loader.load_definitions` for the real
  `EADDefinitionModel` mapping guidance (`shopify_mapping`/`erp_mapping`).

## Round-trip walkthrough (BL-6)

`test_round_trip_shopify_and_erp_real_fixtures` is the concrete, runnable proof of this Build's
whole reason for existing:

1. Loads the real verified colour attribute, its real EAR entry, its real EAD definition.
2. `resolve_distribution(..., "shopify")` → `status="dry_run"`, `external_id.value ==
   "custom.primary_colour"`.
3. `resolve_distribution(..., "erp")` → `status="dry_run"`, `external_id.value ==
   "COLOUR_PRIMARY"`.
4. `detect_conflict()` on both, with a matching current value → both stay `dry_run` (no conflict).
5. `ShopifyAdapter().write_review_artifact([shopify_result], tmp_path)` → writes exactly 1 line;
   `ERPAdapter().stub_submit([erp_result])` → counts exactly 1.

`test_round_trip_real_conflict_excluded_from_distribution` proves the inverse: the same attribute,
`detect_conflict()`'d against a deliberately divergent current value, becomes `status="conflict"`
and is excluded from both adapters — zero written, zero counted.

## Regenerating and re-validating

```bash
python -m ai.attribute_distribution.test_attribute_distribution
```

Runs all 23 checks — model construction/validation, `resolve_distribution`, `detect_conflict`,
`ShopifyAdapter`, `ERPAdapter`, the package re-export surface, and both round-trip tests. No
network calls, no stray files left behind (temp files are cleaned up in every test that creates
one).

## Related Standards

[EAD_SPECIFICATION.md](EAD_SPECIFICATION.md), [EAL's Examples.md](../20_Attribute_Language/Examples.md),
[EAR's Examples.md](../40_Enterprise_Attribute_Registry/Examples.md),
[EAD's Examples.md](../50_Enterprise_Attribute_Definitions/Examples.md) (the fixtures this Build
reuses).
