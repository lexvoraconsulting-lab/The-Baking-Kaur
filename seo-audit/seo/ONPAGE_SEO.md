# On-Page SEO Audit

## Title / meta on the flagship product — spot-checked, confirmed already fixed

**Verified via Admin API** (`product(id) { title seo { title description } }` on
`motu-patlu-designer-birthday-cake-meerut`, gid `8491335712937`):

```
title:       "Motu Patlu Designer Birthday Cake"
seo.title:   "Motu Patlu Designer Birthday Cake - Eggless | Meerut"
seo.description: "Custom-designed, hand-painted to your brief. 100% eggless. From Rs.1,700. 3 sizes. Same-day & midnight delivery in Meerut."
```

This matches the H1 correctly, no mojibake, no mismatch. `CLAUDE.md`'s defect #1 (a `<title>` naming
a different, wrong cake) is **already resolved** for this product — consistent with the "All ~602
active products migrated" fact already on record. A full re-sweep across all 602 wasn't re-run this
pass (would need Admin API bulk access); this is a spot-check confirmation, not an exhaustive
re-audit.

## Occasion tag mismatch — confirmed still live

**Verified**: the same product (a birthday cake) carries the tag `anniversary` alongside
`theme cake`. Matches `CLAUDE.md`'s already-tracked ~100+ product occasion-mismatch issue. The fix
tool (`seo-ops/fix_description_occasion.py`) already exists (dry-run → CSV → `--apply` workflow) but
hasn't been run broadly — this audit didn't run it, since that's a separate, already-scoped,
already-tooled task with its own review workflow, not something to fold into this pass without a
separate go-ahead.

## Heading hierarchy

Not independently re-audited beyond what the breadcrumb/product template review already covered
(`sections/main-product-premium-v2.liquid`'s `<h1>` renders the real product title, per
`templates/product.json`'s `title` block). A full H1-H6 hierarchy sweep across every page type
would need either a live crawl (blocked by the password gate) or a template-by-template code review
not completed this pass.

## Image ALT / filename

**Requires Manual Verification** — not audited this pass. Would need either a live DOM inspection or
an Admin API sweep of product image `alt` fields across the catalogue.

## Open Graph / Twitter cards

`layout/theme.liquid` renders `{%- render 'social-meta-tags' -%}` (line 55) — the snippet itself
wasn't opened and verified this pass. Flagged for a follow-up check, not claimed as verified either
way.

## Duplicate content, keyword cannibalization, search intent matching

**Requires Manual Verification** — needs either a live crawl or a bulk content export across all 602
active products, neither performed this pass.

## Related

[../audit/VERIFIED_ISSUES.md](../audit/VERIFIED_ISSUES.md), [TECHNICAL_SEO.md](TECHNICAL_SEO.md).
