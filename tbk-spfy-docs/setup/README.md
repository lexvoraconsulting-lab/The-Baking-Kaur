# Development Environment Setup — Index

This directory documents the development environment and tooling for **The Baking Kaur** project:
what's installed, what's verified working, what's configured but unconfirmed, and what's
recommended. Everything here was written from real, checked evidence (command output, actual tool
calls) — not assumed — consistent with this project's standing no-fabrication practice (see
`seo-audit/`). Moved here from the former `setup/` directory (2026-07-30) as permanent project
documentation, alongside the rest of `docs/`.

**Read this as a snapshot with a shelf life.** Several files record a specific tool's connection
status or a specific machine's installed-software state as of the date they were written — that
status can and will change (a connector reconnects, a package gets installed). Treat "✅ verified" as
"verified as of the date in that file," and re-check before relying on a status claim in a new
session if it matters.

## File index

| File | Purpose |
|---|---|
| **[ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md)** | Baseline: what's installed on this machine (Node, npm, Git, Shopify CLI, Claude Code, VS Code), with real version numbers and command evidence. Start here for "what do we have." |
| **[SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md)** | Shopify-specific tooling: theme pull/push (the deploy-safety cycle this project uses for every theme change), `shopify theme dev` (local preview, not yet used), and `shopify theme check` (the bundled linter) — including an honest breakdown of its ~1,369-finding baseline so raw counts aren't mistaken for a crisis. |
| **[MCP_STATUS.md](MCP_STATUS.md)** | Connection status of the two distinct MCP integrations this project uses: the `claude.ai Shopify` store-management connector (in active use) and `@shopify/dev-mcp` (Shopify's official dev-docs/schema server, configured but not yet confirmed connected). Don't conflate the two. |
| **[SHOPIFY_MCP_CAPABILITIES.md](SHOPIFY_MCP_CAPABILITIES.md)** | The full, real tool-by-tool inventory (28 tools) of the `claude.ai Shopify` connector — what each does, read vs. write, and a documented real gap (`upload-image` doesn't actually exist despite being referenced by other tools' descriptions). The capability reference for that connector. |
| **[API_STATUS.md](API_STATUS.md)** | Cross-cutting API/auth status: Shopify CLI auth, store/theme access, Admin GraphQL, Storefront API (not executable through this project's tool set), REST API and webhooks (untested, not necessarily broken). |
| **[CLAUDE_CAPABILITIES.md](CLAUDE_CAPABILITIES.md)** | What Claude has actually done and verified in this repo, per capability (theme files, product templates, collections, metafields/metaobjects — untested, assets, sections/snippets, Liquid/schema/JSON-LD validation methods). Distinguishes proven-by-real-use from untested. |
| **[AI_WORKFLOW.md](AI_WORKFLOW.md)** | The recommended development loop for this project (VS Code → Claude Code → Shopify CLI → GitHub → Production), based on what's actually been proven working, plus one real, named gap: no local preview (`shopify theme dev`) has been used yet — recommended for any future visual change. |
| **[SHOPIFY_AI_TOOLKIT.md](SHOPIFY_AI_TOOLKIT.md)** | Short clarification: "Shopify AI Toolkit" isn't a real, distinctly-named product — this file points to the three real components (`@shopify/dev-mcp`, the `claude.ai Shopify` connector, Claude Code itself) that together cover what that name might imply. |
| **[PLUGIN_RECOMMENDATIONS.md](PLUGIN_RECOMMENDATIONS.md)** | Four specific, justified VS Code extension recommendations (Shopify Liquid, GraphQL, axe Accessibility Linter, Python) — each tied to a real, verified gap, not a generic best-practices list. Also documents what was deliberately *not* recommended and why (Prettier, a testing-framework extension, a dedicated SEO extension). |
| **[SHOPIFY_ENVIRONMENT_REPORT.md](SHOPIFY_ENVIRONMENT_REPORT.md)** | The roll-up summary tying every file above together: installed/working, configured-but-unconfirmed, missing, authentication status, blocked capabilities, recommended next steps, and an overall readiness assessment. Read this if you only have time for one file. |

## Suggested reading order

1. `SHOPIFY_ENVIRONMENT_REPORT.md` — the summary, links back into everything else.
2. `ENVIRONMENT_AUDIT.md` — the raw baseline it's built from.
3. Whichever specific file matches what you're trying to do (deploy a theme →
   `SHOPIFY_DEV_SETUP.md`; use the Shopify MCP connector → `SHOPIFY_MCP_CAPABILITIES.md`; set up your
   editor → `PLUGIN_RECOMMENDATIONS.md`).

## Related

[../CODING_STANDARDS.md](../CODING_STANDARDS.md), [../ARCHITECTURE.md](../ARCHITECTURE.md),
[../../CLAUDE.md](../../CLAUDE.md).
