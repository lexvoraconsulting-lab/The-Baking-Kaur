"""
Enterprise Attribute Registry (EAR) v1 - whole-registry validation.

WHY
  Per-entry shape (datatype, eal_reference grammar, status/deprecated_in
  consistency) is already enforced by EARAttributeEntryModel's own validators
  at construction time - a bad single entry never reaches here. This module
  only checks invariants that require seeing every entry at once: no two
  entries may claim the same attribute_id, and no two entries may claim the
  same (namespace, canonical_name) pair, since a namespace-scoped name must
  resolve to exactly one attribute.
  See docs/40_Enterprise_Attribute_Registry/Registry_Model.md.

WHAT IS NOT VALIDATED HERE (deliberately deferred)
  taxonomy_references / validation_profile / definition_reference are not
  checked against any live registry - Sprint 2.2 taxonomy content and
  Build-003 (EAD) don't exist yet. See
  docs/40_Enterprise_Attribute_Registry/Validation.md.
"""
from ai.ear.ids import is_valid_attribute_id
from ai.ear.models_pydantic import EARAttributeEntryModel


def validate_registry(entries: list[EARAttributeEntryModel]) -> None:
    seen_ids: dict[str, str] = {}
    seen_names: dict[tuple[str, str], str] = {}

    for entry in entries:
        if not is_valid_attribute_id(entry.attribute_id):
            raise ValueError(
                f"attribute_id {entry.attribute_id!r} does not match ^EAR-\\d{{6}}$"
            )

        if entry.attribute_id in seen_ids:
            raise ValueError(
                f"duplicate attribute_id {entry.attribute_id!r}: claimed by both "
                f"{seen_ids[entry.attribute_id]!r} and {entry.eal_reference!r}"
            )
        seen_ids[entry.attribute_id] = entry.eal_reference

        name_key = (entry.namespace, entry.canonical_name)
        if name_key in seen_names:
            raise ValueError(
                f"duplicate (namespace, canonical_name) {name_key!r}: claimed by both "
                f"{seen_names[name_key]!r} and {entry.attribute_id!r}"
            )
        seen_names[name_key] = entry.attribute_id
