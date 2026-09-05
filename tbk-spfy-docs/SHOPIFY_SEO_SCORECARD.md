# Shopify SEO Scorecard (Phase 7.2)

> **Update (Phase 7.4, 2026-07-31): the 1/5 meta-description row below is fixed and live** — 0
> remaining duplicate groups across all 602 active products. Scores here reflect the pre-fix state;
> see `seo-audit/audit/CHANGELOG.md` (Phase 7.4 entry).

| Dimension | Score (1–5) | Evidence |
|---|---|---|
| Product title uniqueness | 5/5 | 0 duplicate groups across all 602 active products, verified exhaustively |
| Product title format compliance | 5/5 | 100% match the documented `"{Name} - Eggless \| Meerut"` / `"{Name} \| Meerut"` convention |
| **Product meta-description uniqueness** | **1/5** | **83.8% of the 500 products exactly checked share a duplicate description with at least one other product** (419/500); the pattern continues into the unchecked remainder. The single most severe finding in this entire program. |
| Page-level SEO metadata completeness | 3/5 | 2 of 5 gap pages fixed with real content; 3 have no real content to derive from (not fabricated) |
| Collection-level SEO metadata completeness | 4/5 | 32 of 36 collections fully complete; 4 are low-traffic system/thin collections with no real content to derive from |
| Canonical / robots / sitemap / pagination architecture | 5/5 | Carried forward from Phase 7.1 — no new issues found |
| Redirect hygiene | 5/5 | Carried forward from Phase 7.1 (25 chains fixed, verified) |
| Heading hierarchy | 4/5 | Carried forward from Phase 7.1 — product/collection clean, homepage duplicate H1 known and unresolved (different workstream) |
| 404 / search / tag-page handling | 4/5 | Native Shopify defaults correctly in use; live behavior unverifiable (password gate) |
| **Overall Shopify SEO Readiness** | **2.8/5** | Dragged down almost entirely by the meta-description duplication finding — every other dimension scores 4–5/5. This is a single, well-understood, well-evidenced problem with a clear (but business-gated) fix path, not a diffuse set of small issues. |

## Why the overall score is this low despite most dimensions scoring well

A single defect affecting 84% of the active catalogue's meta descriptions is not a minor deduction
— duplicate meta descriptions at this scale is a well-documented Google Search Console "Duplicate,
Google chose different canonical than user" / "Duplicate without user-selected canonical" risk
factor across hundreds of URLs simultaneously. The score reflects severity × scope, not a simple
average across dimensions.

## What moves this score fastest

Approving and executing the description-formula fix recommended in `docs/SHOPIFY_SEO_REPORT.md`
(incorporate the product name into the description template, mirroring the already-proven title
formula) would likely move the meta-description dimension from 1/5 toward 5/5 and the overall
score from 2.8/5 to approximately 4.5/5+ — the single highest-leverage fix identified in this
entire Phase 6–7.2 program.

## Related

[SHOPIFY_SEO_REPORT.md](SHOPIFY_SEO_REPORT.md), [TECHNICAL_SEO_SCORECARD.md](TECHNICAL_SEO_SCORECARD.md).
