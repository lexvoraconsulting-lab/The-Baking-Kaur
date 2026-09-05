# Site Tree — Current (As-Built) and Target (Production)

Generated 2026-07-30, BUILD-020. Grounded in a live re-query of Collections, Pages, and Menus via
the Admin API this pass — not a re-statement of prior audits. Companion to
[WEBSITE_ARCHITECTURE.md](WEBSITE_ARCHITECTURE.md); see that document for the reasoning behind each
change below. No handles are renamed here (per `CLAUDE.md`'s deferred handle-optimization policy —
live URLs are not touched by a planning document).

## Part 1 — Current tree, as it actually exists today

```
/ (Home — currently unpublished custom "Home" page exists but this is the storefront's real front page)
├── /collections/all (1,235 products)
├── /collections/best-selling-products  (1,235 — NOT a real curation, identical count to /all)
├── /collections/newest-products        (1,235 — NOT a real curation, identical count to /all)
├── /collections/birthday-cakes         (279)
├── /collections/anniversary-cakes      (102)
├── /collections/wedding-cakes          (134)
├── /collections/designer-theme-cakes   (165)
│   ├── /collections/baby-girl (28)          ┐
│   ├── /collections/butterfly (23)          │
│   ├── /collections/criciket (10, typo'd handle) │  13 theme sub-collections, not
│   ├── /collections/motu-patlu (12)         │  nested under designer-theme-cakes
│   ├── /collections/unicorn (16)            │  in Shopify's collection model
│   ├── /collections/jungle-animal-theme (17)│  (Shopify collections don't nest) —
│   ├── /collections/chartered-accountant(10)│  grouped here logically, not
│   ├── /collections/roblox (8)              │  structurally
│   ├── /collections/paw-petrol (4)          │
│   ├── /collections/teddy (7)               │
│   ├── /collections/ribbon-cake (8)         │
│   ├── /collections/kpop-cake (9)           │
│   └── /collections/boy-or-girl-cake (12)   ┘
├── /collections/cake-hampers           (119)
│   └── /collections/luxury-diwali-hampers (44)
├── /collections/for-him (11), /collections/for-her (1)
├── /collections/photo-cakes (4), /collections/flowers-cake-combos (1)
├── /collections/showstopper-wedding-cake (78, titled "Surprise Cake Setup with Revolving Cake")
├── /collections/winter-strawberry-collection (23)
├── /collections/gourmet-cookies-meerut (4)
├── ⚠ 7 near-duplicate "Meerut" collections, all showing 986 products (i.e. all essentially the
│   same underlying set, tagged for keyword variations, not real distinct merchandising):
│   /collections/cakes, /collections/cake-delivery-meerut,
│   /collections/same-day-cake-delivery-meerut, /collections/midnight-cake-delivery-meerut,
│   /collections/midnight-cake-delivery (986 — same count, different handle again),
│   /collections/custom-cakes-meerut (617 — the one outlier count),
│   /collections/kids-birthday-cakes-meerut (128)
├── /pages/about-us (live)
├── /pages/contact (live, "Contact Us")
├── /pages/frequently-asked-questions-faqs (live — real content as of SEO-013)
├── /pages/100-percent-eggless-bakery (live)
├── /pages/cake-delivery-in-meerut (live)
├── /pages/30-minute-cake-delivery-in-meerut-premium-reliable-service (live)
├── /pages/midnight-cake-delivery (live)
├── /pages/gift-hampers (live)
├── /pages/customised-hampers-meerut (live)
├── /pages/festive-hampers-meerut (live)
├── /pages/surprise-hampers-meerut (live)
├── /pages/photo-cakes (live)
├── /pages/theme-cakes (live)
├── /pages/terms-and-conditions (live, ⚠ empty body — SEO-034)
├── /pages/refund-return-policy (live, "Refund & Return Policy" — canonical candidate per POLICY_ARCHITECTURE.md)
├── /policies/privacy-policy, /policies/refund-policy, /policies/shipping-policy,
│   /policies/terms-of-service, /policies/contact-information (Shopify Shop Policies — 4 of 5
│   conflict with the above per POLICY_CONSOLIDATION.md, not restated here)
├── /pages/return-refund-replacement-policy (unpublished draft, duplicate of refund-return-policy)
├── /pages/store-locator (unpublished, fake London/Madrid/Tokyo content — SEO-030)
├── /pages/corporate-gifting-solutions (unpublished, empty body — stub)
├── /pages/delivery-information (unpublished, empty/unchecked this pass)
├── /pages/midnight-surprise-delivery (unpublished)
├── /pages/why-choose-the-baking-kaur (unpublished)
├── /pages/cake-customization-guide (unpublished)
├── /pages/freshness-guarantee (unpublished)
├── /pages/theme-cake-1 (unpublished)
├── /pages/data-sale-opt-out ("Your Privacy Choices", unpublished — CCPA/GPC opt-out)
├── /pages/rewind-menu-backup-page (dead, "do not delete" backup artifact)
└── No blog exists (no blog template, no blog page)
```

