# Phase 7 Dependency Graph

Dependency relationships across SEO, Schema, Entity SEO, GEO, AEO, AI Search, Merchant Center,
Search Console, Knowledge Graph, Local SEO, Content Authority, Internal Linking, Structured Data,
and Trust Signals. Task IDs reference `docs/PHASE7_TASK_BREAKDOWN.md`.

## Graph (textual — dependencies flow top to bottom)

```
C-1 Password gate decision (BLOCKS EVERYTHING BELOW MARKED "gated")
 │
 ├─→ E-1/H-1 Real Lighthouse/PSI measurement ─────────────────┐
 │                                                             │
 ├─→ E-2 AI/search crawler indexing                            │
 │    │                                                        │
 │    ├─→ Search Console verification (external creds)         │
 │    ├─→ Merchant Center verification (external creds)        │
 │    └─→ Knowledge Graph / entity confirmation (depends on     │
 │         crawlability + the structured-data foundation below) │
 │                                                             │
 └─→ Google Business Profile reconciliation (external creds,   │
      independent of password gate — GBP is a separate listing) │
                                                                 ▼
Structured Data foundation (ALREADY DONE, R0–R7/Phase 6 — not gated)
 │  Product/Organization/WebSite/Breadcrumb schema, centralized,
 │  non-duplicated (docs/AEO_READINESS.md, docs/GEO_READINESS.md)
 │
 ├─→ Entity SEO (builds directly on the existing schema foundation
 │    — NOT blocked by the password gate for the *architecture* work,
 │    only blocked for *verification* that search engines see it correctly)
 │
 ├─→ H-2 FAQPage schema confirmation (independent, can run NOW)
 │
 ├─→ Trust Signals (B-4 reviews, B-6 FSSAI number — business decisions,
 │    independent of password gate, can be resolved in parallel)
 │
 └─→ Local SEO (NAP consistency already resolved by prior B3 work —
      not gated, already complete; GBP reconciliation is external-creds-gated only)

Internal Linking / Content Authority
 │  M-1 Internal-linking graph audit — independent, can run NOW
 │  M-2 Content-chunking review — independent, can run NOW
 │  (both build on, don't repeat, Sprint 2's hub-linking work)
 │
 └─→ feeds into GEO readiness (content structure) and AEO readiness
      (answer-extraction quality) — improves both once real content
      work begins in Phase 7

AEO ← depends on: Structured Data foundation (done) + H-2 (FAQPage) + Content Authority work
GEO ← depends on: Entity SEO (done) + Internal Linking + Content Authority work
AI Search ← depends on: EVERYTHING ABOVE (architecture) + C-1 (password gate, for real-world effect)
```

## What can execute in parallel (no dependency conflicts)

**Track A — Documentation reconciliation** (no external dependency, no business decision needed):
- C-2 (reconcile the two CHANGELOG.md files)
- H-5 (fix `docs/ARCHITECTURE.md`'s stale template count)
- M-4 (reconcile the two PERFORMANCE_BASELINE.md files)
- M-5 (add cross-references from root design docs to `design/*.md`)
- L-1, L-2, L-3 (low-priority doc fixes)

**Track B — Architecture work not gated by the password gate**:
- H-2 (FAQPage schema confirmation)
- M-1 (internal-linking graph audit)
- M-2 (content-chunking review)
- M-3 (WebSite `SearchAction` schema check)

**Track C — Business decisions** (can be surfaced to the business owner simultaneously, don't
block each other):
- B-1 (password gate), B-2 (`shine-trust.liquid`), B-3 (B4/B5/B6), B-4 (reviews), B-5 (photography),
  B-6 (FSSAI number)

**Track D — External-access items** (can be pursued in parallel once credentials exist, don't
block each other):
- E-3/V-1 (`tbk-product.liquid` app check), E-5 (Merchant Center/Search Console), E-6 (GBP)

**Sequential dependency (cannot parallelize)**:
- C-1 (password gate resolution) → H-1/E-1 (real Lighthouse measurement) → any further
  performance-optimization prioritization decisions (per `docs/PERFORMANCE_ROADMAP.md` P6.2's own
  sequencing rationale, carried forward)
- C-1 → E-2 (crawler indexing) → Search Console/Merchant Center *verification* (though the
  Console/Merchant Center *accounts themselves* can be set up in parallel, ahead of time)

## Key insight

**Most of Phase 7's architecture-level work (Tracks A and B) is not blocked by the password gate
at all.** The password gate only blocks *measurement* and *real-world crawl verification* — not
the underlying architectural readiness work, which can and should proceed in parallel with
resolving C-1, not wait for it.

## Related

[PHASE7_TASK_BREAKDOWN.md](PHASE7_TASK_BREAKDOWN.md), [PHASE7_EXECUTION_PLAN.md](PHASE7_EXECUTION_PLAN.md),
[PHASE7_BLOCKERS.md](PHASE7_BLOCKERS.md), [PHASE7_PRIORITY_MATRIX.md](PHASE7_PRIORITY_MATRIX.md).
