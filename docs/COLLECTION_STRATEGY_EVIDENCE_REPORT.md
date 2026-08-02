# Collection Strategy — Evidence Report (Phase 7.8, investigation only)

**No production changes were made to produce this report.** No collection was merged, redirected,
renamed, deleted, or had its handle changed; no page was modified; no navigation was edited. Every
number below was pulled live via read-only Admin GraphQL queries (`shopify store execute`, no
`--allow-mutations` used) on 2026-08-01. This is a documented implementation plan with evidence and
a recommended execution order — it ends with a request for approval, not an action.

## Executive summary

`tasks/README.md` names a single "collection audit" awaiting action. **It doesn't exist as a
single thing.** Four independent audits, two weeks apart, each proposed different — sometimes
contradictory — dispositions for the same collections, and none of the four has ever been executed:

| # | Date | Document | Framing |
|---|---|---|---|
| 1 | 2026-07-16 | `CATALOG_ARCHITECTURE.md` | 8 collections at **0 products** ("empty, doorway-page risk") — per-collection merge/redirect/convert table |
| 2 | 2026-07-18/20 | `SEO_AUDIT_LEDGER.md` (P0-04, Phase 20) | Same 8, reframed as thin/doorway pages; applied a blanket `noindex` instead of the table above; separately logs an **undocumented parallel session** that converted all 8 from manual to smart collections |
| 3 | 2026-07-24 | `docs/blog-os/` (`CURRENT_STATE.md`, `BLOG_OS_ROADMAP.md`) | Discovers the parallel session's smart-collection rules made 5 of the 8 show **985 identical products each** — no longer empty, now a duplicate-content cluster; proposes a third, different fix (four 301s to `/collections/cakes`) |
| 4 | 2026-07-30 | `seo-audit/final/` (`WEBSITE_ARCHITECTURE.md`, `ARCHITECTURE_VERIFICATION.md`, `IMPLEMENTATION_BACKLOG.md`) | Re-confirms the cluster (now 7 collections, ~986 products each) still live, unresolved; frames it as a fresh, still-open `<<BUSINESS APPROVAL REQUIRED>>` item — doesn't reference audits 1–3 |

