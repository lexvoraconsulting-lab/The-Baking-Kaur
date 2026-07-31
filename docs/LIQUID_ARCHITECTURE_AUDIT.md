# Liquid Architecture Audit and Refactoring Plan

Generated 2026-07-31, Phase 5 (Shopify Enterprise Development). Source of truth consulted before
writing this: `business/` (canonical facts), `design/` (the real, shipped design system this audit
directly concerns), `docs/` (coding standards, architecture, prior setup docs), `seo-audit/`
(prior findings this audit builds on, doesn't repeat). **This document is an audit and a plan. No
refactoring is executed by it** — per the phase's own instruction, implementation happens one
subsystem at a time in subsequent, separately-approved passes.

Real inventory: 29 templates, 131 sections, 148 snippets, 76 assets (`ls` counts, this pass).

---

## Finding 0 (Critical, new this pass): the real design-token system is not wired into the live storefront layout — FIXED 2026-07-31 (R0)

**Status: resolved.** `render 'tbk-tokens'` and `render 'tbk-components'` were added to
`layout/theme.liquid`, deployed live, and verified (Theme Check offenses dropped by exactly the 2
`OrphanedSnippet` findings these two files previously carried; zero new errors). See
`seo-audit/audit/CHANGELOG.md`'s 2026-07-31 entry for full verification detail. The finding below is
preserved as the historical record of what was broken and why.

**This was the single most important finding in this audit.**

`snippets/tbk-tokens.liquid` (the real `--tbk-*` CSS custom-property system — colors, spacing,
typography, shadows — fully documented in `design/DESIGN_SYSTEM.md`) and
`snippets/tbk-components.liquid` (the real `.tbkx-*` component CSS — buttons, cards, grid
primitives, documented in `design/COMPONENT_LIBRARY.md`) are **only rendered by
`layout/password.liquid`** — confirmed via a direct grep across every `.liquid`/`.json` file in the
repo: the only two `{% render 'tbk-tokens' %}` / `{% render 'tbk-components' %}` calls that exist
anywhere are both in `layout/password.liquid`. **`layout/theme.liquid` — the layout that renders
every real storefront page — contains neither render call.**

This matters because live, confirmed-rendering sections depend heavily on the variables these two
snippets define: `sections/tbk-header.liquid` alone references `var(--tbk-*)` **145 times**,
`sections/site-footer.liquid` **30 times**, `sections/tbk-announcement-bar.liquid` **2 times** — all
three are real, confirmed-live sections (`header-group.json`, `footer-group.json`). With no `:root`
definition reaching the real theme layout, every one of those 177 references currently resolves to
nothing on any real storefront page — buttons, header, and footer would render with undefined
colors/spacing/shadows (browser-default fallback behavior for an unset custom property), not the
intended warm-luxury palette.

**Why this hasn't been caught yet**: the storefront is intentionally password-gated
(`business/BUSINESS_MASTER.md` §16). Anonymous visitors and most external checks this whole project
has run only ever see `layout/password.liquid` — which, by coincidence or original design intent,
*does* correctly render the tokens. A staff/theme-editor preview that bypasses the password gate
would be the first place this actually surfaces visually, and no such preview appears to have
happened this project (every prior verification pass used pull/diff-based code checks, not a visual
render, precisely because the gate blocks `WebFetch`-based visual checks too).

**This traces to a previously-logged but under-characterized finding**: `seo-audit/audit/CHANGELOG.md`'s
2026-07-30 SEO-024 entry already noted "two `render` calls (`tbk-tokens`, `tbk-components`) present
in git... were absent from the live theme, apparently abandoned/incomplete work" and states local git
was "synced to the live truth" (i.e. the render calls were *removed* from local git to match what was
missing live, not restored). That entry characterized this as low-stakes cleanup; this audit's fuller
dependency analysis (177 real references across 3 confirmed-live sections) shows it is not — it's a
sitewide styling defect currently masked only by the password gate.

**Recommended fix** (not executed this pass): add `{%- render 'tbk-tokens' -%}` and
`{%- render 'tbk-components' -%}` to `layout/theme.liquid`, in the same position/pattern already
proven correct in `layout/password.liquid`. This is purely additive — restores two render calls that
already exist and work correctly elsewhere, removes nothing, and directly fixes 177 currently-broken
variable references. Recommended as **Phase R0**, first in the refactoring order below, since every
other visual-architecture question is harder to reason about while this is unresolved.

---

## Finding 1: confirmed-dead "-hulkapps-backup" files (11 files, zero live references) — 10 REMOVED 2026-07-31 (R1)

**Status: mostly resolved.** The 10 files below with confirmed zero references were removed and
deployed live. `rewind_menu_backup_do_not_delete.liquid` and
`header-menu-bottom-hulkapps-backup.liquid` (referenced, disabled block) were explicitly excluded,
per this finding's own original recommendation — see `seo-audit/audit/CHANGELOG.md`'s 2026-07-31
entry for full verification detail, including a real, unrelated drift (`main-password.liquid`'s live
WhatsApp/Call feature) that was deliberately routed around during deployment.

Cross-checked two independent ways — a direct grep for each file's section `"type"` string across
every `*-group.json`/`templates/*.json`, and `shopify theme check`'s own `OrphanedSnippet` detector
(which independently flagged the same snippet-level files). Both agree:

| File | Kind | References found |
|---|---|---|
| `sections/cart-drawer-hulkapps-backup.liquid` | Section | 0 |
| `sections/header-e-commerce-hulkapps-backup.liquid` | Section | 0 |
| `sections/header-inline-hulkapps-backup.liquid` | Section | 0 |
| `sections/main-cart-hulkapps-backup.liquid` | Section | 0 |
| `sections/main-gift-cart-hulkapps-backup.liquid` | Section | 0 |
| `snippets/cart-checkbox-hulkapps-backup.liquid` | Snippet | 0 (theme-check `OrphanedSnippet`) |
| `snippets/cart-complementary-hulkapps-backup.liquid` | Snippet | 0 (theme-check `OrphanedSnippet`) |
| `snippets/cart-shipping-bar-hulkapps-backup.liquid` | Snippet | 0 (theme-check `OrphanedSnippet`) |
| `snippets/item-cart-hulkapps-backup.liquid` | Snippet | 0 (theme-check `OrphanedSnippet`) |
| `snippets/item-cart-page-hulkapps-backup.liquid` | Snippet | 0 (theme-check `OrphanedSnippet`) |

All 11 are real dead code by the filename's own admission ("-backup") and by both independent
detection methods. Strong candidates for removal — recommended **Phase R1**.

**One file explicitly excluded from this list**: `snippets/rewind_menu_backup_do_not_delete.liquid`
and its template `templates/page.rewind_menu_backup_do_not_delete.liquid` — the filename itself is an
explicit instruction not to remove it. Respected literally; not touched, not even proposed for
removal.

**One file requiring different treatment**: `sections/header-menu-bottom-hulkapps-backup.liquid` —
**Status: resolved 2026-07-31 (R2), decision KEEP.** Investigated fully: referenced once, as the
`header_menu_bottom_hulkapps_backup_kgkQBL` block in `header-group.json`, `disabled: true`. Not
orphaned (Theme Check confirms — only a `HardcodedRoutes` warning, no unused-code flag). Not removed:
doing so safely requires also editing the active `header-group.json`'s block/order entries, a bigger,
riskier change than a plain deletion, for a block that's already fully inert. Full evidence and the
correct future removal sequence (if ever wanted) in `seo-audit/audit/CHANGELOG.md`'s 2026-07-31 R2 entry.

## Finding 2: product template duplication — 4 real variants, uneven live usage

| Template | Section rendered | Live usage evidence this pass |
|---|---|---|
| `templates/product.json` (default, `templateSuffix: null`) | `main-product-premium-v2.liquid` | **Dominant** — 48/50 and 45/50 in two independent samples of active/mixed products (~96%); this is the confirmed default for the real 602-product active catalogue (`business/BUSINESS_MASTER.md`) |
| `templates/product.premium.json` (`templateSuffix: "premium"`) | `main-product-premium.liquid` | **Confirmed live, rare** — 1/50 in sample; real but minor usage, not obsolete |
| `templates/product.hampers-template.json` (`templateSuffix: "hampers-template"`) | `main-product.liquid` | **Confirmed live, rare** — 1/50 in sample; matches this project's prior finding of real Cake Hampers products using it |
| `templates/product.tbk.json` (`templateSuffix: "tbk"`) | `tbk-product.liquid` | **Zero occurrences across two independent 50-product samples (~100 products, ~8% of the 1,235-product catalogue)** |

`tbk-product.liquid` is a real, historically significant file — it's where the fabricated
"Customer Reviews" section and hardcoded 5-star widget were found and removed
(`seo-audit/issues.yml` SEO-005/SEO-006).

**Status: resolved 2026-07-31 (R3).** Full exhaustive census, all 1,235 products (no sampling):
`product.json` 1,228 · `product.premium.json` 3 · `product.hampers-template.json` 4 ·
`product.tbk.json` **0**. Also censused `product.only_config.json` (**0**, but confirmed to be an
intentionally-unassigned alternate quick-view/quick-add template reached via `view=` query string
— not a cleanup candidate, unlike `tbk`). `tbk-product.liquid` has zero usage and no alternate-view
wiring of any kind. Marked **SAFE TO REMOVE** pending a manual app-reference check (not
automatable from this environment) — **not removed in R3**, per that phase's audit-only scope.
Full matrix and reference-check evidence: `docs/TEMPLATE_CENSUS.md`.

## Finding 3: 23 orphaned snippets (theme-check verified), several needing content review before removal

Full list, theme-check's `OrphanedSnippet` check (never rendered by any section, template, or other
snippet):

