<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/banners/lexvora/rules-dark.svg">
  <img alt="Rules" src="../../assets/banners/lexvora/rules-light.svg" width="100%">
</picture>

# Rules

Binding constraints for everyone working on Client Portal Platform.

## Navigation

Parent: [`README.md`](./README.md) · Theme:
[`Lexvora Company`](../../references/lexvora-company.md) ·
Rules: [`banner-and-badge-system.md`](../../references/banner-and-badge-system.md)

## Table of Contents

- [Navigation](#navigation)
- [Status Summary](#status-summary)
- [Binding Rules](#binding-rules)
- [Footer Navigation](#footer-navigation)

## Status Summary

Counted from the tables below. The bold `Total` row must always sum them.

| S.No. | Status | Count |
| ---: | --- | ---: |
| 1 | Confirmed | 4 |
| 2 | Proposed | 1 |
| **Total** | **Tracked records** | **5** |

## Binding Rules

These are not suggestions. Breaking one requires a Decision record.

| S.No. | Rule | Applies to | State |
| ---:  | --- | --- | --- |
| 1 | No client data in logs, ever | All code | ![Confirmed](../../assets/badges/lexvora/confirmed.svg) |
| 2 | Every schema change ships with a reversible migration | Database | ![Confirmed](../../assets/badges/lexvora/confirmed.svg) |
| 3 | Every Plan task links to a source record | Documentation | ![Confirmed](../../assets/badges/lexvora/confirmed.svg) |
| 4 | Secrets never enter process arguments | All code | ![Confirmed](../../assets/badges/lexvora/confirmed.svg) |
| 5 | Public API changes need an accepted Decision first | API | ![Proposed](../../assets/badges/lexvora/proposed.svg) |

> [!NOTE]
> A rule that quietly disappears is worse than one that never existed. Retire rules explicitly.

## Footer Navigation

Parent: [`README.md`](./README.md) · Gallery:
[`theme-asset-gallery.md`](../theme-asset-gallery.md)
