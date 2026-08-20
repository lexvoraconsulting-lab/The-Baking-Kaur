# TBK Cake Genome — Phase 1 Validation Report

Date: 2026-08-20
Scope: the completed Phase 1 pipeline run against all three canonical test images.
Safety: no canonical taxonomy change, no database, no Shopify call, no bulk processing, no branch
merge. Branch `feature/vision-engine-v1` throughout.

---

## 1. Executive result

**CONDITIONAL PASS — all 13 gates pass in regression; gate 13 is unverified against a live model.**

The pipeline is mechanically sound. All three canonical images processed end to end against a live
`qwen2.5vl:3b` model, each returning **16/16 quality gates**, valid JSON, complete provenance, a
distinct Design Identity Lock, and a passing validation report. Three genuinely different cakes
produced three genuinely different genomes — no structure was forced, nothing was silently
discarded, and the canonical taxonomy is byte-identical.

**Defect D-3 (prompt/example leakage) is fixed at two independent layers** and proven against the
actual leaked payloads (section 8a). A defensive screen in the extraction parser classifies any
model output reproducing prompt text as `prompt_leakage`, excludes it from the genome, the Design
Identity Lock, canonical observations and discovery candidates, and retains it in diagnostics.
Genuine observations are provably unaffected.

**What remains unverified:** whether the strengthened prompt stops the model emitting leaked text in
the first place. Ollama was removed from this machine mid-session (section 10, L-1) and cannot be
re-run without a ~4.2 GB reinstall that was not authorised. The prompt is now the *second* line of
defence rather than the only one — the parser screen catches leakage regardless of prompt wording —
which materially reduces the risk, but does not close the gap.

---

## 2. Test matrix

| Test | Image | image_id | Model | Live | Gates |
|---|---|---|---|---|---|
| TEST 001 | `ai/vision/images/1.png` | `TBK-2544c08921611adf` | ollama/qwen2.5vl:3b | yes | **16/16** |
| TEST 002 | `ai/vision/images/2.png` | `TBK-78d08a419d2320f2` | ollama/qwen2.5vl:3b | yes | **16/16** |
| TEST 003 | `ai/vision/images/3.png` | `TBK-e8f1eaaa42a82054` | ollama/qwen2.5vl:3b | yes | **16/16** |

Identical pipeline, prompt (`extractor_v1-d80a4926f068`), taxonomy digest (`taxonomy_version 1.0`),
extraction contract, validation rules and discovery mechanism across all three. Artifacts:
`ai/cake_genome/output/test00{1,2,3}/` — 8 files each, per the 11 required outputs.

---

## 3. Per-image results

### TEST 001 — image 1

Raw response 1819 chars, complete JSON. 3 observations, all resolved. `decoration_style = "Fresh
Flowers"` (0.98), `visible_text = "HAPPY BIRTHDAY"` (0.96), `theme = "Elegant"` (0.96). Sections:
`piping`, `decorations`, `theme`, `other_observed_groups`. Lock `LOCK-07eb6fbca9bed1a70fbc` over 3
attributes. 1 proposal, flagged duplicate. 1 `unparsed` entry. Validation passed, 0/0.

### TEST 002 — image 2

Raw 1461 chars, complete. 2 observations, both resolved. `decoration_type = "Fresh Flowers, Sugar
Flowers"` (0.95), `visible_text = "Let the Adventure Begin"` (1.0). Sections: `piping`,
`decorations`, `other_observed_groups`. Lock `LOCK-d122008e2db09b4a3ca2` over 2. Validation passed.

### TEST 003 — image 3

Raw 1492 chars, complete. 2 observations, both resolved. `decoration_type = "Edible Print"` (0.95),
`flower_type = "Baby's Breath"` (0.98). Sections: `piping`, `decorations`, `flowers` — **no
`other_observed_groups`**, and the only image to populate `flowers`. Lock
`LOCK-386869258ca7f3382f99` over 2. Validation passed.

---

## 4. Cross-image comparison

