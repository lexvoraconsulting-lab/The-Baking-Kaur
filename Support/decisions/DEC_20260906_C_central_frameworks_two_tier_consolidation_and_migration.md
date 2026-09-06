<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/decisions-dark.svg">
  <img alt="Decisions" src="../../skills/ThemeStyleOps/assets/banners/lexvora/decisions-light.svg" width="100%">
</picture>

# DEC_20260906_C — Central Frameworks Two-Tier Architecture & Multi-Runtime Consolidation

> **Date:** 2026-09-06 · **Status:** Accepted · **Scope:** Framework Toolchain & Runtime Infrastructure
> **Related Architecture:** [`ARC_20260906_E`](../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md)
> **Fed Plan:** [`FRM`](../plans/02-operations/PLN006-central-frameworks-consolidation-and-migration-plan.md)

---

## Context

Audit findings revealed that while base Python was placed on the `F:` drive, all 1.75 GB of Python dependencies (197 packages: PyTorch, Torchvision, Transformers, Pillow, Pytest, Requests, Pydantic) were actually residing on the `C:` drive in `C:\Users\DELL\AppData\Roaming\Python\Python314\site-packages`. Furthermore, Node.js resided in `C:\Program Files\nodejs\` and Shopify CLI / npm global tools resided in `C:\Users\DELL\AppData\Roaming\npm\`.

This violated the architectural requirement of a centralized, isolated frameworks directory on the dedicated `F:` drive.

## Decision

1. **Mandatory Two-Tier Naming Convention:**
   All language runtimes, toolchains, and interpreters under `F:\frameworks\` must strictly follow the two-tier structure:
   ```
   F:\frameworks\<framework-family>\<framework-version>\
   ```
   - Python: `F:\frameworks\python\python314\`
   - Node.js: `F:\frameworks\nodejs\node-v24\`
   - npm Global Tools & Shopify CLI: `F:\frameworks\nodejs\npm-global\`
   - npm Cache: `F:\frameworks\nodejs\npm-cache\`
   - Future Oracle Java: `F:\frameworks\oracle-java\oracle_java10\`
2. **Self-Contained Dependency Isolation:**
   - Migrate all 1.75 GB of site-packages directly into `F:\frameworks\python\python314\Lib\site-packages\`.
   - Set User environment variable `PYTHONUSERBASE=F:\frameworks\python\python314` to prevent Python from writing to `%APPDATA%` on the `C:` drive.
   - Configure npm prefix and cache to `F:\frameworks\nodejs\npm-global\` and `F:\frameworks\nodejs\npm-cache\`.
3. **Tooling & Process Alignment:**
   - Update all repository scripts (`tools-script/win/`, `tbk-menu.bat`, `tbk-menu.ps1`, `tbk_cli.py`) to target `F:\frameworks\python\python314\python.exe`.

## Consequences

- The `C:` drive is completely freed from 1.75+ GB of deep learning, AI, and npm toolchain packages.
- Runtimes are 100% self-contained and reproducible on the `F:` drive.
- Consistent folder naming pattern enables multi-version support (e.g. `python314`, `python312`, `oracle_java10`, `node-v24`) without collision.

## Footer

Parent: [`decisions-master.md`](./decisions-master.md) ·
Architecture: [`../architecture/architecture-master.md`](../architecture/architecture-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
