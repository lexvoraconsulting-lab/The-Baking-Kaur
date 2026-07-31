# Product Template Census (R3)

Exhaustive `templateSuffix` census of the entire catalogue — no sampling. All 1,235 products
paginated via Admin GraphQL (`sortKey: ID`, cursor pagination), tallied to completion, and the
sum cross-checked against `productsCount` (unfiltered + per-status) at both the start and end of
the pass. Continues from R2 (`ae7b7f0`); no files were removed in this phase.

**Why exhaustive, not sampled**: Shopify's product search does not support a `template_suffix:`
filter — confirmed via `search_docs_chunks` (not in the documented field list) and empirically
(a `query: "template_suffix:premium"` search silently ignores the term and returns the full
unfiltered `1235` count, rather than erroring). There is no query-side shortcut; only full
pagination gives a real count.

## Method

```graphql
query($cursor: String) {
  products(first: 250, after: $cursor, sortKey: ID) {
    edges { node { handle templateSuffix status } }
    pageInfo { hasNextPage endCursor }
  }
}
```

Paginated to `hasNextPage: false`. Running total cross-checked against `productsCount` (1,235)
and the active/draft/archived split (602/588/45, sums to 1,235) both before and after the pass —
unchanged, confirming no concurrent catalogue edits skewed the count.

## Template inventory

5 files under `templates/product*.json`:

| Template file | `templateSuffix` value | Section rendered | Nature |
|---|---|---|---|
| `templates/product.json` | `null` or `""` (empty string) | `main-product-premium-v2.liquid` | Default — **protected module**, no assignment needed |
| `templates/product.premium.json` | `"premium"` | `main-product-premium.liquid` | Alternate product-page template |
| `templates/product.hampers-template.json` | `"hampers-template"` | `main-product.liquid` | Alternate product-page template |
| `templates/product.tbk.json` | `"tbk"` | `tbk-product.liquid` | Alternate product-page template |
| `templates/product.only_config.json` | `"only_config"` | `main-quick-view` / `main-quick-add` / `product-group-media` (JSON template, not a `.liquid` section file) | **Not a product-page template** — see below |

## Usage map (exhaustive, 1,235/1,235 products)

| Template | Products using it | Count | % of catalogue |
|---|---|---|---|
| `product.json` (default: `null` + `""`) | e.g. `motu-patlu-cake-for-girls-meerut`, `classy-tuxedo-husband-birthday-cake-meerut`, ~1,226 more | **1,228** | 99.4% |
| `product.premium.json` | `motu-patlu-designer-birthday-cake-meerut` + 2 more | **3** | 0.2% |
| `product.hampers-template.json` | `h6`, `hamper14`, `hamper36` + 1 more | **4** | 0.3% |
| `product.tbk.json` | *(none)* | **0** | 0% |
| `product.only_config.json` | *(none — not assigned via `templateSuffix`, see below)* | **0** | 0% |

1,228 + 3 + 4 = 1,235. Total reconciles exactly.

## Orphan template verification (zero-usage templates, verified per the required standard)

### `product.only_config.json` — zero `templateSuffix` assignments is **expected and correct**, NOT orphaned

This is not a normal customer-facing product-page template. It is Shopify's alternate-template
mechanism for the theme's quick-view/quick-add modals:

- `sections/main-quick-view.liquid:1,5,477` and `sections/main-quick-add.liquid:1,25,104` all gate
  their modal markup on `{%- if template == 'product.only_config' -%}`.
- `layout/theme.liquid:171,186` gates head-tag behaviour the same way.
- `assets/global.min.js` fetches it via the query-string alternate-template convention
  (`view=only_config`), which Shopify resolves per-request without requiring `templateSuffix` to
  ever be set on the product record — any product can be fetched through this view on demand.

**Verified twice**: (1) the exhaustive 1,235-product pagination shows 0 assignments; (2) grepping
the theme confirms it's live and referenced by three separate files via the `view=` convention,
not the `templateSuffix` convention — the census methodology simply doesn't (and can't) detect
this usage pattern, by design. **Conclusion: KEEP. Not a cleanup candidate.**

### `product.tbk.json` / `sections/tbk-product.liquid` — zero usage, no alternate-view wiring either

**Verified twice**: (1) the exhaustive 1,235-product pagination shows 0 `templateSuffix: "tbk"`
assignments (upgrading the Phase 5 audit's ~100-product sample finding to a full-catalogue
certainty); (2) unlike `only_config`, there is no `view=tbk` or `template == 'product.tbk'` gate
anywhere in the theme — `tbk-product.liquid` is not wired into any alternate-view mechanism.

Additional reference checks:
- **Theme references**: none — not rendered by any other section/snippet/layout file.
- **Section references**: `templates/product.tbk.json` is the only file that references
  `tbk-product` as a section type (`"type": "tbk-product"`), and that template itself has zero
  live product assignments.
- **Alternate templates**: no other `product.*.json` template references `tbk-product`.
- **App references**: cannot be fully verified from this repository/API surface — installed
  Shopify apps' internal configuration is not inspectable here. Flagged as a residual caveat, not
  assumed clear.
- `sections/tbk-product.liquid`'s own header comment (line 3) reads: *"Drop this in /sections,
  then assign the template product.tbk.json to a single product."* — confirming it was built as a
  manual single-product template, and nothing in the theme, section groups, or product catalogue
  shows that assignment ever happened.

`tbk-product.liquid` is also where the fabricated "Customer Reviews"/hardcoded 5-star widget was
originally found and removed (`seo-audit/issues.yml` SEO-005/SEO-006) — it has known history as a
legacy/experimental file, consistent with this finding.

**Conclusion: SAFE TO REMOVE** (pending manual app-reference confirmation the user can perform —
not automatable from here). **Not removed in this phase** — per R3's explicit scope, this is a
census only.

## Duplicate templates

None. All 5 templates render distinct sections; `product.premium.json` and
`product.hampers-template.json` are each genuinely, if rarely, in live use (3 and 4 products
respectively) and are not candidates for consolidation without a business decision to migrate
those 7 products onto the default template.

## Cleanup recommendations

| Item | Recommendation | Blocking factor |
|---|---|---|
| `templates/product.tbk.json` + `sections/tbk-product.liquid` | Candidate for removal in a future phase (R4+) | App-reference check cannot be fully automated from this environment; recommend a manual Shopify Admin → Apps review before deletion |
| `templates/product.only_config.json` + its wiring | No action — actively used, correctly excluded from removal consideration | N/A |
| `product.premium.json`, `product.hampers-template.json` | No action — genuinely live on 3 and 4 products respectively | N/A |

No files were removed, renamed, or modified in this phase.