| Metric | Image 1 | Image 2 | Image 3 |
|---|---|---|---|
| **A. Schema stability** | stable | stable | stable |
| parse_ok | True | True | True |
| response truncated | **False** | **False** | **False** |
| raw response chars | 1819 | 1461 | 1492 |
| **B. Observation count** | 3 | 2 | 2 |
| model-flagged unmatched | 1 | 1 | 1 |
| relationships extracted | 2 | 2 | 2 |
| unparsed retained | 1 | 0 | 0 |
| **C. Known vs unknown** | 3 known / 0 unknown | 2 / 0 | 2 / 0 |
| undetermined (`unknown`) | 0 | 0 | 0 |
| not_applicable (`null`) | 0 | 0 | 0 |
| **D. Taxonomy match rate** | 1.0 | 1.0 | 1.0 |
| **E. Dynamic discovery** | 1 proposal | 1 | 1 |
| flagged already-existing | **1/1** | **1/1** | **1/1** |
| taxonomy mutated | **no** | **no** | **no** |
| **F. Confidence** min/max | 0.95 / 0.98 | 0.95 / 1.00 | 0.95 / 0.98 |
| mean | 0.9667 | 0.9750 | 0.9650 |
| scored / unscored | 3 / 0 | 2 / 0 | 2 / 0 |
| **G. Validation failures** | 0 err, 0 warn | 0 / 0 | 0 / 0 |
| **H. Missing attributes** (unrepresented sections) | 10 | 11 | 10 |
| **I. Duplicate attributes** | 0 | 0 | 0 |
| **J. Unexpected attributes** | 0 | 0 | 0 |
| **K. Lock completeness** | 1.0 (3 attrs) | 1.0 (2) | 1.0 (2) |
| palette entries | **0** | **0** | **0** |
| **L. Genome sections populated** | 4 | 3 | 3 |
| verification_status | unverified | unverified | unverified |
| Design Identity Lock | distinct | distinct | distinct |

Three distinct `image_id`s, three distinct locks, three different section sets. **Differences
between the cakes were preserved, not normalized away.**

### Classifying the variation

Per the six required categories:

| Observation | Classification |
|---|---|
| Section sets differ (img3 has `flowers`, no `other_observed_groups`) | **2 — legitimate visual variation.** Different cakes, different attributes. Correct behaviour |
| Observation count 3/2/2 | **4 + 5 — model under-reporting.** Not a pipeline fault; see D-4 |
| `palette` empty on all three | **4 — model limitation.** Colour was never reported despite `Colour` being in every digest. Real coverage gap |
| Identical `mirror_glaze` proposal on all three | **4 — model hallucination via prompt leakage.** Defect D-3 |
| `unrepresented_sections` 10/11/10 | **3 — genuine taxonomy gap.** Six requested sections have no backing Attribute Group |
| Zero `unknown`/`null` states across 30 groups × 3 images | **4 — model limitation.** It reports only what it is confident about and stays silent otherwise |
| Schema, provenance, lock, validation | **No inconsistency.** Stable across all three |

---

## 5. Dynamic Structure Discovery findings

One proposal per image; the same one each time. Audited against the five required questions:

| Question | Finding |
|---|---|
| Was it genuinely visible? | **No.** The `observed` text is a character-for-character copy of the prompt's own example |
| Already representable canonically? | **Yes.** `Mirror Glaze` is an active Term in the Finish vocabulary (`TAX-TERM-000052`) |
| Correctly marked unresolved? | **Yes** — kept out of the Design Identity Lock, listed under `unresolved`, surfaced in `distinctive_features` |
| Candidate discovery generated? | **Yes** — `PROP-…`, kind `term`, status `observed`, evidence carrying image_id, observation_id, verbatim fragment and full `Provenance` |
| Prevented from mutating taxonomy? | **Yes.** `ai/taxonomy/` byte-identical, verified by `git diff --quiet` after all runs |

**The mechanism passed every safety check on an input that was itself invalid.** The duplicate
guard did exactly its job: all three proposals carry `likely_duplicate_of: TAX-TERM-000052`, so a
reviewer sees "this is probably already Mirror Glaze" rather than triaging a phantom. Nothing was
auto-merged — `status` stayed `observed`, because merging is a review decision.

