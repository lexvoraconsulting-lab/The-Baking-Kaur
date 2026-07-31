# Answer Engine Optimization (AEO) Readiness — Architecture Only

Generated 2026-07-31 (Phase 6). **No SEO content was changed to produce this document** — this is
an architecture-readiness assessment only, per the phase's explicit instruction ("prepare the
architecture... do NOT change SEO content").

AEO concerns whether a page's content can be cleanly extracted and cited as a direct answer by
answer engines, voice assistants, and featured-snippet systems — a narrower, more literal-answer
focused cousin of GEO (`docs/GEO_READINESS.md`) and AI Search readiness (`docs/AI_SEARCH_READINESS.md`).

## Current architecture — evidence

| Signal | Status | Evidence |
|---|---|---|
| FAQ content exists | ✅ Present | `templates/page.faq-01.json` (live) and `page.faq-02.json` (unused duplicate, per prior SEO audit) |
| FAQPage-type schema capability exists in the codebase | 🟡 Partial | `mainEntity`/`FAQPage`-related patterns found in `snippets/tbk-schema-article.liquid` and `snippets/tbk-schema-collection.liquid` — not confirmed wired to the FAQ page template itself; needs a follow-up check, not performed in this pass |
| Single, semantic `<h1>` per page | ✅ Confirmed | `sections/main-product-premium-v2.liquid` — exactly 1 `<h1>` (product title), consistent with clean answer-extraction structure |
| Central, non-duplicated Product structured data | ✅ Confirmed, strong | `snippets/structured-data.liquid`, gated on `request.page_type == 'product'`, rendered once from `layout/theme.liquid` regardless of which of the 4 product-page section templates renders the visual layout — the snippet's own comment explicitly notes this avoids "two @type:Product entities describing the same URL" |
| Breadcrumb schema | ✅ Present, site-wide | `snippets/tbk-schema-breadcrumb.liquid`, referenced from `layout/theme.liquid` |
| Canonical URLs | ✅ Present, site-wide | `layout/theme.liquid:28` — `<link rel="canonical" href="{{ canonical_url }}">` on every page |
| Semantic `<main>` landmark | ✅ Present | `layout/theme.liquid:180` — `<main id="MainContent" role="main">` |

## What "answer-extraction readiness" needs beyond architecture (content work, out of this
document's scope)

- FAQ content itself needs to be reviewed for direct-answer phrasing (a question immediately
  followed by a concise, factual answer) — a content task, not an architecture task, and
  explicitly out of scope here.
- Whether `page.faq-01.json`'s content is wrapped in `FAQPage` schema markup needs direct
  confirmation (flagged above as partial/unconfirmed) — a follow-up architecture check, not a
  content change, recommended for Phase 7.

## AEO readiness score

| Dimension | Score (1–5) | Basis |
|---|---|---|
| Structured-data foundation | 5/5 | Product/Breadcrumb/WebSite/Organization schema all centrally, non-redundantly emitted |
| Heading/semantic structure | 4/5 | Confirmed clean on the product page; homepage/collection heading hierarchy not individually re-verified in this pass |
| FAQ infrastructure | 3/5 | Content exists; FAQPage schema wiring unconfirmed |
| Canonical/URL architecture | 5/5 | Site-wide, consistent |
| **Overall AEO architecture readiness** | **4.25/5** | Strong foundation; the one open item (FAQPage schema confirmation) is a quick follow-up, not a rebuild |

## Recommendations for Phase 7 (not implemented here)

1. Confirm whether `page.faq-01.json` content is wrapped in `FAQPage`/`Question`/`Answer` JSON-LD —
   if not, this is a high-value, low-risk addition (structured data only, no visible UX change).
2. Audit collection and homepage heading hierarchy the same way the product page was checked here.
3. Consider a dedicated "answer box" content pattern (question as a heading, answer as the
   immediately following paragraph) for high-intent queries once real content work is greenlit —
   a content/copy decision, not an architecture one.

## Related

[GEO_READINESS.md](GEO_READINESS.md), [AI_SEARCH_READINESS.md](AI_SEARCH_READINESS.md),
[PERFORMANCE_FINAL_REPORT.md](PERFORMANCE_FINAL_REPORT.md).
