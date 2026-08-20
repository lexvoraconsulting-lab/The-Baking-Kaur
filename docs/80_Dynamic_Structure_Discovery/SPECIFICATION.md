# TBK Dynamic Visual Structure Discovery — Specification v1

Date: 2026-08-20
Status: **Proposed** — specification only. No code was written, no frozen package modified, no
taxonomy content changed. Awaiting review.

Governs how the platform handles a visual observation that **does not fit the existing taxonomy**,
without either discarding it or forcing it into the wrong field.

Operates on the frozen content of the
[Enterprise Master Taxonomy (Build-005)](../70_Enterprise_Master_Taxonomy/README.md) — the Cake
Genome's authored Bakery vocabulary — and feeds, once a proposal is approved and registered, both
the [Product Genome](../PRODUCT_INTELLIGENCE_ARCHITECTURE.md) read model and the
[Knowledge Graph](../KNOWLEDGE_GRAPH.md) semantic layer.

---

## 1. The requirement

> TBK Cake Intelligence must not be limited to a fixed predefined attribute list.

When an image contains a characteristic the taxonomy has no home for, the system must be able to
propose a new attribute, a new attribute value, a new attribute group, a new relationship, or a new
structural entity — through a controlled process, never by mutating the production taxonomy
directly.

This document specifies that process. It is a **reconciliation**, not a new architecture: most of
the required machinery already exists and is reused verbatim.

---

## 2. What already exists (reused, not rebuilt)

| Requirement | Existing mechanism | Where | State |
|---|---|---|---|
| Unknown observation must not be lost | `value_state: "unknown"` — distinct from `"null"` (does not apply) | `ai/eal/models.py`, [Null_and_Unknown_Standard.md](../20_Attribute_Language/Null_and_Unknown_Standard.md) | **Built** |
| Candidate attribute must be distinguishable from canonical | `EARAttributeEntry.status = "draft"` (default), promotable to `"active"` | `ai/ear/models.py` | **Built** |
| Evidence vs. fact separation | `Attribute` → `Genome Attribute` promotion | [Entity_Model.md](../10_Taxonomy/Entity_Model.md) | Documented |
| Human approval gate | `HumanVerification.status` — 5 states, `original_value` preserved on correction | `ai/eal/models.py`, [Human_Verification_Standard.md](../20_Attribute_Language/Human_Verification_Standard.md) | **Built** |
| Traceability of every derived fact | `Provenance` — provider/model/model_version/prompt_version/schema_version/taxonomy_version/extracted_at | `ai/eal/models.py` | **Built** |
| Multi-source candidate values, losers retained | `AttributeObservation` + `ConflictRecord` + `ResolvedAttribute` | `ai/attribute_intelligence/models.py` | **Built** |
| Free-text → Term normalization | `Term.label` + `Term.synonyms` | `ai/taxonomy/models.py`, `normalizer.py` | **Built** |
| Unmapped-value feedback loop | `tbk_unmapped_attributes` — `raw_value`, `occurrence_count`, `suggested_canonical_id`, `status` | `n8n/TBK-A-OS/Data Tables/` | **Built (n8n)** |
| Additive-only growth without redesign | Additive inheritance; new Terms are additive; Terms are deprecated, never deleted | [Inheritance.md](../10_Taxonomy/Inheritance.md), [Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md) | Documented |
| The doctrine itself | *"an unmapped observation isn't lost, it's a signal that the vocabulary may need a new Term"* | [Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md) | Documented |

**The last row matters most.** Sprint 2.1 already decided that an unmapped observation is a signal,
not an error. This specification is the implementation of a decision already taken, not a new
direction.

---

## 3. What is genuinely missing

Four gaps, verified in code. All four are narrow.

**G1 — Taxonomy entries have no proposed state.**
`ai/taxonomy/models.py`: `EntryStatus = Literal["active", "deprecated"]`. There is no way to record
a Term, AttributeGroup, Vocabulary, Category or Relationship that has been *proposed but not
approved*. `ai.ear` solved this for attributes with `"draft"`; `ai.taxonomy` never did.
**This single omission blocks candidate values, candidate groups and candidate relationships.**

**G2 — No evidence record for a proposal.**
Taxonomy models deliberately carry no `confidence` and no `provenance` — correctly, since they are
the canonical meaning layer, not records *about* an entity. So even with G1 fixed, there is nowhere
to record *why* a structure was proposed, from which image, by which model, with what confidence.

