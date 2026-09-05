# Accessibility Audit (Phase 7.5)

Continues from Phase 7.4 (`seo-audit/audit/CHANGELOG.md`, commit `baf22f5`). This is the first
dedicated WCAG pass on this repo — `docs/PROJECT_SCORECARD.md` and `ENTERPRISE_CERTIFICATION.md`
both previously flagged "no dedicated WCAG pass completed; only performance-linked accessibility
checked (Phase 6, image `srcset`/lazy-loading)." That gap is what this phase closes.

**Method**: 100% static code evidence (`grep`/read of the actual `.liquid`/`.css`/`.js` files),
cross-referenced against `sections/header-group.json`/`footer-group.json`/`templates/*.json` to
confirm which sections are actually live vs. disabled scaffolding, before flagging anything. No
live browser, screen reader, or Lighthouse run was possible — the storefront remains password-gated
(unchanged constraint, carried from every prior phase). Findings below are marked accordingly.

## Fixed and deployed live

| # | Finding | File(s) | Fix | WCAG |
|---|---|---|---|---|
| A11Y-001 | "Delivery Date" / "Delivery Time Slot" trigger buttons on the default product template have no accessible name until a value is picked (empty `<span>`, no `aria-label`) — announced as just "button" by screen readers on every product page | `sections/main-product-premium-v2.liquid:337,374` | Added static `aria-label="Delivery Date"` / `aria-label="Delivery Time Slot"` to each button | 4.1.2 Name, Role, Value |
| A11Y-002 | Modal close buttons (quick view, quick add, compare, ask-a-question) render inside a shadow-DOM `::part(close-button)` with `outline: none` and no focus-visible replacement — keyboard users get zero visible focus indicator when tabbing to close any of these 4 live modals | `assets/theme.css:4225` (new rule, additive) | Added one shared `::part(close-button):focus-visible` rule reusing the theme's existing `--color-focus` token, covering all 4 modal classes at once | 2.4.7 Focus Visible |
| A11Y-003 | Newsletter email input relies on `placeholder` only — not a valid label substitute (placeholder disappears on input, isn't read as a label by most screen readers) | `snippets/newsletter.liquid:15` (shared by 3 live sections: `newsletter.liquid`, `newsletter-with-image.liquid`, `newsletter-modal.liquid`) | Added `aria-label` matching the existing placeholder text | 1.3.1 Info and Relationships, 3.3.2 Labels or Instructions |
| A11Y-004 | Cart drawer and full cart page fail to render the customer's own uploaded reference photo at all — `<imgsrc="...">` (missing space) is not a valid `<img>` element, so the browser silently drops it | `snippets/item-cart.liquid:39`, `snippets/item-cart-page.liquid:41` | Added the missing space (`<img src=`) | 1.1.1 Non-text Content (the image, and its `alt`, literally never reached the DOM) |
| A11Y-005 | `id="RowOrder"` / `id="RowDiscount"` are static inside a `{% for %}` loop — duplicate IDs across order rows / discount lines break the `headers`/`id` table-cell association screen readers use for data-table navigation as soon as a customer has more than one order (or an order has more than one discount) | `sections/main-account.liquid:46,55,58,61,64`, `sections/main-order.liquid:208,215` | Interpolated `{{ forloop.index }}` into both the `id` and every matching `headers` reference | 1.3.1 Info and Relationships |
| A11Y-006 | Account-area `<nav>` landmarks (dashboard, addresses, order-detail sidebars) have no `aria-label` — screen reader users navigating by landmark get multiple ambiguous "navigation" regions on the same page (header nav + footer nav + this one) | `sections/main-account.liquid:8`, `sections/main-addresses.liquid:9`, `sections/main-order.liquid:8` | Added `aria-label="{{ 'customer.account.title' | t }}"` to all three | 1.3.1 Info and Relationships, 2.4.1 Bypass Blocks |

All 8 changed files verified via the established deploy-safety cycle: pull → diff-confirm zero
drift → edit → scoped `--only` push (all 8 files in one push) → re-pull → diff-confirm byte-identical
live → Theme Check unchanged (343 files / 1,351 offenses / 80 files / 1,161 errors / 190 warnings —
identical to the Phase 7.4 baseline, confirming no regression from any of these edits).

Every fix above is additive-only (`aria-label`, `aria-*`, an interpolated `id`/`headers` value, one
CSS rule, one missing space) — zero visual, layout, or flow changes, consistent with `CLAUDE.md`'s
product-page protection rule even where a file isn't the explicitly protected template.

## Found, not fixed — requires a product/business decision

**A11Y-OPEN-001: the "Date:" field on 2 of 3 product templates points at an input that was never built.**

`sections/main-product.liquid` (used by `templates/product.hampers-template.json`) and
`sections/main-product-premium.liquid` (used by `templates/product.premium.json`) both contain:

```liquid
<label class="hdt-product-form__label hdt-s-text is-type-block" for="delivery-date">Date:</label>
<input form="{{ product_form_id }}" type="file" id="reference-image" name="properties[Reference Image]" accept="image/*">
```

The label's `for="delivery-date"` matches no element in either file — and it isn't simply mislabeling
the file-upload input either, since that input has its own distinct `id="reference-image"`. Both
files' own JavaScript (`main-product.liquid:670`, `main-product-premium.liquid:691`) calls
`document.getElementById("delivery-date-{{ section.id }}")`, expecting a real date-picker element
that **does not exist anywhere in either template's markup**. The default product template
(`main-product-premium-v2.liquid`, `templates/product.json`) has a fully working date-picker button
+ modal (see A11Y-001 above) — these two other templates appear to have lost theirs, or never had
one built to match the JS.

**Not fixed.** Building the missing input is a visible UX/flow change (exactly what `CLAUDE.md`'s
protected-module rule exists to gate even outside the explicitly-named v2 template), and the correct
fix depends on a product decision this audit can't make: should the hampers/premium(non-v2) product
pages get the same date-picker UI as the default template, or was a plain "Date:" text field always
intended, or is the field simply dead and should be removed? Each answer produces a different,
visible change. Flagging with full evidence per this program's stop-condition rule, not guessing.

There's also a duplicate `name="properties[Reference Image]"` file input in both files (one at the
`id="reference-image"` line above, a second, un-id'd one a few lines below with an identical
`name`) — two inputs sharing one form-field name is itself a latent bug (only one value reaches the
order), but fixing which one to keep is bound up in the same product decision above, so it's flagged
together rather than resolved unilaterally.

