# AR-003: Image Taxonomy Architecture Review

Date: 2026-07-27
Scope: `docs/10_Taxonomy/{Architecture,Entity_Model,Hierarchy,Attribute_Group_Architecture,
Inheritance,Relationship_Model,Controlled_Vocabulary,Versioning,Validation,Roadmap}.md` — the
Sprint 2.1 taxonomy architecture, reviewed against the governance library (VIG-000–VIG-009,
AR-001, AR-002) and against this store's actual catalog (per `CLAUDE.md`).

## Method

Same self-audit method as AR-002: every document in scope was authored this session, so the review
reads them adversarially for contradiction, gaps, and unstated assumptions rather than re-confirming
intent, plus a grep-verified cross-reference check (every `VIG-0\d\d` reference and every internal
`docs/10_Taxonomy/*.md` link resolves to a real file).

## Critical Issues

None found. No document authors actual taxonomy content (no real Category/Attribute/Vocabulary
lists beyond illustrative examples) — confirmed compliant with Sprint 2.1's explicit "architecture
only" instruction. No document contradicts VIG-000, and no cross-reference is broken.

## Major Improvements (fixed in this pass)

1. **Image → Business Entity cardinality was wrong for this business.**
   `Relationship_Model.md` originally modeled one Image as belonging to at most one Business Entity
   (N→1). This store's catalog includes Cake Hampers — bundles of multiple distinct sellable items
   (a cake, a card, a balloon) that plausibly share one product photo. A strict N→1 model would have
   forced an artificial choice of which single Business Entity a hamper photo belongs to, losing
   information the moment Sprint 2.2's real taxonomy meets real hamper products. **Fixed**: changed
   to N→N, with the hamper case stated explicitly as the reason.
2. **Relationship types had no stated governance.** `ON`, `NEAR`, `PART_OF` were introduced as if
   free strings, with no statement that they are themselves subject to VIG-000 Principle 5
   ("taxonomy is authoritative"). Left as-is, a future implementer could invent new relationship
   types ad hoc per module, fragmenting the Knowledge Graph's edge vocabulary exactly the way
   uncontrolled Attribute values would fragment node data. **Fixed**: `Relationship_Model.md` now
   states relationship types are a Controlled Vocabulary, versioned like any other term.

## Minor Improvements (fixed in this pass)

1. **Validation's four dimensions were presented as applying uniformly to every Attribute Group.**
   Confidence-thresholding and consistency-conflict checks are meaningful for a classification value
   but don't naturally apply to a raw embedding vector in the Embeddings group. Presenting them as
   uniform risked a future implementer forcing a meaningless "confidence score" onto embeddings just
   to satisfy the document as originally written. **Fixed**: `Validation.md` now states which
   dimensions apply with which weight per group, using Embeddings as the concrete example.
2. **`Attribute_Group_Architecture.md` never mentioned that groups are versioned**, even though
   `Versioning.md` states this as a rule. A reader starting from the group-defining document had no
   way to discover that fact without independently finding `Versioning.md`. **Fixed**: added a
   one-line cross-reference.

## Minor Improvements / Future Scalability Risks (not fixed — correctly deferred)

1. **Category tree traversal at scale.** `Hierarchy.md` permits unbounded depth below Subcategory,
   and `Inheritance.md`'s additive rule means resolving "which Attribute Groups apply to this
   Category" requires walking the tree to the root. At the "millions of images" scale named in
   Sprint 2.1's success criteria, a naive parent-pointer implementation would make this walk
   expensive per read. **Not fixed in this pass**: this is a storage/query-implementation decision
   (materialized path, closure table, or cached/denormalized "applicable groups" per Category),
   correctly deferred to whichever future ADR selects the Knowledge Graph's physical storage
   technology, per [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md). Flagged here so
   Sprint 2.2+ implementers don't discover it cold.
2. **No enforcement mechanism** for the additive-only inheritance rule or the "no domain modifies a
   platform-level group" rule beyond review discipline — same category of gap AR-002 already noted
   for the governance library generally, now confirmed to extend to the taxonomy architecture too.
   Appropriately deferred until a second real domain is added to check against.

## Scalability Risks (verified, no fix needed)

Confirmed by design, not just assumed: adding the 5,000th Attribute is adding one row under an
existing or new Attribute Group — no Category, other group, or Vocabulary is touched
([Attribute_Group_Architecture.md](Attribute_Group_Architecture.md),
[Inheritance.md](Inheritance.md)). Adding a new industry Domain (Flowers, Gifts, etc.) is a new
subtree plus, at most, a small number of new domain-specific groups — no existing Domain's data is
touched ([Inheritance.md](Inheritance.md) "Domain extension pattern"). This satisfies Sprint 2.1's
500/1,000/3,000/5,000+ success criterion structurally, independent of which database eventually
implements it.

## Knowledge Graph / Vector DB Compatibility

Confirmed: the Entity Model + Relationship Model together are a complete logical Knowledge Graph
schema (nodes: Image/Region/Object/Attribute/Genome Attribute/Category/Term/Business Entity; typed,
versioned, provenance-carrying edges). Embeddings are modeled as an Attribute within the
Embeddings group scoped to whatever was embedded, meaning a Vector Search implementation reuses the
same Relationship Model rather than needing a parallel entity system — verified in
`Relationship_Model.md`'s "Vector Search / Embedding compatibility" section.

## Naming Consistency

Verified: all ten documents plus `Architecture.md` use consistent terminology for every shared term
(`Genome Attribute`, `Controlled Vocabulary Term`, `TBK_*_ID`, `Product Genome`) with no
abbreviation or renaming drift between documents. Section structure across the ten content
documents is not templated as rigidly as the VIG series (no fixed 12-section requirement was placed
on this sprint), but every document consistently ends with a "Related Standards" section citing
the specific VIG principle(s) it implements — checked via grep, present in all ten.

## Final Readiness Score

**9/10.** Both Major findings and both fixable Minor findings were closed in this same pass. The
remaining point is withheld for the one legitimately deferred item with real near-term consequence
(Category-tree query performance) — not a defect in the architecture, but a decision Sprint 2.2/2.3
implementers will need to make deliberately rather than discover under load.

## Go / No-Go Recommendation

**GO** for authoring the Master Image Taxonomy (Sprint 2.2). The architecture is internally
consistent, grounded in this store's actual catalog structure (the hamper cardinality fix), fully
cross-referenced to the governance library with no duplication, and structurally verified to
support the required attribute-count growth without redesign. Sprint 2.2 should begin with the
Bakery domain's highest-value Attribute Groups (Classification, Colour, Decoration, Occasion) per
[Roadmap.md](Roadmap.md), and its authors should treat the deferred Category-tree performance
question as a decision to make explicitly before, not after, real volume arrives.
