# Business Decision Guide — Sprint 1 Blockers

Generated 2026-07-30. Expands `SPRINT1_BLOCKERS.md`'s six approved blockers into full decision
sheets for sign-off. **No code is changed, no Shopify data is modified, nothing is implemented by
this document.** Every "Recommended option" and "Alternative options" entry traces to a
recommendation already documented in `POLICY_ARCHITECTURE.md`, `POLICY_CONSOLIDATION.md`,
`ADDRESS_AUDIT.md`, `DELIVERY_AREA_SPEC.md`, or `WEBSITE_ARCHITECTURE.md` — nothing new is invented
here. This document waits for your approval before any implementation begins.

---

## B1 — Refund / Cancellation / Shipping policy contradiction (SEO-031)

**1. Current implementation**
- Custom Page "Refund & Return Policy" (live, `/pages/refund-return-policy`): 12-hour cancellation
  window for a full refund/credit, 4-hour issue-report window for damaged/wrong/quality problems,
  5-7 business day refund timeline.
- Shop Policy: Refund policy (live, built-in): *"No Refunds or Replacements: All orders are final...
  Quality Issues: Report within 2 hours... no refunds or replacements will be given."* Names the
  business "The Bakery Kaur."
- Shop Policy: Terms of Service (live, built-in): *"Once you place an order, it is considered final.
  We do not accept cancellations or changes... We do not offer refunds or replacements."* Also
  "The Bakery Kaur."
- Shop Policy: Shipping (live, built-in): "2-5 hours" delivery window, "1 hour" issue-report window —
  neither figure sourced anywhere else on the site. Also "The Bakery Kaur."
- Unpublished draft custom Page "Return, Refund & Replacement Policy": a third variant (2-hour issue
  window, cancel-before-production-starts).
- No Shopify Cancellation Policy type (`SUBSCRIPTION_POLICY`) is set for this shop at all.

**2. Evidence collected**
Live `shop.shopPolicies` GraphQL query (types `REFUND_POLICY`, `TERMS_OF_SERVICE`,
`SHIPPING_POLICY`) and live Page queries on both Refund custom pages, run this project and
cross-referenced in `POLICY_CONSOLIDATION.md` and `POLICY_ARCHITECTURE.md` §1.

**3. Recommended option**
Make the custom "Refund & Return Policy" page canonical (per `POLICY_ARCHITECTURE.md` §3). Rewrite
the three built-in Shop Policies to match it exactly. Fold Cancellation into the same page under its
existing "Cancellations & Changes" heading — no separate Cancellation Policy needed. Fix "The Bakery
Kaur" → "The Baking Kaur" in all three Shop Policies while editing.

**4. Alternative options**
- **Alt A**: Make the stricter Shop Policy ("all orders final, no refunds ever") canonical instead,
  and rewrite the custom page down to match.
- **Alt B**: Draft an entirely new, different policy not currently live anywhere.
- **Alt C**: Leave both live, unresolved (status quo).

**5. Pros** (of recommended option)
Uses already-published, specific, currently-live customer-facing terms — no new legal drafting
needed beyond copying into the Shop Policies. More generous terms typically support conversion and
trust. Fixes the business-name error in the same pass. Folds Cancellation in without creating a new
policy type.

**6. Cons**
More generous terms mean higher actual refund/cancellation exposure than the "no refunds ever"
stance. Requires a manual Shopify Admin edit outside the theme-deploy path — someone has to actually
make this change, it isn't a code deploy. The custom page's specific numbers (12hr/4hr/5-7 day) have
never been independently confirmed as the business's real intended policy either; this recommendation
favors them because they're specific and reasonable, not because they're independently verified.

**7. SEO impact**
Indirect but real: removes a live trust-signal conflict that damages E-E-A-T; this is the highest-
priority trust fix identified in the entire audit. No direct keyword/ranking impact expected.

**8. UX impact**
Customers get one consistent answer regardless of where they look (footer, checkout, FAQ) instead of
contradictory claims. If the friendlier terms are adopted, the customer experience genuinely improves
(a clear, generous, predictable policy).

**9. Operational impact**
If the friendlier terms become the enforced real policy, support/fulfillment needs to actually honor
12-hour cancellations, 4-hour issue windows, and 5-7 day refunds consistently — this is a real
process commitment, not just a text change. If the stricter alternative were chosen instead, no new
operational burden, but a worse customer-facing promise.

