# Audit Changelog

Chronological record of what was actually deployed to the live theme (`151307485353`,
`ae86ba-2a.myshopify.com` / `thebakingkaur.com`), with the deploy-safety evidence for each.

## 2026-07-29 — Commit `52a3821`: remove fabricated ratings and fake customer reviews

**Files**: `sections/main-product-premium-v2.liquid`, `sections/main-product.liquid`,
`sections/main-product-premium.liquid`, `sections/tbk-footer.liquid`, `sections/tbk-product.liquid`.

**Issues closed**: SEO-001 through SEO-006.

**Deploy safety**:
1. `shopify theme pull --only <file>` for each file, into a scratch path.
2. `diff --strip-trailing-cr` against `git show HEAD:<path>` — zero real drift (the CLI's
   line-endings differ from git's checkout, which a plain `diff` misreports as 100% divergence;
   `--strip-trailing-cr` is required for an accurate check).
3. Edited locally, `shopify theme push --allow-live --only <file>` for all 5 files.
4. Re-pulled post-push, diffed against the edited local copies — byte-for-byte match confirmed for
   all 5 files before considering the change live.

## 2026-07-29 — Commit `eaad74f`: remove remaining unverified count claims, fix placeholder contact email

**Files**: `sections/main-product-premium-v2.liquid` (second edit), `sections/site-footer.liquid`,
`templates/page.contact-1.json`, `templates/page.contact-2.json`, `templates/page.our-store.json`.

**Issues closed**: SEO-007, SEO-008, SEO-009, SEO-010, SEO-011, SEO-012.

**Key correction this pass**: `sections/tbk-footer.liquid` (fixed in `52a3821`) turned out not to be
the live footer — `sections/footer-group.json` wires in `site-footer.liquid` instead. The real live
footer still carried the unsourced count claim; fixed here.

**Deploy safety**: identical pull → diff (zero drift) → push `--allow-live` → re-pull → diff-confirm
cycle as above, run against all 5 files in this commit.

## 2026-07-30 — Commit `4d23a2e`: remove duplicate Product schema, gate sitewide FAQPage, fix sameAs

**Files**: `snippets/tbk-schema-website.liquid`, `snippets/structured-data.liquid`,
`sections/main-product-premium-v2.liquid`, `sections/main-product-premium.liquid`,
`layout/theme.liquid`.

**Issues closed**: SEO-020, SEO-023, SEO-024.

**Drift found and reconciled before editing**: `layout/theme.liquid` had diverged from git
independent of this fix — two `render` calls added in commit `011f9be` were absent from the live
theme. Synced local to live truth for this file, then applied only the intended FAQPage-gate edit
on top, so the push carried exactly one change to this file, not an unrelated reintroduction.

**Deploy safety**: identical pull → diff (drift found + reconciled for `theme.liquid`, zero drift on
the other 4) → edit → push `--allow-live` → re-pull → diff-confirm cycle as prior commits, run
against all 5 files.

## 2026-07-30 — Commit `edf458f`: stop lazy-loading the main product gallery image

**Files**: `snippets/tbk-gallery.liquid`.

**Issues closed**: SEO-026 (Core Web Vitals). Also logged, not fixed: SEO-025 (Technical SEO, Low —
a hidden duplicate `<h1>` in `layout/theme.liquid`, needs template-by-template heading verification
before a safe removal).

**Discovery method**: `grep -rc "loading=\"lazy\""` across every section/snippet, then manually
checked whether the *first* image in each product gallery was included in that lazy-loading net —
Google's own guidance is that the LCP image should never be lazy-loaded. Found one real instance
(`tbk-gallery.liquid`, used by the "tbk" product template) and confirmed the actually-live default
template (`product-media.liquid`, all 602 active products) already handles this correctly via a
`lazy_load: false` parameter on the first media item — no fix needed there.

**Deploy safety**: pulled live copy, diffed against last commit (zero drift), pushed
`--allow-live`, re-pulled and confirmed byte-for-byte live.

## Verification queries used (for reuse once Admin API access is restored)

```graphql
# Confirm live store domain
query { shop { name } }  # via get-shop-info tool

# Confirm a collection's real product count and sample template assignments
query($id: ID!) {
  collection(id: $id) {
    products(first: 8) {
      edges { node { id title handle templateSuffix status } }
    }
  }
}

# Confirm a specific product's SEO title/description fields
query($id: ID!) {
  product(id: $id) { title seo { title description } }
}

# Confirm real product-status counts
{
  active: productsCount(query: "status:active") { count }
  draft: productsCount(query: "status:draft") { count }
  archived: productsCount(query: "status:archived") { count }
}
```

## Related

[AUDIT_LEDGER.md](AUDIT_LEDGER.md), [VERIFIED_ISSUES.md](VERIFIED_ISSUES.md).
