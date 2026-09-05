<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/tahoe/concept-design-dark.svg">
  <img alt="Concept & Design" src="../../assets/banners/tahoe/concept-design-light.svg" width="100%">
</picture>

# Concept & Design

Proposed direction for Client Portal Platform, before it is committed.

## Navigation

Parent: [`README.md`](./README.md) · Theme:
[`macOS Tahoe Liquid Glass`](../../references/macos-tahoe-liquid-glass.md) ·
Rules: [`banner-and-badge-system.md`](../../references/banner-and-badge-system.md)

## Table of Contents

- [Navigation](#navigation)
- [Status Summary](#status-summary)
- [Concept Statements](#concept-statements)
- [Open Questions](#open-questions)
- [Footer Navigation](#footer-navigation)

## Status Summary

Counted from the tables below. The bold `Total` row must always sum them.

| S.No. | Status | Count |
| ---: | --- | ---: |
| 1 | Open Question | 2 |
| 2 | Confirmed | 1 |
| 3 | Future / Held | 1 |
| 4 | Planned | 1 |
| 5 | Proposed | 1 |
| 6 | Resolved by Addition | 1 |
| **Total** | **Tracked records** | **7** |

## Concept Statements

Every statement carries a status. No status means it is not tracked.

| S.No. | Statement | State | Maps to |
| ---:  | --- | --- | --- |
| 1 | Clients self-serve their own API keys | ![Planned](../../assets/badges/tahoe/planned.svg) | `PLAN-03` |
| 2 | One dashboard for all client activity | ![Confirmed](../../assets/badges/tahoe/confirmed.svg) | `PLAN-01` |
| 3 | Usage alerts are opt-in per client | ![Proposed](../../assets/badges/tahoe/proposed.svg) | Unmapped |
| 4 | White-label branding per client | ![Future / Held](../../assets/badges/tahoe/future-held.svg) | Not scheduled |

## Open Questions

An unanswered question blocks the concept that depends on it.

| S.No. | Question | State | Blocks |
| ---:  | --- | --- | --- |
| 1 | Do clients need sub-accounts? | ![Open Question](../../assets/badges/tahoe/open-question.svg) | Concept 1 |
| 2 | Who owns key revocation? | ![Open Question](../../assets/badges/tahoe/open-question.svg) | Concept 1 |
| 3 | Is SSO mandatory for all tiers? | ![Resolved by Addition](../../assets/badges/tahoe/resolved-by-addition.svg) | Answered in `ADR-001` |

> [!NOTE]
> A concept that stays unmapped past one cycle is either rejected or held. Decide.

## Footer Navigation

Parent: [`README.md`](./README.md) · Gallery:
[`theme-asset-gallery.md`](../theme-asset-gallery.md)
