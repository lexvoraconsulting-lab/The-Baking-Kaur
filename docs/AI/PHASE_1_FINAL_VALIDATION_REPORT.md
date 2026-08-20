# TBK Cake Genome — Phase 1 Final Validation Report (live VPS runtime)

Date: 2026-08-20
Runtime: Hostinger VPS Ollama, reached over an SSH tunnel to `127.0.0.1:11434`
Safety: no taxonomy change, no Shopify/theme change, no reinstall, no model download, port 11434
never exposed. Branch `feature/vision-engine-v1`, no merges.

---

## Verdict

# CONDITIONAL PASS — PHASE 1 NOT LOCKED

**Image 1 executed live against `qwen3.5:4b` and passed all 17 gates.** Images 2 and 3 did **not
execute**: the SSH tunnel dropped after image 1 completed and did not recover across repeated
checks. One of three images is not a three-image regression, so Phase 1 does not lock.

No gate failed. The shortfall is coverage, not correctness.

---

## A. Exact model used

| Field | Value |
|---|---|
| Endpoint | `http://127.0.0.1:11434/api/generate` (source: `OLLAMA_BASE_URL`) |
| Model | `qwen3.5:4b` (source: `OLLAMA_MODEL`) |
| Ollama version | 0.32.14 |
| Reported by `/api/tags` | family `qwen35`, 4.7B, `Q4_K_M`, 3.39 GB |
| Recorded in provenance | `"provider": "ollama", "model": "qwen3.5:4b"` |

Every run prints its resolved runtime and the source of each value, so a run's target is never
ambiguous:

```
runtime : http://127.0.0.1:11434/api/generate [OLLAMA_BASE_URL] model=qwen3.5:4b [OLLAMA_MODEL]
```

## B. Exact images / fixtures used

The three canonical images already in the repository. No fixture, no replay — image 1 was a live
model call (`offline_replay: false`).

| Image | Bytes | `TBK_IMAGE_ID` | Executed |
|---|---|---|---|
| `ai/vision/images/1.png` | 2,331,134 | `TBK-2544c08921611adf` | **yes, live** |
| `ai/vision/images/2.png` | 2,342,389 | — | **no — tunnel down** |
| `ai/vision/images/3.png` | 2,024,534 | — | **no — tunnel down** |

## C. Pipeline stages executed (image 1)

All stages of the existing implementation, unmodified in structure:

```
image_validation → image_preprocessing → prompt_render (taxonomy digest, 30 groups)
→ vision_model (live) → raw_observations → prompt_leakage_screen
→ taxonomy_match → unknown_preserved → dynamic_discovery
→ cake_genome → design_identity_lock → validation → persistence_ready_output
```

Artifacts: `ai/cake_genome/output/vps_001/` — 9 files (`00_test_report.json` …
`08_diagnostics.json`).

## D. Live vision test

**PASS.** Raw response 4,762 characters, `parse_ok: true`, complete JSON envelope, no truncation.

## E. Observations (image 1)

**14 observations**, 13 present-valued and all scored. Model-flagged `unmatched`: 0.

| Group.attribute | Value | Match state | Conf |
|---|---|---|---|
| Decoration.decoration_type | Balloon Arch, Photo Strip, Floral Bouquet, Tuxedo Cake Design | matched¹ | 0.95 |
| Decoration.decoration_style | Fondant Figures, Fresh Flowers | **unmatched** | 0.90 |
| Colour.primary_colour | White | matched | 0.95 |
| Colour.secondary_colour | Black | matched | 0.95 |
| Colour.secondary_colour | Gold | matched | 0.95 |
| Writing.visible_text | "Happy Birthday to Our Hero in House… We love you, Dad." | matched | 0.95 |
| Occasion.occasion | Birthday | matched | 0.98 |
| Recipient.recipient | Him | matched | 0.95 |
| Theme.theme | Elegant | matched | 0.90 |
| Packaging.packaging_type | Premium Box | matched | 0.90 |
| Flowers.flower_type | Rose | matched | 0.95 |
| Flowers.flower_type | Baby's Breath | matched | 0.95 |
| Tier.tier_count | 1 | matched | 0.95 |
| Finish.finish | Satin | matched | 0.85 |

¹ `decoration_type` is a free-text attribute with no vocabulary, so any string "matches". Four
distinct features were concatenated into one value — see §L, limitation 2.

## F. Dynamic Structure Discovery

**1 candidate discovery**, generated from a genuine vocabulary gap:

