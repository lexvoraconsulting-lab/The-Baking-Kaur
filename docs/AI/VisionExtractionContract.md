# AI Vision Engine — Extraction Contract v1 (Build-008)

Date: 2026-08-20
Status: **Proposed** — specification only. `ai/vision/prompts/extractor_v1.md`,
`ai/vision/schemas/taxonomy_v1.json` and `ai/vision/schemas/tbk_image_schema_v1.json` remain
**0 bytes on disk** and were not written. This document specifies what goes in them.

This is the content layer [Roadmap.md](Roadmap.md) Phase 2 and
[EPR Build-008](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md) have both been
waiting on. It is also, per [ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md) interface
#1, the artifact n8n reads at job start instead of embedding a prompt in workflow JSON.

---

## The governing principle

> **Known fields are a controlled vocabulary, not a ceiling on visual intelligence.**

Every rule below serves that sentence. The model is told what the taxonomy currently knows so that
it can *name things consistently*, and is told explicitly that anything it sees which does not fit
must be reported rather than forced into the nearest field.

---

## 1. What exists today, and why it must be replaced

Two extraction implementations exist. Both are hard ceilings.

**Python** — `ai/vision/python/pipeline.py` falls back to an inline hardcoded cake-description
prompt because `extractor_v1.md` is empty, and returns **raw text** that no code path converts into
a record. Marked with a `ponytail:` comment as deletable once the real prompt is authored.

**n8n** — `TBK Qwen Vision Analysis.json` hardcodes:

> *"Analyze the cake image and return ONLY a JSON object with keys: layers (integer),
> frosting_type (string), decorations (array of strings), colors (array of strings), quality_score
> (float 0-1), confidence (float 0-1). No prose."*

Six keys. A cake with a mirror glaze, a fondant plaque, a sugar-flower cascade and a hand-piped
inscription produces four strings in `decorations[]` and loses every structural distinction between
them. `tbk_vision_results` then flattens even that into columns.

Neither can express "I saw something I have no name for" — which is the single capability this
contract exists to add.

---

## 2. What the extraction is scoped against

The real, authored, frozen Bakery taxonomy: **6 categories, 30 attribute groups, 17 controlled
vocabularies, 26 attributes, 96 terms, 24 typed relationships**
(`ai/taxonomy/content/bakery_v1.json`, Build-005).

The 30 groups already cover the required subject matter almost exactly:

| Requested coverage | Existing group | Attribute(s) | Vocabulary (terms) |
|---|---|---|---|
| geometry, shape | Geometry, Board | `shape`, `board_shape` | Shape (5) |
| tiers | Tier | `tier_count`, `tier_style` | Tier Style (4) |
| dimensions, size, weight, servings | Size, Weight, Servings | `weight_grams`, `servings_count` | — (numeric) |
| occasion | Occasion | `occasion` | Occasion (9) |
| theme | Theme | `theme` | Theme (11) |
| style | Style | `style` | Style (5) |
| colors | Colour | `primary_colour`, `secondary_colour` | Colour Name (10) |
| decorations | Decoration | `decoration_type`, `decoration_style` | Decoration Style (5) |
| flowers | Flowers | `flower_type` | Flower (5) |
| toppers | **Topper** | **none — group is empty** | — |
| figurines, characters | Characters | `character_name` | — (free text) |
| typography, text | Writing | `visible_text` | — (free text) |
| frosting, cream, ganache | Cream, Ganache | `icing_type`, `ganache_type` | Cream & Icing (4), Ganache (4) |
| finish | Finish | `finish` | Finish (5) |
| textures | Texture | `texture` | Texture (5) |
| techniques | **Material** | **none — group is empty** | — |
| structural components | Tier, Board | `tier_style`, `board_shape` | Tier Style (4) |
| edible / non-edible | **Material** | **none — group is empty** | — |
| packaging, presentation | Packaging | `packaging_type` | Packaging Type (4) |
| dietary, allergens | Dietary, **Allergens** | `dietary_labels` (Allergens empty) | Dietary (4) |
| flavour | Sponge, Filling, **Flavour** | `sponge_flavour`, `filling_flavour` | Flavour (6) |
| recipient | Recipient | `recipient` | Recipient (6) |
| delivery | Delivery | `delivery_attribute` | Delivery Attribute (4) |
| premium / luxury indicators | **none** | — | — |
| visual complexity | **none** | — | — |
| customization indicators | **none** | — | — |

