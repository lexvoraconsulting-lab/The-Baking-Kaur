# ADR 0006: Workstream ID Convention + Build-004 Relabeling

Date: 2026-07-27

## Status

Accepted

## Context

[ADR 0005](2026-07-27-build-003-renumbering.md) renumbered Build-003 to Enterprise Attribute
Definitions and shifted Enterprise Attribute Distribution to Build-004 — but it only fixed the
*Build number*, not the *label*. Every document written since (the Enterprise Program Roadmap,
`docs/00_Foundation/`, and Build-003's own doc set) continued to call Build-004
**"EAD: Enterprise Attribute Distribution"** or **"EAD Distribution"** — reusing the very
initialism ADR-0005 had just reassigned to Build-003. A repo-wide grep confirmed the ambiguity:
~20 occurrences across 7 files, spanning the Enterprise Program Roadmap, this ADR series, and two
of Build-003's own documents.

This was found while drafting the BUILD-004 Sprint Charter, before any Build-004 code was written,
and flagged per this project's standing rule to stop on discovered architecture conflicts rather
than silently work around them.

## Decision

Introduce three independent naming axes, replacing the single-acronym-per-Build pattern EAL/EAR/
EAD established:

1. **BUILD-xxx** — identifies the implementation increment. Unchanged in meaning or numbering;
   Build-004 stays Build-004. (Notational note: this repository's existing documents write this
   identifier as "Build-004" — title case, hyphenated — not "BUILD-004"; both refer to the same
   identifier. This ADR does not rename or re-case any existing Build reference — doing so would
   touch dozens of already-committed files for no substantive gain. New documents may use either
   casing consistently within themselves.)
2. **Workstream ID** — a short, stable code identifying the *business capability* a Build belongs
   to, independent of Build number. Permanent capability identifiers, extensible on real need
   (never speculatively, VIG-001 Principle 4):

   | Workstream | Capability |
   |---|---|
   | `ATTR` | Enterprise Attributes (EAL/EAR/EAD/Distribution lineage) |
   | `SEO` | Search Engine Optimisation |
   | `GEO` | Generative Engine Optimisation |
   | `AI` | AI Platform |
   | `VIS` | Vision Engine |
   | `CRM` | Customer Relationship Management |
   | `INV` | Inventory |
   | `PROD` | Production |
   | `REC` | Recipe Management |

   This list is illustrative, not exhaustive — a new workstream is added the same way a new
   taxonomy Domain is added elsewhere in this platform: additively, when a real Build needs it.
3. **Title** — human-readable prose, never abbreviated to a 3-4 letter acronym. Build-004's title
   is **"Enterprise Attribute Distribution"** — plain text, no "EAD," "EAX," "ADS," or any other
   initialism.

Retroactive assignment, applied only to the four Builds this decision directly concerns (no other
Build history is touched):

| Build | Workstream | Title |
|---|---|---|
| Build-001 | ATTR | Enterprise Attribute Language |
| Build-002 | ATTR | Enterprise Attribute Registry |
| Build-003 | ATTR | Enterprise Attribute Definitions |
| Build-004 | ATTR | Enterprise Attribute Distribution |

"EAD" now refers **only** to Build-003 (Enterprise Attribute Definitions), everywhere in this
repository, with no exception. Build-004 has no acronym — every reference to it uses "Build-004"
and/or its full title.

## Files changed

Wording-only correction (no factual or technical content changed), replacing "EAD: Enterprise
Attribute Distribution" / "EAD Distribution" with unambiguous "Build-004 (Enterprise Attribute
Distribution)" phrasing:

- `docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md`
- `docs/50_Enterprise_Attribute_Definitions/BUILD_003_COMPLETION_REPORT.md`
- `docs/50_Enterprise_Attribute_Definitions/EAD_SPECIFICATION.md`
- `docs/50_Enterprise_Attribute_Definitions/Mapping_Guide.md`
- `docs/00_Foundation/FOUNDATION_v1.md`
- `docs/00_Foundation/PROJECT_MEMORY_2026-07-27.md`
- `docs/20_Attribute_Language/Roadmap.md`
- `docs/adr/2026-07-27-build-003-renumbering.md` (reworded for clarity; the historical fact that
  Build-003 was *once* labeled this way is preserved, it is simply no longer stated as Build-004's
  current label)

## Files deliberately NOT changed

`docs/40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md` and `Validation.md` — their
"Build-003 (EAD)" mentions already correctly meant Definitions (confirmed by ADR-0005 itself); no
ambiguity existed there and no edit was needed.

No code file changes anywhere — this is a documentation-only correction. `ai/eal/`, `ai/ear/`, and
`ai/ead/` are untouched.

## Consequences

- Every future Build gets a Workstream ID at the time its Sprint Charter is written, preventing
  this exact class of collision (an acronym reused across two Builds) from recurring.
- "EAD" is now permanently and unambiguously Build-003's identifier; Build-004's Python package
  (to be created under BL-1 of the BUILD-004 Sprint Charter) is named descriptively
  (`ai/attribute_distribution/`), not by a new acronym, consistent with the "Titles remain
  human-readable, no acronym" rule above.
- Historical documents (ADR-0005, and any future dated completion report) are worded to state past
  facts accurately without asserting a now-superseded label as current.

## Notes

Satisfies [VIG-009 (ADR Standard)](../00_Governance/VIG-009-ADR-Standard.md)'s one-decision-one-
document rule and [VIG-000 (Constitution)](../00_Governance/VIG-000-Constitution.md)'s amendment
process (in-place correction of already-committed documents, recorded here, not a silent rewrite —
no shipped code or reviewed architecture principle is reversed by this change).
