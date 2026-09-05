#!/usr/bin/env python3
"""
The Baking Kaur — Master Operations CLI
Interactive menu-based operations hub for theme, governance, SEO, AI, and releases.
"""
from __future__ import annotations

import argparse
import datetime
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


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
            f"=== The Baking Kaur — Operations Session Log ===\n"
            f"Session Started: {datetime.datetime.now().isoformat()}\n"
            f"Repository: {self.repo_root}\n"
            f"=================================================\n\n"
        )
        self.session_log_path.write_text(header, encoding="utf-8")
        self.update_latest_pointer()

    def update_latest_pointer(self) -> None:
        try:
            shutil.copy2(self.session_log_path, self.latest_log_path)
        except Exception:
            pass

    def log(self, message: str) -> None:
        with open(self.session_log_path, "a", encoding="utf-8", errors="replace") as f:
            f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.update_latest_pointer()


class TBKConsoleCLI:
    """Master interactive console interface for The Baking Kaur operations."""

    def __init__(self, repo_root: Path, test_mode: bool = False):
        self.repo_root = repo_root
        self.test_mode = test_mode
        self.logger = SessionLogger(repo_root)
        self.pdm_bin = Path(r"F:\GitRepos\LXC-AI-Skills\skills\projectops-v2\bin\pdm")

    def print_banner(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("\033[93m" + "╔" + "═" * 70 + "╗")
        print("║" + "       THE BAKING KAUR — MASTER OPERATIONS HUB".center(70) + "║")
        print("║" + "        100% Eggless Luxury Cake Studio · Meerut".center(70) + "║")
        print("╚" + "═" * 70 + "╝" + "\033[0m")
        print(f"\033[90mSession Log: logs/sessions/{self.logger.session_log_path.name}\033[0m\n")

    def run_clean_step(self, title: str, cmd: list[str], cwd: Path | None = None) -> bool:
        """Run a command cleanly, suppressing noise and piping verbose logs to the session file."""
        print(f"⏳  {title}...", end="", flush=True)
        self.logger.log(f"COMMAND START: {' '.join(cmd)}")

        working_dir = cwd or self.repo_root
        try:
            process = subprocess.Popen(
                cmd,
                cwd=str(working_dir),
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
            if exit_code == 0:
                print("\r\033[92m✔  " + f"{title} [Completed Successfully]\033[0m")
                return True
            else:
                print("\r\033[91m✖  " + f"{title} [Failed with code {exit_code}]\033[0m")
                print("\033[93m  Last lines from output:\033[0m")
                for err_line in output_lines[-5:]:
                    print(f"    \033[90m{err_line.strip()}\033[0m")
                print(f"  \033[90mDetailed log available in: logs/latest_session.log\033[0m")
                return False
        except Exception as ex:
            print("\r\033[91m✖  " + f"{title} [Error: {ex}]\033[0m")
            self.logger.log(f"EXCEPTION: {ex}")
            return False

    def pause(self) -> None:
        if not self.test_mode:
            print()
            input("\033[96mPress Enter to return to main menu...\033[0m")

    # --- Subsystem Handlers ---

    def handle_theme_dev(self) -> None:
        print("\n\033[94m▶ Launching Shopify Theme Development Server...\033[0m")
        print("\033[90mTarget: Preview Theme #151370334377 on ae86ba-2a.myshopify.com\033[0m")
        print("\033[92mLocal Preview URL: http://127.0.0.1:9292\033[0m")
        print("\033[90m(Press Ctrl+C inside the server to terminate and return to menu)\033[0m\n")
        subprocess.run(
            [
                "shopify", "theme", "dev",
                "--store", "ae86ba-2a.myshopify.com",
                "--theme", "151370334377",
                "--path", "tbk-spfy-theme"
            ],
            cwd=str(self.repo_root)
        )
        self.pause()

    def handle_theme_check(self) -> None:
        print("\n\033[94m▶ Running Theme Linter & Code Health Check...\033[0m")
        self.run_clean_step("Analyzing theme Liquid & JSON files", ["shopify", "theme", "check", "tbk-spfy-theme"])
        self.pause()

    def handle_theme_deploy_preview(self) -> None:
        print("\n\033[94m▶ Deploying to Preview Theme (#151370334377)...\033[0m")
        success = self.run_clean_step(
            "Pushing theme code to Preview Theme #151370334377",
            ["shopify", "theme", "push", "--store", "ae86ba-2a.myshopify.com", "--theme", "151370334377", "--path", "tbk-spfy-theme"]
        )
        if success:
            print("\033[92m✔ Preview is ready: https://ae86ba-2a.myshopify.com/?preview_theme_id=151370334377\033[0m")
        self.pause()

    def handle_pdm_audit(self) -> None:
        print("\n\033[94m▶ Running ProjectOps v2 Conformance Audit (12-Point Gate)...\033[0m")
        self.run_clean_step(
            "Verifying 12-point architectural conformance",
            [sys.executable, str(self.pdm_bin), "audit", "Support"]
        )
        self.pause()

    def handle_pdm_context(self) -> None:
        print("\n\033[94m▶ Checking Project Context & Active Delivery Tasks...\033[0m")
        subprocess.run([sys.executable, str(self.pdm_bin), "context", "check"], cwd=str(self.repo_root))
        self.pause()

    def handle_task_workflow(self) -> None:
        print("\n\033[94m▶ Task Management Workflow (ProjectOps v2)...\033[0m")
        print("  [1] Start Task (Set to IN PROGRESS)")
        print("  [2] Complete Task (Set to COMPLETED)")
        print("  [0] Cancel")
        choice = input("\nSelect action [0-2]: ").strip()
        if choice == "1":
            task_id = input("Enter Task ID to start (e.g. SLOT-01.01, HOME-01.01): ").strip()
            if task_id:
                self.run_clean_step(f"Starting task {task_id}", [sys.executable, str(self.pdm_bin), "worklog", "start", task_id])
        elif choice == "2":
            task_id = input("Enter Task ID to complete (e.g. SLOT-01.01, HOME-01.01): ").strip()
            if task_id:
                self.run_clean_step(f"Completing task {task_id}", [sys.executable, str(self.pdm_bin), "worklog", "complete", task_id])
        self.pause()

    def handle_pdm_checkpoint(self) -> None:
        print("\n\033[94m▶ Create Clean Git Governance Checkpoint...\033[0m")
        msg = input("Enter semantic commit message: ").strip()
        if msg:
            self.run_clean_step(
                f"Committing checkpoint: {msg}",
                [sys.executable, str(self.pdm_bin), "checkpoint", "-m", msg]
            )
        self.pause()

    def handle_seo_ops(self, apply_mode: bool = False) -> None:
        mode_label = "APPLY" if apply_mode else "DRY-RUN PREVIEW"
        print(f"\n\033[94m▶ Running SEO Title & Snippets Migration ({mode_label})...\033[0m")
        flag = "--apply" if apply_mode else "--dry-run"
        self.run_clean_step(
            f"Executing SEO snippet tool ({flag})",
            [sys.executable, "tbk-spfy-seo/ops/fix_seo_snippets.py", flag]
        )
        self.pause()

    def handle_ai_vision(self) -> None:
        print("\n\033[94m▶ Running AI Cake Genome & Vision Pipeline Tests...\033[0m")
        self.run_clean_step(
            "Executing vision pipeline test harness",
            [sys.executable, "-m", "unittest", "tbk-spfy-ai/ai/vision/python/test_vision.py"]
        )
        self.run_clean_step(
            "Validating cake taxonomy & attributes",
            [sys.executable, "-m", "unittest", "tbk-spfy-ai/ai/taxonomy/test_taxonomy.py"]
        )
        self.pause()

    def handle_build(self) -> None:
        print("\n\033[94m▶ Package Versioned Theme Build...\033[0m")
        version = input("Enter build version (e.g. 1.0.0): ").strip() or "1.0.0"
        packager_path = self.repo_root / "tools-script" / "win" / "build_packager.py"
        self.run_clean_step(
            f"Packaging build v{version.lstrip('v')}",
            [sys.executable, str(packager_path), "--version", version]
        )
        self.pause()

    def handle_release(self) -> None:
        print("\n\033[94m▶ Publish Major/Minor Release...\033[0m")
        version = input("Enter release version (e.g. 1.0): ").strip() or "1.0"
        major = input("Enter major release grouping (default: 1): ").strip() or "1"
        release_path = self.repo_root / "tools-script" / "win" / "release_manager.py"
        self.run_clean_step(
            f"Publishing release v{version.lstrip('v')} under releases/v{major}/",
            [sys.executable, str(release_path), "--version", version, "--major", major]
        )
        self.pause()

    def handle_view_log(self) -> None:
        print("\n\033[94m▶ Session Log Summary:\033[0m")
        if self.logger.session_log_path.exists():
            lines = self.logger.session_log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            for line in lines[-25:]:
                print(f"  \033[90m{line}\033[0m")
        self.pause()

    # --- Main Loop ---

    def run_menu(self) -> None:
        while True:
            self.print_banner()
            print("\033[97m[1] Storefront & Theme Operations\033[0m")
            print("    1.1  Start Local Dev Server (Live Preview on #151370334377)")
            print("    1.2  Run Theme Code Health Check (Linter)")
            print("    1.3  Deploy to Preview Theme (#151370334377)")
            print("    1.4  Deploy Single File to Live Theme (#151307485353) [Diff Protocol]")
            print()
            print("\033[97m[2] Governance & Tasks (ProjectOps v2)\033[0m")
            print("    2.1  Run 12-Point Conformance Audit")
            print("    2.2  View Project Context & Task Summary")
            print("    2.3  Manage Tasks (Start / Complete tasks)")
            print("    2.4  Create Clean Git Governance Checkpoint")
            print()
            print("\033[97m[3] Store Automation & SEO Operations\033[0m")
            print("    3.1  Run SEO Title & Snippets (Safe Dry-Run Preview)")
            print("    3.2  Apply SEO Snippet Fixes to Live Store")
            print()
            print("\033[97m[4] AI Cake Genome & Vision Pipeline\033[0m")
            print("    4.1  Run Vision & Taxonomy Test Harness")
            print()
            print("\033[97m[5] Build & Release Management\033[0m")
            print("    5.1  Package Versioned Theme Build (build/vX.Y.Z/)")
            print("    5.2  Publish Major/Minor Release (releases/v<Major>/v<Minor>/)")
            print()
            print("\033[97m[L] View Current Session Log Summary\033[0m")
            print("\033[91m[0] Exit\033[0m")
            print("─" * 72)

            if self.test_mode:
                print("Test mode enabled. Exiting menu loop.")
                break

            choice = input("\033[93mSelect option: \033[0m").strip().lower()

            if choice == "0" or choice == "exit" or choice == "q":
                print("\n\033[92mExiting The Baking Kaur Operations Hub. Goodbye!\033[0m\n")
                break
            elif choice in ("1.1", "11"):
                self.handle_theme_dev()
            elif choice in ("1.2", "12"):
                self.handle_theme_check()
            elif choice in ("1.3", "13"):
                self.handle_theme_deploy_preview()
            elif choice in ("1.4", "14"):
                file_to_deploy = input("Enter theme file relative path (e.g. sections/bk-trust-strip.liquid): ").strip()
                if file_to_deploy:
                    deploy_script = self.repo_root / "tools-script" / "win" / "theme_deploy_live.ps1"
                    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(deploy_script), "-File", file_to_deploy])
                    self.pause()
            elif choice in ("2.1", "21"):
                self.handle_pdm_audit()
            elif choice in ("2.2", "22"):
                self.handle_pdm_context()
            elif choice in ("2.3", "23"):
                self.handle_task_workflow()
            elif choice in ("2.4", "24"):
                self.handle_pdm_checkpoint()
            elif choice in ("3.1", "31"):
                self.handle_seo_ops(apply_mode=False)
            elif choice in ("3.2", "32"):
                self.handle_seo_ops(apply_mode=True)
            elif choice in ("4.1", "41"):
                self.handle_ai_vision()
            elif choice in ("5.1", "51"):
                self.handle_build()
            elif choice in ("5.2", "52"):
                self.handle_release()
            elif choice == "l":
                self.handle_view_log()
            else:
                print("\n\033[91mInvalid selection. Please choose an option from the menu.\033[0m")
                time.sleep(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="The Baking Kaur Master Operations CLI")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode without blocking prompt")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent
    cli = TBKConsoleCLI(repo_root, test_mode=args.test_mode)
    cli.run_menu()


if __name__ == "__main__":
    main()
