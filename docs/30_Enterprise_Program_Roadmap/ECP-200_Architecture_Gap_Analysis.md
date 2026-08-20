# ECP-200 — Architecture Gap Analysis: current system vs. required system

Date: 2026-08-20
Status: **Analysis only.** No production code, Shopify data, taxonomy content, database, or branch
was modified. Successor to [ECP-100](ECP-100_Architecture_Review.md), which reviewed the Python
side alone and explicitly scoped `n8n` out.

**Required system** = the platform described by the standing functional requirement: an image
pipeline producing known attributes, discovered attributes, **and** proposals for new structure,
under controlled validation and human approval, feeding a Cake Genome consumed by search, Shopify
and AI systems.

Every "Built" claim below was verified against code or workflow JSON on disk, not against a
document asserting it.

---

## 1. Legend

| Mark | Meaning |
|---|---|
| **B** | Built — code or a workflow exists and runs |
| **D** | Documented only — a specification exists, no implementation |
| **P** | Partial — exists but does not meet the requirement |
| **—** | Absent |

---

## 2. Layer-by-layer

### 2.1 Python (`ai/`, branch `feature/vision-engine-v1` only)

| Capability | State | Evidence |
|---|---|---|
| EAL wire format | **B** | `ai/eal/` + generated JSON Schema, Build-001, AR-004 GO |
| EAR attribute registry | **B** | `ai/ear/`, Build-002, AR-005 GO |
| EAD definitions | **B** | `ai/ead/`, committed — **AR-006 never closed** |
| Attribute Distribution | **P** | `ai/attribute_distribution/` — `shopify_adapter` dry-run only, `erp_adapter` fully stubbed |
| Master Taxonomy content | **B** | `bakery_v1.json`: 6 cat / 30 grp / 17 vocab / 26 attr / 96 terms / 24 rel — frozen, AR-007 pending |
| Product Intelligence (Product Genome) | **B** | `ai/product_intelligence/`, ADR 0008 — in-memory, owns no data by design |
| Knowledge Graph (semantic) | **B** | `ai/knowledge/`, ADR 0009 — 29 node types, 33 edge types, **in-memory only** |
| Attribute Intelligence | **B** | `ai/attribute_intelligence/`, ADR 0010 — N-source reconciliation, conflict retention |
| Pricing | **B** | `ai/pricing/` — AI token cost + 8 domain ports, one live caller |
| Validation Engine (Build-006) | **—** | No package. Rules documented in [Validation.md](../10_Taxonomy/Validation.md) only |
| Persistence | **—** | None anywhere in `ai/`. By deliberate decision (ADR 0009), not oversight |
| Runtime / deployment | **—** | CLI entrypoints only; no service, no scheduler |
| **Reachable from a mainline branch** | **—** | 147 files on `feature/vision-engine-v1`; **0 on master, develop, phase-a, sync** |

### 2.2 n8n (`n8n/TBK-A-OS/`, `n8n/tbk-vision-workflow-complete/`)

| Capability | State | Evidence |
|---|---|---|
| Orchestration | **B** | `TBK Vision Master Orchestrator` — 13 nodes, webhook, Slack, sub-workflow calls |
| Input validation | **B** | `TBK Input & Validation` — 13 nodes, crypto hashing |
| Audit logging | **B** | `TBK Audit Logger` — 5 nodes, `tbk_pipeline_audits` |
| Vision call | **P** | `TBK Qwen Vision Analysis` — real Ollama call, **6 hardcoded output keys** |
| Taxonomy lookup | **P** | `TBK Taxonomy Lookup` + `tbk_taxonomy_attributes` — **17 rows, 3 attribute types** |
| Synonym normalization | **B** | `tbk_taxonomy_synonyms` with `match_type` (alias/spelling/abbreviation) + confidence |
| Attribute Intelligence | **B** | `TBK Attribute Intelligence Engine` — 15 nodes |
| AI validation | **B** | `TBK Attribute AI Validation (optional)` — 10 nodes |
| Product Intelligence | **B** | `TBK Product Intelligence Engine` — 9 nodes, `tbk_product_intelligence` |
| Conflict handling | **B** | `tbk_attribute_conflicts` — existing vs incoming value + confidences + resolution |
| **Unmapped-value loop** | **B** | `tbk_unmapped_attributes` — `raw_value`, `occurrence_count`, `suggested_canonical_id`, `status`. **Currently 0 rows** |
| Externalised business config | **B** | `tbk_pi_config` — product_type, vendor, google_product_category, `default_status: draft` |
| Persistence | **B** | n8n Data Tables today; PostgreSQL schema specified in `TBK_n8n_Deployment_Operations.md` |
| EAL envelope / `value_state` / `Provenance` / `human_verification` | **—** | None present in any workflow or table |
| Versioned prompts | **—** | Prompt is a string literal inside workflow JSON; no `prompt_version` obtainable |
| Shopify Publisher / Sync | **—** | Listed as pending in `TBK-A-OS/Readme.md.txt` |
| Embedding / Similarity / Image Genome | **—** | Listed as pending |