**10. Risk**
**High if left unresolved** — live legal contradiction on real customer rights, real dispute/support
exposure. **Low technical risk to fix** once wording is decided (text-only Shopify Admin edit).

**11. Reversibility**
Fully reversible — policy text can be edited again at any time in Shopify Admin; no destructive or
irreversible action involved.

**12. Final recommendation**
Approve the custom page's existing terms (12hr/4hr/5-7 day) as canonical, fold Cancellation into it,
and direct that the three Shop Policies be rewritten to match plus corrected to "The Baking Kaur" —
pending your explicit sign-off before any Shop Policy is actually edited.

---

## B2 — Empty "Terms and Conditions" page (SEO-034)

**1. Current implementation**
`/pages/terms-and-conditions` (custom Page, `gid://shopify/Page/110844510377`) is live, published,
and has a completely empty body (`""`).

**2. Evidence collected**
Fresh live Page query, confirmed empty and published on multiple separate occasions this project
(most recently during `ARCHITECTURE_VERIFICATION.md`'s pass).

**3. Recommended option**
Populate with a short pointer paragraph plus a link to the canonical Shop Policy Terms of Service URL
— once B1 is approved and that Shop Policy carries the correct wording. Do not duplicate full Terms
text on this custom page (that would recreate the same two-system duplication problem B1 addresses).

**4. Alternative options**
- **Alt A**: Write the full Terms wording directly on this custom page instead of pointing to the
  Shop Policy.
- **Alt B**: Unpublish this page until real content exists.
- **Alt C**: Leave as-is (status quo — empty and live).

**5. Pros** (of recommended option)
Avoids creating a second duplicate wording surface for Terms; minimal content to write and maintain;
keeps the Shop Policy as the single source of truth.

**6. Cons**
A visitor landing on a page titled "Terms and Conditions" and finding only a short pointer may
perceive it as less complete than expected. Fully depends on B1 landing first — can't be finished in
isolation.

**7. SEO impact**
Low direct traffic impact (Terms pages rarely drive search traffic), but meaningful E-E-A-T impact —
an empty, indexed legal page is a real negative trust signal; fixing it removes a thin/empty-content
flag.

**8. UX impact**
Currently a dead-end page for anyone checking terms before ordering. Any of the three real options
(pointer, full text, or unpublish) fixes the current broken experience; the pointer option gets a
visitor to the real terms fastest.

**9. Operational impact**
Minimal — a one-time content edit once B1 is settled, no ongoing maintenance burden either way.

**10. Risk**
**Medium if left unresolved** — a published, empty legal page is a real (if not severe) completeness
gap. **Low risk to fix** in any of the three real options.

**11. Reversibility**
Fully reversible — page content and publish status can both be changed again at any time.

**12. Final recommendation**
Approve the pointer-plus-link approach, to be executed immediately after B1's Shop Policy rewrite
lands. If B1 is delayed significantly, unpublish this page in the interim rather than leave it
empty-and-live — pending your sign-off on either path.

---

## B3 — Address, coordinates, and NAP consistency (SEO-015 / SEO-029 / SEO-036)

**1. Current implementation**
Four distinct address wordings are live simultaneously: `bk-local-business.liquid`'s schema
("Fatah Complex, Thapar Nagar Lane 7" — note the typo) and the footer files (same typo); the Contact
page's prose ("Fateh Complex, Thapar Nagar — Lane No. 7," correct spelling); the Refund & Return
Policy page ("390/1, Lane Number 7, Thapar Nagar," a different structure entirely); and the Shopify
Admin's own billing address ("Thapar Nagar Gali Number 7 Lajpat Bazaar Thapar Nagar" +
"Fateh Complex, 390/1, Lane Number 7, opposite Ice Factory") — which matches none of the other three
exactly. Two geo-coordinate pairs are live ~600 m apart: `bk-local-business.liquid`'s
(28.9931, 77.6939) vs. the Shopify Admin billing address's (28.9897017, 77.7044604).
`tbk-schema-website.liquid`'s Organization entity has no street address or geo data at all.

**2. Evidence collected**
Full detail and source-by-source comparison in `ADDRESS_AUDIT.md` §1-2, built from a live theme grep
plus live Admin GraphQL queries (`shop.billingAddress`) run this project.

