# Crawl Report (Phase 7.1)

Redirects, redirect chains, and broken-link status. Data source: Shopify Admin GraphQL API
(`urlRedirects`), exhaustively paginated — 825 redirects reviewed in full, not sampled.

## Redirect inventory

**825 total redirects** at the start of this pass (verified via `urlRedirectsCount`). Overwhelming
majority are legitimate: old numeric/legacy product handles → `/collections/cakes` (bulk-migration
cleanup), old `-in-meerut-the-baking-kaur`-suffixed handles → their shorter renamed equivalents,
old product handles → the most relevant surviving collection, `?variant=...`/`?country=...`
parameter URLs from since-removed products' old cart/share links → the relevant collection, and a
handful of legacy `/pages/*` routes (`terms`, `privacy-policy`, `faq`, `about`, `careers`, etc.) →
either their current equivalent or the homepage.

## Redirect chains — FOUND and FIXED

Two confirmed multi-hop redirect chains, found by cross-referencing all 825 `path`/`target` pairs
against each other (not sampling):

### Chain 1: `theme-cakes-1` → `theme-cakes` → `designer-theme-cakes`

- **Before**: `/collections/theme-cakes-1` → `/collections/theme-cakes` → `/collections/designer-theme-cakes`
  (2 hops for any visitor/crawler hitting the first URL).
- **Fixed**: `/collections/theme-cakes-1` now points directly to `/collections/designer-theme-cakes`
  (1 hop). `/collections/theme-cakes`'s own redirect (→ `designer-theme-cakes`) was left untouched
  — it's still needed as a valid single-hop redirect for anyone hitting that URL directly.
- **Redirect ID changed**: `gid://shopify/UrlRedirect/358221906089`.

### Chain 2: 24 product redirects → `flowers` → `cake-hampers`

- **Before**: 24 separate product-handle redirects all targeted `/collections/flowers`, which was
  itself a redirect to `/collections/cake-hampers` — every one of those 24 was a silent 2-hop chain.
  Found via a systematic Admin API query (`urlRedirects(query: "target:/collections/flowers")`),
  not manual sampling — this method surfaced 24 entries, one more than an initial manual read of
  the paginated data had counted, demonstrating why systematic verification (not eyeballing) matters
  here.
- **Fixed**: all 24 now point directly to `/collections/cake-hampers` (1 hop each).
  `/collections/flowers`'s own redirect (→ `cake-hampers`) was left untouched, same reasoning as
  above.
- **Redirect IDs changed** (24 total): `355797598377`, `355797794985`, `358211813545`,
  `358212075689`, `358213451945`, `358213517481`, `358213877929`, `358214271145`, `358214500521`,
  `358214566057`, `358214992041`, `358215090345`, `358215155881`, `358215188649`, `358215221417`,
  `358215254185`, `358215319721`, `358215352489`, `358215385257`, `358215581865`, `358215614633`,
  `358215712937`, `358217089193`, `358217154729`.

## Verification performed

- **Before**: fresh `urlRedirects` query confirmed each chain's exact current state immediately
  before mutating — no IDs guessed, all fetched live.
- **User approval obtained**: the auto-mode classifier flagged the bulk live-redirect mutation for
  explicit confirmation before executing (a real production change to live traffic routing, not a
  theme-file deploy) — approval was requested and given before any mutation ran.
- **Mutation**: `urlRedirectUpdate`, executed in 4 batches (≤8 per batch, per this project's
  established Admin API batching convention), 25 total mutations, **zero `userErrors`** across all
  batches.
- **After**: re-queried `path:/collections/theme-cakes-1` (now → `designer-theme-cakes`, confirmed)
  and `target:/collections/flowers` (zero results — confirms no redirect anywhere still creates a
  chain through that collection).

## Not verifiable this pass (password gate)

- Live HTTP status of any redirect (whether Shopify actually serves a 301/302 as expected) — the
  Admin API confirms the redirect *record* is correct; confirming the *served* HTTP behavior
  requires a live request, blocked by the password gate.
- Site-wide broken-link (404) detection — requires crawling the live rendered site.
- Soft-404 detection — same constraint.

## Recommendation for Phase 7.2 / once unlocked

Re-run a live crawl (e.g., Screaming Frog or equivalent) once the storefront is reachable, to
confirm the fixed redirects serve correctly and to catch any 404/broken-link issue this Admin-API-
only pass couldn't reach.

## Related

[TECHNICAL_SEO_AUDIT.md](TECHNICAL_SEO_AUDIT.md), [SEO_CHANGELOG.md](SEO_CHANGELOG.md),
[URL_ARCHITECTURE.md](URL_ARCHITECTURE.md).
