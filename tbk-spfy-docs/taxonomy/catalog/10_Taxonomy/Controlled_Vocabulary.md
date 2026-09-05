# Image Taxonomy — Controlled Vocabulary

Sprint 2.1. Defines what a controlled vocabulary is, how a Genome Attribute's value normalizes onto
one, and how vocabularies grow — the concrete mechanism behind
[VIG-000](../00_Governance/VIG-000-Constitution.md) Principle 5, "taxonomy is authoritative."

## What a Controlled Vocabulary is

A named, versioned set of authoritative Terms for one Attribute or family of Attributes (e.g. a
"Shape" vocabulary with Terms `round`, `square`, `heart`, `number`, `custom`). Not every Attribute
needs one — free-text Attributes (e.g. an open-ended description field) are valid but are
explicitly *not* authoritative in the same sense; only vocabulary-backed Attributes satisfy the
Constitution's "taxonomy is authoritative" principle for that value.

## Term structure

Each Term carries:

- A stable identifier, independent of its label (so renaming a Term's display label never breaks
  references to it — same principle as [VIG-006](../00_Governance/VIG-006-Identifier-Standard.md)).
- A canonical label.
- Zero or more synonyms/aliases used to normalize free-text Observations onto this Term.
- An optional parent Term, where a shallow within-vocabulary hierarchy helps grouping or similarity
  (e.g. "Maroon" as a child of "Red").
- A status: Active, Deprecated (see [Versioning.md](Versioning.md)).

## Normalization: Observation → candidate Attribute → Term

An AI Observation produces free text ("looks reddish-brown"). Parsing that into a candidate
Attribute is a separate step from normalizing that candidate onto a Controlled Vocabulary Term
("Maroon") — these are two distinct operations, and the taxonomy models them as two distinct
states (candidate Attribute value vs. Genome Attribute's normalized Term reference), not one. This
lets a candidate Attribute exist and be human-reviewable even before a matching Term is found or
created — an unmapped observation isn't lost, it's a signal that the vocabulary may need a new Term.

## Growing a vocabulary

Adding a new Term to an existing vocabulary is additive: create the Term, it becomes immediately
available for new Genome Attributes to reference. Existing Genome Attributes referencing other
Terms are unaffected. This is the same additive-growth principle as
[Inheritance.md](Inheritance.md) applied to vocabulary content instead of the Category tree.

## Deprecating a Term

A Term is never deleted. It is marked Deprecated and, where a replacement exists, points to the
Term that supersedes it — mirroring
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) Principle 4's migration-path requirement.
Genome Attributes already referencing a deprecated Term remain valid and resolvable; new Attributes
are steered toward the replacement.

## Vocabulary scope

A vocabulary may be global (reusable across every Domain — e.g. "Colour Name") or domain-scoped
(meaningful only within one Domain — e.g. a "Flower Type" vocabulary meaningful only under a future
Flowers domain). This mirrors the platform-level vs. domain-level split in
[Attribute_Group_Architecture.md](Attribute_Group_Architecture.md) — a global vocabulary is defined
once and reused; a domain-scoped vocabulary is added when its domain is added, without touching
any other vocabulary.

## Related Standards

Implements [VIG-000](../00_Governance/VIG-000-Constitution.md) Principle 5,
[VIG-005](../00_Governance/VIG-005-Versioning-Standard.md) (Term versioning/deprecation),
[VIG-006](../00_Governance/VIG-006-Identifier-Standard.md) (stable Term identifiers).
