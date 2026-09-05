# SEO Changelog (Phase 7.1)

Every real change made in Phase 7.1, with full evidence. This is the SEO-specific changelog,
distinct from `seo-audit/audit/CHANGELOG.md` (the broader SEO-audit/Liquid-cleanup workstream
changelog it lives alongside) and `CHANGELOG.md` root (the separate homepage-build workstream) —
see `docs/FILE_OWNERSHIP.md` for the ownership convention this follows.

## 2026-07-31 — Collapsed 2 confirmed redirect chains (25 redirects)

**What**: retargeted 25 URL redirects from a 2-hop chain to a direct 1-hop redirect.

**Before**:
- `/collections/theme-cakes-1` → `/collections/theme-cakes` → `/collections/designer-theme-cakes`
- 24 product-handle redirects → `/collections/flowers` → `/collections/cake-hampers`

**After**:
- `/collections/theme-cakes-1` → `/collections/designer-theme-cakes` (direct)
- All 24 product-handle redirects → `/collections/cake-hampers` (direct)
- `/collections/theme-cakes` and `/collections/flowers` themselves left untouched — still valid
  1-hop redirects for anyone hitting those specific URLs directly.

**Why**: redirect chains add unnecessary round-trips for crawlers and users, dilute link equity
across each hop, and are flagged by every major technical-SEO audit standard as a fix-when-found
issue. This project's own instruction explicitly lists redirect chains as an audit target.

**Evidence**: found via systematic Admin API queries (exhaustive 825-redirect pagination +
targeted `query: "target:/collections/flowers"` search), not manual sampling — full detail in
`docs/CRAWL_REPORT.md`.

**Verification**:
1. Fetched fresh redirect IDs immediately before mutating (never guessed, per `CLAUDE.md`'s
   standing rule).
2. **User approval explicitly requested and given** before executing — this is a live production
   change to real URL routing (instant effect, not a theme deploy), and the auto-mode classifier
   correctly flagged it for confirmation rather than letting it proceed autonomously.
3. Executed via `urlRedirectUpdate`, 4 batches of ≤8 mutations (per this project's established
   Admin API batching convention), **zero `userErrors`** across all 25 mutations.
4. Re-queried after: `path:/collections/theme-cakes-1` confirms the new direct target;
   `target:/collections/flowers` returns zero results, confirming no redirect anywhere still
   chains through that collection.

**Risk**: low — redirect updates are simple, immediately reversible (the original target values are
recorded in `docs/CRAWL_REPORT.md` if a revert is ever needed), and affect only the destination of
an already-redirecting URL, not any live page's content or availability.

**Rollback**: `urlRedirectUpdate` each of the 25 IDs listed in `docs/CRAWL_REPORT.md` back to their
original `target` value (`/collections/theme-cakes` for the one, `/collections/flowers` for the
24).

## What was found but NOT changed (documented, not silently dropped)

- **Homepage duplicate `<h1>`** (`docs/TECHNICAL_SEO_AUDIT.md`, heading hierarchy section) —
  corroborates an already-known, pre-existing finding from root `CHANGELOG.md`'s Phase A
  verification record. Not fixed: it lives inside a content-bearing custom-liquid block belonging
  to the separate homepage-build workstream, and this phase's own rule is "never modify business
  content."
- **Absolute vs. relative redirect-target URL inconsistency** (`docs/URL_ARCHITECTURE.md`) —
  cosmetic, both forms work correctly, low priority, not touched this phase.
- **Legacy non-descriptive product handles** — a real, already-documented, deliberately-deferred
  decision (`CLAUDE.md`) with its own 8-step checklist. Not reopened.
- **Full internal-linking graph / orphan-collection census** — already correctly scoped as its own
  dedicated task (M-1) in Phase 6.5's planning; not folded into this phase as a shortcut.
- **Duplicate title/description re-verification across 602+ active products** — prior work already
  addressed this; a fresh full re-audit wasn't performed here without specific evidence prompting
  one.

## Related

[CRAWL_REPORT.md](CRAWL_REPORT.md), [TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md),
[TECHNICAL_SEO_SCORECARD.md](TECHNICAL_SEO_SCORECARD.md).
