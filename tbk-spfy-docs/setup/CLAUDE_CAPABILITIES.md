# Claude Capabilities

What's actually been verified working this session (not assumed), per capability.

| Capability | Status | Evidence |
|---|---|---|
| Theme files (read/edit) | ✅ Verified, extensive | Dozens of edits to `sections/`, `snippets/`, `layout/theme.liquid` this project, each followed by a deploy-safety pull/diff/push/re-pull cycle |
| Product templates | ✅ Verified | `templates/product*.json`, `templates/page.contact-*.json` read and edited this session |
| Collections | ✅ Verified, working now | Real collection data fetched earlier this project (e.g. the "Cake Hampers" collection, 119 products); connector re-verified working again this pass with a live `get-shop-info` call and a full 28-tool inventory — see [SHOPIFY_MCP_CAPABILITIES.md](SHOPIFY_MCP_CAPABILITIES.md) |
| Metaobjects | ⚠️ Not used/verified this session | No metaobject was read or written in any task so far — genuinely untested, not assumed working or broken |
| Metafields | ⚠️ Not used/verified this session | Same — `CLAUDE.md` documents that the Admin API handles metafields, but no task this session actually exercised one |
| Assets (`assets/`) | ✅ Verified | `assets/base.css`, `assets/theme.css` read this session (checking a CSS class's real behavior) |
| Sections | ✅ Verified, extensive | Primary editing surface this whole project |
| Snippets | ✅ Verified, extensive | Same |
| Liquid syntax validation | ⚠️ Indirect only — no dedicated linter available | No Liquid Language Server or `theme-check` tool is installed (confirmed in [ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md)). Verification this session has been manual (reading full context around every edit, checking tag balance) plus an indirect real check: `shopify theme push` itself performs server-side validation, and every push this session succeeded without a reported Liquid error |
| Schema (`{% schema %}` JSON) validation | ⚠️ Manual, not automated | Verified via Python `json.loads` after stripping Shopify's non-standard leading comment block (`/* ... */`), not a dedicated Liquid-schema linter |
| Schema.org JSON-LD validation | ⚠️ Manual only, no external validator used | Every JSON-LD block this session was read and manually checked for structural correctness; no call was made to Google's Rich Results Test or validator.schema.org (both require a public URL, which the storefront doesn't currently have — see `seo-audit/schema/SCHEMA_VALIDATION.md`) |

## What would upgrade the "⚠️" rows to "✅"

- **Metaobjects/metafields**: exercise them in a real task — nothing to install, just untested.
- **Liquid/schema linting**: install `theme-check` (Shopify's own official linter) — see
  [PLUGIN_RECOMMENDATIONS.md](PLUGIN_RECOMMENDATIONS.md) for the concrete recommendation.
- **JSON-LD validation**: needs the storefront's password gate lifted (or a temporary test) so an
  external validator can actually fetch a real page — already tracked as blocked in
  `seo-audit/schema/SCHEMA_VALIDATION.md`.

## Related

[ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md), [MCP_STATUS.md](MCP_STATUS.md),
[SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md).
