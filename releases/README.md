# Releases Hub (`releases/`)

> Authority: [`Support/rules.md`](../Support/rules.md) · Architecture: [`Support/architecture/`](../Support/architecture/)

This directory contains structured major and minor releases for **The Baking Kaur**.

---

## Release Directory Structure

Releases are partitioned by Major version directories, with nested Minor version folders:

```
releases/
├── v1/                             # Major Release Series (v1)
│   ├── v1.0/                       # Minor Release 1.0
│   │   ├── the-baking-kaur-v1.0.zip# Release package
│   │   ├── RELEASE_NOTES.md        # Comprehensive changelog & highlights
│   │   └── release-manifest.json   # Integrity checksums and git commit
│   └── v1.1/                       # Minor Release 1.1
│       └── ...
└── v2/                             # Future Major Release Series
```

---

## Publishing a Release

Using the Master Operations CLI:
1. Run `.\tbk-menu.bat`
2. Select Option `5.2 (Publish Major/Minor Release)`
3. Provide version (e.g. `1.0`) and major series (`1`)

Or via direct script:
```powershell
python tools-script/win/release_manager.py --version 1.0 --major 1
```