**3. Recommended option**
Use the Shopify Admin billing address as the base text (the merchant's own account record, the most
authoritative source available), spot-check its spelling/detail against the real signage or lease
before finalizing, commission a fresh Google Maps pin-drop rather than trusting either existing
coordinate pair, then propagate the confirmed address and coordinates identically across all
affected surfaces in one coordinated pass.

**4. Alternative options**
- **Alt A**: Pick one of the four on-site wordings as-is (e.g. the Contact page's, since it already
  has the correct "Fateh" spelling).
- **Alt B**: Commission an entirely new address description from scratch, independent of any
  existing source, confirmed directly against the physical location.
- **Alt C**: Leave as-is (status quo — 4 wordings, 2 coordinate pairs).

**5. Pros** (of recommended option)
Uses the account-of-record data, which is harder to argue isn't "official." Requires no new address
to be drafted from nothing. A single coordinated pass fixes both the text and (once a fresh pin is
taken) the geo-coordinate problem together, rather than as two separate efforts.

**6. Cons**
The Admin billing address's own text doesn't exactly match any on-site wording either, so it isn't
fully risk-free without a human sanity check on the "Fatah" vs. "Fateh" spelling and the exact
building/lane detail. A fresh geo pin-drop is a real-world action (someone standing at or confirming
the actual location on Google Maps), not a data lookup — it has its own small lead time.

**7. SEO impact**
**High.** NAP (Name/Address/Phone) consistency is a core Local Pack ranking factor; a ~600 m
coordinate error is enough to misplace the business pin for "near me" searches. This is one of the
highest-leverage Local SEO fixes identified in the whole audit.

**8. UX impact**
A correct, single address and map pin means customers and delivery partners aren't misdirected.
Today, a customer clicking between pages could see three or four different spellings of the same
address, which reads as careless even where the underlying facts are close.

**9. Operational impact**
A wrong map pin is a genuine, non-cosmetic operational risk beyond SEO — it can misdirect real
delivery attempts. Fixing this has real logistics value, not just a marketing benefit.

**10. Risk**
**Medium if left unresolved** — misplaces the business in local search and risks real-world delivery
confusion. **Low technical risk to fix** once the correct values are confirmed (largely a
find-and-replace across ~7 known files/surfaces).

**11. Reversibility**
Fully reversible — both the text and the schema/geo values can be corrected again later at no cost;
even a wrong Maps pin-drop can be corrected afterward.

**12. Final recommendation**
Approve using the Shopify Admin billing address as the base text (pending a quick spelling/detail
sanity check against the real signage) and commissioning a fresh Google Maps pin-drop; propagate both
together across `bk-local-business.liquid`, `tbk-schema-website.liquid`, the three footer files,
`page.contact-2.json`, the Refund & Return Policy page, and the Shop Policy Contact Information body
— pending your sign-off before any of those are edited.

---

## B4 — Delivery-area list conflict (SEO-035)

**1. Current implementation**
The live "Cake Delivery in Meerut" page lists: Thapar Nagar, Shastri Nagar, Ganga Nagar, Partapur,
Jagriti Vihar. The live footer's `service_areas` setting lists: Thapar Nagar, Shastri Nagar, Sadar
Bazaar, Civil Lines, Pallavpuram, Ganga Nagar. Only 2 of the 5 distinctly-named localities (Thapar
Nagar, Shastri Nagar, and arguably Ganga Nagar) appear on both lists.

**2. Evidence collected**
Live page-body fetch and live theme grep of `sections/site-footer.liquid`, documented in
`DELIVERY_AREA_SPEC.md` §2, re-confirmed during `ARCHITECTURE_VERIFICATION.md`'s pass.

**3. Recommended option**
Confirm the true, complete list of serviceable localities against actual delivery-fee/logistics data
— i.e., whichever zones the existing distance-based delivery-fee system genuinely reaches — rather
than picking either existing list on faith.

**4. Alternative options**
- **Alt A**: Adopt the footer's list as authoritative.
- **Alt B**: Adopt the delivery page's list as authoritative.
- **Alt C**: Merge both lists into one superset.

