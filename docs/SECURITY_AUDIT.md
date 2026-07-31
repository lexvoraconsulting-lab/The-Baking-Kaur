# Security Audit (Sprint — Enterprise Certification continuation)

First dedicated security pass in this engagement. Continues from Phase 7.3
(`docs/STRUCTURED_DATA_REPORT.md`, commit `ea9e3ee`). Format per this program's Enterprise Issue
Governance: Issue ID, Category, Severity, Confidence, Risk Level, Evidence, Root Cause, Files
Affected, Recommended Action, Verification Status, Sprint, Commit Reference, Current Status.

---

## SEC-001 — Undisclosed third-party data exfiltration (theme vendor licensing check)

- **Category**: Security / Privacy
- **Severity**: High
- **Confidence**: High (verified by decoding the obfuscated payload directly)
- **Risk Level**: Medium-High (real privacy/trust exposure; not confirmed exploitable by an
  external attacker, but confirmed to send real merchant data to an undisclosed third party)
- **Evidence**: `assets/custom.js` (~line 2170–2270) contains a licensing/"activation" check that:
  1. Reconstructs its target URL from a deliberately shuffled character array
     (`mix = ['4','t','h','e','p','l','i','c','o','/','.',':','n','s']`, reassembled via a
     hardcoded index sequence) rather than a plain string literal — decoded by hand in this audit
     to **`https://lic.the4.co/license/check`**.
  2. Reads the real, live store's `shop.email` (via `atob(window[atob('VTJodmNFMWxiMVEw')])` —
     itself base64-double-obfuscated) and the store's domain, theme name, and purchase code.
  3. Sends all four fields, `JSON.stringify`'d, URI-encoded, then base64-encoded
     (`btoa(encodeURIComponent(JSON.stringify(data)))`), via `fetch()` with `mode: "cors"`, to that
     decoded domain.
  4. Uses `atob()` again elsewhere in the same code path to obfuscate a CSS selector
     (`#purchase_codet4`), reinforcing that obfuscation is deliberate and systematic, not
     incidental minification.
- **Root cause**: this is the theme vendor's (The4/Ecomus, per `docs/SHOPIFY_ARCHITECTURE.md`'s
  own note that the theme's `theme_author` field is "mislabelled 'Shopify'" — itself a signal
  worth independent verification) own licensing/anti-piracy mechanism, bundled into the purchased
  theme. This is a known pattern for premium theme marketplaces generally, but the specific
  implementation here — sending the merchant's real email address off-site on every qualifying
  page load, via code deliberately obscured from casual review — is a real trust and privacy
  concern regardless of the vendor's legitimacy.
- **Files Affected**: `assets/custom.js`.
- **Recommended Action**: **Do NOT remove unilaterally.** This is a **Level 3/4 decision** — it
  concerns the store's licensing relationship with a paid third-party theme vendor, not a pure
  technical defect. Removing it could trigger vendor-side tamper detection (some licensing schemes
  degrade functionality or display warnings if their check is stripped) or could constitute a
  license-terms violation depending on the vendor's actual agreement. Recommend the business: (1)
  confirm the theme's license status directly with the vendor/original purchase records, (2)
  decide whether continued phone-home behavior is acceptable given the merchant email exposure, and
  (3) only then decide on removal, replacement, or acceptance.
- **Verification Status**: AUDITED — root cause and payload fully decoded and confirmed; live
  network behavior (whether this fetch actually fires on the current production theme, and what
  response it receives) not independently observed (would require live browser network inspection,
  additionally blocked by the password gate).
- **Sprint**: Enterprise Certification continuation (this sprint).
- **Commit Reference**: N/A — no code changed for this issue.
- **Current Status**: **CLASSIFIED**, escalated to Level 3/4 (business/vendor decision required).
  Not implemented, not closed.

---

## SEC-002 — Reflected XSS: unescaped `search.terms` echo — FIXED

