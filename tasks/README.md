# Tasks

Lightweight work tracking for The Baking Kaur.

## Convention

- **Open work** lives as checklist items below, grouped by area. Keep each item one line with enough context to act (file paths, IDs).
- When an item is done, either check it off with the completion date or move it to a `done/` note — TODO: pick one once volume warrants; for now, check off in place.
- Larger initiatives are the blueprint **phases** in `../VERSION.md` / `../PROJECT_ROADMAP.md`; don't duplicate them here, link to them.

## Open — SEO / catalog (owner: automated tooling + review)

- [ ] Product images: add stills to the 2 drafted products (Velvet Crown, Handcrafted) and ~9 video-only products, then reassess status. *Blocked on client photos.*
- [ ] Variant option typos (`fruit-cocoktail`, `chocolate-moouse`, `lotus-biscoffStrawberry Vanila`) — deliberately untouched; need a metaobject fix first (variant-surgery risk).

## Open — needs the client / manual (not automatable here)

- [ ] Google Search Console → **Validate Fix** on "Not found (404)" and "Soft 404" rows (root causes cleared; this just re-triggers Google's crawl).
- [ ] Set `SHOPIFY_TOKEN` in the shell if the `seo-ops` scripts are to run directly instead of via MCP.

## Open — blueprint phases (see ../PROJECT_ROADMAP.md)

- [ ] Promote **Phase A** (footer restore + schema dedup) from preview to the live theme.
- [ ] Act on the **collection audit** dispositions (redirects / merges / populate).
- [ ] Phases **B–J**: design foundation, homepage build, collections redesign, header/footer, SEO/GEO completion, missing pages, performance (Lighthouse 95+, CWV), accessibility (WCAG 2.2 AA), analytics.

## Recently done (2026-07)

- [x] Migrated SEO snippets on all ~602 active products.
- [x] Trimmed 8 bloated collection descriptions; added intros to 14 empty ones.
- [x] Published 5 landing pages (eggless, midnight, photo, theme, 30-min).
- [x] Fixed broken Product JSON-LD (`| json`) and deployed to live theme.
- [x] Corrected occasion mismatch on the Baby Girl collection (18 products).
- [x] Finished the description occasion-mismatch fix catalogue-wide (2026-08-01, Phase 7.7): 70 more products fixed live, 0 remaining.
- [x] Reviewed the hardcoded-looking price range in generated descriptions (2026-08-01) — checked all 1,235 products (not just active): 893 carry a "from Rs.X to Rs.Y" sentence, and every single one matches the product's real `priceRangeV2` min/max exactly. Not a defect; no fix needed.

TODO: this list is reconstructed from session history; reconcile against `CHANGELOG.md` for anything missing.
