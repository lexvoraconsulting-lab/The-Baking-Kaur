# AR-004: Enterprise Attribute Language (EAL) Build-001 Review

Date: 2026-07-27
Scope: `docs/20_Attribute_Language/*.md` (all 20 documents), `ai/eal/{__init__.py,models.py,
models_pydantic.py,test_eal.py}`, `ai/eal/schemas/*.schema.json`, `ai/eal/examples/*` — Build-001
of the Enterprise Attribute Language, reviewed against the governance library (VIG-000–VIG-009),
the Sprint 2.1 taxonomy architecture (AR-002, AR-003), and its own generated schemas/examples.

## Method

Same self-audit method as AR-002/AR-003: every document and code file in scope was authored this
session, so the review reads them adversarially for contradiction, gaps, and unstated assumptions
rather than re-confirming intent, plus a grep-verified cross-reference check (every internal
`docs/20_Attribute_Language/*.md` link resolves to a real file; every `VIG-0\d\d` and
`docs/10_Taxonomy/*.md` reference resolves) and a runnable check
(`python -m ai.eal.test_eal` against the actual code, not just the docs describing it).

## Critical Issues

None found. No document contradicts the governance library or the Sprint 2.1 taxonomy
architecture, no cross-reference is broken, and `python -m ai.eal.test_eal` passes against every
example.

## Major Improvements (fixed in this pass)

1. **No test verified that an example's `attribute_id`/`relationship_id` still matched its own
   `canonical_path`/`source_id`+`type`+`target_id`.** Every example file hardcodes its ID rather
   than computing it at load time (correct — `EALAttributeRecordModel.attribute_id` is a required
   plain `str`, not auto-derived, matching how a real wire payload arrives). But nothing in
   `test_eal.py` re-derived the expected ID and compared it — an editor could change an example's
   `canonical_path` (say, fixing a typo) without updating its `attribute_id`, and every existing
   test would still pass, silently shipping a self-inconsistent example. All IDs were confirmed
   correct today by manual recomputation, but the drift-detection gap was real. **Fixed**: added
   `test_example_ids_match_computed_ids` to `ai/eal/test_eal.py`, recomputing and asserting against
   every attribute example (including each entry of the `api_payload_example.json` batch) and the
   relationship example.

## Minor Improvements (not fixed — correctly deferred, already stated in the docs they concern)

These are pre-existing, explicitly-flagged deferrals confirmed still accurate on this pass, not new
findings — collected here in one place per AR-002/AR-003's format:

1. **AI-derived ⇒ `confidence` is set is not a cross-field validator.** Only the range check
   (`[0.0, 1.0]`) is live. See [Confidence_Standard.md](Confidence_Standard.md),
   [Validation_Standard.md](Validation_Standard.md).
2. **`data_type == "enum"` ⇒ `vocabulary` is set is not a cross-field validator**, and no live
   registry validates `vocabulary`'s name or `value`'s membership in it. See
   [Enum_Standard.md](Enum_Standard.md).
3. **`type` (Relationship Record) is not validated against a live relationship-type vocabulary.**
   See [Relationship_Naming.md](Relationship_Naming.md).
4. **No controlled unit vocabulary exists yet**; no measurement-typed attribute exists in any
   Build-001 example to need one. See [Units_Standard.md](Units_Standard.md).

All four require a live registry (Sprint 2.2 Master Taxonomy / Build-002 EAR, per
[Roadmap.md](Roadmap.md)) that does not exist yet — building one now, with nothing real to validate
against, would itself violate [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md)
Principle 4 (no speculative scaffolding). Correctly deferred, not defects.

## Missing Principles Check (against Build-001's own stated scope)

Canonical path grammar (Attribute_Path_Syntax, Naming_Convention), namespace model, identifier
strategy, data types, enum/vocabulary linkage, units, null/unknown three-state, confidence,
provenance, human verification, relationship naming, external ID join, validation summary, worked
examples, Vision Engine migration mapping, forward roadmap, self-review — all present, each with a
corresponding document and, where applicable, a runnable test. Nothing in the original mission
scope (serialize Sprint 2.1's Entity/Attribute/Relationship model into a validated wire format) is
missing.

## Naming Consistency

Verified: all 20 documents plus `ai/eal/__init__.py`'s docstring use consistent terminology
(`EALAttributeRecord`, `EALRelationshipRecord`, `canonical_path`, `TBK_*_ID`, `Genome Attribute`
where taxonomy-level) with no renaming drift. Every document ends with a "Related Standards"
section citing the specific VIG principle(s) and/or Sprint 2.1 document(s) it implements or reuses
— checked via grep, present in all 20.

## Cross-Reference and Runnable-Check Verification

- Every `[text](path)` link inside `docs/20_Attribute_Language/*.md` resolves to an existing file
  (script-checked; 0 broken links).
- `docs/20_Attribute_Language/README.md`'s document index table's 19 document rows all resolve.
- `python -m ai.eal.test_eal` passes end-to-end: regenerates both JSON Schemas from the Pydantic
  models, validates all 6 example files against their models, and asserts canonical-path grammar,
  identifier determinism, example/ID consistency (new this pass), and value-state consistency.

## Final Readiness Score

**9/10.** The one Major finding (ID/example drift risk) was found and closed in this same pass,
verified by re-running `python -m ai.eal.test_eal` after the fix. The remaining point is withheld
for the four legitimately deferred cross-field/registry validations — not defects, but real gaps
until Sprint 2.2's Master Taxonomy and Build-002's registry exist to validate against, consistent
with the one point withheld in both AR-002 and AR-003 for their own analogous deferred items.

## Go / No-Go Recommendation

**GO** for closing Build-001. The EAL wire format is internally consistent, fully cross-referenced
to the governance library and Sprint 2.1 taxonomy with no duplication, mechanically validated
end-to-end by its own test suite (now including drift detection), and its remaining gaps are
correctly identified as depending on future work (Sprint 2.2 taxonomy content, Build-002 EAR
registry) rather than being omissions in this build. Build-002 should not begin until a real
Sprint 2.2 Master Taxonomy exists for it to validate against — starting it earlier would repeat the
exact premature-scaffolding risk this review confirms Build-001 correctly avoided.
