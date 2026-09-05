# Image Taxonomy — Entity Model

Sprint 2.1. Defines the core entities the taxonomy architecture is built around. This is a data
model, not a database schema — it names the entities and their responsibilities; storage
technology is a future ADR-level decision (per
[VIG-002](../00_Governance/VIG-002-Architecture-Principles.md)).

## Entities

| Entity | Responsibility |
|---|---|
| **Image** | The immutable root entity (`TBK_IMAGE_ID`, per [VIG-006](../00_Governance/VIG-006-Identifier-Standard.md)). Everything else in this model exists to describe an Image. |
| **Region** | A localized area within an Image (a bounding box or segment). Optional — not every Observation needs a Region; a Region exists when an Observation is about *part* of an Image rather than the whole thing. |
| **Object** | A distinct visual thing detected within an Image or Region (a cake, a topper, a balloon, a box). Objects carry their own Attributes and can relate to other Objects. |
| **Decoration** | A domain-specific specialization of Object for the Bakery domain (a topper, a flower, a ribbon). Future domains define their own Object specializations without modifying this entity. |
| **Writing** | A specialization capturing visible text (an OCR-style observation): text content, confidence, and the Region it was read from. |
| **Packaging** | A domain-specific specialization of Object for anything wrapping or containing the product (a box, a bag). |
| **Attribute** | A candidate value produced by parsing an Observation (e.g. `shape: round`), scoped to an Image, Region, or Object. Not yet verified — this is evidence, per [VIG-000](../00_Governance/VIG-000-Constitution.md) Principle 3. |
| **Genome Attribute** | An Attribute that has passed the verification gate ([VIG-007](../00_Governance/VIG-007-Quality-Standard.md)) and been promoted into the Knowledge Graph. Carries confidence, provenance, and schema/taxonomy version. This is what the Product Genome is built from. |
| **AI Observation** | The raw, unparsed record of one AI provider call: which provider, model, prompt version, schema version, timestamp, and raw response. One Observation may produce zero or more candidate Attributes. |
| **Human Review** | A record of a human verifying, correcting, or rejecting an Attribute before (or instead of) automatic promotion to a Genome Attribute. The concrete implementation of VIG-007's verification gate's human path. |
| **Category** | A node in the taxonomy's hierarchical classification tree (see [Hierarchy.md](Hierarchy.md)) that an Image or Object is classified under. |
| **Attribute Group** | A named, schema-level collection of related Attribute definitions (e.g. the Colour group defines `primary_colour`, `secondary_colour`). See [Attribute_Group_Architecture.md](Attribute_Group_Architecture.md). |
| **Controlled Vocabulary Term** | An authoritative term a Genome Attribute's value maps to, satisfying VIG-000 Principle 5 ("taxonomy is authoritative"). See [Controlled_Vocabulary.md](Controlled_Vocabulary.md). |
| **Relationship** | A typed edge between two entities (Object-to-Object, Image-to-Business Entity, Attribute-to-Term). The Knowledge Graph's edges. See [Relationship_Model.md](Relationship_Model.md). |
| **Business Entity** | The join point to Shopify/ERP/CRM — a product, order, or customer record an Image is associated with. The taxonomy does not model Business Entities' internal structure; it only defines how an Image relates to one. |

## Entity lifecycle (how these connect)

```
Image
  └─ AI Observation (raw, per provider call)
       └─ Attribute (candidate, parsed from Observation)
            ├─ Human Review (optional verification step)
            └─ Genome Attribute (promoted, verified, versioned)
                 └─ Controlled Vocabulary Term (normalized value, where applicable)

Image ──has──> Region ──contains──> Object ──has──> Attribute (same lifecycle as above)
Object ──specializes──> Decoration | Writing | Packaging (domain/content specializations)
Image ──classified-under──> Category
Image ──relates-to──> Business Entity
Object ──relates-to──> Object (via Relationship)
```

## Why these entities, not fewer or more

- **Attribute is separate from Genome Attribute** because [VIG-000](../00_Governance/VIG-000-Constitution.md)
  Principle 3 requires observations to be evidence, not fact, until verified — collapsing these
  into one entity would make "unverified" and "verified" indistinguishable, violating
  [VIG-003](../00_Governance/VIG-003-Data-Principles.md) Principle 5.
- **Region is optional, not mandatory**, so a whole-image Observation (most of today's Vision
  Engine output) doesn't need a meaningless placeholder Region — this keeps the model usable at
  today's simplicity level while still supporting future localized/segmented observations.
- **No "Ingredient", "Cake", or other domain-specific top-level entity exists here.** Those are
  Category values and Object specializations, not new entities — adding a new domain (Flowers,
  Gifts) extends Category and adds Object specializations; it never requires a new core entity.
  This is what makes the model support "millions of images, thousands of attributes, multiple
  industries... without redesign" (Sprint 2.1's success criterion).

## Related Standards

Implements [VIG-000](../00_Governance/VIG-000-Constitution.md),
[VIG-003](../00_Governance/VIG-003-Data-Principles.md),
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md),
[VIG-007](../00_Governance/VIG-007-Quality-Standard.md).
