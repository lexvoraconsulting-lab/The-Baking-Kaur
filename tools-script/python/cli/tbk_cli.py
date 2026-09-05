#!/usr/bin/env python3
"""
The Baking Kaur — Master Atelier Operations CLI
High-ergonomics interactive console operations hub for storefront theme,
governance, SEO, AI Cake Genome, and release management.
"""
from __future__ import annotations

import argparse
import datetime
import os
import shutil
import subprocess
import sys
import time
import traceback
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


# --- Atelier Luxury Terminal Palette ---
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"

# Brand colors (TrueColor with ANSI fallback)
C_ROSE = "\033[38;2;192;20;87m"        # Atelier Velvet Rose (#C01457)
C_ROSE_DEEP = "\033[38;2;122;33;71m"   # Deep Wine (#7A2147)
C_GOLD = "\033[38;2;212;163;89m"       # Champagne Gold (#D4A359)
C_GOLD_BRIGHT = "\033[38;2;243;229;171m"  # Shimmer Gold Light
C_IVORY = "\033[38;2;253;242;244m"      # Pure Silk Ivory
C_MINT = "\033[38;2;46;204;113m"        # Verification Emerald
C_SKY = "\033[38;2;52;152;219m"         # Atelier Sky Blue
C_AMBER = "\033[38;2;230;126;34m"       # Warning Amber
C_LAVENDER = "\033[38;2;155;89;182m"    # Royal Lilac
C_BORDER = "\033[38;2;180;130;145m"     # Subtle Rose-Gold Border
C_MUTED = "\033[38;2;125;125;135m"      # Subtle Gray
C_BG_ROSE = "\033[48;2;90;15;45m"       # Header Rose Background


