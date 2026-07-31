# MCP Status

Two distinct MCP integrations exist for this project — don't conflate them, they serve different
purposes.

## `claude.ai Shopify` — the store-management connector (already in use all session)

**Status: ✅ Fully working, re-verified.** Earlier in this same task, `ToolSearch` found zero
matching tools despite `claude mcp list` showing "Connected" — that was a real, observed stale-tool-
list state at the time, not a guess. It has since resolved on its own (exactly the "tool availability
can update mid-session" behavior predicted below at the time). Re-verified properly this pass: all
28 tools enumerated by name (matching the announced count exactly) and one live call
(`get-shop-info`) executed successfully, returning real, current store data. Full breakdown:
[SHOPIFY_MCP_CAPABILITIES.md](SHOPIFY_MCP_CAPABILITIES.md).

## `@shopify/dev-mcp` — Shopify's official dev-docs/schema MCP server (Task 4, newly configured)

**Status**: Installed and configured this session, **not yet connected**.

- **Verified real and official**: `npm view @shopify/dev-mcp` confirms a genuine package (v1.14.4),
  maintained by `shopify-admin`/Shopify staff, providing an MCP server for GraphQL schema search
  (Admin API, Storefront API, Functions) and Shopify dev documentation search.
- **Added to Claude Code**: `claude mcp add shopify-dev-mcp --scope local -- npx -y @shopify/dev-mcp`
  — succeeded, config written to `C:\Users\DELL\.claude.json` (project-scoped to this repo).
- **Verified the package itself works**: ran `npx -y @shopify/dev-mcp` standalone — it downloaded
  and started without a fatal error (only harmless `npm warn` peer-dependency resolution notices,
  common and non-blocking).
- **`claude mcp list` shows it as "✘ Failed to connect"** despite the above. The most likely
  explanation: stdio MCP servers are typically spawned once when a Claude Code session starts: this
  session was already running before the server was added to config, so it was never actually
  launched as a child process this session.
- **Not fabricated as working** — this is reported as configured-but-unverified-live, not "done."

## What to do to actually verify `shopify-dev-mcp` (the remaining unconfirmed item)

1. **Restart Claude Code** (start a new session/conversation in this project directory).
2. Run `claude mcp list` again — should show connected if the restart-spawns-it theory is correct
   (the same theory that turned out to explain `claude.ai Shopify`'s temporary tool-exposure gap
   above, without even needing a restart in that case).

## Documentation search / GraphQL schema / Admin API schema / Storefront API schema (Task 4 sub-items)

All of these are capabilities `@shopify/dev-mcp` provides once actually connected — **none can be
verified as working yet**, since the server hasn't successfully connected in a live session. Not
claimed as functional until confirmed after the restart above.

## Related

[ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md), [CLAUDE_CAPABILITIES.md](CLAUDE_CAPABILITIES.md),
[API_STATUS.md](API_STATUS.md), [SHOPIFY_MCP_CAPABILITIES.md](SHOPIFY_MCP_CAPABILITIES.md) (the
full 28-tool inventory and capability matrix).
