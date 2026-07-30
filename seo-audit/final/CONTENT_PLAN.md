# Content Briefs

Generated 2026-07-30. These are **briefs** — structure, angle, and real facts to build from — not
finished copy. Per the project's standing principle (`CLAUDE.md`), no brief invents a business fact;
each one flags where real input (a photo, a number, a policy decision) is still needed before the
page can actually be written or rebuilt.

## Homepage

Blocked on two open items already tracked in `CLAUDE.md`: the hero is a temporary product shot
(photography blocked on the client), and S8 Trust is gated on FSSAI number or real reviews. Brief for
when those unblock:
- Lead with the single clearest differentiator that's actually verifiable today: 100% eggless as
  standard practice (not a substitution), same-day/midnight delivery in Meerut, made-to-order.
- Do **not** lead with a customer count, rating, or "trusted by X" claim — none exist yet (see
  `EEAT_REPORT.md`).
- Once P0 photography lands, replace hero copy references to a "temporary product shot" framing.

## Collections (Birthday, Anniversary, Wedding, Designer/Theme, Hampers)

- Each collection page should link to the single most relevant delivery page (e.g. Birthday →
  same-day delivery, Wedding → the venue-setup FAQ) — currently these collections aren't
  cross-linked into the delivery content at all (see `LOCAL_SEO_ROADMAP.md` §7).
- Collection descriptions were already trimmed from "walls of text" per `CLAUDE.md` — keep new
  additions short, don't reintroduce length.

## Products

- No brief-level change recommended beyond what's already tracked: the SEO title/description
  migration is done for ~602 active products (`CLAUDE.md`), and the occasion-mismatch fix
  (`seo-ops/fix_description_occasion.py`) is the open item, not a new content brief.

## Blogs

**No blog exists on this storefront** — no blog template, no blog page found in the Admin pages query
this session ran. Before briefing blog content, confirm with the business whether a blog is even
planned; if not, this line item should be dropped rather than speculatively planned.

## FAQ (shipped this session, SEO-013)

Now live with 19 real, grounded topics (see `seo-audit/audit/CHANGELOG.md`). Next content step, not
done this pass: cross-link the FAQ page from the delivery/hamper pages (`LOCAL_SEO_ROADMAP.md` §8).

## Delivery Areas

Full brief already exists: [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md) — this is that page's
content specification, ready to write once the two open gaps (confirmed area list, confirmed express
cutoff) are settled.

## Wedding Cakes

Real material already exists and is scattered rather than consolidated: About Us ("bespoke wedding
cakes," "luxury wedding cakes in Meerut") and the sitewide FAQ's venue-setup answer
(`layout/theme.liquid`). Brief: a dedicated Wedding Cakes landing page could consolidate these two
already-real facts plus link to the wedding-cakes collection — no new facts needed to start this,
only a business decision on whether it's worth a dedicated page versus relying on the collection page.

## Birthday Cakes

Already has strong real material across 3 live pages (cake-delivery-in-meerut, 30-minute delivery,
midnight delivery) — birthday is the most-covered occasion in the existing content. Brief: if a
dedicated Birthday Cakes content page is wanted beyond the collection page itself, it can be
assembled almost entirely from already-published sentences on those 3 pages; low content-creation
cost relative to other briefs here.

## Corporate Orders

Real material exists on the Gift Hampers page ("Corporate Gifting Solutions" section) but the
dedicated `/pages/corporate-gifting-solutions` page is **unpublished with an empty body** — a stub.
Brief: before writing this page, get from the business: (1) any minimum order size/lead time for
corporate orders, (2) whether invoicing/GST matters for corporate clients (ties to `EEAT_REPORT.md`'s
open GST question), (3) any real example of a corporate client relationship that can be referenced
(even anonymized) to make the page more credible than generic "we do corporate gifting" copy.

## Hampers

Best-covered content on the entire site already — `/pages/gift-hampers` is thorough, real, and needs
no rewrite. Brief: this page is a good template for the eventual Wedding Cakes and Corporate Orders
pages above, structurally (occasion list → contents list → customization note → delivery note →
related collections).

## Cross-cutting rule for every brief above

Nothing here should ship with a rating, review count, customer count, "years in business," or
award/press claim unless it's independently verified first — this is the same standard the rest of
this audit pass applied, and it's the one that's already caused real content removals on this project
(`CLAUDE.md`: "this has already caused three removals; assume it will cause more").

## Related

[LOCAL_SEO_ROADMAP.md](LOCAL_SEO_ROADMAP.md), [DELIVERY_AREA_SPEC.md](DELIVERY_AREA_SPEC.md),
[EEAT_REPORT.md](EEAT_REPORT.md).
