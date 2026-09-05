# VIG-000: Constitution

Status: Active
Version: 1.0
Supersedes: `docs/AI/PROJECT_CONSTITUTION.md` (placeholder, never populated)

## Purpose

This document is the supreme governing standard of the VISIONARY IMAGE GENOME™ platform. It states
the principles that every other standard, decision, and system in the platform must be consistent
with. Where any other document appears to conflict with this one, this document controls until the
conflict is resolved by amendment.

## Scope

Applies to every present and future module of the platform, without exception: Vision Engine,
Cake Genome, Knowledge Graph, Embedding Engine, Vector Search, Visual Search, Shopify AI, SEO AI,
Marketing AI, JARVIS, ERP AI, CRM AI, Business Intelligence, and any module not yet named. No
module is exempt from this document by virtue of being early-stage, experimental, or small.

## Definitions

- **Platform**: the VISIONARY IMAGE GENOME™ system as a whole, comprising all present and future
  modules built on its shared data foundation.
- **Entity**: any first-class thing the platform tracks with a permanent identity — an image, a
  product, an observation, an embedding, or a future entity type.
- **Observation**: a claim produced by an AI provider about an entity (e.g. "this image shows a
  round cake"). An observation is evidence, not a verified fact, until it passes the standard
  described in VIG-007.
- **System of Record**: the single authoritative store for a category of data. For product/image
  attributes, the system of record is the Knowledge Graph, not any individual AI provider's output.
- **Product Genome**: the normalized, versioned, queryable representation of a product's attributes
  that applications (Shopify AI, SEO AI, Marketing AI, JARVIS, and others) are expected to consume.

## Principles

1. **Images are immutable.** Once an image is admitted to the platform, its bytes are never edited
   in place. Reprocessing produces a new observation against the same permanent identity; it does
   not alter the image.
2. **Every entity has a permanent identifier.** No entity is tracked, referenced, or reasoned about
   without a `TBK_*_ID` assigned at admission and never reused or reassigned. See VIG-006.
3. **Vision produces observations, not decisions.** No AI provider's raw output is treated as ground
   truth. It is evidence subject to confidence scoring, provenance recording, and verification.
4. **Business logic never lives inside an AI prompt.** Prompts describe what to observe; they do not
   encode pricing rules, merchandising decisions, or any logic that must be independently auditable
   and testable outside a model call.
5. **Taxonomy is authoritative.** Where a controlled vocabulary exists for a concept, observations
   are mapped onto it. Free-text observations that bypass taxonomy are provisional, not final.
6. **The Knowledge Graph is the system of record.** No downstream module (Shopify AI, SEO AI,
   Marketing AI, JARVIS, or any other) reads directly from raw AI provider output. They read from
   the Knowledge Graph / Product Genome.
7. **Every observation requires confidence.** An observation without a confidence score is
   incomplete and may not be promoted past the verification gate described in VIG-007.
8. **Every observation requires provenance.** What produced it (which provider, model, prompt
   version, schema version, timestamp) is recorded and retrievable for as long as the observation
   exists.
9. **Every schema is versioned.** No schema, taxonomy, or prompt is silently mutated. A change
   produces a new version; old versions remain resolvable. See VIG-005.
10. **Applications consume normalized Product Genome data, never raw AI output directly.** This
    keeps every consuming module (present or future) decoupled from the specifics of any one AI
    provider or extraction pipeline.
11. **AI providers are interchangeable.** No module's business logic may depend on which AI vendor
    produced an observation. Adding, removing, or replacing a provider must never require rewriting
    a consuming module.

## Rules

- No module may write directly to another module's system of record.
- No schema, taxonomy, or identifier scheme may be introduced without a version (VIG-005) and, if
  it introduces a new entity type, an identifier convention (VIG-006).
- No AI-derived attribute may be exposed to a customer-facing surface (storefront, marketing copy,
  structured data) without having passed the verification gate in VIG-007. This includes, without
  exception, any claim resembling a rating, certification, or delivery promise the business cannot
  verify it can fulfill.
- No document at any layer (VIG, ADR, or module documentation) may contradict this Constitution.
  A perceived need to contradict it is a request to amend this Constitution, not a license to
  proceed inconsistently with it.
- **Amendment process**: a VIG document (including this one) is amended in place — content edited,
  version bumped, and the change logged in its Version History table — as long as the amendment
  does not reverse a principle any already-approved ADR or shipped module depends on. An amendment
  that would reverse such a dependency instead requires a new VIG document that explicitly
  supersedes the old one, following VIG-009's ADR supersession model. This Constitution may not be
  silently reinterpreted by a lower-layer document (VIG-008 Principle 2) as a substitute for
  amending it here first.

## Examples

- An image is uploaded once, assigned `TBK-<hash>`, and reprocessed by three different providers
  over time. All three observations reference the same permanent ID. Correct.
- A vision provider's raw text output is parsed, confidence-scored, tagged with its schema version,
  and written to the Knowledge Graph before any downstream module reads it. Correct.

## Non-examples

- A script computes a product description by calling an AI provider directly inside the code path
  that renders a storefront page, with no Knowledge Graph in between. Violates Principle 6.
- Two different modules each maintain their own copy of "what this image shows," which drift out of
  sync over time. Violates Principle 6 (no single system of record) and Principle 8 (provenance
  would have prevented undetected drift).
- A prompt contains a rule like "always describe cakes under ₹1,000 as budget-friendly." Violates
  Principle 4 — that is business logic, not an observation instruction.

## Implementation Guidance

Any implementation satisfying this Constitution must be able to answer, for any entity, at any
time: what is its permanent ID, what observations exist about it, what produced each observation,
how confident each observation is, and which version of which schema each observation conforms to.
An implementation that cannot answer all five questions does not yet satisfy this Constitution,
regardless of how functional it otherwise appears.

## Future Compatibility

This Constitution is written to be industry-agnostic in its principles even though the platform's
first domain is cakes. Nothing in this document names cakes, Shopify, or any specific vendor,
precisely so the platform can extend to new product categories or entirely new industries without
requiring this document to change.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. Supersedes the unpopulated `docs/AI/PROJECT_CONSTITUTION.md` placeholder. |

## Related Standards

VIG-001 (Platform Principles), VIG-002 (Architecture Principles), VIG-003 (Data Principles),
VIG-004 (AI Principles), VIG-005 (Versioning Standard), VIG-006 (Identifier Standard), VIG-007
(Quality Standard), VIG-008 (Documentation Standard), VIG-009 (ADR Standard) — each elaborates
exactly one thread of the Principles above and must remain consistent with them.

## References

- `docs/AI/ARCHITECTURE_REVIEW_AR001.md` — the review that first surfaced the need for a
  permanent identifier and version-aware schema strategy, ahead of this Constitution formalizing
  both as platform-wide law.
- `docs/adr/2026-07-27-vision-identity-and-packaging.md` — the first concrete implementation of
  Principles 2 and 9 (TBK_IMAGE_ID, schema/taxonomy versioning), predating this document.
