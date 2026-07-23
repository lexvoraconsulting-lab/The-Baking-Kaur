# Decisions

Log of consequential decisions actually made on this project, newest first. Dates are best-effort from `VERSION.md`, the SEO audit ledger, and session history; mark uncertain ones TODO.

Format: **what was decided** — context / why — consequence.

---

### 2026-07 · Product descriptions: fix mis-assigned "occasion"
The bulk-import descriptions wove an occasion into the copy ("Designed for anniversaries… This anniversary cake") that was frequently wrong for kids/baby/theme cakes. **Decision:** rewrite the occasion to *birthday* **only** where the title contradicts it (title has no "anniversary"/"wedding"); genuine anniversary/wedding cakes (word in title) are never touched; design detail and varied phrasing are preserved. Tool: `seo-ops/fix_description_occasion.py` (+ test). Baby Girl collection (18 products) corrected; ~100+ remaining tracked in `tasks/`.

### 2026-07 · Product JSON-LD: escape description with `| json`
`main-product-premium-v2.liquid` built the Product schema `description` with `| strip_html | escape`. `escape` does not escape JSON control characters, so raw newlines produced invalid JSON and Google discarded the block on ~600 pages. **Decision:** switch to `| strip_html | json`. Deployed single-file to live theme and verified. Standard: always build JSON-LD with `| json`.

### 2026-07 · Collection descriptions trimmed
Eight collections carried 400–850-word walls of repeated headings and bullet lists (plus a leaked `<style>` block and a pasted admin URL on Winter Strawberry). **Decision:** replace with short 2-line intros that keep primary keywords + delivery signals; leave SEO meta tags untouched. Empty theme/character collections given short crawlable intros.

### 2026-07 · Active-product SEO snippet format
Position ~5.3 at ~1.1% CTR with a legacy `"{Name} in Meerut | The Baking Kaur"` template (grammar bug, shared descriptions). **Decision:** migrate all active products to `"{Name} - Eggless | Meerut"` (short form `"{Name} | Meerut"` when >60 chars) + a type-specific hooked meta description. Tool: `seo-ops/fix_seo_snippets.py`. All ~602 active products migrated.

**Format history (superseded, kept for context):**
- *v1* (bulk import): `"{Name} in Meerut | The Baking Kaur"` — grammar bug ("1 sizes"), one shared description skeleton, mojibake in many titles.
- *v2 proposal* (2026-07-18, in the now-removed `seo-ops/v2/`): `"{Clean Title} | The Baking Kaur"`, **no appended locality**. Reasoning: only 81/607 (13%) product titles mention Meerut natively; titles are already unique (606 distinct of 607, avg 32 chars); a locality token repeated across 606 titles is a rewrite signal that buys nothing on the map pack (driven by GBP/proximity/reviews); locality belongs on category/service pages. **Superseded** by the current format, which re-adds *Meerut* as the local qualifier but drops the brand suffix (Google appends the site name anyway, saving ~18 chars to truncation). The "locality belongs on category/service pages" reasoning still holds for those page types.

Reusable title-cleaning logic from that work — repeated trailing brand/locality stripping (`clean_base`) and mojibake / handle-as-title detection (`is_broken`, `MOJI`) — is preserved in `seo-ops/title_utils.py`.

### 2026-07 · Merchant Center: `identifier_exists` = custom_product true (all products)
Segmented from the product export (evidence, not assumed) across 606 active products: **A** custom-made / no manufacturer GTIN = 606 (all); **B** legitimate GTIN/barcode = 0; **C** branded packaged / resold = 0 (vendor is "The Baking Kaur" on all 607); **D** has MPN = 0; **E** uncertain = 0 (3 hampers reviewed → A: the sold unit is an in-house assembled hamper). **Decision:** set `mm-google-shopping.custom_product = true` for every product; never invent GTIN/MPN/barcode. Applied via the v2 run; the generator scripts have since been removed as scratch (this record preserves the reasoning).

### 2026-07 · Redirects: repoint, don't delete
GSC read redirects to `/collections/all` as soft-404s, causing "fixed" 404s to reappear. **Decision:** repoint catch-all redirects to the closest real collection via an ordered rules table (`seo-ops/repoint_redirects.py`) rather than deleting. Genuinely-deleted products are allowed to 404 (correct behaviour), not mass-redirected.

### 2026-07 · Merchant Center shipping = Manual
The Google & YouTube channel showed 0 eligible products because shipping profiles exposed 0 countries. **Decision:** set Merchant Center Shipping Information to **Manual**, decoupling it from Shopify shipping profiles, without deleting the Meerut delivery policy or making an India-wide delivery claim. Also turned **off** "Local Inventory Retail Locations" (dropped Not-Approved from ~4,980 to ~99).

### 2026-07 · Local delivery: ₹350 minimum, distance-based fees
**Decision:** set the minimum order to **₹350** across all three distance zones (0–5 km ₹150, 5–10 km ₹200, 10–15 km ₹450) to enable ₹350 bento cakes, keeping distance-based fees. Do **not** expand the 15 km radius; do **not** add Modinagar. Shopify Local Delivery and Merchant Center kept consistent.

### 2026-07 · Two imageless products set to Draft
`Velvet Crown Birthday Cake` (8768184484009) and `Handcrafted Birthday Cake` (8768184516777) lacked images → **Decision:** set to Draft (not deleted; titles/handles/variants/pricing untouched).

### (foundational) · Default product template = `main-product-premium-v2`
All products render `main-product-premium-v2` via `product.json`. This template is a **protected module** — no visual/UX/flow/CSS/JS changes. See `memory/`.

### (foundational) · Protected modules & value gate
Logo, brand colors, and the product page are protected. Every change must pass the value gate (improves UX / trust / conversion / SEO / GEO / accessibility / performance / maintainability / scalability). See `00_START_HERE.md` and the flagship-operating-standard memory.

---

TODO: back-fill exact dates and any pre-2026-07 architectural decisions (theme selection, IA) from `PROJECT_ROADMAP.md` / `CHANGELOG.md`.