**G3 — Observations cannot exist without a registered attribute.**
`AttributeObservation.registry_reference` is documented as *"always a real `ai.ear` attribute_id
(EAR-NNNNNN)"*. An observation of something with no EAR entry yet cannot be represented at all.

**G4 — `EntityType` and `RelationshipType` are closed literals in frozen packages.**
`ai.eal.EntityType = Literal["image","region","object"]`;
`ai.taxonomy.RelationshipType` = 10 fixed values; `TaxonomyEntityType` = 5 fixed values. Build-001
and Build-005 are frozen. A genuinely new structural entity cannot be expressed.

---

## 4. The eight states

The requirement named eight states. Six already have a canonical representation; two are the gap.

| # | State | Canonical representation | Status |
|---|---|---|---|
| 1 | Existing canonical taxonomy | `ai.taxonomy` entry, `status = "active"` | Exists |
| 2 | Observed image fact | `AIObservation` — raw provider response, immutable | Documented ([Entity_Model.md](../10_Taxonomy/Entity_Model.md)), **not coded** |
| 3 | AI-inferred attribute | `EALAttributeRecord`, `human_verification.status = "unverified"` | Exists |
| 4 | Candidate new attribute | `EARAttributeEntry`, `status = "draft"` | **Exists — reuse, do not invent** |
| 5 | Candidate new attribute value | `Term`, `status = "proposed"` | **Gap G1** |
| 6 | Candidate new structure | `AttributeGroup` / `Relationship` / `Category` / entity type, `status = "proposed"` | **Gap G1 + G4** |
| 7 | Validated taxonomy element | Passed all four dimensions of [Validation.md](../10_Taxonomy/Validation.md); still `"proposed"` | Rules exist, engine does not (Build-006) |
| 8 | Human-approved canonical | `status = "active"` + a `StructureProposal` in terminal state `approved` | Gate exists, promotion path does not |

**States 7 and 8 are deliberately separate.** Passing validation means a proposal is *well-formed
and non-contradictory*. It does not make it canonical. Only a human does that
([EPR §04](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md): *AI agents may
draft, extract and verify; only a human may publish*).

### 4.1 Nine-state conformance

The states as enumerated in the standing requirement, each mapped to its representation. Added
2026-08-20 by the documentation integration pass.

| Required state | Representation | Where it lives | Exists today |
|---|---|---|---|
| **Known observation** | `MatchState = "matched"` / `"matched_synonym"` → `EALAttributeRecord`, `value_state: "present"` | `ai.eal` | Model yes, producer no |
| **Unknown observation** | `MatchState = "undetermined"` / `"unmatched"` → `value_state: "unknown"` | `ai.eal` | **Yes** |
| **Candidate attribute** | `ProposalKind = "attribute"` → `EARAttributeEntry(status="draft")` | `ai.ear` | **Yes — reuse** |
| **Candidate attribute value** | `ProposalKind = "term"` → `Term(status="proposed")` | `ai.taxonomy` | No — gap **G1** |
| **Candidate attribute group** | `ProposalKind = "attribute_group"` → `AttributeGroup(status="proposed")` | `ai.taxonomy` | No — gap **G1** |
| **Candidate relationship** | `ProposalKind = "relationship"` → `Relationship(status="proposed")`; a new *type* is `"relationship_type"` | `ai.taxonomy` | No — gaps **G1**, **G4** |
| **Candidate structure** | `ProposalKind = "category"` / `"vocabulary"` / `"entity_type"` | `ai.taxonomy`, `ai.eal` | No — gaps **G1**, **G4** |
| **Validated taxonomy element** | `ProposalStatus = "validated"` — passed all four dimensions of [Validation.md](../10_Taxonomy/Validation.md). **Still not canonical** | `structure_discovery` + Build-006 | No — Build-006 absent |
| **Canonical taxonomy element** | `status = "active"` + `ProposalStatus = "approved"` + `human_verification.status = "verified"` | `ai.taxonomy`, `ai.ear` | Gate yes, promotion path no |

Three of the nine already have a working representation. The remaining six are blocked by two
narrow gaps (G1: one additive word; G4: two frozen literals), not by six separate problems.

### 4.2 The controlled lifecycle