```
snippets/product_tabs.liquid          snippets/product-btns.liquid
snippets/bk-datetime.liquid           snippets/cake-addons.liquid
snippets/choose_style.liquid          snippets/delivery-date.liquid
snippets/hdt-pr-single-rating.liquid  snippets/lookbook-card-product.liquid
snippets/meta-tags.liquid             snippets/product-form-bundle.liquid
snippets/product-form-bundle2.liquid  snippets/product-thumbnail.liquid
snippets/shine-trust.liquid           snippets/tbk-components.liquid *
snippets/tbk-tokens.liquid *          snippets/type.liquid
(+ the 5 -hulkapps-backup snippets from Finding 1, already covered there)
(+ 2 files under design_handoff_shopify_product/, a separate non-live reference folder — see Finding 5)
```

`*` — `tbk-tokens.liquid`/`tbk-components.liquid` are flagged orphaned by the same static analysis
that surfaced Finding 0 — **not actually unused, just not reachable from the live layout**. Resolving
Finding 0 (Phase R0) will make these two `OrphanedSnippet` findings disappear on their own; don't
treat them as removal candidates.

The remaining 14 real candidates split into two risk tiers:

- **Low-risk, likely genuine dead code**: `product_tabs.liquid`, `product-btns.liquid`,
  `bk-datetime.liquid`, `type.liquid`, `meta-tags.liquid`, `product-thumbnail.liquid` — generic
  utility snippets with no special sensitivity.
