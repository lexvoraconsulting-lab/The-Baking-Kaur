# Implementation Backlog — Production Build

Generated 2026-07-30. Every task below traces to a specific finding in a completed report — nothing
here is a new audit finding. Sources: `issues.yml`/`AUDIT_LEDGER.md` (SEO-NNN IDs), `POLICY_ARCHITECTURE.md`/
`POLICY_REDIRECT_PLAN.md`, `ADDRESS_AUDIT.md`, `DELIVERY_AREA_SPEC.md`, `EEAT_REPORT.md`,
`LOCAL_SEO_ROADMAP.md`, `CONTENT_PLAN.md`, `WEBSITE_ARCHITECTURE.md` family, `ARCHITECTURE_VERIFICATION.md`,
`schema/SCHEMA_AUDIT.md`, `seo/TECHNICAL_SEO.md`, `seo/GEO_AUDIT.md`, `ux/CRO_AUDIT.md`, `ux/UX_AUDIT.md`.
Sprint order follows dependency order, not just the requested numbering — Sprint 1's decisions gate
several later-sprint tasks explicitly noted in **Dependencies**.

Field conventions: **Manual approval required** means a business decision, legal sign-off, or visible-
layout sign-off is needed before implementation (per this project's standing "invisible edits only
without explicit sign-off" convention) — it does not mean "needs a developer to review the diff,"
which is assumed for every task regardless.

---

## Sprint 1 — Critical Fixes

### 1.1 Resolve the refund/cancellation policy contradiction (SEO-031)

- **Description**: The live custom "Refund & Return Policy" page (12hr cancellation / 4hr issue
  window / 5-7 day refund) and Shopify's built-in Refund policy + Terms of Service ("all orders
  final, no refunds ever") make opposite promises about the same customer right. Confirm which terms
  are actually true, then rewrite the Shop Policies (Refund, Terms of Service, and while there, fix
  Shipping's unsourced "2-5 hours"/"1 hour" windows) to match the canonical custom page exactly, and
  fix "The Bakery Kaur" → "The Baking Kaur" in all three.
- **Files affected**: Shopify Admin → Settings → Policies (Refund, Shipping, Terms of Service) — not
  theme files; `templates/page.contact-2.json`/footer if the canonical URL choice changes a link target.
- **Dependencies**: None — this is the top-of-chain decision. Gates 1.5, 2.3, 2.5.
- **Estimated effort**: Small (content rewrite only, ~1-2 hours once terms are decided) + the decision
  itself, which is the real bottleneck, not the editing.
- **Risk**: High if left unresolved — live legal contradiction on customer rights. Low technical risk
  to fix (text-only edit in Shopify Admin).
- **Expected SEO/CRO impact**: High trust/EEAT impact; removes a live inconsistency that actively
  damages customer confidence and could trigger a support dispute or platform policy complaint.
- **Manual approval required**: **Yes** — this is a legal-content decision, not implementable without it.

### 1.2 Populate or unpublish the empty "Terms and Conditions" page (SEO-034)

- **Description**: `/pages/terms-and-conditions` is live, published, and has a completely empty body.
  Either populate it (ideally mirroring the approved Shop Policy Terms of Service from 1.1) or
  unpublish it until real content exists.
- **Files affected**: Shopify Admin Page body (`gid://shopify/Page/110844510377`), not a theme file.
- **Dependencies**: Best done after 1.1 (so the content matches, rather than being written twice).
- **Estimated effort**: Small.
- **Risk**: Medium — a published, indexable, contentless legal page is a real trust/completeness gap.
- **Expected SEO/CRO impact**: Low direct traffic impact, meaningful trust/EEAT impact.
- **Manual approval required**: **Yes** (legal content).

### 1.3 Confirm canonical address + fresh geo pin, propagate everywhere (SEO-015/029/036)

- **Description**: 4 distinct address wordings and 2 geo-coordinate pairs (~600m apart) are live
  simultaneously, including a mismatch against the Shopify Admin's own billing-address record.
  Confirm one address (recommend starting from the Admin billing address) and get a fresh Google Maps
  pin-drop, then propagate identically to every surface in one coordinated deploy.
- **Files affected**: `snippets/bk-local-business.liquid`, `snippets/tbk-schema-website.liquid` (add
  missing `streetAddress`/`geo`), `sections/site-footer.liquid` (default), `sections/footer.liquid`,
  `sections/tbk-footer.liquid`, `templates/page.contact-2.json`, the Refund & Return Policy page body,
  the Shopify Admin Contact Information Shop Policy.
- **Dependencies**: None technical; gates 6.1 (GBP consistency check) and 6.4 (schema areaServed expansion).
- **Estimated effort**: Medium (one address is trivial to change everywhere; the geo pin-drop and
  confirming across ~7 files/surfaces in one pass is the real work).
- **Risk**: Medium if left unresolved — misplaces the business on Google Maps/Local Pack; low
  technical risk once the correct values are confirmed (find-and-replace across known files).
- **Expected SEO/CRO impact**: High for Local Pack accuracy and "near me" search relevance.
- **Manual approval required**: **Yes** (confirming the real address/coordinates is a business fact,
  not a guess this project will make).

### 1.4 Resolve the delivery-area-list conflict (SEO-035)

- **Description**: The live "Cake Delivery in Meerut" page and the live footer's `service_areas`
  setting name different sets of localities (only 2 of 5 named areas match). Confirm the true,
  complete serviceable-area list once.
- **Files affected**: `sections/site-footer.liquid` (`service_areas` default), the Cake Delivery in
  Meerut page body.
- **Dependencies**: Gates 3.4 (Festival collections, indirectly via area confidence), 6.2 (Delivery
  Areas hub content), 6.3 (per-locality pages), 6.4 (schema areaServed).
- **Estimated effort**: Small to edit once decided; the decision itself is the work.
- **Risk**: Medium — active local-SEO inconsistency, and blocks several downstream Local SEO tasks.
- **Expected SEO/CRO impact**: High — directly determines what neighborhood-level content can be built.
- **Manual approval required**: **Yes**.

### 1.5 Fix the footer's Refund/Terms link targets (from `ARCHITECTURE_VERIFICATION.md` A2/A3)

- **Description**: The live footer's Refund link falls back to the unpublished draft policy page
  instead of the canonical live one; its Terms links (one conditional, one unconditionally hardcoded
  at a separate location in the same file) point at the empty Terms page instead of
  `shop.terms_of_service.url`.
- **Files affected**: `sections/site-footer.liquid` (lines ~98-101 and ~127-128).
- **Dependencies**: **Blocks on 1.1 and 1.2** — the correct target URL isn't fixed until those land.
- **Estimated effort**: Small (a few-line Liquid edit) once the target is known.
- **Risk**: Low technical risk; the current live risk (sending customers to the wrong side of the
  policy conflict) is covered under 1.1's risk rating.
- **Expected SEO/CRO impact**: Medium — every visitor who clicks Refund/Terms in the footer currently
  lands on the wrong page; fixing this is pure navigation correctness.
- **Manual approval required**: No (mechanical fix, once 1.1/1.2 set the target).

### 1.6 Decide the fate of the duplicate collection cluster (from `WEBSITE_ARCHITECTURE.md` §6, `ARCHITECTURE_VERIFICATION.md` B3/B4)

- **Description**: 7 collections (`cakes`, `cake-delivery-meerut`, `same-day-cake-delivery-meerut`,
  `midnight-cake-delivery-meerut`, `midnight-cake-delivery`, `custom-cakes-meerut`,
  `kids-birthday-cakes-meerut`) all resolve to essentially the same ~986-product set. Separately,
  "Best Selling Products" and "Newest Products" both show the full 1,235-product catalogue with no
  real curation. Decide which (if any) of the 7 stay live, and whether to wire real sort logic into
  the two utility collections or unpublish them.
- **Files affected**: Shopify Admin → Collections (publish/unpublish, sort-rule changes) — no theme
  file changes required for the decision itself.
- **Dependencies**: None; gates 3.1 and 3.2 (Sprint 3 implementation).
- **Estimated effort**: Small to implement once decided (unpublishing/re-sorting collections is an
  Admin action, not a code change).
- **Risk**: Medium — active duplicate-content SEO risk today, same family as the policy conflict.
- **Expected SEO/CRO impact**: High — resolving this stops 7 collection URLs from competing against
  each other for the same search queries, and makes "Best Selling" mean something again.
- **Manual approval required**: **Yes** (merchandising decision).

### 1.7 Decide the permanent fate of the Store Locator page (SEO-030)

- **Description**: Currently unpublished (mitigated) with fake London/Madrid/Tokyo content. Decide:
  delete, or repurpose into the real Delivery Areas hub (content spec already written and ready in
  `DELIVERY_AREA_SPEC.md`).
- **Files affected**: `templates/page.store-locations.json` (if repurposing, becomes the new Delivery
  Areas template — or a new template is built and this one is deleted).
- **Dependencies**: Recommend deciding this alongside 1.4, since the repurpose path needs the
  area-list decision anyway.
- **Estimated effort**: Small (decision) + Medium (if repurposing, building the actual page — tracked
  as 6.2 in Sprint 6).
- **Risk**: Low — already mitigated (unpublished), so no live exposure either way.
- **Expected SEO/CRO impact**: Medium — unlocks a real Delivery Areas landing page if repurposed.
- **Manual approval required**: **Yes**.

---

## Sprint 2 — Navigation

### 2.1 Wire the live header to the 6-collection `header` menu (`NAVIGATION.md` §1, `ARCHITECTURE_VERIFICATION.md` A1)

- **Description**: The live header renders a 4-item menu (Home/About/Contact/Categories-link) while a
  real 6-collection menu (`header`: Birthday, Anniversary, Wedding, Theme, Hampers, Diwali Hampers)
  sits wired only to a disabled section block. Either merge `header`'s items into `main-menu`, or
  re-enable the existing (currently disabled) two-tier header block that already points at `header`.
- **Files affected**: `sections/header-group.json` (either edit `main-menu`'s content in Shopify
  Admin's menu editor, or flip `header_menu_bottom_hulkapps_backup_kgkQBL`'s `disabled` flag).
- **Dependencies**: None technical.
- **Estimated effort**: Small (reusing existing linklist content) to Medium (if re-enabling the
  two-tier block requires visual QA across breakpoints).
- **Risk**: Low technical risk; the only real risk is shipping a visible layout change without sign-off.
- **Expected SEO/CRO impact**: High — this is the single biggest navigation gap: real customers
  currently have no direct path from the header to any collection.
- **Manual approval required**: **Yes** (visible layout/UX change).

### 2.2 Populate the `meerut-delivery` menu (`NAVIGATION.md` §3)

- **Description**: Currently an empty shell. Populate with the Delivery Areas hub (once built) and
  the three existing real delivery-mode pages (same-day, midnight, express).
- **Files affected**: Shopify Admin → Navigation → `meerut-delivery` menu.
- **Dependencies**: **Blocks on 1.4 (area-list decision) and Sprint 6's hub page (6.2)** for a
  complete menu; the three existing delivery-mode links can be added immediately without waiting.
- **Estimated effort**: Small.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium — gives delivery content a real navigational home instead of
  being reachable only via internal links or search.
- **Manual approval required**: No, once the hub page exists (mechanical menu population); partial
  version (3 existing pages only) can ship without approval now.

### 2.3 Fix `quick-links-menu`'s Terms item type (`NAVIGATION.md` §4, `ARCHITECTURE_VERIFICATION.md` A5)

- **Description**: This menu already correctly uses Shopify's native `SHOP_POLICY` type for
  Privacy/Refund/Shipping, but its Terms item is `type: PAGE` pointing at the empty custom page.
  Switch it to `SHOP_POLICY` once Terms is canonical.
- **Files affected**: Shopify Admin → Navigation → `quick-links-menu`.
- **Dependencies**: **Blocks on 1.1/1.2.**
- **Estimated effort**: Small.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Low-Medium (consistency/correctness, not a traffic driver by itself).
- **Manual approval required**: No (mechanical, once target is decided).

### 2.4 Remove or repoint "Store Locations" in `about-us-menu` (`NAVIGATION.md` §5, `ARCHITECTURE_VERIFICATION.md` A6)

- **Description**: Points at the unpublished fake Store Locator page. Drop it, or repoint to the real
  Delivery Areas hub once 1.7/6.2 land.
- **Files affected**: Shopify Admin → Navigation → `about-us-menu`.
- **Dependencies**: None urgent (menu not confirmed wired to a live section currently) — but should be
  fixed before this menu is ever surfaced.
- **Estimated effort**: Small.
- **Risk**: Low (not confirmed live currently).
- **Expected SEO/CRO impact**: Low currently; prevents a future 404 if this menu is ever activated.
- **Manual approval required**: No.

### 2.5 Consolidate footer navigation to one source of truth (`NAVIGATION.md` §2/§4)

- **Description**: The live footer hardcodes its own links instead of rendering the `footer` linklist,
  and duplicates logic the `quick-links-menu` already does correctly. Replace the footer's hardcoded
  policy links with a render of `quick-links-menu` (once 2.3 is done), and add FAQ to the footer link set.
- **Files affected**: `sections/site-footer.liquid`.
- **Dependencies**: **Blocks on 1.1/1.2/2.3** (needs the correct Terms/Refund targets settled first).
- **Estimated effort**: Medium (structural section change, not just a link swap).
- **Risk**: Low-Medium — touches a sitewide section; needs a visual QA pass after the change.
- **Expected SEO/CRO impact**: Medium — one consistent, correct policy link set on every page.
- **Manual approval required**: **Yes** (visible footer layout change, even if content-equivalent).

### 2.6 Add missing internal links to/from delivery, eggless, and FAQ pages (`INTERNAL_LINKING.md` §2, `LOCAL_SEO_ROADMAP.md` §7/§8, `ARCHITECTURE_VERIFICATION.md` D2)

- **Description**: `/pages/cake-delivery-in-meerut` doesn't link to the FAQ page; the eggless page
  doesn't link out to the FAQ page; the FAQ page's sections should each link to their matching topic
  page (Delivery section → delivery page, Eggless section → eggless page, Hampers section → gift
  hampers page).
- **Files affected**: `templates/page.faq-01.json`, `templates/page.faq-02.json`, and the relevant
  Page bodies (`cake-delivery-in-meerut`, `100-percent-eggless-bakery`) via Admin API `pageUpdate`.
- **Dependencies**: None.
- **Estimated effort**: Small (adding hyperlinks into already-published copy, no new content).
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium — closes the "FAQ is an island" gap at genuinely relevant entry
  points, improving both crawl depth and on-site discovery.
- **Manual approval required**: No (adding links to existing approved copy, not new claims).

### 2.7 Cross-link the three hamper sibling pages and the Gift Hampers hub (`INTERNAL_LINKING.md`, `ARCHITECTURE_VERIFICATION.md` D5)

- **Description**: Verified this pass — `customised-hampers-meerut`, `festive-hampers-meerut`, and
  `surprise-hampers-meerut` link only to collections, not to `/pages/gift-hampers` or to each other.
  Add links between all four pages.
- **Files affected**: The 4 hamper Page bodies, via Admin API `pageUpdate`.
- **Dependencies**: None.
- **Estimated effort**: Small.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium — consolidates topical authority across the hamper cluster and
  improves cross-navigation for a customer researching hamper options.
- **Manual approval required**: No.

### 2.8 Convert Gift Hampers' "Related Collections" from plain text to real links (`INTERNAL_LINKING.md`, `ARCHITECTURE_VERIFICATION.md` D4)

- **Description**: Verified this pass — the "Related Collections" list on `/pages/gift-hampers` is
  plain `<li>` text with no `<a>` tags at all.
- **Files affected**: `/pages/gift-hampers` Page body, via Admin API `pageUpdate`.
- **Dependencies**: None.
- **Estimated effort**: Small.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium — the richest page on the site currently sends zero internal
  link equity to 6 relevant collections.
- **Manual approval required**: No.

---

## Sprint 3 — Collections

### 3.1 Implement the collection consolidation decision (depends on 1.6)

- **Description**: Execute whichever outcome 1.6 decides — unpublish the non-canonical "Meerut"
  collections, or repurpose/differentiate them if a real distinct use is found.
- **Files affected**: Shopify Admin → Collections.
- **Dependencies**: **Hard dependency on 1.6.**
- **Estimated effort**: Small (Admin publish/unpublish actions).
- **Risk**: Low once decided; verify no live menu/page links to a collection about to be unpublished
  first (none currently confirmed in this audit, but re-check before executing).
- **Expected SEO/CRO impact**: High (see 1.6).
- **Manual approval required**: No additional approval beyond 1.6's (this is execution of an already-
  approved decision).

### 3.2 Wire real sort logic for "Best Selling"/"Newest Products" or unpublish (depends on 1.6)

- **Description**: Execute whichever outcome 1.6 decides for these two collections.
- **Files affected**: Shopify Admin → Collections (smart collection sort rules).
- **Dependencies**: **Hard dependency on 1.6.**
- **Estimated effort**: Small.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium — a "Best Selling" collection that actually curates is a real
  CRO asset (social-proof-adjacent, even without explicit review data).
- **Manual approval required**: No additional approval beyond 1.6's.

### 3.3 Cross-link core collections to delivery/policy content (`CONTENT_PLAN.md` Collections brief)

- **Description**: Each core collection (Birthday, Anniversary, Wedding, Designer & Theme, Hampers)
  should link to its single most relevant delivery page from its description.
- **Files affected**: Collection description fields, via Admin API `collectionUpdate`.
- **Dependencies**: None technical; Wedding's link target (a venue-setup FAQ or future Wedding page)
  is richer if 4.x/Wedding content work (see Sprint 4/`CONTENT_PLAN.md`) lands first, but a baseline
  link to the FAQ's existing venue-setup answer works today.
- **Estimated effort**: Small.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium — closes a currently-zero internal link path between the
  commercial collections and the content that answers logistics questions before purchase.
- **Manual approval required**: No.

### 3.4 Festival collection expansion (`WEBSITE_ARCHITECTURE.md` §12)

- **Description**: Replicate the real, working Diwali pattern (`luxury-diwali-hampers`, 44 products)
  for other festivals named on the Gift Hampers page (Rakhi, Karwa Chauth, Christmas, etc.) — only
  for festivals with enough real, distinct inventory to justify a dedicated collection.
- **Files affected**: New Shopify collections (Admin), `URL_STRUCTURE.md`'s established
  `/collections/{festival}-hampers` pattern.
- **Dependencies**: **Business approval on which festivals clear the inventory bar** — this document
  does not invent inventory levels.
- **Estimated effort**: Medium (one collection setup per approved festival).
- **Risk**: Low — additive, no existing content touched.
- **Expected SEO/CRO impact**: Medium-High per festival, seasonal (real precedent already proves the
  format works).
- **Manual approval required**: **Yes** (which festivals, and confirming real inventory exists).

### 3.5 Fix the `criciket` handle typo (deferred)

- **Description**: `/collections/criciket` should be "cricket." Per `CLAUDE.md`'s standing
  handle-optimization policy, this is deliberately deferred until the full 8-step handle-change
  checklist (mapping → 301s → internal links → QR audit → indexing → sitemap → canonicals →
  monitoring) is run, not fixed in isolation.
- **Files affected**: Collection handle (Admin), plus a 301 redirect.
- **Dependencies**: The broader handle-optimization pass (not yet started, per `CLAUDE.md`).
- **Estimated effort**: Small in isolation, but deliberately bundled into a larger future pass.
- **Risk**: Low-Medium — any live handle change risks breaking a printed QR code or bookmarked link.
- **Expected SEO/CRO impact**: Low (cosmetic/credibility only — a visible typo in a URL, not a
  ranking factor by itself).
- **Manual approval required**: **Yes**, and explicitly not scheduled for this backlog's active
  sprints — listed here for completeness, tracked for the future handle-optimization pass instead.

---

## Sprint 4 — Homepage

### 4.1 Build homepage slot architecture (`WEBSITE_ARCHITECTURE.md` §5)

- **Description**: Structure the homepage as: hero → verifiable differentiators strip (100% eggless,
  same-day/midnight delivery, made-to-order) → occasion entry points (the same 6 collections from
  2.1) → hampers cross-sell → gated trust section → FAQ teaser → footer.
- **Files affected**: Homepage template/sections (theme).
- **Dependencies**: Should ship after 2.1 (so the homepage and header share one link set, not two
  independently-maintained ones).
- **Estimated effort**: Large (full homepage build).
- **Risk**: Medium — homepage is high-visibility; needs full visual QA before launch.
- **Expected SEO/CRO impact**: High — this is the highest-traffic page on the site once launched.
- **Manual approval required**: **Yes** (major visible layout work).

### 4.2 Hero photography swap (client-blocked, tracked in `CLAUDE.md`)

- **Description**: Replace the current temporary product shot with real studio photography, once
  available.
- **Files affected**: Homepage hero section/image asset.
- **Dependencies**: **Blocked entirely on the client providing real photography** — not something this
  backlog can schedule a date for.
- **Estimated effort**: Small (once the asset exists, swapping it in is trivial).
- **Risk**: None once the real asset lands.
- **Expected SEO/CRO impact**: High — real photography is one of the two items `CLAUDE.md` flags as
  unblocking multiple sections (hero + S6 Craft Story) at zero code cost.
- **Manual approval required**: **Yes** (waiting on the client's asset, not a development task).

### 4.3 Trust section content (client-blocked, tracked in `CLAUDE.md`/`EEAT_REPORT.md`)

- **Description**: S8 Trust section is built but has no content to show — gated on either a real
  FSSAI licence number or 3 real customer reviews landing.
- **Files affected**: Homepage trust section (theme, already built, just unpopulated).
- **Dependencies**: **Blocked on the client** (FSSAI number or Judge.me/review collection setup).
- **Estimated effort**: Small once inputs exist.
- **Risk**: None — architecture correctly reserves the slot rather than filling it with a placeholder.
- **Expected SEO/CRO impact**: High once unblocked (genuine trust signal, exactly where CRO evidence
  says it belongs).
- **Manual approval required**: **Yes**.

---

## Sprint 5 — Product Pages

### 5.1 Fix occasion-mismatch in product descriptions (already-written tool, `CLAUDE.md`)

- **Description**: ~100+ products still labelled "anniversary" when the actual occasion (e.g. baby
  girl/theme cakes) differs. Tool already exists: `seo-ops/fix_description_occasion.py`
  (dry-run → review CSV → `--apply`).
- **Files affected**: Product `descriptionHtml` via Admin API, batched per this project's
  `CODING_STANDARDS.md` (≤8-10 mutations per batch).
- **Dependencies**: None — tool is ready, this is an execution task.
- **Estimated effort**: Medium (running the dry-run, reviewing the CSV, then applying in batches).
- **Risk**: Low (dry-run-first workflow already de-risks this).
- **Expected SEO/CRO impact**: Medium — corrects a real, customer-visible mismatch between product
  and description on 100+ live pages.
- **Manual approval required**: **Yes** for the review-CSV sign-off before `--apply`, per this
  project's standing dry-run-by-default convention.

### 5.2 Full duplicate-title/thin-content sweep across all 602 active products (`seo/TECHNICAL_SEO.md`)

- **Description**: Only spot-checked so far (the flagship product's SEO title format was confirmed).
  A full bulk export/check across all 602 active products' `seo.title`/`seo.description` hasn't run.
- **Files affected**: Read-only Admin API export; any found duplicates would become their own
  follow-up tasks.
- **Dependencies**: None.
- **Estimated effort**: Medium (bulk export + analysis; fixes, if any are found, would be scoped
  separately once the scale of the problem is known).
- **Risk**: Low (read-only analysis task).
- **Expected SEO/CRO impact**: Unknown until run — potentially Medium-High if duplicates are found at
  scale across 602 products.
- **Manual approval required**: No for the analysis; **Yes** for any resulting content changes.

### 5.3 Variant option typo fix — `fruit-cocoktail`, `chocolate-moouse` (deferred, `CLAUDE.md`)

- **Description**: Real typos in variant option values. Deliberately deferred — touching option
  values risks deleting variants; needs a metaobject-based fix first, per standing project policy.
- **Files affected**: Product variant options (Admin API `productOptionUpdate`, always with
  `variantStrategy: LEAVE_AS_IS` per `CLAUDE.md`'s golden rules).
- **Dependencies**: The metaobject fix this needs hasn't been scoped yet — a prerequisite task, not
  included in this backlog.
- **Estimated effort**: Not yet scoped (blocked on the prerequisite).
- **Risk**: **High if attempted directly** — this is exactly why it's deferred; a naive option-value
  edit can silently delete variants.
- **Expected SEO/CRO impact**: Low-Medium (cosmetic typo visible to customers at checkout/variant
  selection).
- **Manual approval required**: **Yes**, and explicitly out of scope for active scheduling until the
  metaobject prerequisite is designed.

### 5.4 Product handle cleanup — opaque codes and pure-numeric handles (deferred, `URL_STRUCTURE.md` E1)

- **Description**: Handles like `b110`, and pure-numeric handles (`5`, `28`, `29`...) alongside
  readable ones. Real SEO upside from keyword handles, but deferred per `CLAUDE.md`'s standing
  8-step checklist (mapping → 301s → internal links → QR audit → indexing → sitemap → canonicals →
  monitoring) — starts only after the homepage ships and duplicate drafts are archived.
- **Files affected**: Product handles (Admin), plus 301 redirects for every changed handle.
- **Dependencies**: Explicitly sequenced after Sprint 4 (homepage) per `CLAUDE.md`'s own stated order.
- **Estimated effort**: Large (602 active products, many with non-ideal handles) — this is a
  dedicated future project, not a quick task.
- **Risk**: **High** if done without the full checklist — printed QR codes on physical packaging can
  silently break.
- **Expected SEO/CRO impact**: High (real keyword-handle SEO upside), but only once safely executed.
- **Manual approval required**: **Yes**, and not scheduled within this backlog's active sprints —
  listed for completeness per `CLAUDE.md`'s existing deferral.

---

## Sprint 6 — Local SEO

### 6.1 Google Business Profile consistency check (`LOCAL_SEO_ROADMAP.md` P0.3)

- **Description**: Once the address/hours are confirmed internally (1.3), compare against the real
  GBP listing — this session has no GBP access; needs the business or a browser session with login.
- **Files affected**: None (external platform, GBP dashboard).
- **Dependencies**: **Hard dependency on 1.3.**
- **Estimated effort**: Small (a manual comparison once both sides are known).
- **Risk**: Low.
- **Expected SEO/CRO impact**: High — NAP consistency between site and GBP is a core Local Pack
  ranking factor.
- **Manual approval required**: **Yes** (requires GBP login access this session doesn't have).

### 6.2 Build the Delivery Areas hub page (`DELIVERY_AREA_SPEC.md`, repurposing Store Locator per 1.7)

- **Description**: Content specification is fully written and ready. Build the real page, linking to
  the three existing delivery-mode pages.
- **Files affected**: New/repurposed page template (built from `templates/page.store-locations.json`
  if repurposing, per 1.7's decision).
- **Dependencies**: **Hard dependency on 1.4 (area-list decision) and 1.7 (repurpose-vs-delete decision).**
- **Estimated effort**: Medium.
- **Risk**: Low (content spec already de-risks the "what goes on this page" question).
- **Expected SEO/CRO impact**: High — a real, non-fake Delivery Areas page targeting exactly the
  local-intent queries this business should rank for.
- **Manual approval required**: **Yes** (net-new published page).

### 6.3 Per-locality delivery pages (only if approved, `LOCAL_SEO_ROADMAP.md` §6)

- **Description**: Dedicated pages per confirmed serviceable locality, if the business judges the
  investment worthwhile.
- **Files affected**: New pages, one per approved locality.
- **Dependencies**: **Hard dependency on 1.4** (need the confirmed list first) and a separate
  investment-sizing decision (how many localities merit a dedicated page).
- **Estimated effort**: Medium-Large, scales with the number of localities approved.
- **Risk**: Low technically; the real risk is investing in pages for localities that don't drive
  meaningful search volume — size this only once 1.4 is confirmed.
- **Expected SEO/CRO impact**: Medium-High per page, if the locality has real local-search demand.
- **Manual approval required**: **Yes**.

### 6.4 Expand LocalBusiness schema `areaServed` from city-level to neighborhood-level (`LOCAL_SEO_ROADMAP.md` P1.5)

- **Description**: Currently a single "Meerut" city entity; expand to the confirmed neighborhood list.
- **Files affected**: `snippets/bk-local-business.liquid`.
- **Dependencies**: **Hard dependency on 1.4.** Should ship alongside 6.2, not independently.
- **Estimated effort**: Small (schema edit once the list is confirmed).
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium — richer structured data for neighborhood-level local search.
- **Manual approval required**: No, once 1.4 is settled (mechanical schema update).

### 6.5 Re-check `sitemap.xml` once the password gate lifts (SEO-019)

- **Description**: Currently 404s — very likely a symptom of the password gate, not confirmed either
  way while it's active.
- **Files affected**: None (verification task).
- **Dependencies**: **Blocked on the storefront password gate lifting** (a separate, business-timed
  launch decision, not a development task).
- **Estimated effort**: Small (a single fetch-and-check once the gate is down).
- **Risk**: Low.
- **Expected SEO/CRO impact**: High if it turns out to be a real misconfiguration (a broken sitemap
  meaningfully hurts crawl/index coverage) — unknown severity until re-checked.
- **Manual approval required**: No (verification only); any fix found would be scoped separately.

---

## Sprint 7 — Performance

### 7.1 Remove the hidden duplicate `<h1>` in `layout/theme.liquid` (SEO-025)

- **Description**: A `display:none` duplicate H1 renders sitewide. Safe removal needs confirming every
  other page type still has its own visible H1 first — this hasn't been done yet.
- **Files affected**: `layout/theme.liquid`.
- **Dependencies**: The template-by-template heading check itself is a prerequisite sub-task.
- **Estimated effort**: Small fix, Medium prerequisite investigation.
- **Risk**: Low-Medium — removing it without confirming every page type has its own H1 first could
  leave some page type headless.
- **Expected SEO/CRO impact**: Low-Medium (a minor on-page SEO cleanliness issue, not a major ranking factor).
- **Manual approval required**: No (technical fix, no business decision involved) — but requires the
  investigation step first.

### 7.2 Full Core Web Vitals / Lighthouse pass once the password gate lifts

- **Description**: One real fix already made this project (LCP lazy-loading, SEO-026); no full
  Lighthouse/PageSpeed score exists yet because the gate blocks real measurement.
- **Files affected**: TBD, pending what a real measurement surfaces.
- **Dependencies**: **Blocked on the password gate lifting.**
- **Estimated effort**: Small to run once ungated; follow-up fixes sized once findings exist.
- **Risk**: Low (measurement task).
- **Expected SEO/CRO impact**: Unknown until measured — Core Web Vitals are a confirmed ranking factor.
- **Manual approval required**: No for the measurement; **Yes** implicitly for the gate-lift timing
  itself (a launch decision, not this backlog's to make).

### 7.3 Image optimization, lazy-loading, and compression audit (`seo/TECHNICAL_SEO.md`)

- **Description**: Requires either a live page render (blocked by the gate) or infrastructure-level
  checks not performed yet.
- **Files affected**: TBD.
- **Dependencies**: Same gate dependency as 7.2 — can partially run in parallel via code-level review
  without waiting for the gate, but full confirmation needs live rendering.
- **Estimated effort**: Medium.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium-High (image weight is a common, high-leverage Core Web Vitals lever).
- **Manual approval required**: No.

### 7.4 Security headers and caching review (`seo/TECHNICAL_SEO.md`)

- **Description**: Response headers and CDN config weren't checked this pass; HTTPS itself is
  Shopify-default and not in question.
- **Files affected**: TBD (infrastructure-level, not theme files).
- **Dependencies**: None blocking, but lower priority than the gate-blocked items above.
- **Estimated effort**: Small (a header/config audit).
- **Risk**: Low.
- **Expected SEO/CRO impact**: Low-Medium.
- **Manual approval required**: No.

---

## Sprint 8 — AI SEO (GEO)

### 8.1 Reconcile `sameAs` inconsistency between Organization and Bakery schema (SEO-020)

- **Description**: The Organization entity's `sameAs` lists Instagram only; the Bakery entity's lists
  Instagram + Facebook. Same real business, two schema sources disagreeing — reconcile to whichever
  list is actually current.
- **Files affected**: `snippets/tbk-schema-website.liquid` and/or `snippets/bk-local-business.liquid`.
- **Dependencies**: Needs confirmation of the current real social-profile list (small business input,
  not a major decision).
- **Estimated effort**: Small.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Low-Medium — entity-graph consistency is exactly what AI knowledge-graph
  matching depends on, per `GEO_AUDIT.md`.
- **Manual approval required**: **Yes**, minimally (confirm the real, current profile list).

### 8.2 Verify Shopify Liquid `article` object's real update-timestamp property (SEO-021)

- **Description**: `dateModified` is hardcoded to equal `datePublished` in `tbk-schema-article.liquid`
  — under-reports freshness for edited articles if Shopify exposes a real last-modified property.
- **Files affected**: `snippets/tbk-schema-article.liquid`.
- **Dependencies**: Needs checking against Shopify's documented Liquid objects first (a small research
  task) before any code change.
- **Estimated effort**: Small.
- **Risk**: Low (affects freshness signals only, not indexability).
- **Expected SEO/CRO impact**: Low.
- **Manual approval required**: No.

### 8.3 AI citation testing (`GEO_AUDIT.md` — Requires Manual Verification)

- **Description**: Test actual AI systems (ChatGPT, Perplexity, Gemini) for "eggless cake Meerut"-type
  queries to see if/how this brand surfaces. External, ongoing measurement — not something a code
  audit can determine directly, and not something this backlog can execute as a one-time dev task.
- **Files affected**: None (external measurement).
- **Dependencies**: Ideally run after the password gate lifts and content fixes (Sprints 1-6) have
  shipped, so the measurement reflects the improved site, not the pre-fix state.
- **Estimated effort**: Small per test round, but ongoing/recurring rather than one-and-done.
- **Risk**: None (measurement only).
- **Expected SEO/CRO impact**: Informational — establishes a baseline to measure future GEO work against.
- **Manual approval required**: No (recommend the business or a marketing owner runs this periodically).

### 8.4 Confirm FAQ schema and cross-linking closes the "chunkability" gap (`GEO_AUDIT.md`)

- **Description**: The FAQPage schema/content gap (SEO-013) is now fixed; this task verifies the
  Sprint 2 cross-linking work (2.6) actually closes the structural gap `GEO_AUDIT.md` flagged as the
  main blocker to AI answerability.
- **Files affected**: None new — a verification pass over Sprint 2's work.
- **Dependencies**: **Depends on 2.6 shipping first.**
- **Estimated effort**: Small (a verification check, not new work).
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium — confirms real ROI on the FAQ content investment already made.
- **Manual approval required**: No.

### 8.5 Populate Wedding/Corporate content once business inputs land (ties `CONTENT_PLAN.md` to GEO answerability)

- **Description**: Once the Wedding Cakes page (if approved, per `WEBSITE_ARCHITECTURE.md` §10) and
  Corporate Gifting page (§11) are populated with real content, ensure they're well-chunked
  (clear headings, direct answers) for AI-search extraction, consistent with the pattern already
  working on the FAQ and Gift Hampers pages.
- **Files affected**: The relevant Page bodies, once populated.
- **Dependencies**: **Depends on the underlying content decisions in Sprint 4/`CONTENT_PLAN.md`**
  (business inputs: minimum order size, GST/invoicing, whether a dedicated Wedding page is worth building).
- **Estimated effort**: Small (a structure/formatting check layered onto content work already scoped
  elsewhere) — not double-counted as new content-writing effort here.
- **Risk**: Low.
- **Expected SEO/CRO impact**: Medium, once the underlying content exists.
- **Manual approval required**: No additional approval beyond what the underlying content task already requires.

---

## Cross-sprint dependency summary

```
1.1 (policy terms) ──┬──> 1.5 (footer links) ──> 2.5 (footer consolidation)
                      └──> 2.3 (quick-links menu)
1.2 (empty Terms) ────┴──> (same as above)
1.3 (address/geo) ───────> 6.1 (GBP check), 6.4 (schema areaServed)
1.4 (area list) ──────┬──> 2.2 (meerut-delivery menu, partial)
                      ├──> 6.2 (Delivery Areas hub)
                      ├──> 6.3 (per-locality pages)
                      └──> 6.4 (schema areaServed)
1.6 (collection cluster) ─> 3.1, 3.2
1.7 (Store Locator fate) ─> 6.2
2.1 (header nav) ─────────> 4.1 (homepage, shares link set)
2.6 (FAQ links) ──────────> 8.4 (GEO verification)
Sprint 4 (homepage) ──────> 5.4 (handle cleanup, explicitly sequenced after per CLAUDE.md)
Password gate lift ───────> 6.5, 7.2, 7.3 (partially)
```

## Related

[../issues.yml](../issues.yml), [../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md),
[WEBSITE_ARCHITECTURE.md](WEBSITE_ARCHITECTURE.md), [POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md),
[ARCHITECTURE_VERIFICATION.md](ARCHITECTURE_VERIFICATION.md), [CONTENT_PLAN.md](CONTENT_PLAN.md),
[LOCAL_SEO_ROADMAP.md](LOCAL_SEO_ROADMAP.md), [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md).
