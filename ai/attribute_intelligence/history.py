"""
Enterprise Attribute Intelligence Engine (Build-303) - Attribute History.

WHY THIS MIRRORS ai.pricing.audit.AuditEngine EXACTLY
  Same append-only, one-record-per-line JSONL log in ai/logs/, same
  "records what it's handed, never re-derives it" decoupling (AttributeHistoryLog
  imports nothing from confidence.py/conflicts.py/service.py - it only knows
  how to persist a ResolvedAttribute transition). This repo already settled
  the audit-log question once; reusing the same shape here is the
  composition-over-duplication rule applied to logging infrastructure, not
  just to business logic.

WHY A TRANSITION (previous_value -> new_value), NOT JUST A SNAPSHOT
  "What did this attribute used to be" needs to be answerable without
  replaying every ResolvedAttribute ever produced for a subject - an
  append-only snapshot log would require scanning the whole file and
  reconstructing order; a transition log states the change directly.
"""
import json
from dataclasses import asdict
from pathlib import Path

from ai.attribute_intelligence.models import AttributeHistoryEntry, ResolvedAttribute

DEFAULT_LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "attribute_history.jsonl"


class AttributeHistoryLog:
    def __init__(self, log_path: Path | str = DEFAULT_LOG_PATH):
        self._log_path = Path(log_path)

    def record_transition(
        self, previous: ResolvedAttribute | None, new: ResolvedAttribute,
    ) -> AttributeHistoryEntry:
        entry = AttributeHistoryEntry(
            registry_reference=new.registry_reference, subject_id=new.subject_id,
            previous_value=previous.value if previous else None, new_value=new.value,
            resolution_id=new.resolution_id, recorded_at=new.resolved_at,
        )
        self._append(entry)
        return entry

    def _append(self, entry: AttributeHistoryEntry) -> None:
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")