### 2.3 Cross-layer summary

| Layer | Current | Required | Gap |
|---|---|---|---|
| **Vision model** | Ollama `qwen2.5vl` (n8n) / `qwen2.5vl:3b` (Python) | One declared model+version, recorded in provenance | **Two different model tags for the same work** — corrupts lineage. Must be reconciled before first joint run |
| **Extraction layer** | 6 fixed keys (n8n); raw text, no parser (Python); 3 files **0 bytes** | Two-channel output: matched observations + unmatched proposals | [Vision Extraction Contract](../AI/VisionExtractionContract.md) — specified today, unimplemented |
| **Taxonomy** | Two unrelated taxonomies: 26 attrs/96 terms (Python) vs 17 rows/3 types (n8n) | One canonical source, exported to consumers | ADR 0011 §"What Python owns" — reconciliation is a **prerequisite**, not a side-effect |
| **Attribute registry** | EAR with `draft/active/deprecated/retired` | Same — already sufficient for candidate attributes | **None. Reuse as-is** |
| **Cake Genome** | Bakery domain content, 7 of 30 groups empty | Domain content that grows from evidence | Growth mechanism missing (Discovery spec); content gaps are the *first output*, not a blocker |
| **Database** | n8n Data Tables; PostgreSQL DDL written, not deployed | Persistent store, schema generated from the Python contract | Storage ADR still owed — but scope now narrowed by ADR 0011 |
| **Vector search** | No package exists. **`pgvector`: 0 hits repo-wide** | Similarity search over image embeddings | Entirely absent. Build-009. Correctly not scaffolded |
| **Knowledge graph** | `ai/knowledge/` real but in-memory; no lineage, no persistence | VIG-003's persistent system of record with per-attribute lineage | ADR 0009 Phase 1 done; Phase 2 (persistence + lineage) not started |
| **Shopify integration** | `seo-ops/` live for title/description/SEO only. **`tags`, `metafields`, `variants`, `vendor` never touched** | Write attributes to metafields; read/write tags for classification | No live tag/metafield path. Blocks Collection Architecture *and* Product Genome classification |
| **Validation** | Rules fully specified (4 dimensions); `n8n` has an optional AI-validation workflow | Runtime enforcement of structural/confidence/consistency/completeness | Build-006 — **no package exists** |
| **Review / human approval** | `HumanVerification` 5-state model built in `ai.eal`; no queue, no UI, no promotion path | Reviewer can approve a proposal and promote it to canonical | State machine exists; **transport and interface do not** |

---

## 3. How the current architecture handles the eleven required behaviours

Answering A–K directly.