Every new structure follows this path. No step may be skipped, and no automated actor may perform
the **APPROVE** step.

```
OBSERVE   Vision reports a fact. Nothing is written to the taxonomy.
   |      Output: an unmatched item on the extraction's second channel.
   v
PROPOSE   A StructureProposal is created with its Evidence (image_id,
   |      observation_id, verbatim raw_fragment, provenance).
   |      Deduped by (kind, canonical_name); occurrence_count increments.
   |      status: observed -> candidate
   v
VALIDATE  Validation.md's four dimensions run against the proposal.
   |      Failure routes to review; it never drops the proposal and never
   |      patches it to pass.               status: candidate -> validated
   v
APPROVE   *** HUMAN ONLY. No automatic path exists at any confidence. ***
   |      A reviewer approves, rejects, merges, or defers.
   |                                        status: validated -> approved
   v
REGISTER  promote() writes the real entry: an EAR entry at status "draft",
   |      and/or a taxonomy entry at status "proposed" -> "active".
   |      promoted_to records the created ID.
   v
VERSION   taxonomy_version increments. Additive, therefore a MINOR change
   |      under Versioning.md - existing records stay valid and are never
   |      silently reinterpreted.
   v
USE       Now visible to catalog resolution, EAL vocabulary validation,
          Shopify distribution, and search indexing. Not before.
```

The two halves of the governing principle map onto this directly: **OBSERVE** and **PROPOSE** are
where the taxonomy stops being a ceiling; **APPROVE** is where the AI stops being able to mutate it.

---

## 5. Proposed minimal additions

Three changes. Nothing else. Each is stated as a proposal requiring approval — none is implemented.

### 5.1 One-word additive change to `EntryStatus`

```python
EntryStatus = Literal["active", "deprecated", "proposed"]
```

Additive, so per [Versioning.md](../10_Taxonomy/Versioning.md) it is a **minor** change: no existing
record's interpretation changes, no existing Term is invalidated. It is nonetheless a change to
**frozen Build-005 code** and therefore requires the AR-007 gate to be aware of it. It cannot be
made unilaterally.

Every consumer must treat `"proposed"` as **non-canonical**: excluded from `TaxonomyCatalog`
resolution, from EAL `vocabulary` validation, from Shopify distribution, and from search indexing.
A proposed Term is visible to reviewers and to the discovery engine, and to nothing else.

### 5.2 A new sidecar package `ai/structure_discovery/`

Justified because no existing package owns "a proposal and its evidence" — ECP-100 §14 found no
duplicate responsibilities anywhere, and §13 lists exactly this class of gap. It exists to hold the
evidence (G2) and to avoid unfreezing three packages to add fields none of them should own.

It **references** frozen packages and never mutates them.

```
ai/structure_discovery/
  models.py       ProposalKind, MatchState, ProposalStatus, Evidence,
                   StructureProposal, DiscoveryResult
  ids.py           compute_proposal_id() — uuid5, own namespace UUID
  matcher.py        match_observation() — wraps ai.attribute_intelligence.normalizer
                   (Term.label/.synonyms), returns a MatchState — no new matching rule
  proposer.py        propose() — unmatched observation -> StructureProposal
  dedupe.py           merge proposals by (kind, canonical_name); increments occurrence_count,
                   mirroring n8n's tbk_unmapped_attributes semantics
  validator.py         validate_proposal() — the four dimensions of 10_Taxonomy/Validation.md
                   applied to a proposal rather than to a value
  promotion.py          promote() — human-gated; emits an EAR draft entry and/or a proposed
                   taxonomy entry. Never writes to a live system itself.
  test_structure_discovery.py    self-check, no network
```

### 5.3 New structural entities are recorded but not auto-promotable

For G4, a proposal of kind `entity_type` or `relationship_type` may be **recorded and reviewed**,
but promotion requires its own ADR and architecture gate, because `EntityType` is load-bearing in
`ai.eal`'s generated JSON Schema and in every stored record. Recording the demand for a new entity
type is valuable; silently widening a frozen wire format is not.

---

## 6. The pipeline

