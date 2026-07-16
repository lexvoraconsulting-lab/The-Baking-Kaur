# PROJECT_ROADMAP.md — The Baking Kaur

Enterprise Shopify transformation roadmap. Status as of v1.0 (2026-07-14). Governed by the value gate in the flagship operating standard; every phase paused for approval, validated on preview before live.

## Legend
✅ done · 🔵 validated on preview (pending live promote) · ⏳ planned · 🔒 protected (no change)

## Planning track (complete)
| Deliverable | Status |
|---|---|
| Phase-1 Audit · Master Plan · Design Foundation · Operating Standard | ✅ |
| Information Architecture (5-yr) · Collection Audit | ✅ |
| Homepage Specification · Content Strategy | ✅ |
| Documentation library (20 docs) | ✅ |

## Implementation phases
| Phase | Name | Scope | Status |
|---|---|---|---|
| **A** | Production Safety | Schema dedup, dead-code removal, **footer restore + refine**, living docs | 🔵 preview-validated, pending promote |
| **A.1** | Collection Audit actions | Fix/redirect/merge 8 empty collections | ⏳ pending approval |
| **B** | Design Foundation | Extend `tbk-tokens` (type scale, spacing), buttons/cards/forms/icons/motion | ⏳ |
| **C** | Homepage | Build 9 sections per spec, section-by-section | ⏳ |
| **D** | Collections | Hero, filters, sorting, buying guides, SEO/GEO, premium cards | ⏳ |
| **E** | Navigation | One header, mega menu, predictive search, enterprise footer | ⏳ |
| **F** | SEO + GEO | Schema completion, entity linking, FAQ page-scope, titles/meta | ⏳ |
| **G** | Missing Pages | Local/delivery landings, guides, reviews, trust, help center | ⏳ |
| **H** | Performance | Lighthouse 95+, LCP<2s, CLS<0.1, INP; fonts/CSS/JS, app-script audit | ⏳ |
| **I** | Accessibility | WCAG 2.2 AA | ⏳ |
| **J** | Analytics | GA4, Meta, Clarity, WhatsApp tracking, enhanced ecommerce | ⏳ |
| **K** | Final QA | Cross-device, schema, CWV, regression, sign-off | ⏳ |
| — | **Product Page** | 🔒 protected — schema/analytics/perf-invisible only | 🔒 |

## Cross-cutting
- Every phase runs `QA_CHECKLIST.md` before promotion; `CHANGELOG.md` records file · reason · impact · rollback.
- Deploy model: preview theme → validate → promote to live (scoped pushes).
- Content from `HOMEPAGE_CONTENT_STRATEGY.md`; visuals from `DESIGN_SYSTEM.md` / `COMPONENT_LIBRARY.md`; schema from `SCHEMA_MASTER.md`.


## Backlog

### 🔤 SEO CONTENT FIX – Product Titles & Encoding  *(project · raised 2026-07-16 · does NOT block homepage)*
**No homepage dependency.** Homepage sections render titles from the product record; they neither cause nor fix this. Client directive: do not block homepage development.

**The defect.** The same bad import behind CATALOG_ARCHITECTURE §1b corrupted product text. Two distinct faults:
1. **Mojibake (encoding corruption).** UTF-8 read as CP1252 and re-encoded, turning an em-dash/apostrophe into `ÃÂÃÂ¢??`. Confirmed on **8 DRAFT products** (`ch290`, `ch292`–`ch296`, `ch298`) — e.g. `Eternal Wish Birthday Cake ÃÂÃÂ¢?? The Baking Kaur, Meerut`.
2. **Wrong title on a LIVE product — worse than the encoding.** `/products/motu-patlu-designer-birthday-cake-meerut` — the store's **#1 bestseller** — has H1 `Motu Patlu Designer Birthday Cake` but a `<title>` of `Celestial Charm Cake ÃÂÃÂ¢?? 100% Eggless Cakes & 2ÃÂÃÂ¢??4 hour express delivery in Meerut | The BaÃÂÃÂ¢?ÃÂÃÂ¦`. **It names a different cake**, and it is what Google shows in search results. This is a live, revenue-facing defect on the highest-traffic PDP — a customer searching Google sees the wrong product name.

