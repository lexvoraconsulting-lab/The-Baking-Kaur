#!/usr/bin/env python3
"""
The Baking Kaur — Intelligent Theme Development Server Controller
Validates remote theme existence, handles automatic fallback, supports remote theme pull/download,
checks port availability, and launches the Shopify Theme Development Server with rich diagnostics.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

# Enable ANSI colors and UTF-8 encoding on Windows
if os.name == "nt":
    os.system("")

theme_mod_dir = str(Path(__file__).resolve().parent)
if theme_mod_dir not in sys.path:
    sys.path.insert(0, theme_mod_dir)
from theme_manager import ensure_theme_directory, pull_theme_from_store, check_theme_directory

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

STORE_DOMAIN = "ae86ba-2a.myshopify.com"
CANONICAL_PREVIEW_ID = "152070258857"  # TBK Birthday Collection V3 — Pastel Premium
DEFAULT_THEME_DIR = "tbk-spfy-theme"
DEFAULT_PORT = 9292


def resolve_executable(name: str) -> str:
    """Locate executable path, resolving F:\frameworks first, then PATH."""
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
        npm_bat = Path(appdata) / "npm" / f"{name}.bat"
        if npm_bat.exists():
            return str(npm_bat)

    python_dir = Path(sys.executable).parent
    script_tool = python_dir / "Scripts" / f"{name}.exe"
    if script_tool.exists():
        return str(script_tool)

    return name


def is_port_in_use(port: int) -> bool:
    """Check if a local TCP port is already open/in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def fetch_store_themes(store: str, shopify_bin: str) -> list[dict]:
    """Fetch all remote themes from Shopify store as parsed JSON list."""
    try:
        proc = subprocess.run(
            [shopify_bin, "theme", "list", "--store", store, "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=25,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            match = re.search(r"(\[\s*\{.*\}\s*\])", proc.stdout, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return json.loads(proc.stdout.strip())
    except Exception as ex:
        print(f"\033[93m[WARN] Could not retrieve theme list via JSON ({ex}). Falling back to cached catalog.\033[0m")
    return []


def resolve_target_theme(
    requested_id: str | None,
    themes: list[dict],
    interactive: bool = False
) -> tuple[dict | None, list[dict]]:
    """
    Intelligently resolve the target theme.
    If requested_id is found, returns that theme.
    If requested_id is missing or stale (e.g. 151370334377), automatically finds active preview theme.
    """
    theme_map = {str(t.get("id")): t for t in themes if t.get("id")}

    # 1. Direct match
    if requested_id and requested_id in theme_map:
        return theme_map[requested_id], themes

    # 2. Check canonical preview theme
    if CANONICAL_PREVIEW_ID in theme_map:
        canonical_theme = theme_map[CANONICAL_PREVIEW_ID]
        if requested_id and requested_id != CANONICAL_PREVIEW_ID:
            print(f"\n\033[91m✖ Requested Theme ID '{requested_id}' does not exist on {STORE_DOMAIN}.\033[0m")
            print(f"\033[92m✔ Automatically resolved to active preview theme: #{CANONICAL_PREVIEW_ID} ({canonical_theme.get('name')})\033[0m")
        return canonical_theme, themes

    # 3. Find any active unpublished preview theme
    for t in themes:
        if t.get("role") == "unpublished":
            return t, themes

    # 4. Fallback to development theme or live theme
    for t in themes:
        if t.get("role") == "development":
            return t, themes

    if themes:
        return themes[0], themes

    return None, themes


def pull_theme_code(store: str, theme_id: str, theme_dir: Path, shopify_bin: str) -> bool:
    """Download/pull remote theme code to local directory."""
    print(f"\n\033[96m📥 Initiating connection and downloading theme code from Theme #{theme_id}...\033[0m")
    try:
        proc = subprocess.run(
            [
                shopify_bin, "theme", "pull",
                "--store", store,
                "--theme", str(theme_id),
                "--path", str(theme_dir),
                "--nodelete"
            ],
            text=True,
        )
        return proc.returncode == 0
    except Exception as ex:
        print(f"\033[91m[ERROR] Failed to download theme: {ex}\033[0m")
        return False


def start_server(
    theme_id: str | None = None,
    sync_first: bool = False,
    port: int = DEFAULT_PORT,
    auto_open: bool = False,
    allow_interactive: bool = True
) -> int:
    """Main dev server orchestrator."""
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    theme_dir = repo_root / DEFAULT_THEME_DIR
    shopify_bin = resolve_executable("shopify")

    print("\n\033[95m" + "═" * 70 + "\033[0m")
    print("\033[95m  THE BAKING KAUR · INTELLIGENT THEME DEV SERVER\033[0m")
    print("\033[90m  Store: " + STORE_DOMAIN + " | Directory: " + DEFAULT_THEME_DIR + "\033[0m")
    print("\033[95m" + "═" * 70 + "\033[0m")

    # Step 1: Pre-flight theme check
    print("🔍 Checking store theme connectivity...", end="", flush=True)
    themes = fetch_store_themes(STORE_DOMAIN, shopify_bin)
    if themes:
        print(f"\r\033[92m✔ Connected to {STORE_DOMAIN} ({len(themes)} themes discovered)\033[0m")
    else:
        print(f"\r\033[93m⚠ Proceeding with local configuration\033[0m")

    target_theme, all_themes = resolve_target_theme(theme_id or CANONICAL_PREVIEW_ID, themes)
    target_id = str(target_theme.get("id")) if target_theme else CANONICAL_PREVIEW_ID
    target_name = target_theme.get("name", "TBK Birthday Collection V3 — Pastel Premium") if target_theme else "TBK Birthday Collection"
    target_role = target_theme.get("role", "preview") if target_theme else "preview"

    # Step 2: Interactive Menu or Direct Sync
    if allow_interactive and not sync_first and sys.stdin and sys.stdin.isatty():
        print(f"\n\033[96mTarget Theme: #{target_id} — {target_name} [{target_role}]\033[0m")
        print("  \033[93m[1]\033[0m Start dev server immediately (default)")
        print("  \033[93m[2]\033[0m Pull / Download latest files from Shopify before starting")
        print("  \033[93m[3]\033[0m Select a different theme from the store list")
        try:
            choice = input("\033[96mChoose option [1-3, default=1]: \033[0m").strip()
            if choice == "2":
                pull_theme_code(STORE_DOMAIN, target_id, theme_dir, shopify_bin)
            elif choice == "3":
                print(f"\nAvailable themes on {STORE_DOMAIN}:")
                for idx, t in enumerate(all_themes, 1):
                    role_b = f"[{t.get('role', 'unknown')}]"
                    print(f"  {idx:2d}. #{t.get('id')} - {t.get('name')} {role_b}")
                sel = input("\nEnter theme number or ID: ").strip()
                if sel.isdigit():
                    val = int(sel)
                    if 1 <= val <= len(all_themes):
                        target_theme = all_themes[val - 1]
                        target_id = str(target_theme.get("id"))
                        target_name = target_theme.get("name")
                        target_role = target_theme.get("role")
                    elif str(val) in {str(t.get("id")) for t in all_themes}:
                        target_id = str(val)
                        for t in all_themes:
                            if str(t.get("id")) == target_id:
                                target_theme = t
                                target_name = t.get("name")
                                target_role = t.get("role")
                                break
        except (KeyboardInterrupt, EOFError):
            print()

    # Step 3: Proactive theme directory pre-flight & self-healing
    if not ensure_theme_directory(theme_dir, STORE_DOMAIN, target_id, interactive=allow_interactive, shopify_bin=shopify_bin):
        print("\n\033[91m[ERROR] Theme directory verification failed. Dev server cannot start.\033[0m")
        return 1
    elif sync_first:
        pull_theme_from_store(STORE_DOMAIN, target_id, theme_dir, shopify_bin)

    # Step 3: Check port availability
    chosen_port = port
    if is_port_in_use(chosen_port):
        print(f"\n\033[93m[PORT CHECK] Port {chosen_port} is currently in use.\033[0m")
        for alt_port in range(chosen_port + 1, chosen_port + 10):
            if not is_port_in_use(alt_port):
                print(f"\033[92m✔ Automatically shifted dev server to available port: {alt_port}\033[0m")
                chosen_port = alt_port
                break

    # Step 4: Display rich connection status
    print("\n\033[92m┌" + "─" * 68 + "┐")
    print(f"│ \033[1mTARGET THEME:\033[0m #{target_id} ({target_role})".ljust(77) + "│")
    print(f"│ \033[1mTHEME NAME:\033[0m   {target_name[:52]}".ljust(77) + "│")
    print(f"│ \033[1mLOCAL URL:\033[0m    http://127.0.0.1:{chosen_port}".ljust(77) + "│")
    print(f"│ \033[1mTHEME EDITOR:\033[0m https://{STORE_DOMAIN}/admin/themes/{target_id}/editor".ljust(77) + "│")
    print("└" + "─" * 68 + "┘\033[0m\n")
    print("\033[96m⚡ Live hot-reload and asset sync active. Press Ctrl+C to terminate.\033[0m\n")

    cmd = [
        shopify_bin, "theme", "dev",
        "--store", STORE_DOMAIN,
        "--theme", target_id,
        "--path", str(DEFAULT_THEME_DIR),
        "--port", str(chosen_port)
    ]
    if not auto_open:
        cmd.append("--no-open")

    try:
        proc = subprocess.run(cmd, cwd=str(repo_root))
        return proc.returncode
    except KeyboardInterrupt:
        print("\n\033[93mDev server gracefully stopped by user.\033[0m")
        return 0
    except Exception as ex:
        print(f"\n\033[91m[ERROR] Server execution failed: {ex}\033[0m")
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="The Baking Kaur Theme Dev Server")
    parser.add_argument("--theme", default=None, help="Target theme ID or name")
    parser.add_argument("--sync", action="store_true", help="Download/sync remote theme code before starting")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to bind (default: 9292)")
    parser.add_argument("--open", action="store_true", help="Automatically open browser on start")
    parser.add_argument("--list-themes", action="store_true", help="List all themes on store and exit")
    args = parser.parse_args()

    shopify_bin = resolve_executable("shopify")

    if args.list_themes:
        themes = fetch_store_themes(STORE_DOMAIN, shopify_bin)
        print(f"\nAvailable themes on {STORE_DOMAIN}:")
        for idx, t in enumerate(themes, 1):
            role_badge = f"[{t.get('role', 'unknown')}]"
            print(f"  {idx:2d}. #{t.get('id')} - {t.get('name')} {role_badge}")
        return

    code = start_server(
        theme_id=args.theme,
        sync_first=args.sync,
        port=args.port,
        auto_open=args.open
    )
    sys.exit(code)


if __name__ == "__main__":
    main()
