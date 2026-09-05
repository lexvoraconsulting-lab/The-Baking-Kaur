# Missing Assets — TBK Homepage

**Last updated:** 2026-08-14
**Homepage status:** Built and rendering. Hero is image-led. No blank hero.

---

## 1. Hero image — RESOLVED (interim)

**Status:** ✅ Wired and verified rendering.

The hero now renders real TBK photography, sourced from the store's own Shopify
Files library:

| Field | Value |
|---|---|
| Asset | `shopify://shop_images/classic-strawberry-whipped-cream-cake-meerut-the-baking-kaur_webp.webp` |
| Origin | Featured image of product `b32` — Classic Strawberry Whipped Cream Cake |
| Dimensions | 1196 × 1600 (portrait, 3:4) |
| Format | WebP |
| Alt text | Inherited from the asset: "Classic Strawberry Whipped Cream Cake — eggless anniversary cake by The Baking Kaur, Meerut" |
| Loading | `eager` + `fetchpriority="high"` (LCP) |
| Responsive | srcset 400–3200px, `sizes="100vw"` |
| Desktop height | Fixed 780px |
| Mobile height | Fixed 560px |

**Why fixed heights, not `adapt_image`:** the asset is portrait (0.75 ratio). At
full-bleed width with `adapt_image`, a 1920px viewport would render a ~2560px-tall
hero. Fixed heights + `object-fit` crop keep the hero at a usable height on every
breakpoint.

**Why this asset:** it is the only catalogue image verified free of Zomato/TWC
watermarks, piped customer names, and third-party branding. Selected per the
approved spec as the official *temporary* production hero.

**No local repository photography exists.** `assets/` contains only UI assets
(`flavor-icons.png`, `no-image.svg`). `ai/vision/images/{1,2,3}.png` are
vision-model smoke-test samples, explicitly not a production image store
(see `ai/vision/images/README.md`). `design/` and
`design_handoff_shopify_product/` contain documentation and code only — no imagery.

---

## 2. Flagship hero photography — STILL REQUIRED

The current hero is a product shot standing in for a real hero. It works, but it
is not an editorial hero composition. Replacing it is a settings change with
**zero code cost** — set the image in the theme editor, or update
`templates/index.json` → `sections.hero.settings.image`.

### Exact requirement

| Spec | Value |
|---|---|
| Filename | `tbk-homepage-hero-desktop.webp` |
| Desktop dimensions | 2880 × 1620 minimum (16:9 landscape) |
| Mobile variant | `tbk-homepage-hero-mobile.webp`, 1080 × 1350 (4:5 portrait) |
| Aspect ratio | 16:9 desktop · 4:5 mobile |
| Subject | One premium designer or occasion cake, hero-lit, as the single focal object |
| Composition | Cake positioned right-of-centre (desktop) / lower third (mobile) |
| Focal point | On the cake's top tier |
| Text-safe area | Left 45% (desktop) / top 40% (mobile) kept low-detail for the H1, subheading and two CTAs |
| Background | Warm ivory / cream / soft blush, or a clean natural studio set |
| Lighting | Soft directional key, editorial quality, no harsh flash |
| Must not contain | Watermarks, customer names, third-party branding, other studios' marks |
| Alt text | `Designer eggless celebration cake by The Baking Kaur, Meerut` |

Once supplied: upload to Shopify Files, then set `sections.hero.settings.image`
(and `image_mb` for the mobile crop). With a 16:9 asset, `image_height` may be
returned to `adapt_image`.

---

## 3. Testimonials — BLOCKED, section removed from the homepage

**Status:** ⛔ Not on the page.

Zero verified customer reviews exist. Per the standing project rule, fabricated
testimonials are permanently off the table, and a testimonials section with no
quotes renders as an empty band. The section has therefore been **left out of
`templates/index.json` `order`** rather than shipped empty.

**To enable:** supply at least 3 real reviews (transcribed Google Business Profile
reviews with `source_url`, or Judge.me verified-buyer reviews). Then re-add a
`testimonials` section with `quote` blocks — the section type exists and is ready.

---

## 4. Collections referenced but not present in Shopify

The original homepage draft pointed at four collections that do not exist. Those
references were replaced with real, populated collections so no section renders
empty:

| Originally referenced | Exists? | Now using | Products |
|---|---|---|---|
| `romantic-cakes` | ✗ | `wedding-cakes` | 134 |
| `kids-cakes` | ✗ | `designer-theme-cakes` | 165 |
| `surprise-hampers` | ✗ | `cake-hampers` | 119 |
| `celebration-hampers` | ✗ | `cake-hampers` | 119 |
| `best-sellers` | ✗ | `best-selling-products` | 1235 |
| `hampers` (CTA target) | ✗ | `cake-hampers` | 119 |

If the missing collections are later created, swap the handles back in
`templates/index.json`. No code change needed.

---

## 5. FSSAI licence number — STILL REQUIRED

The storefront claims "FSSAI approved" with no number. This is a checkable entity
fact and high trust-per-effort. Supply the licence number to display it.

---

## Deployment status

| Item | Status |
|---|---|
| Hero renders a real image | ✅ Verified in preview |
| Blank hero possible? | ❌ No — image set; gradient emergency fallback retained |
| Shopify validation errors | ✅ 0 |
| Blocking for launch | Flagship photography (quality), FSSAI number (trust), reviews (S5) |