**Seven of the thirty groups hold no attribute at all** — Classification, Material, Business,
Topper, Size, Flavour, Allergens. Three requested concepts (premium/luxury, visual complexity,
customization) have no group.

**This is not a blocker; it is the first real test of the discovery mechanism.** Rather than
pre-authoring ten attributes by guesswork, the extraction reports these as `unmatched` observations
and lets [Dynamic Structure Discovery](../80_Dynamic_Structure_Discovery/SPECIFICATION.md) surface
them as evidence-backed proposals from real photographs. That is the intended path, and it is
cheaper and better-grounded than inventing a vocabulary in advance.

---

## 3. Output contract

The extraction returns **two parallel channels**. This shape is the whole design.

```
                    ┌──────────────────────────────┐
   image ─────────▶ │      vision extraction        │
                    └───────────┬──────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              v                                   v
      observations[]                        unmatched[]
   facts the model could                facts the model saw but
   name in taxonomy terms               could NOT place in the taxonomy
              │                                   │
              v                                   v
     EALAttributeRecord                    StructureProposal
```

Plus a third, deliberately lossy-nothing channel: `unparsed[]`, for model output that became
neither.

### 3.1 Top-level envelope

```json
{
  "extraction_version": "1.0",
  "image_id": "TBK-<sha256[:16]>",
  "taxonomy_version": "v1",
  "schema_version": "v1",
  "prompt_version": "extractor_v1",
  "provider": "ollama",
  "model": "qwen2.5vl:3b",
  "model_version": null,
  "extracted_at": "2026-08-20T09:14:22Z",
  "observations": [],
  "unmatched": [],
  "relationships": [],
  "unparsed": [],
  "extraction_notes": null
}
```

The seven identity/version fields map 1:1 onto `ai.eal.models.Provenance` — they are **not a new
provenance scheme**. `image_id` is `compute_image_id()` from `ai/vision/python/pipeline.py`,
unchanged; because it is a content hash, re-extraction of the same bytes is idempotent for free.

### 3.1a Where verification state comes from

The extraction output carries **no** `human_verification` field, deliberately. Every record it
produces enters the platform at
[`HumanVerification(status="unverified")`](../20_Attribute_Language/Human_Verification_Standard.md)
— the dataclass default — because a model has no authority to assert its own review state.
Verification status is set later, by the review path, never by the extractor. A record arriving
from a provider with a `verified` claim would be discarded.

Low confidence does not set `pending_review` here either; that routing is
[Validation.md](../10_Taxonomy/Validation.md)'s confidence-thresholding dimension, enforced by
Build-006 (the Validation Engine), which does not yet exist.

### 3.2 `observations[]` — facts the model could name

```json
{
  "group": "Colour",
  "attribute": "primary_colour",
  "value": "white",
  "value_state": "present",
  "data_type": "enum",
  "vocabulary": "colour_name",
  "confidence": 0.91,
  "evidence": "a smooth white buttercream base covering all tiers",
  "region": null,
  "entity_type": "image"
}
```

- `value_state` is the existing three-state
  [Null_and_Unknown_Standard](../20_Attribute_Language/Null_and_Unknown_Standard.md) field.
  `"null"` means *this cake genuinely has no topper*; `"unknown"` means *I cannot tell whether it
  has one*. The model is required to distinguish these, and the prompt says so explicitly.
- `confidence` must be `null` when `value_state` is not `"present"` — there is nothing to be
  confident about. Enforced today by
  `EALAttributeRecordModel._value_state_consistency`.
- `evidence` is the model's own words for why. Verbatim, never paraphrased downstream. It is what
  makes a low-confidence record reviewable instead of merely doubtful.
- `entity_type` is constrained to `"image" | "region" | "object"` — `ai.eal`'s frozen literal.

### 3.3 `unmatched[]` — the capability that does not exist today

```json
{
  "observed": "a hand-piped royal icing lace collar around the upper rim",
  "closest_group": "Decoration",
  "closest_attribute": "decoration_style",
  "closest_term": null,
  "why_unmatched": "no term in the Decoration Style vocabulary describes a piped lace collar",
  "suggested_kind": "term",
  "suggested_label": "Lace Collar",
  "confidence": 0.74,
  "region": null
}
```

