# TBK — Cross-Program Glossary

Date: 2026-08-20

Three programs share this repository and reuse each other's words with different meanings. This
glossary states which term is canonical for what, and — where two names describe one thing — which
name wins and why. It defines nothing new; every entry cites the document that already owns it.

**The three programs:**

| Program | Numbering | Documents | Home |
|---|---|---|---|
| **VISIONARY IMAGE GENOME™** — the AI/data platform | Build-001…012, Sprint 2.x, ECP-1xx/2xx/3xx, AR-001…012 | `docs/00_*`–`docs/80_*`, `docs/AI/`, `docs/adr/` | `ai/` |
| **Storefront transformation** — the Shopify theme rebuild | Phase A…K | root `*.md`, `docs/release/` | `layout/ sections/ templates/` |
| **SEO-audit & Liquid cleanup** | Sprint 1–2, Phase 4–7.x | `seo-audit/`, most flat `docs/*.md` | `seo-ops/` |

**Never mix their numbering.** "Phase A" is a storefront phase; "Build-005" is a platform build;
"Phase 7.6" is an SEO-audit phase. Three unrelated sequences.

---

## Genome family — the five names that cause the most confusion

| Term | Means | Owns | Canonical source |
|---|---|---|---|
| **VISIONARY IMAGE GENOME™** | The umbrella platform brand. Everything in `ai/` | Nothing directly — it is the program name | [VIG-000](../00_Governance/VIG-000-Constitution.md) |
| **EPGF** — Enterprise Product Genome Framework | The reusable, category-agnostic core: Vision + EAL + EAR + EAD + Knowledge Graph + Validation | Framework mechanics | [EPR §02](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md) |
| **Cake Genome™** | EPGF's first instance: the **Bakery Domain's authored content** — its Category tree, Attribute Groups, Vocabularies, Terms. **Content, not machinery** | Bakery domain meaning | [EPR §02](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md); realised as `ai/taxonomy/content/bakery_v1.json` |
| **Product Genome** | The normalized, application-facing **read model** over a whole product. Applications read this, never the Knowledge Graph's internals | The aggregate read surface | [VIG-003](../00_Governance/VIG-003-Data-Principles.md); implemented as `ai/product_intelligence/` |
| **Business Entity** | The same aggregate, named from the taxonomy side — the join point to Shopify/ERP/CRM | Same thing as Product Genome | [Entity_Model.md](../10_Taxonomy/Entity_Model.md) |

**Rulings:**

- **"Product Genome", "Business Entity" and "Product Intelligence" are one concept.** Settled by
  [ADR 0008](../adr/2026-08-02-product-intelligence-engine.md). "Product Genome" is the preferred
  name in prose; `ai.product_intelligence` is the package that implements it.
