# Structured Data & Schema Report (Phase 7.3, partial — stopped on business decision)

> **Update (Phase 7.4, 2026-07-31): the FAQPage finding below is resolved** — the block was removed
> entirely from `layout/theme.liquid` (approved decision: remove rather than restrict/build matching
> content). The FAQ pages' own accordion sections already carry correct, independent Microdata, so
> removal created zero schema-coverage gap. See `seo-audit/audit/CHANGELOG.md` (Phase 7.4 entry).

Continues from Phase 7.2 (`docs/SHOPIFY_SEO_REPORT.md`, commit `f8269f3`). Per "never repeat
previous work," this does not re-run Phase 6's full schema audit (`docs/AEO_READINESS.md`,
`docs/GEO_READINESS.md`) — it verifies current state and resolves/investigates the specific open
items that audit left flagged.

## Confirmed sound, no action needed

- **`SearchAction`** present in `snippets/tbk-schema-website.liquid` — sitelinks search box
  eligibility already satisfied (this was Phase 6.5's open task M-3; confirmed done, closing it).
- **Canonical schema sources** (per root `CHANGELOG.md`'s own tracking table, re-verified):
  Organization+WebSite → `tbk-schema-website.liquid`; Bakery/LocalBusiness →
  `bk-local-business.liquid`; BreadcrumbList → `tbk-schema-breadcrumb.liquid`; Product/Article
  (native) → `structured-data.liquid`. No duplicate entities found across any of these — consistent
  with the Phase A schema-dedup work (`77861b3`, verified live in Phase 7.0).

## Real, still-open finding: global FAQPage schema doesn't match visible content on most pages

**Evidence**: `layout/theme.liquid:79` gates a 9-question `FAQPage` JSON-LD block with
`{%- unless template.suffix == 'faq-01' or template.suffix == 'faq-02' -%}` — i.e., it renders on
**every page except the two dedicated FAQ pages**. The 9 questions (delivery timing, hampers,
wedding setups, theme cakes, WhatsApp ordering, pickup) are real business facts, not fabricated —
but no visible accordion, FAQ section, or equivalent on-page Q&A content matching these 9 specific
questions was found anywhere outside the two FAQ page templates themselves (checked
`sections/site-footer.liquid` — only 6 unrelated keyword mentions, not this Q&A content).

**Why this is a real problem, not resolved by the prior fix**: the existing in-code comment
(labeled `SEO-024`) explains the *original* bug was this FAQPage block "rendering unconditionally
on every page... regardless of whether that page shows this Q&A content — a violation of Google's
structured-data guideline that markup must match visible on-page content." The fix applied
(excluding the two FAQ page templates) only solved the **duplication** half of that problem — it
stops the schema from clashing with the FAQ pages' own accordion-based FAQPage markup. It does
**not** solve the **mismatch** half: the schema still renders, with the same 9 questions, on the
homepage, every one of the ~602 active product pages, every collection page, and every other page
type — none of which visibly display this Q&A content.

**Why not fixed in this pass**: resolving this requires a genuine choice between (a) removing the
global block entirely (loses whatever AI-answer-extraction/rich-result value it provides on
non-FAQ pages, if any), or (b) restructuring it to only render where matching visible content
exists (a real theme-code change to rendering logic, not a metadata tweak). Both are judgment calls
with real trade-offs — not a deterministic technical fix. Per this phase's own stop condition
("stop only if... business approval is required"), this is exactly that case.

## Stopping Phase 7.3 here

Per the explicit instruction to continue automatically "unless a hard blocker exists" and to "stop
only if... business approval is required" — this finding qualifies. Recommend surfacing to the
business/product owner: **keep the global FAQPage schema as-is (accept the visible-content
mismatch as a known, low-severity risk), remove it from non-FAQ pages, or build matching visible
FAQ content on a wider set of pages** (a content decision, separate from the schema question
itself).

## Related

[SHOPIFY_SEO_REPORT.md](SHOPIFY_SEO_REPORT.md), [AEO_READINESS.md](AEO_READINESS.md),
[GEO_READINESS.md](GEO_READINESS.md).
