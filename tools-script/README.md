# Tools and Automation Scripts (`tools-script/`)

> Authority: [`Support/rules.md`](../Support/rules.md) · Architecture: [`Support/architecture/`](../Support/architecture/)

This directory houses the developer tooling, automated runners, and the Master Menu CLI for **The Baking Kaur**.

---

## Directory Overview

```
tools-script/
├── python/                         # Centralized Python automation engines & CLI
│   ├── tbk_cli.py                  # Master interactive console operations CLI
│   ├── theme_dev_server.py         # Intelligent theme dev server controller & auto-resolver
│   ├── build_packager.py           # Compiles versioned theme packages into build/vX.Y.Z/
│   └── release_manager.py          # Publishes structured releases into releases/v<Major>/v<Minor>/
│
├── win/                            # Windows automation scripts (Batch & PowerShell)
│   ├── tbk-menu.bat                # 1-Click launcher for Windows
│   ├── theme_dev.bat / .ps1        # Dev server launcher (defaults to preview #152070258857)
│   ├── theme_check.bat / .ps1      # Theme Liquid & JSON code health check
│   ├── theme_deploy_preview.bat    # Deploy changes to Preview theme (#152070258857)
│   ├── theme_deploy_live.bat       # Guarded single-file live deploy with diff protocol (#152071602345)
│   ├── pdm_governance.bat / .ps1   # 12-point conformance audit runner
│   ├── pdm_tasks.bat / .ps1        # ProjectOps v2 task workflow runner
│   ├── seo_ops.bat / .ps1          # Shopify Admin GraphQL ops (Dry-Run & Apply)
│   ├── ai_vision.bat / .ps1        # AI Cake Genome & Vision test harness
│   ├── build_package.bat           # Theme build packager runner
│   ├── release_publish.bat         # Release publisher runner
│   └── run_tests.bat               # Pytest suite runner (233 tests)
│
└── mac/                            # macOS & Linux automation shell scripts
    ├── tbk-menu.sh                 # Master CLI launcher for macOS / Linux
    ├── theme_dev.sh                # Dev server launcher
    ├── theme_check.sh              # Theme Liquid & JSON code health check
    ├── theme_deploy_preview.sh     # Deploy changes to Preview theme (#152070258857)
    ├── theme_deploy_live.sh        # Guarded single-file live deploy with diff protocol
    ├── pdm_governance.sh           # PDM 12-point conformance audit runner
    ├── pdm_tasks.sh                # ProjectOps v2 task workflow runner
    ├── seo_ops.sh                  # SEO operations runner
    ├── ai_vision.sh                # AI Vision test harness runner
    ├── build_package.sh            # Theme build packager runner
    ├── release_publish.sh          # Release publisher runner
    └── run_tests.sh                # Pytest suite runner (233 tests)
```

---

## Quick Start: Master Operations Hub

Double-click `tbk-menu.bat` or run from PowerShell/Terminal:
```powershell
.\tbk-menu.bat
```

### Key Features
1. **Interactive Menu Loop:** Always returns to the main menu after running an action.
2. **Noise Suppression:** Raw console churn and verbose output are suppressed and routed into session logs.
3. **Layman-Friendly Progress:** Displays clear progress steps (`⏳ [1/2] Processing...` and `✔ [Success]`).
4. **Session Logging:** Every execution is recorded into `logs/sessions/session_<timestamp>.log`.