- **Category**: Security
- **Severity**: Medium (real vulnerability class; currently unreachable in production — see below)
- **Confidence**: High
- **Risk Level**: Low (dead code path today; would be Medium-High if the gating linklist were ever
  populated)
- **Evidence**: `sections/header-e-commerce.liquid:13` (before fix):
  `echo search.terms | remove_first: ' OR ' | remove_first: 'submenu' | strip` — echoes the raw
  search query string with no `| escape`, inside a `{%- capture brand -%}` block that is later
  output directly into page HTML (line 35's `key_brand` capture, and the `brand` variable used in
  comparisons/output throughout the rest of the section). A crafted search query containing HTML/
  script would be reflected unescaped.
- **Root cause**: the surrounding "multi-brand" navigation feature (`linklists.theme_brands`) is
  entirely gated on `{%- if linklists.theme_brands.links -%}` — confirmed via `config/` search that
  no `theme_brands` linklist exists on this store, so this whole code block, including the
  vulnerable line, **does not currently render on the live site**. This matches this project's
  established "fix defensively regardless of current liveness" precedent (used previously for
  `assets/no-image.svg`, R6) — a dead-today code path can become live again if a `theme_brands`
  linklist is ever created via the theme editor, at which point the vulnerability would become
  real without any further code change.
- **Files Affected**: `sections/header-e-commerce.liquid`.
- **Recommended Action**: add `| escape` to the `echo` — purely additive, zero behavior change for
  any legitimate (non-HTML) search term, eliminates the vulnerability class entirely regardless of
  whether/when the feature is ever activated.
- **Verification Status**: **VERIFIED**. Deploy safety: pulled live copy, diff-confirmed zero drift
  before editing; edited; pushed via scoped `--only` push; re-pulled and diff-confirmed the fix is
  live (`grep` on the freshly-pulled copy shows `| escape` present). Theme Check run after — no new
  offenses introduced (see verification section below).
- **Sprint**: Enterprise Certification continuation (this sprint).
- **Commit Reference**: (this sprint's commit, see `seo-audit/audit/CHANGELOG.md`).
- **Current Status**: **CLOSED**. NEW → AUDITED → CLASSIFIED → IMPLEMENTED → VERIFIED → COMMITTED →
  CLOSED, full lifecycle completed this sprint.

---

## Other security checks performed, no issues found

| Check | Result |
|---|---|
| Hardcoded Shopify Admin API tokens (`shpat_...`) in tracked source | None — all 4 matches are placeholder examples (`shpat_xxx`) in `seo-ops/*.py` usage-instruction comments |
| `.env`/credentials files tracked in git | None found |
| `.gitignore` coverage for generated sensitive output | Adequate — `seo-ops/*.csv`, `*.jsonl`, `*.log` excluded |
| `eval()`/`exec()`/`os.system()`/`subprocess(..., shell=True)` in `seo-ops/*.py` | None found |
| Other raw, unescaped Liquid `echo`/`{{ }}` of user-controlled input (search/predictive-search) | None found beyond SEC-002 — `predictive_search.terms` usages found are either inside a URL query-string context (`?q={{ predictive_search.terms }}`, which needs `url_encode` more than `escape`; not independently re-verified as a separate issue this pass) or passed through the `t:` translation filter (auto-escaped by Shopify's translation system) |

## Not audited this pass (flagged, not silently skipped)

- Whether `?q={{ predictive_search.terms }}` (found during this audit, `hdt_predictive-search.liquid:10`)
  needs a `url_encode` filter for correctness/safety — noted but not independently confirmed as a
  vulnerability or fixed; flagged as a follow-up item, not closed.
- Live network-request inspection to confirm `SEC-001`'s actual behavior on the current production
  theme (password gate blocks this).
- Dependency-vulnerability scanning for `seo-ops/`'s Python dependencies (no internet-connected
  vulnerability database access in this environment).

## Related

[STRUCTURED_DATA_REPORT.md](STRUCTURED_DATA_REPORT.md), [SHOPIFY_SEO_REPORT.md](SHOPIFY_SEO_REPORT.md).