> **Corrected 2026-08-20 (implementation).** This example previously used "mirror glaze". `Mirror
> Glaze` is in fact an active Term in the Finish vocabulary, and the implemented matcher resolves
> it — so it was a false illustration of an unmatched observation. Replaced with a genuinely
> unmatched feature, verified against the real catalog.

- `suggested_kind` maps directly onto `ProposalKind` in the
  [Discovery specification](../80_Dynamic_Structure_Discovery/SPECIFICATION.md) §7.2.
- `closest_*` may all be `null`. A cake feature belonging to none of the 30 groups is a legitimate
  and expected output, and is what a `attribute_group` proposal is made from.
- `why_unmatched` is required. It is the difference between a usable proposal and a stray string,
  and it is what a reviewer reads first.

**The model is never permitted to place an observation in `observations[]` by approximation.** If
nothing fits, it goes in `unmatched[]`. This is stated twice in the prompt, in both the instruction
and the constraint block, because it is the single behaviour most likely to regress.

### 3.4 `relationships[]`

```json
{
  "type": "PART_OF",
  "source": "sugar flower cascade",
  "target": "top tier",
  "confidence": 0.72,
  "evidence": "flowers are affixed to and descend from the uppermost tier"
}
```

`type` must be one of `ai.taxonomy.RelationshipType`'s 10 values, or `ON` / `NEAR` / `MATCHES` from
[Relationship_Model.md](../10_Taxonomy/Relationship_Model.md). A relationship the model wants that
is in neither list goes to `unmatched[]` with `suggested_kind: "relationship_type"` — and per the
Discovery spec §5.3, widening a frozen literal requires its own ADR and gate.

### 3.5 `unparsed[]`

Model output that became neither an observation nor an unmatched item. Retained rather than
dropped: it is the only signal that would make prompt regression visible, and it costs a string
array to keep.

---

## 4. Prompt construction

`ai/vision/prompts/extractor_v1.md` is a **template**, not a static string. At job start it is
rendered against the current taxonomy so the model is told exactly what vocabulary exists, and the
result is hashed into `prompt_version`.

Structure:

1. **Role** — a cake product analyst producing structured observations, not prose.
2. **Rendered taxonomy digest** — the 30 groups, their attributes, and each vocabulary's terms,
   generated from `bakery_v1.json`. Never hand-copied; a hand-copy would silently drift the moment
   a Term is added.
3. **Output schema** — `tbk_image_schema_v1.json`, inlined.
4. **The constraint block**, stated verbatim:

   > The vocabulary above is what the system currently knows. It is **not** a limit on what you may
   > report. If you observe something the vocabulary has no term for, put it in `unmatched` with
   > your own description and an explanation of why nothing fits. **Never** place an observation
   > under an attribute that does not actually describe it. Reporting something as unmatched is
   > always correct; forcing it into an approximate field is always wrong.
   >
   > Distinguish *absent* from *unseen*. If the cake has no topper, that is `value_state: "null"`.
   > If you cannot tell whether it has one, that is `value_state: "unknown"`. Do not guess.
   >
   > Report only what is visible in the photograph. Do not infer ingredients, price, weight, or
   > provenance you cannot see. If you are uncertain, lower the confidence — do not omit the
   > observation.

5. **Few-shot examples** — at minimum one matched observation, one `null`, one `unknown`, one
   `unmatched`. The `unmatched` example is load-bearing: without it, models reliably default to
   forcing values into the nearest listed field.

Point 4's third paragraph is [VIG-007](../00_Governance/VIG-007-Quality-Standard.md) Principle 3
("no fabricated attributes, ever") and `CLAUDE.md`'s "never invent" rule, restated where the model
will actually read them.

---

## 5. Provider requirements

- **Structured output is mandatory.** The Ollama call already passes `format: "json"`; that stays,
  now with the real schema rather than six ad-hoc keys.
- **A parse failure is data.** It produces a record with `value_state: "unknown"` and the raw
  response preserved, exactly as `Build Vision Failure` already does. It never produces an absence.
- **Provider-interchangeable** per [VIG-004](../00_Governance/VIG-004-AI-Principles.md). This
  contract names no provider. `qwen2.5vl:3b` (Python config) and `qwen2.5vl` (n8n workflow) are
  currently different model tags for the same family — **that discrepancy must be resolved before
  first joint run**, since `model` is a provenance field and two runs claiming different models for
  identical processing corrupts lineage.
