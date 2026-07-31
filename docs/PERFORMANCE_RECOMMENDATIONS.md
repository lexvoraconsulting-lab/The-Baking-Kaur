# Performance Recommendations (Phase 6, P6.0)

Prioritized, evidence-linked recommendations from `docs/PERFORMANCE_AUDIT.md`. Every row includes
Evidence, Measurement, Expected benefit, Risk level, Priority, and Owner, per this phase's quality
gate. **Nothing here has been implemented** — this is the recommendation set for P6.1's approval
gate.

| # | Recommendation | Evidence | Measurement (how to verify) | Expected benefit | Risk | Priority | Owner | **Status** |
|---|---|---|---|---|---|---|---|---|
| R-1 | Add `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` to `layout/theme.liquid`, alongside the existing font preconnects (lines 36, 40) | `docs/PERFORMANCE_AUDIT.md` F-7 — 0 occurrences of `fonts.gstatic.com` confirmed via grep | Before/after: DevTools Network waterfall, connection-setup time for the first `.woff2` font request | Removes ~1 round-trip (DNS+TCP+TLS) from the critical font-loading path | **None** — purely additive | P0 | Engineering | **✅ DONE (P6.6)** — deployed live, diff-confirmed byte-identical |
| R-2 | ~~Remove the duplicate `uploadcare.full.min.js` tag at line 292~~ | ~~F-8~~ | — | — | — | — | — | **❌ RETRACTED (P6.5)** — deeper read found the second tag sets 4 additional config globals (multi-file, camera/URL tabs, images-only, 1600×1600 shrink) not present at the first load, indicating a distinct real feature, not a duplicate. Not implemented — would have risked breaking real functionality. |
| R-3 | Evaluate adding `defer` to the Uploadcare tags | F-8 (superseded) | N/A | N/A | N/A | Withdrawn | — | **Withdrawn** — moot once R-2 was retracted; both tags are load-bearing, not redundant |
| R-4 | Trace the actual `<script src>` reference path(s) for all 7 `shine-trust-v4-*.js` files (~136 KB combined); determine live/dead status independently of the already-confirmed-broken CSS include | `docs/PERFORMANCE_AUDIT.md` F-9 | Repo-wide grep for each filename | Up to ~136 KB removed if confirmed fully dead | None to investigate; removal itself (if warranted) is a separate, later decision | P1 | Engineering | **✅ RESOLVED (P6.5)** — all 7 confirmed referenced only inside the already-dead `shine-trust.liquid`; transitively dead, but gated on the same unresolved business decision (R-5) — not removed |
| R-5 | Resolve the pending `shine-trust.liquid` business decision (turn the widget on vs. delete entirely) — blocks R-4's final action | `SEO_AUDIT_LEDGER.md` P2-26, `docs/ORPHAN_SNIPPET_AUDIT.md` | N/A — business decision, not a technical measurement | Either activates a real bundle/upsell widget or removes ~78 KB CSS + up to ~136 KB JS of dead weight | Medium — turning it on is a real visible/UX change requiring sign-off | P1 | **Business/Product owner** |
| R-6 | Critical-CSS extraction for `theme.css` (264 KB) + `base.css` (129 KB): inline above-the-fold styles, defer the rest | `docs/PERFORMANCE_AUDIT.md` F-5 | Before/after Lighthouse FCP/LCP (once measurable — see `docs/CORE_WEB_VITALS.md`); visual regression test suite across homepage, collection, and product pages | Meaningful FCP/LCP improvement (unquantified without lab access) | **Medium-High** — real visual-regression risk, and the product page is a protected module (`CLAUDE.md`) requiring extra sign-off | P2 | Engineering + a visual QA pass before any live push |
| R-7 | Complete a live-page `content_for_header` inventory (what installed apps actually inject) once the storefront is unlocked or a preview-bypass session exists | `docs/PERFORMANCE_AUDIT.md` F-11 | View-source / DevTools Network on a real authenticated session | Surfaces any invisible third-party performance cost not visible in this repo | None to investigate | P2 | Engineering |
| R-8 | Confirm no Theme App Extension blocks exist beyond Uploadcare + Shine Trust, via a full `templates/*.json` block-type sweep | `docs/PERFORMANCE_AUDIT.md` F-15 | `grep` all `"type"` values in `templates/*.json` against known app-block UUID patterns | Completeness confidence for the third-party-script inventory | None | P2 | Engineering |
| R-9 | Run a real Lighthouse/PageSpeed Insights pass (mobile + desktop) on homepage, one product page, one collection page, once the site is reachable by an authenticated session or public | `docs/CORE_WEB_VITALS.md` | The PSI/Lighthouse report itself becomes the measurement | Replaces every proxy risk signal in this audit with real, numeric Core Web Vitals data | None — read-only measurement | **P0 — should happen before any further optimization work is prioritized** | Business owner (to grant access) + Engineering (to run it) |
| R-10 | DevTools Coverage run (unused JS/CSS %) against a real render, to quantify F-9/F-5's actual dead-weight percentage | `docs/PERFORMANCE_AUDIT.md`, JS/CSS review sections | DevTools → Coverage tab, record page load | Precise KB-level unused-code numbers, replacing the current static-size proxy | None — read-only measurement | P1 | Engineering |
| R-11 (future, high complexity) | Consolidate the 17 near-duplicate `card-product*.liquid` snippets into one parameterized snippet | `docs/PERFORMANCE_AUDIT.md` F-2 | Full behavioral diff across all 17 variants before/after | Maintainability, not runtime performance | **High** — 17-way behavioral-equivalence risk | P3 (future phase, not P6.1) | Engineering (dedicated phase) |
| R-12 (new, found during P6.2/P6.3 execution) | Remove 3 verified-orphaned CSS/JS assets not caught by P6.0's audit (`hdt-section-password.css`, `video_with_text2.css`, `day.js`) | Repo-wide grep, zero references, verified twice | Pre/post file-count and byte-size diff | ~10.7 KB total dead-weight removed | **None** — zero references confirmed twice | P0 | Engineering | **✅ DONE (P6.2/P6.3)** |

## Implementation status summary (post P6.1–P6.7)

Of the original 11 recommendations plus 1 discovered during execution: **2 implemented** (R-1,
R-12), **1 retracted after deeper investigation** (R-2, corrected to avoid a real regression),
**1 resolved as an investigation with no removal warranted yet** (R-4, gated on R-5's business
decision), **1 withdrawn as moot** (R-3). The remainder (R-5 through R-11, plus R-9/R-10's
measurement tasks) remain open, correctly deferred to a business decision, external access, or a
future dedicated phase — see `docs/PERFORMANCE_ROADMAP.md` for sequencing.

## Related

[PERFORMANCE_AUDIT.md](PERFORMANCE_AUDIT.md), [PERFORMANCE_BASELINE.md](PERFORMANCE_BASELINE.md),
[CORE_WEB_VITALS.md](CORE_WEB_VITALS.md), [PERFORMANCE_SCORECARD.md](PERFORMANCE_SCORECARD.md),
[PERFORMANCE_ROADMAP.md](PERFORMANCE_ROADMAP.md).
