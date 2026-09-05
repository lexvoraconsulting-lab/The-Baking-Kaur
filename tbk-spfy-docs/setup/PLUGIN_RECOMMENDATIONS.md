# Plugin Recommendations

Deliberately short — only extensions that fill a real, verified gap for this project. No filler.

## 1. Shopify Liquid (official, publisher: Shopify)

**Why**: This project has zero Liquid tooling installed in VS Code right now (confirmed —
`code --list-extensions` returned no matches for Shopify/Liquid/theme-check). This extension
provides Liquid syntax highlighting and surfaces the exact same `theme-check` lints already
verified working via the CLI (see [SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md)) inline in the
editor, instead of only via a manual terminal run. Directly closes the "Liquid LSP: not installed"
gap from [CLAUDE_CAPABILITIES.md](CLAUDE_CAPABILITIES.md).

## 2. GraphQL (official, publisher: GraphQL Foundation)

**Why**: This project does real Admin GraphQL work (every query this session used raw GraphQL
strings, per `CLAUDE.md`'s own stated preference for GraphQL over REST). Syntax highlighting and
inline validation for `.graphql`/embedded GraphQL strings is a direct fit, not a speculative
addition.

## 3. axe Accessibility Linter (publisher: Deque Systems)

**Why**: This is a real customer-facing storefront (a bakery selling directly to consumers, not an
internal tool) — accessibility directly affects real customers, and nothing in the current toolchain
checks it. `theme-check` (already verified working) covers some structural HTML issues but not
accessibility semantics specifically.

## 4. Python (official, publisher: Microsoft)

**Why**: The `ai/` platform track (taxonomy, attribute distribution, etc.) is real, substantial
Python work with its own test pattern already established (`assert`-based `test_<module>.py`
files, deliberately no pytest/framework — see this repo's own established convention). The official
Python extension supports exactly this pattern (running a file as `python -m ai.X.test_X` from the
editor) without imposing a testing framework the project has deliberately avoided.

## Deliberately not recommended

- **Prettier** — Liquid files aren't well-supported by Prettier's formatting rules, and this
  project's established convention doesn't currently enforce automated formatting; adding it now
  would be an unrequested process change, not a gap-fill.
  ("simplify, don't over-tool" — see this project's own ponytail/YAGNI-style standing preference.)
- **A dedicated SEO extension** — no strong, focused VS Code extension exists for this; real SEO
  verification for this project already happens through the `seo-audit/` tooling and (once
  reachable) Google's own external tools (Rich Results Test, PageSpeed Insights), not an editor
  plugin.
- **A testing-framework extension** (e.g. pytest runner) — would conflict with this project's
  deliberate no-framework, `assert`-based test convention; recommending one would push an
  unrequested architecture change.

## Related

[SHOPIFY_DEV_SETUP.md](SHOPIFY_DEV_SETUP.md), [CLAUDE_CAPABILITIES.md](CLAUDE_CAPABILITIES.md).
