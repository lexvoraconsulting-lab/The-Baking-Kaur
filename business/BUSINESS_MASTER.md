# Business Master — The Baking Kaur

**Single canonical source of truth**, consolidated 2026-07-30 from every completed audit, report, and
implementation this project has produced. All future development, SEO, Local SEO, Schema, AI SEO,
Shopify configuration, and documentation should read this file first.

**How to read status tags**: every fact below carries one of four tags —
**✅ Confirmed** (single, consistent, verified value — safe to reuse anywhere),
**🟡 Partial** (fixed on some surfaces, not yet on others — named explicitly),
**🔴 Conflicting** (two or more live, contradictory values — **do not pick one; this file does not
resolve conflicts, it documents them**), or
**⬜ Missing / Blocked** (no real value exists yet — client-blocked or awaiting a business decision).
Nothing in this document is invented. Where evidence conflicts or is absent, that is stated plainly
rather than resolved by guessing — consistent with this project's standing rule throughout
(`CLAUDE.md`: "verifiability beats persuasion").

**No code, Shopify configuration, or prior implementation is changed by this document.**

---

## 1. Company Information

| Field | Value | Status |
|---|---|---|
| Legal / trading name | The Baking Kaur | ✅ Confirmed — consistent across every theme file, page, and schema block |
| Business type | 100% eggless custom cake studio (bakery), single location | ✅ Confirmed |
| Location city | Meerut, Uttar Pradesh, India | ✅ Confirmed |
| Founding year / "years in business" | Not stated anywhere live | ⬜ Missing — a "Since 2018" claim exists only in dead, non-live code (`sections/footer.liquid`, SEO-014); never surfaced as a real claim |
| Named founder / owner | None named anywhere | ⬜ Missing — `EEAT_REPORT.md` flags this as a real, cheap E-E-A-T opportunity, not yet actioned |
| FSSAI licence | Claimed ("FSSAI-licensed kitchen") on the live eggless page and elsewhere; **no licence number given anywhere** | 🟡 Partial — claim exists, number doesn't; tracked in `CLAUDE.md` "Blocked on the client" |
| GST / GSTIN | Not found anywhere in the theme, pages, or schema | ⬜ Missing — not necessarily required for a D2C storefront; confirm with business whether it should be surfaced |
| Customer/order counts | 113 customers, 24 orders (real, Admin API, 2026-07-30) | ✅ Confirmed — this is why every "20,000+ customers" claim found across the theme was fabricated and removed |

## 2. Brand Information

| Field | Value | Status |
|---|---|---|
| Brand name (customer-facing) | "The Baking Kaur" | ✅ Confirmed, sitewide |
| **Business name on 3 Shop Policies** | **"The Bakery Kaur" (wrong)** | 🔴 Conflicting — Shopify's built-in Refund, Shipping, and Terms of Service policies all misname the business; fix is bundled into the still-blocked B1 (SEO-031) policy rewrite |
| Logo tagline | "Luxury Eggless Creations" | ✅ Confirmed (`header-group.json`, `tbk_header_main` block) |
| Positioning | 100% eggless as standard practice (not a substitution or special request), made-to-order, custom/designer/wedding cake specialist | ✅ Confirmed — repeated consistently across About Us, the eggless page, and every delivery page |
| Brand story / founding narrative | None beyond generic positioning | ⬜ Missing — `EEAT_REPORT.md` flags as a content opportunity, not a defect |
| Price positioning | `priceRange: "₹₹"` (schema) | ✅ Confirmed |

## 3. Contact Information

| Field | Value | Status |
|---|---|---|
| Phone / WhatsApp | +91 8218862928 | ✅ Confirmed — same 10-digit number everywhere; only string *formatting* varies (`+918218862928` / `+91-8218862928` / `+91 8218862928`), cosmetic only |
| Email | thebakingkaur@gmail.com | ✅ Confirmed — identical everywhere checked (Admin `contactEmail`, Contact page, footer, Refund policy page, all schema files) |
| Contact page tel:/WhatsApp links | Fixed 2026-07-30 (SEO-033) — were previously broken (`tel:+91` with no digits, `wa.me/91` with no number) | ✅ Confirmed fixed and live |
| Sticky WhatsApp button (sitewide) | `https://wa.me/918218862928?text=Hi%20I%20want%20to%20order%20a%20cake` | ✅ Confirmed, `layout/theme.liquid` |

