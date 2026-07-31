# Generative Engine Optimization (GEO) Readiness — Architecture Only

Generated 2026-07-31 (Phase 6). Architecture-only assessment — **no SEO/GEO content was changed**.
GEO concerns whether a page's content and entities are structured so generative AI systems (Google
AI Overviews, ChatGPT browsing, Gemini, Perplexity, Copilot) can accurately understand, summarize,
and cite the business — broader than AEO's literal-answer focus.

## Entity architecture — evidence

| Signal | Status | Evidence |
|---|---|---|
| Organization/LocalBusiness entity, single source of truth | ✅ Confirmed | `snippets/bk-local-business.liquid` — this project's own prior work (B3, R-series) already unified address/geo across 5 theme files to eliminate conflicting entity data (`seo-audit/audit/CHANGELOG.md`, 2026-07-30 B3 entry) |
| WebSite entity schema | ✅ Present | `snippets/tbk-schema-website.liquid`, rendered from `layout/theme.liquid` |
| No duplicate/conflicting Organization schema | ✅ Confirmed | `structured-data.liquid`'s own design explicitly avoids emitting the same entity twice per URL (see `AEO_READINESS.md`) |
| Consistent NAP (Name/Address/Phone) | ✅ Established | Prior project work (B3, `ADDRESS_AUDIT.md`) already resolved a real address-inconsistency defect across the theme — not re-litigated here, per "never repeat completed work" |
| Internal linking architecture | 🟡 Partial evidence | Prior Sprint 2 work added real cross-links between location-specific pages and a hub page (`seo-audit/audit/CHANGELOG.md`, 2026-07-30 entries); a full site-wide internal-linking graph was not re-audited in this performance phase (out of this phase's scope — see `docs/final/INTERNAL_LINKING.md` if present from earlier phases) |
| Content chunking (clear, extractable sections) | 🟡 Not directly re-verified | The product page's tab structure (`snippets/product_tabs.liquid` — description/reviews/additional-info/custom tabs, confirmed **ACTIVE** in `docs/ORPHAN_SNIPPET_AUDIT.md`) already provides natural content chunking; a dedicated content-chunking audit for GEO purposes was not performed in this pass |

## Why this matters for GEO specifically

Generative engines synthesize answers from multiple sources and are more likely to cite a business
accurately when: (1) its core facts (name, address, hours, offerings) appear identically everywhere
they're stated — already true here per the B3 unification work; (2) structured data unambiguously
labels what kind of entity is on each page — already true here per the centralized
`structured-data.liquid`/`bk-local-business.liquid` architecture; (3) content is chunked into
clearly-delineated, self-contained sections rather than one undifferentiated wall of text — partly
true here (tabs), not independently re-verified as a GEO-specific concern in this pass.

## GEO readiness score

| Dimension | Score (1–5) | Basis |
|---|---|---|
| Entity consistency (NAP, single source of truth) | 5/5 | Already resolved by prior project work, carried forward, not re-broken |
| Structured-data entity clarity | 5/5 | Non-duplicated, centrally emitted Organization/WebSite/Product/Breadcrumb schema |
| Internal linking architecture | 3/5 | Some real cross-linking exists; not comprehensively re-audited this phase |
| Content chunking | 3/5 | Product tabs provide a real structure; not GEO-specifically audited |
| **Overall GEO architecture readiness** | **4/5** | Strong entity foundation inherited from prior phases; internal-linking and content-chunking depth are the two open items for Phase 7 |

## Recommendations for Phase 7 (not implemented here)

1. A dedicated internal-linking graph audit (which pages link to which, anchor-text patterns,
   orphaned pages) — builds on, doesn't repeat, the Sprint 2 hub-linking work already done.
2. A content-chunking review across collection/page templates (not just the product page's
   existing tabs) for clearer AI-extractable sections.
3. Confirm the WebSite schema includes a `SearchAction` (sitelinks search box eligibility) if not
   already present — a quick architecture check, not performed in this pass.

## Related

[AEO_READINESS.md](AEO_READINESS.md), [AI_SEARCH_READINESS.md](AI_SEARCH_READINESS.md),
[PERFORMANCE_FINAL_REPORT.md](PERFORMANCE_FINAL_REPORT.md).
