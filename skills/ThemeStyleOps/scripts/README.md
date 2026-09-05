# Documentation Visual Theme — Scripts & Automation

This directory contains the automated generation and validation utilities for the `ThemeStyleOps` skill.

![Theme Generator Pipeline](../assets/theme_generator_pipeline.svg)

---

## Purpose

Theme assets (area banners, status badge chips, and governance vector graphics) must remain synchronized across both supported visual profiles (`lexvora-company` and `macos-tahoe-liquid-glass`). 

To avoid manual drawing discrepancies, broken links, or XML syntax errors, all canonical assets are generated deterministically via the Python scripts in this folder.

---

## Scripts

### 1. `generate_theme_assets.py`
Generates the complete set of status chips, priority badges, record-type markers, and light/dark `<picture>` area banners for both theme profiles.

- **Outputs**:
  - `../assets/badges/lexvora/*.svg` (46 badge chips)
  - `../assets/badges/tahoe/*.svg` (46 badge chips)
  - `../assets/banners/lexvora/*-{light,dark}.svg` (8 area banners)
  - `../assets/banners/tahoe/*-{light,dark}.svg` (8 area banners)
- **Execution**:
  ```bash
  python3 skills/ThemeStyleOps/scripts/generate_theme_assets.py
  ```

### 2. `generate_governance_visuals.py`
Automates the generation and XML validation of repository governance diagrams:
- **Architecture Diagrams**: Master component flow, toolchain stack, and repository dependency topologies.
- **Decision Diagrams**: Migration flows, gap record standards (`DEC_20260901_A`), theme tokens (`DEC_20260901_B`), and v2 upgrade architecture (`DEC_20260901_C`).
- **Concept Diagrams**: Baseline architecture (`CON001`) and dogfooding loop diagrams.
- **Self-Governance Gaps**: Migration and conformance visual records.
- **Execution**:
  ```bash
  python3 skills/ThemeStyleOps/scripts/generate_governance_visuals.py
  ```

---

## Rule of Asset Modification

> [!IMPORTANT]
> **Never hand-edit generated SVGs in `assets/badges/` or `assets/banners/`.**  
> Modify the token definitions or geometry templates in `generate_theme_assets.py` or `generate_governance_visuals.py` and re-run the script so that both theme profiles remain in 100% mechanical synchronization.