## 4. Address

| Field | Value | Status |
|---|---|---|
| **Canonical address (as of 2026-07-30, B3)** | "Fateh Complex, 390/1, Lane Number 7, opposite Ice Factory, Thapar Nagar Gali Number 7 Lajpat Bazaar Thapar Nagar, Meerut, Uttar Pradesh 250001" | 🟡 Partial — this is the Shopify Admin billing-address text, now propagated to 5 theme files (`bk-local-business.liquid`, `tbk-schema-website.liquid`, `site-footer.liquid`, `footer.liquid`, `tbk-footer.liquid`) |
| **Still-inconsistent surfaces** | Custom "Refund & Return Policy" page body still says "390/1, Lane Number 7, Thapar Nagar, Meerut, Uttar Pradesh 250001" (older, shorter variant); the Shopify built-in Contact Information Shop Policy still says "Fateh complex, Thapar Nagar Gali no 7, Meerut city, Pincode :250001" (also has stray malformed `<meta charset="utf-8">` HTML) | 🔴 Conflicting — both are Admin-API-only surfaces, blocked from this session's last implementation pass (MCP disconnected) |
| Independent real-world corroboration | A real Google Business Profile listing (see §5) resolved 2026-07-30 shows near-identical address text to the canonical value above | ✅ Confirmed as corroborating evidence, not a fourth conflicting source |
| Postal code | 250001 | ✅ Confirmed, no conflict |
| City / State / Country | Meerut / Uttar Pradesh / India | ✅ Confirmed, no conflict |

## 5. Google Business Profile

