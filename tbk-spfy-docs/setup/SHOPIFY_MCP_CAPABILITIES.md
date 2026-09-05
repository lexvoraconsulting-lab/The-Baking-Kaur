# Shopify MCP Capabilities

Covers only the connected `claude.ai Shopify` MCP server (`https://setup.shopify.com/mcp`), per
your instruction. The locally-configured `shopify-dev-mcp` (still failed, see
[MCP_STATUS.md](MCP_STATUS.md)) is explicitly out of scope here.

**Authentication: ✅ Complete.** Proven by a real test call performed for this report (see
"Live Test" below), not assumed from the "Connected" status alone.

## Complete tool inventory (28 tools — verified against the announced count)

| Tool | Description | Operations |
|---|---|---|
| `get-shop-info` | Store name/domain/email/plan/currency/timezone/country | Read |
| `search-products` | Search/browse the product catalogue | Read |
| `get-product` | Full detail for one product by GID | Read |
| `create-product` | Create a new product (title, variants, images, status) | Write |
| `update-product` | Edit title/description/status/images/variant price/options | Write |
| `bulk-update-product-status` | Set ACTIVE/DRAFT/ARCHIVED across many products or a whole collection | Write |
| `get-inventory-levels` | Stock per variant per location | Read |
| `set-inventory` | Set available quantity at a location (with optimistic-lock `compareQuantity`) | Write |
| `search_collections` | Search/browse collections | Read |
| `get-collection` | Full detail for one collection by GID | Read |
| `create-collection` | Create manual or smart (rule-based) collection | Write |
| `update-collection` | Edit title/description/image/sort/rules | Write |
| `add-to-collection` | Add products to an existing collection | Write |
| `list-orders` | Recent orders, totals, fulfillment/financial status | Read |
| `get-order` | Full detail for one order by GID or order number | Read |
| `list-customers` | Customer list/search (name, email, tags, order recency, etc.) | Read |
| `create-discount` | Percentage-off discount code, scoped to collection/segment/minimum | Write |
| `run-analytics-query` | ShopifyQL analytics (sales, sessions, conversion, inventory, customers) | Read |
| `graphql_query` | Arbitrary read-only Admin API GraphQL — covers anything without a dedicated tool | Read |
| `graphql_mutation` | Arbitrary Admin API GraphQL mutation — same, for writes | Write (some mutations blocked, see below) |
| `graphql_schema` | Introspect the Admin GraphQL schema (types/fields/mutations) | Read (schema only) |
| `validate_graphql_codeblocks` | Validate a GraphQL operation against a schema before running it | Read (validation only) |
| `search_docs_chunks` | Search shopify.dev documentation | Read (docs, not store data) |
| `switch-shop` | Revoke current store token, prompt auth for a different store | Auth action |
| `get-new-store-previews` | Generate brand-new store design previews (not for editing existing stores) | Write (new store only) |
| `find-sample-product` | Suggest sample products for a new store, by category | Read (suggestions, not store data) |
| `claim-storefront-preview` | Internal — claims a generated preview as a new store (widget-only, never called directly) | Write (new store only) |
| `get-storefront-generation` | Poll status of a preview generation job | Read |

## Real gap found: `upload-image` doesn't exist

Four tools (`create-product`, `update-product`, `create-collection`, `update-collection`)
explicitly instruct: *"call the upload-image tool FIRST"* when you only have a local file or
generated image. **This tool does not exist in the available set** — checked directly via an
exact-name lookup, zero matches. Practical consequence: any image passed to those four tools must
already be a public HTTPS URL; there is currently no path from a local file to a usable one through
this MCP connector alone.

## Capability access matrix

| Capability | Access | Which tools / how |
|---|---|---|
| **Theme files** | ⚠️ Partial, and restricted | Only via generic `graphql_query`/`graphql_mutation` (no dedicated theme tool exists here at all — theme work this whole project has gone through the separate Shopify CLI instead, never this MCP). `graphql_mutation`'s own description states theme file writes (`themeFilesCopy`, `themeFilesUpsert`) are **allowed only on unpublished themes** — writes targeting the live/MAIN theme are explicitly blocked through this path |
| **Liquid** | ⚠️ Same as Theme files | Liquid source is theme file content — same read/write-to-unpublished-only restriction |
| **Products** | ✅ Full | Dedicated tools for search/read/create/update/bulk-status/inventory, plus generic GraphQL for anything uncovered |
| **Collections** | ✅ Full | Dedicated tools for search/read/create/update/add-product, plus generic GraphQL |
| **GraphQL** | ✅ Full (Admin API only) | `graphql_query`, `graphql_mutation`, `graphql_schema`, `validate_graphql_codeblocks` |
| **Admin API** | ✅ Full | This entire tool set *is* the Admin API — every tool above is a wrapper or direct passthrough to it |
| **Storefront API** | ❌ Not executable, only validatable | `validate_graphql_codeblocks` accepts `storefront-graphql` as a validation target (syntax-checks an operation), but no tool actually *executes* a Storefront API query — there is no equivalent of `graphql_query` for the Storefront API in this set |
| **Metafields** | ✅ Via generic GraphQL only | No dedicated tool; `graphql_query`/`graphql_mutation`'s own descriptions explicitly name metafields as something to reach via generic GraphQL |
| **Metaobjects** | ✅ Via generic GraphQL only | Same |
| **Files** (Shopify's Files/uploaded-assets resource) | ⚠️ Partial | No dedicated tool (and the referenced `upload-image` tool doesn't exist, see above); reachable in principle via generic GraphQL for anything already hosted at a public URL |
| **Theme deployment** | ❌ Not available here at all | No tool in this set deploys/publishes a theme. This project's actual theme deployment has used the Shopify CLI directly all session (`shopify theme push --allow-live`), a completely separate path from this MCP connector |

## Live Test (real, performed for this report)

```
get-shop-info → {"name":"The Baking Kaur","domain":"thebakingkaur.com",
"email":"thebakingkaur@gmail.com","planName":"Basic","currencyCode":"INR",
"timezone":"IST","country":"India","criticalUserMessage":""}
```

**Result: success.** Confirms authentication is complete, the Admin API is reachable, and the
returned data matches what this connector returned earlier in this same project (same store,
same domain) — a real, reproducible result, not a one-off fluke or a fabricated example.

## Related

[MCP_STATUS.md](MCP_STATUS.md), [API_STATUS.md](API_STATUS.md),
[CLAUDE_CAPABILITIES.md](CLAUDE_CAPABILITIES.md).
