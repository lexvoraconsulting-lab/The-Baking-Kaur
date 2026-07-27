# ADR 0007: Build-005 through Build-007 Resequencing

Date: 2026-07-28

## Status

Accepted

## Context

While BUILD-004's Sprint Charter was being executed, the user redefined the roadmap's near-term
sequence: Enterprise Master Taxonomy moved from Build-006 to Build-005, a new standalone Enterprise
Validation Engine was introduced as Build-006 (this workstream previously existed only as WS-07,
folded into other Builds' Architecture Gates, with no Build number of its own), and Knowledge Graph
moved from Build-005 to Build-007. Everything originally numbered Build-007 or higher shifted up by
one more to make room.

This is a numbering change only, per explicit instruction: no Build's scope, objective, or
deliverables changed — Knowledge Graph is still the same physical-storage implementation it always
was, Enterprise Master Taxonomy is still the same Sprint 2.2 content-authoring work, and the new
Enterprise Validation Engine's scope is exactly what WS-07 already specified (wiring EAR's and
EAD's already-documented, already-deferred cross-field validators into runtime enforcement) — not
a newly invented responsibility.

## Decision

Resequence Builds 005 through 011, following the same insertion pattern [ADR 0005](2026-07-27-build-003-renumbering.md)
established for Build-003:

| Old | New | Content |
|---|---|---|
| Build-004 | Build-004 | Enterprise Attribute Distribution — unchanged |
| Build-006 | **Build-005** | Enterprise Master Taxonomy (Sprint 2.2) |
| *(new)* | **Build-006** | **Enterprise Validation Engine** (Workstream: ATTR) — was WS-07, folded into other gates; now its own Build |
| Build-005 | **Build-007** | Enterprise Knowledge Graph (physical implementation) |
| Build-007 | Build-008 | Vision Engine structured extraction (Sprint 2.3) |
| Build-008 | Build-009 | Embeddings + Vector Search |
| Build-009 | Build-010 | ERP + Shopify Distribution at volume |
| Build-010 | Build-011 | JARVIS integration |
| Build-011 | Build-012 | Production Release v1.0 |

Architecture Gates: AR-005 and AR-006 (Build-002, Build-003 — both already closed or in progress)
are unchanged. AR-007 keeps its number (it already meant "review the taxonomy content," and that
content is simply attached to a different Build number now). A new **AR-008** is inserted for the
Validation Engine; every AR-00N for N≥8 (old scheme) shifts by +1:

| Old | New | Reviews |
|---|---|---|
| AR-007 | AR-007 | Enterprise Master Taxonomy (now Build-005) — unchanged number |
| *(new)* | **AR-008** | **Enterprise Validation Engine (Build-006)** |
| AR-008 | AR-009 | Knowledge Graph (now Build-007) |
| AR-009 | AR-010 | Embeddings/Search (now Build-009) |
| AR-010 | AR-011 | Vision Extraction (now Build-008) and/or Attribute Distribution (Build-004) |
| AR-011+ | AR-012+ | Remaining Builds (now 010, 011, 012) |

## Files changed

- `docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md` — full pass: header status,
  Sections 01, 05, 06 (workstream table, including un-folding WS-07's Architecture Review from
  "folded into other gates" to its own AR-008), 07 (rewrote Build-005/006/007 entries; renumbered
  008-012), 08 (all three Mermaid dependency graphs), 09 (gate table, new AR-008 row), 10, 11, 12,
  15, 17 (self-review), Stop Condition.
- `docs/20_Attribute_Language/Roadmap.md` — its own Build-005 (Knowledge Graph) heading renumbered
  to Build-007, with a pointer to this ADR.
- `docs/00_Foundation/FOUNDATION_v1.md` — its Build summary table and two Mermaid diagrams updated
  (this document is explicitly a living index per its own §13, not a dated snapshot).

## Files deliberately NOT changed (preserved as historical record)

- `docs/00_Foundation/PROJECT_MEMORY_2026-07-27.md` — a dated session snapshot. On 2026-07-27,
  Build-005 genuinely was Knowledge Graph; that document accurately records what was true that day
  and is not rewritten to match today's resequencing, the same treatment
  `docs/50_Enterprise_Attribute_Definitions/BUILD_003_COMPLETION_REPORT.md` and
  `docs/adr/2026-07-27-build-003-renumbering.md`'s own historical quotes already received under
  ADR-0005/0006.
- `docs/adr/2026-07-27-build-003-renumbering.md` and `2026-07-27-workstream-id-convention.md` —
  both correctly describe the numbering as it stood on 2026-07-27, before this second resequencing;
  left untouched as accurate history of that decision.
- No code file changes anywhere — this is a documentation-only correction. `ai/eal/`, `ai/ear/`,
  and `ai/ead/` are untouched. BUILD-004's own Sprint Charter and backlog are unaffected — its
  number, workstream (ATTR), and title (Enterprise Attribute Distribution) do not change.

## Consequences

- The Build numbering sequence is now: 001 (EAL) → 002 (EAR) → 003 (EAD Definitions) → 004
  (Attribute Distribution) → 005 (Master Taxonomy) → 006 (Validation Engine) → 007 (Knowledge
  Graph) → 008 (Vision Extraction) → 009 (Embeddings/Search) → 010 (Distribution at volume) → 011
  (JARVIS) → 012 (Production Release).
- Validation Engine (WS-07) now has a dedicated Build and Architecture Gate, closing a gap where it
  previously had no independent review of its own.
- Future roadmap edits must use this table as ground truth. Per the standing principle
  [ADR 0005](2026-07-27-build-003-renumbering.md) already established: Builds 001-004 are never
  renumbered again; this ADR extends that same protection to Builds 005-012 as of this date — any
  further roadmap change inserts new numbers going forward rather than reshuffling this sequence a
  third time.

## Notes

Satisfies [VIG-009 (ADR Standard)](../00_Governance/VIG-009-ADR-Standard.md)'s one-decision-one-
document rule and [VIG-000 (Constitution)](../00_Governance/VIG-000-Constitution.md)'s amendment
process. Applies the Workstream ID convention from
[ADR 0006](2026-07-27-workstream-id-convention.md): the new Build-006 is Workstream **ATTR**,
Title **"Enterprise Validation Engine"** — no acronym.
