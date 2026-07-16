# CHANGELOG — The Baking Kaur Enterprise Transformation

Living record of every file changed: what, why, and how to roll back.
Format per entry: **File · Reason · Business · SEO · Performance · Risk · Rollback.**

Rollback baseline for the whole transformation: branch `phase-a/production-safety`, commit **`2aeff64`** ("Phase A baseline snapshot"). `git checkout 2aeff64 -- <path>` restores any single file; `git reset --hard 2aeff64` restores everything.

---

## Phase A — Production Safety & Cleanup  *(staged in repo, not yet deployed)*

### A1. Rollback baseline
- **File:** (git) branch `phase-a/production-safety` @ `2aeff64`
- **Reason:** capture full working tree before any change.
- **Business/SEO/Perf:** none (safety only). **Risk:** none.
- **Rollback:** n/a — this *is* the rollback point.

### A2. Dead-code removal (10 files)
- **Files removed:**
  `sections/cart-drawer-hulkapps-backup.liquid`, `sections/header-e-commerce-hulkapps-backup.liquid`, `sections/header-inline-hulkapps-backup.liquid`, `sections/main-cart-hulkapps-backup.liquid`, `sections/main-gift-cart-hulkapps-backup.liquid`, `snippets/cart-checkbox-hulkapps-backup.liquid`, `snippets/cart-complementary-hulkapps-backup.liquid`, `snippets/cart-shipping-bar-hulkapps-backup.liquid`, `snippets/item-cart-hulkapps-backup.liquid`, `snippets/item-cart-page-hulkapps-backup.liquid`
- **Reason:** orphaned HulkApps migration backups — verified **0 references** across all `.liquid`/`.json`.
- **Business:** cleaner, faster-to-maintain theme; less editor confusion. **SEO:** none. **Perf:** none at runtime (unreferenced); smaller theme package.
- **Risk:** ○ very low (proven unreferenced). **Rollback:** `git checkout 2aeff64 -- <path>`.

### A3. Duplicate schema removal — conflicting Bakery entity
- **File:** `layout/theme.liquid`
- **Reason:** an inline `Bakery` JSON-LD block duplicated `snippets/bk-local-business.liquid` **with conflicting geo (28.9845,77.7064 vs 28.9931,77.6939) and hours (21:00 vs 23:59)**. Removed the inline block; `bk-local-business` is now the single Bakery source.
- **Business:** consistent business info to Google/AI. **SEO:** high-positive — removes a conflicting duplicate LocalBusiness entity. **GEO:** cleaner entity graph. **Perf:** minor (less inline JSON).
- **Risk:** ○ low (one entity remains). **Rollback:** `git checkout 2aeff64 -- layout/theme.liquid`. **Validate:** Rich Results Test on deploy.

### A4. Duplicate schema removal — WebSite & BreadcrumbList
- **File:** `snippets/structured-data.liquid`
- **Reason:** emitted a 2nd `WebSite` (dup of `tbk-schema-website.liquid`) and a 2nd `BreadcrumbList` (dup of `tbk-schema-breadcrumb.liquid`). Rewrote to keep ONLY Shopify-native `Product`/`Article` schema (its unique, valuable contribution).
- **Business:** correct rich results. **SEO:** high-positive — removes duplicate WebSite + Breadcrumb; **preserves native Product schema**. **GEO:** single canonical entities. **Perf:** minor.
- **Risk:** ◐ medium (schema surface). **Rollback:** `git checkout 2aeff64 -- snippets/structured-data.liquid`. **Validate:** Rich Results Test on Home/Product/Collection/Article before promote.

### Canonical schema sources after Phase A
| Entity | Source |
|---|---|
| Organization + WebSite | `snippets/tbk-schema-website.liquid` |
| Bakery / LocalBusiness | `snippets/bk-local-business.liquid` |
| BreadcrumbList | `snippets/tbk-schema-breadcrumb.liquid` |
| Product / Article (native) | `snippets/structured-data.liquid` |
| FAQPage | inline in `theme.liquid` *(placement flagged — see SEO plan)* |

