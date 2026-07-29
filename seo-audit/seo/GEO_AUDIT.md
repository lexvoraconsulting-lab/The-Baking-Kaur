# GEO / AI Search Readiness Audit

Generative Engine Optimization — how well this storefront's content and markup can be discovered,
parsed, and cited by AI search systems (Google AI Overview, ChatGPT, Perplexity, etc.). No claim
below is estimated from general SEO theory alone where the codebase gave a direct, checkable answer.

## Structured data (the backbone of machine readability)

**Verified strong.** See [../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md) in full — WebSite,
Organization, Bakery/LocalBusiness, BreadcrumbList, CollectionPage, Product (native Shopify), and
Article schema are all present, dynamic, and free of fabricated fields. This is a genuinely solid
foundation for AI crawlers and citation systems to parse entity relationships correctly.

## FAQPage schema and question coverage

**Critical, verified gap (SEO-013).** `FAQPage`-style accordion schema exists in
`sections/accordion.liquid`/`accordion_inline.liquid`, and two real page templates
(`page.faq-01.json`, `page.faq-02.json`) actually use it — but both currently render **Lorem Ipsum
placeholder text**, 12 instances each, not real answers. This is worse than having no FAQ page at
all for AI-search purposes: a well-formed `FAQPage` schema block containing gibberish is a strong,
structured signal pointing an AI crawler at nonsense, which actively damages citation trust rather
than merely failing to build it. **This is the single highest-priority GEO fix**, and it requires
real business content (see [../audit/MANUAL_VERIFICATION.md](../audit/MANUAL_VERIFICATION.md)) —
not something to invent.

## Entity graph consistency

**SEO-020 (open, Low)**: the Organization entity's `sameAs` (Instagram only) and the Bakery entity's
`sameAs` (Instagram + Facebook) describe the same real-world business inconsistently across two
schema sources. Small, but entity-graph consistency is exactly what AI knowledge-graph matching
depends on — worth reconciling once someone confirms the canonical current social profile list.

## Brand mention strength / AI citation readiness

**Requires Manual Verification** — this needs testing actual AI systems (asking ChatGPT/Perplexity/
Gemini about "eggless cake Meerut" and seeing if/how this brand surfaces), which is an external,
ongoing measurement, not something a code audit can determine directly. Not attempted this pass.

## Chunkability / semantic blocks / answerability

Content structure (headings, breadcrumbs, schema) supports this reasonably well where real content
exists (product pages, once SEO-006's fake-review removal and the header decision land). The FAQ
gap (SEO-013) is the main structural blocker — once real, well-chunked Q&A content exists there, the
schema plumbing to expose it to AI crawlers is already built and correct.

## Related

[../schema/SCHEMA_AUDIT.md](../schema/SCHEMA_AUDIT.md), [../audit/VERIFIED_ISSUES.md](../audit/VERIFIED_ISSUES.md).
