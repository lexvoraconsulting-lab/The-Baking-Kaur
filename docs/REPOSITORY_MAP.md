# Repository Map

High-level structure, generated during Phase 7.0 reconciliation (2026-07-31). Complements
`docs/DOCUMENTATION_INDEX.md` (docs organized by topic) with a directory-first view.

## Live Shopify theme (what Shopify actually deploys)

```
layout/        — theme.liquid (entry point), password.liquid
templates/     — 33 JSON/liquid templates (corrected count, was misreported as 40)
sections/      — reusable page sections (includes the protected main-product-premium-v2.liquid)
snippets/      — reusable partials
assets/        — CSS/JS/SVG/images (no local product photos — all Shopify-CDN-served)
config/        — settings_schema.json, settings_data.json
locales/       — translation files
```

Deployed as theme `#151307485353` on `ae86ba-2a.myshopify.com`. Full detail: `SHOPIFY_ARCHITECTURE.md`,
`docs/SHOPIFY.md`.

## Non-live reference material (Shopify never reads these)

```
design_handoff_shopify_product/  — handoff/reference material, confirmed non-live (Finding 5,
                                    docs/LIQUID_ARCHITECTURE_AUDIT.md)
```

## Business & brand documentation

```
business/      — BUSINESS_MASTER.md, TBK_BRAND_GUIDELINES.md (canonical business/brand facts)
design/        — DESIGN_SYSTEM.md, COMPONENT_LIBRARY.md, CONTENT_SYSTEM.md, COPY_GUIDELINES.md
                 (code-verified implementation layer, companion to root blueprint docs of the
                 same names)
```

## Documentation workstreams (two separate, non-overlapping tracks — see `CANONICAL_SOURCES.md`)

```
Track 1 — Enterprise Transformation (homepage/build, Phase A→J):
  CHANGELOG.md (root)          — canonical changelog for this track
  PROJECT_ROADMAP.md
  HOMEPAGE_SPECIFICATION.md, HOMEPAGE_CONTENT_STRATEGY.md
  PERFORMANCE_BASELINE.md (root) — historical Phase-A-era baseline

Track 2 — SEO-audit & Liquid-cleanup (Sprint 1-2, Phase 4-6.5):
  seo-audit/audit/CHANGELOG.md   — canonical changelog for this track
  seo-audit/audit/AUDIT_LEDGER.md
  seo-audit/issues.yml
  docs/*.md — the large majority of docs/, see DOCUMENTATION_INDEX.md
```

## Tooling

```
seo-ops/       — Python scripts for Admin API operations (dry-run by default, --apply to commit)
.venv/         — Python virtual environment (third-party, not project code)
```

## Unrelated subsystem (not part of the Shopify/SEO work)

```
ai/            — a separate enterprise-attribute-language build program (EAL/EAR/EAD/attribute
                 distribution), with its own docs/10_Taxonomy/, docs/20_Attribute_Language/,
                 docs/40_Enterprise_Attribute_Registry/, etc. Each module has its own
                 Roadmap.md/Examples.md/Validation.md/Versioning.md by intentional per-module
                 design — not a documentation conflict with the Shopify/SEO tree, just a
                 different program sharing this repository.
```

## Reconciliation artifacts (this pass, Phase 7.0)

```
docs/CANONICAL_SOURCES.md        — which file is canonical for which topic, and why
docs/DOCUMENTATION_INDEX.md      — every doc, organized by topic
docs/REPOSITORY_MAP.md           — this file
docs/FILE_OWNERSHIP.md           — who/what owns each major doc going forward
docs/DOCUMENTATION_CHANGELOG.md  — what changed in this reconciliation pass
docs/PHASE7_READY.md             — final GO/NO-GO
```

## Related

[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md), [CANONICAL_SOURCES.md](CANONICAL_SOURCES.md),
[FILE_OWNERSHIP.md](FILE_OWNERSHIP.md), [DOCUMENTATION_CHANGELOG.md](DOCUMENTATION_CHANGELOG.md).
