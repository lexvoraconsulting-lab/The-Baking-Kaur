#!/usr/bin/env python3
"""
The Baking Kaur — Centralized Theme Manager and Pre-Flight Resilience
Provides proactive theme directory validation, automatic directory scaffolding,
and self-healing synchronization/downloads from Shopify with zero guesswork.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

if os.name == "nt":
    os.system("")

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

C_RESET   = "\033[0m"
C_BOLD    = "\033[1m"
C_GOLD    = "\033[38;2;212;165;116m"
C_ROSE    = "\033[38;2;192;20;87m"
C_MINT    = "\033[38;2;46;204;113m"
C_SKY     = "\033[38;2;52;152;219m"
C_AMBER   = "\033[38;2;230;126;34m"
C_MUTED   = "\033[38;2;135;135;145m"

STORE_DOMAIN = "ae86ba-2a.myshopify.com"
DEFAULT_THEME_DIR = "tbk-spfy-theme"
CANONICAL_PREVIEW_ID = "152070258857"
CANONICAL_LIVE_ID = "152071602345"

REQUIRED_THEME_SUBDIRS = (
    "assets",
    "config",
    "layout",
    "locales",
    "sections",
    "snippets",
    "templates",
)


def resolve_executable(name: str) -> str:
    """Locate executable path, resolving centralized F:\frameworks first, then PATH."""
    f_npm = Path(r"F:\frameworks\nodejs\npm-global")
    if (f_npm / f"{name}.cmd").exists():
        return str(f_npm / f"{name}.cmd")
    if (f_npm / f"{name}.bat").exists():
        return str(f_npm / f"{name}.bat")
    if (f_npm / name).exists():
        return str(f_npm / name)

    resolved = shutil.which(name)
    if resolved:
        return resolved

    appdata = os.environ.get("APPDATA", "")
    if appdata:
        npm_cmd = Path(appdata) / "npm" / f"{name}.cmd"
        if npm_cmd.exists():
            return str(npm_cmd)

    return name


def check_theme_directory(theme_dir: Path) -> tuple[bool, str, dict]:
    """
    Inspect theme directory health.
    Returns (is_healthy, message, statistics_dict).
    """
    stats = {
        "exists": theme_dir.exists(),
        "is_dir": theme_dir.is_dir() if theme_dir.exists() else False,
        "subdirs_present": [],
        "subdirs_missing": [],
        "file_count": 0,
        "has_layout": False,
        "has_config": False,
    }

    if not stats["exists"]:
        return False, f"Theme directory '{theme_dir.name}' does not exist.", stats

    if not stats["is_dir"]:
        return False, f"Path '{theme_dir.name}' is a file, not a directory.", stats

    for sub in REQUIRED_THEME_SUBDIRS:
        sub_path = theme_dir / sub
        if sub_path.is_dir():
            stats["subdirs_present"].append(sub)
        else:
            stats["subdirs_missing"].append(sub)

    all_files = list(theme_dir.glob("**/*"))
    stats["file_count"] = len([f for f in all_files if f.is_file()])

    stats["has_layout"] = (theme_dir / "layout" / "theme.liquid").is_file()
    stats["has_config"] = (theme_dir / "config" / "settings_schema.json").is_file()

    if stats["file_count"] == 0:
        return False, f"Theme directory '{theme_dir.name}' is empty (0 files).", stats

    if stats["subdirs_missing"]:
        missing_str = ", ".join(stats["subdirs_missing"])
        return False, f"Missing standard theme directories: {missing_str}", stats

    if not stats["has_layout"]:
        return False, "Theme is missing required 'layout/theme.liquid'.", stats

    return True, f"Theme directory is healthy ({stats['file_count']} files verified).", stats


def scaffold_theme_directory(theme_dir: Path) -> bool:
    """Create standard Shopify theme directory structure if missing."""
    try:
        theme_dir.mkdir(parents=True, exist_ok=True)
        for sub in REQUIRED_THEME_SUBDIRS:
            (theme_dir / sub).mkdir(parents=True, exist_ok=True)

        theme_liquid = theme_dir / "layout" / "theme.liquid"
        if not theme_liquid.exists():
            theme_liquid.write_text(
                '<!doctype html>\n<html lang="{{ request.locale.iso_code }}"><head>{{ content_for_header }}</head><body>{{ content_for_layout }}</body></html>\n',
                encoding="utf-8"
            )

        settings_schema = theme_dir / "config" / "settings_schema.json"
        if not settings_schema.exists():
            settings_schema.write_text('[\n  {\n    "name": "theme_info",\n    "theme_name": "The Baking Kaur",\n    "theme_version": "1.0.0"\n  }\n]\n', encoding="utf-8")

        print(f"{C_MINT}✔ Successfully scaffolded standard Shopify theme folders in '{theme_dir.name}/'{C_RESET}")
        return True
    except Exception as ex:
        print(f"{C_AMBER}[ERROR] Failed to scaffold theme directory: {ex}{C_RESET}")
        return False


def pull_theme_from_store(
    store: str = STORE_DOMAIN,
    theme_id: str = CANONICAL_PREVIEW_ID,
    theme_dir: Path | None = None,
    shopify_bin: str | None = None,
    force: bool = False
) -> bool:
    """Pull / download theme files from Shopify store into target directory."""
    if theme_dir is None:
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        theme_dir = repo_root / DEFAULT_THEME_DIR

    theme_dir.mkdir(parents=True, exist_ok=True)
    bin_path = shopify_bin or resolve_executable("shopify")

    print(f"\n{C_SKY}📥 Initiating theme download from Shopify...{C_RESET}")
    print(f"   Store:    {C_BOLD}{store}{C_RESET}")
    print(f"   Theme ID: {C_BOLD}#{theme_id}{C_RESET}")
    print(f"   Target:   {C_BOLD}{theme_dir}{C_RESET}")

    cmd = [
        bin_path, "theme", "pull",
        "--store", store,
        "--theme", str(theme_id),
        "--path", str(theme_dir),
    ]
    if force:
        cmd.append("--force")
    else:
        cmd.append("--nodelete")

    try:
        proc = subprocess.run(cmd, text=True)
        if proc.returncode == 0:
            print(f"\n{C_MINT}✔ Theme download complete from #{theme_id} into '{theme_dir.name}'.{C_RESET}")
            return True
        else:
            print(f"\n{C_AMBER}✖ Shopify CLI returned exit code {proc.returncode} during pull.{C_RESET}")
            return False
    except Exception as ex:
        print(f"\n{C_AMBER}[ERROR] Subprocess error running theme pull: {ex}{C_RESET}")
        return False


def ensure_theme_directory(
    theme_dir: Path | None = None,
    store: str = STORE_DOMAIN,
    theme_id: str = CANONICAL_PREVIEW_ID,
    interactive: bool = True,
    shopify_bin: str | None = None
) -> bool:
    """
    Proactively verify that theme directory exists and is populated.
    If missing or incomplete, presents self-healing options to the operator.
    """
    if theme_dir is None:
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        theme_dir = repo_root / DEFAULT_THEME_DIR

    healthy, reason, stats = check_theme_directory(theme_dir)
    if healthy:
        return True

    # Alert operator of gap
    print(f"\n{C_AMBER}╔════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_AMBER}║  ⚠ THEME DIRECTORY GAP DETECTED [GAP001]                                      ║{C_RESET}")
    print(f"{C_AMBER}╠════════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
    print(f"{C_AMBER}║{C_RESET} Target Path: {C_BOLD}{str(theme_dir):<66}{C_RESET}{C_AMBER}║{C_RESET}")
    print(f"{C_AMBER}║{C_RESET} Status:      {C_ROSE}{reason:<66}{C_RESET}{C_AMBER}║{C_RESET}")
    print(f"{C_AMBER}╚════════════════════════════════════════════════════════════════════════════════╝{C_RESET}")

    if not interactive or not (sys.stdin and sys.stdin.isatty()):
        print(f"{C_MUTED}Non-interactive session detected: auto-scaffolding directory structure...{C_RESET}")
        return scaffold_theme_directory(theme_dir)

    print(f"\n{C_GOLD}{C_BOLD}▶ Self-Healing Options:{C_RESET}")
    print(f"  {C_GOLD}[1]{C_RESET} Download/Pull latest files from Shopify (Theme #{theme_id} on {store}) [Recommended]")
    print(f"  {C_GOLD}[2]{C_RESET} Scaffold empty standard Shopify folders ({', '.join(REQUIRED_THEME_SUBDIRS)})")
    print(f"  {C_MUTED}[0] Cancel operation{C_RESET}")

    try:
        choice = input(f"\n{C_GOLD}Select recovery action [1/2/0, default=1]: {C_RESET}").strip() or "1"
        if choice == "1":
            return pull_theme_from_store(store, theme_id, theme_dir, shopify_bin)
        elif choice == "2":
            return scaffold_theme_directory(theme_dir)
        else:
            print(f"{C_MUTED}Operation cancelled by operator.{C_RESET}")
            return False
    except (KeyboardInterrupt, EOFError):
        print()
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="The Baking Kaur Theme Manager and Pre-Flight Health Validator")
    parser.add_argument("--check", action="store_true", help="Inspect theme directory health")
    parser.add_argument("--pull", action="store_true", help="Pull/download theme from Shopify")
    parser.add_argument("--scaffold", action="store_true", help="Scaffold standard theme folders")
    parser.add_argument("--theme", default=CANONICAL_PREVIEW_ID, help="Shopify Theme ID to target")
    parser.add_argument("--store", default=STORE_DOMAIN, help="Shopify Store Domain")
    parser.add_argument("--path", default=DEFAULT_THEME_DIR, help="Local theme directory name")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    theme_dir = repo_root / args.path

    if args.check:
        healthy, reason, stats = check_theme_directory(theme_dir)
        status_color = C_MINT if healthy else C_AMBER
        print(f"\n{status_color}{C_BOLD}Theme Directory Check:{C_RESET} {reason}")
        print(f"  Path:       {theme_dir}")
        print(f"  Files:      {stats.get('file_count', 0)}")
        print(f"  Subdirs:    {', '.join(stats.get('subdirs_present', []))}")
        sys.exit(0 if healthy else 1)

    elif args.pull:
        success = pull_theme_from_store(args.store, args.theme, theme_dir)
        sys.exit(0 if success else 1)

    elif args.scaffold:
        success = scaffold_theme_directory(theme_dir)
        sys.exit(0 if success else 1)

    else:
        success = ensure_theme_directory(theme_dir, args.store, args.theme, interactive=True)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
