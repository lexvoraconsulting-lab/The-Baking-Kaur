# URL Architecture

Generated 2026-07-30, BUILD-020. **No handle is renamed by this document.** Per `CLAUDE.md`'s
already-standing, deliberate decision: handle optimization (`b158`, `hamper13`, `chNN` → keyword
handles) is real SEO upside but real risk (silently breaks printed QR codes), and is explicitly
deferred until the homepage ships and duplicate drafts are archived, with an 8-step checklist. This
document works within that constraint — it defines the pattern for **new** URLs only, and flags
existing pattern violations for a future, separately-approved cleanup pass.

## 1. Current URL patterns actually in use

| Content type | Pattern | Example |
|---|---|---|
| Collections (core) | `/collections/{occasion-or-category}` | `/collections/birthday-cakes` |
| Collections (theme sub-collections) | `/collections/{theme-name}`, flat — not nested under designer-theme-cakes in the URL (Shopify collections don't nest) | `/collections/unicorn` |
| Collections (SEO/location variants) | `/collections/{keyword}-meerut` or `/collections/{keyword}` | `/collections/custom-cakes-meerut` |
| Products | Mixed — some human-readable (`motu-patlu-designer-birthday-cake-meerut`), many opaque codes per `CLAUDE.md` (`b158`, `hamper13`, `chNN`) | both patterns live today |
| Content/marketing pages | `/pages/{topic}-in-meerut` or `/pages/{topic}` | `/pages/cake-delivery-in-meerut`, `/pages/gift-hampers` |
| Legal (custom Pages) | `/pages/{policy-name}` | `/pages/refund-return-policy` |
| Legal (Shop Policies) | `/policies/{policy-type}` — Shopify-controlled, not theme-editable | `/policies/refund-policy` |

## 2. Real problems in the current pattern (found, not invented)

- **Collection URL sprawl**: 7 collections (`cakes`, `cake-delivery-meerut`,
  `same-day-cake-delivery-meerut`, `midnight-cake-delivery-meerut`, `midnight-cake-delivery`,
  `custom-cakes-meerut`, `kids-birthday-cakes-meerut`) all resolve to essentially the same ~986-item
  product set under different URLs — the collection-level equivalent of the duplicate-policy problem
  already found in `POLICY_CONSOLIDATION.md`. Google can penalize or simply ignore near-duplicate
  category pages competing for the same queries. `<<BUSINESS APPROVAL REQUIRED>>`: which of these
  (if any) stays live, since unpublishing a collection is a merchandising call, not an architecture
  one — flagged in `SITE_TREE.md` §2, not resolved here.
- **Two policy URL systems for the same topic** (`/pages/refund-return-policy` vs.
  `/policies/refund-policy`) — already fully covered in `POLICY_ARCHITECTURE.md`/
  `POLICY_REDIRECT_PLAN.md`, not repeated here.
- **A typo baked into a live handle**: `/collections/criciket` (should be "cricket") — a handle
  rename is exactly the kind of live-URL change `CLAUDE.md` says to defer; noted here as a candidate
  for the eventual handle-optimization pass, not acted on now.

## 3. Pattern for new URLs (what this BUILD actually specifies)

Every new page this architecture proposes follows the site's own already-established, working
pattern — no new convention is invented:

| New content | Pattern | Example |
|---|---|---|
| Delivery Areas hub (repurposing the unpublished Store Locator page) | `/pages/{topic}-in-meerut`, matching `cake-delivery-in-meerut` | `/pages/delivery-areas-in-meerut` |
| Per-locality delivery pages (if approved, see `LOCAL_SEO_ROADMAP.md` §6) | `/pages/cake-delivery-{locality}-meerut` | `/pages/cake-delivery-shastri-nagar-meerut` (illustrative — locality list is `<<BUSINESS APPROVAL REQUIRED>>`, see SEO-035) |
| Wedding Cakes content page (optional, see `CONTENT_PLAN.md`) | `/pages/{topic}-meerut`, matching `customised-hampers-meerut` | `/pages/wedding-cakes-meerut` |
| Corporate Gifting (already exists, unpublished) | No new URL — populate the existing `/pages/corporate-gifting-solutions` handle | — |
| Festival hamper pages (if built beyond the existing Diwali collection, see §12/Festival architecture) | `/collections/{festival}-hampers`, matching the existing `luxury-diwali-hampers` pattern | `/collections/rakhi-hampers` |
| Blog (`<<BUSINESS APPROVAL REQUIRED>>` — only if a blog is approved at all) | `/blogs/{blog-handle}/{article-handle}` — Shopify's standard pattern, not a custom scheme | `/blogs/journal/{article}` |

## 4. Canonicalization

Once `POLICY_ARCHITECTURE.md`'s canonical decisions are implemented, canonical tags for the
non-canonical policy surfaces should point at the chosen URL (already Shopify's default behavior for
most page types; verify it holds for the specific pages named in `POLICY_REDIRECT_PLAN.md`). The same
applies to any of the 7 near-duplicate collections that stay live and unpublished rather than deleted
— point their canonical tag at whichever one (if any) remains the real merchandising page, once that
business decision is made.

## Related

[SITE_TREE.md](SITE_TREE.md), [NAVIGATION.md](NAVIGATION.md), [INTERNAL_LINKING.md](INTERNAL_LINKING.md),
[POLICY_REDIRECT_PLAN.md](POLICY_REDIRECT_PLAN.md).