| Field | Value | Status |
|---|---|---|
| Listing found | *"The Baking Kaur \| Premium Bakery and Cake Shop \| Best bakery in meerut \| Best cakes in meerut"* | ✅ Confirmed real — resolved 2026-07-30 from a pre-existing Google Maps share link (`https://maps.app.goo.gl/LmD25vZFZYQL3TTd6`) sitting in `sections/footer.liquid`, never previously checked |
| Google Place ID | `0x390c65d0e49bbaef:0x3e9dd4af9a9b1468` | ✅ Confirmed, extracted from the resolved Maps URL |
| Listing address text | "Fateh Complex, 390/1, Lane Number 7, opposite Ice Factory, near Hemkund Car Accessories, Thapar Nagar, Lajpat Bazaar, Thapar Nagar, Meerut, Uttar Pradesh 250001" | ✅ Confirmed — closely corroborates the canonical address in §4, plus one new detail ("near Hemkund Car Accessories") not previously known anywhere in the theme |
| Exact GBP coordinates | Not extractable | ⬜ Missing — Google Maps place pages are JS-rendered; neither a direct fetch nor a CID-based URL lookup could retrieve decimal coordinates with the tools available this session |
| GBP rating / review count | Not checked this pass (out of scope — this document consolidates, it doesn't re-audit) | ⬜ Not evaluated — `EEAT_REPORT.md` already established 0 verified on-site reviews exist |
| Manual QA follow-up | A human with local knowledge should visually confirm the GBP pin location matches the real storefront | ⬜ Outstanding, per `IMPLEMENTATION_SUMMARY.md`'s QA checklist |

## 6. Map Coordinates

| Field | Value | Status |
|---|---|---|
| **Canonical coordinates (as of 2026-07-30, B3)** | Latitude `28.9897017`, Longitude `77.7044604` | 🟡 Partial — sourced from the Shopify Admin billing address (`shop.billingAddress`), now live in both `bk-local-business.liquid` and `tbk-schema-website.liquid` |
| Prior schema value (now replaced) | Latitude `28.9931`, Longitude `77.6939` | Superseded — this value predated any real sourcing and had an in-code comment flagging it as unverified even before this project's audit began |
| Discrepancy this resolved | The two live schema sources were ~600 m apart before 2026-07-30 | ✅ Resolved — both now agree |
| Independent verification | **Not yet a literal human-confirmed fresh pin-drop** | ⬜ Outstanding — the real GBP listing (§5) corroborates the address text but its exact coordinates couldn't be extracted; `ADDRESS_AUDIT.md`'s original recommendation for a fresh Maps pin-drop is not fully satisfied |

## 7. Delivery Areas

| Field | Value | Status |
|---|---|---|
| Service radius | ~15 km from the Meerut studio | ✅ Confirmed, `CLAUDE.md` |
| Minimum order for delivery | ₹350 | ✅ Confirmed, `CLAUDE.md` |
| Fee structure | Distance-based; Merchant Center shipping set to Manual, decoupled from Shopify shipping profiles | ✅ Confirmed, `CLAUDE.md` |
| **Named localities — List A** (live "Cake Delivery in Meerut" page) | Thapar Nagar, Shastri Nagar, Ganga Nagar, Partapur, Jagriti Vihar (+ "nearby localities") | 🔴 Conflicting with List B |
| **Named localities — List B** (live footer `service_areas` setting) | Thapar Nagar, Shastri Nagar, Sadar Bazaar, Civil Lines, Pallavpuram, Ganga Nagar | 🔴 Conflicting with List A — only 2 of 5 distinct names match between the two lists |
| Resolution status | **Unresolved (B4, SEO-035)** — the approved decision was to confirm the real list against actual logistics/fee-zone data, not to pick or merge either list; no concrete list has been supplied yet | ⬜ Blocked — do not merge these lists as a shortcut |
| Same-day delivery | Available for "most designs ordered within cut-off time" — exact cut-off hour never stated anywhere | ✅ Confirmed as-worded; ⬜ cut-off hour missing |
| Midnight delivery | Booked in advance, cake baked fresh same-day, delivered around midnight | ✅ Confirmed |
| 30-minute express delivery | Selected ready-to-go designs only, selected areas only (not specified which) | ✅ Confirmed as-worded; ⬜ qualifying-area list missing |
| Wedding venue delivery | "Flexible on-site setup depending on the venue and client requirement" — real, live sitewide FAQ claim | ✅ Confirmed as a service exists; ⬜ no radius/fee specifics |
| Corporate/bulk delivery | Home, Office, Venue delivery; no stated minimum order size or lead time | ✅ Confirmed as a service exists; ⬜ specifics missing |

## 8. Working Hours

| Field | Value | Status |
|---|---|---|
| **Schema value** (`bk-local-business.liquid`, live sitewide) | 09:00–23:59, all 7 days | 🔴 Conflicting with the Contact page |
| **Contact page prose value** (`page.contact-2.json`, live) | "Open daily from 10:00 AM to 12:00 Midnight" | 🔴 Conflicting with the schema value — a 1-hour gap on opening time (9 AM vs. 10 AM); closing time is effectively the same once rounded |
| Resolution status | **Unresolved** — not one of the B1-B6 blockers explicitly, first flagged in `ADDRESS_AUDIT.md` §5; needs the same kind of "confirm the real hours" business input as the delivery-area conflict | ⬜ Open |

## 9. Policies

| Policy | Canonical-recommended source | Current live reality | Status |
|---|---|---|---|
| **Refund / Return / Cancellation** | Custom Page "Refund & Return Policy" (12hr cancellation, 4hr issue window, 5-7 day refund) — approved as canonical (B1) | Shopify's built-in Refund policy and Terms of Service **still say "all orders final, no refunds or replacements ever,"** directly contradicting the approved canonical page | 🔴 **Conflicting, unresolved** — B1 approved but not yet executed (Admin API blocked); this is the single highest-priority open item in the entire project |
| **Terms of Service** | Shop Policy: Terms of Service (once corrected) recommended as canonical | Custom "Terms and Conditions" page is live, published, **completely empty** (SEO-034); Shop Policy version still says "The Bakery Kaur" and contradicts Refund policy | 🔴 **Conflicting, unresolved** — B2 approved but not yet executed |
| **Shipping** | Shop Policy: Shipping — no competing custom page | Live text says "2-5 hours" delivery / "1 hour" issue window — unsourced anywhere else, inconsistent with the Refund policy's 4-hour window | 🔴 Unsourced, not yet corrected (part of B1's scope) |
| **Privacy** | Shop Policy: Privacy policy | Correct, functioning, Shopify default template with merge fields intact | ✅ Confirmed — no conflict, no action needed |
| **Cookies** | Folded into Privacy Policy (no separate Shopify policy type exists for this shop) | "Your Privacy Choices" (CCPA/GPC opt-out widget) exists but is **unpublished** | 🟡 Partial — architecture is fine, the opt-out mechanism itself is switched off; needs a business call on whether this store serves jurisdictions requiring it |
| **Contact Information** | Custom "Contact Us" page (already accurate, links fixed 2026-07-30) recommended over the Shop Policy version | Shop Policy: Contact Information still has old address text + malformed `<meta charset="utf-8">` HTML | 🔴 Conflicting, unresolved (same Admin-API block as B1/B2) |
| Draft duplicate | "Return, Refund & Replacement Policy" custom page | Unpublished (not deleted) — holds one clause (customised-products-non-returnable, worded more explicitly) not yet merged into the canonical page | ⬜ Awaiting merge-then-delete once B1 executes |

