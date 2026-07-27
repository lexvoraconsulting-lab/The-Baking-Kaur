# VIG-008: Documentation Standard

Status: Active
Version: 1.0

## Purpose

Defines the platform's documentation layers, so that principles, decisions, and system descriptions
each have exactly one authoritative home and never duplicate one another.

## Scope

Applies to every document the platform produces about itself: governance standards, architecture
decision records, and per-module system documentation.

## Definitions

- **VIG Document**: a platform-wide principle or standard (this document series), living in
  `docs/00_Governance/`. States rules, not implementation.
- **ADR (Architecture Decision Record)**: a record of one specific, dated decision made by one
  module or the platform as a whole, living in `docs/adr/`. States what was decided and why, for one
  decision.
- **Module Documentation**: documentation describing a specific system's current concrete shape
  (e.g. `docs/AI/Architecture.md`, `docs/AI/VisionPipeline.md`), living alongside the module it
  describes. States how a system works today.

## Principles

1. Each of the three layers (VIG, ADR, Module Documentation) is authoritative for exactly one
   altitude of information: principle, decision, or current system shape, respectively.
2. No layer duplicates another layer's content. A VIG document does not describe how a specific
   module implements a principle; an ADR does not restate a principle already stated in a VIG
   document; module documentation does not re-litigate a decision already recorded in an ADR.
3. Every layer cross-references the layers above and below it, so a reader can move from principle
   to decision to implementation (or back) without searching.
4. A document is written once and updated in place as its subject changes; a new document is created
   only for a genuinely new principle, decision, or module — never as a duplicate covering the same
   ground from a different angle.
5. Documentation explains *why*, not only *what*. A document that only restates what code already
   makes obvious is not adding value and should not exist.

## Rules

- Before writing a new document, check whether an existing VIG, ADR, or module document already
  covers the same ground; extend or amend it rather than creating a parallel one.
- A VIG document may not contain file paths, class names, or language-specific implementation
  detail — that belongs in module documentation.
- An ADR's "Related Standards"/"Notes" section should cite the VIG principle(s) its decision
  satisfies, once such principles exist.
- Module documentation's introduction should note which ADR(s) established the system it describes,
  and, once established, which VIG principle(s) that system implements.

## Examples

- `docs/AI/VisionPipeline.md` describes concretely how `TBK_IMAGE_ID` is computed today
  (`compute_image_id()`, SHA-256, `pipeline.py`); `VIG-006-Identifier-Standard.md` states the
  platform-wide rule that every entity gets a permanent identifier, with no file or function names.
  Correct — one altitude each.
- ADR 0004 records the specific decision to introduce `TBK_IMAGE_ID` and package structure changes,
  dated and scoped to that moment; it does not restate the general identifier principle at length,
  only cites it. Correct.

## Non-examples

- A new VIG document is created that mostly repeats content already in `docs/AI/Architecture.md`,
  just phrased more abstractly. Violates Principle 2 and 4 — it should have cited the existing
  document instead of duplicating it.
- An ADR includes a multi-paragraph restatement of a platform-wide principle instead of a one-line
  citation to the VIG document that already states it. Violates Principle 2.

## Implementation Guidance

When starting a new document, first identify its altitude (principle / decision / current system)
and confirm no existing document at that altitude already covers the same subject. If one does,
edit it. If none does, write the new document at the correct altitude only, and add cross-references
to the adjacent layers.

## Future Compatibility

This three-layer model does not assume any particular tooling (a wiki, a static site, plain
Markdown) — it is a content-organization principle, applicable regardless of how documents are
rendered or hosted.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. |

## Related Standards

VIG-000 (Constitution — the document this whole series' layering exists to protect from
duplication), VIG-009 (ADR Standard — the decision-layer format this document assumes).

## References

- `CLAUDE.md` — "One decision, one document. The Jul-19 NAP cluster is five files for one decision;
  don't repeat it." — the existing repo principle this document formalizes and extends across all
  three documentation layers, not just ADRs.
- `docs/AI/Architecture.md`, `docs/AI/FolderStructure.md`, `docs/AI/VisionPipeline.md`,
  `docs/AI/Configuration.md`, `docs/AI/Roadmap.md` — the existing example of the "Module
  Documentation" layer this standard describes.
