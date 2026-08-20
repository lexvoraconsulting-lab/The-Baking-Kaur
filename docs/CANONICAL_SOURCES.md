# Canonical Sources

For every documentation topic with more than one file, this table states which is canonical for
what, and why. Generated during Phase 7.0's pre-flight reconciliation (2026-07-31). No file was
deleted to produce this — every duplicate found was either corrected in place, cross-referenced,
or confirmed to be a legitimately separate, non-competing document.

## Real conflicts found and resolved

| Topic | Files | Resolution |
|---|---|---|
| **Enterprise-transformation changelog** | `CHANGELOG.md` (root) | **Canonical for**: Phase A→J homepage/build workstream (schema dedup, footer restore, hero/trust-strip, S1–S8 sections). **Not a duplicate** of the SEO-audit changelog — a separate, real, non-overlapping workstream. Corrected in place: the file's own "Phase A... staged, not yet deployed" header contradicted its own later "PROMOTED TO LIVE (2026-07-14)" entry — fixed (struck through the stale line, didn't delete it). Added a scope-clarifying header. |
| **SEO-audit / Liquid-cleanup changelog** | `seo-audit/audit/CHANGELOG.md` | **Canonical for**: Sprint 1–2, Phase 4 re-verification, Phase 5's R0–R7 Liquid refactor, Phase 6 performance engineering, Phase 6.5 planning. Added a matching scope-clarifying header pointing to the root file for the other workstream. |
| **Performance baseline** | `PERFORMANCE_BASELINE.md` (root) vs. `docs/PERFORMANCE_BASELINE.md` | **Canonical going forward**: `docs/PERFORMANCE_BASELINE.md` (Phase 6, P6.0, static code-level baseline, most current). **Historical, preserved**: root version — a genuine earlier "Phase A"-era preview-theme runtime measurement (DOMContentLoaded, Load, resource count via the browser Performance API) that `docs/PERFORMANCE_BASELINE.md` didn't know about and had incorrectly implied never happened. Corrected `docs/PERFORMANCE_BASELINE.md`'s overstated claim; added a pointer note to the root file marking it historical, not deleted. |
| **Design System / Component Library / Content System / Copy Guidelines** | Root `*.md` vs. `design/*.md` | **Both canonical, different layers**: root files are the original vision/blueprint documents; `design/*.md` files are later, code-verified companions adding engineering-level implementation detail grounded directly in shipped code. Neither superseded the other — added symmetric cross-reference pointers (previously only `design/*.md` pointed back to root/business docs; now root docs point forward too). |
| **Architecture template count** | `docs/ARCHITECTURE.md` | Corrected a stale factual claim (40 templates → actual current count 33, verified via `ls templates/`), with a note on what changed it (R3.5's removal of `product.tbk.json`). |
| **Font render-blocking / Uploadcare notes** | `SHOPIFY_ARCHITECTURE.md` (root) | Updated to reflect Phase 6's actual findings: the `fonts.gstatic.com` preconnect gap this file already flagged is now closed (P6.6); the "duplicate Uploadcare" item this file already flagged was independently re-investigated and confirmed NOT a true duplicate (P6.5) — both findings cross-referenced to `docs/PERFORMANCE_FINAL_REPORT.md` rather than restated. |
| **`CLAUDE.md`'s Phase A status claim** | `CLAUDE.md` | Corrected: claimed Phase A was "not promoted"; commit `77861b3` (2026-07-14) and a live pull-diff performed during this reconciliation confirm it was promoted and remains live and in sync. Also noted: design-token restoration (the roadmap's "unlocks the homepage build" step) is also done, via R0. |

## 2026-08-20 — platform-tree conflicts found and resolved

Added by the documentation integration pass following the n8n/Python reconciliation. These sit in
the `ai/` platform tree, which the 2026-07-31 pass above explicitly scoped out.

