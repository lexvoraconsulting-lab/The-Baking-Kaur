# Navigation Architecture

Generated 2026-07-30, BUILD-020. Companion to [SITE_TREE.md](SITE_TREE.md)'s menu inventory. This is
a plan — no menu is edited, no link_list is reassigned by this document. Design principle used
throughout: **reuse the six existing menu handles before proposing new ones.** Three of them
(`explore-cakes`, `quick-links`, `meerut-delivery`) already exist as empty shells, seemingly created
for exactly this purpose and never finished — production architecture should fill those in, not
invent a seventh and eighth handle alongside them.

## 1. Primary header navigation

**Current state**: the live header renders `main-menu` (Home / About Us / Contact Us / a link to
`/collections`) — four items, no direct collection links at all. A second menu, `header`, already
contains real, correct links to all six primary collections (Birthday, Anniversary, Wedding, Theme,
Hampers, Diwali Hampers) but is only referenced by a `disabled: true` section block, so it renders
nowhere.

**Recommendation**: wire the live header to render the six real collection links already sitting in
the `header` menu, rather than routing every visitor through the generic `/collections` catch-all
first. Two ways to do this, both reuse existing content instead of creating new menu items:

- Option A (simpler): add `header`'s six items directly into `main-menu`, so one live menu carries
  both the utility links (About/Contact) and the collection links.
- Option B (matches the existing two-tier header component already in the theme, currently
  disabled): re-enable the bottom navigation bar block that already points at `header`, so the
  top bar keeps Home/About/Contact and a second row surfaces the six collections — this is
  effectively turning on infrastructure that was already built and switched off, not building new
  UI. `<<BUSINESS APPROVAL REQUIRED>>` only in the sense of a visual/UX call (site's product page and
  overall visual system are protected per `CLAUDE.md` — a header-nav change is not the product page,
  but any visible layout change should still get a deliberate go-ahead before deploying, per this
  project's "invisible edits only without explicit sign-off" convention).

Target header link set (7 items, all real, all already-existing collections/pages — nothing invented):
Birthday Cakes · Anniversary Cakes · Wedding Cakes · Designer & Theme Cakes · Cake Hampers ·
Delivery Areas (new page, see §3) · FAQ.

## 2. Footer navigation

**Current state**: the live footer (`site-footer.liquid`) does not render the `footer` menu at all —
it hardcodes its own links directly in the section file. Two real, concrete defects found this pass:

1. Its Refund link uses `shop.refund_policy.url` with a fallback to
   `/pages/return-refund-replacement-policy` — **the unpublished draft page**, not the live canonical
   `/pages/refund-return-policy`. If the Shop Policy were ever cleared, this footer would 404.
   Right now it silently sends every visitor to the Shop Policy side of the SEO-031 contradiction,
   with no path at all to the more reasonable custom page.
2. Its "Terms & Conditions" link (two occurrences) points straight at `/pages/terms-and-conditions` —
   the empty page (SEO-034) — instead of `shop.terms_of_service.url`, which is the pattern already
   correctly used one line above it for Refund and Shipping.

**Recommendation**: once POLICY_ARCHITECTURE.md's canonical decision is made, the footer's link
targets should be corrected to match it exactly (not decided here — this document only identifies
*where* the mismatch lives, consistent with "no coding" scope). Add FAQ to the footer (currently
absent from both the live footer and the unused `footer` menu) — every delivery/hamper page already
recommends linking to it (`LOCAL_SEO_ROADMAP.md` §8) and the footer is the one placement that reaches
every page at once.

Target footer link set: Search · Contact Us (custom page) · Privacy Policy (Shop Policy) · Refund
& Return Policy (**canonical target TBD**) · Shipping Policy (Shop Policy) · Terms
(**canonical target TBD**) · FAQ (new) · Your Privacy Choices (publish decision — see
`POLICY_ARCHITECTURE.md` §3).

## 3. Delivery Areas navigation (the `meerut-delivery` menu, currently empty)

**Recommendation**: this is the natural home for the Delivery Areas hub page recommended in
`SITE_TREE.md`/`DELIVERY_AREA_SPEC.md`. Populate `meerut-delivery` with:

- Delivery Areas in Meerut (hub — new page, repurposing the unpublished Store Locator page)
- Same-Day Delivery → `/pages/cake-delivery-in-meerut`
- Midnight Delivery → `/pages/midnight-cake-delivery`
- Express (30-Minute) Delivery → `/pages/30-minute-cake-delivery-in-meerut-premium-reliable-service`
- `<<BUSINESS APPROVAL REQUIRED>>`: per-locality links, once SEO-035's area-list conflict resolves

Surface this menu somewhere real visitors reach it — a footer column or a header sub-item — not just
create the linklist and leave it unwired (the same mistake `header` and `quick-links-menu` already
made).

## 4. Quick Links (the `quick-links-menu`, currently unwired)

This menu is already the best-built one in the account: it correctly uses Shopify's native
`SHOP_POLICY` type for Privacy/Refund/Shipping instead of hardcoding a page URL, which means it
auto-updates if those policies' URLs ever change. Its one defect: "Terms & Condition" points at
`type: PAGE` → the empty page, same issue as the footer. **Recommendation**: fix that one item to
also use `SHOP_POLICY` (once Terms is decided canonical, per `POLICY_ARCHITECTURE.md`), add FAQ, and
surface this menu — e.g. as the footer's policy column, replacing the footer's hardcoded links
entirely so there's one source of truth instead of two.

## 5. About/Company navigation (the `about-us-menu`, currently unwired)

Recommendation: keep About Us and Contact Us; drop "Store Locations" (points at the unpublished fake
page, SEO-030) until/unless the Delivery Areas hub in §3 is built and this item is repointed to that
instead. Do not surface this menu pointing at a 404 in the meantime.

## 6. What's explicitly not decided here

Which of Option A/B in §1 ships, the exact canonical Refund/Terms URLs (pending
`POLICY_ARCHITECTURE.md` approval), and the real delivery-area locality list (pending SEO-035) are
all flagged, not resolved, consistent with this project's standing rule against guessing business
decisions.

## Related

[SITE_TREE.md](SITE_TREE.md), [URL_STRUCTURE.md](URL_STRUCTURE.md),
[INTERNAL_LINKING.md](INTERNAL_LINKING.md), [POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md).
