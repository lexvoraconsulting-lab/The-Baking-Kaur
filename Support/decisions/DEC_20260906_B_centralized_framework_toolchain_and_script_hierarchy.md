<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/decisions-dark.svg">
  <img alt="Decisions" src="../../skills/ThemeStyleOps/assets/banners/lexvora/decisions-light.svg" width="100%">
</picture>

# DEC_20260906_B — Centralized Framework Toolchain (`ENV_FRM_01`), Domain-Categorized Script Layout & Terminal UX

> **Date:** 2026-09-06 · **Status:** Accepted · **Scope:** Toolchain Architecture & Developer Operations
> **Related Concepts:** [`CON005`](../concept-design/CON005_Unified_Developer_Toolchain_Master_Console_Concept.md)
> **Related Research:** [`RSH_20260906_D`](../research/RSH_20260906_D_developer_toolchain_centralized_runtime_and_console_ux.md)
> **Related Architecture:** [`ARC_20260906_E`](../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md)
> **Fed Plan:** [`TOOL`](../plans/02-operations/PLN005-developer-toolchain-and-master-operations-console-plan.md)

---

## Context

Development on **The Baking Kaur** spans multiple domains: Shopify Online Store 2.0 Liquid & JSON theme templates, PyTorch/Torchvision AI Cake Genome pipelines, Shopify Admin GraphQL SEO automations, and ProjectOps v2 repository governance.

Previously, automation scripts were scattered across flat folders or risk-prone virtual environments. Stale theme IDs caused local development server startup failures, and unformatted console outputs hindered developer ergonomics.

## Decision

1. **Central Framework Invariant (`ENV_FRM_01`):**
   - Mandate that all language runtimes, interpreters, and framework installations reside strictly in `F:\frameworks\` (specifically `F:\frameworks\Python314\python.exe`).
   - Forbid creating scattered virtual environments (`.venv/`, `env/`) in the repository root or subfolders. All deep learning and automation libraries (PyTorch, torchvision, transformers, requests, pytest, PIL) reside centrally.
   - Enforce this via agent instructions in project root [`AGENTS.md`](../../AGENTS.md) and [`GEMINI.md`](../../GEMINI.md).
2. **Three-Tier Domain-Categorized Script Hierarchy:**
   - Partition `tools-script/` into `win/`, `python/`, and `mac/`.
   - Organize all scripts inside these directories into dedicated domain subdirectories: `theme/`, `governance/`, `seo/`, `ai/`, `release/`, `tests/`, and `cli/`.
3. **Resilient Theme Dev Server Resolver:**
   - Deprecate hardcoded stale theme IDs.
   - Build [`tools-script/python/theme/theme_dev_server.py`](../../tools-script/python/theme/theme_dev_server.py) with dynamic Shopify CLI store theme discovery, automatic fallback to active unpublished preview theme `#152070258857`, auto-pull download on empty local folders, and port collision detection.
4. **Artisanal Luxury Console Experience:**
   - Build [`tools-script/python/cli/tbk_cli.py`](../../tools-script/python/cli/tbk_cli.py) with double-line Unicode box frames, TrueColor ANSI styling (Atelier Rose, Champagne Gold), live status cards, noise-suppressed command execution, and session logging into `logs/sessions/`.

## Consequences

- **Guaranteed Environment Reproducibility:** Zero drift across machines, agents, or subprocess runners; all packages resolve from `F:\frameworks\Python314`.
- **Zero Startup Breakage:** If a preview theme is deleted on Shopify, the server detects it and smoothly recovers rather than aborting.
- **Auditable History:** Every execution across theme deploy, audit, SEO ops, and releases is permanently recorded in `logs/sessions/`.
- **Path Traversal Depth:** Moving scripts into domain subdirectories shifts relative path depth from `%~dp0\..\..` to `%~dp0\..\..\..`, which is codified and enforced across all batch and shell runners.

## Footer

Parent: [`decisions-master.md`](./decisions-master.md) ·
Architecture: [`../architecture/architecture-master.md`](../architecture/architecture-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
