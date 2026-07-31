# CONTENT_SYSTEM.md — The Baking Kaur

**Cross-reference (added 2026-07-31, Phase 7.0 reconciliation)**: `design/CONTENT_SYSTEM.md` is a
later, code-verified companion documenting page-level content structure — read both; see
`docs/CANONICAL_SOURCES.md`.

The content model: editor-managed structured content via metaobjects + metafields, so sections carry no hardcoded copy/data. Copy source = `HOMEPAGE_CONTENT_STRATEGY.md`; consumed by sections per `HOMEPAGE_SPECIFICATION.md`.

## Principle
Content is data, not markup. Merchant edits content in Shopify admin (metaobjects/section settings); Liquid only renders. No copy baked into `.liquid`.

## Metaobject definitions
| Definition | Fields | Powers |
|---|---|---|
| `home_hero_slide` | headline, subtext, cta_label, cta_url, image_desktop, image_mobile, alt | Hero |
| `occasion_tile` | title, image, url, blurb | Occasions |
| `testimonial` | author, rating(int 1–5), body, avatar(image), source(Google/Zomato), verified(bool), date | Reviews |
| `trust_stat` | value ("20,000+"), label, icon | Trust rows/credibility |
| `craft_step` | title, body, image | Craft story |

## Metafields
| Owner | namespace.key | Type | Used by |
|---|---|---|---|
| Product | `custom.is_bestseller` | boolean | Bestsellers fallback |
| Product | `custom.badge` | single_line_text | card badge |
| Product | `custom.same_day_eligible` / `custom.midnight_eligible` | boolean | delivery cues |
| Product | `custom.occasion` / `custom.flavor` / `custom.theme` | list.single_line_text | facets/link band |
| Collection | `custom.subtitle` | single_line_text | tiles/hero |
| Collection | `custom.hero_image` | file_reference(image) | tiles/cards |

## Rules
- Every homepage data point maps to a metaobject entry, metafield, or section setting — never a literal string in Liquid.
- Sections degrade gracefully when content missing (see empty states in `HOMEPAGE_SPECIFICATION.md`).
- Copy changes: edit `HOMEPAGE_CONTENT_STRATEGY.md` → update metaobject/setting (single source discipline).
- Naming: `custom` namespace for merchant metafields; metaobject handles kebab-case.

_v0.1 — content model for homepage build._
