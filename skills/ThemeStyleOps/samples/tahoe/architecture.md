<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/tahoe/architecture-dark.svg">
  <img alt="Architecture" src="../../assets/banners/tahoe/architecture-light.svg" width="100%">
</picture>

# Architecture

Systems, boundaries, and dependencies for Client Portal Platform.

## Navigation

Parent: [`README.md`](./README.md) · Theme:
[`macOS Tahoe Liquid Glass`](../../references/macos-tahoe-liquid-glass.md) ·
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
| 1 | Edge gateway | ![Current](../../assets/badges/tahoe/arch-current.svg) | Platform | Handles auth and routing. |
| 2 | Client service | ![Current](../../assets/badges/tahoe/arch-current.svg) | Platform | Owns client records. |
| 3 | Quota service | ![Target](../../assets/badges/tahoe/arch-target.svg) | Platform | Agreed in `ADR-003`, not built. |
| 4 | Reporting store | ![TBD](../../assets/badges/tahoe/arch-tbd.svg) | Unassigned | Shape not decided. |
| 5 | Legacy billing bridge | ![Deprecated](../../assets/badges/tahoe/deprecated.svg) | Finance | Removed after the v2 cutover. |

## Dependencies

A dependency you cannot name is a dependency you cannot manage.

| S.No. | Depends on | Direction | Risk |
| ---:  | --- | --- | --- |
| 1 | Finance API v2 | Outbound | ![Risk High](../../assets/badges/tahoe/risk-high.svg) |
| 2 | Identity provider | Inbound | ![Risk Medium](../../assets/badges/tahoe/risk-medium.svg) |
| 3 | Object storage | Outbound | ![Risk Low](../../assets/badges/tahoe/risk-low.svg) |

> [!NOTE]
> Keep this file honest about `Current` versus `Target`; that gap is the real backlog.

## Footer Navigation

Parent: [`README.md`](./README.md) · Gallery:
[`theme-asset-gallery.md`](../theme-asset-gallery.md)
