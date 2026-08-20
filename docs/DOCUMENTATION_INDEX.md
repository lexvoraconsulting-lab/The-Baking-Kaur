# Documentation Index

Every canonical document in this repository relevant to the Shopify theme/SEO/performance work,
organized by topic. For duplicate-filename reconciliation detail, see `docs/CANONICAL_SOURCES.md`.
This index does not cover the separate `ai/` enterprise-attribute-system documentation tree
(`docs/10_Taxonomy/`, `docs/20_Attribute_Language/`, etc.) — that is a distinct subsystem, out of
scope here.

**That subsystem has its own index:** [docs/00_Foundation/FOUNDATION_v1.md](00_Foundation/FOUNDATION_v1.md)
(§7 ADR index, §7A architecture and contract documents, §8 repository structure), with
[docs/00_Foundation/GLOSSARY.md](00_Foundation/GLOSSARY.md) as the cross-program terminology
authority. New platform documents are registered there, not here — recorded 2026-08-20 so the
boundary between the two indexes is explicit rather than merely implied.

## Entry points (read these first)

| Document | Purpose |
|---|---|
| `CLAUDE.md` | Standing instructions, golden rules, current roadmap state — the single entry point for any new session |
| `00_START_HERE.md`, `TABLE_OF_CONTENTS.md` | Original enterprise-blueprint entry points |
| `docs/PHASE7_HANDOFF.md` | Entry point specifically for Phase 7 (SEO/GEO/AEO/AI Search) |

## Business & brand (canonical hierarchy: read in this order)

1. `business/BUSINESS_MASTER.md` — canonical business facts
2. `business/TBK_BRAND_GUIDELINES.md` — brand operating system
3. `design/DESIGN_SYSTEM.md`, `design/COMPONENT_LIBRARY.md`, `design/CONTENT_SYSTEM.md`,
   `design/COPY_GUIDELINES.md` — code-verified implementation layer
4. Root `DESIGN_SYSTEM.md`, `COMPONENT_LIBRARY.md`, `CONTENT_SYSTEM.md`, `COPY_GUIDELINES.md` —
   original vision/blueprint documents (companion to #3, not superseded by it)
5. `BRAND_VOICE.md`, `ANIMATION_GUIDELINES.md` — supplementary blueprint docs

## Theme architecture

| Document | Purpose |
|---|---|
| `SHOPIFY_ARCHITECTURE.md` (root) | Canonical, detailed theme architecture reference |
| `docs/SHOPIFY.md` | Working summary of the above |
| `docs/ARCHITECTURE.md` | Repo-wide 3-layer architecture overview (theme / enterprise blueprint / seo-ops tooling) |
| `docs/CODING_STANDARDS.md` | seo-ops Python conventions |
| `docs/DECISIONS.md` | Consequential-decision log |
| `CATALOG_ARCHITECTURE.md`, `DATA_ARCHITECTURE.md`, `INFORMATION_ARCHITECTURE.md` | Blueprint-era architecture docs |

## SEO-audit & Liquid-cleanup workstream (Phase 4–6.5, this conversation's primary track)

| Document | Purpose |
|---|---|
| `seo-audit/audit/CHANGELOG.md` | Canonical changelog for this workstream |
| `seo-audit/audit/AUDIT_LEDGER.md` | Canonical audit ledger for this workstream |
| `docs/LIQUID_ARCHITECTURE_AUDIT.md` | Phase 5 audit + R0–R7 phased plan |
| `docs/TEMPLATE_CENSUS.md` | R3 exhaustive product-template census |
| `docs/ORPHAN_SNIPPET_AUDIT.md` | R4 orphan-snippet classification |
| `docs/FINAL_REPORT.md` | R0–R7 final certification |
| `docs/PERFORMANCE_BASELINE.md`, `PERFORMANCE_AUDIT.md`, `PERFORMANCE_RECOMMENDATIONS.md`, `CORE_WEB_VITALS.md`, `PERFORMANCE_SCORECARD.md`, `PERFORMANCE_ROADMAP.md` | Phase 6 performance engineering set |
| `docs/PERFORMANCE_FINAL_REPORT.md` | Phase 6 final certification |
| `docs/AEO_READINESS.md`, `GEO_READINESS.md`, `AI_SEARCH_READINESS.md` | Phase 6 SEO/GEO/AEO architecture readiness |
| `docs/PHASE7_HANDOFF.md`, `PHASE7_EXECUTION_PLAN.md`, `PHASE7_DEPENDENCIES.md`, `PHASE7_RISK_REGISTER.md`, `PHASE7_PRIORITY_MATRIX.md`, `PHASE7_TASK_BREAKDOWN.md`, `PHASE7_ACCEPTANCE_CRITERIA.md`, `PHASE7_BLOCKERS.md`, `PHASE7_SUCCESS_METRICS.md` | Phase 6.5 handoff/readiness planning set |
| `docs/CANONICAL_SOURCES.md`, `DOCUMENTATION_INDEX.md` (this file), `REPOSITORY_MAP.md`, `FILE_OWNERSHIP.md`, `DOCUMENTATION_CHANGELOG.md`, `PHASE7_READY.md` | Phase 7.0 pre-flight reconciliation set |

## Enterprise-transformation homepage/build workstream (Phase A→J, separate track)

| Document | Purpose |
|---|---|
| `CHANGELOG.md` (root) | Canonical changelog for this workstream — Phase A (promoted live), Phase C1/S1–S8 (preview-only, status not re-verified in Phase 7.0) |
| `PROJECT_ROADMAP.md` | Roadmap for this workstream |
| `HOMEPAGE_SPECIFICATION.md`, `HOMEPAGE_CONTENT_STRATEGY.md` | Homepage build specs |
| `MERCHANDISING_GUIDE.md`, `QA_CHECKLIST.md` | Supporting docs |
| `PERFORMANCE_BASELINE.md` (root) | Historical Phase-A-era performance baseline (see `CANONICAL_SOURCES.md`) |

## SEO / local / policy (pre-existing, not re-audited this pass)

| Document | Purpose |
|---|---|
| `SEO_AUDIT_LEDGER.md`, `SEO_GEO_MASTER_PLAN.md`, `GSC_AUDIT.md` | SEO tracking |
| `SCHEMA_MASTER.md` | Structured-data reference |
| `NAP_RECONCILIATION.md`, `FINAL_NAP_AND_MC_ARCHITECTURE.md` | Address/NAP work |
| `LOCAL_DELIVERY_SETUP_STEPS.md`, `PROPOSED_DELIVERY_CONFIG.md`, `PROPOSED_SERVICE_AREA.md`, `SERVICE_AREA_ZONE_MAP.md` | Delivery/service-area docs |
| `REVIEW_STRATEGY.md` | Governs all review/rating/testimonial content — referenced throughout the R0–R7 series |
| `MD_FILE_INVENTORY.md` | An earlier attempt at cataloguing the repo's `.md` files |

## Repository/git

| Document | Purpose |
|---|---|
| `docs/GIT_RELEASE.md` | Branch-publish record |
| `VERSION.md` | Version tracking |
| `README.md` | Repo root readme |
| `docs/setup/README.md` (+ `docs/setup/*.md`) | Development-environment documentation |

## Related

[CANONICAL_SOURCES.md](CANONICAL_SOURCES.md), [REPOSITORY_MAP.md](REPOSITORY_MAP.md),
[FILE_OWNERSHIP.md](FILE_OWNERSHIP.md), [DOCUMENTATION_CHANGELOG.md](DOCUMENTATION_CHANGELOG.md),
[PHASE7_READY.md](PHASE7_READY.md).
