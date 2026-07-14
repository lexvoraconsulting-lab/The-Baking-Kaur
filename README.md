# The Baking Kaur — Enterprise Shopify Blueprint

This archive is the complete planning & standards documentation for transforming **The Baking Kaur** (a 100% eggless luxury cake studio in Meerut) into a premium Shopify digital flagship. **Documentation only — no theme code.**

Guiding rules across all documents: preserve brand colors & logo; the **product page is a protected module** (no visual/UX/flow change); every change must pass the value gate (improves UX / trust / conversion / SEO / GEO / accessibility / performance / maintainability / scalability).

---

## Document purpose
| Document | Purpose |
|---|---|
| `VERSION.md` | Version, date, completed & pending milestones |
| `PROJECT_ROADMAP.md` | All phases with status; next decisions |
| `TABLE_OF_CONTENTS.md` | Linked index of every document |
| `SHOPIFY_ARCHITECTURE.md` | The current theme's technical architecture (stack, folders, apps, debt) |
| `DESIGN_SYSTEM.md` | Design tokens — color, typography, spacing, shadow, radius, motion |
| `COMPONENT_LIBRARY.md` | Per-component specs, variants, states, accessibility |
| `ANIMATION_GUIDELINES.md` | Motion system — allowed/forbidden, easing, reduced-motion |
| `BRAND_VOICE.md` | Voice, tone, personality |
| `COPY_GUIDELINES.md` | Copy mechanics — grammar, keywords, CTAs, microcopy |
| `INFORMATION_ARCHITECTURE.md` | 5-year IA — URLs, hierarchy, clusters, entities, expansion |
| `SEO_GEO_MASTER_PLAN.md` | SEO/GEO strategy, internal linking, local SEO, content roadmap |
| `SCHEMA_MASTER.md` | Canonical structured-data reference (entity graph, per-template) |
| `MERCHANDISING_GUIDE.md` | What products/collections appear where, and how |
| `CONTENT_SYSTEM.md` | Content model — metaobjects & metafields |
| `HOMEPAGE_SPECIFICATION.md` | Homepage structure & behavior (implementation-ready) |
| `HOMEPAGE_CONTENT_STRATEGY.md` | Homepage copy, trust, local-SEO, content hierarchy |
| `QA_CHECKLIST.md` | Per-phase pre-promotion quality gate |
| `PERFORMANCE_BASELINE.md` | Baseline metrics + Phase-H targets |
| `CHANGELOG.md` | Every file change, reason, and rollback |

## Recommended reading order
1. **Orient:** `README` → `TABLE_OF_CONTENTS` → `VERSION` → `PROJECT_ROADMAP`
2. **Understand the system:** `SHOPIFY_ARCHITECTURE`
3. **Standards:** `DESIGN_SYSTEM` → `COMPONENT_LIBRARY` → `ANIMATION_GUIDELINES`; then `BRAND_VOICE` → `COPY_GUIDELINES`
4. **Strategy:** `INFORMATION_ARCHITECTURE` → `SEO_GEO_MASTER_PLAN` → `SCHEMA_MASTER` → `MERCHANDISING_GUIDE` → `CONTENT_SYSTEM`
5. **Build target:** `HOMEPAGE_SPECIFICATION` → `HOMEPAGE_CONTENT_STRATEGY`
6. **Operate:** `QA_CHECKLIST` · `PERFORMANCE_BASELINE` · `CHANGELOG`

## Document dependencies
```
INFORMATION_ARCHITECTURE ─┬─▶ SEO_GEO_MASTER_PLAN ─▶ SCHEMA_MASTER
                          └─▶ MERCHANDISING_GUIDE
DESIGN_SYSTEM ─▶ COMPONENT_LIBRARY ─▶ ANIMATION_GUIDELINES
BRAND_VOICE ─▶ COPY_GUIDELINES ─▶ HOMEPAGE_CONTENT_STRATEGY
CONTENT_SYSTEM ─▶ HOMEPAGE_SPECIFICATION
HOMEPAGE_SPECIFICATION ─▶ (references) CONTENT_STRATEGY · COMPONENT_LIBRARY · SCHEMA_MASTER · CONTENT_SYSTEM · ANIMATION_GUIDELINES · PERFORMANCE_BASELINE
QA_CHECKLIST + CHANGELOG ─▶ apply to every phase
SHOPIFY_ARCHITECTURE + PERFORMANCE_BASELINE ─▶ current-state inputs
```

## Status
v1.0 — planning complete; implementation pending client approval. See `VERSION.md` / `PROJECT_ROADMAP.md`.
