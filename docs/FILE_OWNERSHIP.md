# File Ownership

Which document is authoritative for which kind of update, going forward. Written to prevent the
exact ambiguity Phase 7.0 found and fixed (a future session updating the wrong file, or updating
both inconsistently).

## Rule of thumb

**If you're about to update a changelog, ask: which workstream is this change part of?**
- Shopify theme cleanup, Liquid refactoring, performance engineering, or SEO/GEO/AEO architecture
  work → `seo-audit/audit/CHANGELOG.md` + `seo-audit/audit/AUDIT_LEDGER.md`
- Homepage/build content work (sections, hero, trust strip, Phase A–J roadmap items) →
  `CHANGELOG.md` (root)

Never split one logical change across both files. If a change genuinely touches both workstreams,
log it in the more specific one and add a one-line cross-reference in the other.

## Ownership table

| File | Owner (what kind of change updates it) |
|---|---|
| `seo-audit/audit/CHANGELOG.md` | Any Sprint 1–2, Phase 4–6.5 SEO-audit/Liquid-cleanup/performance change |
| `seo-audit/audit/AUDIT_LEDGER.md` | Same workstream — the ledger's summary table, updated alongside the changelog |
| `CHANGELOG.md` (root) | Any Phase A–J homepage/build-track change |
| `docs/ARCHITECTURE.md` | Any change to the repo's 3-layer structure or template/section/snippet counts — **must be numerically verified** (`ls`, not remembered) before updating |
| `SHOPIFY_ARCHITECTURE.md` (root) | Canonical theme-architecture facts — update when the underlying theme structure changes; cross-reference Phase 6/7 findings rather than duplicating them |
| `docs/SHOPIFY.md` | Working summary — update only to stay in sync with `SHOPIFY_ARCHITECTURE.md`, never diverge from it |
| `business/BUSINESS_MASTER.md` | Real business facts only — never invent, always verify against Shopify Admin or the business owner |
| `design/*.md` | Implementation-detail updates, grounded in shipped code — verify against the actual `.liquid`/`config` files before writing |
| Root `DESIGN_SYSTEM.md`/`COMPONENT_LIBRARY.md`/`CONTENT_SYSTEM.md`/`COPY_GUIDELINES.md` | Vision/blueprint updates — if a change is really an implementation detail, it belongs in `design/*.md` instead |
| `docs/PERFORMANCE_BASELINE.md` | Static/code-level baseline — update on every future performance-audit pass; don't overwrite historical data, add a new dated section |
| `PERFORMANCE_BASELINE.md` (root) | Frozen historical record (Phase A era) — do not edit further except to correct a factual error in what was actually measured then |
| `docs/CANONICAL_SOURCES.md` | Update whenever a new duplicate-filename or conflicting-claim situation is found and resolved |
| `docs/DOCUMENTATION_INDEX.md` | Update whenever a new canonical document is created |
| `CLAUDE.md` | The living entry point — update its roadmap section whenever a phase status changes (this is the file Phase 7.0 found most out of date; keep it current going forward) |

## Anti-pattern this document exists to prevent

Before Phase 7.0, `CLAUDE.md` and the root `CHANGELOG.md` both stated Phase A was "not promoted,"
while a commit dated 2026-07-14 and the live theme itself both showed it had been. Nobody
maliciously introduced this — it happened because there was no single documented answer to "which
file do I check to know if Phase A shipped," so the stale claim simply never got corrected when the
promotion happened. This document is that single answer, going forward.

## Related

[CANONICAL_SOURCES.md](CANONICAL_SOURCES.md), [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md),
[REPOSITORY_MAP.md](REPOSITORY_MAP.md), [DOCUMENTATION_CHANGELOG.md](DOCUMENTATION_CHANGELOG.md).