```
IMAGE
  |
  v
PREPROCESS ............ n8n. Fetch bytes, compute TBK_IMAGE_ID (sha256 content hash,
  |                     ai/vision/python/pipeline.py). Idempotent by construction.
  v
VISION EXTRACTION ..... n8n calls the provider using the prompt + output schema supplied by
  |                     Python (ADR 0011 interface #1). Raw response persisted immutably.
  v
OBSERVED FACTS ........ AIObservation. One per provider call. Never edited, never deleted.
  |                     Zero or more candidate facts parse out of it.
  v
ATTRIBUTE MATCHING .... matcher.match_observation() against ACTIVE taxonomy only.
  |                     Emits MatchState per fact. Proposed entries are invisible here.
  |
  +--- matched / matched_synonym --> EALAttributeRecord, value_state "present"
  |                                  -> ai.attribute_intelligence for multi-source resolution
  |
  +--- ambiguous ------------------> EALAttributeRecord, value_state "unknown"
  |                                  -> human_verification "pending_review"  (never guess)
  |
  +--- unmatched ------------------> UNKNOWN DETECTION
                                        |
                                        v
                          NEW ATTRIBUTE PROPOSAL   (kind: attribute)
                          NEW VALUE PROPOSAL       (kind: term)
                          NEW GROUP PROPOSAL       (kind: attribute_group)
                          RELATIONSHIP PROPOSAL    (kind: relationship | relationship_type)
                          STRUCTURE PROPOSAL       (kind: category | entity_type)
                                        |
                                        v
                          DEDUPE  — merge by (kind, canonical_name), increment
                                    occurrence_count. A one-off is noise; a recurring
                                    unmatched observation is a taxonomy gap.
                                        |
                                        v
                          VALIDATION  — Validation.md's four dimensions:
                                    structural / confidence threshold /
                                    consistency / completeness.
                                    Failure routes to review; it never drops the
                                    proposal and never patches it to pass.
                                        |
                                        v
                          HUMAN REVIEW  — the only transition to canonical.
                                    approved | rejected | merged | deferred
                                        |
                            approved    v
                          TAXONOMY / ATTRIBUTE REGISTRY
                                    EAR entry status "draft" -> "active"
                                    Taxonomy entry status "proposed" -> "active"
                                    taxonomy_version increments (additive = minor)
                                        |
                                        v
                                  CAKE GENOME       (Bakery domain content, now wider)
                                        |
                                        v
                          SEARCH INDEX / SHOPIFY / AI SYSTEMS
```

**The unmatched branch never blocks the matched branch.** A cake with twelve recognised attributes
and one unrecognised feature yields twelve records and one proposal, not a failed extraction.

---

## 7. Machine-readable output contract

### 7.1 Reconciliation with the requested field list

The requirement listed `known`, `unknown`, `candidate_new_attribute`, `candidate_new_value`,
`candidate_new_structure` as five independent booleans, and invited reconciliation against a
stronger canonical equivalent. There is one, and this specification uses it:

- Five independent booleans admit contradictory states (`known: true` *and* `unknown: true`). They
  are replaced by **one `match_state` enum**, extending the existing three-state `value_state`
  pattern that `ai.eal` already proved.
- The three `candidate_new_*` booleans collapse into **one `proposal_kind` enum**, because a single
  observation proposes exactly one kind of structure. Where an observation implies several (a new
  value inside a new group), those are separate linked proposals, not flags on one record.
- `confidence`, `source`, `model`, `model_version`, `taxonomy_version`, `schema_version` and
  `provenance` are **not new fields** — six of the seven already live inside `ai.eal.Provenance`,
  and `source` already exists as `ai.attribute_intelligence.Source`. They are referenced, not
  redefined.
- `human_verification_status` is `ai.eal.HumanVerification.status`, unchanged.
- `evidence` is genuinely new (gap G2) and is the only added concept in the record itself.

### 7.2 Enumerations

