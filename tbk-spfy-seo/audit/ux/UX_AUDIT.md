# UX Audit

## Scope limitation — stated plainly, not glossed over

The storefront is currently password-gated (SEO-022, confirmed intentional). This audit could not
render or interact with a real page as an anonymous visitor would — everything below is either a
code-level inference (reading the Liquid/CSS) or explicitly marked as not assessed. No UX score is
claimed from this pass; see [../audit/SCORECARD.md](../audit/SCORECARD.md).

## What was reviewed at the code level

- **Product page structure** (`sections/main-product-premium-v2.liquid`): gallery, variant picker,
  price, buy buttons, delivery schedule, and a "Why Customers Love Us" trust block all present in
  the template — structurally reasonable for a product page, per a code read (not a rendered view).
- **Trust signal placement**: the fabricated ratings/reviews removed this session (SEO-001 through
  SEO-009) were positioned exactly where genuine trust signals belong (near the buy button, in the
  footer) — meaning once real, sourced trust content exists (verified reviews, a real GBP link), the
  same structural slots can likely hold it without a layout redesign.
- **FSSAI/dietary/delivery trust-pills**: real, conditionally-rendered patterns exist alongside the
  fabricated ones (e.g. `site-footer.liquid`'s `service_areas` and `fssai_text` only render if the
  merchant fills them in) — a good, safe pattern already in use elsewhere in the theme that the
  fabricated instances didn't follow.

## Not assessed this pass

Navigation/menu usability, filter/search UX, cart and checkout flow, form usability, typography/
spacing/contrast, mobile vs. desktop rendering, sticky CTA behavior, visual hierarchy — all require
either a live rendered page (blocked by the password gate) or a real device/browser session, neither
available this pass.

## Recommended next step

Once the password gate lifts (or via an authenticated preview session bypassing it), a real
browser-based UX pass — ideally on both mobile and desktop viewports — covering the checklist above.

## Related

[CRO_AUDIT.md](CRO_AUDIT.md), [../audit/SCORECARD.md](../audit/SCORECARD.md).
