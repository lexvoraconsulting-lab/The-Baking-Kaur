# Requires Manual Verification

Issues where the underlying question is real, but answering it needs something this audit didn't
have this session: a business fact, a reconnected tool, or an external service. Listed here instead
of guessed at.

## Needs a business fact

| ID | Question | Why it can't be answered here |
|---|---|---|
| SEO-013 | What are the real FAQ answers (refund policy, delivery cutoffs, etc.)? | Writing plausible-sounding answers would be fabrication, the exact thing this audit exists to catch |
| SEO-014 | Is "Since 2018" the real founding year? | No access to business incorporation/founding records |
| SEO-015 | Is the Google Maps pin at lat 28.9931, long 77.6939 actually correct for Fatah Complex, Thapar Nagar Lane 7, Meerut? | No Google Maps access; the original author already flagged this in-code as unverified |

## Needs the Shopify Admin API (MCP `claude.ai Shopify` server disconnected mid-session)

| ID | Question | What reconnecting would answer |
|---|---|---|
| SEO-017 | Which of `page.contact-1.json`, `page.contact-2.json`, `page.our-store.json`, `page.faq-01.json`, `page.faq-02.json` is actually assigned to a live page? | Confirms true urgency of SEO-013 and whether SEO-010/011/012 reached a real page, or fixed dead code defensively |
| SEO-018 | What is the real, current customer/order count? | Could let a sourced number replace the unsourced "20,000+" claims removed in SEO-007/008/009, rather than leaving the space empty |
| SEO-003, SEO-005 | Is any published product assigned `templateSuffix: "premium"` or `"tbk"`? | Confirms whether those two fixes patched live-rendering pages or defensive/dead-code cleanup |

## Needs the site to be publicly reachable (currently password-gated, confirmed intentional)

| ID | Question |
|---|---|
| SEO-019 | Is `sitemap.xml`'s 404 caused solely by the password gate, or a separate misconfiguration? |
| — | Core Web Vitals, real Lighthouse/PageSpeed scores — not measurable against a gated site |
| — | Real Google Search Console / Google Business Profile data — no API access this session |

## How to close these out

1. Reconnect the Shopify MCP server, then re-run the `graphql_query` checks for SEO-017/018 (see
   [../../CHANGELOG.md](CHANGELOG.md) for the exact queries already used earlier in this audit).
2. Ask the business for real FAQ content, founding year, and current customer/order figures if they
   want SEO-013/014/018 resolved with real numbers rather than left blank.
3. Re-check SEO-019 the moment the password gate lifts, before assuming it's fixed by that alone.

## Related

[AUDIT_LEDGER.md](AUDIT_LEDGER.md), [VERIFIED_ISSUES.md](VERIFIED_ISSUES.md).
