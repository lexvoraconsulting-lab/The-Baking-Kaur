# The Baking Kaur — Shopify & E-Commerce Platform

Repository for **The Baking Kaur**, a 100% eggless luxury cake studio in Meerut, Uttar Pradesh.

---

## Project Structure Overview

```
The-Baking-Kaur/
├── assets/ config/ layout/ locales/ sections/ snippets/ templates/  # Active Shopify Theme (Online Store 2.0)
│
├── ai/                                                              # AI Cake Genome & Vision Intelligence (Python)
├── seo-ops/                                                         # Shopify Admin GraphQL Automation & SEO scripts
├── n8n/                                                             # n8n workflows & automation packages
│
├── docs/                                                            # Centralized Knowledge & Blueprint Hub
│   ├── 00_START_HERE.md                                             # Foundation & reading order
│   ├── specs/                                                       # Design System, Component Library, Liquid Specs
│   ├── strategy/                                                    # Brand Guidelines, Business Master, Roadmaps, NAP
│   ├── audits/                                                      # SEO Ledgers, 404 Audits, Accessibility & CWV
│   └── operations/                                                  # Deployment guides, checklists, collections setup
│
├── archive/                                                         # Historical & Staging Artifacts
│   ├── theme-snapshots/                                             # Backups of downloaded live themes
│   ├── verification-steps/                                          # Step-by-step verification staging artifacts
│   └── logs/                                                        # Large theme-check logs & audit outputs
│
├── CLAUDE.md                                                        # Agent guidance & golden rules
└── README.md                                                        # Project entry point
```

---

## Store Facts

| Parameter | Details |
| :--- | :--- |
| **Storefront** | [thebakingkaur.com](https://thebakingkaur.com) |
| **Admin Store** | `ae86ba-2a.myshopify.com` |
| **Live Theme** | `Baking Kaur — Draft` (`#151307485353`) |
| **Theme Architecture** | Ecomus v1.6.1 (Halo/The4 "hdt-" family), Online Store 2.0 |
| **Catalogue** | ~1,235 products (≈602 active, remainder draft/archived) · 100% Eggless |
| **Market** | Meerut, UP — Local delivery within ~15 km |

---

## Golden Rules

See [CLAUDE.md](CLAUDE.md) for full operational instructions.
- **Product page is a protected module** — No visual/UX/flow/CSS/JS changes. Only invisible enhancements (structured data, analytics, accessibility, performance) are permitted.
- **Preserve** the logo and canonical brand colors.
- **Never** invent GTINs, MPNs, barcodes, fake reviews, or delivery promises the store cannot fulfill.
- **Drafts stay drafts** — Do not bulk-flip DRAFT → ACTIVE.

---

## Documentation Index

Start at [`docs/00_START_HERE.md`](docs/00_START_HERE.md) or explore key documentation categories:
* **Design & Specs:** [`docs/specs/DESIGN_SYSTEM.md`](docs/specs/DESIGN_SYSTEM.md) · [`docs/specs/COMPONENT_LIBRARY.md`](docs/specs/COMPONENT_LIBRARY.md) · [`docs/specs/HOMEPAGE_SPECIFICATION.md`](docs/specs/HOMEPAGE_SPECIFICATION.md)
* **Strategy & Brand:** [`docs/strategy/BUSINESS_MASTER.md`](docs/strategy/BUSINESS_MASTER.md) · [`docs/strategy/TBK_BRAND_GUIDELINES.md`](docs/strategy/TBK_BRAND_GUIDELINES.md) · [`docs/strategy/PROJECT_ROADMAP.md`](docs/strategy/PROJECT_ROADMAP.md)
* **Audits & Ledgers:** [`docs/audits/SEO_AUDIT_LEDGER.md`](docs/audits/SEO_AUDIT_LEDGER.md) · [`docs/audits/404_AUDIT_COMPLETE.md`](docs/audits/404_AUDIT_COMPLETE.md)
* **Operations & Deploy:** [`docs/operations/DEPLOYMENT_GUIDE.md`](docs/operations/DEPLOYMENT_GUIDE.md) · [`docs/operations/QA_CHECKLIST.md`](docs/operations/QA_CHECKLIST.md)
