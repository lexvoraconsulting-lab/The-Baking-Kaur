# Image Taxonomy — Versioning Strategy

Sprint 2.1. Applies [VIG-005 (Versioning Standard)](../00_Governance/VIG-005-Versioning-Standard.md)
concretely to every versionable artifact this taxonomy architecture introduces: Category tree
structure, Attribute Group definitions, individual Attribute definitions, and Controlled Vocabulary
Terms.

## What gets a version

| Artifact | Versioned as | Immutable once published? |
|---|---|---|
| Taxonomy as a whole | `taxonomy_version` (e.g. `v1`, matching the existing `ai/vision/config/vision.json` field) | Yes — a new overall version is cut when any of the below changes in a way that affects interpretation of existing data. |
| Category tree | Implicitly versioned via the overall taxonomy version; individual Category nodes carry a stable ID (Hierarchy.md) that outlives tree reshuffling. | Node IDs: yes. Tree shape: no — the tree may grow between taxonomy versions as long as growth is additive (Inheritance.md). |
| Attribute Group definition | Its own version, incremented when Attributes are added to or changed within it. | Yes, per VIG-005 Principle 2. |
| Attribute definition | Inherits its owning Attribute Group's version. | Yes. |
| Controlled Vocabulary | Its own version, incremented when Terms are added or deprecated. | Yes for existing Terms; new Terms are additive. |

## Rule: additive changes don't require a new major version; redefinitions do

Adding a new Category, a new Attribute within an existing group, or a new Vocabulary Term is a
**minor, additive change** — existing Genome Attributes are unaffected, and the taxonomy version
can increment without invalidating anything already extracted.

Redefining what an existing Attribute *means* (not just adding to its group, but changing what
`primary_colour` is expected to represent) is a **breaking change** — it requires a new taxonomy
version, and Genome Attributes produced under the old version remain tagged with that old version
and are not silently reinterpreted (per VIG-005 Principle 2 and
[VIG-003](../00_Governance/VIG-003-Data-Principles.md) Principle 4, lineage).

## Every Genome Attribute records its version at creation

Consistent with the `schema_version`/`taxonomy_version` fields already introduced in the Vision
Engine ([ADR 0004](../adr/2026-07-27-vision-identity-and-packaging.md)), every Genome Attribute
carries the taxonomy version (and, where applicable, the specific Attribute Group and Vocabulary
version) active at the time it was created. This is what lets a future schema-evolution project
identify exactly which records need reprocessing when a definition changes, without guessing from
timestamps.

## Reprocessing and migration

When a taxonomy version is deprecated, existing Genome Attributes are not deleted or silently
migrated — they remain queryable, tagged with their original version, until an explicit
reprocessing pass (a future Vision Engine batch capability, not built yet) produces new Genome
Attributes under the new version. This is the taxonomy-specific instance of
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) Principle 4's migration-path requirement.

## Related Standards

Implements [VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) in full, for the taxonomy
domain specifically. Cross-references
[VIG-003](../00_Governance/VIG-003-Data-Principles.md) (lineage) and
[Controlled_Vocabulary.md](Controlled_Vocabulary.md) (Term-level deprecation).
