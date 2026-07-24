# Markdown File Inventory

40 files. Every commit author is **Navneet Singh** — git records no other author.
"Made by" below = who actually wrote the text, inferred from commit message and content.

## Jul 02 — design handoff (2)

| File | Lines | Made by |
|---|---|---|
| design_handoff_shopify_product/CLAUDE_CODE_TASK.md | 126 | brief written for Claude |
| design_handoff_shopify_product/theme_files/README.md | 66 | handoff package |

## Jul 14 — blueprint dump (23)

Committed together as the "enterprise blueprint". Claude-generated.

| File | Lines |
|---|---|
| CHANGELOG.md | 347 |
| HOMEPAGE_CONTENT_STRATEGY.md | 270 |
| HOMEPAGE_SPECIFICATION.md | 266 |
| CATALOG_ARCHITECTURE.md | 218 |
| PROJECT_ROADMAP.md | 172 |
| DATA_ARCHITECTURE.md | 136 |
| SEO_GEO_MASTER_PLAN.md | 130 |
| COMPONENT_LIBRARY.md | 104 |
| 00_START_HERE.md | 80 |
| DESIGN_SYSTEM.md | 76 |
| INFORMATION_ARCHITECTURE.md | 70 |
| QA_CHECKLIST.md | 55 |
| SCHEMA_MASTER.md | 54 |
| PERFORMANCE_BASELINE.md | 49 |
| README.md | 47 |
| VERSION.md | 39 |
| TABLE_OF_CONTENTS.md | 38 |
| BRAND_VOICE.md | 37 |
| COPY_GUIDELINES.md | 37 |
| SHOPIFY_ARCHITECTURE.md | 37 |
| CONTENT_SYSTEM.md | 33 |
| ANIMATION_GUIDELINES.md | 32 |
| MERCHANDISING_GUIDE.md | 28 |

## Jul 16–18 — SEO work (2)

| File | Lines | Made by |
|---|---|---|
| SEO_AUDIT_LEDGER.md | 1468 | Claude — output log of the ~602-product SEO migration |
| REVIEW_STRATEGY.md | 185 | Claude |

## Jul 19 — NAP / delivery cluster (5)

One decision (Meerut, ~15 km, ₹350 min). Four drafts + one final.

| File | Lines | Status |
|---|---|---|
| FINAL_NAP_AND_MC_ARCHITECTURE.md | 184 | final |
| PROPOSED_DELIVERY_CONFIG.md | 289 | superseded |
| NAP_RECONCILIATION.md | 202 | superseded |
| PROPOSED_SERVICE_AREA.md | 168 | superseded |
| SERVICE_AREA_ZONE_MAP.md | 114 | superseded |
| LOCAL_DELIVERY_SETUP_STEPS.md | 145 | manual checklist, still useful |

## Jul 23 — cleanup layer (6)

Second doc system, added because the root was unreadable. Claude-generated.

| File | Lines |
|---|---|
| GSC_AUDIT.md | 156 |
| CLAUDE.md | 62 |
| docs/DECISIONS.md | 50 |
| docs/SHOPIFY.md | 50 |
| docs/CODING_STANDARDS.md | 42 |
| docs/ARCHITECTURE.md | 40 |
| tasks/README.md | 37 |

## Verdict

- **Keep:** CLAUDE.md, docs/*, tasks/README.md, SEO_AUDIT_LEDGER.md, LOCAL_DELIVERY_SETUP_STEPS.md
- **Merge into FINAL_NAP_AND_MC_ARCHITECTURE.md, then delete:** the 4 superseded Jul-19 files
- **Dead weight:** most of the Jul-14 blueprint — specs for a store that already exists; the theme code is the spec now