**5. Pros** (of recommended option)
The only option that doesn't risk enshrining an error from either existing source. Ties directly to
real, checkable delivery-fee logic already documented (₹350 minimum order, distance-based fees, ~15
km radius, per `CLAUDE.md`).

**6. Cons**
Requires actual business time to confirm against logistics reality rather than a five-minute pick.
A fresh confirmation could still surface internal disagreement about which areas are genuinely served.

**7. SEO impact**
**High.** This determines what neighborhood-level content and schema (`areaServed`) can be built
truthfully. Under-claiming reach loses search visibility for genuinely served areas; over-claiming
risks a false-advertising-adjacent problem if a listed area isn't actually reachable.

**8. UX impact**
A customer checking "do you deliver to my area" currently gets a different answer depending which
page they land on — this directly affects purchase-decision confidence at exactly the moment a
customer is deciding whether to proceed.

**9. Operational impact**
This is fundamentally an operational-reality question before it's a marketing-copy one — the real
list must match what delivery/logistics can actually fulfill, not the other way around.

**10. Risk**
**Medium** — an active, live local-SEO inconsistency, and a real customer-service risk (promising
delivery somewhere it doesn't reach, or omitting somewhere it does).

**11. Reversibility**
Fully reversible — a text-only change once the real list is confirmed.

**12. Final recommendation**
Confirm the real serviceable-area list against actual logistics/fee-zone data first; do not merge the
two existing lists as a shortcut, since that risks overstating coverage into areas neither source
actually confirmed — pending your sign-off on the confirmed list once gathered.

---

## B5 — Duplicate collection cluster + non-curating utility collections

**1. Current implementation**
Seven collections — `cakes`, `cake-delivery-meerut`, `same-day-cake-delivery-meerut`,
`midnight-cake-delivery-meerut`, `midnight-cake-delivery`, `custom-cakes-meerut` (617 products, the
one outlier), `kids-birthday-cakes-meerut` (128) — otherwise all show ~986 products, essentially the
same set under different URLs. Separately, "Best Selling Products" and "Newest Products" both show
the full, unfiltered 1,235-product catalogue — identical to `/collections/all` — meaning neither
applies any real curation or sort logic.

**2. Evidence collected**
Live `collections()` GraphQL query, re-confirmed on three separate occasions this project with
identical counts each time (`WEBSITE_ARCHITECTURE.md` §6, `ARCHITECTURE_VERIFICATION.md` B3/B4).

**3. Recommended option**
Keep at most 1-2 of the 7 "Meerut" collections if a genuinely distinct merchandising purpose is
identified for them; unpublish the rest. Wire native Shopify smart-collection sort rules (by
units/orders sold, and by creation date respectively) into "Best Selling Products" and
"Newest Products" rather than leaving them as unfiltered clones of the full catalogue.

**4. Alternative options**
- **Alt A**: Unpublish all 7 near-duplicate collections outright, keeping only the 5 core
  merchandising collections (Birthday, Anniversary, Wedding, Designer & Theme, Cake Hampers).
- **Alt B**: Keep all 7 as-is (status quo).
- **Alt C**: Differentiate each of the 7 with genuinely distinct content or filtering so they stop
  being duplicates in substance, not just in name.

**5. Pros** (of recommended option)
Balances cleanup against any accumulated SEO equity those 7 URLs may already carry if indexed.
Restores real meaning to "Best Selling"/"Newest" using a native, already-available Shopify feature —
no new build required.

**6. Cons**
Deciding which 1-2 (if any) of the 7 to keep requires genuine merchandising judgment about which
might independently drive traffic — not a one-line fix, a real (if quick) review.

**7. SEO impact**
**High.** Stops 7 near-duplicate collection URLs from competing against each other and diluting
ranking signal for the same search queries. A "Best Selling" collection that actually curates
products is also a real trust/CRO asset in its own right.

**8. UX impact**
Reduces real navigational confusion — a customer today can browse "Cake Delivery in Meerut,"
"Custom Cakes Meerut," and "Cakes" and see nearly the same ~986 products under three-plus different
names. Fixing "Best Selling"/"Newest" also restores a genuinely useful discovery/browsing aid.

**9. Operational impact**
Low — a merchandising and Admin-configuration decision with no fulfillment or logistics implications.
The sort-rule wiring is a one-time setup; Shopify maintains it automatically afterward.

**10. Risk**
**Medium if left unresolved** — an active duplicate-content SEO risk today. **Low risk to execute**
once decided (Admin publish/unpublish and sort-rule actions only, no theme code).

**11. Reversibility**
Fully reversible — unpublishing a collection is not deletion; any of the 7 can be republished later
if a genuine use is identified.

**12. Final recommendation**
Conduct a short merchandising review of the 7 "Meerut" collections to flag any with genuinely
independent value; unpublish the remainder. Wire native sort logic into Best Selling and Newest
immediately regardless of the other decision, since that specific fix carries no real downside —
pending your sign-off on which (if any) of the 7 to retain.

---

## B6 — Store Locator page's permanent fate (SEO-030)

**1. Current implementation**
`/pages/store-locator` remains unpublished (mitigated via a prior, user-approved interim decision),
its template still containing fake London/Madrid/Tokyo demo store-locator content. Not live, not
publicly reachable.

**2. Evidence collected**
Live Page query confirming `isPublished: false`, checked and reconfirmed at three separate points
across this project; original finding and interim mitigation documented in `AUDIT_LEDGER.md` (SEO-030).

**3. Recommended option**
Repurpose the page/template into the real Delivery Areas hub, using the content specification already
written and ready in `DELIVERY_AREA_SPEC.md` — sequenced immediately after B4 (the delivery-area-list
conflict) is resolved, since the hub's real content depends on knowing the confirmed service-area list.

**4. Alternative options**
- **Alt A**: Delete the page and template outright.
- **Alt B**: Leave it unpublished indefinitely (permanent status quo).

**5. Pros** (of recommended option)
Reuses an existing template/URL slot rather than building an entirely new page from scratch. A full,
evidence-based content specification already exists and is ready to use. Unlocks a genuine,
already-scoped local-SEO opportunity at low incremental cost once B4 lands.

**6. Cons**
Fully blocked until B4 resolves — cannot be completed independently right now. The existing
fake-store-locator template will likely need real Liquid/theme adjustments to fit real delivery
content instead of its current layout — a real (if bounded) implementation-phase task, not a decision-
phase concern, but worth noting the effort isn't zero.

**7. SEO impact**
**Medium.** Unlocks a real Delivery Areas landing page targeting genuine local-intent search queries.
The status-quo (unpublished) option has zero SEO impact either way, since the page isn't indexed.

**8. UX impact**
None currently, since the page isn't live. Repurposing gives customers one clear, dedicated place to
check delivery coverage instead of piecing it together across three separate delivery-mode pages.

**9. Operational impact**
None — this is a content/marketing page with no fulfillment implications of its own.

**10. Risk**
**Low** under every option — the page is already mitigated (unpublished), so there is no live
exposure regardless of which path is chosen. The only real "risk" is opportunity cost from delaying
a genuine, already-specified local-SEO asset.

**11. Reversibility**
Fully reversible under repurposing or leaving unpublished — either can be changed again later.
Deleting the template is the one option with a real (if small) reversibility cost, since recreating a
Delivery Areas page from scratch afterward would mean building a new template rather than adapting
an existing one.

**12. Final recommendation**
Approve repurposing into the Delivery Areas hub, explicitly sequenced to begin only after B4 is
resolved; do not delete the template, since it is the ready-made target for the content
specification already written — pending your sign-off.

---

## What this document does not do

No Shop Policy, page body, collection, or theme file is modified by this document. No blocker is
resolved. Every "Recommended option" is drawn from an existing report's own recommendation
(`POLICY_ARCHITECTURE.md`, `ADDRESS_AUDIT.md`, `DELIVERY_AREA_SPEC.md`, `WEBSITE_ARCHITECTURE.md`) —
nothing new is proposed here that wasn't already documented before this pass.

## Related

[SPRINT1_BLOCKERS.md](SPRINT1_BLOCKERS.md), [IMPLEMENTATION_BACKLOG.md](IMPLEMENTATION_BACKLOG.md),
[POLICY_ARCHITECTURE.md](POLICY_ARCHITECTURE.md), [POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md),
[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md), [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md),
[BUSINESS_DECISION_IMPLEMENTATION.md](BUSINESS_DECISION_IMPLEMENTATION.md),
[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md).

---

**Waiting for your approval on the six final recommendations above before any implementation begins.**
