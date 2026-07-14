# PERFORMANCE_BASELINE.md — The Baking Kaur

Starting performance state + targets. Honest about measurement limits in this environment. Rigorous lab measurement is Phase H.

## Measurement caveats
- No official Lighthouse lab run available in the current tooling. Figures below are best-effort from the browser Performance API on the **preview** theme (slower than live) + Theme Check + static asset inspection. Treat as directional, not certified.
- Re-baseline with real Lighthouse (mobile + desktop) at Phase H start.

## Asset weight (static)
| Asset | Size |
|---|---|
| `theme.css` | 264 KB |
| `base.css` | 128 KB |
| `global.min.js` | 152 KB |
| `vendor.min.js` | 124 KB |
| `es-photoswipe.min.js` | 60 KB |
| ShineTrust v4 scripts | 20+ files |
Fonts: Google Fonts (Cormorant + Manrope) — **render-blocking** `<link>` in head.

## Runtime (preview homepage, best-effort)
| Metric | Reading | Note |
|---|---|---|
| CLS | ≈ 0 | good |
| DOMContentLoaded | ~4.9 s | slow (apps + observers + blocking fonts) |
| Load | ~9.2 s | slow; preview slower than live |
| LCP | not captured | measure at Phase H |
| Resources | ~139 | high count |

## Known perf drags (pre-existing)
- 3 whole-document `MutationObserver`s in `theme.liquid` (sticky-ATC remover, `<`-arrow remover, mojibake walker) — continuous main-thread work; also block screenshot capture.
- Uploadcare loaded twice (2× parser-blocking scripts) — feeds protected PDP; needs PDP-safe fix.
- Render-blocking Google Fonts + large `theme.css`/`base.css`.
- 20+ ShineTrust app scripts — usage audit needed.
- Theme Check: **1,365 offenses / 88 files** (1,163 errors, 202 warnings) — overwhelmingly base-theme/app pre-existing; Phase-A files added **0**. Notable types: LiquidHTMLSyntaxError, UnusedAssign, ParserBlockingScript, RemoteAsset.

## Targets (Phase H)
| Metric | Target |
|---|---|
| Lighthouse (mobile) | 90+ |
| Lighthouse (desktop) | 95–100 |
| LCP | < 2.0 s |
| CLS | < 0.1 |
| INP | "Good" (<200ms) |
| Render-blocking | fonts subset/`font-display`, critical CSS, defer JS |

## Phase-A impact
Net perf-neutral-to-positive: removed inline duplicate schema + 10 dead files; added one small self-contained footer (scoped CSS, lazy logo). No new blocking assets.

_v0.1 — re-baseline at Phase H with Lighthouse._
