# Tasks

Lightweight work tracking for The Baking Kaur.

## Convention

- **Open work** lives as checklist items below, grouped by area. Keep each item one line with enough context to act (file paths, IDs).
- When an item is done, either check it off with the completion date or move it to a `done/` note — TODO: pick one once volume warrants; for now, check off in place.
- Larger initiatives are the blueprint **phases** in `../VERSION.md` / `../PROJECT_ROADMAP.md`; don't duplicate them here, link to them.

## Open — SEO / catalog (owner: automated tooling + review)

- [ ] Finish the description **occasion-mismatch** fix across the catalogue (~100+ products beyond Baby Girl). Tool ready: `../seo-ops/fix_description_occasion.py` (dry-run → review CSV → `--apply`). Needs `SHOPIFY_TOKEN` set, or continue via the MCP path.
- [ ] Review the hardcoded price range ("from Rs.1,700 to Rs.2,900") that appears in every generated description — verify against real per-product min/max and correct where wrong. TODO: confirm scope.
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

TODO: this list is reconstructed from session history; reconcile against `CHANGELOG.md` for anything missing.