- **Needs content review before any removal decision**: `shine-trust.liquid` (the filename strongly
  suggests a trust-badge component — given this project's history of fabricated trust-signal content
  found in similarly-named files, this must be read and checked for fabricated claims before being
  either restored to use or removed, not blindly deleted); `hdt-pr-single-rating.liquid` (a
  single-rating display component — same category of risk, given `REVIEW_STRATEGY.md`'s governance
  applies to any rating-display code, live or not); `delivery-date.liquid` (the name suggests a real,
  wanted feature — e.g. an order delivery-date picker — that may be intentionally staged for future
  use rather than dead; check before removing); `cake-addons.liquid`, `choose_style.liquid`,
  `lookbook-card-product.liquid`, `product-form-bundle.liquid` / `-bundle2.liquid` — product-
  configuration features that may represent unfinished or paused work rather than confirmed-dead
  code.

**Status: resolved 2026-07-31 (R4).** Direct re-verification (grep, not Theme Check's label) found
this list itself was partly wrong: `product-form-bundle.liquid`, `product-form-bundle2.liquid`, and
`product_tabs.liquid` are genuinely rendered by all 3 product templates (including the default,
protected one) — reclassified **ACTIVE**, not touched. `shine-trust.liquid`, conversely, is referenced
only via a broken `{% include 'shine-trust.liquid' %}` (extension included in the name, resolves to
a non-existent path) — corroborates pre-existing `SEO_AUDIT_LEDGER.md` P2-26. No fabrication risk
found anywhere. Full classification (4 ACTIVE, 2 MANUAL REVIEW, 11 SAFE TO REMOVE, none removed):
`docs/ORPHAN_SNIPPET_AUDIT.md`.

## Finding 4: numbered-suffix variants — mixed liveness, needs individual review

| File | References found elsewhere |
|---|---|
| `sections/testimonials-2.liquid`, `sections/testimonials-3.liquid` | 0 |
| `sections/video-2.liquid` | 0 |
| `snippets/quote_2.liquid`, `snippets/quote_3.liquid` | 1 each |
| `snippets/article_loop_2.liquid` | 1 |
| `snippets/product-form-bundle2.liquid` | 3 |

`testimonials-2.liquid`/`testimonials-3.liquid` carry the same elevated risk category as
`shine-trust.liquid` above — **must be read and checked for fabricated review content before any
decision**, given this exact class of file (`sections/testimonials*.liquid`) is explicitly named as
"not confirmed live" but unaudited in `design/COMPONENT_LIBRARY.md`'s Testimonials entry, and this
project's real, documented history includes multiple independent instances of fabricated reviews
found in similarly-generic-sounding template files. **Do not delete without reading their content
first** — if they're truly empty/inert, removal is safe; if either contains fabricated
names/quotes/ratings like the four already-removed instances, that's a live finding requiring the
same treatment as SEO-005/006, not a routine cleanup. Recommended as part of **Phase R4**, prioritized
before the lower-risk items in that phase given the historical pattern.

`quote_2`/`quote_3`/`article_loop_2`/`product-form-bundle2` have at least one real reference each —
**not confirmed dead**, need a second-order liveness check (is the file that references them itself
live?) before any classification. Deferred to a later phase, not urgent.

**`testimonials-2.liquid`/`testimonials-3.liquid`/`video-2.liquid` status: resolved 2026-07-31
(R4).** Read in full — both testimonials sections carry `"disabled_on": {"groups": ["*"]}`
(a Shopify-level lockout preventing them from ever being added via the theme editor) and their
only content is generic Ecomus fashion-demo placeholder copy, never populated with real block
instances. No fabricated review/rating content found. `video-2.liquid` likewise carries the same
lockout and only a generic demo video preset. All 3 classified **SAFE TO REMOVE**, not removed
this phase. `product-form-bundle2.liquid`'s "at least one real reference" is now fully resolved:
it's rendered by all 3 product templates, reclassified **ACTIVE**. Full detail:
`docs/ORPHAN_SNIPPET_AUDIT.md`.

## Finding 5: `design_handoff_shopify_product/` is not live theme code

This directory (containing `bk-*.liquid` files referencing non-existent `assets/baking-kaur.css`/`.js`
— 6 of the 8 total `MissingAsset` findings this pass) sits outside the theme's actual root
(`sections/`, `snippets/`, `templates/`, `assets/`, `layout/`, `config/` — the directories Shopify's
theme engine actually reads). It is reference/handoff material, not live code, and its "missing
asset" references are not a real defect — those assets were never meant to exist in this repo's
context. **Out of scope for this refactoring plan entirely** — noted here only so it isn't confused
with the live theme audit above.

## Finding 6: one real, live missing-asset defect

`snippets/tbk-gallery.liquid` references `assets/no-image.svg`, which does not exist in `assets/`.
This file is used by the `tbk` product template (`product.tbk.json`) — given Finding 2's uncertainty
about that template's live status, this is low-priority until Phase R3 resolves whether `tbk-product.liquid`
is even retained. If retained, this is a small, safe fix (**Phase R6**): add the missing SVG or point
the reference at an existing placeholder asset.

## What this audit did not cover

- **`assets/` (76 files)**: not individually audited this pass beyond the one `MissingAsset` finding
  above — a dedicated asset-usage sweep (unused CSS/JS files, duplicate/superseded stylesheets) is
  its own future phase, not attempted here given the scope already covered.
- **`UndefinedObject` (43 findings) and `HardcodedRoutes` (34 findings)** from the theme-check
  baseline (`docs/setup/SHOPIFY_DEV_SETUP.md`): real, but each needs individual verification before
  being called a defect (per that file's own noted false-positive risk for some Liquid-scope checks)
  — a separately-scoped future phase, not part of this duplicate/obsolete-file audit.
- **Full 1,235-product `templateSuffix` census**: only sampled (100 products) this pass — Phase R3
  scopes the exhaustive version.

---

## Phased Refactoring Plan

Each phase is one subsystem, independently reversible, with its own verify-before/implement/theme-check/
verify-after/changelog/ledger/commit cycle when executed — none of that happens in this document.

| Phase | Scope | Risk | Business decision needed? |
|---|---|---|---|
| **R0** | Add the 2 missing render calls (`tbk-tokens`, `tbk-components`) to `layout/theme.liquid` | Very low — purely additive, restores already-proven-correct behavior | No — this is a bug fix, not a business-fact or architecture question |
| **R1** | Remove the 10 confirmed-dead `-hulkapps-backup` files (Finding 1, excluding the `do_not_delete` file and the disabled-but-referenced one) | Low — zero references found by two independent methods | No |
| **R2** | Decide the fate of `header-menu-bottom-hulkapps-backup.liquid`'s disabled block | Low technical risk; the decision itself is a judgment call, not a business fact | Recommend a quick confirm, not a hard block — this is "which of 3 reasonable options," not an unverifiable claim |
| **R3** | Exhaustive `templateSuffix` census across all 1,235 products; decide `tbk-product.liquid`'s fate based on real, complete data | Low (read-only census); removal itself (if warranted) is separately scoped after | No for the census; possibly yes for removal, depending on what it finds |
| **R4** | Content-review the 14 real orphaned-snippet candidates (Finding 3) and the 3 numbered-variant files (Finding 4), prioritizing the fabrication-risk tier first | Low for the read; low for removing confirmed-empty files | Only if fabricated content is found (same as any past SEO-00X finding) |
| **R5** | (Reserved) — any fabricated-content remediation surfaced by R4 | Depends on finding | Likely no — same removal precedent as SEO-005/006 |
| **R6** | Fix the `assets/no-image.svg` missing-asset reference | Very low | No |
| **R7** | (Future, not scoped in detail here) `UndefinedObject`/`HardcodedRoutes` triage, `assets/` audit | TBD per-item | TBD |

**Recommended starting point**: R0, given its severity (177 currently-broken variable references on
live, confirmed-rendering sections) and near-zero risk (purely additive, two-line change, restores
already-proven behavior from `password.liquid`). R1 is the next-safest, highest-confidence cleanup.

## Related

[../business/BUSINESS_MASTER.md](../business/BUSINESS_MASTER.md),
[../design/DESIGN_SYSTEM.md](../design/DESIGN_SYSTEM.md),
[../design/COMPONENT_LIBRARY.md](../design/COMPONENT_LIBRARY.md),
[setup/SHOPIFY_DEV_SETUP.md](setup/SHOPIFY_DEV_SETUP.md),
[../seo-audit/issues.yml](../seo-audit/issues.yml), [../seo-audit/audit/CHANGELOG.md](../seo-audit/audit/CHANGELOG.md),
[../REVIEW_STRATEGY.md](../REVIEW_STRATEGY.md) (governs Finding 3/4's fabrication-risk items).

---

**No code was changed by this document. Awaiting direction on which phase to begin with — R0 is
recommended, given its severity and near-zero risk, but this is presented for confirmation, not
assumed approval, consistent with this project's "stop and ask only when needed" standing practice
being applied here as "confirm the starting point," even though R0 itself needs no business-fact
approval.**
