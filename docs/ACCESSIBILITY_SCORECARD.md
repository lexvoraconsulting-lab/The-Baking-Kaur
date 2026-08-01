# Accessibility Scorecard (Phase 7.5)

| Dimension | Score (1–5) | Evidence |
|---|---|---|
| Skip navigation | 5/5 | Present, correctly targets `#MainContent` |
| Icon-only interactive controls (wishlist/compare/quick-view/header) | 5/5 | All confirmed paired with `sr-only`/`aria-label` accessible names |
| Modal/dialog mechanics (role, focus trap, Escape) | 5/5 | `role="dialog"`, `aria-modal`, focus-trap library confirmed on quick view/quick add/compare; hand-rolled equivalent on mobile nav drawer |
| Landmark structure (`main`, footer `nav`) | 5/5 | Single `main`, footer has 4 distinctly-labelled `nav` regions |
| **Modal close-button focus visibility** | **2/5 → fixed** | Was a real WCAG 2.4.7 gap across 4 live modals (shadow-DOM `::part()`, unreachable by the theme's global focus-visible rule) — closed this phase with one shared CSS rule |
| **Default-template delivery-date/slot button names** | **2/5 → fixed** | Was announced as bare "button" on every product page — closed this phase with static `aria-label`s |
| **Newsletter email input labeling** | **2/5 → fixed** | Placeholder-only, no real label — closed this phase, shared snippet used by 3 live sections |
| **Cart reference-photo rendering** | **1/5 → fixed** | Markup typo silently dropped the image entirely (not an accessibility-only bug — nobody, sighted or not, could see it) — closed this phase |
| **Account-page table `id`/`headers` association** | **2/5 → fixed** | Static ids inside loops broke screen-reader table navigation for any customer with >1 order/discount — closed this phase |
| **Account-area nav landmark labeling** | **2/5 → fixed** | 3 unlabeled `nav` regions on account pages — closed this phase |
| Hampers/premium(non-v2) product templates' delivery-date field | **1/5, open** | Label points at a non-existent input; JS expects an element the markup never renders — real functional gap, needs a product decision before a fix can be written (see `ACCESSIBILITY_AUDIT.md`) |
| Heading hierarchy on default product template | 3/5, open | h1→h3 skip, structural not blocking, deferred to a dedicated pass |
| Reduced motion | 4/5 | Correctly gated at the base-theme layer; bespoke `tbk-*` transitions not independently re-verified line-by-line |
| Live verification (contrast ratios, real screen reader pass, keyboard-only walkthrough) | Not measured | Password gate blocks every live/lab tool, unchanged constraint carried from every prior phase |
| **Overall Accessibility Readiness (code-evidence basis)** | **3.6/5** | 6 real, live-impacting defects found and fixed this phase (up from "not yet independently scored"); 1 real defect found and correctly escalated rather than guessed at; 2 items deferred to a future structural pass |

## Why this is a code-evidence score, not a live-tested one

Every finding here is backed by an actual file:line read, not inference — but none of it was run
through a real screen reader, a keyboard-only walkthrough, or a contrast-ratio tool, because the
storefront is intentionally password-gated (per the standing decision to keep the gate until final
certification) and this environment has no browser. That gate is exactly why this score is a floor,
not a ceiling: static analysis catches missing names, broken associations, and dead markup
reliably, but it cannot catch everything a real assistive-technology pass would (timing, dynamic
announcement of live regions, actual contrast against the rendered palette). Re-score once the gate
lifts and a real pass is possible.

## Related

[ACCESSIBILITY_AUDIT.md](ACCESSIBILITY_AUDIT.md), [PROJECT_SCORECARD.md](PROJECT_SCORECARD.md).
