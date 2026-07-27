# VIG-009: ADR Standard

Status: Active
Version: 1.0

## Purpose

Formalizes how Architecture Decision Records are written and used across the platform, so decision
history stays a single, dated, unambiguous trail rather than being re-argued or duplicated across
scattered documents.

## Scope

Applies to every architecture-affecting decision made by any module or the platform as a whole,
present and future.

## Definitions

- **ADR (Architecture Decision Record)**: a single, dated, immutable-once-accepted record of one
  decision, its context, and its consequences, living in `docs/adr/`.
- **Amendment**: a new ADR that supersedes or extends a previous one, referencing it explicitly,
  rather than editing the original's Decision/Consequences after acceptance.

## Principles

1. One decision, one document. A single ADR records exactly one decision; a decision with multiple
   facets that were genuinely decided together may share one ADR, but a decision unrelated to it
   gets its own.
2. ADRs are immutable once Accepted. A later change of mind produces a new ADR that supersedes the
   old one; the old ADR's content is not rewritten to look as if it always reflected the new
   decision.
3. An ADR records why, not just what — the context that made the decision necessary, and the
   consequences the author expects to follow from it.
4. Every ADR states its status explicitly (Accepted, Superseded, Deprecated) so a reader never has
   to infer whether a decision still holds.
5. An ADR is only necessary for decisions with lasting architectural weight — not every code change
   warrants one; a commit message or module doc update suffices for anything without future decision
   consequences.

## Rules

- ADRs live in `docs/adr/`, filed as `YYYY-MM-DD-short-slug.md`, numbered sequentially in each
  document's title (`ADR 000N: Title`).
- Every ADR contains, at minimum: Status, Context, Decision, Consequences. A Notes section citing
  related VIG principles and prior ADRs is required once such principles or prior decisions exist.
- Superseding a decision requires a new ADR referencing the superseded one by number and explaining
  why; it does not require (and should not involve) editing the superseded ADR's Decision section.

## Examples

- ADR 0003 records the decision to introduce a `VisionProvider` abstraction, with Context (why the
  hardcoded script needed to change), Decision (the interface and factory), and Consequences
  (adding a provider requires one class + one config value). Correct format.
- ADR 0004 responds to a specific review (AR-001) with three related, jointly-decided changes
  (packaging, identity, secrets convention) recorded in one ADR because they were reviewed and
  decided together. Correct application of Principle 1's "genuinely decided together" allowance.

## Non-examples

- A team reopens ADR 0003 and edits its Decision section to reflect a later change of approach,
  with no new ADR marking the supersession. Violates Principle 2.
- Five separate ADRs are filed for what was actually one review's set of related required changes,
  fragmenting one decision across five documents a reader must assemble by hand. Violates Principle
  1 in the opposite direction — over-splitting a single coherent decision.

## Implementation Guidance

Before writing an ADR, ask: will a future engineer need to know *why* this was decided, not just
*what* the code currently does? If the answer is no — if the module documentation (VIG-008) already
captures everything needed — an ADR is not warranted for this change.

## Future Compatibility

This standard does not mandate a specific ADR template beyond the four required sections — teams
may add sections (as this platform's ADRs already do, with "Notes") without violating this standard,
as long as Status/Context/Decision/Consequences remain present.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption, formalizing an ADR practice already in use since ADR 0001. |

## Related Standards

VIG-008 (Documentation Standard — the three-layer model this standard's ADR layer belongs to).

## References

- `CLAUDE.md` — "One decision, one document" — the existing repo principle this standard
  formalizes.
- `docs/adr/2026-07-25-platform-foundation-primitives.md` (ADR 0002), `2026-07-27-vision-provider-
  abstraction.md` (ADR 0003), `2026-07-27-vision-identity-and-packaging.md` (ADR 0004) — the
  existing ADRs whose format this standard codifies.
