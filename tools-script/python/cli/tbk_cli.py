#!/usr/bin/env python3
"""
The Baking Kaur — Master Atelier Operations CLI
Executive luxury terminal interface for storefront theme, governance,
SEO, AI Cake Genome, and release management.
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import unicodedata
from pathlib import Path

# Enable ANSI escape sequences and UTF-8 encoding on Windows console
if os.name == "nt":
    os.system("")

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# --- Atelier Haute Pâtisserie Palette (24-bit TrueColor) ---
C_RESET        = "\033[0m"
C_BOLD         = "\033[1m"
C_DIM          = "\033[2m"
C_ITALIC       = "\033[3m"

# Brand colors
C_GOLD_SHIMMER = "\033[38;2;248;238;200m"  # Shimmer Gold Light
C_GOLD_BRIGHT  = "\033[38;2;235;195;125m"  # Pale Champagne
C_GOLD         = "\033[38;2;212;163;89m"   # Classic Patisserie Gold (#D4A359)
C_ROSE_GOLD    = "\033[38;2;215;130;120m"  # Rose Gold Transition
C_ROSE         = "\033[38;2;192;20;87m"    # Atelier Velvet Rose (#C01457)
C_ROSE_DEEP    = "\033[38;2;140;22;65m"    # Deep Berry Wine (#8C1641)
C_WINE         = "\033[38;2;100;15;45m"    # Dark Burgundy
C_IVORY        = "\033[38;2;253;245;246m"  # Pure Silk Ivory
C_MINT         = "\033[38;2;46;204;113m"   # Verification Emerald
C_SKY          = "\033[38;2;52;152;219m"   # Atelier Sky Blue
C_AMBER        = "\033[38;2;230;126;34m"   # Warning Amber
C_LAVENDER     = "\033[38;2;175;110;200m"  # Royal Lilac
C_BORDER       = "\033[38;2;160;105;125m"  # Subtle Velvet Rose Border
C_BORDER_GOLD  = "\033[38;2;180;140;90m"   # Soft Gold Border
C_MUTED        = "\033[38;2;135;135;145m"  # Elegant Slate Muted


def vis_len(s: str) -> int:
    """Calculate visible console width of a string, accounting for ANSI codes and wide glyphs."""
    clean = re.sub(r"\x1b\[[0-9;]*m", "", s)
    width = 0
    for ch in clean:
        ea = unicodedata.east_asian_width(ch)
        if ea in ("W", "F"):
            width += 2
        else:
            width += 1
    return width


def resolve_executable(name: str) -> str:
    """Locate executable path, resolving centralized F:\frameworks first, then PATH."""
    # 1. Check centralized npm-global tools directory on F: drive
    f_npm = Path(r"F:\frameworks\nodejs\npm-global")
    if (f_npm / f"{name}.cmd").exists():
        return str(f_npm / f"{name}.cmd")
    if (f_npm / f"{name}.bat").exists():
        return str(f_npm / f"{name}.bat")
    if (f_npm / name).exists():
        return str(f_npm / name)

    # 2. Check centralized Python Scripts directory on F: drive
    f_python_scripts = Path(r"F:\frameworks\python\python314\Scripts")
    if (f_python_scripts / f"{name}.exe").exists():
        return str(f_python_scripts / f"{name}.exe")

    # 3. Check current python runtime directory
    python_dir = Path(sys.executable).parent
    if (python_dir / "Scripts" / f"{name}.exe").exists():
        return str(python_dir / "Scripts" / f"{name}.exe")

    # 4. Standard shutil.which fallback
    resolved = shutil.which(name)
    if resolved:
        return resolved

    # 5. Check APPDATA npm fallback
    appdata = os.environ.get("APPDATA", "")
    if appdata:
        if (Path(appdata) / "npm" / f"{name}.cmd").exists():
            return str(Path(appdata) / "npm" / f"{name}.cmd")
        if (Path(appdata) / "npm" / f"{name}.bat").exists():
            return str(Path(appdata) / "npm" / f"{name}.bat")

    return name


class SessionLogger:
    """Manages session-based logging in logs/sessions/."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.logs_dir = repo_root / "logs"
        self.sessions_dir = self.logs_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_log_path = self.sessions_dir / f"session_{timestamp}.log"
        self.latest_log_path = self.logs_dir / "latest_session.log"

        header = (
            f"=== The Baking Kaur — Atelier Operations Session Log ===\n"
            f"Session Started: {datetime.datetime.now().isoformat()}\n"
            f"Repository: {self.repo_root}\n"
            f"Python Runtime: {sys.executable}\n"
            f"=========================================================\n\n"
        )
        self.session_log_path.write_text(header, encoding="utf-8")
        self.update_latest_pointer()

    def update_latest_pointer() -> None:
        pass

    def update_latest_pointer(self) -> None:
        try:
            shutil.copy2(self.session_log_path, self.latest_log_path)
        except Exception:
            pass

    def log(self, message: str) -> None:
        try:
            with open(self.session_log_path, "a", encoding="utf-8", errors="replace") as f:
                f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n")
            self.update_latest_pointer()
        except Exception:
            pass


