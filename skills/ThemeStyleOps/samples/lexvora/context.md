<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/lexvora/context-dark.svg">
  <img alt="Context" src="../../assets/banners/lexvora/context-light.svg" width="100%">
</picture>

# Context

Where Client Portal Platform stands right now, and what is assumed.

## Navigation

Parent: [`README.md`](./README.md) · Theme:
[`Lexvora Company`](../../references/lexvora-company.md) ·
Rules: [`banner-and-badge-system.md`](../../references/banner-and-badge-system.md)

## Table of Contents

- [Navigation](#navigation)
- [Status Summary](#status-summary)
- [Current State](#current-state)
- [Working Assumptions](#working-assumptions)
- [Footer Navigation](#footer-navigation)

## Status Summary

Counted from the tables below. The bold `Total` row must always sum them.

| S.No. | Status | Count |
| ---: | --- | ---: |
| 1 | Confirmed | 1 |
| 2 | Draft | 1 |
| 3 | In Delivery | 1 |
| 4 | On Hold | 1 |
| **Total** | **Tracked records** | **4** |

## Current State

What is true today, not what is intended.

| S.No. | Area | State | Note |
| ---:  | --- | --- | --- |
| 1 | Authentication | ![Confirmed](../../assets/badges/lexvora/confirmed.svg) | Single sign-on is live for internal users. |
| 2 | Client onboarding | ![In Delivery](../../assets/badges/lexvora/in-delivery.svg) | Two of five screens are built. |
| 3 | Reporting | ![Draft](../../assets/badges/lexvora/draft.svg) | Requirements captured, not evaluated. |
| 4 | Billing export | ![On Hold](../../assets/badges/lexvora/on-hold.svg) | Waiting on the finance system upgrade. |

## Working Assumptions

Each assumption is a risk until it is confirmed.

| S.No. | Assumption | Risk | Owner |
| ---:  | --- | --- | --- |
| 1 | The finance API stays on v2 until Q4 | ![Risk High](../../assets/badges/lexvora/risk-high.svg) | Architect |
| 2 | Client count stays under 500 | ![Risk Low](../../assets/badges/lexvora/risk-low.svg) | Delivery lead |
| 3 | No offline mode is required | ![Risk Medium](../../assets/badges/lexvora/risk-medium.svg) | Product |

> [!NOTE]
> Update this file whenever reality moves. A stale context file is worse than none.

## Footer Navigation

Parent: [`README.md`](./README.md) · Gallery:
[`theme-asset-gallery.md`](../theme-asset-gallery.md)
