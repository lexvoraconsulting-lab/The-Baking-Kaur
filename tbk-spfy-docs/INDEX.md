# Master Documentation Index — The Baking Kaur Platform

Welcome to the enterprise knowledge base. Documentation is organized into functional engineering, strategy, audit, and architecture domains.

---

## 🧭 Governance & Meta
- [00_START_HERE](./00_START_HERE.md) — Single onboarding entry point & reading order
- [ARCHITECTURE](./ARCHITECTURE.md) — System & platform high-level architecture
- [CODING_STANDARDS](./CODING_STANDARDS.md) — Code quality & team conventions
- [DECISIONS](./DECISIONS.md) — Architectural decision log
- [RISK_REGISTER](./RISK_REGISTER.md) — Project risk register & mitigations
- [KNOWN_LIMITATIONS](./KNOWN_LIMITATIONS.md) — Technical debt & system boundaries
- [FILE_OWNERSHIP](./FILE_OWNERSHIP.md) — Codebase ownership map

---

## 📐 Technical Specifications (`specs/`)
* **Design System (`specs/design-system/`):**
  - [DESIGN_SYSTEM](./specs/design-system/DESIGN_SYSTEM.md) — Design tokens, typography, colors, grid
  - [COMPONENT_LIBRARY](./specs/design-system/COMPONENT_LIBRARY.md) — 19 UI component specifications
  - [ANIMATION_GUIDELINES](./specs/design-system/ANIMATION_GUIDELINES.md) — Motion & transition standards
  - [BRAND_VOICE](./specs/design-system/BRAND_VOICE.md) — Brand voice & tone principles
  - [COPY_GUIDELINES](./specs/design-system/COPY_GUIDELINES.md) — Microcopy, CTA, and grammar standards
  - [CONTENT_SYSTEM](./specs/design-system/CONTENT_SYSTEM.md) — Content model & layout rules
* **Shopify Theme Architecture (`specs/shopify-theme/`):**
  - [SHOPIFY_ARCHITECTURE](./specs/shopify-theme/SHOPIFY_ARCHITECTURE.md) — Online Store 2.0 theme stack
  - [HOMEPAGE_SPECIFICATION](./specs/shopify-theme/HOMEPAGE_SPECIFICATION.md) — Homepage structure & section rules
  - [HOMEPAGE_CONTENT_STRATEGY](./specs/shopify-theme/HOMEPAGE_CONTENT_STRATEGY.md) — Editorial content matrix
  - [ENTERPRISE_COLLECTION_ARCHITECTURE](./specs/shopify-theme/ENTERPRISE_COLLECTION_ARCHITECTURE.md) — Collection page system
  - [TEMPLATE_CENSUS](./specs/shopify-theme/TEMPLATE_CENSUS.md) — Census of all active theme templates
* **Data Model (`specs/data-model/`):**
  - [SCHEMA_MASTER](./specs/data-model/SCHEMA_MASTER.md) — Structured data (JSON-LD) master guide
  - [DATA_ARCHITECTURE](./specs/data-model/DATA_ARCHITECTURE.md) — Metafields, metaobjects, and data flow
  - [CATALOG_ARCHITECTURE](./specs/data-model/CATALOG_ARCHITECTURE.md) — Product hierarchy & variants
  - [INFORMATION_ARCHITECTURE](./specs/data-model/INFORMATION_ARCHITECTURE.md) — 5-year taxonomy roadmap
  - [URL_ARCHITECTURE](./specs/data-model/URL_ARCHITECTURE.md) — Canonical URL structures & handles

---

## 🎯 Commercial & Brand Strategy (`strategy/`)
* **Business & Merchandising (`strategy/business/`):**
  - [BUSINESS_MASTER](./strategy/business/BUSINESS_MASTER.md) — Core business model & product tiers
  - [TBK_BRAND_GUIDELINES](./strategy/business/TBK_BRAND_GUIDELINES.md) — Master brand identity standard
  - [MERCHANDISING_GUIDE](./strategy/business/MERCHANDISING_GUIDE.md) — Collection merchandising rules
  - [REVIEW_STRATEGY](./strategy/business/REVIEW_STRATEGY.md) — Review collection & rating governance
  - [COLLECTION_DOMINATION_STRATEGY](./strategy/business/COLLECTION_DOMINATION_STRATEGY.md) — Category SEO strategy
* **Roadmap & Phases (`strategy/roadmap/`):**
  - [PROJECT_ROADMAP](./strategy/roadmap/PROJECT_ROADMAP.md) — Comprehensive delivery roadmap
  - [VERSION](./strategy/roadmap/VERSION.md) — Version release milestones
  - [CHANGELOG](./strategy/roadmap/CHANGELOG.md) — Detailed historical ledger of all changes
