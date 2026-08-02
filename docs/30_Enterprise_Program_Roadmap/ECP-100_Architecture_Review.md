# ECP-100 — Enterprise Architecture & Governance Review

**Sprint 100.1 — Repository Research (resumed, not restarted).** Architecture only. No production
code was modified, no file renamed, no folder reorganized, no duplicate system created, and neither
Product Intelligence nor Cake Genome was implemented in this pass — this document is the complete
deliverable for this sprint. **STOP. Wait for approval.** The next implementation sprint (ECP-300
Product Intelligence Platform) begins only after explicit approval of the recommendations below.

**A note on naming, up front, because it matters for governance**: "ECP-100/ECP-300" are this
engagement's own sprint labels (the same role "Phase 7.x" played earlier in this project for the
Shopify/SEO side of the work) — they are **not** a new entry in the existing TBK AI OS Build
registry (Build-001 through Build-012, frozen per ADR 0007). If Product Intelligence is approved for
implementation, it should be assigned a real Build number and Workstream ID through this project's
own established governance process (ADR 0006's convention), not inferred from "ECP-300." See §23.

Both research passes referenced below were genuinely resumed from saved transcripts, not restarted,
per the explicit instruction — their full findings are folded into every section below with
citations preserved.

---

## 1. Repository Architecture Inventory

The "TBK AI OS" side of this repository (`ai/`, `docs/00_Governance/` through `docs/70_*`) is a
five-Build attribute-language stack, fully or partially built, plus two newly-built-this-session
capabilities (Vision's token-cost engine and the Enterprise Collection Architecture) that sit
adjacent to it, not inside it:

| Build | Title | Workstream | Status | Package |
|---|---|---|---|---|
| 001 | Enterprise Attribute Language (EAL) | ATTR | **Done** (AR-004 GO) | `ai/eal/` |
| 002 | Enterprise Attribute Registry (EAR) | ATTR | **Done** (AR-005 GO) | `ai/ear/` |
| 003 | Enterprise Attribute Definitions (EAD) | ATTR | Committed, AR-006 not formally closed | `ai/ead/` |
| 004 | Enterprise Attribute Distribution | ATTR | **Complete**, awaiting AR-011 | `ai/attribute_distribution/` |
| 005 | Enterprise Master Taxonomy | TAX | **Frozen**, awaiting AR-007 | `ai/taxonomy/` |
| 006 | Enterprise Validation Engine | ATTR | **Not started** | — (no package) |
| 007 | Enterprise Knowledge Graph | — | **Not started** — no storage-tech ADR yet | `ai/knowledge/` (empty dir) |
| 008 | Vision Engine — structured extraction | VIS | **Not started** (see §7 — today's Vision returns raw text) | `ai/vision/` (raw-text version exists) |
| 009 | Embeddings + Vector Search | — | Not started | `ai/embeddings/`, `ai/vectordb/` (empty dirs) |
| 010 | ERP + Shopify Distribution at volume | — | Not started | — |
| 011 | JARVIS integration | — | Not started | — |
| 012 | Production Release v1.0 | — | Not started | — |

Two capabilities built this session sit **outside** this numbering entirely:
- `ai/pricing/` — a provider-agnostic AI-usage token/cost engine plus a domain-extension layer
  (discounts, corporate rates, delivery, recipe costing, packaging, customization, ERP/AI-quote
  ports). Zero production integration; one live caller (`ai/vision/python/pipeline.py`).
- `docs/ENTERPRISE_COLLECTION_ARCHITECTURE.md` + `docs/COLLECTION_STRATEGY_EVIDENCE_REPORT.md` —
  Shopify-collection-layer taxonomy design (Occasion/Theme/Flavor axes, `product_type` controlled
  vocabulary, `occasion:*`/`theme:*`/`flavor:*` tag namespace). Documentation only, not implemented.

Workstream registry (ADR 0006): `ATTR, SEO, GEO, AI, VIS, CRM, INV, PROD, REC`. **`PROD` means
Production/baking-operations, not a "Product domain" workstream** — confirmed no existing workstream
ID represents a product-aggregate concept (see §13, §17).

## 2. Module Dependency Graph

```
ai/eal/  (Build-001, envelope: attribute facts about image/region/object)
  ^
  | eal_reference join
  |
ai/ear/  (Build-002, registry: "does this attribute exist", EAR-NNNNNN)
  ^
  | registry_reference join
  |
ai/ead/  (Build-003, definitions: business meaning + shopify_mapping/erp_mapping guidance)
  ^
  | registry_reference join
  |
ai/attribute_distribution/  (Build-004, write path: resolve + detect conflicts + adapters)
       |-- shopify_adapter.py   (dry-run only, no live write)
       `-- erp_adapter.py       (fully stubbed, no real ERP)

ai/taxonomy/  (Build-005, frozen, real Bakery content)
       category/vocabulary/term system - NOT joined to EAL/EAR/EAD by any code today
       (only prose-level intent that they should relate, per docs/10_Taxonomy/*)

ai/vision/  (raw-text pipeline exists; Build-008 structured extraction not started)
       TokenUsage --> ai/pricing/  (PricingService, live-wired, cost calculation)
       response (raw text) --> NOWHERE - no code path converts this into an EAL record today

ai/knowledge/   EMPTY - Build-007 not started, no storage-tech decision
ai/embeddings/  EMPTY - Build-009 not started
ai/vectordb/    EMPTY - Build-009 not started
ai/automation/  EMPTY
ai/api/         EMPTY

seo-ops/*.py  (independent - Admin GraphQL scripts, no dependency on ai/ at all)
       queries: id, handle, title, status, productType, descriptionHtml,
                priceRangeV2, options{name,optionValues}, seo{title,description}
       NEVER queries or writes: tags, vendor, totalInventory, metafields, variants
```

**The load-bearing fact this graph exposes**: every arrow above is a real, working join *within*
the attribute-language stack (EAL→EAR→EAD→Distribution), but **there is no arrow from that stack to
anything Shopify actually stores a product under** — no code anywhere resolves "this EAL/EAR/EAD
chain is about *this* Shopify product." Distribution's `shopify_mapping` carries *field-level*
guidance (which Shopify field an attribute writes to) but nothing supplies the *product-level*
identity (which product) at write time. This is the central gap formalized in §13 and §17.

## 3. Domain Boundary Analysis

| Domain | Owns | Explicitly does NOT own (per its own spec) |
|---|---|---|
| EAL | Attribute *instances* on image/region/object | Category/Vocabulary content, physical KG storage, validators |
| EAR | Attribute *existence* (schema-level registry) | Business definitions, taxonomy validation |
| EAD | Business *meaning* + target-system mapping guidance | Any actual write to Shopify/ERP/KG |
| Attribute Distribution | The write *mechanism* (resolve, detect conflict, adapt) | Which product an attribute belongs to |
| Taxonomy | Category/Vocabulary/Term content, Bakery domain knowledge | Pricing, ERP, SEO, Manufacturing (13 concepts explicitly rejected) |
| Vision | Calling a vision model, returning raw text + token usage | Parsing that text into structured attributes (Build-008, not started) |
| Pricing | AI-token cost; domain-extension points for delivery/discount/etc. | Any live Shopify pricing, any production integration |
| Collection Architecture (docs only) | Shopify collection taxonomy, `product_type`/tag vocabulary design | Implementation (Phase 0 of its own roadmap is still pending) |
| **Product/Business Entity** | **Nothing — no owner exists** | — |

Every domain above has a clean, respected boundary with every OTHER domain. The one boundary that
doesn't exist is the one enclosing "a product" itself.

## 4. Existing Enterprise Engines

- **EAL/EAR/EAD/Attribute Distribution** (Builds 001-004) — the attribute-language stack, described
  above. Genuinely enterprise-grade: dataclass+Pydantic dual models, deterministic content-hash IDs
  where multi-producer, sequential IDs where single-allocator, full test coverage per module.
- **Enterprise Master Taxonomy** (Build-005) — six real entity types (Category, AttributeGroup,
  Vocabulary, Term, TaxonomyAttribute, Relationship), frozen with real Bakery content (6 categories,
  30 attribute groups, 26 attributes, 17 vocabularies, 96 terms, 24 relationships).
- **Vision Pipeline** (pre-Build-008) — a working, tested, live-callable image-analysis pipeline
  (Ollama today), content-hash image identity (`TBK_IMAGE_ID`), but pre-structured-output: it
  returns raw text, not validated attributes.
- **Enterprise Pricing Intelligence Engine** (this session, unnumbered) — provider-agnostic
  AI-token cost engine plus 8 domain extension points, Repository+Strategy patterns, 95% measured
  test coverage, zero production callers beyond Vision's own token accounting.
- **Enterprise Collection Architecture** (this session, docs only) — a fully specified, unbuilt
  three-axis taxonomy (Occasion/Theme/Flavor) with an exact `product_type` + tag-namespace scheme
  already designed, ready to implement.

## 5. Existing Platform Services

Genuinely reusable, cross-cutting services that already exist and should be reused, not
re-implemented, by any Product Intelligence design:

- `ai.pricing.shopify_gql.gql()` (extended this session) — dual HTTP-token / authenticated-CLI
  Admin GraphQL execution, already the access pattern for every live Shopify read/write this
  engagement has performed.
- `ai.attribute_distribution.resolver.resolve_distribution()` / `conflicts.detect_conflict()` — the
  only existing write-orchestration logic for pushing an attribute value toward Shopify/ERP.
- `ai.taxonomy`'s Relationship model (`IS_A, PART_OF, BELONGS_TO, USES, RELATED_TO, PAIRS_WITH,
  CONTRASTS_WITH, COMPLEMENTS, AVAILABLE_IN, SUITABLE_FOR`) — the only existing typed-relationship
  vocabulary; a Business Entity relationship model should extend this, not invent a second one.
- `ai.eal.ids` / `ai.ear.ids` / `ai.ead.ids` / `ai.attribute_distribution.ids` — two proven ID
  philosophies (content-hash uuid5 for multi-producer entities, sequential prefixed IDs for
  single-allocator catalogs) that any new entity type should choose between, not reinvent.
- `seo-ops/`'s dry-run → review CSV → `--apply` convention — the established, safe pattern for any
  future tool (e.g. the collection architecture's proposed `classify_product.py`) that writes to
  live Shopify data.

## 6. Product Data Flow (as it exists today — fragmented, no single flow)

```
Shopify Admin (source of truth for id/handle/title/status/productType/price/options/seo)
      |
      v  (read-only, seo-ops/*.py scripts, Admin GraphQL)
seo-ops/fix_seo_snippets.py, fix_description_occasion.py, fix_mojibake.py, fix_product_handles.py
      |
      v  (narrow, single-field writes: handle-only / descriptionHtml-only / seo{title,desc}-only)
Shopify Admin (written back)
```

There is **no read/write path today that touches `tags`** — the field the entire Collection
Architecture's `occasion:*`/`theme:*`/`flavor:*` scheme depends on. No existing script reads or
writes it. This is confirmed by grep across every `seo-ops/*.py` query string (§ from Research
Agent 2). A Product Intelligence layer (or its `classify_product.py` prerequisite) would be the
**first** code in this repository to touch that field.

## 7. Vision Data Flow

```
image file (ai/vision/images/*.png)
      |
      v
compute_image_id(bytes) -> TBK_IMAGE_ID  (content-hash, deterministic, permanent)
      |
      v
VisionProvider.analyze() -> ProviderResponse{text, input_tokens, output_tokens}
      |                              |
      |                              v
      |                       ai.pricing.TokenUsage -> PricingService -> CostResult -> AuditEngine
      v
VisionResult{image_id, image_path, schema_version, taxonomy_version,
             provider_name, model, response (RAW TEXT), token_usage, cost}
      |
      v
????  <-- no code path exists past this point. response is never parsed into
          EALAttributeRecord instances, never joined to a Shopify product ID,
          never validated against ai/taxonomy's vocabulary.
```

`response` is raw, unstructured text today — Build-008 (structured extraction) is the not-yet-built
step that would turn it into something EAL-shaped. The identity join (`TBK_IMAGE_ID` → which Shopify
product this image is even *of*) does not exist in code anywhere; it's acknowledged only in prose
(`docs/10_Taxonomy/Entity_Model.md`'s "Business Entity" stub, §17).

## 8. Pricing Data Flow

```
AI provider response (Ollama today)
      |
      v
TokenUsage (always recorded, independent of pricing success)
      |
      v
PricingService.calculate_cost() --> FileConfigPricingRepository.get_pricing()
      |                                    (ai/pricing/config/<provider>.json)
      v
CostResult (calculated, or Pending with a reason - never an exception)
      |
      v
AuditEngine.record(usage, cost) --> ai/logs/pricing_audit.jsonl
```

Fully closed-loop, tested, live. Zero connection to Shopify product pricing — this engine prices AI
API calls, not cakes. The domain-extension layer (`ai/pricing/domains/`) has the shape to eventually
price a real order (delivery + discount + corporate rate), but has zero live callers today.

## 9. Collection Data Flow (as specified, not yet implemented)

```
Product (Shopify) --[product_type: fixed 8-value enum]--> Occasion collection (smart, rule = product_type match)
        |
        `--[tags: occasion:*, theme:*, flavor:*, recipient:*]--> Theme collection (smart, rule = tag match)
                                                                       |
                                                       (parent declared via custom.parent_occasion metafield)
```

This is a **complete specification** (`docs/ENTERPRISE_COLLECTION_ARCHITECTURE.md` §1, §4, §17) —
the controlled vocabulary, the tag namespace, the smart-collection rule basis, and a proposed
`classify_product.py` automation script are all designed. **None of it is built.** Phase 0
(the data-model/tagging prerequisite) has not started.

## 10. Shopify Integration Points

| Integration | Direction | Scope | Status |
|---|---|---|---|
| `seo-ops/*.py` (Admin GraphQL) | Read + narrow write | id/handle/title/status/productType/descriptionHtml/priceRangeV2/options/seo | Live, production |
| `ai.attribute_distribution.shopify_adapter` | Write (planned) | Attribute-level, via `shopify_mapping` | **Dry-run only**, never live |
| Theme deploy (`shopify theme push`) | Write | Liquid/CSS/JS files | Live, production (unrelated to product *data*) |
| `ai.pricing.shopify_gql` | Read + write | Whatever query/mutation is passed in | Live, general-purpose (this session's CLI-fallback addition) |
| Collection Architecture's proposed tooling | Write (planned) | `tags`, smart collection rules | **Not built** |

**No integration point today writes `tags`.** Every future capability that depends on the
Collection Architecture's tag scheme (and, by extension, any Product Intelligence classification)
needs this built first, or needs to build it itself as a prerequisite.

## 11. AI Integration Points

| Point | Model/Provider | Structured output? | Cost tracked? |
|---|---|---|---|
| `ai.vision` | Ollama (local), OpenAI/Anthropic/Google planned | **No** — raw text | Yes, via `ai.pricing` |
| `ai.attribute_distribution` | N/A (no AI call, pure data mapping) | N/A | N/A |
| Future Build-008 (structured Vision) | Same providers | Planned | Would reuse `ai.pricing` unchanged |
| Future Build-009 (embeddings) | Not selected | N/A | Not designed |

## 12. Reusable Components (safe to build Product Intelligence on top of, unchanged)

- `ai.eal.models.{EALAttributeRecord, ExternalId, Provenance, compute_attribute_id}`
- `ai.ear.models.EARAttributeEntry` + `ai.ear.ids.{compute_registry_uuid, allocate_attribute_id}`
- `ai.ead.models.EADDefinition` (specifically its `shopify_mapping`/`erp_mapping` fields)
- `ai.attribute_distribution.{resolver, conflicts, models.DistributionRecord}`
- `ai.taxonomy.models.Relationship` (extend its type vocabulary, don't fork it)
- `ai.pricing.{models.CostResult, service.PricingService, domains.*}` (for eventual order/product pricing)
- `ai.pricing.shopify_gql.gql()` (for any live Shopify read Product Intelligence needs)
- The Collection Architecture's `product_type` enum + tag namespace (reuse verbatim, see §17)
- `seo-ops/title_utils.py`'s `clean_base`/`is_broken`/`MOJI` (existing, tested SEO-title hygiene)

## 13. Missing Enterprise Capabilities

1. **A Business Entity / Product aggregate model** — named as a concept since "Sprint 2.1"
   (`docs/10_Taxonomy/Entity_Model.md:26`: "the join point to Shopify/ERP/CRM — a product, order, or
   customer record an Image is associated with") but **never modeled in code**. No `entity_type`
   value for it in EAL's `Literal["image","region","object"]`, no dataclass, no ID scheme.
2. **The Image ↔ Business Entity relationship itself** — explicitly specified as N:N
   (`docs/10_Taxonomy/Relationship_Model.md:19`, citing this store's own Cake Hampers as the reason:
   one photo can cover a bundle of several distinct sellable items) but no code resolves this edge.
3. **"Product Genome"** — defined in `docs/00_Governance/VIG-003-Data-Principles.md:24-26` as "the
   normalized, application-facing view derived from the Knowledge Graph. Applications read the
   Product Genome; they do not read the Knowledge Graph's internal representation directly." Zero
   implementation, zero schema, zero code. **This is the existing governance name for exactly what
   this sprint's "Product Intelligence Platform" request is asking to build.**
4. **A live `tags` read/write path** — nothing in this repo touches it today (§10).
5. **Build-008 structured Vision extraction** — the step between "raw text" and "an EAL record."
6. **Build-006 Validation Engine** — EAR/EAD's `validation_profile`/`allowed_values` fields exist
   but nothing enforces them at runtime.
7. **Build-007 Knowledge Graph physical storage** — no storage-technology ADR exists yet; `ai/knowledge/`
   is an empty directory.

## 14. Duplicate Responsibilities

**None found.** Every domain boundary in §3 is real and respected — this is a genuinely clean
finding, not a gap in the research. The one near-duplication risk is *prospective*: if Product
Intelligence is built as a second system that re-stores attribute values, business definitions, or
category assignments, it would directly violate VIG-003 Principle 2 ("No second, competing system
of record may exist for data the Knowledge Graph already governs") and duplicate EAL/EAR/EAD/
Taxonomy. See §17 and §18 for how to avoid this.

## 15. Technical Debt

- **AR-006 (Build-003/EAD) not formally closed** — carried forward from earlier in this engagement,
  still open.
- **Vision's `response` field is unstructured** — a known, acknowledged gap (Build-008), not
  something introduced this sprint.
- **`ai/knowledge/`, `ai/embeddings/`, `ai/vectordb/`, `ai/automation/`, `ai/api/` are empty
  directories** — correctly so per VIG-002's "no folder without a tenant" principle, but they are
  reserved names other designs (including a Product Intelligence Platform) must not silently
  colonize without going through the same Build-numbering governance.
- **The Collection Architecture's Phase 0 (tagging prerequisite) is unstarted** — Product
  Intelligence's classification ambitions are blocked on this exact same prerequisite, so this is
  shared, not new, debt.

## 16. Root Cause Analysis

**Why does "a whole product" not exist as a concept anywhere in this codebase, despite five Builds
of attribute infrastructure?** Because every Build to date was deliberately scoped *below* the
product level by design, not by oversight: EAL scopes to image/region/object (a deliberate choice —
`docs/20_Attribute_Language/EAL_SPECIFICATION.md`'s own non-scope section explicitly excludes
Category/Vocabulary content and Knowledge Graph storage). EAR/EAD scope to attribute *definitions*,
not instances-of-a-product. Distribution scopes to one-attribute-at-a-time writes. Taxonomy scopes
to category/vocabulary *content*, explicitly excluding Pricing/ERP/SEO/Manufacturing. **This is
correct, principled scoping, not a mistake** — VIG-002's "structure in proportion to actual
responsibilities" governed every one of these decisions, and building a product aggregate before the
attribute layer beneath it existed would have been building on sand. The gap is real, but it is the
*next*, not a *missed*, step — "Product Genome" was named in governance from the start
(`VIG-003-Data-Principles.md`) as the thing that comes after the Knowledge Graph, precisely because
the team already knew this aggregation layer would eventually be needed.

## 17. Enterprise Gap Analysis

| Gap | Severity | Blocks |
|---|---|---|
| No Business Entity / Product aggregate model | **Critical** | Everything — Distribution can't target a product, Vision can't attach output to one, Taxonomy can't classify one |
| No Image↔Business Entity relationship implementation | High | Multi-item photo scenarios (hampers), Vision→Product join |
| No Knowledge Graph storage (Build-007) | High | "Product Genome" as VIG-003 defines it literally cannot exist without this |
| No live `tags` read/write path | High | Both Collection Architecture and any tag-based Product classification |
| No Validation Engine (Build-006) | Medium | Runtime enforcement of EAR/EAD's already-defined validation fields |
| No structured Vision output (Build-008) | Medium | Turning image analysis into EAL-shaped facts automatically |

## 18. Recommended Canonical Architecture

**Do not build a new, independent "Product Intelligence Platform" as a sixth silo alongside
EAL/EAR/EAD/Distribution/Taxonomy.** Build it as the formal specification and (eventually) the
implementation of the **already-named "Product Genome"** (VIG-003) sitting *on top of* the existing
stack, joined through one new concept:

```
                    ┌─────────────────────────────────────────┐
                    │   Business Entity (NEW - the missing     │
                    │   aggregate root named in Entity_Model.md  │
                    │   since Sprint 2.1, never modeled)          │
                    └───────────────┬─────────────────────────────┘
                                    │  joins, does not replace, everything below
        ┌───────────────────────────┼───────────────────────────┐
        │                            │                            │
        v                            v                            v
  EAL attributes            Taxonomy classification       Shopify product
  (image/region/object,     (Category/Vocabulary/         (id/handle/title/
   via a NEW Image↔          Term, via Relationship         tags/productType,
   BusinessEntity edge)      types already defined)          via seo-ops'
                                                               existing GraphQL access)
        │                            │                            │
        v                            v                            v
  EAR/EAD (definitions,       Collection Architecture's    ai.pricing (once a
   shopify_mapping/           product_type + tag             real product-pricing
   erp_mapping guidance)      namespace (reuse verbatim)      domain is wired in)
        │
        v
  Attribute Distribution (the existing write mechanism -
   just needs a Business Entity ID to target, which it
   doesn't have today)
```

Concretely, this recommends: (1) define `Product`/`BusinessEntity` as a new `entity_type` in the EAL
family (or a sibling model that references EAL records the same way EAD references EAR entries) —
an aggregation, not a competing store; (2) implement the Image↔BusinessEntity relationship using
`ai.taxonomy`'s existing Relationship type vocabulary (add `HAS_IMAGE`/`DEPICTS` if needed, don't
fork the enum); (3) treat "Product Genome" as the read-model name for what this sprint calls
"Product Intelligence" — one name, not two competing ones; (4) sequence the *live, materialized*
version of this behind Build-006 (Validation) and Build-007 (Knowledge Graph), since a live read
model over ungoverned, unvalidated data would itself become the "second system of record" VIG-003
forbids — but the **specification/schema work** (the Business Entity model itself, its ID scheme,
its relationship to EAL/Taxonomy) has no such dependency and can proceed now.

## 19. Product Intelligence Entry Points

Where a future Product Intelligence Platform would attach to existing code, once built:

- `ai.eal` — via a new `entity_type` or a sibling `BusinessEntity` model referencing `entity_id`s.
- `ai.taxonomy.models.Relationship` — via a new relationship type joining an Image entity to a
  BusinessEntity entity.
- `ai.attribute_distribution` — as the *target* a `DistributionRecord` resolves against, once
  BusinessEntity IDs exist (today `target_system` has no product-level addressing at all).
- `ai.vision.python.pipeline.VisionResult` — `image_id` is already the correct join key; Product
  Intelligence would consume it, not replace it.
- `ai.pricing` — once a real product-pricing domain strategy is written (not built this sprint),
  it would price a BusinessEntity, not a raw Shopify product ID directly.
- `seo-ops/*.py`'s existing Admin GraphQL access — the only proven, live read/write path to real
  Shopify product data; any Product Intelligence sync would reuse this pattern (or
  `ai.pricing.shopify_gql`), not invent a third.
- The Collection Architecture's `product_type`/tag scheme — becomes Product Intelligence's
  classification vocabulary directly, not a second one.

## 20. Cake Genome Entry Points

"Cake Genome" was not found named anywhere in this repository's existing documentation (distinct
from "Product Genome," which is named in VIG-003). Treating it, per this sprint's own framing, as a
Baking-Kaur-specific specialization of Product Genome/Product Intelligence for cake products
specifically (design attributes, recipe references, manufacturing attributes) — its entry points are
a subset of §19's:

- `ai.taxonomy`'s existing Bakery content (`bakery_v1.json` — 6 categories, 26 attributes, 96 terms)
  is **already** cake-domain-specific content; Cake Genome would consume this directly, not
  duplicate it.
- `ai.pricing.domains.recipe_costing` (this session's interface-only extension point) is the
  existing, correctly-stubbed hook for ingredient/recipe cost data a Cake Genome would eventually
  need — it already declares exactly what real data is missing.
- Vision's design/style/decoration attributes (once Build-008 structures them) would be Cake
  Genome's primary raw-material input.

No new naming/numbering decision is recommended for "Cake Genome" separately from "Product
Genome"/"Product Intelligence" — introducing a third name for what is architecturally the same
aggregate, cake-scoped, would recreate the exact "EAD means two things" collision ADR 0006 already
had to fix once.

## 21. Enterprise Build Sequence (recommended, not decided)

1. **Now (documentation)**: ratify this review; if approved, draft the Business Entity model
   specification as an ADR + a `docs/8X_Product_Intelligence/` (or similarly numbered) doc set,
   mirroring the EAL/EAR/EAD spec pattern.
2. **Build-006 (Validation Engine)** — unblocks runtime enforcement everything downstream needs.
3. **Build-007 (Knowledge Graph)** — storage-technology ADR, then implementation. Product
   Genome/Intelligence's live read model depends on this existing.
4. **Business Entity model implementation** (new Build number, e.g. Build-013 per ADR 0007's
   "never reshuffle, only insert" rule) — the aggregate root itself, plus the Image↔BusinessEntity
   relationship.
5. **Collection Architecture Phase 0-2** (already scoped in its own doc) — the `tags`/`product_type`
   read-write path everything above also needs.
6. **Build-008 (Vision structured extraction)** — can proceed in parallel with 2-5; it only depends
   on EAL, which already exists.
7. **Product Intelligence / Product Genome live implementation** — after 2-6 exist, joining all of
   them per §18's diagram.
8. **Cake Genome** — a thin, cake-domain-scoped consumer of step 7, not a separate build track.

## 22. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Product Intelligence built as a competing system of record (violates VIG-003 Principle 2) | Medium if sequenced before Build-007 | High — re-litigates governance already settled | Sequence per §21; spec-only work now, live implementation after Build-006/007 |
| A third name ("Cake Genome") collides with "Product Genome" the way "EAD" once collided | Low if this review is followed | Medium — repeat of the exact ADR 0006 fire drill | §20's recommendation: one name, cake-scoped usage, not a second concept |
| `tags` gets written by two independently-built systems (Collection Architecture's tooling and a future Product Intelligence classifier) without coordination | Medium | Medium — conflicting tag writes | Single controlled vocabulary already specified (§9); both consumers should share one write path, not two |
| Business Entity ID scheme invented ad hoc, inconsistent with EAL/EAR's two established philosophies | Low | Medium — a third, incompatible ID scheme | §12/§18: choose content-hash vs. sequential deliberately, per the precedent in §12 |
| Scope creep: "Product Intelligence" absorbs Pricing/ERP/SEO/Manufacturing responsibilities Taxonomy already explicitly rejected | Medium | Medium | Re-affirm Taxonomy's own non-scope list in the Business Entity spec |

## 23. Architecture Decision Recommendations (for future ADRs, not adopted here)

This sprint recommends — but does not itself adopt — the following, each of which should get its
own `docs/adr/YYYY-MM-DD-*.md` following this project's established ADR process before any
implementation sprint begins:

1. **ADR-REC-1**: Adopt "Product Genome" (VIG-003's existing name) as the canonical term for what
   this sprint's request called "Product Intelligence Platform" — one name, not two.
2. **ADR-REC-2**: Assign a real Build number (next available per ADR 0007's frozen sequence) and a
   Workstream ID (new, or a case for reusing `ATTR`) to the Business Entity model, once its spec is
   drafted.
3. **ADR-REC-3**: Define the Image↔BusinessEntity relationship as an extension of
   `ai.taxonomy.models.Relationship`'s existing type vocabulary, not a new relationship system.
4. **ADR-REC-4**: Ratify the Collection Architecture's `product_type`/tag namespace
   (`docs/ENTERPRISE_COLLECTION_ARCHITECTURE.md` §1/§17) as Product Genome's classification
   vocabulary too — single source of truth across both.
5. **ADR-REC-5**: Sequence the live/materialized Product Genome implementation after Build-006 and
   Build-007, per §21 — with the Business Entity *specification* (not implementation) explicitly
   exempted from that dependency, since it's a schema/contract, not a live system.

## 24. Final Executive Summary

Five Builds of attribute-language infrastructure (EAL/EAR/EAD/Distribution/Taxonomy) are real,
tested, and cleanly bounded — every domain owns exactly what it says it owns, and nothing found in
this review duplicates anything else. The gap this sprint set out to investigate is real and
singular: **there is no aggregate concept for "a whole product" anywhere in this codebase**, despite
that gap being named in governance since early in this project (`VIG-003`'s "Product Genome",
`Entity_Model.md`'s "Business Entity" stub). This is a natural next step in an already-coherent
architecture, not a missing piece someone forgot.

**What already exists**: the full attribute-language stack, a frozen and content-populated
taxonomy, a working (pre-structured) Vision pipeline, a complete AI-cost Pricing engine, and a fully
specified (unbuilt) Collection Architecture.

**What should remain**: all of it, unchanged — no duplication was found anywhere.

**What should be merged**: nothing needs merging; the gap is additive, not corrective.

**What should become reusable**: the Business Entity model's join points (§19), once built.

**What becomes the canonical Product Intelligence Platform**: the formal implementation of the
already-named "Product Genome" — an aggregation layer over EAL/EAR/EAD/Taxonomy/Vision/Pricing/
Collections, not a sixth independent silo, sequenced behind Build-006/007 for its live form but
specifiable now.

**What becomes the Cake Genome foundation**: the same layer, cake-scoped — not a second concept.

**What becomes the future TBK AI OS foundation**: the sequence in §21, in order.

This review recommends proceeding to draft the Business Entity specification (§21 step 1) as the
next concrete deliverable, gated on approval of this document. **STOP. Waiting for approval.**

## Related

`docs/00_Governance/VIG-003-Data-Principles.md` (Product Genome's origin), `docs/10_Taxonomy/Entity_Model.md`
and `Relationship_Model.md` (Business Entity's origin), `docs/adr/2026-07-27-workstream-id-convention.md`
(ADR 0006), `docs/adr/2026-07-28-build-005-007-resequencing.md` (ADR 0007),
`docs/60_Enterprise_Attribute_Distribution/README.md`, `docs/70_Enterprise_Master_Taxonomy/*`,
`docs/AI/PricingService.md`, `docs/ENTERPRISE_COLLECTION_ARCHITECTURE.md`,
`docs/COLLECTION_STRATEGY_EVIDENCE_REPORT.md`, `Enterprise_Program_Roadmap_v1.md`.
