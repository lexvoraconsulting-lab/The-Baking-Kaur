# Image Taxonomy — Attribute Group Architecture

Sprint 2.1. Defines the logical groups Attributes are organized into, and — the key scalability
decision of this document — splits them into two tiers so that adding a new domain never touches
the groups every other domain already depends on.

## Two tiers

### Platform-level groups (defined once, apply to every domain, never modified per-domain)

| Group | Covers |
|---|---|
| **Identity** | `TBK_IMAGE_ID` and any other permanent identifiers ([VIG-006](../00_Governance/VIG-006-Identifier-Standard.md)). |
| **System** | Ingestion metadata — source, admission timestamp, file format, retirement status. |
| **AI** | Which provider/model produced an Observation ([VIG-004](../00_Governance/VIG-004-AI-Principles.md)). |
| **Audit** | Change history — who/what modified a record and when. |
| **Search** | Fields that exist purely to support search relevance, independent of any one domain's content. |
| **Embeddings** | Embedding vectors and the model/version that produced them. |
| **Vectors** | Vector-index-specific metadata (index name, dimensionality) distinct from the embedding values themselves. |
| **Relationships** | Edges to other entities — see [Relationship_Model.md](Relationship_Model.md). |
| **Review** | Human Review records ([VIG-007](../00_Governance/VIG-007-Quality-Standard.md)). |
| **Confidence** | Confidence scores attached to every Genome Attribute. |
| **Provenance** | Prompt version, schema version, taxonomy version per Genome Attribute ([VIG-005](../00_Governance/VIG-005-Versioning-Standard.md)). |

### Domain/content groups (apply per Category, extensible per domain, never redefine platform-level groups)

| Group | Covers |
|---|---|
| **Classification** | Which Category/Subcategory/Type an Image or Object belongs to. |
| **Geometry** | Shape, size, proportions. |
| **Colour** | Primary/secondary colour, palette. |
| **Material** | Physical material composition (fondant, buttercream, foam, fabric — domain-dependent). |
| **Texture** | Surface texture description. |
| **Decoration** | Decorative elements present (toppers, flowers, ribbons). |
| **Characters** | Licensed or generic characters depicted. |
| **Writing** | Visible text content (see Entity_Model.md's Writing entity). |
| **Occasion** | The occasion the product is suited for. |
| **Theme** | The visual/thematic style. |
| **Packaging** | Packaging type present (see Entity_Model.md's Packaging entity). |
| **Business** | Attributes that exist to serve a downstream Business Entity mapping (e.g. a field that maps cleanly to a Shopify product tag) without encoding Shopify-specific logic here ([VIG-004](../00_Governance/VIG-004-AI-Principles.md) Principle 3 — no business logic inside the taxonomy itself, only data that a downstream module's business logic can consume). |

## Why this split is the core scalability decision

Platform-level groups answer questions every domain needs answered identically (what is this,
which AI produced it, how confident are we, is it verified) — defining them once means Sprint 2.2's
Bakery attribute authoring and a future Flowers domain's authoring both build on the same eleven
groups without re-deciding what "confidence" or "provenance" means per domain.

Domain/content groups are where the "500 → 5,000 attributes" growth actually happens: a new
Category (e.g. Bouquets, under a future Flowers domain) can introduce new *Attributes* within
existing groups (Colour, Material, Occasion) and, if genuinely needed, an entirely new group
specific to that domain (e.g. a "Stem Count" group for Flowers) — without ever touching the
Platform-level groups or requiring a redesign of Bakery's existing groups.

## Rule: no domain may modify a platform-level group

A domain that appears to need a change to a Platform-level group (e.g. "Confidence needs a
domain-specific scale") is a signal that the group's definition was too narrow, not a license to
special-case it per domain — that change goes through
[VIG-000](../00_Governance/VIG-000-Constitution.md)'s amendment process at the platform level, so
every domain benefits from the fix, and no domain silently diverges from another.

## Versioning

Each Attribute Group definition carries its own version, incremented when Attributes are added to
or changed within it — see [Versioning.md](Versioning.md) for the full rule. An Attribute inherits
its owning group's version.

## Relationship to Category (see Hierarchy.md / Inheritance.md)

Which Domain/content groups apply to a given Image or Object is determined by its Category
assignment, following the inheritance rules in [Inheritance.md](Inheritance.md). All Platform-level
groups apply unconditionally, to every entity, in every domain, always.

## Related Standards

Implements [VIG-001](../00_Governance/VIG-001-Platform-Principles.md) (shared foundation across
modules), [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4 (minimum
viable structure — new groups added only when a real domain needs one).
