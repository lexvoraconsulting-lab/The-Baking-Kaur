# Phase 7 Acceptance Criteria

What "done" means for each major Phase 7 initiative. Written so a future session (or human
reviewer) can objectively check completion without re-deriving intent.

## Documentation reconciliation (Track A)

- [ ] Exactly one authoritative `CHANGELOG.md` location is documented and used going forward (C-2)
      — either the root file is deprecated with an explicit pointer to `seo-audit/audit/CHANGELOG.md`,
      or the two are merged, or the split is explicitly justified in writing.
- [ ] `docs/ARCHITECTURE.md`'s template count matches `ls templates/*.json templates/*.liquid`'s
      actual output at time of update (H-5).
- [ ] Root and `docs/` versions of `PERFORMANCE_BASELINE.md` either agree on what measurement was
      actually performed, or one explicitly supersedes the other with a dated note (M-4).
- [ ] Root `DESIGN_SYSTEM.md`/`COMPONENT_LIBRARY.md`/`CONTENT_SYSTEM.md`/`COPY_GUIDELINES.md` each
      carry a one-line pointer to their `design/*.md` counterpart, stating which is authoritative
      for implementation detail (M-5).

## Password gate resolution (C-1)

- [ ] A business decision is recorded (in `docs/DECISIONS.md` or equivalent) — unlock, define a
      public-preview path, or explicitly reaffirm the gate stays, with a reason.
- [ ] If unlocked or a preview path exists: a real Lighthouse/PSI run has been performed and
      `docs/CORE_WEB_VITALS.md` updated with real numbers, replacing every proxy risk signal.
- [ ] If the gate stays: this is documented as a deliberate, revisited decision — not silently
      re-carried forward without confirmation.

## FAQPage schema (H-2)

- [ ] `page.faq-01.json`'s content is confirmed either already wrapped in `FAQPage`/`Question`/
      `Answer` JSON-LD, or a specific gap is identified with a proposed (not yet implemented) fix.
- [ ] No FAQ content is changed — only schema wiring is assessed/proposed, per this project's
      standing "prepare the architecture, don't change content" rule.

## `shine-trust.liquid` decision (H-3)

- [ ] Business owner has explicitly chosen: turn the bundle/upsell widget on (fix the include typo)
      or delete it entirely (CSS + all 7 JS files, ~214 KB).
- [ ] Whichever choice is made is executed with the same pull→diff→edit→push→re-pull→diff
      discipline as every other change in this project, verified via Theme Check before/after.

## `tbk-product.liquid` removal (H-4)

- [ ] A manual Shopify Admin → Apps check has confirmed zero app dependencies on this section.
- [ ] If confirmed clear: the section is removed following the same scoped-deploy pattern as R1/
      R3.5/R5, with before/after Theme Check and a changelog/ledger entry.
- [ ] If any app dependency is found: this is documented as a new finding, and the section is left
      in place with the reason recorded.

## Internal-linking and content-chunking audits (M-1, M-2)

- [ ] A concrete map exists of which pages link to which, with orphaned-page candidates identified.
- [ ] Content-chunking recommendations are documented (not implemented) for at least the homepage
      and one collection-page template, building on the existing product-tabs pattern.

## Overall Phase 7 kickoff acceptance

- [ ] Every task in `docs/PHASE7_TASK_BREAKDOWN.md` has either been completed, explicitly deferred
      with a reason, or assigned to a named future phase.
- [ ] No new documentation conflicts have been introduced (verified by re-running this review's
      duplicate-filename check: `find . -iname "*.md" | xargs -n1 basename | sort | uniq -d`).
- [ ] `seo-audit/audit/CHANGELOG.md` and `seo-audit/audit/AUDIT_LEDGER.md` have an entry for every
      real change made during Phase 7, matching this project's established convention.

## Related

[PHASE7_SUCCESS_METRICS.md](PHASE7_SUCCESS_METRICS.md), [PHASE7_TASK_BREAKDOWN.md](PHASE7_TASK_BREAKDOWN.md),
[PHASE7_EXECUTION_PLAN.md](PHASE7_EXECUTION_PLAN.md).
