# AI Search & LLM Crawler Readiness — Architecture Only

Generated 2026-07-31 (Phase 6). Architecture-only assessment — **no content changed**. Covers
crawl efficiency, LLM readability, and citation readiness for AI crawlers (GPTBot, ClaudeBot,
Google-Extended, PerplexityBot, etc.) and knowledge-graph compatibility, distinct from the
narrower AEO (`AEO_READINESS.md`) and entity-focused GEO (`GEO_READINESS.md`) documents.

## Crawl efficiency — evidence

| Signal | Status | Evidence |
|---|---|---|
| Storefront currently blocks ALL crawlers (including AI crawlers) | 🔴 **Active blocker** | The site is intentionally password-gated (`business/BUSINESS_MASTER.md` §16) — no crawler, AI or otherwise, can currently index any page. This is the single largest AI-search-readiness blocker, and it is a **business decision**, not an architecture gap. |
| `robots.txt` / crawler-access architecture (once unlocked) | ⚪ Not assessed | Cannot be meaningfully assessed while the password gate makes the entire site return the password page to every crawler regardless of `robots.txt` content. |
| Semantic HTML (reduces LLM parsing ambiguity) | ✅ Confirmed | `<main role="main">` landmark present (`layout/theme.liquid:180`); single `<h1>` per product page (confirmed in `AEO_READINESS.md`). |
| Structured data (machine-readable facts, independent of visual layout) | ✅ Strong | Centralized Product/Organization/WebSite/Breadcrumb schema (`AEO_READINESS.md`, `GEO_READINESS.md`) — this is exactly the kind of unambiguous, layout-independent fact source LLM crawlers and knowledge-graph builders prefer over parsing visual HTML. |
| Render-blocking resources affecting crawl budget/render cost | 🟡 Real but minor | `docs/PERFORMANCE_AUDIT.md` F-5 (large unconditional CSS) — most AI crawlers execute minimal or no JS/CSS rendering and read server-rendered HTML/schema directly, so this is a smaller concern for AI-crawler readiness than for human-visitor Core Web Vitals, but not zero (crawlers with a render step, e.g. Googlebot's second wave, are affected). |

## Knowledge-graph compatibility

The existing schema architecture (`snippets/bk-local-business.liquid`, `tbk-schema-website.liquid`,
centralized `structured-data.liquid`) already emits `LocalBusiness`/`Bakery`, `Organization`, and
`WebSite` entity types with consistent NAP data — the exact shape a knowledge-graph ingestion
pipeline (Google's own, or any LLM's retrieval-augmented pipeline) needs to build a confident entity
node. This is a genuine strength carried forward from prior project phases, not new work in this
phase.

## AI citation readiness

For an LLM to cite this business confidently in an answer, it needs: consistent facts across every
page (✅, established), structured data confirming entity type and attributes (✅, established), and
**the ability to actually crawl the site at all** (🔴, blocked by the password gate). The first two
are architecturally sound; the third is an active, total blocker that makes the first two currently
moot for any real AI crawler — until the site is unlocked, no AI system can discover any of this
good architecture.

## AI Search readiness score

| Dimension | Score (1–5) | Basis |
|---|---|---|
| Crawlability (right now, today) | **1/5** | Total block via password gate — not an architecture problem, a business-state problem |
| Crawlability (architecture, once unlocked) | 4/5 | Semantic HTML + structured data are already in good shape; `robots.txt` specifics unassessed |
| Structured-data / knowledge-graph compatibility | 5/5 | Strong, centralized, non-duplicated entity schema |
| LLM readability (semantic structure) | 4/5 | Clean heading/landmark structure confirmed on the product page; not exhaustively checked site-wide |
| **Overall AI Search readiness (as currently deployed)** | **2.5/5** — dragged down entirely by the crawlability blocker | **Overall AI Search readiness (architecture, once unlocked)** | **4.5/5** |

## Recommendation for Phase 7 (business decision required, not implemented here)

**The single highest-leverage action for AI-search readiness is unlocking the storefront** (or
publishing a subset of pages, e.g. via a public preview) — every architectural strength documented
in this file and in `AEO_READINESS.md`/`GEO_READINESS.md` is currently invisible to every AI
crawler and search engine. This is explicitly a **business decision** (per this project's own
standing rule that the password gate is intentional, `business/BUSINESS_MASTER.md` §16) — not an
engineering task, and not performed or recommended to be silently reversed here.

Once unlocked:
1. Confirm `robots.txt` explicitly allows the AI crawlers the business wants to permit (GPTBot,
   ClaudeBot, Google-Extended, PerplexityBot) rather than relying on defaults.
2. Re-run this readiness assessment against the real, crawlable site.
3. Proceed with Phase 7's Enterprise SEO + GEO + AEO + AI Search content work, now that the
   architecture underneath it is confirmed sound.

## Related

[AEO_READINESS.md](AEO_READINESS.md), [GEO_READINESS.md](GEO_READINESS.md),
[CORE_WEB_VITALS.md](CORE_WEB_VITALS.md) (same password-gate constraint affects both AI-crawl
readiness and lab performance measurement), [PERFORMANCE_FINAL_REPORT.md](PERFORMANCE_FINAL_REPORT.md).
