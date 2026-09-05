# ADR 0005: Build-003 Renumbering — Enterprise Attribute Definitions

Date: 2026-07-27

## Status

Accepted

## Context

`docs/20_Attribute_Language/Roadmap.md`, committed as part of Build-001, and
`docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md` (reviewed and passed at
AR-005) both defined **Build-003 as "EAD: Enterprise Attribute Distribution"** — the write path
from validated EAL records to Shopify metafields and ERP attribute codes.

The next implementation brief named Build-003 **"Enterprise Attribute Definitions (EAD)"** — the
semantic definition layer over EAR (Build-002) attributes: business definition, purpose, display
name, guidance, mappings, and so on. This is a different responsibility from Distribution, using
the same "EAD" initialism for a different meaning under the same Build number — a genuine
collision, not a rephrasing.

Asked to reconcile, the decision was: **renumber**. Enterprise Attribute Definitions becomes
Build-003; Enterprise Attribute Distribution and every Build after it shift up by one. This is
also, independently, the more consistent outcome: `ai/ear/*.py` and every document under
`docs/40_Enterprise_Attribute_Registry/` already describe "Build-003 (EAD)" as the module
responsible for *business definitions* (e.g. `ai/ear/models.py`: "EAR does not
contain business definitions (Build-003/EAD)... those are Build-003's responsibility") — those
frozen references were already assuming Definitions, not Distribution, before this decision was
made.

## Decision

Renumber every Build from the original Build-003 (Distribution) onward by +1, and insert
Enterprise Attribute Definitions as the new Build-003:

| Old | New | Content |
|---|---|---|
| Build-002 | Build-002 | EAR: Enterprise Attribute Registry — unchanged |
| *(new)* | **Build-003** | **EAD: Enterprise Attribute Definitions** |
| Build-003 | Build-004 | Enterprise Attribute Distribution (see [ADR 0006](2026-07-27-workstream-id-convention.md) — no acronym, to avoid reusing "EAD") |
| Build-004 | Build-005 | Knowledge Graph physical implementation |
| Build-005 | Build-006 | Master Image Taxonomy content (Sprint 2.2) |
| Build-006 | Build-007 | Vision Engine structured extraction (Sprint 2.3) |
| Build-007 | Build-008 | Embeddings + Vector Search |
| Build-008 | Build-009 | ERP + Shopify Distribution at volume |
| Build-009 | Build-010 | JARVIS integration |
| Build-010 | Build-011 | Production Release v1.0 |

Architecture Gates: AR-005 (already passed, reviewing the EPR and Build-002) is not renumbered.
Every AR-00N for N≥6 shifts by +1 to make room for a new **AR-006**, reserved for this Build's own
review:

| Old | New | Reviews |
|---|---|---|
| AR-005 | AR-005 | EPR + Build-002 — **GO**, unchanged |
| *(new)* | **AR-006** | **Build-003, Enterprise Attribute Definitions** |
| AR-006 | AR-007 | Sprint 2.2 taxonomy content (now Build-006) |
| AR-007 | AR-008 | Knowledge Graph storage (now Build-005) |
| AR-008 | AR-009 | Embeddings/Search (now Build-008) |
| AR-009 | AR-010 | Vision Extraction (now Build-007) and/or Attribute Distribution (now Build-004) |
| AR-010+ | AR-011+ | Remaining Builds (now 009, 010, 011) |

Workstreams: WS-04 ("Enterprise Attribute Definitions"), previously folded into WS-03/Build-002 in
the Enterprise Program Roadmap because no separate Build existed for it, is un-folded and given its
own row pointing at the new Build-003.

One non-numeric correction made in the same pass: a shorthand in the Enterprise Program Roadmap
read "Build-003/012" (Section 12 Risk R-3, Section 13), meaning "Build-003 (old Distribution) /
WS-12 (ERP Integration workstream)" — not an Architecture Gate number. Spelled out unambiguously as
"Build-004/WS-12" after the shift.

## Files changed

- `docs/20_Attribute_Language/Roadmap.md` — inserted the new Build-003 section; renumbered the
  original Build-003→004 and Build-004→005 headings. No other content changed.
- `docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md` — full pass across every
  section referencing a Build or AR number (03, 05–15, 17); inserted the new Build-003/AR-006/WS-04
  content per the tables above; un-folded WS-04; fixed the Build-003/012 shorthand; updated the
  status line and Stop Condition with an amendment note.
- `docs/30_Enterprise_Program_Roadmap/EPR_v1_COMPLETION_REPORT.md` — appended an addendum pointing
  here; the original report body is preserved unedited as the dated record of what AR-005 actually
  reviewed.
- This ADR.

## Files deliberately NOT changed

- `ai/eal/`, `ai/ear/` (all code) — frozen implementation contracts, per instruction; not touched.
- `docs/20_Attribute_Language/BUILD_001_COMPLETION_REPORT.md` and
  `docs/40_Enterprise_Attribute_Registry/BUILD_002_COMPLETION_REPORT.md` — historical, point-in-time
  completion reports, not living documents. Their mentions of the pre-renumbering scheme (e.g.
  "Build-003 (EAD distribution)" in the Build-001 report) are accurate records of what was true
  when they were written and are left as-is, the same way this ADR does not rewrite
  `EPR_v1_COMPLETION_REPORT.md`'s original body.
- `docs/40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md` and `Validation.md` — their existing
  "Build-003 (EAD)" mentions already meant Definitions (see Context above) and are correct
  unchanged under the new numbering; no edit needed.

## Consequences

- The "EAD" initialism now means **Enterprise Attribute Definitions** everywhere in the repo,
  consistently, including in documents that already assumed this before the decision was formally
  made.
- Every future Build reference in newly-authored documents must use the table above, not the
  original brief's numbering.
- A reader consulting `EPR_v1_COMPLETION_REPORT.md`'s original body alongside the current
  `Enterprise_Program_Roadmap_v1.md` will see different Build-003 definitions for the two AR-005
  scope items — the addendum in that report and this ADR are the explicit bridge between them.

## Notes

Satisfies [VIG-009 (ADR Standard)](../00_Governance/VIG-009-ADR-Standard.md)'s one-decision-one-
document rule and [VIG-000 (Constitution)](../00_Governance/VIG-000-Constitution.md)'s amendment
process (in-place correction with a recorded rationale, not a silent rewrite of history).
