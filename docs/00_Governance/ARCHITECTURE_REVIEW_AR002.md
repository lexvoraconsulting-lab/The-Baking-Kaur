# AR-002: Governance Library Architecture Review

Date: 2026-07-27
Scope: `docs/00_Governance/VIG-000` through `VIG-009`, `SPRINT_2_0_COMPLETION_REPORT.md`,
`docs/adr/2026-07-27-vision-provider-abstraction.md`, `docs/adr/2026-07-27-vision-identity-and-
packaging.md`, `docs/AI/{Architecture,FolderStructure,VisionPipeline,Configuration,Roadmap,
PROJECT_CONSTITUTION}.md`, and every cross-reference between them.

Distinct from AR-001 (which reviewed the Vision Engine's code), this review audits the governance
library itself — the ten VIG documents produced in Sprint 2.0 — for internal consistency,
duplication, gaps, and whether it will hold up as the platform grows.

## Method

Every document in scope was authored by the same session performing this review, so this is a
self-audit rather than an independent-team review in the literal sense — mitigated by reading each
document adversarially (checking for contradiction, duplication, and unstated assumptions) rather
than re-confirming intent. Checks performed: cross-reference resolution (grep-verified: every
`VIG-0\d\d` reference across all 18 files in scope resolves to an existing document), section-
structure consistency (grep-verified: all 10 VIG documents contain exactly the same 12 required
section headings), terminology consistency ("Product Genome" vs. domain-specific "Cake Genome"),
and a read-through of every document's Principles/Rules/Examples against VIG-000's principle list
for contradiction.

## Critical Issues

None found. No document contradicts VIG-000's principle list, no cross-reference is broken, and no
document makes a claim that misrepresents the platform's actual current state in a way that would
mislead a reader about what exists versus what is planned (the one instance found — see Minor
Improvements — was a tense/framing issue in an illustrative example, not a factual
misrepresentation of system state, and has been fixed in this pass).

## Major Improvements (fixed in this pass)

1. **No amendment process existed for the VIG documents themselves.** VIG-009 defines how ADRs are
   superseded, and every VIG document carries a Version History table, but nothing stated the rule
   for *when* a VIG document is edited in place versus superseded by a new one — a real gap for a
   document set explicitly designed to govern the platform "for many years." **Fix applied**:
   added an explicit Amendment Process rule to `VIG-000-Constitution.md`'s Rules section — in-place
   amendment with a version bump and Version History entry, unless the change would reverse a
   principle an already-approved ADR or shipped module depends on, in which case a new superseding
   VIG document is required instead.
2. **`VIG-005-Versioning-Standard.md`'s scope was ambiguous about whether it governs the VIG
   documents' own versioning.** Its Scope section named "extraction schemas, taxonomies, prompts,
   and any future artifact class with the same property" without stating whether governance
   documents count — and the VIG documents use `Version: 1.0`-style versioning, not the `v1`/`v2`
   sequential style VIG-005 mandates for content artifacts, creating an apparent (if likely
   unintended) inconsistency. **Fix applied**: added an explicit scope exclusion to VIG-005 stating
   that governance documents follow VIG-000's amendment process and VIG-009's ADR model instead,
   since they are incrementally revised prose, not machine-consumed contracts.

## Minor Improvements (fixed in this pass)

1. **`VIG-003-Data-Principles.md`'s Marketing AI example used present tense** ("Marketing AI reads
   a product's attributes...") in a way that could read as asserting Marketing AI already exists,
   inconsistent with `VIG-001-Platform-Principles.md`'s correctly-hedged phrasing ("When Marketing
   AI is added later..."). **Fix applied**: reworded to match VIG-001's hedged framing.
2. **No navigational index existed across the ten documents**, already flagged as a Suggested
   Improvement (not a defect) in `SPRINT_2_0_COMPLETION_REPORT.md`. A reader had to open VIG-000
   and follow Related Standards citations manually to find their way around. **Fix applied**: added
   `docs/00_Governance/INDEX.md` with a one-line summary of each document.

## Minor Improvements (not fixed — tracked, not blocking)

1. **No enforcement mechanism beyond review discipline.** Confirmed still true and still not
   addressed (this was already an Open Question in the Sprint 2.0 report). This is appropriately
   deferred — introducing a lint rule or CI gate now, with zero real modules built against these
   standards yet, would be process for its own sake. Revisit once a second real module exists to
   check compliance against.
2. **VIG-002 and VIG-004 both discuss provider interchangeability** at different altitudes (VIG-002
   generally, VIG-004 AI-specific) and cross-reference each other correctly — not duplication, but
   worth flagging that a future reader skimming only one of the two could miss the other's more
   specific rules. No fix needed; both documents' Related Standards sections already point to each
   other.

## Missing Principles Check (against the original mission brief)

Confidence scores (VIG-007), human verification (VIG-007), provenance (VIG-000, VIG-003, VIG-007),
reprocessing (VIG-003 example), Knowledge Graph as system of record (VIG-003, VIG-000), schema
versioning (VIG-005), permanent identifiers (VIG-006), AI provider interchangeability (VIG-004) —
all present. Embeddings and vector search are named only as examples within existing documents
(VIG-001, VIG-005), not given a dedicated VIG document — correctly deferred, since no embeddings
code exists yet and a principle document with nothing to govern would itself violate VIG-001
Principle 4. Shopify-specific field readiness (title, alt text, tags, structured data) is
deliberately absent from all VIG documents, since VIG documents state rules, not implementation
targets for one consuming module — this is correct application of VIG-008's layering, not a gap.

## Future Scalability Risks

`VIG-006`'s content-hash identifier strategy is explicitly scoped (via its own Principle 4) to
entities with stable, hashable content — the standard already anticipates that not every future
entity type (e.g. a live session, a customer) will fit the content-hash model, and provides the
fallback (random generation, still permanent and non-reusable) without requiring a future amendment
to VIG-006 itself. No other scalability risk was found in this pass — the library's principles are
written at a level of abstraction (VIG-008's own requirement) that doesn't lock in a technology
choice a future module would need to fight.

## Final Readiness Score

**9/10.** Both Major findings and both fixable Minor findings were closed in this same pass,
verified by re-running the cross-reference and structure checks after editing. The remaining point
is withheld for the one legitimately deferred item (no enforcement mechanism yet) — appropriately
deferred, not a defect, but real until a second module exercises these standards in practice.

## Go / No-Go Recommendation for Sprint 2.1

**GO**, conditional on nothing further — the governance library is now internally consistent, its
one real gap (amendment process) is closed, and its structure has been verified end-to-end. Sprint
2.1 (Master Image Taxonomy) may begin. `VIG-005-Versioning-Standard.md` will be the standard most
directly exercised by that work (taxonomy versions); its authors should confirm in practice that
the sequential `v1`/`v2` convention holds up for taxonomy specifically, and report back if it
doesn't — per VIG-000's newly-added amendment process, that would be a documentation fix, not a
blocker.
