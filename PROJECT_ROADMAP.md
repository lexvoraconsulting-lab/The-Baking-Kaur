# PROJECT_ROADMAP.md — The Baking Kaur

Enterprise Shopify transformation roadmap. Status as of v1.0 (2026-07-14). Governed by the value gate in the flagship operating standard; every phase paused for approval, validated on preview before live.

## Legend
✅ done · 🔵 validated on preview (pending live promote) · ⏳ planned · 🔒 protected (no change)

## Planning track (complete)
| Deliverable | Status |
|---|---|
| Phase-1 Audit · Master Plan · Design Foundation · Operating Standard | ✅ |
| Information Architecture (5-yr) · Collection Audit | ✅ |
| Homepage Specification · Content Strategy | ✅ |
| Documentation library (20 docs) | ✅ |

## Implementation phases
| Phase | Name | Scope | Status |
|---|---|---|---|
| **A** | Production Safety | Schema dedup, dead-code removal, **footer restore + refine**, living docs | 🔵 preview-validated, pending promote |
| **A.1** | Collection Audit actions | Fix/redirect/merge 8 empty collections | ⏳ pending approval |
| **B** | Design Foundation | Extend `tbk-tokens` (type scale, spacing), buttons/cards/forms/icons/motion | ⏳ |
| **C** | Homepage | Build 9 sections per spec, section-by-section | ⏳ |
| **D** | Collections | Hero, filters, sorting, buying guides, SEO/GEO, premium cards | ⏳ |
| **E** | Navigation | One header, mega menu, predictive search, enterprise footer | ⏳ |
| **F** | SEO + GEO | Schema completion, entity linking, FAQ page-scope, titles/meta | ⏳ |
| **G** | Missing Pages | Local/delivery landings, guides, reviews, trust, help center | ⏳ |
| **H** | Performance | Lighthouse 95+, LCP<2s, CLS<0.1, INP; fonts/CSS/JS, app-script audit | ⏳ |
| **I** | Accessibility | WCAG 2.2 AA | ⏳ |
| **J** | Analytics | GA4, Meta, Clarity, WhatsApp tracking, enhanced ecommerce | ⏳ |
| **K** | Final QA | Cross-device, schema, CWV, regression, sign-off | ⏳ |
| — | **Product Page** | 🔒 protected — schema/analytics/perf-invisible only | 🔒 |

## Cross-cutting
- Every phase runs `QA_CHECKLIST.md` before promotion; `CHANGELOG.md` records file · reason · impact · rollback.
- Deploy model: preview theme → validate → promote to live (scoped pushes).
- Content from `HOMEPAGE_CONTENT_STRATEGY.md`; visuals from `DESIGN_SYSTEM.md` / `COMPONENT_LIBRARY.md`; schema from `SCHEMA_MASTER.md`.


## Backlog

### 🎯 Flagship Hero Photoshoot  *(raised 2026-07-15 · blocks: canonical homepage hero)*
The current homepage hero is a **Temporary Production Hero** — `Classic Strawberry Whipped Cream Cake` (product `b32`), chosen because **no compliant designer-cake asset exists**: every designer/theme/wedding shot in the catalogue carries customer names, printed messages, monograms, third-party branding (a `zomato` watermark, a `TWC` easel) or green outdoor backgrounds.

**Required final asset:**
- Exclusive **designer** cake (signature showpiece)
- **No text on cake** · no customer names · no watermark
- **White luxury background**, studio lighting
- **Landscape + portrait** versions (desktop 3:2 + mobile 4:5 crops)
- **High-resolution master** (≥3000px on the long edge)
- Becomes the **canonical homepage hero**

**Swap cost: zero code.** Theme editor → *Home · Editorial Hero* → upload to **"Flagship Hero master"**. The uploaded Files image always takes precedence over the temporary product source.

**Related cleanup (same shoot/decision):** remove the `zomato`-watermarked product image, the `TWC`-branded frame, and decide policy on customer names printed across catalogue photography.

## Immediate next decisions (owner: client)
1. Promote Phase A to live.
2. Approve Collection Audit dispositions.
3. Kick off Phase B (design tokens) — the unlock for C/D/E.
