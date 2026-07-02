# The Baking Kaur — Shopify Online Store 2.0 Product Page

Production-ready section-based product page. Drop the files into your theme, assign the template to a product, and configure everything from the Theme Editor.

## File map

```
shopify/
├─ templates/
│  └─ product.baking-kaur.json      → copy to  templates/
├─ sections/
│  ├─ bk-main-product.liquid        → copy to  sections/
│  ├─ bk-trust-strip.liquid         → copy to  sections/
│  ├─ bk-info-cards.liquid          → copy to  sections/
│  ├─ bk-reviews.liquid             → copy to  sections/
│  ├─ bk-related-products.liquid    → copy to  sections/
│  └─ bk-faq.liquid                 → copy to  sections/
└─ assets/
   ├─ baking-kaur.css               → copy to  assets/
   └─ baking-kaur.js                → copy to  assets/
```

The `shopify/` wrapper is only for organisation here — in your theme the folders are top-level (`sections/`, `templates/`, `assets/`).

## Install

1. **Upload files.** In your theme: *Edit code* → add each file under the matching top-level folder. (Or push with Shopify CLI: `shopify theme push`.)
2. **Fonts.** Add to `layout/theme.liquid` `<head>`:
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,500&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
   ```
3. **Assign the template.** Open a product → *Theme templates* → select **product.baking-kaur** (or set it as default in the JSON’s file name).
4. **Configure in the Theme Editor** (Customize → the product): rating text, WhatsApp number, time-slot options, review blocks, FAQ blocks, and the “You May Also Like” product list.

## Product data model (important)

| Design field   | Shopify mechanism            | Notes |
|----------------|------------------------------|-------|
| **Weight**     | Product **variant option**   | Drives price. Name the option exactly `Weight`. |
| **Flavour**    | Product **variant option**   | Name it `Flavour`. |
| **Delivery date** | Line-item **property**    | `properties[Delivery date]` |
| **Time slot**  | Line-item **property**       | Options set in section settings |
| **Message on cake** | Line-item **property**  | Optional text |

So in **Products → Variants**, create options `Weight` and `Flavour`, add the combinations and their prices. The buy box, price, sticky bar, and share-URL all update automatically via `baking-kaur.js`.

## What’s included

- **bk-main-product** — sticky gallery + thumbnails, rating pill, price, variant selects, date/slot/message properties, Add to Cart with live price, native Shopify Dynamic Checkout (Buy Now) button, WhatsApp CTA, mobile sticky bar, **Product JSON-LD**.
- **bk-trust-strip / bk-info-cards / bk-reviews / bk-related-products / bk-faq** — each a standalone, editable section with blocks. FAQ emits **FAQPage JSON-LD**.
- **baking-kaur.css / .js** — self-contained, no theme dependencies, no jQuery.

## Notes & recommendations

- **Money format:** the JS reads `Shopify.money_format` automatically. No change needed.
- **Reviews:** the blocks are for static/social-proof display. For live review data + rich snippets, connect an app (Judge.me, Loox, Okendu) and swap the `bk-reviews` grid for the app’s block.
- **LocalBusiness / GEO schema:** add a `Bakery` JSON-LD snippet in `theme.liquid` with your real address, phone, geo-coordinates, and hours — this belongs site-wide, not per product.
- **Wishlist** button is visual only; wire `data-bk-wish` to your wishlist app if used.
- **Alt text:** upload real product photos with descriptive alt text in the admin — the section already outputs it.

## Placeholders to replace before launch

- WhatsApp number (`91XXXXXXXXXX`) in section settings.
- Real product images, variants, and prices.
- Your Bakery/LocalBusiness JSON-LD (address, phone, coordinates) in `theme.liquid`.
