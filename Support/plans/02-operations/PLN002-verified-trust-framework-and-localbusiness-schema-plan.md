# Plan — Verified Trust Framework and LocalBusiness Schema (`TRST`)

> **Parent:** [`../plans-master.md`](../plans-master.md) · **Code:** `TRST`
> **Status:** Active · **Owner:** SEO & Compliance Team

## Sources and Traceability

| S.No. | Code | Source record | Plan role | Status |
| ---: | --- | --- | --- | --- |
| 1 | `RUL` | [`../../rules.md`](../../rules.md) | Binding constraints and governance | Current |
| 2 | `CON` | [`../../concept-design/CON004_Verified_Trust_Framework_Fssai_Entity_Concept.md`](../../concept-design/CON004_Verified_Trust_Framework_Fssai_Entity_Concept.md) | Trust framework and LocalBusiness schema specification | Current |

## Statistics

`TL = PD + IP + CD`. From task markers below.

| S.No. | Plan Scope | TL | PD | IP | CD |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `TRST` direct tasks | 6 | 6 | 0 | 0 |
| 2 | Total | **6** | **6** | **0** | **0** |

## Context

Implement authentic Google Business Profile review curation module, display official 14-digit FSSAI licence registration badge in footer, and inject `snippets/bk-local-business.liquid` LocalBusiness JSON-LD schema into `<head>` with verified Meerut geo-coordinates (`28.9845, 77.7064`) to build local trust and GEO entity authority.

## 01. Trust & Schema Tasks

- [ ] `TRST-01.01` Reconcile canonical NAP and verify Google Maps place coordinates for Thapar Nagar, Meerut.
- [ ] `TRST-01.02` Deploy `snippets/bk-local-business.liquid` with verified coordinates and FSSAI entity properties.
- [ ] `TRST-01.03` Inject `{% render 'bk-local-business' %}` into `<head>` of `layout/theme.liquid`.
- [ ] `TRST-01.04` Add official FSSAI registration badge and licence display block in site footer.
- [ ] `TRST-01.05` Build GBP review showcase module rendering genuine customer reviews with direct Google Maps link.
- [ ] `TRST-01.06` Validate schema using Google Rich Results Test and verify zero schema duplication against `snippets/structured-data.liquid`.

## Footer Navigation

Parent: [`../plans-master.md`](../plans-master.md) · Plans Master: [`../plans-master.md`](../plans-master.md)