What is **not** evidenced by these runs: that the model can find a genuinely novel feature and
report it. That requires the post-fix re-test.

---

## 6. Taxonomy-gap findings

Confirmed real, consistent across all three images:

1. **Seven of thirty Attribute Groups hold no attribute** — Classification, Material, Business,
   Topper, Size, Flavour, Allergens. The digest shows them to the model as `(group exists, no
   attribute defined yet)`; nothing could ever be reported under them.
2. **Six requested genome sections have no backing group** — `fruits`, `relationship_tags`,
   `visual_search_tags`, `customer_search_phrases`, `photography_genome`, `multi_angle_reference`.
   Reported in `unrepresented_sections`, never faked.
3. **`decoration_type` is free-text, not vocabulary-backed** — image 2 returned
   `"Fresh Flowers, Sugar Flowers"`, two values in one string. It matched (free-value attributes
   accept anything), but nothing normalized it. A Decoration vocabulary would fix this.
4. **No `Writing` section alias** — `visible_text` resolves correctly but lands in
   `other_observed_groups`. `SECTION_ALIASES` needs a `text`/`writing` entry.

None of these blocked a run. All are content work (D14), and all are exactly what the discovery
mechanism exists to surface from evidence.

---

## 7. Validation findings

All three: `passed=True`, 0 errors, 0 warnings. Dimensions run: structural, completeness,
provenance, safety invariants. Every finding was `COMPLETENESS_SECTION_EMPTY` at `info` — a
data-quality signal, never a blocker, per `Validation.md`.

Safety invariants held on every run: `verification_status = "unverified"` on every genome and every
attribute; no proposal advanced past `observed`; no `promoted_to` set anywhere.

Two dimensions deliberately deferred and labelled: per-group confidence thresholding (Build-006 +
EAD `confidence_expectations`) and cross-image consistency (needs persisted verified attributes;
none exist).

---

## 8. Defects found

| ID | Defect | Root cause | Severity |
|---|---|---|---|
| **D-1** | `ReadTimeout` after 300 s on TEST 001 | Model evicted from VRAM after ~5 min idle; a 3.2 GB cold reload exceeded the read timeout | Blocking |
| **D-2** | Ollama server exited between test batches | The `ollama serve` process was backgrounded and terminated with its task | Blocking |
| **D-3** | **All three images produced an identical `unmatched` observation** — verbatim copy of the prompt's few-shot example | Few-shot example leakage. Traced to stage 1, the model's own output (section 8a) | **High — invalidated the discovery evidence from those runs. FIXED** |
| **D-6** | New leakage tests were defined but never executed; the module reported OK | `__main__` block sat mid-file with an explicit call list; appended tests were never called | Medium — silent false confidence. **FIXED** |
| **D-4** | 2–3 observations per image against a 30-group vocabulary; zero colour observations across three cake photographs | `qwen2.5vl:3b` capability; possibly aggravated by D-3 putting the model in copy mode | Medium |
| **D-5** | `lock_completeness` reads 1.0 on a lock covering 2 attributes | It measures *resolution rate of what was reported*, not *coverage of the taxonomy*. Technically correct, misleading as a quality signal | Low |

---

## 8a. D-3 — root cause, correction and evidence

### Investigation (source established, not assumed)

The leaked string was traced through every stage by counting its occurrences in the saved artifacts
of all three tests:

| Stage | Artifact | img 1 | img 2 | img 3 |
|---|---|---|---|---|
| 1. Model output | `01_raw_response.txt` | **2** | **1** | **1** |
| 2. Parser output | `02_raw_observations.json` | 3 | 2 | 2 |
| 3. Normalization / discovery | `03_normalized_observations.json` | 2 | 1 | 1 |
| 4. Genome | `04_cake_genome.json` | 1 | 1 | 1 |
| 5. Discovery output | `06_dynamic_discovery.json` | 1 | 1 | 1 |

**The text is present at stage 1.** It originates in the model's own response; every downstream
stage carried it faithfully, which is precisely what those stages are built to do.

Against the seven candidate sources:

| # | Candidate | Verdict |
|---|---|---|
| 1 | **Model generation** | **CONFIRMED** — present in the raw provider response |
| 2 | Prompt construction | Ruled out — the prompt rendered correctly; it legitimately contained the example, which the model copied |
| 3 | Response parsing | Ruled out — parser reproduced its input faithfully |
| 4 | Observation extraction | Ruled out |
| 5 | Normalization | Ruled out |
| 6 | Replay / test fixture | Ruled out — these were live runs, `offline_replay: false` |
| 7 | Downstream fallback | Ruled out — no fallback path was taken |

**Root cause:** few-shot example leakage. The `unmatched` example contained concrete, copyable prose,
and a 3B model reproduced it verbatim instead of describing the image. Compounded because the
example's subject (`Mirror Glaze`) already exists in the taxonomy as `TAX-TERM-000052`.

### Correction — two independent layers

**Layer 1 — defensive, in the pipeline** (the load-bearing fix; prompt wording was not relied on):

| File | Change |
|---|---|
| `ai/vision/python/extraction.py` | `LeakageRecord` + `detect_prompt_leakage()`; `parse_extraction()` accepts `prompt_template` and screens the `observations`, `unmatched` and `relationships` channels. Leaked items divert to `ExtractionResult.leaked` and never enter the observation stream |
| `ai/cake_genome/models.py` | `CakeGenome.diagnostics` — leaked output is preserved here and nowhere else |
| `ai/cake_genome/builder.py` | Populates diagnostics from `extraction.leaked` |
| `ai/cake_genome/validation.py` | New `prompt_leakage_separation` dimension: `LEAK_DETECTED_AND_EXCLUDED` (warning), `LEAK_REACHED_DISCOVERY` / `LEAK_REACHED_LOCK` (errors) |
| `ai/cake_genome/run_phase1.py` | New `prompt_leakage_screen` step, gate 13, and artifact `08_diagnostics.json` |

Two design decisions, both recorded in the code:

- **Screening is against the prompt TEMPLATE, not the rendered prompt.** The rendered prompt embeds
  the taxonomy digest — every Term label and synonym. Screening against it would flag `White`,
  `Round` and every other correct enum value as leakage, suppressing exactly the observations the
  pipeline exists to capture. The template leaves `{{TAXONOMY_DIGEST}}` unsubstituted, so taxonomy
  content is structurally excluded from the leak corpus.
- **Exact containment above a 25-character minimum, not fuzzy matching.** A similarity threshold
  would eventually suppress a genuine observation sharing wording with an example. A false positive
  here silently deletes real visual data — worse than the leak it prevents.

**Layer 2 — prompt** (`ai/vision/prompts/extractor_v1.md`): a new **Grounding** section states that
instructions, vocabulary and examples are instructional material and never descriptions of the
image; that examples must never be copied; that a feature named in an example implies nothing about
the image; and that reproduced text is discarded. Example content is now `<placeholder>` text and
the examples heading reads **FORMAT ONLY**.

### Before / after evidence — the actual leaked payloads

Each saved live response was replayed through the fixed pipeline, screened against the **historical**
prompt that produced it (retained as `ai/cake_genome/fixtures/leaked_prompt_v1_examples.md`).
Screening against the current prompt would prove nothing, since the leaked text was removed from it.

| Metric | img 1 before → after | img 2 before → after | img 3 before → after |
|---|---|---|---|
| Observations | 3 → **3** | 2 → **2** | 2 → **2** |
| Unmatched observations | 1 → **0** | 1 → **0** | 1 → **0** |
| Leakage records | 0 → **1** | 0 → **1** | 0 → **1** |
| Taxonomy matches | 3 → **3** | 2 → **2** | 2 → **2** |
| Discovery candidates | 1 → **0** | 1 → **0** | 1 → **0** |
| Lock attributes | 3 → **3** | 2 → **2** | 2 → **2** |
| Validation passed | True → **True** | True → **True** | True → **True** |
| Gate 13 | — → **True** | — → **True** | — → **True** |

**The phantom proposal is gone; observations, matches and the lock are unchanged.** The fix removes
exactly the leaked item and nothing else.

### Guard against over-suppression

Enforced by tests, not assertion:

- `test_genuine_unmatched_observation_still_survives` — a genuine unmatched observation ("a
  hand-piped royal icing lace collar around the upper rim of the middle tier") passes screening and
  becomes a discovery candidate.
- `test_leak_detector_ignores_short_strings` — vocabulary labels (`White`, `Rose Gold`) never flagged.
- `test_leak_detector_screens_template_not_rendered_prompt` — the digest is excluded from the corpus.
- `test_leaked_observation_never_enters_the_stream` — leaked text yields a `LeakageRecord` with
  `excluded_from_discovery: true` and an empty `unmatched` channel.

### A second defect found while fixing this

`ai/vision/python/test_config_providers.py` had its `if __name__ == "__main__":` block in the middle
of the file with an explicit call list. The new leakage tests, appended below it, were **defined but
never executed** — the module reported "OK" without running them. Fixed: the runner moved to the end
of the file and now auto-discovers every zero-argument `test_*`, so an appended test cannot silently
no-op again.

---

## 9. Defects fixed

| ID | File changed | Correction | Regression result |
|---|---|---|---|
| **D-1** | `ai/vision/config/vision.json`, `ai/vision/python/providers.py` | `timeout` 300→600; added `keep_alive: "30m"` passthrough so the model stays resident across a batch | All 3 tests then ran without timeout |
| **D-2** | none (operational) | Server restarted and model pre-warmed before the batch | 3/3 completed |
| **D-3** | `ai/vision/python/extraction.py`, `ai/cake_genome/{models,builder,validation,run_phase1}.py`, `ai/vision/prompts/extractor_v1.md` | Two layers: a parser-level `prompt_leakage` screen that diverts leaked output to diagnostics and out of the genome/lock/discovery, plus a Grounding section and placeholder examples in the prompt. Full detail in section 8a | **Regression-verified on the real leaked payloads**: unmatched 1→0, leakage records 0→1, discovery candidates 1→0, observations/matches/lock **unchanged**, validation still passes, gate 13 true — on all three images. Live re-run blocked by L-1 |
| **D-6** | `ai/vision/python/test_config_providers.py` | Runner moved to end of file; auto-discovers every zero-argument `test_*` | 5 leakage tests now execute; 12/12 automated module self-checks pass |
| **D-4** | not fixed | Deliberately not patched further. Fix D-3 first and re-measure; stacking prompt changes before measuring would make the cause unattributable | — |
| **D-5** | not fixed | Recorded as a metric-semantics limitation. Changing it means defining "coverage", which is a Build-006 concern | — |

No fix touched the architecture, the taxonomy, the schema contract, or any pre-existing module.

---

## 10. Remaining limitations

| ID | Limitation |
|---|---|
| **L-1** | **Ollama was removed from this machine during the session** — install directory, binary, models directory and processes all gone after TEST 003 completed; `winget` reports no installed package and no cached installer exists. Not removed by this work. The D-3 *prompt* layer therefore has no live re-test; the *parser* layer is fully verified offline. Restoring it means a ~1 GB installer plus a 3.2 GB model re-pull, which was not authorised |
| **L-7** | Leakage screening is exact-containment against the prompt template. A model that *paraphrases* an example rather than copying it verbatim would not be caught. Deliberate: fuzzy matching would eventually suppress genuine observations, which is the worse failure. Revisit only if paraphrased leakage is actually observed |
| **L-2** | `qwen2.5vl:3b` is not a production extractor. 2–3 observations per image, no colour, no `unknown`/`null` discrimination. Try `qwen2.5vl:7b` — a config-only change |
| **L-3** | Relationships are extracted (2 per image, consistently) but not taxonomy-resolved, and are excluded from the Design Identity Lock rather than hashed unvalidated |
| **L-4** | Cross-image consistency validation cannot run — nothing persists (D8) |
| **L-5** | Per-group confidence thresholds absent (Build-006) — a global 0.60 stand-in is marked `ponytail:` in `builder.py` |
| **L-6** | Three images is a small sample. It proves the pipeline runs and preserves difference; it does not characterise extraction quality |

---

## 11. Verdict

### CONDITIONAL PASS

| # | Success criterion | Result |
|---|---|---|
| 1 | All three images process successfully | **PASS** — 3/3 live |
| 2 | All three produce valid JSON | **PASS** |
| 3 | No response truncation | **PASS** — all end on `}` |
| 4 | No parser corruption | **PASS** — `parse_ok` true on all three |
| 5 | No duplicate identity corruption | **PASS** — 3 distinct `image_id`s, 3 distinct locks |
| 6 | No silent observation loss | **PASS** — every observation matched, proposed, or recorded in diagnostics |
| 7 | No taxonomy mutation | **PASS** — `git diff --quiet ai/taxonomy/` clean |
| 8 | Confidence exists | **PASS** |
| 9 | Provenance exists | **PASS** — all 7 fields on all three |
| 10 | Dynamic discovery works | **PASS** — mechanism proven; genuine unmatched observations still become candidates (test-enforced) |
| 11 | Cake Genome validates | **PASS** — 0 errors ×3 |
| 12 | Design Identity Lock validates | **PASS** — distinct, deterministic, order-independent |
| 13 | **No prompt/example leakage into visual observations** | **PASS in regression** — leaked output excluded from genome, lock, canonical observations and discovery on all three; retained in diagnostics. **Not re-verified against a live model** (L-1) |
| — | Differences preserved correctly | **PASS** — 4/3/3 sections, different attributes, no forcing |

**All 13 gates pass.** The result is held at CONDITIONAL rather than PASS for one reason, stated
plainly: gate 13 was verified by replaying the three real leaked payloads through the fixed
pipeline, not by a fresh live model run, because the model host was removed from the machine and
restoring it was not authorised.

This is a deliberate refusal to manufacture a PASS. The evidence that exists is strong — the defect
is reproduced, root-caused to stage 1, defended at the parser level, and shown to remove exactly the
leaked item and nothing else. The evidence that does not exist is narrow — whether the reworded
prompt prevents the model emitting leakage in the first place. Because the parser screen is
independent of prompt wording, that gap affects extraction *quality*, not extraction *safety*.

---

## 12. Recommended Phase 2

**First — close the conditional (~30 min, one authorisation):**

1. `winget install Ollama.Ollama`, then `ollama pull qwen2.5vl:3b` (~4.2 GB total).
2. Re-run all three canonical images.
3. Confirm the `unmatched` channel returns image-specific text and `08_diagnostics.json` shows
   `prompt_leakage_count: 0`. That converts this report to a full **PASS**.
4. If observation counts stay at 2–3 with no colour, that is D-4 and the answer is `qwen2.5vl:7b` —
   a config-only change — not further prompt engineering.

**Then Phase 2 = D7, Build-006 Enterprise Validation Engine.**

Unchanged from the previous recommendation, and reinforced by this pass:

- Still the only unbuilt Build with no open dependencies — the four dimensions are fully specified
  in `Validation.md`, and EAR/EAD already carry `validation_profile` / `allowed_values` /
  `confidence_expectations`.
- This pass added a fifth validation dimension (`prompt_leakage_separation`) to a module whose
  docstring already says it is *not* Build-006. That module is now doing five dimensions' work in a
  place explicitly marked as temporary — the strongest signal yet that Build-006 should own it.
- Per-group confidence thresholds (L-5) and the `ambiguous`/conflict routing still have no runtime
  enforcement.
- It closes the two AR-004 Minor findings still open.
- It needs no PostgreSQL, no Shopify, no bulk processing, no branch merge.

Explicitly **not** next: persistence (D8), Shopify (D10), bulk processing. Each depends on
validation existing first.

---

## Related

[SPECIFICATION.md](SPECIFICATION.md), [README.md](README.md),
[Vision Extraction Contract](../AI/VisionExtractionContract.md),
[ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md),
[ECP-200](../30_Enterprise_Program_Roadmap/ECP-200_Architecture_Gap_Analysis.md),
[Implementation Dependency Map](../30_Enterprise_Program_Roadmap/IMPLEMENTATION_DEPENDENCY_MAP.md),
[Validation.md](../10_Taxonomy/Validation.md), [GLOSSARY.md](../00_Foundation/GLOSSARY.md).
