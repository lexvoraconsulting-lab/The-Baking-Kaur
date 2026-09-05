# Performance Scorecard (Phase 6, P6.0)

Scored from static code-evidence only (see `docs/CORE_WEB_VITALS.md` for why no lab/field
Core Web Vitals numbers exist yet). Scores reflect **evidenced risk/strength signals**, not
measured Lighthouse scores — conflating the two would violate this project's own no-fabrication
standard. Re-score once R-9 (a real Lighthouse/PSI run, `docs/PERFORMANCE_RECOMMENDATIONS.md`) is
possible.

| Dimension | Score (1–5) | Evidence |
|---|---|---|
| **Render-blocking resources** | 2/5 | `theme.css` (264 KB) + `base.css` (129 KB) load unconditionally with no critical-CSS split (F-5); Google Fonts loaded via a synchronous stylesheet link with an incomplete preconnect set (F-6/F-7). No measurement exists yet to know the *actual* FCP/LCP cost, but the pattern itself is a known anti-pattern. |
| **JavaScript hygiene** | 3/5 | One confirmed duplicate third-party script load (F-8) — trivial fix pending. One ~136 KB script bundle (Shine Trust) with undetermined live/dead status (F-9). No unused-JS coverage data exists yet (R-10). Positive: `hamper-addons.js` correctly uses `defer`. |
| **CSS hygiene** | 3/5 | Same render-blocking size concern as above; no unused-selector data exists yet. No duplicate-CSS-file evidence found beyond the theme's existing structure. |
| **Image delivery** | 5/5 | Responsive `srcset`/`sizes` used pervasively and correctly (F-14); correct `eager`+`fetchpriority="high"` on the primary product image, `lazy` on the rest (F-12); all product imagery correctly served from Shopify's CDN, zero bundled in `assets/` (F-16). Only gap: 4 missing-dimension `<img>` tags, all inside an already-unreachable section (F-1 in `PERFORMANCE_AUDIT.md`, cross-referencing R3.5). |
| **Font loading** | 3/5 | `font-display: swap` correctly present (F-6); missing `fonts.gstatic.com` preconnect is a real, trivial-to-fix gap (F-7). |
| **Pagination & list rendering** | 5/5 | Real `{% paginate %}` used across all 11 listing-type sections, sane merchant-configurable defaults (8, max 50) (F-3). No unbounded-list risk found anywhere. |
| **Third-party script inventory completeness** | 2/5 | `content_for_header` means installed-app scripts are invisible to this static audit (F-11); Theme App Extension block presence not exhaustively confirmed (F-15). Real confidence requires a live-page check this environment cannot perform. |
| **Render-tree complexity** | 3/5 | The default product template is a 4,642-line, 31-render-call file (F-1) — but it's the protected module, and complexity alone isn't proof of a performance problem without real profiling. 17 near-duplicate card snippets (F-2) are a maintainability concern more than a runtime one. |
| **Accessibility-linked performance** | 4/5 | `prefers-reduced-motion` correctly respected across CSS and JS (F-17) — reduces both motion-sickness risk and unnecessary animation work for users who opt out. Focus/contrast not audited this pass (gap, not a negative finding). |
| **Measurement completeness** | 1/5 | **Zero real Core Web Vitals data exists** — the site's own password gate blocks every lab and field measurement path available to this project. This is the single largest gap in this audit and the top-priority item for P6.1 (R-9). |
| **Overall Performance Readiness** | **3.1/5** | A theme with several genuinely strong, correctly-implemented patterns (images, pagination, reduced-motion) alongside a few concrete, low-risk fixes (font preconnect, duplicate script) and one large unknown (no real measurement data yet). Not a theme in poor shape — but not yet *verified* good, because verification itself isn't possible until the site is measurable. |

## Why this scorecard is intentionally conservative

Several dimensions that *could* score higher on "no evidence of a problem found" are held at 3/5
rather than 4–5/5, specifically because this audit's static-analysis method cannot rule out
problems that only a live-render coverage tool would surface (unused JS/CSS %, real render-blocking
timing, actual third-party script weight). A 5/5 is reserved for dimensions with **direct,
complete, positive evidence** (images, pagination, reduced-motion) — not merely "nothing bad found
by grep."

## Related

[PERFORMANCE_AUDIT.md](PERFORMANCE_AUDIT.md), [PERFORMANCE_BASELINE.md](PERFORMANCE_BASELINE.md),
[CORE_WEB_VITALS.md](CORE_WEB_VITALS.md), [PERFORMANCE_RECOMMENDATIONS.md](PERFORMANCE_RECOMMENDATIONS.md),
[PERFORMANCE_ROADMAP.md](PERFORMANCE_ROADMAP.md).
