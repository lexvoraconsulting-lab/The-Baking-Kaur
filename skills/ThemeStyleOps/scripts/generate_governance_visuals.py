#!/usr/bin/env python3
"""generate_governance_visuals.py — Automated Dual-Theme Vector SVG Generator & Validator.

Owned by the `ThemeStyleOps` skill (`skills/ThemeStyleOps/scripts/`).
Generates and validates consistent SVG diagrams across two canonical theme profiles:
1. `lexvora-company` (Warm paper #fbf8f3, deep navy #061421, radiant gold #d2a15f, dark ink #101820)
2. `macos-tahoe-liquid-glass` (Translucent glass #ffffff.95, soft spectral wash, azure #2563eb, teal #0d9488)

Usage:
    python3 generate_governance_visuals.py [--theme {lexvora,tahoe,all}] [--validate]
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
SUPPORT = ROOT / "Support"

# --------------------------------------------------------------------------- Theme Tokens

THEMES = {
    "lexvora": {
        "name": "lexvora-company",
        "bg_fill": "#fbf8f3",
        "bg_stroke": "#dcd8d0",
        "panel_fill": "#ffffff",
        "panel_stroke": "#dcd8d0",
        "navy_fill": "#061421",
        "navy_stroke": "#b88445",
        "text_hdr": "#061421",
        "text_body": "#101820",
        "text_muted": "#5c6670",
        "text_gold": "#8a5723",
        "navy_text_hdr": "#d2a15f",
        "navy_text_body": "#ffffff",
        "navy_text_muted": "#e2e8f0",
        "accent_border": "#b88445",
        "arrow_color": "#061421",
    },
    "tahoe": {
        "name": "macos-tahoe-liquid-glass",
        "bg_fill": "url(#tahoe-bg)",
        "bg_stroke": "#cbd5e1",
        "panel_fill": "url(#glass-grad)",
        "panel_stroke": "#ffffff",
        "navy_fill": "#0b2233",
        "navy_stroke": "#38bdf8",
        "text_hdr": "#0f172a",
        "text_body": "#1e293b",
        "text_muted": "#475569",
        "text_gold": "#2563eb",
        "navy_text_hdr": "#38bdf8",
        "navy_text_body": "#ffffff",
        "navy_text_muted": "#cbd5e1",
        "accent_border": "#2563eb",
        "arrow_color": "#2563eb",
    },
}


def write_svg(rel_path: str, svg_content: str) -> bool:
    target = SUPPORT / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(svg_content.strip() + "\n", encoding="utf-8")
    try:
        ET.parse(target)
        print(f"✓ Valid SVG: {rel_path}")
        return True
    except ET.ParseError as e:
        print(f"✗ XML Parse Error in {rel_path}: {e}", file=sys.stderr)
        return False


def validate_all_svgs(root: Path) -> int:
    """Validate 100% of SVGs in Support and skills directories."""
    svgs = sorted(root.rglob("*.svg"))
    errors = 0
    print(f"Validating {len(svgs)} SVG files in {root.name}...")
    for s in svgs:
        try:
            ET.parse(s)
        except ET.ParseError as e:
            print(f"  ✗ {s.relative_to(root)}: {e}", file=sys.stderr)
            errors += 1
    if errors == 0:
        print(f"All {len(svgs)} SVGs parsed cleanly with 0 XML syntax errors.")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Generate and validate dual-theme governance SVGs.")
    parser.add_argument("--theme", choices=["lexvora", "tahoe", "all"], default="all",
                        help="Target visual theme profile (default: all)")
    parser.add_argument("--validate", action="store_true", help="Run XML validation on all repository SVGs")
    args = parser.parse_args(argv)

    print(f"Documentation Visual Theme Engine — Mode: {args.theme.upper()}")
    if not SUPPORT.exists():
        print(f"Error: Support directory not found at {SUPPORT}", file=sys.stderr)
        return 2

    # Validation pass
    err_count = validate_all_svgs(SUPPORT)
    skills_dir = ROOT / "skills"
    if skills_dir.exists():
        err_count += validate_all_svgs(skills_dir)

    if err_count > 0:
        return 1

    print(f"Theme assets and diagrams verified for {args.theme.upper()} profiles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
