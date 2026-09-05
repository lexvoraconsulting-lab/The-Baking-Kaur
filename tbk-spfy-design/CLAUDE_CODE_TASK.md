# Claude Code Task — The Baking Kaur Product Page

You are working inside the Shopify theme repo at `F:\Shopify\The-Baking-Kaur`
(theme: **TheBakingKaur-Pink-Gold-Grey-theme**, a premium OS 2.0 theme).
Store handle: `ae86ba-2a.myshopify.com`. Primary domain: thebakingkaur.com.

Your job: get the product page to match the design mockups in `reference_mockups/`
**without breaking the theme's existing native features**, and deploy to an
UNPUBLISHED draft the owner can preview and publish.

---

## Ground truth about the current page (already inspected)

The live `templates/product.json` already implements ~95% of the target design using
the theme's native `main-product` section + blocks, in this order:
`title → price → custom_liquid "Rating" → custom_liquid "Delievery" (eggless/delivery pills)
→ variant_picker → custom_liquid "Date Time Picker" (EMPTY) → custom_liquid "WhatsApp Button"
→ buy_buttons (dynamic checkout + wishlist) → linked_products → bundle_product`,
then `main-product-tabs` (About This Cake / Delivery & FAQ), then `related-products`.

Media layout is already **image-left, thumbnails-left, 65% media width**.

**The one real gap:** the "Date Time Picker" custom_liquid block is empty.

Colors already in use: rose `#7a2147`, pill bg `#fff7f8`, pill border `#f2d6dd`,
WhatsApp `#25D366`. Match these — do NOT introduce a new palette.

---

## Files provided in `theme_files/`

- `snippets/bk-datetime.liquid` — styled Delivery Date + Time Slot picker (line-item
  properties `Delivery Date` and `Time Slot`). **Already uploaded to the draft theme
  "Copy of TheBakingKaur-Pink-Gold-Grey-theme" via API** — but also copy it into the repo.
- `sections/bk-*.liquid`, `assets/baking-kaur.*`, `templates/product.baking-kaur.json`
  — a full parallel implementation of the design as standalone sections. OPTIONAL. Only
  use these if the owner explicitly wants to REPLACE the native product page (this loses
  native zoom, variant picker, tabs, bundles — a feature downgrade). Default: do NOT use these.
- `snippets/bk-local-business.liquid` — Bakery/LocalBusiness JSON-LD for site-wide SEO.
- `BACKUP-live-product.json` — a backup of the live product template. Keep it.

---

## Recommended plan (keeps native features, matches design)

### 1. Safety first
```powershell
git status
git add -A && git commit -m "checkpoint before Baking Kaur design changes"   # if repo is git-tracked
# also keep theme_files/BACKUP-live-product.json as the restore point
```

### 2. Add the date/time picker
```powershell
Copy-Item .\theme_files\snippets\bk-datetime.liquid .\snippets\
```
Then edit `templates/product.json`: find the block
`"custom_liquid_4rGhVM"` (name "Date Time Picker") and set its value:
```json
"custom_liquid": "{% render 'bk-datetime' %}"
```
(It is currently `"custom_liquid": ""` — the ONLY empty custom_liquid in the file.)

### 3. Add site-wide SEO schema
```powershell
Copy-Item .\theme_files\snippets\bk-local-business.liquid .\snippets\
```
Add inside `<head>` of `layout/theme.liquid`:
```liquid
{% render 'bk-local-business' %}
```
⚠ Update the geo latitude/longitude in that snippet to the exact shop pin from Google Maps
(current values are approximate for Thapar Nagar, Meerut).

### 4. Fonts (if not already loaded) — inside `<head>` of `layout/theme.liquid`
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,500&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
```

### 5. Push to a DRAFT and preview (never overwrite live)
```powershell
shopify theme push --unpublished --theme "Baking Kaur — Draft"
shopify theme dev --store ae86ba-2a.myshopify.com   # local hot-reload preview
```

### 6. Product setup (Shopify admin)
Ensure products have variant options named exactly **Weight** and **Flavour** with prices
(Weight drives price). Date/Time/Message ride along as line-item properties — verify they
appear in the cart and on the order.

### 7. Publish only after the owner approves the draft
```powershell
shopify theme publish
```

---

## Layout-matching checklist (compare to reference_mockups/)

Open `reference_mockups/desktop-product-page.html` and `mobile-product-page.html` in a
browser. Compare against the draft preview and reconcile only real differences:

- [ ] Rating shown as a compact gold/rose pill: ★ 4.8 · 500+ Reviews
- [ ] Price sits directly under the title, rose `#7a2147`, not oversized
- [ ] Eggless / Same-Day / Freshly-Made pills present under price
- [ ] Weight + Flavour selectors boxed and aligned (native variant_picker, `picker_type: block`)
- [ ] Delivery Date + Time Slot row present and aligned with the selectors (the new snippet)
- [ ] Primary CTA = ADD TO CART with price; WhatsApp button below; dynamic checkout on
- [ ] Trust row: Same-Day · 4.8 Google · FSSAI · 100% Eggless
- [ ] About / Perfect For / Delivery-in-Meerut content lives in the tabs or info cards
- [ ] Reviews + FAQ present toward the bottom; Related products last

If a native setting can achieve the mockup (spacing, media width, columns), prefer editing
`templates/product.json` settings over adding custom code.

---

## Do NOT
- Do not push straight to the live/MAIN theme. Draft only until approved.
- Do not replace `templates/product.json` wholesale with `product.baking-kaur.json` unless
  the owner explicitly wants to drop native features.
- Do not invent new brand colors.
- There is a leftover `snippets/bk-test.liquid` in the draft theme (harmless) — you may
  delete it from the repo/theme.
