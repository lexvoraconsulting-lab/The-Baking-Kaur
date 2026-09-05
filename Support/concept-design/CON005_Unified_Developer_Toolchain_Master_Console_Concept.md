<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-dark.svg">
  <img alt="Concept Design" src="../../skills/ThemeStyleOps/assets/banners/lexvora/concept-design-light.svg" width="100%">
</picture>

# Concept — Unified Developer Toolchain & Master Operations Console (`CON005`)

> **Parent:** [`concept-design-master.md`](./concept-design-master.md) · **Status:** `Planned` · **Date:** 2026-09-06
> **Cross-cut:** none
> **Decision:** [`DEC_20260906_B`](../decisions/DEC_20260906_B_centralized_framework_toolchain_and_script_hierarchy.md) · **Fed Plan:** [`TOOL`](../plans/02-operations/PLN005-developer-toolchain-and-master-operations-console-plan.md)

---

## 1. Problem

Development workflows across storefront theme engineering, AI Vision pipeline execution, SEO snippet automation, and ProjectOps governance previously suffered from fragmentation:
1. **Scattered Runtimes:** Language interpreters and dependencies risked fragmentation across multiple scattered virtual environments, violating deterministic execution guarantees.
2. **Brittle Remote Theme Connections:** Hardcoded theme IDs (e.g. stale `#151370334377`) caused dev server crashes when remote themes were deleted or updated on Shopify.
3. **Flat Directory Sprawl:** Automation scripts across Windows, Mac, and Python were intermixed in flat directories without clear domain boundaries.
4. **Subprocess Noise & Ergonomics:** Developers and non-technical operators were confronted with raw console output dumps without structured progress, clear visual cues, or persistent session logs.

## 2. Concept

Deliver a unified, high-ergonomics developer operations hub for **The Baking Kaur** governed by four architectural pillars:
- **Centralized Framework Toolchain (`ENV_FRM_01`):** All runtime interpreters (Python 3.14, PyTorch, Torchvision, Transformers, Requests, Pytest) reside strictly in `F:\frameworks\Python314` with zero scattered virtual environments.
- **Domain-Categorized Script Taxonomy:** Scripts are systematically subdivided by operating system (`win/`, `python/`, `mac/`) and partitioned into domain modules (`theme/`, `governance/`, `seo/`, `ai/`, `release/`, `tests/`, `cli/`).
- **Intelligent Dev Server Controller:** A resilient runtime orchestrator that dynamically inspects Shopify remote themes, falls back to active preview theme `#152070258857`, auto-downloads theme code on empty directories, and gracefully resolves local TCP port conflicts.
- **Executive Luxury Console Experience:** An interactive Master Operations Hub CLI (`tbk-menu.bat` / `tbk_cli.py`) styled in The Baking Kaur's luxury atelier aesthetic (double-line Unicode box frames, TrueColor palette, live status pill, noise suppression, and timestamped session logging).

## 3. Ideas Backlog

| S.No. | Idea | Notes |
| ---: | --- | --- |
| 1 | Central Framework Resolver | Automated pre-flight check in all `.bat`/`.ps1`/`.sh` scripts resolving `F:\frameworks\Python314\python.exe`. |
| 2 | Auto-Pull Theme Recovery | Dev server controller automatically executes `shopify theme pull` when local theme directory is absent or empty. |
| 3 | Port Collision Relocation | Dev server checks port 9292 availability; if occupied, automatically increments to 9293..9299. |
| 4 | Artisanal Console UI | Rich luxury styling with Unicode double borders, Atelier Rose/Champagne Gold highlights, and live status pill. |
| 5 | Session-Isolated Logging | Stdout/stderr cleanly captured and routed to `logs/sessions/session_<timestamp>.log` with latest symlink. |

## 4. Scope

- **In Scope:** `tools-script/` directory structure, `tbk_cli.py`, `theme_dev_server.py`, batch/shell launchers, and session logging infrastructure.
- **Out of Scope:** Storefront runtime Liquid code, protected product page (`templates/product.json`), and Shopify Admin GraphQL schema contracts.

## 5. Open Questions

1. Should the dev server support multi-theme parallel development on distinct local ports? (Handled via `--port` parameter).
2. Can console TrueColor escape sequences gracefully degrade on legacy Windows conhost consoles? (Handled via ANSI fallback).

## 6. Promotion Path

`CON005` -> Decision [`DEC_20260906_B`](../decisions/DEC_20260906_B_centralized_framework_toolchain_and_script_hierarchy.md) -> Architecture [`ARC_20260906_E`](../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md) -> Plan [`PLN005`](../plans/02-operations/PLN005-developer-toolchain-and-master-operations-console-plan.md).

## Footer

Parent: [`concept-design-master.md`](./concept-design-master.md) ·
Decisions: [`../decisions/decisions-master.md`](../decisions/decisions-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
