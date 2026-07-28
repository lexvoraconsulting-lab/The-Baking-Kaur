"""
Enterprise Attribute Distribution v1 (Build-004) - conflict detection.

WHY
  BL-3. Composed after resolve_distribution() (BL-2), not merged into it -
  keeps "resolve a payload" and "check it against downstream state" as two
  separable pure concerns. Serves the roadmap's own Build-004 exit criterion
  ("conflict handling when a downstream system's own value diverges from
  EAL's") without performing any real downstream read itself - that stays
  BL-4/BL-5's job. Pure function: no HTTP, no Shopify/ERP calls, no
  database, no file writes, no AI calls, no retries.

CurrentDownstreamValue.known mirrors EAL's own value_state three-state
distinction (present/null/unknown, see
docs/20_Attribute_Language/Null_and_Unknown_Standard.md) - "no real read has
been attempted yet" is not the same fact as "the value is empty," so it is
modeled the same way EAL already models that distinction, not a second one.
"""
from dataclasses import dataclass
from typing import Any

from ai.attribute_distribution.models_pydantic import DistributionRecordModel


@dataclass(frozen=True)
class CurrentDownstreamValue:
    known: bool
    value: Any = None


def detect_conflict(
    record: DistributionRecordModel, current: CurrentDownstreamValue
) -> DistributionRecordModel:
    if record.status != "dry_run":
        raise ValueError(
            f"detect_conflict() requires a resolved record (status='dry_run'), "
            f"got status={record.status!r}"
        )

    if not current.known or current.value == record.value:
        return record

    data = record.model_dump()
    data["status"] = "conflict"
    data["notes"] = (
        f"downstream value {current.value!r} diverges from resolved value {record.value!r}"
    )
    return DistributionRecordModel(**data)
