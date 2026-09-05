#!/usr/bin/env python3
"""
The Baking Kaur — Build Packager
Compiles versioned production artifacts into build/v<version>/ with checksums and manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path


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


def calculate_sha256(filepath: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def create_theme_zip(theme_dir: Path, output_zip: Path) -> int:
    """Zip the Shopify theme folder excluding extraneous temp files."""
    excluded_patterns = {".git", ".DS_Store", "Thumbs.db", ".shopify", "node_modules"}
    file_count = 0
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(theme_dir):
            dirs[:] = [d for d in dirs if d not in excluded_patterns]
            for file in files:
                if file in excluded_patterns or file.endswith(".tmp"):
                    continue
                file_path = Path(root) / file
                arcname = file_path.relative_to(theme_dir)
                zf.write(file_path, arcname)
                file_count += 1
    return file_count


def package_build(version: str, repo_root: Path, dry_run: bool = False) -> Path:
    """Execute the versioned build process."""
    if not version.startswith("v"):
        build_tag = f"v{version}"
    else:
        build_tag = version
        version = version.lstrip("v")

    theme_dir = repo_root / "tbk-spfy-theme"
    build_dir = repo_root / "build" / build_tag
    zip_path = build_dir / f"theme-{build_tag}.zip"
    manifest_path = build_dir / "build-manifest.json"
    checksum_path = build_dir / "checksums.sha256"

    print(f"Packaging Build [{build_tag}]...")
    if dry_run:
        print(f"  [Dry-Run] Target Directory: {build_dir}")
        print(f"  [Dry-Run] Target Zip: {zip_path}")
        return build_dir

    build_dir.mkdir(parents=True, exist_ok=True)

    # 1. Create Theme Production Zip
    print(f"  -> Archiving theme files from: {theme_dir.name}...")
    file_count = create_theme_zip(theme_dir, zip_path)
    zip_hash = calculate_sha256(zip_path)
    zip_size = zip_path.stat().st_size

    # 2. Write Checksums
    checksum_content = f"{zip_hash}  {zip_path.name}\n"
    checksum_path.write_text(checksum_content, encoding="utf-8")

    # 3. Create Manifest
    commit_sha, branch = get_git_info(repo_root)
    manifest = {
        "project": "The Baking Kaur",
        "build_version": version,
        "build_tag": build_tag,
        "created_at": datetime.now().isoformat(),
        "git": {
            "branch": branch,
            "commit": commit_sha,
        },
        "artifacts": [
            {
                "name": zip_path.name,
                "file_count": file_count,
                "size_bytes": zip_size,
                "sha256": zip_hash,
            }
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"  Build created successfully!")
    print(f"  Directory: {build_dir}")
    print(f"  Package: {zip_path.name} ({file_count} files, {zip_size / 1024:.1f} KB)")
    print(f"  SHA-256: {zip_hash[:12]}...")
    return build_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Packager for The Baking Kaur")
    parser.add_argument("--version", "-v", default="1.0.0", help="Build version (e.g. 1.0.0)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent
    package_build(args.version, repo_root, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

