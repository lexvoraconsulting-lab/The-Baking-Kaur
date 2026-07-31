# Shopify AI Toolkit

## Verified: no such product exists under this name

Checked `npm search "shopify ai toolkit"` against the real npm registry — it returned no matching
package (only unrelated results like `@reduxjs/toolkit`). There is no official Shopify product
distinctly named "Shopify AI Toolkit." Rather than fabricate an installation of something that
doesn't exist, this is reported plainly: **nothing was installed for this task**, because there is
nothing real to install under this name.

## What you likely actually mean, and where it's covered instead

The real, relevant tools for AI-assisted Shopify development are covered under their own tasks:

- **`@shopify/dev-mcp`** — Shopify's real, official MCP server for AI coding assistants (GraphQL
  schema search, dev docs search). This is Task 4's subject — see
  [MCP_STATUS.md](MCP_STATUS.md).
- **The `claude.ai Shopify` connector** — the MCP integration already connected to this session,
  providing Admin GraphQL access (products, collections, orders, theme data) directly to Claude.
  This is the actual "AI + Shopify" capability already in use throughout this project's SEO/schema
  audit work — see [MCP_STATUS.md](MCP_STATUS.md) for its current connection status.
- **Claude Code itself** (this tool) — the AI development environment already installed and in use
  (v2.1.195, confirmed in [ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md)).

Together, these three already form a working "Shopify AI toolkit" for this project — just not
under one single branded package name.

## Related

[MCP_STATUS.md](MCP_STATUS.md), [CLAUDE_CAPABILITIES.md](CLAUDE_CAPABILITIES.md).
