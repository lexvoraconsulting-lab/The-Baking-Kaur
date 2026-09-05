#!/usr/bin/env python3
"""
The Baking Kaur — Release Manager
Promotes builds into structured releases/v<Major>/v<Major>.<Minor>/ with Release Notes and Manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def calculate_sha256(filepath: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_git_info(repo_root: Path) -> tuple[str, str]:
    """Retrieve current commit SHA and branch name."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(repo_root), stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        commit = "unknown"

    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(repo_root), stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        branch = "unknown"

    return commit, branch


def create_release(
    version: str,
    repo_root: Path,
    major: str | None = None,
    dry_run: bool = False,
    notes: str | None = None,
) -> Path:
    """Publish a structured release."""
    clean_ver = version.lstrip("v")
    parts = clean_ver.split(".")
    major_num = major if major else (parts[0] if len(parts) > 0 else "1")
    minor_tag = f"v{parts[0]}.{parts[1]}" if len(parts) >= 2 else f"v{clean_ver}"
    major_folder = f"v{major_num}"

    release_dir = repo_root / "releases" / major_folder / minor_tag
    build_dir = repo_root / "build" / f"v{clean_ver}"
    release_zip = release_dir / f"the-baking-kaur-{minor_tag}.zip"
    manifest_path = release_dir / "release-manifest.json"
    notes_path = release_dir / "RELEASE_NOTES.md"

    print(f"[*] Publishing Release [{minor_tag}] (Major: {major_folder})...")
    if dry_run:
        print(f"  [Dry-Run] Target Directory: {release_dir}")
        print(f"  [Dry-Run] Target Zip: {release_zip}")
        return release_dir

    release_dir.mkdir(parents=True, exist_ok=True)

    # 1. Obtain or compile archive
    theme_zip = build_dir / f"theme-v{clean_ver}.zip"
    if theme_zip.exists():
        print(f"  → Promoting pre-existing build artifact from: {build_dir.name}")
        shutil.copy2(theme_zip, release_zip)
    else:
        print(f"  → Packaging live theme into release archive...")
        # Import and run build_packager
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from build_packager import create_theme_zip
        theme_dir = repo_root / "tbk-spfy-theme"
        create_theme_zip(theme_dir, release_zip)

    zip_hash = calculate_sha256(release_zip)
    zip_size = release_zip.stat().st_size
    commit_sha, branch = get_git_info(repo_root)

    # 2. Generate Release Notes
    release_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    custom_notes = notes or (
        "### Key Highlights\n"
        "- Initial consolidated enterprise release of The Baking Kaur Shopify platform.\n"
        "- Standardized Design Tokens & Typography (Cormorant Garamond + Manrope).\n"
        "- ProjectOps v2 Governance & Living Architecture suite fully synchronized.\n"
        "- Local Delivery Slot & Trust frameworks staged for deployment."
    )

    release_notes_content = f"""# The Baking Kaur — Release {minor_tag}

> **Release Version:** `{minor_tag}` (Major: `{major_folder}`)  
> **Release Date:** {release_date}  
> **Git Commit:** `{commit_sha}` on branch `{branch}`  
> **Archive:** `{release_zip.name}` ({zip_size / 1024:.1f} KB)  
> **SHA-256:** `{zip_hash}`  

---

## Overview

{custom_notes}

---

## Artifact Integrity

| File | Size | SHA-256 Checksum |
| :--- | :--- | :--- |
| `{release_zip.name}` | {zip_size / 1024:.1f} KB | `{zip_hash}` |

---

## Verification & Deployment
To verify and deploy this release:
1. Validate checksum: `Get-FileHash {release_zip.name} -Algorithm SHA256`
2. Deploy to Preview Theme: `shopify theme push --store ae86ba-2a.myshopify.com --theme 151370334377`
"""
    notes_path.write_text(release_notes_content, encoding="utf-8")

    # 3. Create Release Manifest
    manifest = {
        "project": "The Baking Kaur",
        "release_version": clean_ver,
        "release_tag": minor_tag,
        "major_version": major_folder,
        "released_at": datetime.now().isoformat(),
        "git": {
            "branch": branch,
            "commit": commit_sha,
        },
        "artifacts": [
            {
                "name": release_zip.name,
                "size_bytes": zip_size,
                "sha256": zip_hash,
            }
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"  [OK] Release published successfully!")
    print(f"  [DIR] Location: {release_dir}")
    print(f"  [PKG] Package: {release_zip.name}")
    print(f"  [DOC] Notes: {notes_path.name}")
    return release_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Release Manager for The Baking Kaur")
    parser.add_argument("--version", "-v", default="1.0", help="Release version (e.g. 1.0)")
    parser.add_argument("--major", "-m", default="1", help="Major release grouping (e.g. 1)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate release")
    parser.add_argument("--notes", help="Custom release notes summary")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent
    create_release(args.version, repo_root, major=args.major, dry_run=args.dry_run, notes=args.notes)


if __name__ == "__main__":
    main()
