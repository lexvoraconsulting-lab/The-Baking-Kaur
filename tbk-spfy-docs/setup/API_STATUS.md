# API Status

Covers Task 2 (Shopify authentication) and Task 8 (API verification) together — they're the same
underlying checks.

## Shopify CLI authentication

✅ **Functionally proven working** — every `shopify theme pull`/`push` command this session
succeeded against the live theme (`151307485353` on `ae86ba-2a.myshopify.com`) with no login
prompt encountered, meaning valid credentials are already cached by the CLI.

⚠️ **Not verified via a direct "whoami" command** — this CLI version (4.5.2) has no
`auth whoami`/`auth status` subcommand (`shopify auth --help` lists only `login` and `logout`).
The token's storage location wasn't located either (checked `.shopify/` locally and
`~/.config/shopify` — neither exists; likely stored via the OS credential manager or a different
internal path). This doesn't affect the "is it working" answer above, which is proven by actual
successful operations, not inferred.

## Store / theme access

✅ **Verified** — proven by every real pull/push this session, plus real product/collection data
fetched earlier via the `claude.ai Shopify` connector (before it stopped exposing tools to this
conversation — see [MCP_STATUS.md](MCP_STATUS.md)).

## Store permissions

⚠️ **Not exhaustively checked** — no formal "list granted scopes" call was made. Inferred from what
has actually worked: theme read/write, product read, collection read. Product/collection *write*
scopes were never exercised this session (no product or collection was ever edited via Admin API —
only theme files were edited), so write-permission status for those specifically is unconfirmed,
not assumed granted.

## GraphQL Admin API

✅ **Working, re-verified.** Real queries succeeded earlier this session (shop info, collection/
product lookups, status counts); the connector briefly stopped exposing tools to this conversation
mid-session (a stale-tool-list issue, not a server problem), and has since resolved on its own —
re-confirmed with a fresh live call and a full 28-tool inventory, see
[SHOPIFY_MCP_CAPABILITIES.md](SHOPIFY_MCP_CAPABILITIES.md).

## Storefront API

❌ **Not executable through the connected MCP tool set at all** — confirmed via the full tool
inventory in [SHOPIFY_MCP_CAPABILITIES.md](SHOPIFY_MCP_CAPABILITIES.md): `validate_graphql_codeblocks`
can syntax-check a Storefront API operation, but no tool actually executes one (no Storefront-API
equivalent of `graphql_query` exists in this set). All storefront-facing checks this session went
through `WebFetch` against real page URLs instead (blocked by the password gate).

## REST API compatibility

❌ **Never tested this session.** All Admin API work this session used GraphQL exclusively (per
`CLAUDE.md`'s own stated preference — "Admin GraphQL API — for data"). Shopify's REST Admin API
still exists for many resources but wasn't exercised.

## Webhooks

❌ **Not configured, not tested.** No webhook subscription was created or inspected this session.

## Related

[MCP_STATUS.md](MCP_STATUS.md), [ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md).
