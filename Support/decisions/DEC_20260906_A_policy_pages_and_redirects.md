<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../skills/ThemeStyleOps/assets/banners/lexvora/decisions-dark.svg">
  <img alt="Decisions" src="../../skills/ThemeStyleOps/assets/banners/lexvora/decisions-light.svg" width="100%">
</picture>

# DEC_20260906_A — Policy Pages Consolidation and URL Redirection

> **Date:** 2026-09-06 · **Status:** Accepted · **Scope:** Storefront Policies & SEO

---

## Context

Audit findings in `tbk-spfy-seo/audit/final/` identified multiple duplicate and conflicting policy URLs (`/pages/privacy-policy` vs `/policies/privacy-policy`, `/pages/refund-policy` vs `/policies/refund-policy`, `/pages/shipping-policy` vs `/policies/shipping-policy`).

## Decision

1. **Canonical Destination:** Standardize exclusively on Shopify native `/policies/*` routes (`/policies/refund-policy`, `/policies/privacy-policy`, `/policies/terms-of-service`, `/policies/shipping-policy`).
2. **Permanent 301 Redirects:** Establish 301 redirects mapping all legacy `/pages/*-policy` handles directly to their respective `/policies/*` endpoints via Shopify Admin Navigation URL Redirects.
3. **Menu & Footer Synchronization:** Update `sections/site-footer.liquid` and navigation menus to link strictly to `/policies/*`.

## Consequences

- Eliminates duplicate content warnings in Google Search Console.
- Consolidates fragmented policy documentation files (`POLICY_ARCHITECTURE.md`, `POLICY_CONSOLIDATION.md`, `POLICY_REDIRECT_PLAN.md`) into this single decision record.\n