**Scope — full audit required, not just the known cases.** The 8 mojibake drafts and 1 live wrong title are what surfaced incidentally. **Step 1 is to sweep the whole catalogue** — `title`, `seo.title`, `seo.description`, `descriptionHtml` — across all 1,235 products, active and draft. Assume more.

**Required steps:**
1. **Encoding cleanup** — detect the mojibake signature (`Ã`, `Â`, `ÂÂ¢`, `?ÂÂ¦`) across all text fields; repair to correct UTF-8. **Repair, never delete** — the underlying words are recoverable; a naive strip would silently destroy real title text.
2. **Title/H1 consistency** — every product's `seo.title` must describe the same product as its `title`/H1. The Motu Patlu case proves these drifted independently. Flag every mismatch, not only corrupted ones — a *clean* wrong title is just as damaging and won't show up in an encoding sweep.
3. **Search snippet optimization** — once correct, optimise `seo.title` / `seo.description` for length, keyword placement and click-through. **Only after** steps 1–2: optimising a wrong title is polishing the wrong thing.
4. **🚫 Preserve URLs** — **no handle is renamed by this project.** Titles and handles are independent; fixing a title must not touch its URL. Handle changes belong exclusively to **SEO MIGRATION – Product Handle Optimization**, with its own 301/QR checklist. Keeping these projects separate is deliberate: title fixes are safe and reversible, handle changes are neither.
5. **No homepage dependency** — runs entirely in product data, in parallel with any homepage phase.

**Verification:** re-crawl affected PDPs; confirm `<title>` matches H1; request re-indexing; confirm the corrected snippet appears in Search Console.
**Priority:** the live wrong title is **higher-value than the 8 drafts** — drafts are invisible to customers, whereas the #1 bestseller is misrepresented in Google right now.
**Risk if skipped:** the best-selling product keeps advertising the wrong cake in search results.



### ⭐ Collect genuine reviews  *(raised 2026-07-16 · blocks S5 activation · client action)*
**S5 Social Proof is built, frozen and renders nothing — because 0 verified reviews exist.** No approved review source is installed (verified 2026-07-16: no Judge.me, Loox, Shopify Product Reviews, Okendo, Stamped, Yotpo).

The homepage previously filled this gap with **fabricated testimonials** (`REVIEW_STRATEGY.md` §8). That option is permanently closed. The only route to social proof is real reviews.

**Options, in client-ratified priority order:**
1. **Google Business Profile** — reviews likely already exist. No Shopify sync: transcribe each into a `testimonial` metaobject with its public `source_url`, then verify (§3). **Fastest path to a populated S5.**
2. **Judge.me** — **strongest long-term option.** Collects *verified-buyer* reviews automatically after each order, forever, with no transcription. Turns social proof from a one-off task into a compounding asset. **Do not enable review gating** — Google treats it as deceptive.
3. **Loox** — photo reviews; strong fit for cakes, where the product is visual.
4. **Shopify Product Reviews** — native, basic.
5. **Zomato** — ⚠️ **blocked**: approved *only if legally displayable*, and nobody has checked whether Zomato's terms permit off-platform reproduction. Do not transcribe until confirmed.

**Effort → reward:** S5 needs **3 verified reviews** to activate. It then appears automatically — no code change, no deploy.
**Note:** a bakery claiming 20,000+ celebrations should not struggle to source reviews. It has simply never asked. A post-delivery WhatsApp asking for a Google review would likely resolve this in a week.



### 🔗 SEO MIGRATION – Product Handle Optimization  *(project · raised 2026-07-16 · scheduled AFTER homepage)*
**🚫 HARD RULE: no product handle is renamed during Homepage development.** Client directive, 2026-07-16. Every section built in Phase C links to existing handles exactly as they are.

**Scope.** Legacy import handles carry zero keyword signal. Known worst cases — all on the store's **top 8 best-selling products**, i.e. the highest-traffic PDPs:
| Current handle | Product | Status |
|---|---|---|
| `/products/b158` | Dreamy Princess Baby Girl Cake | HTTP 200 — working, but opaque |
| `/products/b155` | Cricket Ground Theme Birthday Cake | HTTP 200 — working, but opaque |
| `/products/hamper13` | Sweet & Fresh Cake and Flower Balloon Basket | HTTP 200 — working, but opaque |

The full population is larger — the same import defect (CATALOG_ARCHITECTURE §1b) produced `bNN` / `chNN` / `hamperNN` handles across the catalogue. **A full inventory of affected handles is step 1, not an assumption.**