```python
MatchState = Literal[
    "matched",           # resolved to an active taxonomy element
    "matched_synonym",   # resolved via Term.synonyms
    "ambiguous",         # more than one active element fits -> review, never guess
    "unmatched",         # observed, nothing fits -> drives a proposal
    "not_applicable",    # the attribute does not apply    (pairs with value_state "null")
    "undetermined",      # applies, not yet determined     (pairs with value_state "unknown")
]

ProposalKind = Literal[
    "attribute",          # -> EAR entry, status "draft"          (mechanism exists today)
    "term",               # -> Term, status "proposed"
    "vocabulary",         # -> Vocabulary, status "proposed"
    "attribute_group",    # -> AttributeGroup, status "proposed"
    "category",           # -> Category, status "proposed"
    "relationship",       # -> Relationship instance, status "proposed"
    "relationship_type",  # -> widens a frozen Literal: ADR + gate required
    "entity_type",        # -> widens a frozen Literal: ADR + gate required
]

ProposalStatus = Literal[
    "observed",     # seen once, below the promotion threshold
    "candidate",    # deduped, occurrence_count above threshold
    "validated",    # passed all four validation dimensions — still NOT canonical
    "approved",     # human-approved; promotion executed
    "rejected",     # human-rejected; retained, never deleted
    "merged",       # judged a duplicate of an existing element; superseded_by is set
    "deferred",     # real but not now
]
```

### 7.3 Records

```python
@dataclass(frozen=True)
class Evidence:
    """Why this proposal exists. The gap ai.taxonomy correctly refuses to carry itself."""
    image_id: str                  # TBK_IMAGE_ID — content hash, always resolvable
    observation_id: str            # the immutable AIObservation this came from
    raw_fragment: str              # the model's own words, verbatim, never paraphrased
    region: dict | None = None     # bounding box, when the provider supplies one
    provenance: Provenance = ...   # ai.eal.models.Provenance — reused unchanged

@dataclass(frozen=True)
class StructureProposal:
    proposal_kind: ProposalKind
    canonical_name: str            # normalized slug, the dedupe key
    label: str                     # human-readable
    status: ProposalStatus = "observed"
    proposal_id: str = ""          # uuid5, own namespace
    parent_reference: str | None = None   # target vocabulary_id / group_id / EAR-NNNNNN
    suggested_data_type: DataType | None = None    # ai.eal DataType, reused
    suggested_vocabulary: str | None = None
    confidence: float | None = None
    occurrence_count: int = 1      # same semantics as tbk_unmapped_attributes
    first_seen: str = ""
    last_seen: str = ""
    evidence: tuple[Evidence, ...] = ()
    validation_issues: tuple[ValidationIssue, ...] = ()   # ai.attribute_intelligence, reused
    human_verification: HumanVerification = ...           # ai.eal, reused
    superseded_by: str | None = None      # set when status == "merged"
    taxonomy_version: str = ""            # the version this was proposed AGAINST
    promoted_to: str | None = None        # the real ID created on approval

@dataclass(frozen=True)
class DiscoveryResult:
    """One image's complete outcome. Records and proposals travel together."""
    image_id: str
    observation_id: str
    records: tuple[EALAttributeRecord, ...] = ()      # matched facts
    proposals: tuple[StructureProposal, ...] = ()     # unmatched facts
    match_states: dict[str, MatchState] = ...          # canonical_path -> state
    unparsed: tuple[str, ...] = ()                     # model output nothing could be made of
```

`unparsed` is deliberate. Text the pipeline could neither match nor turn into a proposal is
retained rather than dropped — it is the raw material for improving the prompt, and discarding it
would make prompt regression invisible.

### 7.4 Worked example

An image shows a cake with a hand-piped royal-icing lace collar. No term in the Decoration Style
vocabulary covers it.

> **Corrected 2026-08-20 (implementation).** This example originally used "mirror glaze", asserting
> it was absent from the taxonomy. It is **not** absent — `Mirror Glaze` is an active Term in the
> Finish vocabulary (`Matte`, `Glossy`, `Satin`, `Mirror Glaze`, `Semi-Naked`), and the implemented
> matcher resolves it correctly. Corrected against the real catalog rather than left as a
> plausible-sounding but false illustration.

