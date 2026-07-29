# Verified Issues

Every issue below was confirmed directly — by reading the actual theme code, by a real Shopify
Admin API query, or by diffing a freshly pulled live-theme copy against the local repo. None are
guesses. See [`../issues.yml`](../issues.yml) for the machine-readable record.

## Fixed

### SEO-001 through SEO-006 — fabricated ratings and fake reviews (first pass, `52a3821`)

Five files carried hardcoded, unsourced "Google Rated" / "Top Rated" claims, and one
(`sections/tbk-product.liquid`) contained an entire fabricated "Customer Reviews" section with four
invented names (Neha Sharma, Rohit Verma, Simran Kaur, Pooja Agarwal) and invented quotes, labeled
"Real feedback from happy customers." `CLAUDE.md` already documents that fabricated testimonials
were removed once and "that route is permanently closed" — SEO-006 is a second instance of exactly
that violation, in a different file, not previously caught. **This is the single most serious
finding of the audit.**

**Evidence chain**: `grep -rn "Rated\|★"` across `sections/*.liquid` and `snippets/*.liquid` →
manual read of each hit's surrounding context → for `main-product.liquid`, confirmed genuinely live
via `graphql_query` on the `Cake Hampers` collection, finding product handle `h6` with
`templateSuffix: "hampers-template"`.

### SEO-007, SEO-008, SEO-009 — second-pass sweep found more instances (`eaad74f`)

A broader grep (`[0-9]+,?[0-9]*\+? *(happy|customers|...)`) found two more unsourced count/rating
claims on the *same* active product template the first pass had already partly fixed, plus the
single most important correction of the whole audit: **`sections/tbk-footer.liquid` (fixed in the
first pass) is not the live footer at all.** `sections/footer-group.json` wires in
`type: "site-footer"` → `sections/site-footer.liquid`, which still carried the identical unsourced
claim, unfixed until this pass.

**Lesson recorded for future audits**: one grep pattern misses re-worded duplicates of the same
claim; a filename resembling "footer" doesn't confirm liveness — always check the section-group
JSON.

### SEO-010, SEO-011, SEO-012 — placeholder contact email (`eaad74f`)

`templates/page.contact-1.json`, `page.contact-2.json`, and `page.our-store.json` all contained the
literal string `EComposer@example.com` — a page-builder app's own placeholder, never replaced with
a real address. Replaced with `thebakingkaur@gmail.com`, the shop's real email, itself verified via
`get-shop-info` earlier in the audit (not invented).

## Fixed (third pass, `4d23a2e`)

### SEO-023 — duplicate Product schema on every product page, all 602 active products affected

`grep -rhoE '"@type":\s*"[^"]+"' sections/*.liquid` surfaced far more schema types than the first
schema pass had catalogued. Tracing `Offer`/`Brand`/`MerchantReturnPolicy` back to their files found
**three separate product section templates each carrying their own hand-rolled `@type: "Product"`
block**, while `snippets/structured-data.liquid` (rendered unconditionally from `layout/theme.liquid`)
*also* emits Shopify's native `product | structured_data` schema on every product page. Every
product — including all 602 currently-active ones on the default template
(`main-product-premium-v2.liquid`) — was shipping two competing Product entities.

Resolution differed by file, based on which schema was actually richer:
- `main-product-premium-v2.liquid` and `main-product-premium.liquid`: hand-rolled blocks added
  nothing beyond what Shopify's native filter already provides — removed outright.
- `main-product.liquid` (hampers-template, confirmed live via `templateSuffix` on a real product):
  its block has `sku`, `category`, `seller`, `shippingDetails` (`OfferShippingDetails` with real
  `MonetaryAmount`/`DefinedRegion`/`ShippingDeliveryTime`), and `hasMerchantReturnPolicy` — genuine
  Merchant Center value the native filter lacks. Kept; `structured-data.liquid` now skips its native
  Product emission specifically when `template.suffix == 'hampers-template'`.

### SEO-024 — sitewide, unconditional FAQPage schema

`layout/theme.liquid` rendered a 9-question `FAQPage` block on every single page (no
`request.page_type` gate at all) — a direct violation of Google's "structured data must match
visible page content" guideline, and a potential duplicate against `page.faq-01.json`/
`page.faq-02.json`'s own FAQPage-bearing accordion sections. Gated to exclude those two template
suffixes. **Content untouched** — the 9 Q&A pairs read as genuine business facts (delivery,
WhatsApp ordering, pickup), consistent with facts already verified elsewhere in the codebase, not
fabricated — this was a placement fix, not a content fix.

### SEO-020 — sameAs consistency

Added the already-verified-real Facebook URL to `tbk-schema-website.liquid`'s `sameAs`, matching
`bk-local-business.liquid`.

### A drift reconciliation, not a schema fix

`layout/theme.liquid` had independently diverged from git before this pass touched it — two
`render` calls (`tbk-tokens`, `tbk-components`) present in git (commit `011f9be`, message "viral
scoopie tin work 0 percnt done" — reads as abandoned/incomplete work) were absent from the live
theme. Synced local to the live truth for this file before applying the FAQPage gate, so the push
didn't silently reintroduce unrelated, seemingly-abandoned changes as a side effect.

## Open (verified, not yet fixed)

### SEO-013 — Lorem Ipsum live on both FAQ page templates

`grep -c "Lorem ipsum\|low hanging fruit" templates/page.faq-01.json templates/page.faq-02.json` →
**12 matches in each file.** These come from the shared `accordion`/`accordion_inline` sections'
default preset content, left unedited in the actual per-page template JSON (not just the
theme-editor's "add new section" defaults — this is the content that renders on a real FAQ page).
**Not fixed**: writing plausible-sounding FAQ answers without the business's real refund/delivery
policies would itself be a fabrication risk, the exact failure mode this whole audit exists to
prevent.

### SEO-016 — the original header rating claim

Unchanged from `CLAUDE.md`'s own tracking: the "★4.9 Rated" claim in the site header
(`tbk_header_main`) is still live. `CLAUDE.md` already states this "Needs an explicit go-ahead" —
that approval hasn't been given yet, so it wasn't touched.

### SEO-020 — sameAs list inconsistency between two schema snippets

`snippets/tbk-schema-website.liquid`'s Organization entity lists only Instagram in `sameAs`;
`snippets/bk-local-business.liquid`'s Bakery entity lists Instagram *and* Facebook. Both are real
URLs, not fabricated — just inconsistent between the two schema sources describing the same
business entity.

## Related

[AUDIT_LEDGER.md](AUDIT_LEDGER.md), [CHANGELOG.md](CHANGELOG.md).