**Why this is a project and not a task.** Renaming a handle changes a live URL. Done carelessly it destroys existing rankings, breaks inbound links, and silently kills any printed QR code. The SEO upside is real but is only realised if *every* step below completes.

**Required steps (all mandatory, in order):**
1. **Handle mapping** — full inventory of affected handles → proposed keyword-bearing target handles. Reviewed and approved before any change.
2. **301 redirect plan** — one permanent redirect per renamed handle, old → new. Written and staged *before* the rename, never after.
3. **Internal link update** — every theme section, metafield, blog, page and navigation entry pointing at an old handle updated to the new one. Redirects are a safety net, not a substitute.
4. **QR code audit** — identify any printed/offline material (boxes, cards, flyers, in-store signage) encoding a product URL. **A printed QR code cannot be updated after printing — its URL must keep resolving forever.** This step can veto a rename.
5. **Google indexing verification** — confirm new URLs are indexed and old ones show as redirected, not 404.
6. **Sitemap update** — regenerate and resubmit; confirm old URLs drop out and new ones appear.
7. **Canonical validation** — each new URL self-canonicals; no old handle left canonicalising to itself or to a dead target.
8. **Search Console monitoring** — track impressions/clicks/position per migrated URL for a defined window post-migration; define a rollback trigger before starting.

**Sequencing:** starts only after the homepage is complete and approved. Should follow the draft-catalogue cleanup (archiving the 56 duplicate twins first avoids migrating URLs that are about to be retired).
**Risk if skipped:** none — current handles work. **Risk if done badly:** loss of rankings on the store's best-selling products. This project is optional and deliberate; it is never urgent.

### 📝 CONTENT TASK – 100% Eggless Brand Page  *(raised 2026-07-15 · parallel workstream — does NOT block homepage)*
**Status:** created as a **DRAFT** — `/pages/100-percent-eggless-bakery` (`gid://shopify/Page/116138016937`, `isPublished: false`, verified 404 publicly).
**Purpose:** the canonical informational resource explaining why The Baking Kaur is a completely eggless bakery. **Not part of any homepage milestone.**
**Contains:** eggless philosophy · what eggless means here · 6 FAQs · links to the 5 primary collections + same-day/midnight pages.
**To do:** client reviews copy → publish → repoint the S2 "100% Eggless" trust card from `/pages/why-choose-the-baking-kaur` to this page (**section setting, zero code**) → add page-scoped `FAQPage` schema in Phase F (the only page permitted to carry it).
**Rule it enforces:** eggless is a brand attribute, never a collection (CATALOG_ARCHITECTURE §10).

### 📦 Publish draft catalogue  *(raised 2026-07-15 · client merchandising decision)*
**584 of 1,235 products are DRAFT** — roughly 47% of the catalogue is invisible to customers. Worst case: **Cake Hampers shows 8 of 119**, so the hamper range is effectively unsellable. This understates every pillar and is why homepage collection counts are currently OFF. Decide which drafts to publish vs archive.


### 🎯 Flagship Hero Photoshoot  *(raised 2026-07-15 · blocks: canonical homepage hero)*
The current homepage hero is a **Temporary Production Hero** — `Classic Strawberry Whipped Cream Cake` (product `b32`), chosen because **no compliant designer-cake asset exists**: every designer/theme/wedding shot in the catalogue carries customer names, printed messages, monograms, third-party branding (a `zomato` watermark, a `TWC` easel) or green outdoor backgrounds.

**Required final asset:**
- Exclusive **designer** cake (signature showpiece)
- **No text on cake** · no customer names · no watermark
- **White luxury background**, studio lighting
- **Landscape + portrait** versions (desktop 3:2 + mobile 4:5 crops)
- **High-resolution master** (≥3000px on the long edge)
- Becomes the **canonical homepage hero**

**Swap cost: zero code.** Theme editor → *Home · Editorial Hero* → upload to **"Flagship Hero master"**. The uploaded Files image always takes precedence over the temporary product source.

**Related cleanup (same shoot/decision):** remove the `zomato`-watermarked product image, the `TWC`-branded frame, and decide policy on customer names printed across catalogue photography.

## Immediate next decisions (owner: client)
1. Promote Phase A to live.
2. Approve Collection Audit dispositions.
3. Kick off Phase B (design tokens) — the unlock for C/D/E.
