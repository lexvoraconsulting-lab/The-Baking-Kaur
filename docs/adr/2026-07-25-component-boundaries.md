# ADR 0001: Component Boundaries

Date: 2026-07-25

## Status

Accepted

## Context

This repository is evolving from a single Shopify theme into a reusable commerce platform. That means the codebase must support multiple page families, including collections, products, blogs, buying guides, local landing pages, corporate pages, campaign pages, and seasonal landing pages without baking business knowledge into reusable UI components.

The architecture needs a stable separation of concerns so future work can scale without duplication, hidden coupling, or page-specific logic leaking into shared modules.

## Decision

The repository follows these component boundaries:

- Templates own page composition.
- Sections own reusable feature modules.
- Snippets own UI primitives.
- Assets own presentation.
- Business content belongs only in templates, theme settings, JSON, or merchant data.
- Reusable Liquid components must remain domain-agnostic.

Reusable components must not encode business entities, category names, product-family names, or collection-specific assumptions. If page-specific data is needed, the template must pass it into the reusable component.

## Consequences

- Shared modules can be reused across current and future commerce experiences without modification.
- Page-specific logic stays visible in templates where it can be audited, tested, and replaced independently.
- Merchant-editable content remains editable through the Theme Editor or JSON config rather than being hardcoded in shared Liquid.
- The repository can support new page types without creating duplicate sections for each business line.

## Example

The generic content builder used on the Gourmet Cookie Desserts collection is intentionally domain-agnostic. It renders configurable blocks only and does not infer or fetch business content on its own. The collection template assembles the page around it.

## Notes

This ADR is a permanent repository standard and applies to all future theme work unless explicitly superseded by a later ADR.
