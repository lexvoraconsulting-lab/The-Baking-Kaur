# ADR 0011: n8n / Python system of record — Python owns the contract, n8n owns execution

Date: 2026-08-20

## Status

Proposed — awaiting review. No code, schema, workflow, branch, or Shopify data was changed to
produce this document.

## Context

Two substantially complete implementations of the same pipeline exist in this repository and
neither document tree acknowledges the other.

**The Python program** (`ai/`, `docs/00_Governance/` through `docs/70_*`, `docs/adr/0001–0010`):
nine packages, ~90 modules, per-module self-check suites, ten accepted ADRs, six governance-
approved documentation trees, five completed Builds. Evidence of maturity: `ai.eal` carries a
three-state `value_state` (`present`/`null`/`unknown`), a required `Provenance` object, and a
five-state `HumanVerification` lifecycle; `ai.ear` carries a four-state entry `Status`
(`draft`/`active`/`deprecated`/`retired`); `ai.taxonomy` holds 6 categories, 30 attribute groups,
17 vocabularies, 26 attributes, 96 terms and 24 typed relationships as real authored content.

**What the Python program cannot do today**, verified on disk:

- `ai/vision/prompts/extractor_v1.md` — **0 bytes**. `ai/vision/schemas/taxonomy_v1.json` — **0
  bytes**. `ai/vision/schemas/tbk_image_schema_v1.json` — **0 bytes**. The pipeline falls back to a
  hardcoded inline prompt and returns raw text no code path converts into a record.
- `ai/attribute_distribution/shopify_adapter.py` is dry-run only; `erp_adapter.py` is fully stubbed.
- `ai/knowledge/` is explicitly in-memory-only per [ADR 0009](2026-08-02-product-knowledge-graph.md).
  There is no persistence anywhere in `ai/`.
- All 147 `ai/` files exist only on branch `feature/vision-engine-v1`. `master`, `develop`,
  `phase-a/production-safety` and `sync/live-theme-baseline` contain **zero** of them.

**The n8n program** (`n8n/TBK-A-OS/`, `n8n/tbk-vision-workflow-complete/`): 8 exported workflows,
15 Data Tables, a deployable 18-node TypeScript orchestrator, a PostgreSQL schema, a 20-case test
suite, and execution screenshots. Evidence of maturity: it actually runs. `TBK Qwen Vision
Analysis` makes a real Ollama call; `TBK Audit Logger` hashes real audit rows; `tbk_pi_config`
externalises business values rather than hardcoding them; `tbk_unmapped_attributes` already carries
`raw_value` / `occurrence_count` / `suggested_canonical_id` / `status` — a working
unmapped-observation feedback loop.

**What the n8n program cannot do today**, verified in the workflow JSON:

- The Qwen prompt is hardcoded inside `TBK Qwen Vision Analysis.json` and asks for exactly six
  keys: `layers`, `frosting_type`, `decorations`, `colors`, `quality_score`, `confidence`. This is
  a hard six-field ceiling.
- `tbk_taxonomy_attributes` holds 17 rows across three `attribute_type` values (`color`,
  `decoration`, `frosting_type`) — against `ai/taxonomy/content/bakery_v1.json`'s 26 attributes and
  96 terms. The two taxonomies are unrelated content with unrelated identifier schemes.
- No `value_state`, no `Provenance` object, no `human_verification` lifecycle, no EAL envelope.
  `tbk_vision_results` flattens everything into columns; `raw_response` is preserved (good) but
  nothing structured sits between it and the product record.
- Prompts are workflow configuration, so they are not versioned as content and no `prompt_version`
  can be recorded against a produced record.
- It uses its own `BUILD-304`…`BUILD-312` numbering with no corresponding document anywhere in
  `docs/`. `tbk_pi_config` contains the note "BUILD-307 owns publish"; no such build is documented.

