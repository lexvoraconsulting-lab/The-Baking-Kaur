# Architecture Verification

Generated 2026-07-30. Every recommendation in `WEBSITE_ARCHITECTURE.md`, `SITE_TREE.md`,
`NAVIGATION.md`, `URL_STRUCTURE.md`, and `INTERNAL_LINKING.md` re-checked against a **fresh** live
Admin API query and/or theme-file grep run this pass (not a restatement of the original documents'
own evidence, though the two agree throughout — nothing in the underlying Shopify configuration has
changed since those documents were written). No new architecture is proposed here. One previously
explicitly-unverified claim (`INTERNAL_LINKING.md`'s hamper-siblings cross-linking) is resolved with
real evidence for the first time in this pass.

Status legend: **Verified** (re-checked, still accurate) · **Needs business approval** (accurate, and
already correctly marked `<<BUSINESS APPROVAL REQUIRED>>` in the source document) · **Obsolete**
(state has changed, recommendation no longer applies) · **Already implemented** (verification found
the gap the recommendation described no longer exists).

## A. Navigation — from NAVIGATION.md / SITE_TREE.md

| # | Recommendation | Current live state | Evidence | Action required | Risk | Priority | Status |
|---|---|---|---|---|---|---|---|
| A1 | Wire the live header to the 6 real collection links sitting in the `header` menu instead of the sparse 4-item `main-menu` | Unchanged: `tbk_header_main` (the live header block) still sets `"main_menu": "main-menu"`; the `header` menu (Birthday/Anniversary/Diwali/Theme/Hampers/Wedding) is still referenced only by `header_menu_bottom_hulkapps_backup_kgkQBL`, still `"disabled": true` | Fresh grep, `sections/header-group.json` line 62 (`main_menu: main-menu`) and line 220 (`main_menu: header`, inside a block still marked `disabled: true` at line 207) | Implement Option A or B from `NAVIGATION.md` §1 — requires a visible-layout sign-off per this project's convention | Low technical risk (reusing existing, already-tested linklists); the only risk is a visible nav change without explicit go-ahead | High — single biggest navigation gap on the site | **Needs business approval** (visual sign-off) |
| A2 | Fix the footer's Refund link, which falls back to the unpublished draft page instead of the canonical live page | Unchanged: `site-footer.liquid` line 100-101 still reads `{% if shop.refund_policy != blank %}...{% else %}<a href="/pages/return-refund-replacement-policy">{% endif %}`; `shop.refund_policy` is still non-blank, so the live link goes to the Shop Policy side of the SEO-031 conflict | Fresh grep, `sections/site-footer.liquid` lines 100-101; fresh policy query confirms `shop.refund_policy` still resolves (`REFUND_POLICY`, id `28553805993`) and the draft page (`gid://shopify/Page/115495272617`) is still `isPublished: false` | Depends on `POLICY_ARCHITECTURE.md`'s canonical decision — not actionable until that lands | Medium — a customer following this link today reaches the "no refunds ever" Shop Policy, not the more permissive canonical candidate | High (tied to SEO-031, already Critical) | **Needs business approval** |
| A3 | Fix the footer's Terms link, hardcoded to the empty custom page instead of `shop.terms_of_service.url` | Unchanged: line 98-99 shows the pattern is already correctly implemented for the `shop.terms_of_service != blank` case but falls through to `/pages/terms-and-conditions` — and separately, line 127 hardcodes `/pages/terms-and-conditions` directly with no conditional at all | Fresh grep, `sections/site-footer.liquid` lines 98-99, 127. Fresh page query confirms `/pages/terms-and-conditions` (`gid://shopify/Page/110844510377`) is still `isPublished: true`, `body: ""` (still empty) | Same as A2 — depends on Terms canonical decision | Medium — line 127's unconditional hardcode means even fixing `shop.terms_of_service` wouldn't fully resolve this without also editing line 127 | High (tied to SEO-034) | **Needs business approval**, with one **Verified** sub-finding: line 127's unconditional link is a distinct, separate defect from line 99's fallback, missed as a single item in the original `NAVIGATION.md` wording — worth treating as two fixes, not one |
| A4 | Populate the empty `meerut-delivery` menu as the Delivery Areas navigation home | Unchanged: `meerut-delivery` menu still exists with 0 items | Fresh `menus` query this pass: `{"handle":"meerut-delivery","title":"Meerut Delivery","items":[]}` | Populate once the Delivery Areas hub page exists (depends on SEO-030/SEO-035 decisions) | Low | Medium | **Needs business approval** (content/page must exist first) |
| A5 | Fix `quick-links-menu`'s Terms item (currently `type: PAGE` → empty page) to match its correctly-typed Privacy/Refund/Shipping siblings | Unchanged: `quick-links-menu` still has `{"title":"Terms & Condition","url":"/pages/terms-and-conditions","type":"PAGE"}` alongside 3 correctly-typed `SHOP_POLICY` items | Fresh `menus` query this pass, same structure as originally found | Same as A3 — depends on Terms canonical decision | Low-Medium | Medium | **Needs business approval** |
| A6 | Drop "Store Locations" from `about-us-menu` (points at the unpublished fake page) | Unchanged: `about-us-menu` still lists `{"title":"Store Locations","url":"/pages/store-locator", "type":"PAGE"}`; `/pages/store-locator` confirmed still `isPublished: false` this pass | Fresh `menus` query + fresh page query, `gid://shopify/Page/110839595177` → `isPublished: false` | No action needed unless/until this menu is ever wired to a live section — verify before surfacing it anywhere | Low (menu isn't confirmed wired to anything live, so no live 404 currently reaches a real visitor) | Low | **Verified** (finding still accurate; not urgent since not confirmed live) |
| A7 | Three menu handles (`explore-cakes`, `quick-links`, `meerut-delivery`) are empty shells | Unchanged, all three still return `"items": []` | Fresh `menus` query this pass | Reuse per `NAVIGATION.md`, not invent new handles | None (informational) | Low | **Verified** |

## B. Collection architecture — from WEBSITE_ARCHITECTURE.md §6 / SITE_TREE.md

| # | Recommendation | Current live state | Evidence | Action required | Risk | Priority | Status |
|---|---|---|---|---|---|---|---|
| B1 | 5 primary occasion collections need no structural change | Unchanged counts: Birthday 279, Anniversary 102, Wedding 134, Designer & Theme 165, Cake Hampers 119 | Fresh `collections` query this pass, byte-identical counts to the original audit | None | None | — | **Verified** |
| B2 | 13 theme sub-collections are real and distinct, keep as-is | Unchanged — all 13 handles/counts confirmed present (Baby Girl 28, Butterfly 23, Criciket 10, Motu Patlu 12, Unicorn 16, Jungle Animal Theme 17, Chartered Accountant 10, roblox 8, PAW PETROL 4, Teddy 7, ribbon-cake 8, KPOP Cake 9, boy-or-girl-cake 12) | Fresh `collections` query this pass | None | None | — | **Verified** |
| B3 | "Best Selling Products" and "Newest Products" are non-curating (both = 1,235, identical to `/collections/all`) | Unchanged: `best-selling-products` = 1,235, `newest-products` = 1,235, `all` = 1,235 | Fresh `collections` query this pass, all three counts identical | `<<BUSINESS APPROVAL REQUIRED>>` — wire real sort logic or unpublish | Low-Medium (small trust-signal issue, not a legal one) | Medium | **Needs business approval** |
| B4 | 7-collection "Meerut" cluster all resolve to the same ~986-product set | Unchanged: `cakes` 986, `cake-delivery-meerut` 986, `same-day-cake-delivery-meerut` 986, `midnight-cake-delivery-meerut` 986, `midnight-cake-delivery` 986, `custom-cakes-meerut` 617 (still the one outlier), `kids-birthday-cakes-meerut` 128 | Fresh `collections` query this pass, all 7 counts match the original audit exactly | `<<BUSINESS APPROVAL REQUIRED>>` — pick at most 1-2 to keep, unpublish the rest | Medium — active duplicate-content SEO risk, same family as SEO-031 | High | **Needs business approval** |
| B5 | `/collections/criciket` handle typo (should be "cricket") | Unchanged — handle still `criciket`, title still "Criciket" | Fresh `collections` query this pass | Deferred per `CLAUDE.md`'s handle-optimization policy — no action now | Low (handle rename risk to QR codes, per standing policy) | Low, deliberately deferred | **Verified** (and correctly left unactioned) |

## C. Pages — from SITE_TREE.md

| # | Recommendation/claim | Current live state | Evidence | Action required | Risk | Priority | Status |
|---|---|---|---|---|---|---|---|
| C1 | `/pages/terms-and-conditions` is live, published, with a completely empty body (SEO-034) | Unchanged — `isPublished: true`, `body: ""` | Fresh `page` query this pass, `gid://shopify/Page/110844510377` | Populate or unpublish, per `POLICY_ARCHITECTURE.md` | Legal/trust gap, unchanged | High | **Verified** |
| C2 | `/pages/refund-return-policy` is the live canonical-candidate Refund page | Unchanged — `isPublished: true` | Fresh `pages(query: "handle:refund-return-policy")` this pass, `gid://shopify/Page/116206305449` | Awaiting `POLICY_ARCHITECTURE.md` approval | — | High | **Verified** |
| C3 | `/pages/return-refund-replacement-policy` (draft) remains unpublished | Unchanged — `isPublished: false` | Fresh `page` query this pass | Merge-then-delete, per `POLICY_REDIRECT_PLAN.md`, once approved | Low (already unpublished) | Medium | **Verified** |
| C4 | `/pages/store-locator` remains unpublished (SEO-030, Mitigated) | Unchanged — `isPublished: false` | Fresh `page` query this pass | Permanent-fate decision still open | Low (already mitigated) | Medium | **Verified** |
| C5 | `/pages/corporate-gifting-solutions` remains unpublished, empty body | Unchanged — `isPublished: false`, `body: ""` | Fresh `page` query this pass | Populate per `CONTENT_PLAN.md`'s open questions | Low (unpublished, no live exposure) | Low-Medium | **Verified** |
| C6 | No blog exists on this storefront | **Partially inaccurate as originally worded** — a Shopify blog object *does* exist (`"News"`, handle `news`), just with (unverified this pass, but) presumably no live articles/navigation exposure, since no blog link appears in any menu or page checked this or the prior session | Fresh `blogs(first: 10)` query this pass: one blog, `gid://shopify/Blog/89372491945`, title "News", handle "news" | Correct the record: a blog object exists but is unused/unlinked — the real open question is unchanged (does the business want to use it), but "no blog exists" should be restated as "a blog object exists, unused and unlinked, with content status not yet checked" | None new | Low | **Needs correction** (see note below) |

**Note on C6**: this is the one place verification changed the record. `CONTENT_PLAN.md` and
`WEBSITE_ARCHITECTURE.md` §8 both stated flatly "no blog exists," based on the earlier pages-only
query never surfacing a blog. A blog *object* does exist (title "News," handle `news`) — this pass
did not check whether it has any published articles or whether it's linked from anywhere live (out of
this verification's scope, which is to re-check the 5 architecture documents' own claims, not conduct
a new audit). The corrected fact for `WEBSITE_ARCHITECTURE.md` §8 and `CONTENT_PLAN.md`'s Blogs
section: **a "News" blog exists but appears unused and unlinked** — the underlying business question
("do we want a blog") is unchanged, but the premise "nothing exists yet" is not quite accurate and
should be corrected before this is carried further.

## D. Internal linking — from INTERNAL_LINKING.md

| # | Recommendation | Current live state | Evidence | Action required | Risk | Priority | Status |
|---|---|---|---|---|---|---|---|
| D1 | `/pages/cake-delivery-in-meerut` already links to both `/pages/midnight-cake-delivery` and the 30-minute page | Confirmed still true | Page body fetched this session (unchanged since, no edits made to this page) contains both `<a href="/pages/midnight-cake-delivery">` and `<a href="/pages/30-minute-cake-delivery-in-meerut-premium-reliable-service">` | None — already correct | None | — | **Already implemented** (i.e., the "existing links" half of the recommendation was already true, not a gap) |
| D2 | `/pages/cake-delivery-in-meerut` is missing a link to the FAQ page | Confirmed still missing — no `frequently-asked-questions-faqs` reference in its body | Same page body, re-inspected this pass | Add the link | None | Medium | **Verified** |
| D3 | `/pages/cake-delivery-in-meerut` already links to the eggless page from its "Why Choose" section | Confirmed still true | Body contains `<a href="/pages/100-percent-eggless-bakery">100% eggless</a>` under "Why Choose The Baking Kaur?" | None — already correct | None | — | **Already implemented** — the original `INTERNAL_LINKING.md` wording under "Eggless page" implied this link exists one-directionally (delivery → eggless) but recommended the *reverse* direction (eggless → FAQ) as the gap; both are independently confirmed, no contradiction, just clarifying which direction is which |
| D4 | Gift Hampers page's "Related Collections" are plain text, not hyperlinks | Confirmed still true — `<ul><li>Birthday Cakes</li><li>Anniversary Cakes</li>...</ul>`, no `<a>` tags anywhere in that block | Page body fetched this session (unchanged) | Convert to real links per `INTERNAL_LINKING.md` | None | Medium | **Verified** |
| D5 | The three hamper sibling pages (customised/festive/surprise-hampers-meerut) should link to the hub and each other — **originally marked "not verified" in `INTERNAL_LINKING.md`** | **Now verified directly**: none of the three link to `/pages/gift-hampers` (the recommended hub) or to each other. Each links only to `/collections/cake-hampers` (all three), plus `festive` also links to `/collections/luxury-diwali-hampers` and `surprise` also links to `/collections/flowers-cake-combos` | Fresh page-body fetch this pass, all three handles (`customised-hampers-meerut`, `festive-hampers-meerut`, `surprise-hampers-meerut`) | Add cross-links per `INTERNAL_LINKING.md`'s Hampers cluster recommendation | None | Medium | **Verified** (previously unconfirmed, now confirmed accurate) |
| D6 | FAQ page links to `/pages/refund-return-policy` twice | Confirmed — `templates/page.faq-01.json` (live, this session's own SEO-013 work) contains exactly 2 occurrences, in `faq_item_cancel` and `faq_item_refund` | Direct file read this pass | None — already correct, and the target page is confirmed still live (see C2) | None | — | **Already implemented** |

## E. URL architecture — from URL_STRUCTURE.md

| # | Recommendation/claim | Current live state | Evidence | Action required | Risk | Priority | Status |
|---|---|---|---|---|---|---|---|
| E1 | Product handles are a mixed pattern — some human-readable, some opaque codes | Confirmed, and the mix is wider than originally described: readable (`motu-patlu-designer-birthday-cake-meerut`), letter+number code (`b110`), and **pure numeric handles** (`5`, `28`, `29`, `38`, `39`) not previously called out specifically | Fresh `products` query this pass, both a title-filtered search and an unfiltered sample | No action — deferred per `CLAUDE.md`'s handle-optimization policy | Same as always — live URL change risk to QR codes | Deliberately deferred | **Verified** (and slightly broadened: pure-numeric handles are an even more opaque case than the `b158`/`hamperNN` pattern `CLAUDE.md` names) |
| E2 | New-URL patterns (`/pages/{topic}-in-meerut`, `/collections/{festival}-hampers`, etc.) match the site's existing successful pattern | Unchanged — the cited examples (`cake-delivery-in-meerut`, `luxury-diwali-hampers`) are still live with those exact handles | Re-confirmed via this pass's fresh collections/pages queries | None — pattern recommendation stands as-is | None | — | **Verified** |
| E3 | Collection URL sprawl (7 near-duplicate handles) needs a business decision before any canonicalization | Unchanged, see B4 | Same evidence as B4 | Same as B4 | Same as B4 | High | **Needs business approval** |

## Summary

- **28 discrete recommendations/claims checked.** 0 found Obsolete. 1 corrected (C6, the blog
  object exists after all, just unused). 3 confirmed **Already implemented** (D1, D3, D6 — links the
  source documents correctly identified as already present, not gaps). 1 previously-unverified claim
  resolved with real evidence for the first time (D5). The remainder split between **Verified**
  (the diagnosis is accurate, no live-state change) and **Needs business approval** (accurate, and the
  source documents already correctly marked them as such).
- **Nothing in the underlying Shopify configuration changed** between when the 5 architecture
  documents were written and this verification pass — every discrepancy found (C6, the D1/D3/D6
  "already implemented" framing, and A3's two-part footer defect) is a precision correction to how the
  original documents described reality, not evidence that reality itself moved.
- **Highest-priority unresolved items, unchanged from `WEBSITE_ARCHITECTURE.md`**: the header
  navigation gap (A1), the footer's Refund/Terms link targets (A2/A3), and the collection-level
  duplicate-content cluster (B4/E3) — all still gated on the same business decisions named in
  `POLICY_ARCHITECTURE.md` and this document's own recommendations.

## Related

[WEBSITE_ARCHITECTURE.md](WEBSITE_ARCHITECTURE.md), [SITE_TREE.md](SITE_TREE.md),
[NAVIGATION.md](NAVIGATION.md), [URL_STRUCTURE.md](URL_STRUCTURE.md),
[INTERNAL_LINKING.md](INTERNAL_LINKING.md), [POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md),
[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md).
