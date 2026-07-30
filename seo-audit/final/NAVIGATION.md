# Navigation Architecture

Generated 2026-07-30, BUILD-020. Companion to [SITE_TREE.md](SITE_TREE.md)'s menu inventory. This is
a plan — no menu is edited, no link_list is reassigned by this document. Design principle used
throughout: **reuse the six existing menu handles before proposing new ones.** Three of them
(`explore-cakes`, `quick-links`, `meerut-delivery`) already exist as empty shells, seemingly created
for exactly this purpose and never finished — production architecture should fill those in, not
invent a seventh and eighth handle alongside them.

## 1. Primary header navigation — IMPLEMENTED 2026-07-30

**Status: done.** Option A was chosen and shipped. `main-menu` (live, wired to `tbk_header_main` via
`header-group.json`'s `main_menu` setting) now carries HOME / ABOUT US / CONTACT US unchanged, plus
the existing "Categories" item converted from a flat link to `/collections` into a parent item with
6 real collection children: Birthday Cake, Anniversary Cake, Diwali Hampers, Theme Cakes, Hampers,
Wedding Cakes — reusing the exact titles/order already curated in the (still-orphaned) `header` menu.
No second navigation row was added; no theme file was edited. The header's own dropdown/disclosure
rendering (`sections/tbk-header.liquid`'s `nav.links` loop, native `<details>/<summary>`, the only
nav surface for both desktop and mobile per this theme's single-drawer design) already supported
nested children with zero code changes required — this was a Shopify Admin navigation-menu content
change only (`menuUpdate` mutation), not a deploy.

All 6 child URLs auto-resolved correctly from each collection's `resourceId` (verified via a
post-change re-query): `/collections/birthday-cakes`, `/collections/anniversary-cakes`,
`/collections/luxury-diwali-hampers`, `/collections/designer-theme-cakes`, `/collections/cake-hampers`,
`/collections/wedding-cakes`. Accessibility is unchanged/preserved — the parent item renders as a
native `<summary>` disclosure control, same pattern already used for any nested menu item in this
theme, no new ARIA needed.

**Not done as part of this change** (out of scope, per "do not modify any unrelated navigation or
header functionality"): adding a standalone Delivery Areas or FAQ link to the header — those depend
on Sprint 1 decisions (delivery-area list, Store Locator repurposing) and Sprint 6 work respectively,
not yet ready. The original target link set below is retained for future reference, not the shipped scope.

Original (pre-implementation) target link set for reference: Birthday Cakes · Anniversary Cakes ·
Wedding Cakes · Designer & Theme Cakes · Cake Hampers · Delivery Areas (new page, see §3) · FAQ —
superseded by the simpler, lower-scope "Categories" dropdown actually shipped.

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

## 5. About/Company navigation (the `about-us-menu`, currently unwired) — IMPLEMENTED 2026-07-30

**Status: done.** "Store Locations" (pointed at the unpublished fake Store Locator page, SEO-030)
removed via `menuUpdate`. About Us and Contact Us items unchanged, same item IDs preserved. Menu is
still not confirmed wired to any live section — this fix is preventive (no future 404 if it's ever
activated), not a live-bug fix. If/when the Delivery Areas hub (§3) is built, consider adding a link
to it here instead.

## 6. What's explicitly not decided here

Which of Option A/B in §1 ships, the exact canonical Refund/Terms URLs (pending
`POLICY_ARCHITECTURE.md` approval), and the real delivery-area locality list (pending SEO-035) are
all flagged, not resolved, consistent with this project's standing rule against guessing business
decisions.

## Related

[SITE_TREE.md](SITE_TREE.md), [URL_STRUCTURE.md](URL_STRUCTURE.md),
[INTERNAL_LINKING.md](INTERNAL_LINKING.md), [POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md).