```json
{
  "proposal_kind": "term",
  "canonical_name": "fondant_figures_fresh_flowers",
  "label": "Fondant Figures, Fresh Flowers",
  "status": "observed",
  "confidence": 0.9,
  "requires_gate": false,
  "likely_duplicate_of": null,
  "promoted_to": null,
  "why_unmatched": "'Fondant Figures, Fresh Flowers' is not a term or synonym in the
                    'Decoration Style' vocabulary used by 'decoration_style'",
  "evidence": [{
    "image_id": "TBK-2544c08921611adf",
    "raw_fragment": "The cake has a fondant tuxedo design and is surrounded by fresh white
                     roses and baby's breath.",
    "provenance": { "provider": "ollama", "model": "qwen3.5:4b",
                    "prompt_version": "extractor_v1-51c3fe933bbc",
                    "schema_version": "v1", "taxonomy_version": "1.0",
                    "extracted_at": "2026-08-20T15:09:15Z" }
  }]
}
```

Evidence, provenance and confidence are all carried. `status: "observed"` and `promoted_to: null` —
it is a candidate, not canonical.

## G. Candidate taxonomy extension

| Requirement | Result |
|---|---|
| `candidate_new_value` (term) | **Demonstrated live** — the proposal above |
| `candidate_new_attribute` | **Not demonstrated live** — no observation named a group/attribute outside the taxonomy. Mechanism unit-tested (`test_no_observation_is_ever_discarded`) |
| `candidate_new_structure` (group / category / relationship_type / entity_type) | **Not demonstrated live** — same reason. Mechanism unit-tested (`test_frozen_literal_kinds_require_a_gate`) |
| Candidates remain non-canonical | **Verified** — `status: observed`, `promoted_to: null` |
| Evidence / provenance / confidence carried | **Verified** |
| Goes through review before promotion | **Verified** — no promotion path is invoked anywhere |
| Genuine unknowns not discarded | **Verified** — the unmatched observation became a proposal rather than being dropped or forced into a wrong field |

**Honest reading:** the discovery mechanism worked on a real gap, but this image did not exercise
the `attribute` or `structure` proposal kinds. Those remain test-verified, not runtime-verified. No
structure was manufactured to make the test look better.

## H. Design Identity Lock

```
LOCK-ffd092d8fad35736b018   completeness 1.0   9 locked attributes
palette: White, Black, Gold
locked:  decoration_type, finish, occasion, packaging_type, primary_colour,
         recipient, theme, tier_count, visible_text
unresolved: "Fondant Figures, Fresh Flowers",
            "secondary_colour (conflicting values)",
            "flower_type (conflicting values)"
```