## 10. Trust Signals

| Signal | Value | Status |
|---|---|---|
| Verified reviews | **0** | ⬜ Missing — 3 real reviews needed to activate the already-built Social Proof section; `CLAUDE.md` recommends transcribing Google Business Profile reviews (now that a real GBP listing is confirmed, §5, this path is more concrete than before) or Judge.me |
| Star ratings / fabricated claims | All previously-found fabricated ratings ("4.8/4.9 Google Rated," fake customer counts, a fake "Customer Reviews" section with invented names) — **removed** | ✅ Confirmed clean — 13 separate fabrication instances found and removed across this project, none currently live |
| Social profiles | Instagram (`instagram.com/thebakingkaur`), Facebook (`facebook.com/thebakingkaur`) | 🟡 Partial — real and verifiable, but **inconsistently listed**: `bk-local-business.liquid`'s `sameAs` includes both; `tbk-schema-website.liquid`'s `sameAs` still lists Instagram only (SEO-020, not yet reconciled) |
| FSSAI | See §1 | 🟡 Partial |
| GST | See §1 | ⬜ Missing |
| Awards / press / certifications | None found anywhere | ⬜ Missing |
| AggregateRating schema | Deliberately never emitted — `bk-local-business.liquid` carries a permanent, self-documenting guardrail comment against ever hardcoding one | ✅ Confirmed correct practice, preserve this guardrail in any future edit |

## 11. Collections

Real inventory, 36 collections total (confirmed via live Admin API query, most recently 2026-07-30):

| Group | Collections | Status |
|---|---|---|
| **Primary occasion** (5) | Birthday Cakes (279), Anniversary Cakes (102), Wedding Cakes (134), Designer & Theme Cakes (165), Cake Hampers (119) | ✅ Confirmed — real merchandising backbone, no issues |
| **Theme sub-collections** (13) | Baby Girl, Butterfly, Criciket *(typo — "cricket," deferred per handle-optimization policy)*, Motu Patlu, Unicorn, Jungle Animal Theme, Chartered Accountant, roblox, PAW PETROL, Teddy, ribbon-cake ("Bow Cake"), KPOP Cake, boy-or-girl-cake | ✅ Confirmed real and distinct, no action needed beyond the known handle typo |
| **Small distinct collections** (4) | For Him (11), For Her (1), Photo Cakes (4), Flowers & Cake Combos (1) | ✅ Confirmed, no issues |
| **Festival collection** (1, precedent for more) | Luxury Diwali Hampers (44) | ✅ Confirmed working pattern; other festivals (Rakhi, Karwa Chauth, etc.) not yet given dedicated collections |
| **Non-curating utility collections** (2) | "Best Selling Products" (1,235) and "Newest Products" (1,235) — both identical to `/collections/all`, no real sort logic applied | 🔴 **Unresolved (B5)** — approved to wire real sort logic or unpublish, not yet executed (Admin API blocked, and no merchandising pick was supplied) |
| **Duplicate "Meerut" cluster** (7) | `cakes` (986), `cake-delivery-meerut` (986), `same-day-cake-delivery-meerut` (986), `midnight-cake-delivery-meerut` (986), `midnight-cake-delivery` (986), `custom-cakes-meerut` (617), `kids-birthday-cakes-meerut` (128) | 🔴 **Unresolved (B5)** — all near-identical, a live duplicate-content risk; approved to keep at most 1-2 with a genuine distinct purpose and unpublish the rest, not yet executed |

