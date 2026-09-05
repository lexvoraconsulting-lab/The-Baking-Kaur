# Project Rules — The-Baking-Kaur

> **Parent:** [`support-master.md`](./support-master.md) · Method: `projectops-v2`
> **Authority:** Governing rulebook for all human and AI agents working on `The-Baking-Kaur`.

## 1. Governance & Boundary Rules (`projectops-v2`)

1. **Documentation Root:** All governed documentation resides strictly within `Support/`.
2. **Git Mode:** `Direct Main` (or tracked branch `feature/vision-engine-v1`).
3. **Visual Documentation Theme:** `lexvora-company` (enforced via [`skills/ThemeStyleOps`](../skills/ThemeStyleOps)).
4. **Continuous Table Sequencing:** Every governed Markdown table must contain a left-most sequence column named `S.No.` continuously numbered 1..N.
5. **Deterministic Hierarchy Balancing:** Every Plan task statistics row and roll-up must strictly satisfy `TL = PD + IP + CD`.
6. **Identifier Token Convention:** Use `_` as identifier token separator (e.g., `G_01`, `WL_YYYYMMDD_A`, `CON001`).
7. **Zero-Token Automation:** All mechanical calculations, worklog entries, syncs, and commits are managed via the `pdm` CLI.

## 2. Protected Modules & Storefront Invariants

1. **Product Page is a Protected Module:** `templates/product.json` renders `sections/main-product-premium-v2.liquid`. No visual, UX, purchase-flow, CSS, or JS changes are allowed. Only invisible enhancements (structured data, analytics, accessibility, performance) are permitted, and only deliberately.
2. **Brand Asset Integrity:** Canonical logo and brand color ramps (`tbk-tokens.liquid`: rose `#7a2147`, soft pill `#fff7f8`, border `#f2d6dd`, gold/champagne accents) must be strictly preserved.
3. **Catalogue Draft Status:** Drafts stay drafts. 584 of 1,235 products are intentionally `DRAFT`. Never bulk-flip `DRAFT` to `ACTIVE` without explicit merchandising sign-off.
4. **Variant Update Safety:** On `productOptionUpdate`, always pass `variantStrategy: LEAVE_AS_IS`; never delete option values (deleting option values permanently destroys variants).
5. **Never Guess Shopify IDs:** Always fetch real IDs from the Admin GraphQL API. Never invent or hardcode IDs.

## 3. Truth, Trust & Content Standards

1. **Verifiability Beats Persuasion:** No rating, count, certification, review, or delivery promise ships without a verifiable source. Never invent GTINs, MPNs, barcodes, reviews/ratings, or promises the studio cannot fulfill.
2. **Review Strategy:** Zero unverified reviews. Fabricated testimonials are strictly prohibited. Reviews must be sourced from verifiable Google Business Profile listings (with direct `source_url`) or verified-buyer platforms (e.g., Judge.me).
3. **SEO Snippet Format:** Active-product SEO title format must follow `"{Name} - Eggless | Meerut"` (or `"{Name} | Meerut"` when exceeding 60 characters) plus a type-specific hooked meta description.
4. **Collection Descriptions:** Collection descriptions must be short editorial intros. Walls of keyword-stuffed text are prohibited.
5. **Delivery Parameters:** Local delivery strictly covers Meerut city within a ~15 km radius with a ₹350 minimum order. Merchant Center shipping must remain set to **Manual** (decoupled from Shopify shipping profiles).
6. **One Decision, One Document:** Consolidate related decisions into a single authoritative record; avoid fragmented NAP/policy file clusters.

## 4. Admin API & `seo-ops` Conventions

1. **Dry-Run by Default:** All Admin API scripts in `tbk-spfy-seo/ops/` must run in dry-run mode by default and output a review CSV. Require explicit `--apply` flag to commit mutations.
2. **Mutation Concurrency Limits:** Batch strictly ≤ 8–10 aliased mutations per GraphQL request to avoid HTTP/MCP gateway timeouts and rate-limit throttling.
3. **Atomic SEO Object Replacement:** When mutating SEO metadata, always provide **both** `seo.title` and `seo.description` together; omitting one clears it on Shopify.
4. **Data Fixes Before Theme Work:** Prioritize data/metafield fixes over theme changes—they are reversible, require no deployment downtime, and reach search indexes faster.

