# Plan — Developer Toolchain & Master Operations Console (`TOOL`)

> **Parent:** [`../plans-master.md`](../plans-master.md) · **Code:** `TOOL`
> **Status:** Active · **Owner:** Tooling & Platform Architecture Team

## Sources and Traceability

| S.No. | Code | Source record | Plan role | Status |
| ---: | --- | --- | --- | --- |
| 1 | `RUL` | [`../../rules.md`](../../rules.md) | Binding runtime constraints (ENV_FRM_01, TOOL-001) | Current |
| 2 | `CON` | [`../../concept-design/CON005_Unified_Developer_Toolchain_Master_Console_Concept.md`](../../concept-design/CON005_Unified_Developer_Toolchain_Master_Console_Concept.md) | Developer toolchain & master console specification | Current |
| 3 | `RSH` | [`../../research/RSH_20260906_D_developer_toolchain_centralized_runtime_and_console_ux.md`](../../research/RSH_20260906_D_developer_toolchain_centralized_runtime_and_console_ux.md) | Runtime isolation & terminal ergonomics research | Current |
| 4 | `ARC` | [`../../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md`](../../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md) | Three-tier categorized architecture specification | Current |
| 5 | `DEC` | [`../../decisions/DEC_20260906_B_centralized_framework_toolchain_and_script_hierarchy.md`](../../decisions/DEC_20260906_B_centralized_framework_toolchain_and_script_hierarchy.md) | Architectural decision record for toolchain hierarchy | Current |

## Statistics

`TL = PD + IP + CD`. From task markers below.

| S.No. | Plan Scope | TL | PD | IP | CD |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `TOOL` direct tasks | 8 | 0 | 0 | 8 |
| 2 | Total | **8** | **0** | **0** | **8** |

## Context

Deliver a unified, cross-platform developer toolchain and Master Operations Console CLI for The Baking Kaur, centralizing all Python execution in `F:\frameworks\Python314\python.exe` (`ENV_FRM_01`), organizing scripts into functional domain subdirectories (`theme/`, `governance/`, `seo/`, `ai/`, `release/`, `tests/`, `cli/`), resolving remote Shopify themes dynamically with automatic preview theme fallback, and providing an executive luxury terminal UI.

## 01. Developer Toolchain & Console Tasks

- [x] `TOOL-01.01` Codify Concept `CON005` and Research `RSH_20260906_D` for developer operations toolchain.
- [x] `TOOL-01.02` Codify Architecture `ARC_20260906_E` and Decision `DEC_20260906_B` for centralized runtime isolation.
- [x] `TOOL-01.03` Codify `ENV_FRM_01` and Rule Section 8 (`TOOL-001`) in `Support/rules.md` and repository agent rules.
- [x] `TOOL-01.04` Implement intelligent theme dev server controller with auto-download and stale theme recovery.
- [x] `TOOL-01.05` Reorganize `tools-script/` into three-tier domain-categorized layout across `win/`, `python/`, and `mac/`.
- [x] `TOOL-01.06` Redesign Master Operations Console CLI with luxury artisanal aesthetic, box frames, and live status card.
- [x] `TOOL-01.07` Synchronize path depth traversal (`..\..\..`) and documentation across all scripts and READMEs.
- [x] `TOOL-01.08` Execute full test suite (233 pytest), AI Vision tests (45 tests), and PDM conformance audit.

## Footer Navigation

Parent: [`../plans-master.md`](../plans-master.md) · Plans Master: [`../plans-master.md`](../plans-master.md)
