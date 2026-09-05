<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/research-dark.svg">
  <img alt="Research" src="../../skills/ThemeStyleOps/assets/banners/lexvora/research-light.svg" width="100%">
</picture>

# Research — Developer Toolchain Architecture, Centralized Runtime Isolation & Console Visual Ergonomics (`RSH_20260906_D`)

> **Parent:** [`research-master.md`](./research-master.md) · **Status:** `Exploring` · **Date:** 2026-09-06
> **From concept:** [`CON005`](../concept-design/CON005_Unified_Developer_Toolchain_Master_Console_Concept.md)

---

## Question

How can we engineer a cross-platform (Windows batch/PowerShell and macOS/Linux bash) developer toolchain that guarantees deterministic execution across 90+ deep learning and store automation packages, eliminates broken remote theme links during local dev server startup, and delivers an executive luxury console aesthetic on Windows terminals?

## Current Baseline

1. **Scattered Tooling Paths:** Previously, `.bat` and `.ps1` files hardcoded relative path depths (`..\..`) assuming a flat folder hierarchy. Introducing categorized subdirectories (`theme/`, `governance/`, `seo/`, `ai/`, `release/`, `tests/`, `cli/`) shifts traversal depth to `..\..\..`.
2. **Terminal Rendering Variability:** Windows CMD (`conhost.exe`) defaults to code page 437/1252 unless explicitly configured with `chcp 65001`, leading to corrupted Unicode characters (`Γûê`, `?`) when printing box-drawing borders and emojis.
3. **Shopify CLI Connection Failures:** When launching local theme dev servers against deleted remote themes (`#151370334377`), the CLI aborts with unhandled errors. If local theme assets are missing, `shopify theme dev` renders a blank storefront.

## Findings

1. **Central Framework Resolution (`ENV_FRM_01`):**
   - Resolving strictly to `F:\frameworks\Python314\python.exe` ensures identical module resolution across standalone terminal prompts, background agent subtasks, and automated batch runs.
   - Injecting `PYTHONPATH` dynamically (`%CD%;%CD%\tbk-spfy-ai;%CD%\tbk-spfy-seo\ops`) guarantees cross-module imports succeed without polluting the global environment.
2. **Windows Terminal & Code Page 65001:**
   - Pre-pending `@chcp 65001 >nul` in batch launchers and invoking `sys.stdout.reconfigure(encoding="utf-8")` in Python unlocks full Unicode box-drawing (`╔═╗`, `║ ║`, `╚═╝`) and TrueColor ANSI rendering across Windows Terminal, VSCode conpty, and modern conhost.
3. **Dynamic Remote Theme Discovery & Recovery:**
   - Inspecting `shopify theme list` before starting allows automatic detection of the active unpublished preview theme (`#152070258857`), preventing crashes caused by stale hardcoded IDs.
   - Performing an automated `shopify theme pull` on empty local directories (`tbk-spfy-theme/`) guarantees immediate functional development.
4. **Subprocess Noise Suppression & Session Streaming:**
   - Wrapping long-running tools (e.g. `pytest`, `pdm audit`, `shopify theme dev`) in a Python supervisor with clean step indicators (`⏳` -> `✔`) suppresses verbose raw console dumps while preserving complete debug transcripts in `logs/sessions/session_<timestamp>.log`.

## Open Questions

1. How should background file synchronization (`theme dev`) handle network drops gracefully without breaking the interactive menu loop? (Handled via graceful keyboard interrupt capture).

## Proposed Promotion

Feeds Decision [`DEC_20260906_B`](../decisions/DEC_20260906_B_centralized_framework_toolchain_and_script_hierarchy.md), Architecture [`ARC_20260906_E`](../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md), and Plan [`PLN005`](../plans/02-operations/PLN005-developer-toolchain-and-master-operations-console-plan.md).

## Footer

Parent: [`research-master.md`](./research-master.md) ·
Concepts: [`../concept-design/concept-design-master.md`](../concept-design/concept-design-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
