# ADR 0009: Product Knowledge Graph scope — semantic layer now, persistence later

Date: 2026-08-02

## Status

Accepted

## Context

Build-302 asked for an "Enterprise Product Knowledge Graph" — explicitly *not* a database, but
"the canonical semantic relationship engine that every future intelligence module will consume."
Repository discovery found this is not a green-field decision:

1. `ai/knowledge/` has existed, empty, since this repo's early scaffolding. ECP-100 already
   recorded it as **Build-007, "Knowledge Graph — not started, no storage-tech ADR yet."** This
   sprint (renumbered Build-302) is that build, not a second, competing package.
2. `docs/00_Governance/VIG-003-Data-Principles.md` already defines "Knowledge Graph" precisely: a
   **persistent, authoritative system of record**, with per-attribute **lineage** back to the
   observation that produced it, gated by VIG-007's verification gate. It explicitly reserves the
   storage-technology decision for "a future ADR" and cites `ARCHITECTURE_REVIEW_AR001.md` §8
   ("the absence of a persistence/lineage layer [is] the correct next prerequisite before any
   Knowledge Graph work begins").
3. `docs/10_Taxonomy/Entity_Model.md` and `Relationship_Model.md` (Sprint 2.1) already designed
   half of this schema — the image side (Image → Region → Object → Attribute → Genome Attribute →
   Controlled Vocabulary Term, plus a typed, confidence+provenance-carrying Relationship edge type)
   — and state plainly: "This Relationship Model, combined with the Entity Model, *is* the
   Knowledge Graph's logical schema." It was never implemented in code. It also explicitly declines
   to model "Business Entity" internal structure, leaving that gap open for exactly this sprint.
4. VIG-003's data-flow direction is: **Product Genome reads from the Knowledge Graph** (Principle
   3: "The Product Genome is the only data surface applications read from"). But
   `ai/product_intelligence/` (ECP-300, already shipped) resolves its `ProductAggregate` directly
   from EAL/EAR/EAD/Taxonomy/Pricing — there is no Knowledge Graph in that path today.

Point 4 is a genuine, pre-existing architectural gap this sprint does not close, and must not
silently paper over.

## Decision

1. **Build-302 is Phase 1 of VIG-003's Knowledge Graph vision, not the whole thing.** It delivers
   the semantic relationship layer (typed nodes and edges, resolved live, held in memory,
   queryable) explicitly requested — no persistence, no lineage, no storage-technology decision.
   VIG-003 compliance (a persistent system of record with per-attribute lineage) remains future
   work, gated on its own storage-tech ADR, exactly as VIG-003 already anticipated.
2. **Implemented at `ai/knowledge/`**, the existing empty Build-007 scaffold — not a new directory.
3. **`NodeType`/`EdgeType` are a superset of the existing, governance-approved vocabulary**, not a
   replacement. Every Entity_Model.md entity (Image, Region, Object, Decoration, Writing,
   Attribute, Genome Attribute, AI Observation, Human Review, Category, Attribute Group,
   Controlled Vocabulary Term, Business Entity) has a corresponding `NodeType`. `EdgeType` includes
   every `ai.taxonomy.models.RelationshipType` string value verbatim (guarded by
   `test_edge_type_is_superset_of_taxonomy_relationship_type`, so future drift fails a test rather
   than silently diverging) plus Relationship_Model.md's Object-to-Object types (`ON`, `NEAR`,
   `MATCHES`) plus the commerce-side predicates Build-302 requested. `ai.taxonomy`'s own frozen
   Build-005 `Relationship` model is unmodified.
4. **Commerce-side entities (Product, Variant, Collection, Occasion, Theme, Flavor, Recipient,
   Pricing, SEO, ...) fill the gap Entity_Model.md explicitly left open** ("The taxonomy does not
   model Business Entities' internal structure") — this is genuinely new scope, not a duplicate of
   anything already built.
5. **Node identity is always a namespaced wrapper of a real, existing identifier** (a Shopify GID,
   a `TAX-CAT-NNNNNN`, an `EAR-NNNNNN`), never a new hash-derived identity competing with one that
   already exists — the same discipline `ai.product_intelligence.ProductIdentity` already
   established (ADR 0008), applied here across every node type.
6. **Known, flagged deviation from VIG-003's ideal data-flow direction**: this sprint's
   `KnowledgeGraphService` reads FROM `ai.product_intelligence` (`ProductAggregate`/
   `ProductReadModel`) and FROM `ai.taxonomy`/`ai.pricing` directly — the reverse of VIG-003
   Principle 3's end-state ("Product Genome reads from the Knowledge Graph"). This is a deliberate,
   pragmatic bootstrap: `ai.product_intelligence` already exists with real resolvers and real data;
   inverting the dependency today would mean rewriting already-shipped, approved ECP-300 code, out
   of Build-302's scope. **Not fixed here, not silently claimed as compliant.** Recommended as a
   Sprint 303+ item: once the Knowledge Graph has real persistence and lineage, re-point
   `ai.product_intelligence`'s resolvers at the Knowledge Graph instead of raw EAL/EAR/EAD, so the
   dependency direction matches VIG-003 exactly.
7. **Every resolver with no real backing system in this repo is a `NotConnected*` port**, mirroring
   `ai.pricing.domains.erp_integration`'s established pattern, not a fabricated implementation:
   Merchant (Google Merchant Center — no read integration exists; shipping is Manual per
   CLAUDE.md), Embedding/Vector Search (`ai/embeddings`, `ai/vectordb` are confirmed-empty
   scaffolds), Recommendation, Automation (`ai/automation` empty), Analytics. AI Genome and ERP
   reuse `ai.product_intelligence.extensions`'s existing `AIGenomeSyncPort`/`ERPSyncPort` directly
   — not redefined, per this sprint's own "prefer composition over duplication" principle.
8. **Inference is rule-based traversal, not ML**, per Build-302 Phase 6's explicit instruction: an
   `InferenceChain` is a declared, ordered predicate sequence walked one hop at a time over real
   edges; a broken/missing hop returns an honest partial path, never a fabricated one.

## Consequences

- Any future consumer (Vision AI, Search Intelligence, a real Recommendation Engine, ERP,
  Automation, Analytics) queries `ai.knowledge.GraphQueryEngine` instead of building its own
  relationship model — satisfying Build-302's stated success criterion.
- `docs/10_Taxonomy/Entity_Model.md` and `Relationship_Model.md` should eventually be updated
  (follow-up, not part of this ADR) to note that their logical schema is now implemented in code at
  `ai/knowledge/`, and to reference this ADR for the commerce-side extension.
- The VIG-003 direction-of-dependency gap (point 6) is now a tracked, documented decision instead
  of an unexamined one — the correct outcome per this project's standing "stop and flag architecture
  conflicts" rule, even though closing it is out of this sprint's scope.
- No storage-technology ADR is created by this decision; `ai/knowledge/`'s graph remains rebuilt
  on-demand, in memory, from live resolver calls, same as `ai.product_intelligence.ProductAggregate`.

## Notes

Satisfies VIG-009's one-decision-one-document rule. Extends [ADR 0008](2026-08-02-product-intelligence-engine.md)'s reasoning (real IDs over invented ones, ports over fabricated
implementations, composition over duplication) to the Knowledge Graph. Does not supersede or modify
VIG-003, VIG-006, VIG-007, or `ai.taxonomy`'s frozen Build-005 contract.
