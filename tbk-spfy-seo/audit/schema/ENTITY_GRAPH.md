# Entity Graph

Documentation-only observation of how `@id` values cross-reference each other across the theme's
schema files — not a fix, just a map, since untangling it is a design decision (see "Open question"
below), not a mechanical correctness bug.

## The canonical anchor: `https://thebakingkaur.com/#organization`

Defined once, in `snippets/tbk-schema-website.liquid`, and correctly *referenced* (not redefined) by:

```
tbk-schema-website.liquid   → defines #organization (Organization)
                            → defines #website (WebSite), references #organization as publisher
tbk-schema-article.liquid   → references #organization as author AND publisher
sections/main-product.liquid → references #organization as seller (both at Product level and
                                nested inside the Offer)
```

This is exactly the correct pattern — one canonical entity, referenced by `@id` everywhere else,
never redefined with different data in different files.

## Where the graph doesn't connect: `Bakery` (LocalBusiness)

`snippets/bk-local-business.liquid`'s `Bakery` entity has **no `@id` at all** — verified by
`grep -n "@id" snippets/bk-local-business.liquid`, zero matches. This means:

- It's a floating, unreferenced node in the overall graph — nothing points to it, and it doesn't
  point to `#organization`, even though both entities describe the same real business.
- A knowledge-graph consumer (Google, an AI crawler) has to infer from matching `name`/`url`/`telephone`
  fields that `Bakery` and `Organization` are the same entity, rather than being told so explicitly
  via a shared or cross-referenced `@id`.

## Open question (not resolved here — a design decision, not a bug)

Should `bk-local-business.liquid`'s `Bakery` entity either (a) reuse
`https://thebakingkaur.com/#organization` as its own `@id` (making it the *same* node, just
described with additional Bakery-specific properties), or (b) get its own `@id` (e.g.
`#localbusiness`) with an explicit `sameAs` or `subOrganization`-style link back to `#organization`?
Both are valid schema.org patterns; picking one is a design call for whoever owns the schema
architecture next, not something this audit pass decided unilaterally.

## Other entities without `@id` (checked, and why that's fine)

`Product` schema in `main-product-premium-v2.liquid`/`main-product-premium.liquid` before their
removal (SEO-023) — n/a now, removed. `FAQPage` (`layout/theme.liquid`) — no `@id`, which is
standard/acceptable for a page-level entity that isn't referenced elsewhere in the graph.

## Related

[SCHEMA_AUDIT.md](SCHEMA_AUDIT.md), [SCHEMA_VALIDATION.md](SCHEMA_VALIDATION.md).
