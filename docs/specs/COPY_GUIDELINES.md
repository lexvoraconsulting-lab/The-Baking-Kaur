# Copy Guidelines

**Canonical hierarchy**: `business/BUSINESS_MASTER.md` → `business/TBK_BRAND_GUIDELINES.md` →
`DESIGN_SYSTEM.md`/`COMPONENT_LIBRARY.md`/`CONTENT_SYSTEM.md` → this document. This document adds
line-level copy mechanics; `TBK_BRAND_GUIDELINES.md` §1 (Tone of Voice, Writing Style, Messaging
Rules) is the authority on brand voice and is not repeated here beyond direct citation.

---

## Tone

See `TBK_BRAND_GUIDELINES.md` §1 in full. One-line summary for quick reference: warm but precise,
confident without inflating, second-person and direct, no exclamation-heavy marketing register — all
derived from the real, already-published copy voice, not invented.

## Grammar

- Second person ("you," "your celebration") in customer-facing copy — matches the real, established
  voice across FAQ/delivery/eggless pages.
- Short declarative sentences preferred over compound marketing sentences (e.g. the real FAQ answer
  "Yes. Every cake we bake is 100% eggless" — a direct answer, not a qualified one).
- Contractions are acceptable and already present in real copy ("it isn't a separate range").

## Capitalization

- Page **titles**: Title Case (real examples: "Cake Delivery in Meerut – Same-Day, Midnight & Express
  Service," "30-Minute Cake Delivery in Meerut – Premium & Reliable Service").
- Body headings (H2/H3) and FAQ questions: Sentence case (real example: "Frequently asked questions,"
  "Are all your cakes eggless?").
- Do not introduce a third capitalization convention for any new heading level.

## Product Naming

Real, established pattern for product titles: `{Descriptor} {Theme/Occasion} Cake` (e.g. "Motu Patlu
Designer Birthday Cake," "White Love Designer Anniversary Cake"). SEO title suffix is separate from
the on-page product title — see SEO Writing below. Do not introduce unverifiable superlatives into a
product name itself (e.g. "Best-Selling," "#1") unless traceable to real data.

## Collection Naming

Real, established pattern: `{Occasion/Theme} Cakes` for core collections (Birthday Cakes, Anniversary
Cakes, Wedding Cakes), or a short theme name for sub-collections (Unicorn, Butterfly, Teddy). Avoid
creating a new collection name that duplicates an existing collection's actual product set under
different wording — `BUSINESS_MASTER.md` §11 already documents 7 such near-duplicates (B5,
unresolved); don't add an 8th.

## SEO Writing

- Product SEO title: `"{Name} - Eggless | Meerut"`, or `"{Name} | Meerut"` if the first form exceeds
  60 characters — the real, already-migrated standard covering ~602 active products (`CLAUDE.md`).
- Meta description: type-specific, hooked, present per product (real, already-migrated pattern).
- Never state a rating, review count, or "years in business" figure in SEO copy — see Messaging Rules
  in `TBK_BRAND_GUIDELINES.md` §1; this has already caused fabricated-content removals three times on
  this project.

## AI Writing

Any AI-assisted or AI-generated copy (product descriptions, FAQ answers, landing-page drafts) must
follow every rule in this document and `TBK_BRAND_GUIDELINES.md` §1/§5 exactly — AI-generated content
is not exempt from the verifiability standard. Specifically:

- Never let an AI system state a number not traceable to `BUSINESS_MASTER.md`.
- Never let an AI system draft refund/cancellation/shipping-specific wording while B1 is unresolved.
- Never let an AI system draft a delivery-area claim naming specific localities while B4 is
  unresolved — use only the verified radius/minimum-order facts (~15 km, ₹350) that aren't in
  conflict.
- Prefer citing the real, existing FAQ page's own phrasing as the canonical answer to a question,
  rather than re-generating a fresh answer that might drift from the established voice or facts.

## CTA Rules

- Primary CTA verb should be concrete and specific to the action (e.g. "Browse Hampers," "Message Us
  on WhatsApp") rather than generic ("Click Here," "Learn More") — matches the real pattern already
  used across delivery/hamper pages' closing paragraphs.
- Every CTA must resolve to a real, live URL — this project's own audit found and fixed multiple
  broken/mistargeted CTA links this year (broken `tel:`/`wa.me` hrefs, footer links pointing at an
  unpublished draft page); re-verify any new CTA target before publishing.
- Use `{% render 'tbk-button' %}` for any button-styled CTA (`DESIGN_SYSTEM.md`) — never hand-roll new
  button markup for a one-off CTA.

## Error Messages

Real, established pattern: `.hdt-form-message--error` / `.hdt-form__message-wrapper` classes
(`snippets/form-status.liquid`, `snippets/buy-buttons.liquid`) render Shopify's native form error
text via `form.errors.messages`. New forms should surface errors through this same real mechanism
rather than a custom error-copy system. No standalone "error message copy style guide" (tone,
phrasing conventions for custom validation messages) exists yet —
**`DESIGN APPROVAL REQUIRED`** if one is wanted beyond Shopify's native error text.

## Microcopy

Real examples already in use: WhatsApp button label "💬 WhatsApp" (sticky button, sitewide); FAQ's
"Still have a question?" CTA block heading; footer trust-pill pattern that renders **only** when a
merchant setting is filled in (never a placeholder string). New microcopy should follow this same
"real value or nothing" discipline — never insert a placeholder string like "Coming soon" or "TBD" in
customer-facing copy without it being clearly a construction-in-progress signal, not a claim.

## Trust Statements

**The single highest-risk copy category on this project.** Every trust statement must trace to
`BUSINESS_MASTER.md` §10 exactly. Currently safe to state: 100% eggless (as standard, not
substitution), made-to-order/fresh-baked, single-location Meerut studio, real verified social
profiles (Instagram/Facebook). **Currently unsafe to state** (no real data exists): any rating, any
review count, any specific customer count, "years in business," FSSAI number, GST number, any award
or press mention. This list is not exhaustive — when in doubt, check `BUSINESS_MASTER.md` §10 before
publishing any new trust statement, and mark it `BUSINESS APPROVAL REQUIRED` if it isn't already
listed there as Confirmed.

---

## What this document does not do

No copy is written or published by this document — it is a style/mechanics reference. Every rule
traces to either a real, observed pattern in already-published copy, or a documented gap requiring
approval before new copy in that category is written.

## Related

[../business/BUSINESS_MASTER.md](../business/BUSINESS_MASTER.md),
[../business/TBK_BRAND_GUIDELINES.md](../business/TBK_BRAND_GUIDELINES.md),
[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md), [COMPONENT_LIBRARY.md](COMPONENT_LIBRARY.md),
[CONTENT_SYSTEM.md](CONTENT_SYSTEM.md), [../REVIEW_STRATEGY.md](../REVIEW_STRATEGY.md).