## 5. Deployment, Staging & Verification Rules

1. **Value Gate:** No change ships unless it measurably improves ≥ 1 of: UX, trust, conversion, SEO, GEO, accessibility, performance, maintainability, or scalability. No purely cosmetic changes without business value.
2. **Preview First:** All theme work must be built and validated on the preview theme (`#152070258857` or development theme `#152228004009`) before proposing live deployment.
3. **Surgical Deploy Protocol:**
   - Step 1: Pull live copy of the file from live theme `#152071602345` (or previous live `#151307485353`) to a temp path and diff against local:
     ```bash
     shopify theme pull --theme 152071602345 --store ae86ba-2a.myshopify.com --only sections/<file>.liquid --path <tmp> --force
     ```
   - Step 2: Push only that specific file to the live theme:
     ```bash
     shopify theme push --theme 152071602345 --store ae86ba-2a.myshopify.com --only sections/<file>.liquid --allow-live --force
     ```
4. **Bypass Cache on Verification:** Shopify CDN serves a full-page cache; verify live pushes with `?preview_theme_id=152071602345` and a cache-buster query parameter before declaring live verification complete.
5. **Rollback Restore Points:** Keep `theme_files/BACKUP-live-product.json` and git commit restore points intact before making theme adjustments.
6. **Lean Code Discipline (`ponytail`):** Avoid extraneous third-party JavaScript libraries or heavy slider plugins when native browser primitives (e.g., CSS scroll-snap) or Liquid features suffice.

## 6. Visionary Image Genome™ Platform Constitution (`VIG-000`)

1. **Images are Immutable:** Once an image is admitted to the platform, its bytes are never edited in place. Reprocessing produces a new observation against the same permanent identity (`TBK_*_ID`).
2. **Permanent Identifiers:** Every entity (image, product, observation) must have a permanent identifier assigned at admission that is never reused.
3. **Observations vs. Decisions:** Raw AI provider output is an observation (evidence), not ground truth. It requires confidence scoring and provenance metadata before promotion.
4. **No Business Logic in Prompts:** Prompts describe what to observe; they do not encode pricing rules or merchandising decisions that must be auditable independently.
5. **Taxonomy is Authoritative:** Visual features must map onto controlled vocabularies and standardized Shopify Metafields.
6. **Knowledge Graph as System of Record:** Downstream modules consume normalized Product Genome data, never raw AI vendor output directly.
7. **AI Providers are Interchangeable:** No module may depend on a specific AI vendor. Swapping models must not require rewriting consumer modules.

## 7. Framework & Environment Governance (`ENV_FRM_01`)

1. **Centralized Framework Toolchain Root:** All language runtimes, interpreters, and framework installations (including Python, Node, etc.) reside strictly within the dedicated frameworks directory: `F:\frameworks\` (e.g., `F:\frameworks\Python314`). Ad-hoc runtime installations across random paths or scattered virtual environments in the repository are strictly prohibited.
2. **Authoritative Environment Variable Mapping:** System and User-level environment variables (`PATH`, `PYTHON_HOME`, `PYTHONHOME`, `PYTHONPATH`) must point directly to `F:\frameworks\...`. Every agent and contributor must verify that execution environments resolve from `F:\frameworks\` prior to running tasks.
3. **Repository Tooling Invariant:** Every script in `tools-script/win/`, batch launcher (`.bat`), PowerShell runner (`.ps1`), Makefile, and automation harness must prioritize and target `F:\frameworks\` as the primary runtime path before falling back to system defaults.
4. **Dependency Integrity:** All project dependencies, PyTorch vision toolchains, transformers, pytest harnesses, and Admin API packages must be maintained directly within the centralized framework environment (`F:\frameworks\Python314\Lib\site-packages`).


