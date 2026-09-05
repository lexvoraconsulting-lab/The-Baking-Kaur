# Environment Audit

Audited 2026-07-30, on this machine (Windows, this session's shell). Every line below is a real
command output, not assumed — where something couldn't be checked, that's stated explicitly rather
than guessed at.

## Core tools

| Tool | Status | Evidence |
|---|---|---|
| Node.js | ✅ Installed — v24.16.0 | `node --version` |
| npm | ✅ Installed — 11.13.0 | `npm --version` |
| Git | ✅ Installed — 2.54.0.windows.1 | `git --version` |
| Shopify CLI | ✅ Installed — 4.5.2 | `shopify version` |
| Claude Code | ✅ Installed — 2.1.195 | `claude --version`; matches `@anthropic-ai/claude-code@2.1.195` in global npm packages |
| VS Code | ✅ Installed — 1.130.0 (commit `1b6a188...`) | `code --version` |
| Theme Kit (legacy) | ❌ Not installed | `theme version` → command not found. Expected — Theme Kit was Shopify's pre-CLI-3 tool; Shopify CLI 4.5.2 supersedes it entirely, no functional gap |
| GitHub CLI (`gh`) | ❌ Not installed | `gh --version` → command not found |

## Global npm packages actually present

```
C:\Users\DELL\AppData\Roaming\npm
+-- @anthropic-ai/claude-code@2.1.195
`-- @shopify/cli@4.5.2
```

Nothing else is globally installed — no Liquid/theme-check tooling, no `@shopify/dev-mcp` (see
[MCP_STATUS.md](MCP_STATUS.md)), no GraphQL CLI tooling. This is the real baseline Tasks 3/6/9
build from.

## GitHub connection

Repo remote is configured and working (this session has pushed/pulled from it throughout):

```
origin  https://github.com/lexvoraconsulting-lab/The-Baking-Kaur.git (fetch)
origin  https://github.com/lexvoraconsulting-lab/The-Baking-Kaur.git (push)
```

**Not verified**: `gh auth status` — the GitHub CLI itself isn't installed, so its own auth state
can't be checked this way. Git's own push/pull access is real and already proven working this
session (multiple real commits pushed), independent of whether `gh` is ever installed — `gh` is a
convenience CLI for PRs/issues, not required for git operations themselves.

## What this audit does not cover

This documents one specific machine's state on the date above. If another developer works on this
project from a different machine, this file won't describe their environment — treat it as a
snapshot, not a live status page.

## Related

[MCP_STATUS.md](MCP_STATUS.md), [SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md).
