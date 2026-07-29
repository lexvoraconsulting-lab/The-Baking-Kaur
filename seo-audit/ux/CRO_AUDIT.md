# CRO Audit

## Scope limitation

Same constraint as [UX_AUDIT.md](UX_AUDIT.md): the storefront is intentionally password-gated, so
no real conversion-flow testing (add-to-cart, checkout, form completion) was possible this pass.
Nothing below is a live-tested conversion finding — code-level observations only.

## Trust-to-conversion chain — directly relevant to this session's fixes

The removed fabricated trust signals (SEO-001 through SEO-009) sat directly adjacent to the buy
button and product promise block — i.e., exactly the CRO-critical zone. Removing unverifiable claims
from that zone without replacing them with anything is a short-term conversion-neutral-to-negative
trade (a badge, even a fake one, "does something" for a casual visitor's confidence) — but shipping
verifiable trust signals in their place (a real review count, a real FSSAI number, a linked GBP
rating) would very likely outperform the fabricated versions once available, since a discovered
fake claim (via a manual action, a customer noticing invented reviews, etc.) does far more
conversion damage than a temporarily sparser trust block. This is a judgment call, not a measured
result — flagged as **Estimated**, not Verified.

## FAQ gap's conversion angle

SEO-013 (Lorem Ipsum on both FAQ page templates) isn't just an SEO problem — an FAQ page a customer
actually opens (to check a return policy, delivery cutoff, etc.) that shows gibberish is a direct,
immediate conversion-killer and trust-destroyer for anyone who does reach it, independent of any
search-engine consideration.

## Not assessed this pass

Cart abandonment friction, checkout step count, form validation UX, sticky add-to-cart behavior on
mobile, upsell/cross-sell placement effectiveness — all require live interaction testing.

## Related

[UX_AUDIT.md](UX_AUDIT.md), [../audit/VERIFIED_ISSUES.md](../audit/VERIFIED_ISSUES.md).