class TBKConsoleCLI:
    """Executive luxury terminal interface for The Baking Kaur operations."""

    WIDTH = 92

    def __init__(self, repo_root: Path, test_mode: bool = False):
        self.repo_root = repo_root
        self.test_mode = test_mode
        self.logger = SessionLogger(repo_root)
        self.pdm_bin = Path(r"F:\GitRepos\LXC-AI-Skills\skills\projectops-v2\bin\pdm")

        # Canonical configuration
        self.store_domain = "ae86ba-2a.myshopify.com"
        self.preview_theme_id = "152070258857"
        self.live_theme_id = "152071602345"

        # Build clean execution environment with PYTHONPATH
        self.env = os.environ.copy()
        ai_dir = str(repo_root / "tbk-spfy-ai")
        seo_dir = str(repo_root / "tbk-spfy-seo" / "ops")
        root_dir = str(repo_root)
        existing_pypath = self.env.get("PYTHONPATH", "")
        self.env["PYTHONPATH"] = f"{root_dir};{ai_dir};{seo_dir}" + (f";{existing_pypath}" if existing_pypath else "")
        self.env["PYTHONIOENCODING"] = "utf-8"
        self.env["PYTHONUSERBASE"] = r"F:\frameworks\python\python314"

    def clear_screen(self) -> None:
        """Clear console screen cleanly on interactive runs."""
        if not self.test_mode:
            os.system("cls" if os.name == "nt" else "clear")

    def print_banner(self) -> None:
        """Render grand 5x sculpted typography and luxury patisserie header."""
        w = self.WIDTH
        inner = w - 2
        border = C_BORDER_GOLD

        baking_rows = [
            ("  ██████╗   █████╗  ██╗  ██╗ ██╗ ███╗   ██╗  ██████╗  ", C_GOLD_SHIMMER),
            ("  ██╔══██╗ ██╔══██╗ ██║ ██╔╝ ██║ ████╗  ██║ ██╔════╝  ", C_GOLD_BRIGHT),
            ("  ██████╔╝ ███████║ █████═╝  ██║ ██╔██╗ ██║ ██║  ███╗ ", C_ROSE_GOLD),
            ("  ██╔══██╗ ██╔══██║ ██╔═██╗  ██║ ██║╚██╗██║ ██║   ██║ ", C_ROSE),
            ("  ██████╔╝ ██║  ██║ ██║ ╚██╗ ██║ ██║ ╚████║ ╚██████╔╝ ", C_ROSE_DEEP),
        ]

        print()
        print(f"{border}╔{'═' * inner}╗{C_RESET}")

        # Atelier header flourish
        top_flourish = "◈  ──  ✧  ──  ❖   🍰   A T E L I E R   D E   P Â T I S S E R I E   🍰   ❖  ──  ✧  ──  ◈"
        t_pad_l = (inner - vis_len(top_flourish)) // 2
        t_pad_r = inner - vis_len(top_flourish) - t_pad_l
        print(f"{border}║{C_RESET}{' ' * t_pad_l}{C_GOLD_SHIMMER}{top_flourish}{C_RESET}{' ' * t_pad_r}{border}║{C_RESET}")
        print(f"{border}╠{'═' * inner}╣{C_RESET}")

        # Ivory Flourish above BAKING
        the_line = "✦   T   H   E   ✦"
        pad_l = (inner - vis_len(the_line)) // 2
        pad_r = inner - vis_len(the_line) - pad_l
        print(f"{border}║{C_RESET}{' ' * pad_l}{C_IVORY}{C_BOLD}{the_line}{C_RESET}{' ' * pad_r}{border}║{C_RESET}")

        # 5x Sculpted BAKING Logo with vertical chromatic gradient
        for row_text, color in baking_rows:
            r_pad_l = (inner - vis_len(row_text)) // 2
            r_pad_r = inner - vis_len(row_text) - r_pad_l
            print(f"{border}║{C_RESET}{' ' * r_pad_l}{color}{C_BOLD}{row_text}{C_RESET}{' ' * r_pad_r}{border}║{C_RESET}")

        # Velvet Rose Flourish below BAKING
        kaur_line = "✧   K   A   U   R   ✧"
        k_pad_l = (inner - vis_len(kaur_line)) // 2
        k_pad_r = inner - vis_len(kaur_line) - k_pad_l
        print(f"{border}║{C_RESET}{' ' * k_pad_l}{C_ROSE}{C_BOLD}{kaur_line}{C_RESET}{' ' * k_pad_r}{border}║{C_RESET}")

        # Subtitle
        sub1 = "100% PURE EGGLESS LUXURY PATISSERIE · MEERUT, INDIA"
        s1_pad_l = (inner - vis_len(sub1)) // 2
        s1_pad_r = inner - vis_len(sub1) - s1_pad_l
        print(f"{border}║{C_RESET}{' ' * s1_pad_l}{C_GOLD}{sub1}{C_RESET}{' ' * s1_pad_r}{border}║{C_RESET}")

        sub2 = "Haute Pâtisserie Française · Artisanal Confections · AI Cake Genome"
        s2_pad_l = (inner - vis_len(sub2)) // 2
        s2_pad_r = inner - vis_len(sub2) - s2_pad_l
        print(f"{border}║{C_RESET}{' ' * s2_pad_l}{C_MUTED}{sub2}{C_RESET}{' ' * s2_pad_r}{border}║{C_RESET}")
        print(f"{border}╚{'═' * inner}╝{C_RESET}")
        print()

        # Active System Telemetry Card (2-Column Structured Grid)
        t_border = C_BORDER
        card_w = inner
        print(f"{t_border}╭─ {C_GOLD}{C_BOLD}SYSTEM TELEMETRY & RUNTIME STATE{C_RESET}{t_border} {'─' * (card_w - 35)}╮{C_RESET}")

        telemetry_left = [
            ("Store Domain", self.store_domain, C_MINT),
            ("Preview Theme", f"#{self.preview_theme_id} (Birthday V3)", C_SKY),
            ("Live Theme", f"#{self.live_theme_id} [Rule 2.1]", C_AMBER),
        ]
        telemetry_right = [
            ("Python Engine", f"v{sys.version.split()[0]} (F:\\frameworks)", C_MINT),
            ("Shopify CLI", "v4.7.1 (F:\\frameworks)", C_MINT),
            ("Session Log", "logs/latest_session.log", C_IVORY),
        ]

        for (l_lbl, l_val, l_col), (r_lbl, r_val, r_col) in zip(telemetry_left, telemetry_right):
            l_plain = f"  {l_lbl:<14} {l_val}"
            l_pad = max(0, 44 - vis_len(l_plain))
            l_display = f"  {C_GOLD}{l_lbl:<14}{C_RESET} {l_col}{l_val}{C_RESET}" + (" " * l_pad)

            r_plain = f"{r_lbl:<14} {r_val}"
            r_pad = max(0, 43 - vis_len(r_plain))
            r_display = f"{C_GOLD}{r_lbl:<14}{C_RESET} {r_col}{r_val}{C_RESET}" + (" " * r_pad)

            print(f"{t_border}│{C_RESET}{l_display}{t_border} │ {C_RESET}{r_display}{t_border}│{C_RESET}")

        print(f"{t_border}╰{'─' * card_w}╯{C_RESET}")
        print()

    def print_menu_body(self) -> None:
        """Render organized, luxury domain cards with intuitive operator UX."""
        w = self.WIDTH
        inner = w - 2
        t_border = C_BORDER

        def section_header(icon: str, title: str) -> None:
            header_text = f" {icon}  {title} "
            remaining = max(2, inner - 2 - vis_len(header_text))
            print(f"{t_border}├──{C_ROSE}{C_BOLD}{header_text}{C_RESET}{t_border}{'─' * remaining}┤{C_RESET}")

        def menu_item(num: str, desc: str, detail: str = "") -> None:
            num_str = f"[{num:^3}]"
            plain_line = f"   {num_str}  {desc:<28} {detail}"
            pad = max(0, inner - vis_len(plain_line))
            display_line = (
                f"   {C_GOLD_BRIGHT}{C_BOLD}{num_str}{C_RESET}  "
                f"{C_IVORY}{desc:<28}{C_RESET} "
                f"{C_MUTED}{detail}{C_RESET}"
                + (" " * pad)
            )
            print(f"{t_border}│{C_RESET}{display_line}{t_border}│{C_RESET}")

        print(f"{t_border}╭── {C_GOLD}{C_BOLD}OPERATIONAL MODULES{C_RESET}{t_border} {'─' * (inner - 24)}╮{C_RESET}")

        # Category 1: Storefront & Theme
        section_header("🌸", "01 · STOREFRONT & THEME STUDIO")
        menu_item("1", "Start Local Dev Server", f"Port 9292 -> Preview #{self.preview_theme_id}")
        menu_item("2", "Run Theme Health Check", "Liquid syntax, schema & JSON integrity")
        menu_item("3", "Deploy to Preview Theme", f"Direct push to Preview #{self.preview_theme_id}")
        menu_item("4", "Deploy File to Live Theme", f"Live #{self.live_theme_id} · Rule 5.2 Differential Protocol")

        # Category 2: Governance & Tasks
        section_header("🏛", "02 · PROJECTOPS GOVERNANCE & PDM")
        menu_item("5", "12-Point Conformance Audit", "pdm audit Support (Strict 0 Errors Gate)")
        menu_item("6", "View Project Context", "Active delivery plans & current sprint matrix")
        menu_item("7", "Task Lifecycle Workflow", "pdm task start / complete / sync")
        menu_item("8", "Create Git Checkpoint", "pdm checkpoint (Audit-Gated Commit & Push)")

        # Category 3: Store Automation & SEO
        section_header("⚡", "03 · STORE AUTOMATION & SEO ENGINE")
        menu_item("9", "Run SEO Snippets Preview", "Safe dry-run preview with CSV audit report")
        menu_item("10", "Apply SEO Fixes to Live", "GraphQL batch mutation sync")

        # Category 4: AI Cake Genome
        section_header("🧬", "04 · AI CAKE GENOME & VISION PIPELINE")
        menu_item("11", "Run Full Pytest Suite", "233 tests: Vision, Taxonomy & Storefront")

        # Category 5: Build & Release
        section_header("📦", "05 · BUILD & RELEASE MANAGEMENT")
        menu_item("12", "Package Versioned Build", "Compile archive into build/vX.Y.Z/")
        menu_item("13", "Publish Versioned Release", "Stage release into releases/v<Major>/")

        # Category 6: Observability & Exit
        section_header("📊", "06 · SYSTEM OBSERVABILITY & CONTROL")
        menu_item("L", "View Session Log Summary", "Tail last 25 operations in real time")
        menu_item("R", "Refresh Telemetry & Status", "Re-query Shopify CLI & Python runtimes")
        menu_item("0", "Exit Atelier Operations", "Graceful session termination")

        print(f"{t_border}╰{'─' * inner}╯{C_RESET}")
        print()

    def run_clean_step(self, title: str, cmd: list[str], cwd: Path | None = None) -> bool:
        """Run a command cleanly with executive step card and session logging."""
        w = self.WIDTH
        inner = w - 2
        start_time = time.time()

        print(f"{C_BORDER}╭─ {C_GOLD}EXECUTING OPERATION{C_RESET}{C_BORDER} {'─' * (inner - 22)}╮{C_RESET}")
        print(f"{C_BORDER}│{C_RESET}  {C_BOLD}{title}{C_RESET}")
        print(f"{C_BORDER}│{C_RESET}  {C_MUTED}Command: {' '.join(cmd[:4])}{'...' if len(cmd) > 4 else ''}{C_RESET}")
        print(f"{C_BORDER}│{C_RESET}")
        print(f"{C_BORDER}│{C_RESET}  ⏳  {C_SKY}Processing operation...{C_RESET}", end="", flush=True)

        self.logger.log(f"COMMAND START: {' '.join(cmd)}")

        working_dir = cwd or self.repo_root
        resolved_cmd = list(cmd)
        resolved_cmd[0] = resolve_executable(resolved_cmd[0])

        try:
            process = subprocess.Popen(
                resolved_cmd,
                cwd=str(working_dir),
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            output_lines = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    output_lines.append(line)
                    self.logger.log(line.strip())

            exit_code = process.poll()
            elapsed = time.time() - start_time

            if exit_code == 0:
                print(f"\r{C_BORDER}│{C_RESET}  {C_MINT}{C_BOLD}✔  Operation Completed Successfully{C_RESET} {C_MUTED}({elapsed:.2f}s){C_RESET}")
                print(f"{C_BORDER}╰{'─' * inner}╯{C_RESET}\n")
                return True
            else:
                print(f"\r{C_BORDER}│{C_RESET}  {C_AMBER}{C_BOLD}✖  Failed with exit code {exit_code}{C_RESET} {C_MUTED}({elapsed:.2f}s){C_RESET}")
                print(f"{C_BORDER}│{C_RESET}  {C_GOLD}Last output lines:{C_RESET}")
                for err_line in output_lines[-5:]:
                    clean_err = err_line.strip()[:inner - 6]
                    print(f"{C_BORDER}│{C_RESET}    {C_MUTED}{clean_err}{C_RESET}")
                print(f"{C_BORDER}│{C_RESET}  {C_MUTED}Full audit log: logs/latest_session.log{C_RESET}")
                print(f"{C_BORDER}╰{'─' * inner}╯{C_RESET}\n")
                return False
        except Exception as ex:
            elapsed = time.time() - start_time
            print(f"\r{C_BORDER}│{C_RESET}  {C_AMBER}{C_BOLD}✖  Execution Exception: {ex}{C_RESET} {C_MUTED}({elapsed:.2f}s){C_RESET}")
            print(f"{C_BORDER}╰{'─' * inner}╯{C_RESET}\n")
            self.logger.log(f"EXCEPTION: {ex}\n{traceback.format_exc()}")
            return False

    def pause(self) -> None:
        """Clean interactive pause prompt."""
        if not self.test_mode:
            print(f"{C_MUTED}──────────────────────────────────────────────────────────────────────────────────────────{C_RESET}")
            try:
                input(f"{C_GOLD}Press Enter to return to Atelier Studio menu...{C_RESET}")
            except (KeyboardInterrupt, EOFError):
                print()

    # --- Operational Handlers ---

    def handle_theme_dev(self) -> None:
        dev_server_py = self.repo_root / "tools-script" / "python" / "theme" / "theme_dev_server.py"
        try:
            subprocess.run(
                [sys.executable, str(dev_server_py)],
                cwd=str(self.repo_root),
                env=self.env,
            )
        except Exception as ex:
            print(f"\n{C_AMBER}Error launching theme dev server: {ex}{C_RESET}")
        self.pause()

    def handle_theme_check(self) -> None:
        shopify_bin = resolve_executable("shopify")
        self.run_clean_step("Analyzing theme Liquid & JSON code health", [shopify_bin, "theme", "check", "--path", "tbk-spfy-theme"])
        self.pause()

    def handle_theme_deploy_preview(self) -> None:
        shopify_bin = resolve_executable("shopify")
        success = self.run_clean_step(
            f"Pushing theme code to Preview Theme #{self.preview_theme_id}",
            [shopify_bin, "theme", "push", "--store", self.store_domain, "--theme", self.preview_theme_id, "--path", "tbk-spfy-theme"]
        )
        if success:
            print(f"\n{C_MINT}✔ Preview is live: https://{self.store_domain}/?preview_theme_id={self.preview_theme_id}{C_RESET}")
        self.pause()

    def handle_pdm_audit(self) -> None:
        self.run_clean_step(
            "Verifying 12-point architectural governance conformance",
            [sys.executable, str(self.pdm_bin), "audit", "Support"]
        )
        self.pause()

    def handle_pdm_context(self) -> None:
        print(f"\n{C_GOLD}{C_BOLD}▶ Active ProjectOps v2 Context & Governance Summary:{C_RESET}\n")
        subprocess.run([sys.executable, str(self.pdm_bin), "context", "resume"], cwd=str(self.repo_root), env=self.env)
        self.pause()

    def handle_task_workflow(self) -> None:
        print(f"\n{C_GOLD}{C_BOLD}▶ Task Management Workflow (ProjectOps v2):{C_RESET}")
        print(f"  {C_GOLD_BRIGHT}[1]{C_RESET} Start Task (Set to IN PROGRESS)")
        print(f"  {C_GOLD_BRIGHT}[2]{C_RESET} Complete Task (Set to COMPLETED)")
        print(f"  {C_MUTED}[0] Cancel{C_RESET}")
        try:
            choice = input(f"\n{C_GOLD}Select action [0-2]: {C_RESET}").strip()
            if choice == "1":
                task_id = input(f"{C_GOLD}Enter Task ID to start (e.g. MENU-01.01, SLOT-01.01): {C_RESET}").strip()
                if task_id:
                    self.run_clean_step(f"Starting task {task_id}", [sys.executable, str(self.pdm_bin), "worklog", "start", task_id])
            elif choice == "2":
                task_id = input(f"{C_GOLD}Enter Task ID to complete (e.g. MENU-01.01, SLOT-01.01): {C_RESET}").strip()
                if task_id:
                    self.run_clean_step(f"Completing task {task_id}", [sys.executable, str(self.pdm_bin), "task", "complete", task_id])
        except (KeyboardInterrupt, EOFError):
            print()
        self.pause()

    def handle_pdm_checkpoint(self) -> None:
        try:
            msg = input(f"\n{C_GOLD}Enter semantic commit message: {C_RESET}").strip()
            if msg:
                self.run_clean_step(
                    f"Creating Git Governance Checkpoint: {msg}",
                    [sys.executable, str(self.pdm_bin), "checkpoint", "-m", msg]
                )
        except (KeyboardInterrupt, EOFError):
            print()
        self.pause()

    def handle_seo_ops(self, apply_mode: bool = False) -> None:
        flag = "--apply" if apply_mode else "--dry-run"
        mode_label = "LIVE APPLY" if apply_mode else "SAFE DRY-RUN"
        self.run_clean_step(
            f"Executing SEO snippet optimization ({mode_label})",
            [sys.executable, "tbk-spfy-seo/ops/fix_seo_snippets.py", flag]
        )
        self.pause()

    def handle_tests(self) -> None:
        self.run_clean_step(
            "Executing full pytest suite (233 tests: Vision + Taxonomy + SEO)",
            [sys.executable, "-m", "pytest", "-q"]
        )
        self.pause()

    def handle_build(self) -> None:
        try:
            version = input(f"\n{C_GOLD}Enter build version (default: 1.0.0): {C_RESET}").strip() or "1.0.0"
            packager_path = self.repo_root / "tools-script" / "python" / "release" / "build_packager.py"
            self.run_clean_step(
                f"Compiling production build package v{version.lstrip('v')}",
                [sys.executable, str(packager_path), "--version", version]
            )
        except (KeyboardInterrupt, EOFError):
            print()
        self.pause()

    def handle_release(self) -> None:
        try:
            version = input(f"\n{C_GOLD}Enter release version (default: 1.0): {C_RESET}").strip() or "1.0"
            major = input(f"{C_GOLD}Enter major release grouping (default: 1): {C_RESET}").strip() or "1"
            release_path = self.repo_root / "tools-script" / "python" / "release" / "release_manager.py"
            self.run_clean_step(
                f"Publishing release v{version.lstrip('v')} into releases/v{major}/",
                [sys.executable, str(release_path), "--version", version, "--major", major]
            )
        except (KeyboardInterrupt, EOFError):
            print()
        self.pause()

    def handle_view_log(self) -> None:
        print(f"\n{C_GOLD}{C_BOLD}▶ Active Session Log Summary (Last 25 Events):{C_RESET}\n")
        if self.logger.session_log_path.exists():
            lines = self.logger.session_log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            for line in lines[-25:]:
                print(f"  {C_MUTED}{line}{C_RESET}")
        else:
            print(f"  {C_MUTED}No log events recorded yet.{C_RESET}")
        self.pause()

    # --- Main Loop ---

    def run_menu(self) -> None:
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu_body()

            if self.test_mode:
                print(f"{C_GOLD}Test mode enabled. Exiting menu loop cleanly.{C_RESET}")
                break

            try:
                prompt_line = f"{C_ROSE}{C_BOLD}tbk-atelier ❯ {C_RESET}"
                choice = input(prompt_line).strip().lower()
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{C_MINT}Exiting The Baking Kaur Studio. Goodbye!{C_RESET}\n")
                break

            if choice in ("0", "exit", "q"):
                print(f"\n{C_MINT}Exiting The Baking Kaur Studio. Goodbye!{C_RESET}\n")
                break
            elif choice in ("r", "refresh"):
                continue
            elif choice in ("1", "1.1"):
                self.handle_theme_dev()
            elif choice in ("2", "1.2"):
                self.handle_theme_check()
            elif choice in ("3", "1.3"):
                self.handle_theme_deploy_preview()
            elif choice in ("4", "1.4"):
                try:
                    file_to_deploy = input(f"\n{C_GOLD}Enter theme file relative path (e.g. sections/bk-trust-strip.liquid): {C_RESET}").strip()
                    if file_to_deploy:
                        deploy_script = self.repo_root / "tools-script" / "win" / "theme" / "theme_deploy_live.bat"
                        subprocess.run(["cmd.exe", "/c", str(deploy_script), file_to_deploy])
                        self.pause()
                except (KeyboardInterrupt, EOFError):
                    print()
            elif choice in ("5", "2.1"):
                self.handle_pdm_audit()
            elif choice in ("6", "2.2"):
                self.handle_pdm_context()
            elif choice in ("7", "2.3"):
                self.handle_task_workflow()
            elif choice in ("8", "2.4"):
                self.handle_pdm_checkpoint()
            elif choice in ("9", "3.1"):
                self.handle_seo_ops(apply_mode=False)
            elif choice in ("10", "3.2"):
                self.handle_seo_ops(apply_mode=True)
            elif choice in ("11", "4.1"):
                self.handle_tests()
            elif choice in ("12", "5.1"):
                self.handle_build()
            elif choice in ("13", "5.2"):
                self.handle_release()
            elif choice in ("l", "log", "logs"):
                self.handle_view_log()
            else:
                print(f"\n{C_AMBER}Invalid selection '{choice}'. Please select an option from 1 to 13, L, R, or 0.{C_RESET}")
                time.sleep(1.2)


def main() -> None:
    parser = argparse.ArgumentParser(description="The Baking Kaur Master Atelier Operations CLI")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode without blocking prompt")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    cli = TBKConsoleCLI(repo_root, test_mode=args.test_mode)
    cli.run_menu()


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"\n[FATAL ERROR] An unexpected error occurred: {ex}")
        traceback.print_exc()
        input("\nPress Enter to close window...")
