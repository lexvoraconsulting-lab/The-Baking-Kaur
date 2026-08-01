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

### Update (Phase 7.4, 2026-07-31): execution-gate found — materially lowers customer-facing risk

Re-read the full surrounding block (`assets/custom.js:2170-2280`) that was not fully traced in the
original pass. The entire mechanism — the `fetch()` call, the merchant-email/domain/theme/purchase-
code payload, and the "ACTIVATED SUCCESSFULLY" banner it injects — is nested inside a single outer
conditional:

```js
if(Shopify.designMode){
  // ... everything described above, including the fetch() to lic.the4.co, lives entirely here ...
}
```

`Shopify.designMode` is a Shopify-platform global that is `true` **only** while a store admin/staff
member has the theme open in the Admin's Theme Editor (Customize / preview mode) — it is `false` for
every ordinary storefront page view. This means the original finding's wording, "sends real merchant
data ... on every qualifying page load," **overstated the exposure**: this code cannot fire during
normal customer browsing at all. It only runs when someone with Shopify Admin access is actively
customizing the theme, and the data sent (store domain, store's own email, theme name, purchase
code) describes the *store itself*, not any customer or visitor — no customer PII is read or sent
anywhere in this code path.

**Revised assessment**: this is the standard license-activation check used by ThemeForest/Envato-
style commercial theme marketplaces (this theme is built on the "The4" framework) — functionally
equivalent to a WordPress premium theme/plugin phoning home to verify a purchase code when an admin
opens its settings screen. The obfuscation (shuffled-character-array URL, double base64 on the
shop-email global, base64-wrapped JSON body) is unusual for a same-vendor legitimate check but is
also a known anti-tamper pattern in this exact marketplace segment, not unique to malicious code.

**Recommended action (unchanged conclusion, now evidence-backed rather than precautionary)**:
**Do NOT remove.** Per this decision's own test ("prove it is unnecessary OR introduces unacceptable
risk") — neither holds: it is not proven unnecessary (removing a marketplace theme's license check
without confirming license terms/tamper-detection behavior is exactly the risk `docs/CLAUDE.md`
already flags), and the customer/privacy risk is now shown to be effectively nil (customers never
trigger this path). The narrower, lower-risk action available to the business, if this remains a
concern, is confirming the theme's own purchase/license record with the vendor — not patching the
check out.
- **Verification Status**: AUDITED, execution gate confirmed by direct code read (not live network
  inspection — still blocked by the password gate, unchanged limitation). Payload/URL decoding from
  the original pass re-confirmed unchanged.
- **Sprint**: Phase 7.4 (this sprint) — correction of Enterprise Certification continuation finding.
- **Commit Reference**: N/A — no code changed for this issue; documentation-only correction.
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
| Other raw, unescaped Liquid `echo`/`{{ }}` of user-controlled input (search/predictive-search) | **SEC-003, FIXED (Phase 7.4)** — `?q={{ predictive_search.terms }}` in `hdt_predictive-search.liquid:10` (the live drawer search, referenced from `snippets/search-form.liquid`) had no encoding at all: a literal `"` in the search term would break out of the `href="..."` attribute. Fixed by adding `\| url_encode`, which both restores query-string correctness and closes the attribute-breakout vector (percent-encoding turns `"` into `%22`, which cannot break the surrounding attribute). Deployed via scoped `--only` push, re-pulled byte-identical, Theme Check unchanged (343/1,351/80/1,161/190). Remaining `predictive_search.terms` usages are passed through the `t:` translation filter (auto-escaped by Shopify's translation system) — no further action needed. |

## Not audited this pass (flagged, not silently skipped)

- Live network-request inspection to confirm `SEC-001`'s actual behavior on the current production
  theme (password gate blocks this).
- Dependency-vulnerability scanning for `seo-ops/`'s Python dependencies (no internet-connected
  vulnerability database access in this environment).

## Related

[STRUCTURED_DATA_REPORT.md](STRUCTURED_DATA_REPORT.md), [SHOPIFY_SEO_REPORT.md](SHOPIFY_SEO_REPORT.md).
