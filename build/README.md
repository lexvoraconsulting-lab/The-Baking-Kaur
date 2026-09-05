# Versioned Builds Hub (`build/`)

> Authority: [`Support/rules.md`](../Support/rules.md) · Architecture: [`Support/architecture/`](../Support/architecture/)

This directory contains version-wise production build artifacts for **The Baking Kaur**.

---

## Build Hierarchy

Each build is compiled into its dedicated semantic version folder:
```
build/
└── v1.0.0/
    ├── theme-v1.0.0.zip        # Production-ready theme bundle
    ├── build-manifest.json     # Metadata, git commit, branch, timestamp
    └── checksums.sha256        # SHA-256 integrity digest
```

---

## Generating a Build

Using the Master Operations CLI:
1. Run `.\tbk-menu.bat`
2. Select Option `5.1 (Package Versioned Theme Build)`
3. Enter desired version number (e.g. `1.0.0`)

Or via direct script:
```powershell
python tools-script/python/release/build_packager.py --version 1.0.0
```

