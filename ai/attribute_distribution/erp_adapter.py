"""
Enterprise Attribute Distribution v1 (Build-004) - ERP Adapter layer.

WHY
  BL-5. `ERPAdapter` is the ERP counterpart to BL-4's `ShopifyAdapter`, same
  class-based shape for consistency and the same future-extensibility intent
  (a real submit/read is added as a new method later, never a rename).
  Deliberately thinner than ShopifyAdapter: TBK Kitchen ERP's real write API
  is unknown to this platform (Enterprise Program Roadmap, Section 13 / Risk
  R-3) - this class cannot shape a realistic ERP payload because no real
  shape has been inspected yet. It proves the interface seam exists; it does
  not guess at ERP's field names, authentication, or write semantics.

SCOPE (BL-5)
  Fully stubbed. No network call, no database write, no file write, no
  external side effect of any kind - stub_submit() only counts what it would
  have submitted.
"""
from ai.attribute_distribution.models_pydantic import DistributionRecordModel


class ERPAdapter:
    def stub_submit(self, records: list[DistributionRecordModel]) -> int:
        """Count ERP-target, dry_run records that would be submitted to TBK
        Kitchen ERP. Performs no I/O, no network call, no database write -
        a pure count, since no real ERP write path exists yet (Risk R-3)."""
        return sum(
            1 for r in records if r.target_system == "erp" and r.status == "dry_run"
        )
