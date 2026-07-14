# QA_CHECKLIST.md — The Baking Kaur

Per-phase quality gate. Run before promoting any change from preview → live. Derived from the Phase-A validation flow. Nothing ships with an open ❌.

## Deploy discipline
- Work on preview theme (`colorful-composition` #151370334377); never edit the published theme directly.
- Rollback point recorded in `CHANGELOG.md`; scoped `--only` pushes; re-verify on live after promote.
- Validation runs on a **real theme** (schema/settings errors don't surface locally).

## 1. Build integrity
- [ ] `{% schema %}` JSON valid; section renders in editor (no "invalid schema").
- [ ] Section-group JSON references only valid sections.
- [ ] Theme Check: **no new offenses** on changed files (baseline in `PERFORMANCE_BASELINE.md`).
- [ ] No dangling references to removed files.

## 2. SEO / Schema
- [ ] One `<h1>` per page.
- [ ] Rich Results Test passes on changed templates; each entity emits **once** (`SCHEMA_MASTER.md`).
- [ ] FAQPage only where visible FAQ exists; AggregateRating only if real.
- [ ] Canonical + meta description present; keyword-aware anchors.

## 3. Accessibility (WCAG 2.2 AA)
- [ ] Landmarks (`main`, `contentinfo`, `nav[aria-label]`); logical headings.
- [ ] Contrast ≥4.5:1 body / ≥3:1 large (gold not for small text).
- [ ] Visible focus rings; keyboard-operable carousels/accordions; targets ≥44px.
- [ ] All images have `alt`; icon-only controls have `aria-label`; no emoji-as-UI.
- [ ] `prefers-reduced-motion` honored.

## 4. Performance
- [ ] LCP image preloaded + dimensioned; below-fold lazy.
- [ ] No new render-blocking assets; no new fonts; no whole-document observers.
- [ ] CLS ≈ 0 (no layout shift); budgets on track (LCP<2s, CLS<0.1, INP good) — Phase H.

## 5. Responsive
- [ ] ≤767 / 768–1023 / ≥1024 / ≥1440 verified.
- [ ] **No horizontal page overflow** at any width.
- [ ] Carousels show peek; grids collapse per spec; touch targets OK.

## 6. Functional smoke (preview)
- [ ] Homepage · Collections · Search · Header/Nav · Footer render (HTTP 200).
- [ ] **Product page unchanged** (premium section, Add-to-Cart, Uploadcare, WhatsApp intact) — protected.
- [ ] Cart page + Cart drawer · WhatsApp · policy pages · internal links resolve.
- [ ] Reviews widget (if present) loads or hides gracefully.

## 7. Analytics (Phase J+)
- [ ] Events fire with correct params (view_item_list, select_item, add_to_cart, whatsapp_click…).

## 8. Content
- [ ] Copy matches `HOMEPAGE_CONTENT_STRATEGY.md` verbatim; no ad-hoc copy in Liquid.
- [ ] Empty/error states verified (no empty grids, graceful fallback).

## Change log
- [ ] `CHANGELOG.md` entry: file · reason · business/SEO/perf impact · risk · rollback.

_v0.1 — the gate for every phase._
