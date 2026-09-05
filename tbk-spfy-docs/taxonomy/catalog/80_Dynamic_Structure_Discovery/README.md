# Dynamic Visual Structure Discovery v1

The layer that lets the platform record a visual observation it has **no taxonomy home for**, as an
evidence-backed proposal, instead of discarding it or forcing it into an approximate field.

Governed by [ADR 0011](../adr/2026-08-20-n8n-python-system-of-record.md) (system of record) and
specified against the frozen content of the
[Enterprise Master Taxonomy](../70_Enterprise_Master_Taxonomy/README.md) (Build-005) — the **Cake
Genome**'s authored Bakery vocabulary. Consumes the two-channel output of the
[Vision Extraction Contract](../AI/VisionExtractionContract.md) (Build-008); once a proposal is
approved and registered, the widened vocabulary flows on to the
[Product Genome](../PRODUCT_INTELLIGENCE_ARCHITECTURE.md) read model (`ai.product_intelligence`)
and the [Knowledge Graph](../KNOWLEDGE_GRAPH.md) semantic layer (`ai.knowledge`).

**This is a discovery layer, not a second taxonomy.** It defines no attribute, owns no vocabulary,
and stores no canonical value. It reuses
[EAL](../20_Attribute_Language/README.md)'s `value_state` / `Provenance` / `HumanVerification`
verbatim, [EAR](../40_Enterprise_Attribute_Registry/README.md)'s existing `status = "draft"` as the
candidate-attribute state, and
[EAD](../50_Enterprise_Attribute_Definitions/README.md)'s `allowed_values` /
`confidence_expectations` as validation input. The only genuinely new record is the proposal's
`Evidence`, which exists because `ai.taxonomy` correctly refuses to carry confidence or provenance
on its canonical entries.

## Status: Proposed — specification only, no implementation

No code exists. No frozen package has been modified. `ai/structure_discovery/` does not exist. The
one change this specification requests to frozen code — adding `"proposed"` to
`ai.taxonomy.EntryStatus` — is additive (a *minor* change under
[Versioning.md](../10_Taxonomy/Versioning.md)) but touches Build-005 and therefore requires
Architecture Gate **AR-007** to be aware of it. It has not been made.

Not yet assigned a Build number. Per [ADR 0007](../adr/2026-07-28-build-005-007-resequencing.md)'s
"never reshuffle, only insert" rule, a number is assigned when implementation is approved — not
inferred from this folder's `80_` prefix, which is a documentation-tree position, not a Build.

## The governing principle

> The taxonomy is a controlled vocabulary, not a ceiling on what the vision system can observe.

with its necessary counterweight:

> AI may observe and propose. Only a human may register a structure as canonical.

Both are already repository doctrine, not new policy — see
[Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md) (*"an unmapped observation
isn't lost, it's a signal that the vocabulary may need a new Term"*),
[EPR §04](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md) (*AI agents may draft,
extract and verify; only a human may publish*), and
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md) Principle 3 (no fabricated attributes).

## Start here

- [SPECIFICATION.md](SPECIFICATION.md) — the full specification: existing mechanisms reused, the
  four real gaps, the nine lifecycle states, the pipeline, and the machine-readable output contract.

## Document index

| Document | Covers |
|---|---|
| [SPECIFICATION.md](SPECIFICATION.md) | Reuse inventory, gaps G1–G4, nine-state model, `OBSERVE → PROPOSE → VALIDATE → APPROVE → REGISTER → VERSION → USE` lifecycle, `MatchState` / `ProposalKind` / `ProposalStatus`, `Evidence` / `StructureProposal` / `DiscoveryResult`, promotion thresholds, invariants. |
| [PHASE_1_VALIDATION_REPORT.md](PHASE_1_VALIDATION_REPORT.md) | Phase 1 gate: three canonical images run live, cross-image comparison, defects D-1…D-5, verdict (CONDITIONAL PASS) and the recommended Phase 2. |
| [README.md](README.md) | This file — scope, status, entry point. |

## Related Standards

Implements the discovery half of [Validation.md](../10_Taxonomy/Validation.md)'s verification gate
and [Controlled_Vocabulary.md](../10_Taxonomy/Controlled_Vocabulary.md)'s vocabulary-growth rule.
Reuses [EAL](../20_Attribute_Language/EAL_SPECIFICATION.md) records unchanged, and
[`ai.attribute_intelligence`](../ATTRIBUTE_ENGINE.md)'s normalizer rather than introducing a second
matching rule. Bounded by [VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) (additive vs.
breaking change), [VIG-007](../00_Governance/VIG-007-Quality-Standard.md) (confidence, provenance,
verification gate, no fabrication) and
[VIG-009](../00_Governance/VIG-009-ADR-Standard.md) (widening a frozen literal needs its own ADR).
Sequenced by [ECP-200](../30_Enterprise_Program_Roadmap/ECP-200_Architecture_Gap_Analysis.md) and
the [Implementation Dependency Map](../30_Enterprise_Program_Roadmap/IMPLEMENTATION_DEPENDENCY_MAP.md).
Terminology: [GLOSSARY.md](../00_Foundation/GLOSSARY.md).
