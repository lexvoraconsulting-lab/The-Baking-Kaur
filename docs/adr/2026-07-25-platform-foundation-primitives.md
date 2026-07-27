# ADR 0002: Platform Foundation Primitives

Date: 2026-07-25

## Status

Accepted

## Context

The repository is moving from a single bespoke storefront toward a reusable commerce platform. Future work needs a stable component foundation that can support many page families without repeating layout, button, card, or media patterns in each section.

The generic content builder already showed that reusable page modules work best when templates own composition and shared components stay domain-agnostic. The next step was to make the primitive layer explicit and load it globally.

## Decision

The theme now includes a generic platform foundation rendered once from the layouts:

- `snippets/tbk-tokens.liquid` owns the design tokens.
- `snippets/tbk-components.liquid` owns reusable layout and UI primitives.
- `snippets/tbk-button.liquid` owns the generic button renderer.

These primitives are loaded centrally so every future page can compose from the same foundation without duplicating CSS or button markup. The primitives remain domain-agnostic and do not infer business entities or page-specific content.

## Consequences

- Future landing pages can reuse the same button, card, grid, split, FAQ, and media primitives.
- Shared CSS stays centralized instead of being copied into sections.
- Templates remain responsible for business composition, while snippets stay focused on presentation primitives.
- The platform can expand without creating parallel component systems for each category or page family.

## Notes

This ADR reinforces the permanent repository standard defined in ADR 0001: reusable components must remain domain-agnostic and business content must live in templates, settings, JSON, or merchant data.