- **"Cake Genome" is a genuinely different layer** — domain *content*, not the product aggregate.
  Cake Genome is what Product Genome classifies *against*.
  [ECP-100 §20](../30_Enterprise_Program_Roadmap/ECP-100_Architecture_Review.md) stated Cake Genome
  "was not found named anywhere in this repository's existing documentation." **That is factually
  incorrect** — EPR §02 defines it in a dedicated subsection five days earlier. ECP-100's
  recommendation (don't invent a fourth name) still stands; its premise does not.
- **"Cake DNA" has zero occurrences in this repository** and is not canonical for anything — see
  the alias ruling below. **"Cake Intelligence"** likewise had zero occurrences before 2026-08-20;
  it is now an accepted *informal* programme name, which is not the same as a canonical one.
- **"Image Genome"** appears only in `n8n/TBK-A-OS/Readme.md.txt`'s pending list. Treat it as an
  informal reference to Cake Genome unless someone defines it otherwise.

### Accepted aliases and normalization ruling (2026-08-20)

| Form | Ruling |
|---|---|
| **TBK Cake Genome** | **Accepted equivalent** of "Cake Genome™" ([EPR §02](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)). Same referent: the Bakery Domain's authored content. Prefer "Cake Genome" in prose; the "TBK" prefix and the ™ are both optional. |
| **TBK Cake Intelligence** / **Cake Intelligence** | **Accepted** as the informal, engagement-level name for the overall intelligence programme. It does **not** supersede **VISIONARY IMAGE GENOME™**, which [VIG-000](../00_Governance/VIG-000-Constitution.md) establishes as the constitutional platform name. Changing the constitutional name requires VIG-000's own amendment process — it cannot be done by a documentation pass. Both names may be used; in governance documents (VIG, ADR, module specs) use VISIONARY IMAGE GENOME™. |
| **Cake DNA** | **Not canonical. Do not introduce.** Zero occurrences in this repository. It is not a synonym for Cake Genome, Product Genome, or anything else here. Any document using it should be corrected to the intended term. |
| **Image Genome** | Informal. Appears only in `n8n/TBK-A-OS/Readme.md.txt`'s pending list. Read as Cake Genome unless separately defined. |

Rationale: the standing instruction was to *use the existing canonical repository terminology*. Where
a requested term matches an existing one (Cake Genome), it is registered as an alias. Where a
requested term would displace a constitutional name (Cake Intelligence vs. VISIONARY IMAGE GENOME™),
it is registered as an accepted informal name rather than silently overriding
[VIG-000](../00_Governance/VIG-000-Constitution.md) — a documentation pass has no authority to amend
the constitution.

---

## Attribute stack — four layers, often confused

| Term | Answers | Package | Spec |
|---|---|---|---|
| **EAL** — Enterprise Attribute Language | *What shape is a fact?* A wire format, not a store | `ai/eal/` | [EAL_SPECIFICATION](../20_Attribute_Language/EAL_SPECIFICATION.md) |
| **EAR** — Enterprise Attribute Registry | *Does this attribute exist?* | `ai/ear/` | [EAR_SPECIFICATION](../40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md) |
| **EAD** — Enterprise Attribute **Definitions** | *What does it mean, and where does it map?* | `ai/ead/` | [docs/50_](../50_Enterprise_Attribute_Definitions/EAD_SPECIFICATION.md) |
| **Enterprise Attribute Distribution** | *How does it reach Shopify/ERP?* **No acronym** | `ai/attribute_distribution/` | [docs/60_](../60_Enterprise_Attribute_Distribution/EAD_SPECIFICATION.md) |

⚠️ **"EAD" once meant both Definitions and Distribution.** Resolved by
[ADR 0006](../adr/2026-07-27-workstream-id-convention.md): EAD = Definitions (Build-003);
Distribution (Build-004) has no acronym. Both still have a file named `EAD_SPECIFICATION.md`, in
different folders — check the path, not the filename.

---

## Record and state vocabulary

| Term | Definition | Source |
|---|---|---|
| **Attribute** | A *candidate* value parsed from an observation. Evidence, not fact | [Entity_Model.md](../10_Taxonomy/Entity_Model.md) |
| **Genome Attribute** | An Attribute that passed the verification gate and was promoted | [Entity_Model.md](../10_Taxonomy/Entity_Model.md) |
| **AI Observation** | The raw, unparsed record of one provider call. Immutable | [Entity_Model.md](../10_Taxonomy/Entity_Model.md) |
| **`value_state`** | `present` / `null` / `unknown`. `null` = does not apply; `unknown` = applies, not yet determined. **Not the same thing** | [Null_and_Unknown_Standard](../20_Attribute_Language/Null_and_Unknown_Standard.md) |
| **`human_verification.status`** | `unverified` / `pending_review` / `verified` / `rejected` / `corrected` | [Human_Verification_Standard](../20_Attribute_Language/Human_Verification_Standard.md) |
| **EAR `status`** | `draft` / `active` / `deprecated` / `retired`. `draft` is the existing candidate-attribute state | `ai/ear/models.py` |
| **Taxonomy `EntryStatus`** | `active` / `deprecated` today. A `proposed` state is **proposed, not built** | `ai/taxonomy/models.py`; [Discovery §5.1](../80_Dynamic_Structure_Discovery/SPECIFICATION.md) |
| **`MatchState`** | `matched` / `matched_synonym` / `ambiguous` / `unmatched` / `not_applicable` / `undetermined` | [Discovery §7.2](../80_Dynamic_Structure_Discovery/SPECIFICATION.md) — **proposed** |
| **`ProposalKind`** | `attribute` / `term` / `vocabulary` / `attribute_group` / `category` / `relationship` / `relationship_type` / `entity_type` | [Discovery §7.2](../80_Dynamic_Structure_Discovery/SPECIFICATION.md) — **proposed** |
| **Provenance** | provider, model, model_version, prompt_version, schema_version, taxonomy_version, extracted_at | [Provenance_Standard](../20_Attribute_Language/Provenance_Standard.md) |
| **`confidence`** | `float [0.0,1.0]` or `None`. `None` whenever `value_state` is not `present`, or when a human corrected the value | [Confidence_Standard](../20_Attribute_Language/Confidence_Standard.md) |
| **Master Taxonomy** | Build-005's authored Category / Attribute Group / Vocabulary / Term content — the Cake Genome, as data | [70_Enterprise_Master_Taxonomy](../70_Enterprise_Master_Taxonomy/README.md); architecture in [10_Taxonomy](../10_Taxonomy/Architecture.md) |
| **Validation Engine** | Build-006. Runtime enforcement of [Validation.md](../10_Taxonomy/Validation.md)'s four dimensions. **No package exists** | [EPR §07](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md) |

---

## Identifiers

| Prefix | Identifies | Derivation |
|---|---|---|
| `TBK-<16 hex>` | An image (`TBK_IMAGE_ID`) | sha256 of the image bytes — same file, same ID, no registry needed |
| `EAL-<16 hex>` | An attribute path | Content hash of `canonical_path` |
| `EAL-REL-<16 hex>` | A relationship | Content hash of `source\|type\|target` |
| `EAR-NNNNNN` | A registry entry | Sequential, single-allocator |
| `TAX-CAT/GRP/VOC/ATTR/TERM-NNNNNN` | Taxonomy entities | Sequential |
| `gid://shopify/Product/...` | A Shopify product | Shopify's. **Never wrapped in a competing primary key** (ADR 0008) |

Two philosophies, deliberately: **content hash** where multiple producers must agree without
coordination; **sequential** where one allocator owns the space. [VIG-006](../00_Governance/VIG-006-Identifier-Standard.md).

---

## Systems

| Term | Is | Is not |
|---|---|---|
| **Knowledge Graph** | Per VIG-003: a *persistent* system of record with per-attribute lineage. `ai/knowledge/` is **Phase 1 only** — semantic layer, in memory, no persistence, no lineage | A database, today |
| **TBK AI OS** | The n8n project's own name for its 8 workflows + 15 Data Tables | A documented entity in `docs/` — it is not |
| **n8n** | Execution, orchestration, retries, batch state | An owner of vocabulary or canonical data ([ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md)) |
| **TBK Kitchen ERP** | An existing external system, reachable only via `external_ids` | Anything this platform designs ([EPR §13](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)) |
| **JARVIS** | A future agent consumer of the Knowledge Graph (Build-011) | Built. Named only |
| **`seo-ops/`** | The only proven live Shopify read/write path — title, description, SEO fields | A path to `tags`, `metafields`, `variants` or `vendor` — it touches none of them |

---

## Governance

| Term | Means |
|---|---|
| **VIG-NNN** | A governance standard. VIG-000 is the constitution; the rest elaborate it |
| **ADR NNNN** | One decision, one document, immutable once accepted ([VIG-009](../00_Governance/VIG-009-ADR-Standard.md)) |
| **AR-NNN** | Architecture Review gate. A Build ships only after its gate returns GO. **AR-006 is open** |
| **Build-NNN** | A unit of platform work, 001–012. ADR 0007: never reshuffle, only insert |
| **WS-NN** | Workstream. Registry: `ATTR, SEO, GEO, AI, VIS, CRM, INV, PROD, REC`. ⚠️ **`PROD` = Production/baking-operations, not "Product"** |
| **ECP-1xx / 2xx / 3xx** | Engagement sprint labels, **not** Build numbers ([ECP-100](../30_Enterprise_Program_Roadmap/ECP-100_Architecture_Review.md) preamble) |
| **BUILD-3xx** | The n8n project's private numbering (BUILD-304…312). **No corresponding documents exist.** Retired by ADR 0011 |
| **Frozen** | Gate-passed, not to be modified without a new ADR and gate. Build-001 and Build-005 are frozen |

---

## Related

[FOUNDATION_v1.md](FOUNDATION_v1.md), [VIG-000](../00_Governance/VIG-000-Constitution.md),
[ADR 0006](../adr/2026-07-27-workstream-id-convention.md), [ADR 0008](../adr/2026-08-02-product-intelligence-engine.md),
[ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md),
[ECP-200](../30_Enterprise_Program_Roadmap/ECP-200_Architecture_Gap_Analysis.md),
[Dynamic Structure Discovery](../80_Dynamic_Structure_Discovery/SPECIFICATION.md),
[docs/CANONICAL_SOURCES.md](../CANONICAL_SOURCES.md).
