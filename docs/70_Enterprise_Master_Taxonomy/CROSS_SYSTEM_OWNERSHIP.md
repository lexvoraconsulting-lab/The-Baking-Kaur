# Cross-System Ownership — items explicitly excluded from taxonomy content

Build-005, BL-1. Per the BL-1 scope reconciliation: several concepts raised during BL-1 planning
belong to another subsystem's ownership, not the taxonomy. Recorded here instead of building
duplicate taxonomy-side structures for them — this document is the pointer, not a spec.

| Concept | Classification | Real owner |
|---|---|---|
| Pricing | Business logic | Not built yet — a future ERP/Shopify integration concern, never taxonomy content |
| Manufacturing, Production | Business process | Kitchen ERP (external, uninspected — EPR Risk R-3) |
| Inventory | Business process | Shopify inventory / ERP, not modeled here |
| Ingredients (as supply chain) | Business process | ERP procurement — distinct from `Flavour`/`Sponge`/`Filling`/`Dietary`/`Allergens` Attribute Groups, which describe the *taxonomy* content those processes consume |
| Shelf Life, Storage, Transport | Business process | Operational/logistics, not attribute vocabulary |
| Quality (QA) | Business process | Operational, not an image/product attribute |
| Photography | Production process | Studio workflow — content BL-1 authors is what gets *photographed*, not the photography process itself |
| Delivery | Cross-System Consumer | `CLAUDE.md`'s local delivery system (Meerut, distance-based fees) — storefront track, never merges with this platform |
| SEO | Cross-System Consumer | The entire Shopify storefront theme track (`docs/ARCHITECTURE.md`, `docs/CODING_STANDARDS.md`) — explicitly separate, per `CLAUDE.md`'s "the two tracks must never be merged" |
| AI Vision | External Consumer | Build-008 (Vision Extraction) — a *consumer* of this taxonomy's content, not a producer of it |
| Search | External Consumer | Build-009 (Embeddings/Search) — consumes `Term.external_ids` where `system="search"`, doesn't own taxonomy structure |
| Shopify | Integration Target | Build-004 (Attribute Distribution), frozen — writes resolved values to Shopify; this taxonomy only supplies `external_ids` labels for it to resolve against |
| ERP | Integration Target | Build-004 (Attribute Distribution) + Kitchen ERP (external) — same relationship as Shopify above |
| Marketing | Future Work | No Build assigned yet — likely JARVIS (Build-011) territory |
| Compliance | Future Work | No Build assigned yet — FSSAI/regulatory concerns are a storefront-track matter (`CLAUDE.md`'s "Blocked on the client" section), not taxonomy content |

## Why this table exists

`Attribute_Group_Architecture.md`'s own rule: "a new group is justified only when it has a real
Attribute to hold, not spun up speculatively." None of the above have a real *taxonomy* Attribute —
they're either processes, other Builds' entire responsibility, or not-yet-assigned future work. This
table is the record that they were considered and deliberately excluded, not overlooked.

## Related Standards

[SPRINT_CHARTER.md](SPRINT_CHARTER.md) (the BL-1 scope-reconciliation decision this table
implements), [Attribute_Group_Architecture.md](../10_Taxonomy/Attribute_Group_Architecture.md)
(the rule being applied).