- **No business logic in the prompt** (VIG-004). Promotion thresholds, confidence bars, and
  Shopify mappings live in configuration and code, never in prompt text.

---

## 6. Versioning

| Artifact | Version field | Changes when |
|---|---|---|
| This contract | `extraction_version` | The envelope shape changes |
| Prompt | `prompt_version` | Template or constraint text changes — hash of the rendered prompt |
| Output schema | `schema_version` | `tbk_image_schema_v1.json` changes |
| Taxonomy digest | `taxonomy_version` | Any taxonomy change, including an additive new Term |

All four are carried on every produced record via `Provenance`. A record whose four versions are
known can always be re-derived; one missing any of them cannot, and per
[ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md) must not be written.

Adding a Term increments `taxonomy_version` and therefore changes the rendered prompt and
`prompt_version` too. That is correct and intended: the same photograph extracted before and after
a vocabulary grows is genuinely two different extractions, and the versions say so.

---

## 6a. Position in the architecture

```
      ai/vision/  ──this contract──▶  observations[]  ──▶  ai.eal records
        (Build-008)                          │                  │
                                             │                  ├─▶ ai.ear registry lookup
                                             │                  │   (Attribute Registry, Build-002)
                                             │                  └─▶ ai.attribute_intelligence
                                             │                      (multi-source resolution)
                                             │
                                    unmatched[] ──▶ Dynamic Structure Discovery
                                                        │
                                                        ▼
                                            Cake Genome / Master Taxonomy grows
                                                        │
                        ai.knowledge (Knowledge Graph) ◀─┴─▶ ai.product_intelligence
                                                                 (Product Genome)
```

| Consumes / feeds | Document |
|---|---|
| The taxonomy it is rendered against | [Enterprise Master Taxonomy (Build-005)](../70_Enterprise_Master_Taxonomy/README.md) — the Cake Genome's authored Bakery content |
| Registry the matched attributes resolve into | [Enterprise Attribute Registry (Build-002)](../40_Enterprise_Attribute_Registry/README.md) |
| Where unmatched observations go | [Dynamic Visual Structure Discovery](../80_Dynamic_Structure_Discovery/README.md) |
| What enforces the confidence/consistency gates on the output | Build-006 Validation Engine — **not built**; rules in [Validation.md](../10_Taxonomy/Validation.md) |
| Downstream read model | [Product Genome](../PRODUCT_INTELLIGENCE_ARCHITECTURE.md) (`ai.product_intelligence`) |
| Downstream semantic layer | [Knowledge Graph](../KNOWLEDGE_GRAPH.md) (`ai.knowledge`) |
| Terminology | [GLOSSARY.md](../00_Foundation/GLOSSARY.md) |

## 7. What this contract does not do

- Does not author the taxonomy digest content — generated from `bakery_v1.json`, never hand-written.
- Does not fill the seven empty attribute groups. They are surfaced through discovery, from real
  images, with evidence.
- Does not perform matching. The model reports what it saw and its best guess at placement;
  authoritative matching against active taxonomy is `structure_discovery.matcher`'s job, on the
  Python side, per ADR 0011's ownership split.
- Does not specify batch orchestration, retries, or concurrency — n8n's, per ADR 0011.
- Does not define embeddings. `data_type: "vector"` attributes are Build-009.

---

## Related

[Dynamic Structure Discovery](../80_Dynamic_Structure_Discovery/SPECIFICATION.md),
[ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md),
[Architecture.md](Architecture.md), [VisionPipeline.md](VisionPipeline.md),
[Configuration.md](Configuration.md), [Roadmap.md](Roadmap.md),
[EAL_SPECIFICATION.md](../20_Attribute_Language/EAL_SPECIFICATION.md),
[Null_and_Unknown_Standard.md](../20_Attribute_Language/Null_and_Unknown_Standard.md),
[Confidence_Standard.md](../20_Attribute_Language/Confidence_Standard.md),
[Provenance_Standard.md](../20_Attribute_Language/Provenance_Standard.md),
[Relationship_Model.md](../10_Taxonomy/Relationship_Model.md),
[VIG-004](../00_Governance/VIG-004-AI-Principles.md),
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md).
