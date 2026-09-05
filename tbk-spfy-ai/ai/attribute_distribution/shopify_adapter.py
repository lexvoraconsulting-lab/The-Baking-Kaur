"""
Enterprise Attribute Distribution v1 (Build-004) - Shopify Adapter layer.

WHY
  BL-4. `ShopifyAdapter` is the one place every Shopify-facing responsibility
  for this Build lives - not a bare "exporter" function. BL-4 implements only
  dry-run review-artifact writing; future responsibilities (preview, export,
  import, validation, sync, real Admin API integration - later Builds, not
  this one) are added as new methods on this same class, never a rename or a
  second module. Named "adapter" deliberately, distinct from
  ai.{eal,ear,ead}.exporter (JSON/YAML serialization of a module's own
  records) - this class does not serialize this module's own state, it
  shapes a preview of what would be sent to an external system.

SCOPE (BL-4)
  Dry-run only. No network call of any kind - not even a GET. Writes a local
  review artifact describing what a future real write would send, mirroring
  this repo's own seo-ops/ dry-run-by-default convention
  (docs/CODING_STANDARDS.md). No credentials are read or held anywhere in
  this class.
"""
from pathlib import Path

from ai.attribute_distribution.models_pydantic import DistributionRecordModel


class ShopifyAdapter:
    def write_review_artifact(
        self, records: list[DistributionRecordModel], path: str | Path
    ) -> int:
        """Write one JSON object per line for every dry_run, Shopify-target
        record in `records`. Records targeting a different system, or not in
        status='dry_run', are skipped - not written, not an error. Returns
        the number of records written."""
        eligible = [
            r for r in records if r.target_system == "shopify" and r.status == "dry_run"
        ]
        with open(path, "w", encoding="utf-8") as f:
            for record in eligible:
                f.write(record.model_dump_json())
                f.write("\n")
        return len(eligible)