## 12. Navigation

State as of 2026-07-30 (post Sprint 2 implementation):

| Menu | Current live content | Status |
|---|---|---|
| `main-menu` (wired to the live header) | HOME, ABOUT US, CONTACT US, and "Categories" — now a dropdown of 6 real collections (Birthday, Anniversary, Diwali Hampers, Theme Cakes, Hampers, Wedding) | ✅ Confirmed — implemented 2026-07-30 (Sprint 2, task 2.1), single row preserved, native accessible disclosure, no second nav row added |
| `meerut-delivery` | Populated with 3 real delivery-mode pages (Cake Delivery in Meerut, Midnight Delivery, 30-Minute Express Delivery) | 🟡 Partial — populated 2026-07-30, but **not yet surfaced in any live section**, and the future Delivery Areas hub item is blocked on B4/B6 |
| `about-us-menu` | About Us, Contact Us (Store Locations item removed 2026-07-30, was pointing at the unpublished fake Store Locator page) | ✅ Confirmed fixed; still not confirmed wired to any live section |
| `header` | Birthday Cake, Anniversary Cake, Diwali Hampers, Theme Cakes, Hampers, Wedding Cakes | ⬜ Still orphaned — only referenced by a `disabled: true` section block; its content was reused (not moved) into `main-menu` |
| `quick-links-menu` | FAQ's, Privacy/Refund/Shipping Policy (correctly typed `SHOP_POLICY`), Terms & Condition (still `type: PAGE` → the empty Terms page) | ⬜ Unwired, and its Terms item still needs the same fix as the footer's, blocked on B1/B2 |
| `footer` | Search, Contact Us, Privacy/Shipping/Refund Policy, Your Privacy Choices | ⬜ Still not rendered by the live footer (which hardcodes its own links instead — see §13) |
| `explore-cakes`, `quick-links` | Empty (0 items) | ⬜ Still unused/orphaned menu shells |

## 13. Footer

| Element | Current state | Status |
|---|---|---|
| Live footer file | `sections/site-footer.liquid` (confirmed live via `footer-group.json`) — hardcodes its own links rather than rendering the `footer` menu | ✅ Confirmed as the actual live footer |
| Address shown | Now the canonical address (§4), updated 2026-07-30 | ✅ Confirmed |
| Refund link | `shop.refund_policy.url` with a fallback to the **unpublished draft** page if blank; since `shop.refund_policy` is non-blank, real visitors currently land on the **uncorrected Shop Policy** (still says "no refunds ever") | 🔴 Conflicting/incorrect — fix blocked on B1 |
| Terms link (2 occurrences) | One conditional (`shop.terms_of_service`, falls back to the empty custom page), one **unconditionally hardcoded** straight to the empty custom page | 🔴 Broken — fix blocked on B1/B2; the unconditional occurrence is a distinct defect from the conditional one, both need the same underlying fix |
| Shipping link | `shop.shipping_policy.url` | ✅ Confirmed working (points at a real, if unsourced-content, Shop Policy) |
| FAQ link | **Absent** from the footer entirely | ⬜ Missing — recommended addition, not yet implemented |

## 14. Social Links

| Platform | URL | Status |
|---|---|---|
| Instagram | `https://www.instagram.com/thebakingkaur` | ✅ Confirmed, listed in both schema sources |
| Facebook | `https://www.facebook.com/thebakingkaur` | 🟡 Partial — listed in `bk-local-business.liquid`'s `sameAs`, **absent** from `tbk-schema-website.liquid`'s `sameAs` (SEO-020, unreconciled) |
| Google Business Profile | See §5 | ✅ Confirmed to exist; not yet added to any `sameAs` array in the theme's schema — a real opportunity discovered this session, not yet actioned |

## 15. Schema Values

