# Orphan Snippet Verification & Risk Classification (R4)

Continues from R3.5 (`2813e8b`). Scope: the 14 real orphan-snippet candidates from
`docs/LIQUID_ARCHITECTURE_AUDIT.md` Finding 3 (excluding `tbk-tokens.liquid`/`tbk-components.liquid`,
resolved by R0, and the 5 `-hulkapps-backup` snippets, resolved by R1) plus the 3 zero-reference
numbered-variant sections from Finding 4 (`testimonials-2.liquid`, `testimonials-3.liquid`,
`video-2.liquid`). **No files were removed this phase** — audit only, per instruction.

## Critical methodology finding: Theme Check's `OrphanedSnippet` detector is unreliable in both directions

Before classifying anything, every file was re-verified with a direct repo-wide `render`/`include`
grep — not just Theme Check's label — because two independent failures surfaced immediately:

1. **False "orphaned" (4 files actually live)**: `product-form-bundle.liquid`,
   `product-form-bundle2.liquid`, `product_tabs.liquid`, and `cake-addons.liquid` were all listed
   as orphaned in Finding 3, but a direct grep shows all four are genuinely rendered:

   | File | Rendered by |
   |---|---|
   | `product-form-bundle.liquid` | `main-product.liquid:523`, `main-product-premium.liquid:544`, `main-product-premium-v2.liquid:840` |
   | `product-form-bundle2.liquid` | `main-product.liquid:563`, `main-product-premium.liquid:584`, `main-product-premium-v2.liquid:894` |
   | `product_tabs.liquid` | `main-product.liquid:547`, `main-product-premium.liquid:568`, `main-product-premium-v2.liquid:864` |
   | `cake-addons.liquid` | `main-product.liquid:95`, `main-product-premium.liquid:111` (not the default v2 template) |

   The first three render on **`main-product-premium-v2.liquid`** — the default, protected product
   template used by 1,228 of 1,235 products. These are core, live, high-traffic features
   (bundle/"frequently bought together" upsell and the product-detail tabs), not dead code.
   **None of these four are touched in this phase; all four are reclassified ACTIVE.**

2. **False "not orphaned" (1 file actually dead, in the opposite direction)**: `shine-trust.liquid`
   is referenced by `layout/theme.liquid:201` — but via `{% include 'shine-trust.liquid' %}`,
   passing the snippet name **with** the `.liquid` extension. Standard Liquid `include`/`render`
   resolves `'name'` to `snippets/name.liquid`; passing `'shine-trust.liquid'` makes Shopify look for
   `snippets/shine-trust.liquid.liquid`, which does not exist. This is independently confirmed as a
   pre-existing, already-documented finding: `SEO_AUDIT_LEDGER.md`'s **P2-26** (found 2026-07-18,
   still open) — Theme Check's `MissingTemplate` check flags this exact line, and the finding states
   plainly: *"include fails silently in production, so a 78 KB trust-badge snippet has never
   rendered."* Status there: **"OWNER INPUT REQUIRED (decide on/off)"** — never resolved. Not
   touched this phase either; see classification below.

Given both failure directions, **every one of the 17 files in this document's scope was verified by
direct grep for a real `render`/`include`/`section type` reference**, not by trusting Theme Check's
label alone.

## Inventory & classification

