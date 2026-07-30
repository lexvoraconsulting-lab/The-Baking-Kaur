# E-E-A-T Audit — Experience, Expertise, Authoritativeness, Trust (SEO-016 family)

Generated 2026-07-30. Every claim below is checked against what's actually live (theme pull, Admin
API, or repo grep) — no scoring of hypothetical future content, and no invented gaps beyond what was
directly observed.

## About / Brand Story

Live page: `/pages/about-us` ("About The Baking Kaur | Premium Eggless Bakery in Meerut").

- Real content: positions the business as a Meerut-based luxury/custom/wedding cake studio, made-to-
  order, premium ingredients, personalised consultation. No fabricated claims found on this page.
- **Minor technical defect**: the page's HTML carries leftover `data-start="..." data-end="..."`
  attributes on nearly every element — artifacts of a copy-paste from an AI writing tool, not
  rendering-breaking but unprofessional if a customer views page source or a scraper surfaces the
  raw markup. Cosmetic; low priority.
- **No specific brand story**: no founding narrative, no "why we started," no specific year or
  origin story. Reads as competent generic bakery copy rather than a distinctive brand story.

## Founder / Named Individual

**No named founder, owner, or head baker appears anywhere** — not on the About page, not on Contact,
not in any schema, not in any live page fetched this session. For a single-location, owner-operated
business, a named, identifiable person (with at least a first name, ideally a short bio/photo) is one
of the strongest, cheapest E-E-A-T signals available and is currently entirely absent. This is a
content gap, not a fabrication risk — recommend the business decide whether to name a founder
publicly.

## Experience / Expertise (years in business, specialisation)

- No live page states a founding year or "X years of experience." `AUDIT_LEDGER.md` (SEO-014) already
  tracked a "Since 2018" claim in `sections/footer.liquid` — confirmed **not live** (dead code, not
  wired into `footer-group.json`), so it correctly carries no weight here either way.
  the business.
- Specialisation claims (wedding cakes, designer/theme cakes, 100% eggless) are consistent and
  repeated across multiple independent live pages (About, Eggless, Gift Hampers, delivery pages) —
  this consistency itself is a positive expertise signal, not a fabricated one.

## Trust Signals

| Signal | Status |
|---|---|
| Verified reviews | **None.** Real Admin API counts (113 customers, 24 orders) confirm no meaningful review volume exists; S5 Social Proof section is built but renders nothing (per `CLAUDE.md`, already known). |
| Star ratings | Resolved this session — see `AUDIT_LEDGER.md` SEO-001–009, SEO-016: fabricated "4.8/4.9" ratings and fake testimonials found and removed in prior commits; the header claim (SEO-016) is now confirmed already-clean, not fabricated. |
| Social profiles | Real, verifiable `sameAs` links to `instagram.com/thebakingkaur` and `facebook.com/thebakingkaur` in both schema files — a genuine, checkable trust signal. |
| Business identity (name) | **Inconsistent on a legal document** — see below. |
| FSSAI | Claimed ("FSSAI-licensed kitchen") on the live eggless page and elsewhere, **no licence number given anywhere**. Already tracked in `CLAUDE.md`'s "Blocked on the client" section — unresolved, needs the real number from the business. |
| GST | **No GST/GSTIN number found anywhere** in the theme, pages, or schema. Not necessarily a defect — on-site GSTIN disclosure isn't universally required for a D2C storefront — but flagged since it was explicitly in scope for this audit. Confirm with the business whether GST registration exists and whether it should be surfaced (e.g., on invoices, footer, or a legal page). |
| Awards / press / certifications | **None found.** No press mentions, no award badges, no "as seen in" anywhere in the live theme or pages. |

## Business Identity — a real, live inconsistency found this pass

The business name renders as **"The Baking Kaur"** consistently across every theme file, page, and
schema block checked — except three of Shopify's own built-in Shop Policies (Refund, Shipping, Terms
of Service; see [POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md)), which all say **"The Bakery
Kaur."** A live legal document with the wrong business name is a direct, checkable E-E-A-T and
trust-signal defect — it's exactly the kind of small inconsistency that undermines "is this a real,
carefully-run business" signals for both users and Google. Fixing it is bundled into the
POLICY_CONSOLIDATION.md recommendation, since it lives in the same documents already flagged for a
content rewrite.

## Contact Information

Real, working, and improved this session (the Contact page's `tel:`/WhatsApp links were broken —
`href="tel:+91"` with no digits, `wa.me/91` with no number — both fixed and deployed live this pass).
The remaining contact-info issue is the address-text/coordinate inconsistency, fully detailed in
[ADDRESS_AUDIT.md](ADDRESS_AUDIT.md) rather than repeated here.

## Summary — where this business's E-E-A-T stands

**Real strengths**: consistent specialisation story across independent pages, genuine (if small)
social presence, no remaining fabricated ratings/reviews as of this session, working contact channels.

**Real gaps, in priority order**:
1. Wrong business name on 3 live legal documents (Business Identity) — mechanical fix once the
   canonical refund/terms text is decided (see POLICY_CONSOLIDATION.md).
2. No named founder/owner anywhere (Experience/Authoritativeness) — business decision, not a defect.
3. FSSAI claimed without a licence number (Trust) — already tracked, blocked on the client.
4. No GST number surfaced anywhere (Trust) — confirm with business whether this matters for this
   storefront.
5. Zero verified reviews (Trust) — already tracked as blocked on the client (needs 3 real reviews to
   activate the built Social Proof section).
6. No brand story beyond generic positioning (Experience) — lowest priority, a content opportunity
   rather than a defect.

## Related

[POLICY_CONSOLIDATION.md](POLICY_CONSOLIDATION.md), [ADDRESS_AUDIT.md](ADDRESS_AUDIT.md),
[../audit/AUDIT_LEDGER.md](../audit/AUDIT_LEDGER.md).
