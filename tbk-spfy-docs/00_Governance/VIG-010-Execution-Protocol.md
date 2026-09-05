# VIG-010: Execution Protocol

Status: Active
Version: 1.0

## Purpose

Formalizes the per-backlog-item execution workflow and the human-agent stop/resume boundary
already practiced across Build-002, Build-003, and Build-004, so a future engineer or AI agent can
read one document instead of re-deriving the pattern from commit history and conversation logs.

## Scope

Applies to any implementation work on this platform (`ai/*`, `docs/00_Foundation` through
`docs/60_*`, `docs/adr/`) done by a human or an AI agent acting on this repository. Does not apply
to the unrelated Shopify storefront track (`CLAUDE.md`, root `*.md` files) — see FOUNDATION_v1.md
§8 (Repository Structure Overview) for why the two are never merged.

## Definitions

- **Backlog item**: one independently-deliverable unit of a Sprint Charter's backlog (e.g.
  Build-004's `BL-0` through `BL-7`), small enough to implement, test, document, and commit as a
  single unit.
- **Architecture conflict**: a naming collision, duplicate responsibility, circular import, or
  contradiction with a frozen contract, discovered while planning or implementing a backlog item.
- **Build boundary**: the line between the currently-approved Build and the next one — crossing it
  means starting a Build no Sprint Charter has yet been approved for.

## Principles

1. Every backlog item follows the same eight-step cycle: PLAN → IMPLEMENT → TEST → VERIFY → UPDATE
   DOCS → COMMIT → REPORT → WAIT. No step is skipped, and no two items are batched into one cycle.
2. A repository-wide architecture verification (naming-collision grep, circular-import check,
   cross-reference sweep) runs before implementation begins on any item, not after.
3. An architecture conflict found at any step is reported immediately and left for explicit
   resolution — never silently resolved by picking a workaround.
4. Frozen modules (a Build already reviewed and committed) are read-only to every later Build. A
   later Build's tests may exercise a frozen module's real output as fixtures, but its code is never
   modified to accommodate the later Build.
5. No new production dependency is added without first stopping to explain why it's needed — see
   `DEVELOPMENT_SETUP.md` for the concrete instance (the `.venv`/`requirements.txt` case) this
   principle already governs.
6. Quality claims are evidence-based, never fabricated. A scorecard states a checklist of
   verifiable claims with the command or test that proves each one — never an invented numeric
   score. This is `CLAUDE.md`'s "verifiability beats persuasion" principle applied to internal
   reporting, not just external SEO claims.
7. Crossing a Build boundary always requires explicit human approval — an agent operating
   autonomously across many small documentation or cleanup tasks never uses that latitude to start
   the next Build.

## Rules

- Every commit is scoped to exactly one backlog item (or one clearly-bounded documentation pass);
  a bad item reverts with `git revert` on its own commit without touching neighbors.
- Every commit report states: Summary, Files changed, Tests executed, Risks, Rollback, Documentation
  updated, and Recommended next step — matching the pattern already used in every Build-002/003/004
  commit.
- An Architecture Gate (`AR-NNN`) is prepared as a submission package (evidence against the gate's
  own stated approval criteria) but its GO/NO-GO verdict is not self-issued by the agent that did
  the implementation — see `docs/60_Enterprise_Attribute_Distribution/AR011_GATE_PACKAGE.md` for
  the current worked example of this split.
- An autonomous documentation-only pass (no new backlog item, no new Build) may proceed through
  many small fixes without a per-fix approval gate, provided: no production code changes, no
  architecture changes, and no invented work items — every change traces to a real, found
  inconsistency, never a manufactured one.

## Examples

- Build-004's BL-2 through BL-7: each was planned, explicitly approved, implemented, tested,
  documented, and committed as its own commit, with the agent reporting and waiting after every
  single item. Correct application of Principle 1.
- This document itself: found missing during a documentation-consolidation pass, added as one
  self-contained governance document rather than three separate ones (agent operating rules,
  execution protocol, onboarding) that would have fragmented one coherent practice across multiple
  files. Correct application of VIG-009's "one decision, one document" principle extended to
  governance documents generally.

## Non-examples

- An agent, mid-autonomous-pass, decides the repository "is ready" and begins Build-005's Sprint
  Charter without being asked. Violates Principle 7.
- An agent finds a stale mermaid diagram and, while fixing it, also renames an unrelated module or
  adds a new dependency "while it's in there." Violates the documentation-only pass's own scope
  rule under Rules — a documentation pass fixes documentation, not architecture.

## Implementation Guidance

Before starting any backlog item, agents should ask: has this exact process already been described
somewhere I should link to, rather than re-explaining? If yes, cite it (per VIG-008's no-duplication
rule) rather than restate it.

## Future Compatibility

Future Builds may extend this protocol with Build-specific steps (e.g. a security review step for
a Build handling credentials) without violating this standard, as long as the eight-step core cycle
and the Build-boundary approval gate remain intact.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-29 | Initial adoption, formalizing the PLAN→IMPLEMENT→TEST→VERIFY→DOCS→COMMIT→REPORT→WAIT cycle already in use since Build-002. |

## Related Standards

VIG-007 (Quality Standard — the no-fabrication principle this document applies to internal
reporting), VIG-009 (ADR Standard — the one-decision-one-document principle this document's own
existence follows).

## References

- `docs/60_Enterprise_Attribute_Distribution/SPRINT_CHARTER.md` — the fullest worked example of
  this protocol across 8 backlog items.
- `docs/60_Enterprise_Attribute_Distribution/AR011_GATE_PACKAGE.md` — the Architecture Gate
  submission-vs-verdict split (Principle 7's gate half).
- `DEVELOPMENT_SETUP.md` — the dependency-addition stop-and-explain instance (Principle 5).