### Menu inventory (real, current — a second orphaned-content pattern, distinct from pages)

| Menu handle | Items | Actually wired to a live section? |
|---|---|---|
| `main-menu` | Home, About Us, Contact Us, Categories (→ `/collections`) | **Yes** — `tbk_header_main`'s `main_menu` setting, the live header |
| `header` | Birthday, Anniversary, Diwali Hampers, Theme Cakes, Hampers, Wedding Cakes (6 real collection links) | **No** — only referenced by a `disabled: true` block (`header_menu_bottom_hulkapps_backup`) |
| `footer` | Search, Contact Us, Privacy/Shipping/Refund Policy, Your Privacy Choices | Not directly — the live footer (`site-footer.liquid`) hardcodes its own links instead of rendering this linklist (see `INTERNAL_LINKING.md`) |
| `quick-links-menu` | FAQ's, Privacy/Refund/Shipping Policy (as `SHOP_POLICY` type — correct), Terms & Condition (→ the empty page) | Not confirmed wired to anything live |
| `about-us-menu` | About Us, Contact Us, Store Locations (→ the unpublished fake Store Locator page) | Not confirmed wired; if it is live anywhere, it 404s on its third item |
| `explore-cakes`, `quick-links`, `meerut-delivery` | **Empty — zero items** | N/A — dead menu shells, likely from an earlier, abandoned navigation attempt |

**This is the real story worth naming plainly**: the site has *more real navigational content already
built* (a 6-collection menu, a quick-links menu with correctly-typed policy links, an empty
`meerut-delivery` menu shell clearly intended for exactly the kind of delivery-area navigation this
BUILD is now designing) **than is actually wired into the live theme.** Production architecture
should reuse this existing infrastructure, not invent new menu handles alongside it.

## Part 2 — Target tree (production architecture)

```
/
├── / (Home) — see WEBSITE_ARCHITECTURE.md §5
├── /collections
│   ├── /collections/birthday-cakes
│   ├── /collections/anniversary-cakes
│   ├── /collections/wedding-cakes
│   ├── /collections/designer-theme-cakes
│   │   └── 13 theme sub-collections (unchanged — real, distinct, keep as-is)
│   ├── /collections/cake-hampers
│   │   └── /collections/luxury-diwali-hampers  (+ festival siblings, see §12/Festival)
│   ├── /collections/for-him, /for-her, /photo-cakes, /flowers-cake-combos (unchanged — small
│   │   but real, distinct collections; no action needed)
│   └── <<BUSINESS APPROVAL REQUIRED>>: retire or repurpose the 7 near-duplicate "Meerut"
│       collections and the 2 non-curating "Best Selling"/"Newest" collections (see
│       WEBSITE_ARCHITECTURE.md §6 for the full recommendation) — not resolved by this document,
│       since unpublishing/merging collections is a merchandising decision, not an architecture one
├── /pages/frequently-asked-questions-faqs (live, unchanged)
├── /pages/refund-return-policy (canonical Refund policy, pending POLICY_ARCHITECTURE.md approval)
├── /pages/terms-and-conditions (populated or unpublished, pending SEO-034 decision)
├── /pages/delivery-areas-in-meerut  ← NEW target for the repurposed Store Locator page
│   (`/pages/store-locator` stays unpublished until this ships, per SEO-030 — see
│   DELIVERY_AREA_SPEC.md; handle shown here is illustrative, not a rename of anything live)
│   ├── links to: /pages/cake-delivery-in-meerut, /pages/midnight-cake-delivery,
│   │   /pages/30-minute-cake-delivery-in-meerut-premium-reliable-service
│   └── <<BUSINESS APPROVAL REQUIRED>>: per-locality pages, only once SEO-035's area-list conflict
│       is resolved and the business confirms neighborhood-level pages are worth the investment
├── /pages/wedding-cakes-meerut ← NEW, optional (see WEBSITE_ARCHITECTURE.md §10), consolidates
│   real existing facts (About Us + sitewide FAQ's venue-setup answer); links to
│   /collections/wedding-cakes
├── /pages/corporate-gifting-solutions ← populate the existing unpublished stub (not a new page)
│   once CONTENT_PLAN.md's open questions (minimum order, GST/invoicing) are answered
├── /pages/gift-hampers (unchanged — already the best-built page on the site)
└── /blog ← <<BUSINESS APPROVAL REQUIRED>>: only if the business confirms a blog is wanted at all
    (CONTENT_PLAN.md already flagged this as unconfirmed; see WEBSITE_ARCHITECTURE.md §8)
```

## Related

[WEBSITE_ARCHITECTURE.md](WEBSITE_ARCHITECTURE.md), [NAVIGATION.md](NAVIGATION.md),
[URL_STRUCTURE.md](URL_STRUCTURE.md), [INTERNAL_LINKING.md](INTERNAL_LINKING.md),
[DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md), [POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md).