| | Behaviour | Current handling | Verdict |
|---|---|---|---|
| **A** | Fixed attributes | `EARAttributeEntry` (existence) + `TaxonomyAttribute` (meaning) + `EALAttributeRecord` (instance). Three clean layers, no overlap | **Adequate. No change needed** |
| **B** | Dynamic attributes | `EAR.status = "draft"` lets an unregistered attribute exist as a candidate. Namespaces are additive (`domain.<name>`) with zero core changes | **Adequate for attributes; unused** |
| **C** | Unknown observations | `value_state: "unknown"` is a first-class third state, distinct from `"null"`, enforced by a Pydantic cross-field validator | **Adequate. Best-in-class. Unused by either runtime** |
| **D** | New attribute discovery | [Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md): *"an unmapped observation isn't lost, it's a signal the vocabulary may need a new Term."* n8n's `tbk_unmapped_attributes` is a working implementation of exactly that — for 3 attribute types | **Doctrine settled; mechanism partial (n8n only, 3 types, 0 rows)** |
| **E** | Taxonomy evolution | Additive-only inheritance; Terms deprecated never deleted; new Domain = zero changes elsewhere. But `EntryStatus = ["active","deprecated"]` — **no proposed state** | **Growth rules excellent; proposal state missing — gap G1** |
| **F** | Schema versioning | `eal_version`, `schema_version`, `taxonomy_version`, per-group and per-vocabulary versions; additive vs. breaking distinction defined; old records never silently reinterpreted | **Adequate. Fully specified, partially carried** |
| **G** | Confidence | `float [0.0,1.0]` range-enforced; `None` when `value_state` isn't `present` or when a human corrected the value. Per-group thresholds specified, not global | **Model adequate. "AI-derived ⇒ confidence set" is documented but not enforced** (AR004 Minor) |
| **H** | Provenance | Required object: provider, model, model_version, prompt_version, schema_version, taxonomy_version, extracted_at | **Adequate. `prompt_version` unobtainable while prompts live in workflow JSON** |
| **I** | Human verification | 5 states; `original_value` preserved on correction so nothing is silently overwritten | **Model adequate; no queue, no UI, no promotion path** |
| **J** | Relationships | `EALRelationshipRecord` (confidence + provenance carrying) + `ai.taxonomy.Relationship` (10 types) + `ai.knowledge.EdgeType` (33, superset, guarded by a drift test) + Image↔Business Entity modeled N:N for hampers | **Adequate and unusually careful. Closed literals block genuinely new types — gap G4** |
| **K** | Visual features | `Entity_Model.md` defines Image / Region / Object / Decoration / Writing / Packaging. Embeddings modeled as ordinary Attributes, not a parallel entity system | **Model adequate; nothing produces any of it — extraction returns 6 keys or raw text** |

**The pattern.** Nine of eleven behaviours have a governance model that is adequate or better. The
deficit is almost entirely in *execution*, not *design* — with two genuine design gaps (E and J)
that are each one literal-widening away from resolved.

---

## 4. Implemented vs. documented-only

| Documented **and** implemented | Documented, **not** implemented |
|---|---|
| EAL / EAR / EAD wire+registry+definitions | Build-006 Validation Engine |
| Master Taxonomy content (frozen) | Build-008 structured Vision extraction |
| Product Intelligence, Knowledge Graph (in-memory), Attribute Intelligence | Build-009 Embeddings + Vector Search |
| Pricing engine | Knowledge Graph persistence + lineage (VIG-003 in full) |
| n8n orchestration, audit, conflict, unmapped-value tables | Enterprise Collection Architecture (Phase 0 unstarted) |
| `seo-ops` Shopify title/description/SEO writes | Shopify `tags` / `metafields` read-write |
| `TBK_IMAGE_ID` content-hash identity | Human review queue / UI (WS-14) |
| Confidence, provenance, verification **models** | Confidence, provenance, verification **in a running pipeline** |

---

## 5. Root cause

ECP-100 §16 asked why no product aggregate existed and answered: deliberate, principled scoping.
That answer holds, and generalises.

**This program has consistently built the layer beneath the one it needed, correctly, and then
started a second program rather than finishing the first.** The Python side built five layers of
attribute infrastructure and stopped one step short of extraction — the step that would have made
any of it produce data. The n8n side, needing data, built extraction and everything downstream of
it from scratch, with a six-field schema, because reaching the Python contract was not possible
(no runtime, no persistence, unmerged branch).

Neither side did anything wrong in isolation. The failure is that no document connected them: `n8n`
appears in exactly four `docs/` files, all written a week before the n8n build existed, all
describing it as an external orchestrator that would never own data.

The correction is [ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md), and it is small,
because the two sides are almost exactly complementary: Python has every contract and no runtime;
n8n has a runtime and no contract.

---

## 6. Gap register

