# Plan — Central Frameworks Two-Tier Consolidation & Migration (`FRM`)

> **Parent:** [`../plans-master.md`](../plans-master.md) · **Code:** `FRM`
> **Status:** Active · **Owner:** Infrastructure & Toolchain Team

## Sources and Traceability

| S.No. | Code | Source record | Plan role | Status |
| ---: | --- | --- | --- | --- |
| 1 | `RUL` | [`../../rules.md`](../../rules.md) | Binding runtime constraints (ENV_FRM_01, TOOL-001) | Current |
| 2 | `DEC` | [`../../decisions/DEC_20260906_C_central_frameworks_two_tier_consolidation_and_migration.md`](../../decisions/DEC_20260906_C_central_frameworks_two_tier_consolidation_and_migration.md) | Architectural decision record for two-tier frameworks | Current |
| 3 | `ARC` | [`../../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md`](../../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md) | Central framework runtime architecture | Current |

## Statistics

`TL = PD + IP + CD`. From task markers below.

| S.No. | Plan Scope | TL | PD | IP | CD |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `FRM` direct tasks | 13 | 0 | 0 | 13 |
| 2 | Total | **13** | **0** | **0** | **13** |

## Context

Consolidate all developer frameworks and dependencies from the `C:` drive into the two-tier centralized architecture under `F:\frameworks\<framework>\<version>\` (`python\python314`, `nodejs\node-v24`, `nodejs\npm-global`), migrating 1.75 GB of Python dependencies, remapping environment variables, and updating all workspace automation scripts.

## 01. Framework Consolidation Tasks

- [x] `FRM-01.01` Author Decision `DEC_20260906_C` and update `Support/rules.md` § 7 (`ENV_FRM_01`).
- [x] `FRM-01.02` Relocate Python 3.14 base installation into `F:\frameworks\python\python314\`.
- [x] `FRM-01.03` Migrate 1.75 GB site-packages (197 packages) and scripts into `F:\frameworks\python\python314\Lib\site-packages\` and `Scripts\`.
- [x] `FRM-01.04` Migrate Node.js v24 runtime to `F:\frameworks\nodejs\node-v24\`.
- [x] `FRM-01.05` Migrate npm global tools & Shopify CLI to `F:\frameworks\nodejs\npm-global\` and configure npm prefix/cache.
- [x] `FRM-01.06` Update all workspace batch scripts, PowerShell runners, and CLI hub (`tbk_cli.py`) to target new `F:\frameworks` paths.
- [x] `FRM-01.07` Execute full test suite (233 pytest), AI Vision tests (45 tests), and verify isolated `-s` loading.
- [x] `FRM-01.08` Run PDM conformance audit (`pdm audit Support`) and close worklog with `pdm checkpoint`.

## 02. Centralized Git Toolchain & Dependencies Tasks

- [x] `FRM-02.01` Repair corrupted 0-byte `.git/index` and verify remote push to origin.
- [x] `FRM-02.02` Install/Relocate Git for Windows into `F:\frameworks\git\git-v254\`.
- [x] `FRM-02.03` Configure User PATH to resolve `F:\frameworks\git\git-v254\cmd` as primary Git binary.
- [x] `FRM-02.04` Verify internet package installation capability across Python (PyPI) and Node (npm) on `F:\frameworks\`.
- [x] `FRM-02.05` Run full test suite (233 pytest), PDM audit (`pdm audit Support`), and close worklog batch.

## Footer Navigation

Parent: [`../plans-master.md`](../plans-master.md) · Plans Master: [`../plans-master.md`](../plans-master.md)
