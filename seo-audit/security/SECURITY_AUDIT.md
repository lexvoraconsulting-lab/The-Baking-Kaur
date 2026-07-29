# Security Audit

## Scope of this pass

This audit's primary focus was content fabrication (EEAT/trust signals) and schema/SEO correctness.
Security was reviewed only incidentally, for whatever surfaced while reading the files already open
for other reasons — this is **not** a complete security audit, and isn't presented as one.

## What was observed (Verified, incidental)

- HTTPS is Shopify's platform default for all stores on a custom domain — not independently
  configured in theme code, and not in question.
- No hardcoded API keys, tokens, or credentials were found in any of the ~15 theme files read this
  session (`sections/*.liquid`, `snippets/*.liquid`, `layout/theme.liquid`, `templates/*.json`).
- No inline `<script>` blocks pulling from a non-Shopify, non-CDN third-party origin were noticed in
  the files reviewed (this is not an exhaustive third-party-script audit).
- `seo-ops/`'s existing Python tooling (per `docs/CODING_STANDARDS.md`) uses an environment-variable
  `SHOPIFY_TOKEN`, not a hardcoded one — consistent with safe practice, unchanged this session.

## Not assessed this pass

Content-Security-Policy headers, cookie configuration, mixed-content scanning across the full asset
list, form spam/bot protection, dependency/app-script vulnerability scanning, and any
infrastructure-level (DNS, hosting, CDN) configuration — none of these were in scope for a
content-fabrication-focused audit, and none were checked.

## Recommended next step

A dedicated security review pass (e.g. via this project's `/security-review` skill), scoped
specifically to headers, third-party app scripts, and form handling, run independently of this
content-focused audit.

## Related

[../audit/SCORECARD.md](../audit/SCORECARD.md).
