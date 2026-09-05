# Image Taxonomy — Inheritance Strategy

Sprint 2.1. Defines how a Category node determines which Attribute Groups apply to it, and how
domain extensions add new Categories/groups without touching existing ones.

## Rule: additive-only inheritance

A Category node inherits every Attribute Group applicable to its ancestors, and may add Attribute
Groups of its own. **A Category may never remove or override an inherited group.** If "Birthday
Cakes" inherits the Colour group from "Cakes", every Birthday Cake image has Colour attributes
available — a subcategory cannot opt out.

```
Bakery (Domain)
  └─ Cakes (Category)             — adds: Geometry, Colour, Material, Texture, Decoration
       └─ Birthday Cakes (Subcategory)   — adds: Occasion, Theme, Characters
            └─ Character Cakes (Type)        — adds: (none required; inherits all of the above)
```

Platform-level groups (Identity, System, AI, Audit, Search, Embeddings, Vectors, Relationships,
Review, Confidence, Provenance — see
[Attribute_Group_Architecture.md](Attribute_Group_Architecture.md)) apply to every Category
unconditionally and are not part of this inheritance chain at all — they don't need to be "added"
anywhere, which is what keeps them immune to per-domain drift.

## Why additive-only, not override-capable

An override-capable model (where a subcategory could redefine or remove an inherited group) creates
exactly the redesign risk Sprint 2.1 exists to prevent: a future change to "Cakes" would require
checking every descendant for an override that might conflict. Additive-only inheritance means a
change at any level is guaranteed to only ever add capability further down the tree, never remove
it — a parent Category can be extended without any risk to its children's existing behavior.

## Domain extension pattern

Adding a new Domain (Flowers, Gifts, Packaging, Balloons, Merchandise, Chocolate, Cookies, Brownies,
Pastries, or an unnamed future one) means:

1. Create a new top-level Category node under the new Domain.
2. Attach existing Domain/content Attribute Groups where they're reusable as-is (e.g. Colour and
   Material apply to Flowers with no changes needed to either group's definition).
3. Define new Attribute Groups only where a genuinely new kind of description is needed (e.g. a
   "Stem Count" group specific to Flowers) — following
   [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md) Principle 4, a new group is
   justified only when it has a real Attribute to hold, not spun up speculatively for a domain that
   might need it.
4. Platform-level groups apply automatically — no step is needed for Identity, AI, Confidence,
   Provenance, etc. to work for the new domain.

No existing Domain's Category tree, Attribute Group, or Attribute definition is touched by adding a
new Domain. This is the mechanism that satisfies Sprint 2.1's requirement that the architecture
support "multiple industries, future product domains... without redesign."

## Attribute-level inheritance (within a group)

An Attribute Group's individual Attributes follow the same additive rule at the Attribute level: a
Subcategory may add new Attributes to an inherited group (e.g. "Character Cakes" adds a
`character_name` Attribute to the Characters group its parent "Birthday Cakes" already has) but may
not remove or redefine an Attribute the group already defines elsewhere in the tree.

## Related Standards

Implements [VIG-001](../00_Governance/VIG-001-Platform-Principles.md) Principle 2 (growth without
redesigning existing modules), [VIG-002](../00_Governance/VIG-002-Architecture-Principles.md)
Principle 4 (minimum viable structure).
