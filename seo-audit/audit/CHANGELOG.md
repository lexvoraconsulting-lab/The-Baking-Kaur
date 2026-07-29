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
