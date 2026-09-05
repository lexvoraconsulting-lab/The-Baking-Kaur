<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/lexvora/architecture-dark.svg">
  <img alt="Architecture" src="../../assets/banners/lexvora/architecture-light.svg" width="100%">
</picture>

# Architecture

Systems, boundaries, and dependencies for Client Portal Platform.

## Navigation

Parent: [`README.md`](./README.md) · Theme:
[`Lexvora Company`](../../references/lexvora-company.md) ·
Rules: [`banner-and-badge-system.md`](../../references/banner-and-badge-system.md)

## Table of Contents

- [Navigation](#navigation)
- [Status Summary](#status-summary)
- [Components](#components)
- [Dependencies](#dependencies)
- [Footer Navigation](#footer-navigation)

## Status Summary

Counted from the tables below. The bold `Total` row must always sum them.

| S.No. | Status | Count |
| ---: | --- | ---: |
| 1 | Current | 2 |
| 2 | Deprecated | 1 |
| 3 | TBD | 1 |
| 4 | Target | 1 |
| **Total** | **Tracked records** | **5** |

## Components

Current is what runs. Target is what is agreed. Nothing else is real.

| S.No. | Component | State | Owner | Note |
| ---:  | --- | --- | --- | --- |
| 1 | Edge gateway | ![Current](../../assets/badges/lexvora/arch-current.svg) | Platform | Handles auth and routing. |
| 2 | Client service | ![Current](../../assets/badges/lexvora/arch-current.svg) | Platform | Owns client records. |
| 3 | Quota service | ![Target](../../assets/badges/lexvora/arch-target.svg) | Platform | Agreed in `ADR-003`, not built. |
| 4 | Reporting store | ![TBD](../../assets/badges/lexvora/arch-tbd.svg) | Unassigned | Shape not decided. |
| 5 | Legacy billing bridge | ![Deprecated](../../assets/badges/lexvora/deprecated.svg) | Finance | Removed after the v2 cutover. |

## Dependencies

A dependency you cannot name is a dependency you cannot manage.

| S.No. | Depends on | Direction | Risk |
| ---:  | --- | --- | --- |
| 1 | Finance API v2 | Outbound | ![Risk High](../../assets/badges/lexvora/risk-high.svg) |
| 2 | Identity provider | Inbound | ![Risk Medium](../../assets/badges/lexvora/risk-medium.svg) |
| 3 | Object storage | Outbound | ![Risk Low](../../assets/badges/lexvora/risk-low.svg) |

> [!NOTE]
> Keep this file honest about `Current` versus `Target`; that gap is the real backlog.

## Footer Navigation

Parent: [`README.md`](./README.md) · Gallery:
[`theme-asset-gallery.md`](../theme-asset-gallery.md)