**Root cause of the mess, not just the collections**: an unlogged parallel/mobile session (referenced
only in `SEO_AUDIT_LEDGER.md:1409-1413`, "a handoff PDF bundle revealed a second session had been
working this store from mobile") converted 8 manual collections to smart collections with poorly
designed, overlapping rules — five of them literally identical (`TYPE contains "Cake"`) — with zero
documentation of what was changed or why. Every audit after that point has been re-discovering the
same symptom from scratch because the actual root event was never written down anywhere query-able.
**This report's own live re-query (§1–2) confirms audit #4's numbers are current** — the cluster is
real, live, and unchanged since 2026-07-30.

This report also surfaces two things no prior audit found: one collection (`gourmet-cookies-meerut`)
that has **never been given a disposition by any of the four audits**, and confirms the exact current
navigation reality (only 6 of 36 collections are in any live menu).

---

## 1. Current collection inventory (live, re-queried 2026-08-01)

36 collections, single page (`hasNextPage: false` at `first: 100`), so this is exhaustive.

| Collection | Handle | Products | Rule basis | SEO fields set? |
|---|---|---|---|---|
| Birthday Cakes | `birthday-cakes` | 279 | Manual | Yes |
| Cake Hampers | `cake-hampers` | 119 | Manual | Yes |
| All | `all` | 1,235 | Auto (vendor != personalizer) | No |
| Anniversary Cakes | `anniversary-cakes` | 102 | Manual | Yes |
| Wedding Cakes | `wedding-cakes` | 134 | Auto — `TITLE contains "wed"` | Yes |
| For Him | `for-him` | 11 | Manual | Yes |
| For Her | `for-her` | **1** | Manual | Yes |
| Designer & Theme Cakes | `designer-theme-cakes` | 165 | Manual | Yes |
| Surprise Cake Setup with Revolving Cake | `showstopper-wedding-cake` | 78 | Auto — `TYPE = Wedding Cake` | Yes |
| Luxury Diwali Hampers | `luxury-diwali-hampers` | 44 | Manual | Yes |
| Best Selling Products | `best-selling-products` | 1,235 | Auto — self-cancelling rule (see §4) | No |
| Newest Products | `newest-products` | 1,235 | Auto — self-cancelling rule (see §4) | No |
| Baby Girl | `baby-girl` | 28 | Manual | Yes |
| Butterfly | `butterfly` | 23 | Manual | Yes |
| Criciket *(sic)* | `criciket` | 10 | Manual | Yes |
| Motu Patlu | `motu-patlu` | 12 | Manual | Yes |
| Unicorn | `unicorn` | 16 | Manual | Yes |
| Jungle Animal Theme | `jungle-animal-theme` | 17 | Manual | Yes |
| Chartered Accountant | `chartered-accountant` | 10 | Manual | Yes |
| roblox | `roblox` | 8 | Manual | Yes |
| PAW PETROL *(sic)* | `paw-petrol` | 4 | Manual | Yes |
| Teddy | `teddy` | 7 | Manual | Yes |
| Bow Cake | `ribbon-cake` | 8 | Manual | Yes |
| KPOP Cake | `kpop-cake` | 9 | Manual | Yes |
| boy or girl cake | `boy-or-girl-cake` | 12 | Manual | Yes |
| Winter Strawberry Collection | `winter-strawberry-collection` | 23 | Manual | Yes |
| Photo Cakes | `photo-cakes` | 4 | Auto — `TITLE contains "Photo"` | Yes |
| Flowers & Cake Combos | `flowers-cake-combos` | **1** | Manual | Yes |
| Midnight Cake Delivery | `midnight-cake-delivery` | 986 | Auto — `TYPE contains "Cake"` | Yes |
| Cake Delivery in Meerut | `cake-delivery-meerut` | 986 | Auto — `TYPE contains "Cake"` | Yes |
| Same Day Cake Delivery Meerut | `same-day-cake-delivery-meerut` | 986 | Auto — `TYPE contains "Cake"` | Yes |
| Midnight Cake Delivery Meerut | `midnight-cake-delivery-meerut` | 986 | Auto — `TYPE contains "Cake"` | Yes |
| Custom Cakes Meerut | `custom-cakes-meerut` | 617 | Auto — `TYPE = Designer Cake OR Theme Cake` | Yes |
| Kids Birthday Cakes Meerut | `kids-birthday-cakes-meerut` | 128 | Auto — 13-way title OR | Yes |
| Cakes | `cakes` | 986 | Auto — `TYPE contains "Cake"` | Yes |
| gourmet-cookies-meerut | `gourmet-cookies-meerut` | 4 | Manual | **No — title is the raw handle** |

Confirms audit #4's exact live counts for the "Meerut cluster" — unchanged since 2026-07-30.

## 2. Existing collection hierarchy / navigation

Shopify collections don't nest natively; "hierarchy" here means what's actually linked.

**Live menus** (re-queried 2026-08-01 via the Admin `menus` API — 9 menus total):

- **`main-menu`** — the menu actually wired to the live header (`sections/header-group.json`'s
  `main_menu` setting = `"main-menu"`, confirmed by reading the file directly). HOME, ABOUT US,
  CONTACT US, and a "Categories" dropdown linking **6 of 36 collections**: Birthday Cake,
  Anniversary Cake, Diwali Hampers, Theme Cakes, Hampers, Wedding Cakes. Confirms
  `seo-audit/final/NAVIGATION.md`'s "IMPLEMENTED 2026-07-30" claim — verified live, not stale.
- **`header`** — the *same* 6 collections, but this menu resource is not referenced by the live
  `main_menu` setting; only used by a mega-menu block that is `"disabled": true` in
  `sections/header-group.json`. Confirmed orphaned.
- **`footer`** — 6 items, all policy/search links, zero collections. The footer's actual visible
  content is hardcoded in `sections/site-footer.liquid`, unrelated to this menu resource.
- **`meerut-delivery`** — 3 page links (not collections): `cake-delivery-in-meerut`,
  `midnight-cake-delivery`, and a 30-minute-express page. Both of the first two were checked live
  this pass (§7) and have real, substantial body content (2,792 and 1,730 characters) — they are
  viable redirect targets today, not aspirational ones.
- **`explore-cakes`**, **`quick-links`** — 0 items, empty shells.

**Net: 30 of 36 collections are in no live menu at all.** `docs/INTERNAL_LINKING_AUDIT.md` (Phase
7.1) flagged this exact question as unverified and deferred it (task M-1); this report's
navigation-menu check closes the "menu" half of that gap. The "any other page" half (stray links
inside product/page/collection body copy) remains unverified — one incidental example found: the
`Cakes` collection's own description links to 4 collections (Birthday, Anniversary, Wedding,
Designer & Theme).

