# Shopify Dev Setup

## Theme pull / push

✅ **Verified extensively working** — the exact deploy-safety cycle used throughout this project
(pull → diff → edit → push → re-pull → diff-confirm) has succeeded on every one of ~10 deploys this
session. No configuration action needed; already working.

## Theme preview (`shopify theme dev`)

⚠️ **Not used this session** — see [AI_WORKFLOW.md](AI_WORKFLOW.md)'s "real gap" section. The
command exists and is bundled with the CLI (confirmed via `shopify theme --help` listing it as a
subcommand), but hasn't actually been run. Recommended for any future visual/layout change.

## Theme linting (`shopify theme check`)

✅ **Verified working — bundled with Shopify CLI 4.5.2, no separate install needed.** Ran it for
real against this theme:

```
shopify theme check --fail-level=crash -o json
```

**Result**: 94 files scanned, 94 flagged, 1369 total offenses (1162 error-level, 207
warning-level) — **but this headline number needs real context, not alarm**:

| Check | Count | What it actually means |
|---|---|---|
| `MatchingTranslations` | **1126 (82% of all offenses)** | Locale JSON files don't all have matching keys — an incomplete-translation completeness check, not a functional bug. Dominates the raw count without being 1126 separate real problems |
| `VariableName` | 78 | Naming-convention style nit (some variables use non-standard casing, including what look like deliberately-obfuscated/generated names in `js-variables.liquid`) |
| `UndefinedObject` | 43 | **Worth reviewing** — references to a Liquid object that may not exist in that context; could be real bugs or could be theme-check not tracking a custom object's scope correctly |
| `HardcodedRoutes` | 34 | Hardcoded URL paths instead of Shopify's `routes` object — a real best-practice gap, medium priority |
| `OrphanedSnippet` | 23 | **Real, useful** — snippets that exist but are never rendered anywhere (dead code, a repo-hygiene opportunity) |
| `LiquidHTMLSyntaxError` + `UnclosedHTMLElement` | 11 + 4 = 15 | **Treat with caution** — this class of check is well-known for false positives on Liquid templates where different `{% if %}` branches open/close HTML tags in ways a static HTML parser flags, even though the actual rendered output is always valid. Given these exact files (`main-product-premium-v2.liquid`, `main-product.liquid`, etc.) have been edited and pushed successfully multiple times this session with no rendering issue observed, several of these are likely false positives, not confirmed live bugs |
| `UnusedAssign` | 10 | Dead code (assigned variable never read) — safe, easy cleanup |
| `MissingAsset` / `RemoteAsset` | 8 / 7 | Could be real broken references, or intentional external CDN usage (e.g. a font or library) flagged as "prefer local" |
| `ImgWidthAndHeight` | 4 | **Real, valuable** — missing `width`/`height` on `<img>` tags causes layout shift (CLS), a genuine Core Web Vitals finding |
| Everything else (`DuplicateRenderSnippetArguments`, `DeprecatedTag`, `DeprecatedFilter`, `UnknownFilter`, `ValidJSON`, `MissingTemplate`, `PaginationSize`, `ParserBlockingScript`, `TranslationKeyExists`) | ≤4 each | Small counts, not individually characterized here |

**This was NOT fixed this session** — verifying the tool works and characterizing its output
honestly was this task's scope; triaging and fixing 1369 findings (even after discounting the 1126
translation-only ones) is a substantial, separately-scoped body of work, not something to blindly
mass-fix as a side effect of an environment-setup task. Recommended as a genuine future audit pass,
ideally tracked the same way `seo-audit/` already tracks other findings — with each real issue
verified individually before being called a defect, not assumed from the raw linter count alone.

## Liquid Language Server (LSP)

❌ **Not installed** — no relevant VS Code extension found (`code --list-extensions` returned no
Liquid/Shopify-related results). See [PLUGIN_RECOMMENDATIONS.md](PLUGIN_RECOMMENDATIONS.md).

## Live reload

Part of `shopify theme dev` (not yet used, see above) — not independently configured.

## Related

[ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md), [AI_WORKFLOW.md](AI_WORKFLOW.md),
[PLUGIN_RECOMMENDATIONS.md](PLUGIN_RECOMMENDATIONS.md).
