<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/tahoe/plans-dark.svg">
  <img alt="Plans" src="../../assets/banners/tahoe/plans-light.svg" width="100%">
</picture>

# Plans

Committed work for Client Portal Platform, with tasks, milestones, and statistics.

## Navigation

Parent: [`README.md`](./README.md) · Theme:
[`macOS Tahoe Liquid Glass`](../../references/macos-tahoe-liquid-glass.md) ·
Rules: [`banner-and-badge-system.md`](../../references/banner-and-badge-system.md)

## Table of Contents

- [Navigation](#navigation)
- [Status Summary](#status-summary)
- [Plan Register](#plan-register)
- [01 Self-Serve API Keys tasks](#01-self-serve-api-keys-tasks)
- [Cumulative Statistics](#cumulative-statistics)
- [Footer Navigation](#footer-navigation)

## Status Summary

Counted from the tables below. The bold `Total` row must always sum them.

| S.No. | Status | Count |
| ---: | --- | ---: |
| 1 | Accepted | 1 |
| 2 | Implemented | 1 |
| 3 | Not Started | 1 |
| 4 | Planning | 1 |
| 5 | Review | 1 |
| 6 | Verified | 1 |
| **Total** | **Tracked records** | **6** |

## Plan Register

A Plan carries a richer status than a task, because done and proven differ.

| S.No. | Plan | Title | State | Priority |
| ---:  | --- | --- | --- | --- |
| 1 | `PLAN-01` | Client dashboard | ![Verified](../../assets/badges/tahoe/plan-verified.svg) | ![P2](../../assets/badges/tahoe/priority-p2.svg) |
| 2 | `PLAN-02` | Onboarding flow | ![Implemented](../../assets/badges/tahoe/plan-implemented.svg) | ![P1](../../assets/badges/tahoe/priority-p1.svg) |
| 3 | `PLAN-03` | Self-serve API keys | ![Accepted](../../assets/badges/tahoe/plan-accepted.svg) | ![P1](../../assets/badges/tahoe/priority-p1.svg) |
| 4 | `PLAN-04` | Usage alerts | ![Review](../../assets/badges/tahoe/plan-review.svg) | ![P3](../../assets/badges/tahoe/priority-p3.svg) |
| 5 | `PLAN-05` | Reporting export | ![Planning](../../assets/badges/tahoe/plan-planning.svg) | ![P2](../../assets/badges/tahoe/priority-p2.svg) |
| 6 | `PLAN-06` | White-label branding | ![Not Started](../../assets/badges/tahoe/plan-not-started.svg) | ![P3](../../assets/badges/tahoe/priority-p3.svg) |

## 01 Self-Serve API Keys tasks

Tasks for `PLAN-03`. Every task names a source record.

| S.No. | Task | Estimate | Risk | Source |
| ---:  | --- | --- | --- | --- |
| 1 | Key issue and revoke endpoints | ![Est M](../../assets/badges/tahoe/estimate-m.svg) | ![Risk Medium](../../assets/badges/tahoe/risk-medium.svg) | `ADR-003` |
| 2 | Key rotation schedule | ![Est S](../../assets/badges/tahoe/estimate-s.svg) | ![Risk Low](../../assets/badges/tahoe/risk-low.svg) | Research 1 |
| 3 | Client-facing key screen | ![Est L](../../assets/badges/tahoe/estimate-l.svg) | ![Risk Low](../../assets/badges/tahoe/risk-low.svg) | Concept 1 |
| 4 | Quota enforcement hook | ![Est L](../../assets/badges/tahoe/estimate-l.svg) | ![Risk High](../../assets/badges/tahoe/risk-high.svg) | `ADR-003` |

## Cumulative Statistics

Counts roll up; they are never estimated by hand.

| S.No. | Measure | Count |
| ---:  | --- | --- |
| 1 | Plans total | 6 |
| 2 | Plans verified | 1 |
| 3 | Tasks in `PLAN-03` | 4 |
| 4 | Tasks blocked | 0 |
| **Total** | **Tracked records** | **11** |

> [!NOTE]
> `IMPLEMENTED` and `VERIFIED` require real evidence. Neither is inferred from a file existing.

## Footer Navigation

Parent: [`README.md`](./README.md) · Gallery:
[`theme-asset-gallery.md`](../theme-asset-gallery.md)
