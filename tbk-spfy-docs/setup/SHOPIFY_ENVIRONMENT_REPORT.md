# Shopify Environment Report — Final Summary

Audited 2026-07-30. No score below is invented — each is a qualitative band with cited evidence,
consistent with this project's standing no-fabrication practice (see `seo-audit/`).

## Installed and working

| Tool | Version | Evidence |
|---|---|---|
| Node.js | v24.16.0 | `node --version` |
| npm | 11.13.0 | `npm --version` |
| Git | 2.54.0.windows.1 | `git --version`, real commits/pushes all session |
| Shopify CLI | 4.5.2 | `shopify version`, ~10 successful theme deploys this session |
| Claude Code | 2.1.195 | `claude --version` |
| VS Code | 1.130.0 | `code --version` |
| `shopify theme check` (linter) | bundled with CLI | Ran for real — 94 files, 1369 offenses (see [SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md) for honest characterization — 82% is one low-urgency check) |

## Configured this session

- **`@shopify/dev-mcp`** — added via `claude mcp add shopify-dev-mcp --scope local -- npx -y @shopify/dev-mcp`. Package verified real and runnable; **not yet connected in a live session** (see [MCP_STATUS.md](MCP_STATUS.md) — needs a Claude Code restart to take effect).

## Missing

- **GitHub CLI (`gh`)** — not installed. Not blocking (git itself works fine for all repo operations); only needed if you want PR/issue management from the terminal instead of the GitHub web UI.
- **Theme Kit** — not installed, and not needed — fully superseded by Shopify CLI 4.5.2.
- **Liquid/Shopify/GraphQL/accessibility VS Code extensions** — none installed; see [PLUGIN_RECOMMENDATIONS.md](PLUGIN_RECOMMENDATIONS.md) for the 4 real, justified additions.
- **"Shopify AI Toolkit"** — doesn't exist as a distinct product; see [SHOPIFY_AI_TOOLKIT.md](SHOPIFY_AI_TOOLKIT.md).

## Authentication status

| System | Status |
|---|---|
| Shopify CLI → store | ✅ Working (proven by real operations; no direct `whoami` command exists in this CLI version to double-confirm) |
| `claude.ai Shopify` MCP connector | ✅ Fully working — re-verified with a live call and a full 28-tool inventory, see [SHOPIFY_MCP_CAPABILITIES.md](SHOPIFY_MCP_CAPABILITIES.md) |
| `shopify-dev-mcp` | ⚠️ Configured, not yet connected (needs session restart) |
| GitHub (git push/pull) | ✅ Working (proven all session) |
| GitHub CLI (`gh`) | ❌ Not installed, not checked |

## Blocked capabilities

- **Storefront API** — genuinely not executable through any tool in the connected MCP set (only
  validatable), confirmed via the full tool inventory.
- **Theme deployment and live-theme Liquid writes via MCP** — not available through this connector
  at all; theme deployment for this whole project has correctly gone through the Shopify CLI
  instead. Theme file writes via MCP GraphQL are further restricted to unpublished themes only.
- **Image upload from a local file** — the `upload-image` tool referenced by 4 other tools'
  descriptions doesn't actually exist in the available set; only pre-hosted HTTPS URLs work.
- REST API, webhooks — never exercised this session, not necessarily broken, just unverified either
  way.
- Any live-crawl-based verification (Rich Results Test, real Core Web Vitals) — blocked by the
  storefront's own intentional password gate, unrelated to this environment setup.

## Recommended Next Steps

1. **Restart Claude Code** (new session) — the `claude.ai Shopify` tool-exposure gap already
   resolved on its own; a restart should similarly get `shopify-dev-mcp` actually connected. Re-run
   `claude mcp list` after.
2. Install the 4 recommended VS Code extensions (Shopify Liquid, GraphQL, axe Accessibility Linter,
   Python) — see [PLUGIN_RECOMMENDATIONS.md](PLUGIN_RECOMMENDATIONS.md).
3. Triage the `theme-check` findings as its own separately-scoped pass once you're ready — start
   with `OrphanedSnippet` (23, dead code) and `ImgWidthAndHeight` (4, real CLS fix) as the
   highest-confidence, lowest-risk wins; treat `LiquidHTMLSyntaxError`/`UnclosedHTMLElement` (15
   total) with skepticism given the false-positive pattern noted in
   [SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md).
4. Consider `shopify theme dev` for any future *visual* change, per [AI_WORKFLOW.md](AI_WORKFLOW.md).

## Risk Assessment

- **Low risk**: everything configured this session (`shopify-dev-mcp` addition) is local-only,
  additive, and reversible (`claude mcp remove shopify-dev-mcp` if unwanted).
- **No credentials were requested, stored, or exposed** by this task — Shopify CLI auth was proven
  via existing successful operations, not by prompting for or inspecting a token.
- **The theme-check findings are a real but not urgent risk** — 1369 raw findings sounds alarming,
  but 82% is a single non-functional i18n-completeness check; the genuinely concerning categories
  (`UndefinedObject`, `LiquidHTMLSyntaxError`) total under 60 combined and include known
  false-positive-prone checks. Not a "your site is broken" finding — a real but calmly-scoped
  future cleanup opportunity.

## Overall Readiness

**Functional for continued development, with one known gap left to close.** Core tooling (Node,
git, Shopify CLI, Claude Code, VS Code) is fully installed and proven working through real,
successful operations all session. The `claude.ai Shopify` connector's earlier tool-exposure gap
has already resolved on its own and is now fully re-verified (28 tools enumerated, one live call
succeeded). The one remaining open item — the newly-added `shopify-dev-mcp` server showing "Failed
to connect" — plausibly resolves with a simple session restart, the same kind of issue that just
resolved for the other connector without one. Nothing in this audit blocks continued theme
development using the exact workflow already proven this session (pull → diff → edit → push →
re-pull → diff-confirm).

## Full file index

[ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md) · [SHOPIFY_AI_TOOLKIT.md](SHOPIFY_AI_TOOLKIT.md) ·
[MCP_STATUS.md](MCP_STATUS.md) · [SHOPIFY_MCP_CAPABILITIES.md](SHOPIFY_MCP_CAPABILITIES.md) ·
[CLAUDE_CAPABILITIES.md](CLAUDE_CAPABILITIES.md) ·
[SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md) · [AI_WORKFLOW.md](AI_WORKFLOW.md) ·
[API_STATUS.md](API_STATUS.md) · [PLUGIN_RECOMMENDATIONS.md](PLUGIN_RECOMMENDATIONS.md)