**The conflict guard fired correctly on live data.** `secondary_colour` was reported twice (Black,
Gold) and `flower_type` twice (Rose, Baby's Breath). Both were excluded from the fingerprint rather
than silently resolved to whichever came last, and both surfaced in `uncertain_attributes`.

## I. Prompt-leakage detection (defect D-3)

```json
{ "prompt_leakage": [], "prompt_leakage_count": 0, "unparsed_count": 0, "parse_ok": true }
```

**`prompt_leakage_count = 0`.** No prompt, template or example text entered observations, the Cake
Genome, the Design Identity Lock or the discovery candidates. Gate 13 passed.

This is the first live verification of the D-3 fix, and it held on a **different model family** from
the one the fix was developed against — evidence the defence is not model-specific.

## J. Confidence

```json
{ "mean_attribute_confidence": 0.9369, "attributes_present": 13, "attributes_scored": 13,
  "attributes_unscored": 0, "resolution_rate": 1.0, "proposals_raised": 1 }
```

Range 0.85–0.98. Every present-valued attribute carries a score. Two attributes reported as
uncertain (both conflicts, not low confidence).

## K. Section population, provenance, taxonomy mutation

**10 sections populated:** `dimensions`, `frosting`, `colors`, `piping`, `decorations`, `flowers`,
`theme`, `occasion_intelligence`, `recipient_tags`, `other_observed_groups`.

**Provenance complete:** provider, model, prompt_version, schema_version, taxonomy_version,
extracted_at, extraction_version, parse_ok. `model_version` is null (Ollama does not report one).

**Taxonomy mutation: NONE.** `git diff --quiet -- ai/taxonomy/` clean after the run.
`verification_status: "unverified"` on the genome and every attribute.

**Validation:** passed, **0 errors, 0 warnings**.

## Gate table (image 1, live)

| # | Gate | Result |
|---|---|---|
| 1 | image_loaded | PASS |
| 2 | vision_model_received_image | PASS |
| 3 | vision_response_received | PASS |
| 4 | raw_observations_generated | PASS |
| 5 | observations_normalized | PASS |
| 6 | taxonomy_matching_works | PASS |
| 7 | unknown_observations_preserved | PASS |
| 8 | candidate_discoveries_generated | PASS |
| 9 | confidence_exists | PASS |
| 10 | provenance_exists | PASS |
| 11 | cake_genome_generated | PASS |
| 12 | design_identity_lock_generated | PASS |
| 13 | validation_executed | PASS |
| 14 | validation_passed | PASS |
| 15 | json_valid | PASS |
| 16 | no_taxonomy_mutation | PASS |
| 17 | no_prompt_leakage_in_observations | PASS |

**17/17 on image 1. Images 2 and 3: not executed.**

## Comparison against the previous regression

| Metric | qwen2.5vl:3b (local, 3 images) | qwen3.5:4b (VPS, image 1) |
|---|---|---|
| Observations | 3 / 2 / 2 | **14** |
| Taxonomy matches | 3 / 2 / 2 | **13** |
| Sections populated | 4 / 3 / 3 | **10** |
| Lock attributes | 3 / 2 / 2 | **9** |
| Palette entries | 0 / 0 / 0 | **3 (White, Black, Gold)** |
| Mean confidence | 0.967 / 0.975 / 0.965 | 0.937 |
| Prompt leakage | **1 per image (D-3)** | **0** |
| Conflicts detected | 0 | **2, correctly excluded** |
| Validation | 0 err | 0 err, 0 warn |

`qwen3.5:4b` is a materially better extractor: 4.7× the observations, colour finally reported
(previously absent on all three images), and the taxonomy-gap signal is real rather than leaked.

## L. Defect found and fixed during this run

**D-7 — empty `response` with structured output on a reasoning model.**

The first live attempt returned a 0-byte response and 7/17 gates. Isolated with four controlled
probes against the live runtime rather than assumed:

| Probe | `format` | `think` | response | thinking |
|---|---|---|---|---|
| A | off | on | 350 | 5,958 |
| B | **on** | on | **0** | 741 |
| C | **on** | on | **0** | 2,106 |
| D | **on** | **off** | **2,104 ✓** | 0 |

**Root cause:** `qwen3.5:4b` is a reasoning model. With Ollama structured output (`format`) *and*
thinking enabled, the model routes its content into the response's `thinking` field and returns an
empty `response`. This is a model-family capability difference, not a pipeline defect.

**Fix:** an optional `think` passthrough in `OllamaProvider`, config-driven, following the existing
`options` / `keep_alive` pattern. Sent only when explicitly configured, so non-reasoning models are
unaffected. The pipeline was **not** rewritten to make the test pass.

### Remaining limitations

1. **Images 2 and 3 unexecuted** — SSH tunnel dropped after image 1 and did not recover. The single
   reason Phase 1 does not lock.
2. **Free-text attributes match trivially.** `decoration_type` has no vocabulary, so "Balloon Arch,
   Photo Strip, Floral Bouquet, Tuxedo Cake Design" — four distinct features — counted as one
   match. A Decoration vocabulary would convert this into four proposals or four matches. Real
   taxonomy-content gap (D14), not a pipeline fault.
3. **Multi-value cramming.** The model puts several values in one string rather than emitting
   repeated observations. The conflict guard catches this when the same attribute repeats, but not
   when values are comma-joined into a single value.
4. **`candidate_new_attribute` and `candidate_new_structure` not demonstrated live** — see §G.
5. **Model reported no `unknown` / `null` states**, so those branches were not exercised live.

## Next implementation phase

**First — finish this regression (~10 min):** re-open the tunnel and run images 2 and 3. If both
reach 17/17 with `prompt_leakage_count: 0`, this report becomes **FULL PASS — PHASE 1 LOCKED**.

```bash
ssh -N -L 11434:127.0.0.1:11434 <user>@<host>
export OLLAMA_BASE_URL=http://127.0.0.1:11434 OLLAMA_MODEL=qwen3.5:4b
python -m ai.cake_genome.run_phase1 --image ai/vision/images/2.png --out ai/cake_genome/output/vps_002
python -m ai.cake_genome.run_phase1 --image ai/vision/images/3.png --out ai/cake_genome/output/vps_003
```

**Then Phase 2 = D7, Build-006 Enterprise Validation Engine** — unchanged, and reinforced: this run
produced live conflict detection with no per-group confidence thresholds behind it, and the Phase-1
validation module now carries five dimensions in a place its own docstring marks as temporary.

## Related

[PHASE_1_VALIDATION_REPORT.md](../80_Dynamic_Structure_Discovery/PHASE_1_VALIDATION_REPORT.md),
[VisionExtractionContract.md](VisionExtractionContract.md), [Configuration.md](Configuration.md),
[ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md),
[Dynamic Structure Discovery](../80_Dynamic_Structure_Discovery/SPECIFICATION.md).
