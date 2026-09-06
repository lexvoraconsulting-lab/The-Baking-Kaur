<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/decisions-dark.svg">
  <img alt="Decisions" src="../../skills/ThemeStyleOps/assets/banners/lexvora/decisions-light.svg" width="100%">
</picture>

# DEC_20260906_D — Atelier Console Menu Luxury Typography & Interactive UI Rebuild

> **Date:** 2026-09-06 · **Status:** Accepted · **Scope:** Developer Experience & CLI Toolchain
> **Related Architecture:** [`ARC_20260906_E`](../architecture/ARC_20260906_E_developer_toolchain_and_operations_console.md)
> **Fed Plan:** [`MENU`](../plans/02-operations/PLN007-atelier-console-menu-luxury-typography-interactive-ui-rebuild-plan.md)

---

## Context

The Baking Kaur atelier console menu previously utilized a single-line ASCII header inside a 76-column box. While functional, it lacked the grandeur, high-fashion luxury identity, and typographic scale appropriate for an elite patisserie studio. Furthermore, operator ergonomics required a more expansive canvas, clear two-column system telemetry with real-time status badges, and prominent, intuitive domain segmentation.

## Decision

1. **5x Multi-Row Sculpted ASCII Typography for `BAKING`:**
   - Implement a 5-row tall sculpted Unicode block-character font for **`BAKING`** flanked by elegant ivory flourish lines (`✦ T H E ✦` and `✧ K A U R ✧`).
   - Render the title using a TrueColor chromatic gradient transitioning from Shimmer Gold (`#F3E5AB`) down through Velvet Rose (`#C01457`) to Deep Wine (`#7A2147`).
2. **Terminal Canvas Expansion & Launcher Dimensioning:**
   - Expand the active console width from 76 to 94 columns to accommodate the 5x typography and dual-column telemetry without line clipping or wrapping.
   - Configure launcher scripts (`tbk-menu.bat`, `tools-script/win/tbk-menu.bat`, `tbk-menu.ps1`) to automatically configure console dimensions (`mode con: cols=94 lines=44`) and UTF-8 code page (`chcp 65001`).
3. **Intuitive 2-Column Telemetry & Domain Action Cards:**
   - Transform system telemetry into a structured 2-column dashboard reporting Store Domain, Active Theme, Live Theme, Python Framework, Node Toolchain, and Session Log pointer with colored status badges (`● ONLINE`, `● CONNECTED`, `● VERIFIED`).
   - Group operational commands into 6 distinct, color-coded domain cards:
     - `🌸 01 · STOREFRONT & THEME STUDIO`
     - `🏛 02 · PROJECTOPS GOVERNANCE & PDM`
     - `⚡ 03 · STORE AUTOMATION & SEO ENGINE`
     - `🧬 04 · AI CAKE GENOME & VISION PIPELINE`
     - `📦 05 · BUILD & RELEASE MANAGEMENT`
     - `📊 06 · SYSTEM OBSERVABILITY & CONTROL`
4. **Ergonomic Operator Controls:**
   - Provide direct numeric hotkeys (`1`-`13`) and mnemonic shortcuts (`H`elp, `R`efresh, `L`ogs, `C`lear, `Q`uit).

## Consequences

- The interactive console provides a world-class luxury atelier developer experience.
- The 94-column standard provides clean layout alignment and visual breathing room.
- Clear domain segmentation eliminates operator cognitive load during daily storefront, AI vision, and governance tasks.

## Footer

Parent: [`decisions-master.md`](./decisions-master.md) ·
Architecture: [`../architecture/architecture-master.md`](../architecture/architecture-master.md) ·
Plans: [`../plans/plans-master.md`](../plans/plans-master.md)
