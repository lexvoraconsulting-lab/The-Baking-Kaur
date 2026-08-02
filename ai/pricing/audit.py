"""
Enterprise Pricing Service v1 - Audit Engine.

WHY THIS FILE HAS NO IMPORT OF repository.py, strategy.py, OR service.py
  "The Audit Engine must never depend directly on pricing configuration" is
  enforced structurally, not by convention: AuditEngine.record() takes a
  TokenUsage and a CostResult as plain, already-computed values. It has no
  way to read a pricing config file, call PricingService, or know which
  strategy produced the cost - it only knows how to persist what it's handed.
  ai/pricing/test_pricing.py asserts this file imports nothing from
  repository/strategy/service, so the decoupling can't silently regress.

  This also means AuditEngine works identically whether cost came from a
  real PricingService call, a Pending fallback, or (in a future integration)
  a completely different pricing subsystem - it never needed to know.

WHY JSONL, APPENDED, IN ai/logs/
  Matches this repo's existing ai/logs/ directory and its JSON-first
  convention (config files, schema files, examples are all JSON already).
  Append-only, one record per line, is the simplest format that never
  requires reading the whole file back in to add one entry, and is the
  standard shape for an audit trail that should never be edited in place.
"""
import json
from dataclasses import asdict
from pathlib import Path

from ai.pricing.ids import compute_audit_id
from ai.pricing.models import CostResult, ExecutionAuditRecord, TokenUsage

DEFAULT_LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "pricing_audit.jsonl"


class AuditEngine:
    def __init__(self, log_path: Path | str = DEFAULT_LOG_PATH):
        self._log_path = Path(log_path)

    def record(self, usage: TokenUsage, cost: CostResult) -> ExecutionAuditRecord:
        """Always succeeds in producing a record, regardless of cost.status -
        usage is recorded even when cost is Pending. Returns the record it
        wrote so the caller can log/inspect it without re-reading the file."""
        record = ExecutionAuditRecord(
            audit_id=compute_audit_id(
                usage.provider, usage.model, usage.recorded_at,
                usage.input_tokens, usage.output_tokens, usage.request_id,
            ),
            usage=usage,
            cost=cost,
            recorded_at=usage.recorded_at,
        )
        self._append(record)
        return record

    def _append(self, record: ExecutionAuditRecord) -> None:
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record)) + "\n")