```json
{
  "image_id": "TBK-9f2a1c4d8b3e7a05",
  "observation_id": "OBS-2026-08-20-0001",
  "records": [
    {
      "canonical_path": "eal.domain.bakery.colour.primary",
      "value": "white", "value_state": "present",
      "data_type": "enum", "vocabulary": "colour_name", "confidence": 0.91,
      "human_verification": { "status": "unverified" }
    }
  ],
  "match_states": {
    "eal.domain.bakery.colour.primary": "matched",
    "eal.domain.bakery.finish.type": "unmatched"
  },
  "proposals": [
    {
      "proposal_kind": "term",
      "canonical_name": "mirror_glaze",
      "label": "Mirror Glaze",
      "status": "observed",
      "parent_reference": "TAX-VOC-000009",
      "suggested_data_type": "enum",
      "confidence": 0.78,
      "occurrence_count": 1,
      "evidence": [{
        "image_id": "TBK-9f2a1c4d8b3e7a05",
        "observation_id": "OBS-2026-08-20-0001",
        "raw_fragment": "a highly reflective poured mirror-glaze finish with a drip edge",
        "provenance": {
          "provider": "ollama", "model": "qwen2.5vl:3b",
          "schema_version": "v1", "taxonomy_version": "v1",
          "prompt_version": "extractor_v1",
          "extracted_at": "2026-08-20T09:14:22Z"
        }
      }],
      "human_verification": { "status": "unverified" },
      "taxonomy_version": "v1"
    }
  ],
  "unparsed": []
}
```

Nothing was forced into `frosting_type`. Nothing was invented. The observation survived.

---

## 8. Promotion thresholds

Thresholds are **configuration, not code**, consistent with
[Validation.md](../10_Taxonomy/Validation.md)'s "per-Attribute-Group configuration value, not a
single global number", and with the n8n side's existing discipline of externalising business values
into `tbk_pi_config`.

Recommended starting values, to be tuned against real data rather than treated as settled:

| Transition | Condition |
|---|---|
| `observed` → `candidate` | `occurrence_count >= 3` across distinct `image_id`s |
| `candidate` → `validated` | all four validation dimensions pass |
| `validated` → `approved` | **human only** — no automatic path exists at any confidence |
| any → `merged` | a reviewer identifies an existing element; `superseded_by` set |
| any → `rejected` | reviewer judgement; record retained permanently |

Distinct `image_id`s, not distinct observations — because `TBK_IMAGE_ID` is a content hash, the
same image reprocessed ten times counts once. Idempotence is free.

---

## 9. Invariants

1. **No proposal is ever auto-promoted.** Any confidence, any occurrence count.
2. **No proposal is ever deleted.** Rejected and merged proposals are retained, mirroring
   [Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md)'s "a Term is never deleted."
3. **`"proposed"` entries are invisible to every consumer** — catalog resolution, EAL vocabulary
   validation, Shopify distribution, search indexing.
4. **An observation is never forced into a wrong field.** `unmatched` is a valid, expected outcome.
5. **`ambiguous` never resolves by guessing.** It routes to review, per Validation.md.
6. **Every proposal carries its `taxonomy_version`** — the version it was proposed *against*, so a
   proposal outliving a taxonomy change is detectable rather than silently stale.
7. **Frozen packages are not modified** except §5.1's single additive `EntryStatus` change, which
   requires the AR-007 gate.
8. **No fabrication.** [VIG-007](../00_Governance/VIG-007-Quality-Standard.md) Principle 3 applies
   unchanged to proposals: a proposal records what was observed, never what would be convenient.

---

## 10. Explicitly out of scope

- ML-based clustering of unmatched observations. `ai.knowledge`'s `InferenceChainRunner` is
  rule-based by deliberate decision ([ADR 0009](../adr/2026-08-02-product-knowledge-graph.md)); this
  specification does not reverse that.
- Automatic prompt rewriting from `unparsed` content.
- A reviewer UI. The review *state machine* is specified here; the interface is
  [EPR](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md) WS-14 and unscheduled.
- Cross-domain proposal sharing. A Flowers domain proposing a Bakery Term is a real future question
  and not one this platform has yet.

---

## Related

[Vision Extraction Contract](../AI/VisionExtractionContract.md),
[ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md),
[ECP-200 Gap Analysis](../30_Enterprise_Program_Roadmap/ECP-200_Architecture_Gap_Analysis.md),
[Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md),
[Validation.md](../10_Taxonomy/Validation.md), [Versioning.md](../10_Taxonomy/Versioning.md),
[Inheritance.md](../10_Taxonomy/Inheritance.md), [Entity_Model.md](../10_Taxonomy/Entity_Model.md),
[Null_and_Unknown_Standard.md](../20_Attribute_Language/Null_and_Unknown_Standard.md),
[Human_Verification_Standard.md](../20_Attribute_Language/Human_Verification_Standard.md),
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md),
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md),
[GLOSSARY.md](../00_Foundation/GLOSSARY.md).