* **Local Delivery & Geo (`strategy/delivery-geo/`):**
  - [FINAL_NAP_AND_MC_ARCHITECTURE](./strategy/delivery-geo/FINAL_NAP_AND_MC_ARCHITECTURE.md) — NAP & Merchant Center
  - [SEO_GEO_MASTER_PLAN](./strategy/delivery-geo/SEO_GEO_MASTER_PLAN.md) — Hyperlocal Meerut geo-targeting
  - [LOCAL_DELIVERY_SETUP_STEPS](./strategy/delivery-geo/LOCAL_DELIVERY_SETUP_STEPS.md) — Delivery configuration guide

---

## 🔍 Audits & Quality Control (`audits/`)
* **SEO & Indexing (`audits/seo/`):**
  - [SEO_AUDIT_LEDGER](./audits/seo/SEO_AUDIT_LEDGER.md) — 600+ product SEO rewrite ledger
  - [TECHNICAL_SEO_AUDIT](./audits/seo/TECHNICAL_SEO_AUDIT.md) — Site-wide crawl & technical findings
  - [SHOPIFY_SEO_REPORT](./audits/seo/SHOPIFY_SEO_REPORT.md) & [SCORECARD](./audits/seo/SHOPIFY_SEO_SCORECARD.md)
  - [STRUCTURED_DATA_REPORT](./audits/seo/STRUCTURED_DATA_REPORT.md) — Schema validation report
  - [AEO_READINESS](./audits/seo/AEO_READINESS.md) & [AI_SEARCH_READINESS](./audits/seo/AI_SEARCH_READINESS.md)
* **Performance (`audits/performance/`):**
  - [PERFORMANCE_AUDIT](./audits/performance/PERFORMANCE_AUDIT.md) — Full Core Web Vitals audit
  - [PERFORMANCE_BASELINE](./audits/performance/PERFORMANCE_BASELINE.md) — Target benchmarks & metrics
  - [PERFORMANCE_RECOMMENDATIONS](./audits/performance/PERFORMANCE_RECOMMENDATIONS.md) — Actionable optimizations
* **Accessibility (`audits/accessibility/`):**
  - [ACCESSIBILITY_AUDIT](./audits/accessibility/ACCESSIBILITY_AUDIT.md) & [SCORECARD](./audits/accessibility/ACCESSIBILITY_SCORECARD.md) — WCAG 2.1 AA audit
* **Quality & Security (`audits/quality-security/`):**
  - [LIQUID_ARCHITECTURE_AUDIT](./audits/quality-security/LIQUID_ARCHITECTURE_AUDIT.md) — Theme code review
  - [ORPHAN_SNIPPET_AUDIT](./audits/quality-security/ORPHAN_SNIPPET_AUDIT.md) — Dead snippet cleanup ledger
  - [SECURITY_AUDIT](./audits/quality-security/SECURITY_AUDIT.md) — App & token security posture
  - [404_AUDIT_COMPLETE](./audits/quality-security/404_AUDIT_COMPLETE.md) — Broken link resolution report

---

## 🚀 Release Engineering (`release/`)
* **Checklists (`release/checklists/`):**
  - [GO_LIVE_CHECKLIST](./release/checklists/GO_LIVE_CHECKLIST.md) — Production go-live gate
  - [DEPLOYMENT_CHECKLIST](./release/checklists/DEPLOYMENT_CHECKLIST.md) — Pre/post push checklist
  - [ROLLBACK_PLAN](./release/checklists/ROLLBACK_PLAN.md) — Emergency rollback protocol
* **Scorecards (`release/scorecards/`):**
  - [PRODUCTION_READINESS_FINAL](./release/scorecards/PRODUCTION_READINESS_FINAL.md) — Final sign-off
  - [ENTERPRISE_CERTIFICATION](./release/scorecards/ENTERPRISE_CERTIFICATION.md) — Architecture certification
* **Phase 7 (`release/phase-7/`):**
  - [PHASE7_EXECUTION_PLAN](./release/phase-7/PHASE7_EXECUTION_PLAN.md) & [TASK_BREAKDOWN](./release/phase-7/PHASE7_TASK_BREAKDOWN.md)

---

## 🧬 Enterprise Taxonomy & Knowledge Graph (`taxonomy/`)
* **Foundations (`taxonomy/foundations/`):** Governance constitutions, glossary, platform principles
* **Attributes (`taxonomy/attributes/`):** Attribute definitions, registry, normalization engine, API
* **Catalog (`taxonomy/catalog/`):** Controlled vocabulary, master taxonomy, dynamic discovery
* **Knowledge Graph (`taxonomy/knowledge-graph/`):** Entity model, relationship graph, graph query engine

---

## ⚙️ Operations & Setup
* [operations/DEPLOYMENT_GUIDE.md](./operations/DEPLOYMENT_GUIDE.md) — Deployment workflows & CLI usage
* [operations/QA_CHECKLIST.md](./operations/QA_CHECKLIST.md) — Quality assurance gates
* [setup/](./setup/) — VPS configuration, local environments, and Shopify CLI authentication
* [tasks/README.md](./tasks/README.md) — Current task backlog & sprint tracking
* [adr/](./adr/) — Formal Architecture Decision Records (001–011)
* [blog-os/](./blog-os/) — Editorial system & blog architecture