| Topic | Files | Resolution |
|---|---|---|
| **System of record — n8n vs. Python** | `docs/30_Enterprise_Program_Roadmap/Enterprise_Program_Roadmap_v1.md` §03 vs. `n8n/TBK-A-OS/*` + `n8n/tbk-vision-workflow-complete/*` | **Real conflict.** EPR §03 scoped n8n as orchestration that would "never be a second write path"; the delivered n8n build owns extraction, taxonomy content, conflict resolution, product assembly and persistence. Resolved by [ADR 0011](adr/2026-08-20-n8n-python-system-of-record.md): Python owns the contract, n8n owns execution, PostgreSQL holds bytes under a Python-defined schema. EPR §03's *when vs. what* split is upheld; its assumption that persistence would sit on the platform side is corrected. |
| **"Cake Genome" naming** | `ECP-100_Architecture_Review.md` §20 vs. `Enterprise_Program_Roadmap_v1.md` §02 | **Real conflict.** ECP-100 §20 stated Cake Genome "was not found named anywhere"; EPR §02 defines Cake Genome™ in a dedicated subsection five days earlier. **EPR wins** (older, more specific, dedicated section). ECP-100 is a closed review, so it carries an in-place correction note rather than an edited finding. Canonical relationship recorded in [00_Foundation/GLOSSARY.md](00_Foundation/GLOSSARY.md). |
| **Two taxonomies** | `ai/taxonomy/content/bakery_v1.json` vs. `n8n/TBK-A-OS/Data Tables/tbk_taxonomy_attributes.csv` + `tbk_taxonomy_synonyms.csv` | **Real conflict, NOT yet resolved.** 26 attributes / 96 terms vs. 17 rows / 3 attribute types, unrelated identifier schemes. `bakery_v1.json` is canonical per ADR 0011 — but the n8n tables hold typed synonym data that exists nowhere else, so a one-way export would destroy content. Sequenced as work item **D1** with an explicit ordering constraint; see [IMPLEMENTATION_DEPENDENCY_MAP.md](30_Enterprise_Program_Roadmap/IMPLEMENTATION_DEPENDENCY_MAP.md). |
| **Empty-directory claims** | `ECP-100` §15, `00_Foundation/FOUNDATION_v1.md` §8 | **Stale fact, corrected.** Both described `ai/api/`, `ai/automation/`, `ai/embeddings/`, `ai/vectordb/`, `ai/ollama/` as empty directories. None exists on disk — git does not track empty directories. FOUNDATION_v1 §8 corrected; ECP-100 carries an in-place note. |
| **Build status staleness** | `00_Foundation/FOUNDATION_v1.md` §11 | **Stale, corrected in place** per that document's own §14 ("the linked source is correct and this document should be updated to match it"). Build-005 shown as "Not started" was frozen and complete; Build-007 shown as "Not started" had its semantic Phase 1 shipped as Build-302. |

## Confirmed NOT conflicts (checked, no action needed)

| Topic | Files | Why no conflict |
|---|---|---|
| `docs/SHOPIFY.md` vs. root `SHOPIFY_ARCHITECTURE.md` | Already self-declares the relationship: `docs/SHOPIFY.md` states it is "the working summary" of the canonical root file. No fix needed — this was already done correctly by a prior phase. |
| `ai/` enterprise-attribute-system docs (`Architecture.md`, `Roadmap.md`, `Examples.md`, `Validation.md`, `Versioning.md`, `SPRINT_CHARTER.md`, `EAD_SPECIFICATION.md` — each appearing 2–4 times) | Each instance lives in a distinct module folder (`docs/10_Taxonomy/`, `docs/20_Attribute_Language/`, `docs/40_Enterprise_Attribute_Registry/`, etc.) — a deliberate, intentional per-module documentation pattern for a completely separate subsystem (the AI/enterprise-attribute build program), unrelated to the Shopify theme/SEO work this reconciliation covers. |
| `README.md` (9 instances) | One per directory/subsystem, the standard, expected pattern — not a conflict. |
| `LICENSE.md` (3 instances) | All inside `.venv/` — third-party Python package licenses, not project documentation at all. |
| `docs/blog-os/CHANGELOG.md` | Scoped to its own separate `blog-os` subsystem, not a Shopify-theme or SEO-audit changelog. |

## How this was verified

Full repo-wide duplicate-filename scan: `find . -iname "*.md" -not -path "./node_modules/*" |
xargs -n1 basename | sort | uniq -d`. Every hit was individually read (not just filename-matched)
before being classified as a real conflict or a legitimate separate document — several suspected
conflicts turned out, on reading, to be entirely different topics or intentionally-scoped
per-module docs.

## Related

[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md), [FILE_OWNERSHIP.md](FILE_OWNERSHIP.md),
[REPOSITORY_MAP.md](REPOSITORY_MAP.md), [DOCUMENTATION_CHANGELOG.md](DOCUMENTATION_CHANGELOG.md),
[PHASE7_READY.md](PHASE7_READY.md).