| File | Referenced? | Rendered? | Schema/app/AJAX/JS/editor/metafield usage | Classification |
|---|---|---|---|---|
| `product-form-bundle.liquid` | Yes — 3 product templates | Yes, live | Real "Complete the Look" bundle upsell, uses `product.metafields.shopify--discovery--product_recommendation` | **ACTIVE** |
| `product-form-bundle2.liquid` | Yes — 3 product templates | Yes, live | Same "frequently bought together" family, second variant | **ACTIVE** |
| `product_tabs.liquid` | Yes — 3 product templates | Yes, live | Product description/reviews/additional-info/custom tabs; `tab_review` case renders `hdt-pr-single-review` (empty stub — see below) | **ACTIVE** |
| `cake-addons.liquid` | Yes — 2 of 3 product templates | Yes, live (not on the default v2 template) | Real feature: "Make it Extra Special" line-item-property checkboxes (Smoke Effect, Flying Butterflies, Balloon Parachute) | **ACTIVE** |
| `bk-datetime.liquid` | No live theme reference | Not currently rendered | Bespoke, brand-colored (TBK pink palette) delivery date + time-slot picker; **documented as an intended integration** in `design_handoff_shopify_product/CLAUDE_CODE_TASK.md` (`"custom_liquid": "{% render 'bk-datetime' %}"`) — a real, planned, not-yet-wired feature | **MANUAL REVIEW** |
| `shine-trust.liquid` | Referenced, but via a broken `{% include %}` (see above) | **No — silently fails** (`MissingTemplate`, pre-existing `SEO_AUDIT_LEDGER.md` P2-26) | 78KB of CSS only (bundle/"sold out" widget styling); no fabricated claims found (no rating/review/counter/urgency text) | **MANUAL REVIEW** (business decision: turn on vs. delete — not this project's call to make silently) |
| `hdt-pr-single-rating.liquid` | No | No | **Empty file (0 bytes)** | **SAFE TO REMOVE** |
| `delivery-date.liquid` | No | No | **Empty file (0 bytes)** | **SAFE TO REMOVE** |
| `meta-tags.liquid` | No | No | Confirmed (`diff`) a whitespace-only duplicate of the real, live `snippets/social-meta-tags.liquid` (rendered by `layout/theme.liquid`, `layout/password.liquid`, `templates/gift_card.liquid`); independently confirmed unreferenced in `SEO_AUDIT_LEDGER.md` (`"Zero hits — confirmed"`) | **SAFE TO REMOVE** |
| `type.liquid` | No (only self-reference inside its own usage-doc comment) | No | Generic product-type link utility, well-documented, no business claims | **SAFE TO REMOVE** |
| `product-btns.liquid` | No | No | Generic 3D-model/360°-view/zoom-gallery button utility; no fabrication risk | **SAFE TO REMOVE** |
| `product-thumbnail.liquid` | No | No | Generic gallery media-thumbnail renderer; no fabrication risk | **SAFE TO REMOVE** |
| `choose_style.liquid` | No | No | Leftover Ecomus demo content — repeats "Men's Long Sleeve Rash Guard" (a clothing product name) 7 times; irrelevant to a bakery, clearly unmodified demo boilerplate, not a business claim | **SAFE TO REMOVE** |
| `lookbook-card-product.liquid` | No | No | Generic reusable product-card component (price, badges, quick-view, `settings.show_rating`-gated `hdt-pr-card-rating`); no hardcoded claims | **SAFE TO REMOVE** |
| `testimonials-2.liquid` | No | No | Section schema has `"disabled_on": {"groups": ["*"]}` — Shopify-level lockout, cannot be added via the theme editor at all; default block content is generic Ecomus fashion-demo copy ("stylish and affordable plus size clothing", "Author's name") | **SAFE TO REMOVE** |
| `testimonials-3.liquid` | No | No | Same `disabled_on: ["*"]` lockout; same demo placeholder copy pattern | **SAFE TO REMOVE** |
| `video-2.liquid` | No | No | Same `disabled_on: ["*"]` lockout; default preset references a generic Ecomus demo YouTube video ("Share your brand story by adding a video to your store") | **SAFE TO REMOVE** |

## Fabrication-risk review (explicit focus per instruction: reviews, ratings, trust badges, testimonials, counters, customer numbers, awards, schema)

**No fabricated claims were found in any file in this document's scope.** Specifically:

- **`shine-trust.liquid`** (the file whose name most strongly suggested risk): read in full — it is
  CSS only (a `{% style %}` block), styling a bundle/cross-sell widget's "sold out" states. No
  rating, review, customer count, or urgency-counter text anywhere in it. It also never renders
  (broken include, see above), so even if it did carry risk, it isn't reaching customers.
- **`testimonials-2.liquid` / `testimonials-3.liquid`**: read in full. Default schema content is
  generic Ecomus theme-demo placeholder copy for a *different business vertical* (fashion/apparel:
  "a great selection of stylish and affordable plus size clothing"), with placeholder
  author name ("Author's name") — not a real name presented as a real customer, and no block
  instances exist in any live section group (both sections have never been added to a page). No
  fabricated Baking-Kaur-specific claim exists in either file.
- **`hdt-pr-single-rating.liquid`**: empty file — cannot carry fabricated content.
- **Bonus, directly relevant discovery (not in the original 14/3 scope, but surfaced by tracing
  `product_tabs.liquid`'s live `tab_review` case)**: `snippets/hdt-pr-single-review.liquid` — also
  **empty (0 bytes)**. This means the live, active `product_tabs.liquid`'s review-tab branch
  renders nothing even when configured, consistent with `REVIEW_STRATEGY.md`'s no-fabrication
  policy. Not proposed for removal in this phase (outside R4's scope), but noted as a positive
  confirmation.
- **Bonus discovery**: `snippets/hdt-pr-card-rating.liquid` (referenced by the dead
  `lookbook-card-product.liquid` and by ~19 live `card-product*.liquid` files, all gated behind
  `settings.show_rating`, which is `true` in `config/settings_data.json`) is **entirely a
  documentation comment** — integration instructions for third-party review apps (Judge.me,
  Stamped.io, Yotpo, rivyo, AliExpress Reviews Importer, Areviews, Ryviu). It renders **nothing** at
  runtime. Despite `show_rating` being enabled site-wide, no fabricated or real rating widget
  currently displays anywhere. This directly confirms the storefront carries zero star-rating
  content today, consistent with `REVIEW_STRATEGY.md` and the prior removal of the fabricated
  "4.9 Rated" claim (`36e1b0c`). Not a cleanup candidate (it's live-referenced infrastructure,
  currently a safe no-op) — noted for completeness given the instruction's explicit focus on rating
  snippets.

## Manual review list (2 items — genuine decisions, not simple dead-code)

| File | Why it needs a decision | Recommendation |
|---|---|---|
| `bk-datetime.liquid` | Real, bespoke, brand-styled delivery date/time-slot feature with a documented (unimplemented) integration plan. Given TBK's delivery-scheduling business model, this may be wanted, unfinished work — not junk. | Business/product decision: wire it in (a real future phase) or explicitly park it. Do not delete without that decision — deleting real unfinished work is different from deleting confirmed-dead demo boilerplate. |
| `shine-trust.liquid` (+ its broken include in `layout/theme.liquid:201`) | Pre-existing, already-flagged decision (`SEO_AUDIT_LEDGER.md` P2-26) never resolved: fix the include (turns on 78KB of bundle-widget CSS site-wide — a real visual/Core Web Vitals change) or delete both the include and the snippet. No fabrication risk either way, but "turn a dormant 78KB widget on" is a UI decision this audit should not make silently. | Recommend deletion (ponytail default, matching the pre-existing note's own suggestion) unless the bundle/cross-sell widget is actively wanted — but this is presented for confirmation, not assumed. |

## Safe-to-remove candidates (11 files) — evidence summary, NOT removed this phase

All 11 confirmed via direct repo-wide grep (0 real references) plus content read (no fabrication
risk, no undocumented planned-feature signal):

```
snippets/hdt-pr-single-rating.liquid   (empty, 0 bytes)
snippets/delivery-date.liquid          (empty, 0 bytes)
snippets/meta-tags.liquid              (confirmed duplicate of live social-meta-tags.liquid)
snippets/type.liquid                   (generic utility, 0 real refs)
snippets/product-btns.liquid           (generic utility, 0 refs)
snippets/product-thumbnail.liquid      (generic utility, 0 refs)
snippets/choose_style.liquid           (Ecomus demo leftover, 0 refs)
snippets/lookbook-card-product.liquid  (generic component, 0 refs)
sections/testimonials-2.liquid         (disabled_on: ["*"], demo content, 0 refs)
sections/testimonials-3.liquid         (disabled_on: ["*"], demo content, 0 refs)
sections/video-2.liquid                (disabled_on: ["*"], demo content, 0 refs)
```

## Cleanup recommendations (ordered)

1. **Do nothing to the 4 reclassified-ACTIVE files** — `product-form-bundle.liquid`,
   `product-form-bundle2.liquid`, `product_tabs.liquid`, `cake-addons.liquid`. Removing any of
   these would break a live feature on the default product template.
2. **Resolve the 2 manual-review items first**, before any deletion pass — `bk-datetime.liquid`
   (business decision on the unfinished feature) and `shine-trust.liquid` (on/off decision, already
   flagged pre-existing and unresolved).
3. **The 11 safe-to-remove files are the lowest-risk cleanup in this entire audit series** — zero
   live references (re-verified by direct grep, not just Theme Check), zero fabrication risk, zero
   business decision required. Recommended as a future **R5** removal pass, mirroring R3.5's
   pull→diff→delete→push→re-pull→diff pattern, one commit.

## Verification performed this phase

- Theme Check: baseline unchanged (354 files, 1,362 offenses/87 files, 1,162 errors, 200 warnings —
  same as R3.5's post-removal state), since no file was modified.
- Repository grep: every one of the 17 files re-verified individually via direct `render`/`include`/
  section-type search (not relying on Theme Check's `OrphanedSnippet` label, which proved unreliable
  in both directions — see above).
- `git diff`: none — this phase is audit-only, `docs/ORPHAN_SNIPPET_AUDIT.md` is the only new file.

## Related

[LIQUID_ARCHITECTURE_AUDIT.md](LIQUID_ARCHITECTURE_AUDIT.md) (Findings 3 & 4, superseded by this
document's re-verification), [TEMPLATE_CENSUS.md](TEMPLATE_CENSUS.md),
[../REVIEW_STRATEGY.md](../REVIEW_STRATEGY.md), [../SEO_AUDIT_LEDGER.md](../SEO_AUDIT_LEDGER.md)
(P2-26, the pre-existing `shine-trust.liquid` finding this phase corroborates independently).
