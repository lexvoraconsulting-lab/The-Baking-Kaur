# VIG-001: Platform Principles

Status: Active
Version: 1.0

## Purpose

Defines the platform's mission and the operating principles that keep its many modules coherent as
a single system rather than a collection of unrelated tools. Where VIG-000 states *what must always
be true*, this document states *what the platform is for* and *how it grows*.

## Scope

Applies to every module family named in the platform's long-term direction: Vision Engine, Cake
Genome, Knowledge Graph, Embedding Engine, Vector Search, Visual Search, Shopify AI, SEO AI,
Marketing AI, Search Intelligence, Customer Intelligence, ERP AI, CRM AI, Business Intelligence,
JARVIS, and any module added after this document's adoption.

## Definitions

- **Module**: a bounded unit of platform capability (e.g. "Vision Engine," "Shopify AI") with its
  own code, configuration, and documentation, built on the platform's shared data foundation.
- **Shared Data Foundation**: the combination of the Knowledge Graph, Product Genome, and the
  identifier/versioning conventions (VIG-005, VIG-006) that every module reads and writes through.
- **Domain**: the specific business this instance of the platform serves today (an eggless cake
  studio). The platform's principles are written to outlive any one domain.

## Principles

1. Every module is built on the same shared data foundation. No module maintains a parallel,
   incompatible representation of an entity another module already tracks.
2. The platform must be able to add a new module family without redesigning existing modules.
   A new consumer of the Knowledge Graph is an addition, not a migration.
3. The platform must be able to extend to a new domain (a different product category, or an
   entirely different business) without rewriting its principles, only its content (taxonomy,
   prompts, schemas).
4. Growth is additive by default. A module is scaffolded only when it has a real responsibility to
   hold — speculative structure for a module with no implementation is not platform maturity, it is
   noise that must later be reconciled or removed.
5. No module is "the platform." The platform is the sum of the shared foundation plus every module
   built on it; no single module may assume permanent primacy over the others.

## Rules

- A new module must identify, before its first line of code, which parts of the shared foundation
  (identifiers, schemas, Knowledge Graph) it reads from and writes to.
- A new module may not introduce a competing identifier scheme, versioning scheme, or system of
  record for an entity type another module already governs.
- Folders, packages, or services for a module family (e.g. `knowledge_graph/`, `vector_db/`,
  `jarvis/`) are created when that module's first real implementation begins — not in advance, and
  not as placeholders. Naming a future module in a roadmap document is sufficient until then.

## Examples

- Shopify AI reads product attributes from the Product Genome rather than calling a vision provider
  directly. When Marketing AI is added later, it reads the same Product Genome — no new integration
  path to the Vision Engine is required. Correct.
- A roadmap document lists "Knowledge Graph" as a future module family with no corresponding empty
  `knowledge_graph/` folder in the repository until real code exists. Correct application of
  Principle 4.

## Non-examples

- A `marketing/` folder is created with no code inside it "to reserve the name." Violates
  Principle 4.
- A new module computes its own product attribute cache instead of reading the Product Genome,
  because integrating with the Knowledge Graph "felt slower." Violates Principle 1 and VIG-000
  Principle 6.

## Implementation Guidance

Before a new module's first commit, its author should be able to state, in one sentence each: what
entity types it reads, what entity types (if any) it writes, and which existing identifier/version
conventions it reuses rather than reinvents. If a module cannot state this, it is not yet ready to
be scaffolded.

## Future Compatibility

This document deliberately does not name specific technologies (which vector database, which graph
engine, which cloud provider) — those are ADR-level decisions (VIG-009) made when a module is
actually built, not platform-level principles fixed in advance.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. |

## Related Standards

VIG-000 (Constitution — supreme document this elaborates), VIG-002 (Architecture Principles —
how modules are structured internally), VIG-005 (Versioning Standard), VIG-006 (Identifier
Standard).

## References

- `docs/AI/Roadmap.md` — names the specific future module families this document generalizes over,
  and the explicit decision not to scaffold folders for them ahead of real implementation.