| ID | Gap | Severity | Blocks | Resolution |
|---|---|---|---|---|
| **X-1** | Two unreconciled taxonomies | **Critical** | Every joint operation | ADR 0011: Python canonical, n8n generated. Reconcile 17 n8n rows against 96 terms **before** any export |
| **X-2** | Vision extraction: 6-key ceiling / 0-byte files | **Critical** | The entire functional requirement | [Vision Extraction Contract](../AI/VisionExtractionContract.md) → Build-008 |
| **X-3** | `EntryStatus` has no `"proposed"` | **Critical** | Candidate values, groups, relationships | One additive word; requires AR-007 awareness (Build-005 frozen) |
| **X-4** | No evidence record for a proposal | High | Reviewable discovery | `ai/structure_discovery/` sidecar (Discovery spec §5.2) |
| **X-5** | No persistence anywhere in Python | High | Volume, lineage, VIG-003 | Storage ADR — scope now narrowed to "PostgreSQL, schema from contract" |
| **X-6** | No live `tags`/`metafields` path | High | Collection Architecture **and** Product Genome classification | Shared prerequisite; scope it once, not twice |
| **X-7** | Build-006 Validation Engine absent | High | States 7→8 of the discovery lifecycle | Only unbuilt Build with no open dependencies |
| **X-8** | Model tag mismatch (`qwen2.5vl` vs `qwen2.5vl:3b`) | Medium | Provenance integrity | Declare one; record it. Trivial, must precede first joint run |
| **X-9** | Prompts unversioned (embedded in workflow JSON) | Medium | `prompt_version` provenance field | ADR 0011 interface #1 moves prompts to files |
| **X-10** | `ai/` unreachable from any mainline branch | Medium | Everything, eventually | Out of scope by instruction; item 8 in the dependency map |
| **X-11** | Closed literals: `EntityType`, `RelationshipType`, `TaxonomyEntityType` | Medium | Genuinely new structural entities | Record proposals; promotion needs its own ADR + gate |
| **X-12** | AR-006 never closed | Low | Governance hygiene | Close it |
| **X-13** | 7 of 30 attribute groups empty; 3 requested concepts have no group | Low | Nothing — **this is the discovery mechanism's first job** | Fill from evidence, not by guesswork |
| **X-14** | `BUILD-3xx` numbering with no documents | Low | Traceability | Map to the documented sequence; retire per ADR 0011 |
| **X-15** | ECP-100 §15 and FOUNDATION_v1 §8 both described `ai/api/`, `ai/automation/`, `ai/embeddings/`, `ai/vectordb/`, `ai/ollama/` as "empty directories" — **none exists on disk** (git does not track empty directories) | Informational | Nothing | FOUNDATION_v1 §8 corrected 2026-08-20; ECP-100 carries an in-place correction note |

---

## 7. What must not be done

Recorded because each is a plausible next move that would cause real damage.

1. **Do not overwrite `tbk_taxonomy_attributes` / `tbk_taxonomy_synonyms` from `bakery_v1.json`
   before reconciling them.** The n8n tables hold 17 hand-authored rows with their own identifier
   scheme and real synonym data (`butter cream`, `buttercreme`, `bc`) that `bakery_v1.json` does
   **not** contain. A one-way export destroys it.
2. **Do not unfreeze Build-005 casually.** X-3 is one additive word. Anything beyond that reopens a
   gate that passed.
3. **Do not build discovery as a sixth silo.** ECP-100 §14's finding — no duplicate responsibilities
   anywhere — is the repository's most valuable structural property. `ai/structure_discovery/`
   references frozen packages and mutates none.
4. **Do not let the AI promote structure.** EPR §04 and VIG-007 both forbid it, and the requirement
   itself says so explicitly.
5. **Do not fill the 7 empty groups by hand to make the taxonomy look complete.** That substitutes
   invention for evidence and wastes the discovery mechanism's first and best test.

---

## Related

[ECP-100](ECP-100_Architecture_Review.md), [ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md),
[Dynamic Structure Discovery](../80_Dynamic_Structure_Discovery/SPECIFICATION.md),
[Vision Extraction Contract](../AI/VisionExtractionContract.md),
[Implementation Dependency Map](IMPLEMENTATION_DEPENDENCY_MAP.md),
[GLOSSARY.md](../00_Foundation/GLOSSARY.md),
[Enterprise_Program_Roadmap_v1.md](Enterprise_Program_Roadmap_v1.md).