def resolve_executable(name: str) -> str:
    """Locate executable path, resolving .cmd/.bat extensions on Windows."""
    resolved = shutil.which(name)
    if resolved:
        return resolved

    # Check common Windows npm global tools directory
    appdata = os.environ.get("APPDATA", "")
    if appdata:
        npm_cmd = Path(appdata) / "npm" / f"{name}.cmd"
        if npm_cmd.exists():
            return str(npm_cmd)
        npm_bat = Path(appdata) / "npm" / f"{name}.bat"
        if npm_bat.exists():
            return str(npm_bat)

    # Check Python Scripts directory
    python_dir = Path(sys.executable).parent
    script_tool = python_dir / "Scripts" / f"{name}.exe"
    if script_tool.exists():
        return str(script_tool)

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

    WIDTH = 76

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

    def clear_screen(self) -> None:
        """Clear console screen cleanly on interactive runs."""
        if not self.test_mode:
            os.system("cls" if os.name == "nt" else "clear")

    def print_banner(self) -> None:
        """Render high-taste luxury atelier header and live system telemetry."""
        w = self.WIDTH
        inner = w - 2

        print()
        print(f"{C_GOLD}╔{'═' * inner}╗{C_RESET}")
        title = "✦   T H E   B A K I N G   K A U R   ·   A T E L I E R   S T U D I O   ✦"
        print(f"{C_GOLD}║{C_BOLD}{C_ROSE}{title.center(inner)}{C_RESET}{C_GOLD}║{C_RESET}")
        sub = "100% Pure Eggless Luxury Patisserie · Meerut, India"
        print(f"{C_GOLD}║{C_MUTED}{sub.center(inner)}{C_RESET}{C_GOLD}║{C_RESET}")
        print(f"{C_GOLD}╚{'═' * inner}╝{C_RESET}")

        # Active System Telemetry Card
        print(f"{C_BORDER}┌─ {C_GOLD}{C_BOLD}ACTIVE SYSTEM TELEMETRY{C_RESET}{C_BORDER} {'─' * (inner - 26)}┐{C_RESET}")

        def print_telemetry_line(label: str, value: str) -> None:
            prefix = f"  {label:<12} "
            vis = prefix + value
            pad = max(0, inner - len(vis))
            print(f"{C_BORDER}│{C_RESET}  {C_GOLD}{label:<12}{C_RESET} {C_IVORY}{value}{C_RESET}{' ' * pad}{C_BORDER}│{C_RESET}")

        print_telemetry_line("Store:", self.store_domain)
        print_telemetry_line("Target:", f"#{self.preview_theme_id} [TBK Birthday Collection V3 — Pastel]")
        print_telemetry_line("Runtime:", f"Python {sys.version.split()[0]} (F:\\frameworks\\Python314)")
        print_telemetry_line("Session:", f"logs/sessions/{self.logger.session_log_path.name}")
        print(f"{C_BORDER}└{'─' * inner}┘{C_RESET}")
        print()

    def print_menu_body(self) -> None:
        """Render organized, luxury domain cards with clear visual cadence."""
        w = self.WIDTH
        inner = w - 2

        def section_header(icon: str, title: str) -> None:
            header_text = f"{icon} {title}"
            remaining = inner - len(header_text) - 4
            print(f"{C_BORDER}├── {C_ROSE}{C_BOLD}{header_text}{C_RESET}{C_BORDER} {'─' * max(2, remaining)}┤{C_RESET}")

        def menu_item(num: str, desc: str, detail: str = "") -> None:
            vis_text = f"  {num:>3}   {desc}" + (f" ({detail})" if detail else "")
            pad = max(0, inner - len(vis_text))
            item_display = (
                f"  {C_GOLD_BRIGHT}{C_BOLD}{num:>3}{C_RESET}   "
                f"{C_IVORY}{desc}{C_RESET}"
                + (f" {C_MUTED}({detail}){C_RESET}" if detail else "")
                + (" " * pad)
            )
            print(f"{C_BORDER}│{C_RESET}{item_display}{C_BORDER}│{C_RESET}")

        # Menu Box Top
        print(f"{C_BORDER}┌── {C_GOLD}{C_BOLD}OPERATIONAL MODULES{C_RESET}{C_BORDER} {'─' * (inner - 22)}┐{C_RESET}")

        # Category 1: Storefront & Theme
        section_header("🌸", "STOREFRONT & THEME STUDIO")
        menu_item("1", "Start Local Dev Server", f"Port 9292 -> Preview #{self.preview_theme_id}")
        menu_item("2", "Run Theme Health Check", "Liquid & JSON integrity linter")
        menu_item("3", "Deploy to Preview Theme", f"Push code to #{self.preview_theme_id}")
        menu_item("4", "Deploy File to Live Theme", f"Live #{self.live_theme_id} · Diff protocol")

        # Category 2: Governance & Tasks
        section_header("🏛", "PROJECTOPS GOVERNANCE & PDM")
        menu_item("5", "12-Point Conformance Audit", "pdm audit Support — 0 errors gate")
        menu_item("6", "View Project Context", "Active delivery plans & current sprint")
        menu_item("7", "Task Lifecycle Workflow", "Start, complete, or sync PDM tasks")
        menu_item("8", "Create Git Checkpoint", "pdm checkpoint with clean commit")

        # Category 3: Store Automation & SEO
        section_header("⚡", "STORE AUTOMATION & SEO ENGINE")
        menu_item("9", "Run SEO Snippets Preview", "Safe read-only dry-run with CSV audit")
        menu_item("10", "Apply SEO Fixes to Live Store", "GraphQL batch mutation update")

        # Category 4: AI Cake Genome
        section_header("🧬", "AI CAKE GENOME & TEST SUITE")
        menu_item("11", "Run Full Pytest Test Suite", "233 tests: Vision + Taxonomy + SEO")

        # Category 5: Build & Release
        section_header("📦", "BUILD & RELEASE MANAGEMENT")
        menu_item("12", "Package Versioned Build", "Compile artifact into build/vX.Y.Z/")
        menu_item("13", "Publish Versioned Release", "Stage release into releases/v<Major>/")

        # Category 6: Observability & Exit
        section_header("📊", "OBSERVABILITY & STUDIO UTILITIES")
        menu_item("L", "View Session Log Summary", "Review last 25 operations in real-time")
        menu_item("0", "Exit Atelier Operations Hub", "Gracefully terminate session")

        # Menu Box Bottom
        print(f"{C_BORDER}└{'─' * inner}┘{C_RESET}")
        print()

    def run_clean_step(self, title: str, cmd: list[str], cwd: Path | None = None) -> bool:
        """Run a command cleanly with executive step card and session logging."""
        w = self.WIDTH
        inner = w - 2
        start_time = time.time()

        print(f"{C_BORDER}┌─ {C_GOLD}EXECUTING OPERATION{C_RESET}{C_BORDER} {'─' * (inner - 22)}┐{C_RESET}")
        print(f"{C_BORDER}│{C_RESET}  {C_BOLD}{title}{C_RESET}")
        print(f"{C_BORDER}│{C_RESET}  {C_MUTED}Command: {' '.join(cmd[:4])}{'...' if len(cmd) > 4 else ''}{C_RESET}")
        print(f"{C_BORDER}│{C_RESET}")
        print(f"{C_BORDER}│{C_RESET}  ⏳  {C_SKY}Processing step in background...{C_RESET}", end="", flush=True)

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
                print(f"{C_BORDER}└{'─' * inner}┘{C_RESET}\n")
                return True
            else:
                print(f"\r{C_BORDER}│{C_RESET}  {C_AMBER}{C_BOLD}✖  Failed with exit code {exit_code}{C_RESET} {C_MUTED}({elapsed:.2f}s){C_RESET}")
                print(f"{C_BORDER}│{C_RESET}  {C_GOLD}Last output lines:{C_RESET}")
                for err_line in output_lines[-5:]:
                    clean_err = err_line.strip()[:inner - 6]
                    print(f"{C_BORDER}│{C_RESET}    {C_MUTED}{clean_err}{C_RESET}")
                print(f"{C_BORDER}│{C_RESET}  {C_MUTED}Full audit log: logs/latest_session.log{C_RESET}")
                print(f"{C_BORDER}└{'─' * inner}┘{C_RESET}\n")
                return False
        except Exception as ex:
            elapsed = time.time() - start_time
            print(f"\r{C_BORDER}│{C_RESET}  {C_AMBER}{C_BOLD}✖  Execution Exception: {ex}{C_RESET} {C_MUTED}({elapsed:.2f}s){C_RESET}")
            print(f"{C_BORDER}└{'─' * inner}┘{C_RESET}\n")
            self.logger.log(f"EXCEPTION: {ex}\n{traceback.format_exc()}")
            return False

    def pause(self) -> None:
        """Clean interactive pause prompt."""
        if not self.test_mode:
            print(f"{C_MUTED}────────────────────────────────────────────────────────────────────────{C_RESET}")
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
        self.run_clean_step("Analyzing theme Liquid & JSON code health", [shopify_bin, "theme", "check", "tbk-spfy-theme"])
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
                task_id = input(f"{C_GOLD}Enter Task ID to start (e.g. TOOL-01.01, HOME-01.01): {C_RESET}").strip()
                if task_id:
                    self.run_clean_step(f"Starting task {task_id}", [sys.executable, str(self.pdm_bin), "worklog", "start", task_id])
            elif choice == "2":
                task_id = input(f"{C_GOLD}Enter Task ID to complete (e.g. TOOL-01.01, HOME-01.01): {C_RESET}").strip()
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
                choice = input(f"{C_ROSE}{C_BOLD}tbk-studio ❯ {C_RESET}").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{C_MINT}Exiting The Baking Kaur Studio. Goodbye!{C_RESET}\n")
                break

            if choice in ("0", "exit", "q"):
                print(f"\n{C_MINT}Exiting The Baking Kaur Studio. Goodbye!{C_RESET}\n")
                break
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
                print(f"\n{C_AMBER}Invalid selection '{choice}'. Please select an option from 1 to 13, L, or 0.{C_RESET}")
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
