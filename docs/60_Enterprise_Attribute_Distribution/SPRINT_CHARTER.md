# BUILD-004 Sprint Charter — Enterprise Attribute Distribution

Workstream: **ATTR** — per [ADR 0006](../adr/2026-07-27-workstream-id-convention.md).
Status: **in progress** — BL-0 and BL-1 done and committed; BL-2 in planning (not yet implemented).

This is the persisted, canonical copy of the Sprint Charter presented and approved before
implementation began. Update the **Backlog Items** status column as each item completes — this
file is the live source of truth for "where is Build-004 right now," not a point-in-time snapshot.

## Sprint Goal

Implement the Enterprise Attribute Distribution engine: the write path that takes a validated
`EALAttributeRecord`, resolved by its EAR entry and enriched by its EAD Definition's mapping
guidance, and produces a correct, reviewable write to Shopify (and, where possible, ERP) — provably
correct via a round-trip test, without ever writing to the live production Shopify store or a real
ERP endpoint during this sprint.

## Backlog Items

| Item | Description | Status | Commit |
|---|---|---|---|
| BL-0 | Naming correction (ADR 0006) | **Done** | `02dd93d` |
| BL-1 | `ai/attribute_distribution/` package skeleton — `DistributionRecord` model | **Done** | `ce31d79` |
| BL-2 | Mapping resolution — EAL+EAR+EAD → concrete write payload, with R-9 verification gating | **Planning** (implementation plan under review, not yet coded) | — |
| BL-3 | Conflict detection — EAL value vs. downstream current value (stubbed) | Not started | — |
| BL-4 | Shopify adapter — dry-run only this sprint | Not started | — |
| BL-5 | ERP adapter — fully stubbed | Not started | — |
| BL-6 | Round-trip test — real Build-002/003 example data | Not started | — |
| BL-7 | Full documentation set + `BUILD_004_COMPLETION_REPORT.md` | Not started | — |

(Note: an unplanned but necessary prerequisite — fixing an empty `.venv` and establishing
`requirements.txt`/`DEVELOPMENT_SETUP.md` as canonical — was completed alongside BL-1, commit
`ce31d79`, since BL-1 could not be tested without it.)

## Scope

Building the distribution *engine* and its Shopify/ERP adapters in dry-run/stub mode; proving
correctness end-to-end against real Build-002/003 example data; documenting the result. Workstream:
**ATTR**.

## Out of Scope

- Any live write to the production Shopify store (no `--apply` path this sprint).
- Any real ERP integration (blocked on a first-contact API inspection this environment cannot
  perform).
- Build-005 onward (Enterprise Master Taxonomy, Validation Engine, Knowledge Graph, ...).
- Re-litigating the Build-003 renumbering, the Workstream ID convention, or the Build-005/006/007
  resequencing.
- Modifying `ai/eal/`, `ai/ear/`, or `ai/ead/` code (read-only contracts).

## Risks

- AR-006 (Build-003 review) has not formally closed, though Build-003 is committed — Build-004
  depends on its contract directly.
- TBK Kitchen ERP's real API remains unknown (EPR Risk R-3) — ERP adapter stays a stub.
- Accidental live write to the production Shopify store is the single highest-severity risk this
  sprint — mitigated by dry-run-only scope.
- Conflict-detection logic (BL-3) has no real downstream read to test against yet.

## Technical Dependencies

`ai/eal/` (frozen, `fbe3931`), `ai/ear/` (frozen, `92e6485`), `ai/ead/` (`5c6515c`, AR-006 open),
`docs/CODING_STANDARDS.md`, `docs/20_Attribute_Language/External_ID_Standard.md`. As of BL-1:
`requirements.txt` / `.venv` (`pydantic`, `PyYAML`, `requests`) as the canonical Python environment.

## Architecture Gates

BUILD-004's own substantive gate is **AR-011** (shared with Build-008 Vision Extraction, per
[Enterprise Program Roadmap §09](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md#section-09--architecture-gates)
after the ADR-0007 resequencing) — sought only after all backlog items are individually
implemented, tested, and approved.

## Testing Strategy

Per-backlog-item `test_<module>.py` self-check (no framework, `assert`-based). BL-6 is the
integration proof: a real round-trip using real Build-002/003 example data.

## Rollback Strategy

Every backlog item is its own commit — a bad item reverts with `git revert` on its single commit.
No live write path exists this sprint, so there is no external-system state to roll back.

## Success Criteria

All 8 backlog items (BL-0 through BL-7) implemented, tested (`OK`), documented, and individually
approved; BL-6's round-trip test passes against real example data; zero live writes attempted;
`docs/60_Enterprise_Attribute_Distribution/` cross-reference sweep clean; `ai/eal/`, `ai/ear/`,
`ai/ead/` test suites still pass unchanged after every item.

## Deliverables

- ADR 0006 (naming convention) + wording correction — done.
- `ai/attribute_distribution/` (package, tests, schema, examples) — in progress.
- `docs/60_Enterprise_Attribute_Distribution/` (this charter, README, spec, validation, examples,
  `BUILD_004_COMPLETION_REPORT.md`) — in progress.
- One commit per backlog item, each with its own Summary/Files changed/Tests executed/Risks/ADR
  updates/Recommended next task report.

## Related Standards

[Enterprise Program Roadmap](../30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md)
Section 07 (Build-004), [ADR 0006](../adr/2026-07-27-workstream-id-convention.md),
[README.md](README.md) (module status + field reference).
