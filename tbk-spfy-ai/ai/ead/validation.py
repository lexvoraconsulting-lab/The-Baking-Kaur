"""
Enterprise Attribute Definitions (EAD) v1 - whole-set validation.

WHY
  Per-entry shape (registry_reference format, confidence range, required
  fields) is already enforced by EADDefinitionModel's own validators at
  construction time. This module only checks the one invariant that requires
  seeing every entry at once: no two Definitions describe the same EAR
  attribute - mirrors ai/ear/validation.py's duplicate-attribute_id check.

WHAT IS NOT VALIDATED HERE (deliberately deferred)
  allowed_values / knowledge_graph_reference are not checked against any live
  taxonomy or Knowledge Graph - Sprint 2.2 content and the Knowledge Graph
  (Build-005) don't exist yet. See
  docs/50_Enterprise_Attribute_Definitions/Validation.md. This build also
  does not implement a validation engine (per its own Constraints) - it
  enforces its own record shape only.
"""
from ai.ead.models_pydantic import EADDefinitionModel


def validate_definition_set(definitions: list[EADDefinitionModel]) -> None:
    seen: dict[str, str] = {}
    for d in definitions:
        if d.registry_reference in seen:
            raise ValueError(
                f"duplicate registry_reference {d.registry_reference!r}: claimed by both "
                f"{seen[d.registry_reference]!r} and {d.definition_id!r}"
            )
        seen[d.registry_reference] = d.definition_id