## Checked, confirmed correct — no action needed

- **Skip-to-content link** (`layout/theme.liquid:97`) — present and correctly targets `#MainContent`.
- **Icon-only buttons** (wishlist, compare, quick view, header search/account/cart/menu) — all
  correctly pair the icon with a `sr-only`/`aria-label` accessible name (`snippets/btn-wishlist.liquid`,
  `snippets/btn-compare.liquid`, `snippets/btn-quick-view.liquid`, `sections/tbk-header.liquid:681-802`).
- **Footer navigation** (`sections/site-footer.liquid`) — 4 distinct `<nav>` landmarks, each with its
  own `aria-label`, plus `role="contentinfo" aria-labelledby` on the footer itself.
- **Modal/dialog mechanics** — the shared `<hdt-drawer>`/`<hdt-lazy-modal>` web component (quick
  view, quick add, compare) sets `role="dialog"`, `aria-modal="true"`, and uses a focus-trap library
  (confirmed in `assets/global.min.js`); the mobile nav drawer (`tbk-header.liquid:852-856`) has
  hand-rolled Escape-to-close and Tab-cycle focus trapping. No gap found.
- **`<main>` landmark** — present exactly once (`layout/theme.liquid:100`), matches the skip-link
  target, no duplicates on the live render path.
- **Reduced motion** (`prefers-reduced-motion`) — correctly gated in the base theme layer
  (`assets/base.css:1610,1971,3296,3302,3550`), including an explicit `reduce` fallback for the
  marquee. Not independently re-verified line-by-line for every bespoke `tbk-*` transition added on
  top of the base theme — flagged as a smaller, lower-confidence follow-up, not a finding.
- **`main`/`nav`/labelled-control patterns elsewhere** — `snippets/product-qty-selector.liquid`
  and the rest of `snippets/newsletter.liquid` already use correct `for`/`id` pairing.

## Confirmed dead code, no live impact — deprioritized, not fixed this pass

`sections/header-e-commerce.liquid` and `sections/header-menu-bottom-hulkapps-backup.liquid` are
`"disabled": true` in `sections/header-group.json`; `snippets/menu_blocks.liquid`,
`menu_blocks_ecomerce.liquid`, `mega_menu_blocks.liquid`, `mega_menu_e_blocks.liquid`, and
`menu_mobile.liquid` are only reachable from those disabled sections. Their unlabeled `<nav>`
elements, static `id="hdt-mega-product-swatch"` inside a loop, and mega-menu thumbnails with no
`alt` are real code-level issues but have **zero current storefront impact** — not touched this
pass; worth a fix-once pass only if that header path is ever re-enabled.
`snippets/reference-images-upload.liquid`'s unassociated label is similarly dead — not rendered
anywhere on the live site (confirmed via grep against `sections/` and `templates/`).

## Lower-confidence / needs live verification (password gate blocks this, as with every prior phase)

- **Heading hierarchy on the default product template**: `main-product-premium-v2.liquid` has one
  correct `<h1>` but zero `<h2>` — sub-headings (modal titles, "About This Cake", "Perfect For",
  "Delivery Information") jump straight to `<h3>`, repeated 7×. Structural, not a hard blocker for
  any assistive technology, but worth a level-restructure in a future pass rather than a quick patch
  (renumbering headings across a protected, high-traffic template deserves its own careful review).
- Homepage's pre-existing duplicate `<h1>` (`layout/theme.liquid:94` + `templates/index.json:393`)
  — already logged in `docs/TECHNICAL_SEO_AUDIT.md:99-102`, confirmed still present in code, not
  re-opened as a new finding here (per "never repeat previous work").

## Related

[SECURITY_AUDIT.md](SECURITY_AUDIT.md), [SHOPIFY_SEO_REPORT.md](SHOPIFY_SEO_REPORT.md),
[STRUCTURED_DATA_REPORT.md](STRUCTURED_DATA_REPORT.md).