**The prior documented position.** [EPR §03](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
already ruled on this, a week before the n8n build existed: *"n8n | Cross-system workflow
orchestration | Consumes Build-004's output events; **never** a second write path into the
Knowledge Graph"* and *"n8n orchestrates **when** things happen, never **what** the canonical data
is."* The n8n build as delivered contradicts that — it owns extraction, taxonomy content, conflict
resolution and product assembly, with PostgreSQL as its store of record.

## Decision

**Option C — hybrid, with explicit boundaries. Python owns the contract; n8n owns execution.**

This is chosen on evidence, not preference:

- **Option A (Python canonical processing, n8n orchestration only) is rejected** because Python has
  no runtime, no persistence, no live write path, and three empty extraction files. Making the
  non-executing side canonical for execution would stop a working pipeline to wait for one that has
  never run.
- **Option B (n8n canonical, Python as services) is rejected** because it discards ten ADRs, six
  governance trees, and the `value_state`/`Provenance`/`human_verification` model — and because its
  six-field extraction ceiling directly contradicts the primary functional requirement now placed
  on this platform (the system must not be limited to a fixed predefined attribute list).
- **Option C is what the existing documentation already says.** EPR §03's split — n8n owns *when*,
  the platform owns *what* — is exactly this decision. Choosing C reconciles the two programs with
  a ruling that already exists rather than issuing a new one.

The one adjustment to EPR §03: it assumed persistence would live on the platform side. It does not
and will not for some time. This ADR therefore separates **schema authority** from **physical
storage**: PostgreSQL holds the bytes; Python defines what shape those bytes must be. One system of
record is preserved in the [VIG-003](../00_Governance/VIG-003-Data-Principles.md) sense because
there remains exactly one authority for the *definition* of any given fact.

## Ownership boundaries

### What Python owns

- **The contract.** `ai.eal` record shapes, `ai.ear` registry entries, `ai.ead` definitions,
  `ai.taxonomy` content, and all generated JSON Schema under `ai/*/schemas/`. These are the
  normative definition of every fact the platform produces.
- **Taxonomy content.** `ai/taxonomy/content/bakery_v1.json` — the
  [Enterprise Master Taxonomy (Build-005)](../70_Enterprise_Master_Taxonomy/README.md) — is the
  single canonical Bakery vocabulary. `tbk_taxonomy_attributes` / `tbk_taxonomy_synonyms` become **generated artifacts**
  exported from it, never hand-authored.
- **Vocabulary, identifier, and version semantics.** `TBK_IMAGE_ID`, `EAL-*`, `EAR-NNNNNN`,
  `TAX-*`, `taxonomy_version`, `schema_version`, `eal_version`.
- **Validation rules** (Build-006), reconciliation logic (`ai.attribute_intelligence`), and the
  graph semantics (`ai.knowledge`).
- **Prompt and output-schema content** — `ai/vision/prompts/`, `ai/vision/schemas/`. These become
  the source of truth that n8n reads, not workflow-embedded strings.

### What n8n owns

- **Execution and orchestration** — when a batch runs, in what order, with what concurrency.
- **Retry, backoff, dead-lettering, and alerting.**
- **Provider invocation** — the actual HTTP call to Ollama/vLLM and any future provider.
- **Batch and job state** — `tbk_batches`, `tbk_image_hashes`, `tbk_pipeline_audits`.
- **Human-review queue surfacing** and operator notification (Slack).

n8n owns no vocabulary, no attribute definition, and no taxonomy content.

### What PostgreSQL owns

- **Physical persistence of every record and every raw observation.** It is the durable store the
  Python side has never had.
- Its schema is **generated from the Python contract**, not authored independently. A column exists
  because a contract field exists.
- It stores raw provider responses immutably ([VIG-003](../00_Governance/VIG-003-Data-Principles.md)
  Principle 1) alongside the derived records, so re-derivation under a new `taxonomy_version` never
  requires re-calling a model.
- It is **not** authoritative for what a field means, only for what value it currently holds.

### What the filesystem owns

- Prompt content, schema content, taxonomy content, JSON Schema, and workflow exports — all under
  git, all versioned, all reviewable by diff.
- Sample images only (`ai/vision/images/`, 3 files, allowlisted in `.gitignore`). Production images
  are referenced by path/URL and never committed.

### What the taxonomy owns

- Category tree, Attribute Groups, Vocabularies, Terms, and typed Relationships — the canonical
  meaning layer.
- It owns **no** confidence, provenance, or review state. Those belong to records *about* entities,
  not to the definitions themselves. This separation is why a proposed-but-unapproved structure
  needs an evidence record alongside it (see
  [Dynamic Structure Discovery](../80_Dynamic_Structure_Discovery/SPECIFICATION.md)).

### What the Cake Genome owns

- Cake Genome is **content, not machinery** — the Bakery Domain's authored Category/Group/
  Vocabulary set, per [EPR §02](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md).
  It owns the domain's meaning, and nothing about how images are processed.
- The read-model over a whole product remains **Product Genome** (`ai.product_intelligence`,
  [ADR 0008](2026-08-02-product-intelligence-engine.md)). These are two layers, not two names for
  one thing. See [GLOSSARY.md](../00_Foundation/GLOSSARY.md).

### What the review system owns

- The transition of any record from evidence to canonical fact.
- Authority over `human_verification.status` and over promotion of any proposed structure.
- Per [EPR §04](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md): *AI agents may
  draft, extract and verify; only a human may publish a record to a live downstream system or
  override a validation gate.* No automated path may set `verified` on a customer-facing field, and
  no automated path may promote a proposed taxonomy structure to `active`.

## API boundaries

Exactly three interfaces cross the n8n↔Python line. No other coupling is permitted.

| # | Direction | Interface | Contract |
|---|---|---|---|
| 1 | Python → n8n | **Extraction bundle** — prompt text + output JSON Schema + `taxonomy_version` | Read from the filesystem at job start. n8n must not embed prompt text in workflow JSON. |
| 2 | n8n → Python | **Raw observation** — provider response, image ID, provider/model/version, timestamps | Submitted verbatim. n8n performs no interpretation. |
| 3 | Python → n8n | **Validated records** — EAL records + any structure proposals, ready to persist | n8n writes them to PostgreSQL unchanged. |

Python runs as a callable process or a thin local HTTP service — that choice is deliberately left
open here and belongs in its own ADR once the first integration is attempted, per
[VIG-002](../00_Governance/VIG-002-Architecture-Principles.md)'s "structure follows real
implementation".

## Failure handling

- **Provider failure** → n8n's concern. The existing `Build Vision Failure` and
  `Future Provider Adapter` nodes already produce a typed failure row; that pattern is kept.
- **Parse failure** → a record is still written, with `value_state: "unknown"` and the raw response
  preserved. A failed parse is data, not an absence of data.
- **Validation failure** → the record is retained and routed to review. It is never dropped and
  never patched to pass. [Validation.md](../10_Taxonomy/Validation.md): *"Validation never
  fabricates a value to satisfy completeness, and never silently resolves a consistency conflict by
  guessing."*
- **Contract-version mismatch** (n8n holding a stale `taxonomy_version`) → hard fail the batch.
  Producing records against an unknown taxonomy version breaks lineage, which is worse than not
  producing them.

## Retries

- Retries are n8n's, at the provider call only. The existing exponential-backoff pattern in
  `TBK_n8n_Deployment_Operations.md` is adopted as-is.
- Validation and parsing are **not** retried — they are deterministic; a second identical run
  yields an identical result.
- Retries must not change `TBK_IMAGE_ID`. Because it is a content hash of the image bytes
  (`ai/vision/python/pipeline.py`), a retried image is automatically idempotent.

## Provenance

The existing `ai.eal.models.Provenance` object is the required shape on every derived record, with
no additions:

```
provider, model, schema_version, taxonomy_version, extracted_at,
model_version | None, prompt_version | None
```

Two consequences follow. `prompt_version` is only meaningful once prompts are versioned files —
which is why interface #1 above moves prompt content out of workflow JSON. And a PostgreSQL row
that cannot populate `schema_version` and `taxonomy_version` must not be written at all.

## Versioning

- `taxonomy_version` and `schema_version` are set by Python and carried through n8n untouched.
- Additive taxonomy change (a new Term, a new Attribute in an existing group) is a **minor**
  change; existing records stay valid, per [Versioning.md](../10_Taxonomy/Versioning.md).
- Redefining an existing attribute's meaning is **breaking**; it requires a new `taxonomy_version`,
  and prior records remain tagged with the old one and are never silently reinterpreted.
- Workflow JSON exports are versioned in git alongside the contract they consume, so a workflow and
  the taxonomy version it was built against can always be paired.

## Consequences

**Accepted:**

- Two runtimes remain. This is a real, permanent operational cost, chosen because collapsing to one
  would discard either the governance layer or the only working execution layer.
- `tbk_taxonomy_attributes` and `tbk_taxonomy_synonyms` become generated. Their current hand-
  authored content (17 rows, 3 attribute types) must be reconciled against `bakery_v1.json` before
  the first generated export overwrites it. **That reconciliation is a prerequisite, not a
  side-effect** — nothing may overwrite those tables until it is done.
- The n8n `BUILD-3xx` numbering is retired in favour of the documented `Build-001`…`Build-012`
  sequence plus ADR 0007's "never reshuffle, only insert" rule. Existing workflow notes referencing
  `BUILD-307` are left in place as historical text and mapped in the
  [dependency map](../30_Enterprise_Program_Roadmap/IMPLEMENTATION_DEPENDENCY_MAP.md).

**Rejected alternatives are recorded above** rather than in a separate document, per
[VIG-009](../00_Governance/VIG-009-ADR-Standard.md)'s one-decision-one-document rule.

## Open questions this ADR deliberately does not decide

1. **Python-as-process vs. Python-as-service.** Needs one real integration attempt first.
2. **PostgreSQL physical schema.** This ADR fixes *who* defines it, not *what* it is. The
   storage-technology ADR that [VIG-003](../00_Governance/VIG-003-Data-Principles.md), EPR
   Build-007 and [ADR 0009](2026-08-02-product-knowledge-graph.md) have each deferred in turn is
   still owed — but its scope is now narrower, because "PostgreSQL, schema generated from the
   Python contract" is settled here.
3. **Branch strategy** for `feature/vision-engine-v1`. Out of scope by instruction; tracked as
   item 8 in the dependency map.

## Related

[EPR §03/§04/§13/§14](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md),
[ECP-100](../30_Enterprise_Program_Roadmap/ECP-100_Architecture_Review.md),
[ECP-200 Gap Analysis](../30_Enterprise_Program_Roadmap/ECP-200_Architecture_Gap_Analysis.md),
[ADR 0008](2026-08-02-product-intelligence-engine.md), [ADR 0009](2026-08-02-product-knowledge-graph.md),
[ADR 0010](2026-08-02-attribute-intelligence-engine.md),
[VIG-003](../00_Governance/VIG-003-Data-Principles.md), [VIG-005](../00_Governance/VIG-005-Versioning-Standard.md),
[GLOSSARY.md](../00_Foundation/GLOSSARY.md).