## 3. The four audits, what each proposed, and why

### Audit #1 — `CATALOG_ARCHITECTURE.md` (2026-07-16), "the" Enterprise Collection Audit

Still the document `VERSION.md`, `PROJECT_ROADMAP.md`, `00_START_HERE.md`, and
`INFORMATION_ARCHITECTURE.md` all point to by name — despite `MD_FILE_INVENTORY.md` (2026-07-24,
a later meta-audit of the docs themselves) calling this whole document batch "dead weight... specs
for a store that already exists." Written when the 8 target collections showed **0 products**.

Proposed, per collection (`CATALOG_ARCHITECTURE.md:102-167`):
- **Merge** `boy-or-girl-cake` → a proposed "Baby & Gender-Reveal" collection (reason: overlaps `baby-girl`).
- **Merge** `for-her` → into occasion collections (reason: 1-product thin audience).
- **Merge or populate** `flowers-cake-combos` (reason: 1-product thin).
- **Redirect** `midnight-cake-delivery-meerut` → `midnight-cake-delivery` (reason: duplicate).
- **Redirect** `cake-delivery-meerut` → `/pages/cake-delivery-in-meerut` (reason: duplicates a delivery-hub page).
- **Redirect** `custom-cakes-meerut` → `designer-theme-cakes` (reason: duplicates designer/theme).
- **Remove, 301** `showstopper-wedding-cake` → `wedding-cakes` (reason: "niche service, no SEO" — written when this collection had 0 products).
- **Convert to landing page** `same-day-cake-delivery-meerut` and `midnight-cake-delivery` (reason: delivery is a service intent, not a product filter).
- **Convert manual → smart** `kids-birthday-cakes-meerut`, `photo-cakes`, and 9 theme sub-collections.

Also ratifies a standing rule: a node becomes a real collection only at **≥8–12 products**; thinner
nodes should be filters, nav-only, or roadmap items, never a thin collection (`§9`, line 172). And
a permanent rule that "100% Eggless" must never become a collection — it's a brand attribute
covering the whole catalogue, not a category (`§10`).

Self-status: "v0.3 — Awaiting approval before implementation." Never approved. Never implemented.

### Audit #2 — `SEO_AUDIT_LEDGER.md` P0-04 (2026-07-18) + Phase 20 (2026-07-20)

Independently re-found the same 8 collections, reframed as a doorway-page / Google-spam-policy
risk, and specifically flagged `midnight-cake-delivery` + `midnight-cake-delivery-meerut` as
cannibalizing the same search query. Investigated redirecting to pages but **rejected it** at the
time because the specific target pages checked then (`/pages/photo-cakes`,
`/pages/midnight-surprise-delivery` — different handles than the `meerut-delivery` menu's current
pages) had empty bodies. Applied a different, narrower fix instead: any 0-product collection gets
`noindex,follow`.

Phase 20 (`SEO_AUDIT_LEDGER.md:1409-1413`) is where the undocumented parallel-session conversion is
recorded: "8 empty collections converted manual→smart" with no detail on what rules were written —
this is the direct cause of audit #3's discovery.

### Audit #3 — `docs/blog-os/CURRENT_STATE.md` + `BLOG_OS_ROADMAP.md` (2026-07-24)