### A6. Restore missing site footer (approved: minimal, production-safe)
- **Files added:** `sections/site-footer.liquid`, `sections/footer-group.json`
- **Reason:** production rendered **no footer** — `theme.liquid` called `sections 'footer-group'` but that group existed on neither repo nor live theme; `footer.liquid` (broken ``` fence, no schema) and `tbk-footer.liquid` (hardcoded, no schema) were orphaned and unusable. Built a minimal, semantic, token-styled footer wired via a new `footer-group.json`.
- **Content (all real):** NAP (`<address>`), `tel:`/`mailto:`, Instagram + WhatsApp, Company/Delivery links to **verified** pages, policies via native `shop.*_policy` (all four resolve), trust strip, copyright. Editable via section settings.
- **Business:** restores trust, navigation, legal-policy access (compliance). **SEO:** footer internal-linking backbone + `SiteNavigationElement`. **GEO:** NAP reinforcement. **Perf:** negligible (scoped CSS, lazy logo).
- **A11y:** `role="contentinfo"`, 3 labelled `<nav>`, `<address>`, visible focus rings, sr-only heading.
- **Risk:** ○ low (additive; no new visual language — uses `tbk-tokens`). **Rollback:** `git rm sections/site-footer.liquid sections/footer-group.json` (or `git checkout 2aeff64`), then footer reverts to prior (absent) state.
- **Note:** premium enterprise footer deferred to Phase E; this is the temporary production-safe restore.

### Phase A validation (on preview theme `colorful-composition` #151370334377)
- Footer renders: `contentinfo`, 3 navs, all links correct, all 4 policies resolve, copyright + NAP present.
- **Schema dedup verified in rendered HTML: Bakery ×1, WebSite ×1, BreadcrumbList ×1** (was ×2 each); native Product schema intact; footer `SiteNavigationElement` present.
- Mobile 375px: single-column stack, **no horizontal overflow**. Brand token bg `#FDFAF8` applied.
- Caught + fixed 2 issues during validation: (1) `url`-type schema settings can't take URL defaults → switched to `text`; (2) `footer-group.json` was rejected on first push because the section it referenced had an invalid schema → re-pushed after fix.
- **Pre-existing issue observed (not introduced):** `tbk-schema-website` throws a Liquid error when `settings.logo` is blank (`image_url` on empty) — flagged for Phase B/F.
- **Deploy state:** staged + validated on preview only. **NOT yet on the live theme** — awaiting approval to promote.

---

## Phase A — DEFERRED (with reasons)
| Item | Why deferred | Owner phase |
|---|---|---|
| **Duplicate Uploadcare load** in `theme.liquid` | Feeds the **protected** PDP reference-image upload; removing a load needs PDP regression testing. | A-2 (post-approval) w/ PDP test |
| **3 whole-document MutationObservers** | Each masks a root cause (sticky bar, `<` arrows, mojibake data). Removing blind reintroduces bugs. | B/H after root-cause |
| **Global FAQPage schema** | Not a duplicate — a placement issue (should be page-scoped). | F/G |
| **Self-asserted AggregateRating** in `bk-local-business` | SEO-quality (needs real review source), not a duplicate. | F |
| **Disabled header backups** in `header-group.json` (`announcement-bar`, `header-e-commerce`, `header-menu-bottom-hulkapps-backup`) | Editing the active header group belongs with header consolidation. | E |
| **`rewind_*` legacy pair** | Marked "do_not_delete"; verify no page uses the template first. | B |

---

## Phase A — PROMOTED TO LIVE (2026-07-14)
Scoped push of `layout/theme.liquid`, `snippets/structured-data.liquid`, `sections/site-footer.liquid`, `sections/footer-group.json` → live theme `Baking Kaur — Draft` (#151307485353, `--allow-live`).
**Verified on live:** footer restored (4 navs, 22 links, 6 policies, NAP, copyright); schema deduped (Bakery/WebSite/Breadcrumb ×1, 0 parse errors); protected PDP intact (premium markers present); collections/search/cart/policies 200; CLS 0; mobile 3-col nav + 2-line trust, no overflow.
**Found (pre-existing, not Phase A):** `tbk-schema-website` Liquid error on blank `settings.logo` (Organization logo field malformed); homepage H1 count = 2; full load ~24.5s.
**Rollback:** `git checkout 2aeff64 -- layout/theme.liquid snippets/structured-data.liquid` + remove footer files, then push to #151307485353.


---

## Phase C1 §2 — Delivery Promise (FROZEN v1.0) — preview only
- **Files:** `sections/home-delivery-promise.liquid` (new), `templates/index.json` (section added as §2, 6 blocks).
- **Reason:** communicate trust immediately below the hero; assembly of the frozen card system (zero new components).
- **Business:** trust + internal linking to delivery/eggless/custom pages. **SEO:** 6 new internal links, semantic list, no H2 pollution, page keeps exactly 1 H1. **GEO:** reinforces same-day/midnight cake delivery in Meerut, eggless, custom designer cakes. **Perf:** zero JS, zero images (inline SVG), CLS 0.
- **Links:** all 6 destinations verified HTTP 200. 4 of the recommended routes 404'd (`same-day-cake-delivery`, `eggless-cakes` collection, `our-promise`, `cake-customization`) → linked to verified pages instead; canonical routes recorded as placeholders (Phase G). `/collections/eggless-cakes` intentionally not created (would duplicate `/collections/all`).
- **Bug fixed in build:** unclosed `{% if count > 0 %}` nested the `{% schema %}` tag → push rejected; fixed + tag-balance check added to validation.
- **Risk:** ○ low (additive, preview only). **Rollback:** `git rm sections/home-delivery-promise.liquid` + remove `home_promise` from `templates/index.json`, or `git checkout 2aeff64 -- templates/index.json`.
