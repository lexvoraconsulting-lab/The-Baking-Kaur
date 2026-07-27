# Image Taxonomy — Roadmap

## Sprint 2.1 (this work) — architecture only

Entity Model, hierarchies (Category / Attribute Group / Vocabulary), inheritance strategy, domain
extension pattern, relationship model, controlled vocabulary mechanics, versioning strategy,
validation strategy. No actual taxonomy content (no real Category names beyond illustrative
examples, no real Attribute lists, no real Vocabulary Terms) was authored — per this sprint's own
explicit instruction not to.

## Sprint 2.2 (not started) — author the Master Image Taxonomy for Bakery

Using this architecture, author the actual Bakery domain's Category tree, populate the
Domain/content Attribute Groups (starting with the highest-value groups — Classification, Colour,
Decoration, Occasion) with real Attributes, and seed the first Controlled Vocabularies (Shape,
Colour Name, Occasion). This is where "hundreds of taxonomy attributes" actually gets written,
against the structure this sprint defined.

## Sprint 2.3+ (not started) — Vision Engine integration

Wire the Vision Engine's `_load_prompt`/schema-file fallback (currently pointing at empty
placeholders, see [docs/AI/VisionPipeline.md](../AI/VisionPipeline.md)) to the real schema/taxonomy
authored in Sprint 2.2, and implement the structured-output parsing step (Observation → candidate
Attribute) that has been deferred since Vision Engine Phase 1
([docs/AI/Roadmap.md](../AI/Roadmap.md)).

## Future domains (not started, no timeline)

Flowers, Gifts, Packaging, Balloons, Merchandise, Chocolate, Cookies, Brownies, Pastries, and
unnamed future categories — each added as a new Domain following the extension pattern in
[Inheritance.md](Inheritance.md), when there is a real business reason to support that domain. No
folders, Category nodes, or Attribute Groups for these are created ahead of that need
([VIG-001](../00_Governance/VIG-001-Platform-Principles.md) Principle 4).

## Explicitly deferred, tracked for awareness only

Knowledge Graph physical storage choice, Vector Search/embedding infrastructure, Recommendation
Engine, AI Training pipeline, JARVIS integration, ERP/CRM field mapping — all of these consume this
taxonomy's Entity/Relationship Model once built, but none are designed or implemented here. This
mirrors [docs/AI/Roadmap.md](../AI/Roadmap.md)'s existing "documented, not scaffolded" approach to
the same future modules.