Discovers the aftermath: 5 collections (`cakes`, `cake-delivery-meerut`, `midnight-cake-delivery`,
`midnight-cake-delivery-meerut`, `same-day-cake-delivery-meerut`) now all carry the **identical**
smart rule `TYPE contains "Cake"` → 985 products each (984 at the time; 986 in this report's live
check — one more active cake product exists now). `custom-cakes-meerut` and
`kids-birthday-cakes-meerut` got their own distinct rules. Also finds `best-selling-products` and
`newest-products` carry **self-cancelling rules** (`TITLE contains "Best Selling" AND TITLE
not-contains "Best Selling"`) that mathematically match everything — both "collections" show all
1,235 products, including 588 drafts, and mean nothing close to their names. And finds
`showstopper-wedding-cake` now has 77 products (78 in this report's check) under the title
"Surprise Cake Setup with Revolving Cake" — handle says wedding, title says surprise setup, rule
selects `TYPE = Wedding Cake`, SEO copy is about surprise setups: **four different subjects on one
collection**, which directly invalidates audit #1's "remove, 301 to wedding-cakes" recommendation —
that was written when this collection was empty and looked like a redundant niche page; it's now a
populated, distinct, mislabeled product line that a plain redirect would silently discard.

Proposes a third, different fix: keep `cakes` as the single canonical `TYPE~Cake` collection; 301
the other four `TYPE~Cake` duplicates to it; fix or retire the self-cancelling Best Selling/Newest
collections; repair `showstopper-wedding-cake`'s mismatched handle/title/rule/SEO; tighten
`wedding-cakes`'s substring rule (`"wed"` would false-match "Wednesday," "wedge," "jewel"). Explicit
warning: **"Four 301s on live URLs. Audit printed QR codes, paid-ad destinations and GSC top pages
first."** Self-status: "Nothing here is authorised. Phase 1 is read-only and ends at approval."
Never executed.

### Audit #4 — `seo-audit/final/` (2026-07-30) — most recent, doesn't cite #1–#3

Re-confirms the cluster (now framed as 7 collections: the 4 identical `TYPE~Cake` duplicates plus
`cakes`, `custom-cakes-meerut`, `kids-birthday-cakes-meerut`) at counts matching this report's live
check exactly. Groups the rest of the 36 by role: 5 primary occasion collections need no structural
change; 13 theme sub-collections are real and distinct, should stay as filtered views not a URL
hierarchy change; 4 small collections (For Him, For Her, Photo Cakes, Flowers & Cake Combos)
explicitly "keep as-is" — **a direct reversal of audit #1's merge recommendation for `for-her`**;
Diwali Hampers is a precedent for festival-collection expansion; the two self-cancelling utility
collections need business approval to fix or unpublish. Recommends, for the 7-collection cluster,
"pick at most 1–2 to keep, unpublish the rest" — deliberately not a redirect/merge decision.
Explicitly gated `<<BUSINESS APPROVAL REQUIRED>>`, still open as of this document.

## 4. Consolidated per-collection disposition — what each audit said, and current validity

| Collection | Audit #1 (07-16) | Audit #2 (07-18) | Audit #3 (07-24) | Audit #4 (07-30) | Still valid today? |
|---|---|---|---|---|---|
| `midnight-cake-delivery` | Convert to landing page | noindex (0 products) | 301 → `cakes` | Unpublish or keep (1 of the cluster) | **Premise (0 products) is stale** — now 986. Audits #3/#4's framing is current. |
| `midnight-cake-delivery-meerut` | Redirect → `midnight-cake-delivery` | noindex | 301 → `cakes` | Unpublish or keep | Premise stale, same as above. |
| `cake-delivery-meerut` | Redirect → `/pages/cake-delivery-in-meerut` | noindex | 301 → `cakes` | Unpublish or keep | Premise stale. **Redirect target now confirmed live with real content (§7).** |
| `same-day-cake-delivery-meerut` | Convert to landing page | noindex | 301 → `cakes` | Unpublish or keep | Premise stale. |
| `custom-cakes-meerut` | Redirect → `designer-theme-cakes` | noindex | Fix rule or 301 | Unpublish or keep | Premise stale (0→617). `designer-theme-cakes` (165 products, manual) is a materially different, smaller set than this collection's 617 — a straight redirect would change what visitors land on. Needs re-evaluation, not a rubber-stamp of the 07-16 target. |
| `kids-birthday-cakes-meerut` | Convert manual → smart | noindex | Keep, review rule | Business decision | Already smart (13-way title OR, 128 products) — audit #1's own recommendation is already in effect, just undocumented. |
| `cakes` | *(didn't exist as this handle yet)* | Created to fix 223 broken redirects (P0-01) | Canonical target of the 301 plan | One of the cluster, "keep as-is" per grouping | Live, 986 products, the same rule as 4 others. |
| `showstopper-wedding-cake` | Remove, 301 → `wedding-cakes` | *(not covered)* | Repair mismatched title/handle/rule/SEO | *(not separately called out)* | **Audit #1's recommendation is now factually wrong** — the collection has 78 real, distinct products; a redirect would silently discard them. Audit #3's "repair, don't remove" is the only one of the four still applicable. |
| `boy-or-girl-cake` | Merge → "Baby & Gender-Reveal" (never created) | *(not covered)* | *(not covered)* | *(covered in "13 theme sub-collections... real, distinct")* | Merge target was never built. Audit #4's later framing (real, distinct, keep) contradicts audit #1. |
| `for-her` | Merge (1 product, thin) | *(not covered)* | "stock or noindex" | **"Keep as-is"** | Direct contradiction between audits #1 and #4. Still 1 product live — genuinely thin by audit #1's own ≥8–12 threshold rule, but audit #4 (more recent, live-requeried) says keep. Neither has fresh reasoning past "it's thin" vs "it's fine." |
| `flowers-cake-combos` | Populate or merge (1 product) | *(not covered)* | "stock or noindex" | "Keep as-is" | Same contradiction pattern as `for-her`. |
| `best-selling-products` | *(not covered — postdates?)* | *(not covered)* | Self-cancelling rule found, fix or retire | Confirmed 1,235/1,235, `<<BUSINESS APPROVAL REQUIRED>>` | Confirmed live: rule is genuinely self-cancelling, shows all 1,235 products including 588 drafts. Real defect, not resolved by any audit. |
| `newest-products` | *(not covered)* | *(not covered)* | Same defect | Same | Same as above. |
| `wedding-cakes` | *(not covered — rule didn't exist at 0-product framing)* | *(not covered)* | Rule `TITLE contains "wed"` flagged as false-match risk | *(not separately called out)* | Confirmed live: rule is exactly `TITLE contains "wed"`, disjunctive. Real latent-defect risk (would match "Wednesday-themed cake" etc. if such a product existed) though not proven to have actually mis-matched anything yet. |
| `gourmet-cookies-meerut` | *(not covered — didn't exist yet or wasn't in scope)* | *(not covered)* | *(not covered)* | *(not covered)* | **Never given a disposition by any audit.** Title is its own raw handle, no SEO fields set — the same "never named" pattern found on ~62 products in Phase 7.6. |
| `criciket`, `paw-petrol`, `boy or girl cake` (title casing) | *(not covered)* | *(not covered)* | *(not covered)* | Flagged (`ARCHITECTURE_VERIFICATION.md` B5) as deliberately deferred, same policy as the product-handle-typo deferral | Confirmed live: titles are still misspelled/miscased. Cosmetic, zero functional risk, correctly low-priority. |

## 5. Root cause, per proposal category

**The Meerut delivery cluster (5 collections sharing `TYPE contains "Cake"` or near-identical
rules)**: root cause is the single undocumented smart-collection conversion event from audit #2's
Phase 20 — not five independent mistakes, one mistake applied five times. **Reusable architectural
fix**: these were never really "collections" in intent — they're local-SEO landing pages for a
service (midnight delivery, same-day delivery) wearing a collection's clothing, which is exactly
audit #1's original diagnosis. The site already has the correct pattern built and working: real
pages (`cake-delivery-in-meerut`, `midnight-cake-delivery`) with substantial, distinct body copy,
linked from the `meerut-delivery` menu. The fix isn't "redirect A to B," it's "stop modeling a
service intent as a product filter" — a pattern, not a one-off. `same-day-cake-delivery-meerut` and
`custom-cakes-meerut` need the same treatment, not individually bespoke fixes.

**`showstopper-wedding-cake`**: root cause is a stale disposition, not a data defect — audit #1
correctly diagnosed an empty, redundant collection, but the underlying data changed (78 products
added) before the fix was ever applied, and no audit re-checked the premise before repeating the
recommendation. This is the same "stale roadmap item" pattern already caught and corrected twice
elsewhere in this project (the header star-rating item, the Motu Patlu title). **Reusable fix**:
the same principle already applied in Phase 7.6/7.7 — re-verify a proposal against live data
immediately before acting on it, every time, not just when a human happens to notice the doc is old.

**`best-selling-products` / `newest-products`**: root cause is a copy-paste rule-authoring error
(a disjunctive `contains X` OR `not-contains X` pair is a tautology — it can never exclude
anything). **Reusable fix**: this is a one-line rule correction per collection (change
`appliedDisjunctively` logic or the rule itself to something that actually filters, e.g. a real
"bestseller" tag/metafield-based rule), not a business decision about content — though *what* the
correct rule should select (which products count as "bestselling") is itself a merchandising call
this report won't guess at.

**`gourmet-cookies-meerut`**: root cause matches Phase 7.6's finding exactly — a collection created
and left with its placeholder handle as the display title, never finished. Not a merge/redirect
candidate at all; it's a content-completion gap, same category as the ~62 unnamed products already
flagged and left untouched in Phase 7.6 for the same reason (never fabricate a name).

## 6. Expected impact per disposition category

**SEO**: the 5-collection `TYPE~Cake` cluster is the one clear, current duplicate-content risk in
this whole audit — five URLs with near-identical product listings and machine-generated overlap is
exactly the pattern Google's own guidance on doorway pages and duplicate content targets. Resolving
it (by whichever mechanism, see §8) removes a real, live risk. The self-cancelling Best
Selling/Newest collections are lower-severity — they're wrong, but "wrong" here means
"meaningless," not "duplicate," so the SEO cost is more about wasted crawl budget and user trust
than ranking cannibalization. Fixing `showstopper-wedding-cake`'s mismatched signals would let
Google understand what the page is actually about, which it currently can't (title, handle, rule,
and body copy all disagree with each other).

**UX**: a customer landing on `cake-delivery-meerut` today sees the same 986-product, unfiltered
list as `midnight-cake-delivery`, `same-day-cake-delivery-meerut`, and `midnight-cake-delivery-meerut`
— none of these pages actually helps a customer trying to order for a specific delivery need find
what they came for. The `meerut-delivery` pages, by contrast, already have delivery-specific,
useful body copy. Consolidating traffic onto the pages (or rebuilding the collections'
rules to something that actually filters relevantly) is a direct UX improvement, not just an SEO
one. `showstopper-wedding-cake`'s confused branding is also a real UX defect today — a customer
following the "wedding cake" signal in the handle lands on a page about revolving surprise cake
setups.

**GEO/AEO/AI Search**: per `docs/AI_SEARCH_READINESS.md`, **the storefront is entirely
password-gated**, so no AI crawler (GPTBot, ClaudeBot, Google-Extended, PerplexityBot) can index
any of this today regardless of collection structure. Every GEO/AEO argument in every one of the
four audits is currently moot in practice — real, but dormant until the password gate lifts (a
separate, already-tracked business decision, not something this report is proposing to change).
Once the gate lifts, `CATALOG_ARCHITECTURE.md §5`'s framing (one clean entity per intent, rather
than 5 competing near-duplicate URLs for the same "cake delivery in Meerut" intent) becomes
directly relevant — worth keeping the recommendation, just noting it has zero live effect today.

## 7. Risks

- **301s on live URLs** — audit #3's own explicit warning stands and this report did not check it:
  before any redirect is created, printed QR codes, paid-ad destinations, and Google Search
  Console's top-performing-pages report for these exact handles need auditing first. Not done in
  this pass (would require GSC access, out of scope for a read-only repo/API investigation).
- **`custom-cakes-meerut` → `designer-theme-cakes` is not a clean redirect** — 617 products vs. 165,
  materially different sets. A visitor following an old link/bookmark/QR code to
  `custom-cakes-meerut` would land on a collection missing 452 products they might have expected.
- **`showstopper-wedding-cake` is not safe to remove or blind-redirect** — 78 real, live products
  would become unreachable via that URL if simply 301'd away without also fixing how those products
  are otherwise discoverable.
- **Unpublishing `best-selling-products`/`newest-products` outright removes functioning URLs** even
  though their current rule is broken — if anything external links to them, that's a new 404, not a
  fix, unless paired with a redirect or a rule repair.
- **No confirmation any of the 30 non-menu collections are truly unlinked** — the internal-linking
  M-1 gap (§2) means a "safe to touch" assessment based on navigation alone could still be wrong if
  a collection is linked from inside a page or product body this pass didn't check.

## 8. Benefits

- Resolving the 5-collection duplicate cluster removes the single clearest, most current SEO risk
  in the catalogue's collection layer.
- Fixing the two self-cancelling utility collections turns two currently-meaningless URLs into
  either working "bestseller"/"newest" pages or an honest removal — either is better than the
  current tautology.
- Repairing `showstopper-wedding-cake` fixes a real, live customer-facing confusion (wrong product
  expectation from the URL/title) independent of any SEO consideration.
- Naming `gourmet-cookies-meerut` properly (once real content exists to name it from) closes a
  content gap in the same family already resolved for products in Phase 7.6.

## 9. Dependencies

- **The M-1 internal-linking graph audit** remains open — narrowed by this report's navigation
  check, not closed.
- **The password gate** — GEO/AEO/AI-Search impact of any collection change is currently dormant.
- **Google Merchant Center currently submits 0 products** (`FINAL_NAP_AND_MC_ARCHITECTURE.md`) — no
  live Shopping-feed impact from any collection change today.
- **GSC/QR/paid-ad audit** — a hard prerequisite before any redirect is created (audit #3's own
  stated blocker), not performed in this pass.
- **A business decision on "which 1–2 of the cluster to keep"** — every one of the four audits
  agrees this specific call needs a human, not an engineer; none of them makes it.

## 10. Recommended safest implementation strategy, per proposal

Ranked by how much of the risk in §7 each carries, safest first:

1. **`gourmet-cookies-meerut`** — no disposition conflict, no redirect risk. Needs real content
   before it can be named or improved; until then, leaving it alone is correct (matches Phase 7.6's
   own precedent for unnamed products).
2. **`best-selling-products` / `newest-products`** — lowest-risk fix available: correct the
   self-cancelling rule to something that actually filters (a real bestseller tag/metafield), or
   explicitly decide these should just be unpublished. Either way, no redirect needed, no products
   become unreachable (they're all reachable through other collections already), and the only open
   question is *what rule should replace it* — a merchandising call this report flags but doesn't make.
3. **`showstopper-wedding-cake`** — repair, don't remove: align title/handle/SEO to describe what
   the collection actually is (audit #3's framing), rather than executing audit #1's now-invalid
   "remove and 301" plan. Lowest-risk path: keep the URL, fix the metadata to match the real
   product set.
4. **Wedding-cakes rule** (`TITLE contains "wed"`) — tighten to `TYPE = Wedding Cake` (matching the
   pattern already used successfully by `showstopper-wedding-cake`'s own rule) — a rule-only change,
   no redirect, no content loss, closes a latent false-match risk before it ever causes a visible
   problem.
5. **The 5-collection `TYPE~Cake` duplicate cluster** — highest-risk, most valuable, and the one
   every audit agrees is a real problem but none has authorized: requires (a) the GSC/QR/paid-ad
   check from §7 first, (b) a business decision on which 1–2 collections survive, (c) only then
   redirects for the rest — to the `meerut-delivery` pages where a suitable page exists (confirmed
   live and content-rich this pass for `cake-delivery-meerut`→`cake-delivery-in-meerut` and
   `midnight-cake-delivery*`→`midnight-cake-delivery`), or to `cakes` where it doesn't.
   `custom-cakes-meerut` needs its own decision (redirecting to `designer-theme-cakes` would drop
   452 products from view) rather than folding it into the same batch as the other four.
6. **`for-her` / `flowers-cake-combos`** — genuinely contested between audits #1 and #4 with no new
   evidence on either side; this report doesn't have grounds to break the tie. Flagged for a
   decision, not a recommendation.

## Related

[CATALOG_ARCHITECTURE.md](../CATALOG_ARCHITECTURE.md), [INFORMATION_ARCHITECTURE.md](../INFORMATION_ARCHITECTURE.md),
[SEO_AUDIT_LEDGER.md](../SEO_AUDIT_LEDGER.md), [docs/blog-os/CURRENT_STATE.md](blog-os/CURRENT_STATE.md),
[docs/blog-os/BLOG_OS_ROADMAP.md](blog-os/BLOG_OS_ROADMAP.md),
[seo-audit/final/WEBSITE_ARCHITECTURE.md](../seo-audit/final/WEBSITE_ARCHITECTURE.md),
[seo-audit/final/ARCHITECTURE_VERIFICATION.md](../seo-audit/final/ARCHITECTURE_VERIFICATION.md),
[seo-audit/final/IMPLEMENTATION_BACKLOG.md](../seo-audit/final/IMPLEMENTATION_BACKLOG.md),
[seo-audit/final/SITE_TREE.md](../seo-audit/final/SITE_TREE.md),
[seo-audit/final/NAVIGATION.md](../seo-audit/final/NAVIGATION.md),
[docs/INTERNAL_LINKING_AUDIT.md](INTERNAL_LINKING_AUDIT.md), [docs/AI_SEARCH_READINESS.md](AI_SEARCH_READINESS.md),
[docs/SHOPIFY_SEO_REPORT.md](SHOPIFY_SEO_REPORT.md).
