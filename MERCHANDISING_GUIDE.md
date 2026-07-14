# MERCHANDISING_GUIDE.md — The Baking Kaur

Rules for what products/collections appear where, and how. Applies to homepage + collection + cross-sell. Copy context in `HOMEPAGE_CONTENT_STRATEGY.md`; hierarchy in `INFORMATION_ARCHITECTURE.md`.

## Live catalog anchors (source counts)
Pillars: Birthday 279 · Anniversary 102 · Wedding 134 · Designer/Theme 165 · Cake Hampers 119 · Festive (Diwali 44, Winter Strawberry 23). Bestsellers pool: `best-selling-products`. Theme subs: Unicorn/Jungle/Butterfly/Baby-Girl/Motu-Patlu/Cricket/KPOP/Roblox/Teddy/Paw-Patrol/Bow.

## Homepage merchandising
| Slot | Source | Why | KPI | Sort | Cap | Seasonality | Fallback |
|---|---|---|---|---|---|---|---|
| Occasions | 5 pillar collections | primary intents | tile CTR | fixed curated | 5 | Corporate→Festive in season | hide empty tile |
| Bestsellers | `custom.is_bestseller` → `best-selling-products` | proven demand | add-to-cart | best-selling | 8 | feature seasonal bestseller | metafield→collection→hide |
| Hampers | `cake-hampers` (+ `luxury-diwali-hampers`) | AOV | hamper CTR/AOV | best-selling/manual | 4–6 | Diwali swap | hide if empty |
| Link band | pillars+guides (links) | SEO equity | internal CTR | IA order | — | seasonal link | n/a |

## Global rules
- **Never render an empty grid** — every slot self-hides or falls back.
- **Caps enforced** to protect performance + focus.
- **Delivery cue:** show "Same-Day eligible" from `custom.same_day_eligible`.
- **Cross-sell:** hampers surfaced from every cake collection (AOV); related-collections = siblings + one cross-axis.
- **Seasonality calendar:** Diwali (Oct–Nov) → festive hampers; Winter (Dec–Feb) → Winter Strawberry; Valentine/Rakhi/Christmas → seasonal collections surfaced on home + relevant pillars, evergreen URLs retained off-season.
- **Bestseller governance:** curate via `custom.is_bestseller` (manual editorial control) with automatic `best-selling-products` fallback; review monthly.
- **No dark patterns:** no fake scarcity/countdowns on premium surfaces.

## Collection sourcing priority (PDP breadcrumb & "part of")
Occasion > Theme > Flavor.

_v0.1 — merchandising rules for build phases._
