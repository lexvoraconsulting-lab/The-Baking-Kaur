<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/lexvora/research-dark.svg">
  <img alt="Research" src="../../assets/banners/lexvora/research-light.svg" width="100%">
</picture>

# Research

Investigations and evidence behind Client Portal Platform choices.

## Navigation

Parent: [`README.md`](./README.md) · Theme:
[`Lexvora Company`](../../references/lexvora-company.md) ·
Rules: [`banner-and-badge-system.md`](../../references/banner-and-badge-system.md)

## Table of Contents

- [Navigation](#navigation)
- [Status Summary](#status-summary)
- [Topics](#topics)
- [Findings](#findings)
- [Footer Navigation](#footer-navigation)

## Status Summary

Counted from the tables below. The bold `Total` row must always sum them.

| S.No. | Status | Count |
| ---: | --- | ---: |
| 1 | Active | 1 |
| 2 | Confirmed | 1 |
| 3 | Open Question | 1 |
| 4 | Rejected | 1 |
| **Total** | **Tracked records** | **4** |

## Topics

Research is intake. Delivery belongs to a Plan.

| S.No. | Topic | State | Effort | Feeds |
| ---:  | --- | --- | --- | --- |
| 1 | Session storage options | ![Confirmed](../../assets/badges/lexvora/confirmed.svg) | ![Est M](../../assets/badges/lexvora/estimate-m.svg) | `ADR-002` |
| 2 | Rate-limit strategies | ![Active](../../assets/badges/lexvora/active.svg) | ![Est L](../../assets/badges/lexvora/estimate-l.svg) | `PLAN-03` |
| 3 | Audit-log retention law | ![Open Question](../../assets/badges/lexvora/open-question.svg) | ![Est S](../../assets/badges/lexvora/estimate-s.svg) | Pending legal |
| 4 | Offline sync feasibility | ![Rejected](../../assets/badges/lexvora/rejected.svg) | ![Est XL](../../assets/badges/lexvora/estimate-xl.svg) | Out of scope |

## Findings

A finding is only useful when something downstream consumes it.

| S.No. | Finding | Confidence | Consumed by |
| ---:  | --- | --- | --- |
| 1 | Token rotation must be server-side | ![Risk Low](../../assets/badges/lexvora/risk-low.svg) | `ADR-002` |
| 2 | Per-client quotas beat global quotas | ![Risk Medium](../../assets/badges/lexvora/risk-medium.svg) | `PLAN-03` |

> [!NOTE]
> Promote a confirmed topic into a Concept or a Plan; do not let it sit here.

## Footer Navigation

Parent: [`README.md`](./README.md) · Gallery:
[`theme-asset-gallery.md`](../theme-asset-gallery.md)
