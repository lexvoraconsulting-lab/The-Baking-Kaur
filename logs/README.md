# Session Logs Hub (`logs/`)

> Authority: [`Support/rules.md`](../Support/rules.md) · Architecture: [`Support/architecture/`](../Support/architecture/)

This directory stores session-based logs generated during operations, audits, builds, and deployments.

---

## Log Hierarchy

```
logs/
├── sessions/
│   ├── session_20260906_040000.log  # Timestamped log for a specific operations run
│   └── ...
└── latest_session.log               # Copy of the most recently generated session log
```

---

## Logging Conventions
- **Timestamped Isolation:** Every launch of the Master Operations Hub (`tbk_cli.py`) creates a unique session log file.
- **Verbose Redirection:** Subprocess output (stdout and stderr) is routed directly to the log file to keep console interactions clean and focused on high-level milestones.
- **Diagnostics:** In the event of a failure, the console points the operator directly to `logs/latest_session.log`.

