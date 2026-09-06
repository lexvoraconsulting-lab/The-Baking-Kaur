# Plan — Atelier Console Menu Luxury Typography & Interactive UI Rebuild (`MENU`)

> **Parent:** [`../plans-master.md`](../plans-master.md) · **Code:** `MENU`
> **Status:** Active · **Owner:** Developer Experience & Infrastructure Team

## Sources and Traceability

| S.No. | Code | Source record | Plan role | Status |
| ---: | --- | --- | --- | --- |
| 1 | `RUL` | [`../../rules.md`](../../rules.md) | Binding constraints (ENV_FRM_01, Rule 2.1, Rule 5.2) | Current |
| 2 | `DEC` | [`../../decisions/DEC_20260906_D_atelier_console_menu_luxury_typography_and_interactive_ui.md`](../../decisions/DEC_20260906_D_atelier_console_menu_luxury_typography_and_interactive_ui.md) | Architectural decision record for 5x typography and 94-column canvas | Current |
| 3 | `ARC` | [`../../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md`](../../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md) | Operations console architecture | Current |
| 4 | `GAP` | [`../../gaps-issues/gap_cluster_active.md`](../../gaps-issues/gap_cluster_active.md) | G_01 Theme Directory Resilience & Pre-Flight Self-Healing Synchronization | Current |

## Statistics

`TL = PD + IP + CD`. From task markers below.

| S.No. | Plan Scope | TL | PD | IP | CD |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `MENU` direct tasks | 15 | 0 | 0 | 15 |
| 2 | Total | **15** | **0** | **0** | **15** |

## Context

Rebuild the developer console menu (`tbk_cli.py`) with a 5x larger sculpted multi-row ASCII art "BAKING" logo, luxury decorative patisserie styling, 94-column expanded canvas, responsive console launcher dimensioning, and an intuitive domain-driven interface. Address operational diagnostics including Shopify CLI argument discrepancies and orphaned global packages. Deliver proactive theme directory validation, automatic directory scaffolding, and self-healing synchronization from Shopify (`GAP001` / `G_01`).

## 01. Console Rebuild Tasks

- [x] `MENU-01.01` Author Decision `DEC_20260906_D` and establish 94-column terminal canvas specification.
- [x] `MENU-01.02` Upgrade Windows `.bat` and PowerShell launchers (`tbk-menu.bat`, `tbk-menu.ps1`, `tools-script/win/`) with auto-dimensioning (`mode con: cols=94 lines=44`).
- [x] `MENU-01.03` Implement 5x multi-row sculpted ASCII typography for `BAKING` with gold-to-rose chromatic gradient and decorative patisserie flourishes in `tbk_cli.py`.
- [x] `MENU-01.04` Rebuild live telemetry into 2-column dashboard with real-time health badges and centralized framework paths.
- [x] `MENU-01.05` Organize operational domain cards (Theme 🌸, Governance 🏛, SEO ⚡, AI Cake Genome 🧬, Release 📦) with intuitive hotkeys and clear visual hierarchy.
- [x] `MENU-01.06` Validate non-interactive rendering with `--test-mode` and verify zero regressions across all 13 dispatch actions.
- [x] `MENU-01.07` Execute full test suite (233 pytest), run PDM conformance audit (`pdm audit Support`), and close worklog.

## 02. Operational Diagnostics & Theme Check Resolution Tasks

- [x] `MENU-02.01` Diagnose 2-hour Shopify CLI theme check syntax error (`shopify theme check tbk-spfy-theme` -> `shopify theme check --path tbk-spfy-theme`).
- [x] `MENU-02.02` Enhance binary resolution in `theme_dev_server.py` to prioritize `F:\frameworks\nodejs\npm-global`.
- [x] `MENU-02.03` Purge orphaned non-framework npm modules from `F:\frameworks\nodejs\npm-global\node_modules\` via robocopy mirror purge.
- [x] `MENU-02.04` Execute regression verification across pytest (233 passed), test-mode CLI rendering, and PDM governance audit (0 errors, 0 warnings).

## 03. Theme Directory Resilience & Self-Healing Tasks

- [x] `MENU-03.01` Create centralized `tools-script/python/theme/theme_manager.py` with directory pre-flight inspection, scaffold automation, and remote theme pull capabilities.
- [x] `MENU-03.02` Integrate pre-flight theme directory verification and self-healing into `theme_dev_server.py`.
- [x] `MENU-03.03` Guard all theme handlers in `tbk_cli.py` with `ensure_theme_directory` and add Option `[ 4 ] Pull / Sync Theme Files`.
- [x] `MENU-03.04` Validate full test suite (233 passed), non-interactive test mode, close `G_01`, and run `pdm audit Support`.

## Footer Navigation

Parent: [`../plans-master.md`](../plans-master.md) · Plans Master: [`../plans-master.md`](../plans-master.md)
