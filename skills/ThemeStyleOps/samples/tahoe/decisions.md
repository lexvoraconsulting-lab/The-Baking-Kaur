<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/tahoe/decisions-dark.svg">
  <img alt="Decisions" src="../../assets/banners/tahoe/decisions-light.svg" width="100%">
</picture>

# Decisions

Accepted direction for Client Portal Platform, with rationale and consequence.

## Navigation

Parent: [`README.md`](./README.md) · Theme:
[`macOS Tahoe Liquid Glass`](../../references/macos-tahoe-liquid-glass.md) ·
Rules: [`banner-and-badge-system.md`](../../references/banner-and-badge-system.md)

## Table of Contents

- [Navigation](#navigation)
- [Status Summary](#status-summary)
- [Decision Register](#decision-register)
- [Footer Navigation](#footer-navigation)

## Status Summary

Counted from the tables below. The bold `Total` row must always sum them.

| S.No. | Status | Count |
| ---: | --- | ---: |
| 1 | Confirmed | 2 |
| 2 | Proposed | 2 |
| 3 | Superseded | 1 |
| **Total** | **Tracked records** | **5** |

## Decision Register

A decision without a consequence line is not a decision.

| S.No. | ID | Decision | State | Consequence |
| ---:  | --- | --- | --- | --- |
| 1 | `ADR-001` | SSO is mandatory for every tier | ![Confirmed](../../assets/badges/tahoe/confirmed.svg) | No password login path is built. |
| 2 | `ADR-002` | Sessions are server-side, rotated hourly | ![Confirmed](../../assets/badges/tahoe/confirmed.svg) | Needs shared session storage. |
| 3 | `ADR-003` | Quotas are enforced per client, not globally | ![Proposed](../../assets/badges/tahoe/proposed.svg) | Adds the quota service. |
| 4 | `ADR-004` | Store reports in the primary database | ![Superseded](../../assets/badges/tahoe/superseded.svg) | Replaced by `ADR-005`. |
| 5 | `ADR-005` | Reports move to a separate store | ![Proposed](../../assets/badges/tahoe/proposed.svg) | Adds an export pipeline. |

> [!NOTE]
> Supersede a decision with a new record. Never edit an accepted one in place.

## Footer Navigation

Parent: [`README.md`](./README.md) · Gallery:
[`theme-asset-gallery.md`](../theme-asset-gallery.md)