| Entity | File | Real values | Status |
|---|---|---|---|
| `WebSite` | `tbk-schema-website.liquid` | Dynamic name/url/description, `SearchAction` wired to `/search?q={search_term_string}` | ✅ Confirmed correct |
| `Organization` | `tbk-schema-website.liquid` | Name, url, logo, telephone; `address` now includes `streetAddress`+`geo` (added 2026-07-30, previously absent) | ✅ Confirmed, `sameAs` gap noted in §14 |
| `Bakery` (LocalBusiness) | `bk-local-business.liquid` | Name, description, telephone, `priceRange`, address+geo (both updated 2026-07-30), `areaServed: "Meerut"` (city-level only, not neighborhood-level — pending B4), `openingHoursSpecification` (09:00-23:59, conflicts with Contact page, §8), `makesOffer` (Midnight Cake Delivery), `sameAs` (both socials) | 🟡 Partial, see §8/§14 for the two open conflicts |
| `BreadcrumbList` | `tbk-schema-breadcrumb.liquid` | Fully dynamic, correct across product/collection/article/page types | ✅ Confirmed correct, no issues |
| `CollectionPage` | `tbk-schema-collection.liquid` | Fully dynamic, real product loop | ✅ Confirmed correct |
| `Article` | `tbk-schema-article.liquid` | Real `published_at`, real author/publisher reference; `dateModified` hardcoded equal to `datePublished` (SEO-021, low priority, needs checking against Shopify's real Liquid objects) | 🟡 Partial, low priority |
| `Product` (native) | `structured-data.liquid` | Shopify's native `structured_data` filter; safe by construction (no review app connected, cannot fabricate `aggregateRating`) | ✅ Confirmed correct |
| `Product` (hand-rolled, hampers only) | `main-product.liquid` | Kept intentionally for `hampers-template` — richer fields (`sku`, `category`, `seller`, real `shippingDetails`, `hasMerchantReturnPolicy`) the native filter lacks; native emission suppressed only for this template to avoid duplication | ✅ Confirmed correct, resolved SEO-023 |
| `FAQPage` | `sections/accordion.liquid` (per-item Microdata) + `layout/theme.liquid` (9-question sitewide block, gated off the 2 FAQ pages) | Real, non-fabricated content on both surfaces as of 2026-07-30 | ✅ Confirmed correct, resolved SEO-013/024 |
| `AggregateRating` / `Review` | Never emitted anywhere | ✅ Confirmed correct — deliberate, guarded against |

## 16. SEO Values

| Value | Standard | Status |
|---|---|---|
| Active-product SEO title format | `"{Name} - Eggless \| Meerut"` (or `"{Name} \| Meerut"` if the first exceeds 60 chars) | ✅ Confirmed, all ~602 active products migrated, per `CLAUDE.md` |
| Meta description | Type-specific hooked description, present per product | ✅ Confirmed for spot-checked products |
| Canonical tags | `<link rel="canonical" href="{{ canonical_url }}">`, Shopify-native, dynamic per page type | ✅ Confirmed correct |
| `robots.txt` | Clean — public routes crawlable, admin/checkout/account disallowed, filter/sort params blocked (crawl-trap mitigation) | ✅ Confirmed correct |
| `sitemap.xml` | Returns 404 | ⬜ Unresolved (SEO-019) — likely a symptom of the storefront's password gate, unconfirmed either way; re-check once the gate lifts |
| `noindex`/`meta robots` | None found anywhere | ✅ Confirmed correct (no defect; a storefront generally shouldn't blanket-noindex) |
| Duplicate title/thin-content sweep (full catalogue) | Only spot-checked, not run at full 602-product scale | ⬜ Not yet performed |
| Storefront crawlability | **Entire site is password-gated** ("Coming Soon"), confirmed intentional (pre-launch) | ⬜ Standing context — no live-crawl-based check is meaningful until this lifts |

## 17. AI Entity Values (GEO)

The canonical, safe-to-cite facts for AI answer engines (ChatGPT, Perplexity, Google AI Overview) —
everything here is independently verified elsewhere in this document, restated together since GEO
readiness depends on a coherent entity picture:

- **Entity name**: The Baking Kaur (note: 3 live Shop Policies still say "The Bakery Kaur" — a real,
  unresolved entity-consistency risk for AI systems too, not just human readers).
- **Entity type**: Bakery / LocalBusiness, single location, Meerut, Uttar Pradesh, India.
- **Core verified differentiator**: 100% eggless as standard practice for every product (not a
  substitution or special request) — repeated consistently across independent pages, a genuine
  positive consistency signal for AI citation.
- **Verified services**: custom/designer/wedding cakes, gift hampers, same-day/midnight/express
  delivery, corporate gifting.
- **Verified contact**: phone/WhatsApp +91 8218862928, email thebakingkaur@gmail.com.
- **Verified address**: see §4 (partial — 2 surfaces still lag).
- **Verified social presence**: Instagram, Facebook (see §14 for the `sameAs` gap).
- **NOT safe to cite** (missing or fabricated-then-removed): any review count, star rating, customer
  count, "years in business," award, or press mention — none are backed by real data as of this
  document. Any future content generation (human or AI-assisted) must not introduce these without a
  real source, per this project's standing rule.
- **Known entity contradiction an AI system might surface**: the refund/cancellation policy conflict
  (§9) — if an AI system is asked about this store's refund policy, it may find and cite either the
  permissive custom page or the restrictive Shop Policy, since both are currently live and
  contradictory. This is a real AI-answer-quality risk, not just a human-UX one.

## 18. Local SEO Values

| Value | Status |
|---|---|
| Service radius | ~15 km — ✅ Confirmed |
| Minimum delivery order | ₹350 — ✅ Confirmed |
| Delivery fee model | Distance-based, Manual Merchant Center shipping — ✅ Confirmed |
| NAP (Name/Address/Phone) consistency | 🟡 Partial — Name has a 3-surface conflict (§2), Address has a 2-surface residual conflict (§4), Phone has no real conflict (formatting only) |
| `areaServed` schema granularity | City-level only ("Meerut") — not neighborhood-level; expansion blocked on the delivery-area-list conflict (§7/B4) |
| Google Business Profile consistency check | Not yet performed against the live GBP listing found this session (§5) — recommended next step now that a real listing is confirmed to exist |
| Delivery-area content | Conflicting (§7) — blocks any Local SEO content investment (Delivery Areas hub, per-locality pages) until resolved |
| Working hours | Conflicting (§8) |

---

## What this document does not do

No code is modified, no Shopify data is changed, and no prior implementation is altered. This is a
consolidation of already-established, already-verified facts and already-approved-but-not-yet-executed
decisions — every conflicting or missing value is stated as such, not resolved here. Where a value is
tagged 🔴 or ⬜, treat it as **not yet safe to use as a single source of truth** until the referenced
blocker (B1/B2/B4/B5/B6, or the working-hours/`sameAs` discrepancies) is actually resolved.

## Source documents consolidated into this file

`CLAUDE.md`, `seo-audit/issues.yml`, `seo-audit/audit/AUDIT_LEDGER.md`, `seo-audit/audit/CHANGELOG.md`,
`seo-audit/audit/SCORECARD.md`, `seo-audit/final/EXECUTIVE_REPORT.md`,
`seo-audit/final/BUSINESS_DECISION_IMPLEMENTATION.md`, `seo-audit/final/ADDRESS_AUDIT.md`,
`seo-audit/final/POLICY_CONSOLIDATION.md`, `seo-audit/final/POLICY_ARCHITECTURE.md`,
`seo-audit/final/POLICY_REDIRECT_PLAN.md`, `seo-audit/final/DELIVERY_AREA_SPEC.md`,
`seo-audit/final/EEAT_REPORT.md`, `seo-audit/final/LOCAL_SEO_ROADMAP.md`,
`seo-audit/final/CONTENT_PLAN.md`, `seo-audit/final/WEBSITE_ARCHITECTURE.md`,
`seo-audit/final/SITE_TREE.md`, `seo-audit/final/NAVIGATION.md`, `seo-audit/final/URL_STRUCTURE.md`,
`seo-audit/final/INTERNAL_LINKING.md`, `seo-audit/final/ARCHITECTURE_VERIFICATION.md`,
`seo-audit/final/SPRINT1_BLOCKERS.md`, `seo-audit/final/BUSINESS_DECISION_GUIDE.md`,
`seo-audit/final/IMPLEMENTATION_SUMMARY.md`, `seo-audit/schema/SCHEMA_AUDIT.md`,
`seo-audit/seo/TECHNICAL_SEO.md`, `seo-audit/seo/GEO_AUDIT.md`, `seo-audit/ux/CRO_AUDIT.md`,
`seo-audit/ux/UX_AUDIT.md`.
