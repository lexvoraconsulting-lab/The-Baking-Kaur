"""
Enterprise Pricing Service v1 - pricing repository (Repository pattern).

WHY AN ABC HERE, LIKE ai.vision.python.providers.VisionProvider
  PricingService depends on "something that can answer get_pricing()", not on
  "a JSON file on disk" - the same separation VisionProvider already
  establishes between "call a vision model" and "which vision model."
  FileConfigPricingRepository is the only tenant today (config-driven pricing
  is the explicit default), but the seam is what "allow future integration
  with provider pricing APIs without changing business logic" means
  concretely: a LivePricingRepository calling OpenAI's/Anthropic's pricing
  endpoint, or a CachingPricingRepository wrapping either, satisfies the same
  ABC and PricingService never changes.

WHY "MOST RECENT record WHERE effective_date <= as_of"
  A rate card is a time series, not a single value - "the $5/1M price that
  started 2026-03-01" must still be resolvable when auditing a call made on
  2026-02-15 even after a 2026-06-01 price change is added to the same file.
  This is exactly what "historical audit records must preserve the pricing
  version used at execution time" requires the repository to support.
"""
import json
from abc import ABC, abstractmethod
from pathlib import Path

from ai.pricing.ids import compute_pricing_id
from ai.pricing.models import PriceComponent, PricingRecord

DEFAULT_CONFIG_DIR = Path(__file__).parent / "config"


class PricingRepositoryBase(ABC):
    @abstractmethod
    def get_pricing(self, provider: str, model: str, as_of: str | None = None) -> PricingRecord | None:
        """The most recent PricingRecord for (provider, model) with
        effective_date <= as_of, or the most recent record overall when
        as_of is None. Returns None - never raises - when nothing is on
        file; PricingService is what turns that into a Pending CostResult."""


class FileConfigPricingRepository(PricingRepositoryBase):
    """Default, config-driven implementation. One file per provider
    (ai/pricing/config/<provider>.json), each holding every historical and
    current rate-card entry for every model that provider serves."""

    def __init__(self, config_dir: Path | str = DEFAULT_CONFIG_DIR):
        self._config_dir = Path(config_dir)
        self._cache: dict[str, list[PricingRecord]] = {}

    def _load_provider(self, provider: str) -> list[PricingRecord]:
        if provider in self._cache:
            return self._cache[provider]
        path = self._config_dir / f"{provider}.json"
        if not path.exists():
            self._cache[provider] = []
            return []
        raw = json.loads(path.read_text(encoding="utf-8"))
        records = [_record_from_dict(entry) for entry in raw.get("records", [])]
        for record in records:
            if record.provider != provider:
                raise ValueError(
                    f"{path}: record for model={record.model!r} declares "
                    f"provider={record.provider!r}, expected {provider!r} (filename mismatch)"
                )
        self._cache[provider] = records
        return records

    def get_pricing(self, provider: str, model: str, as_of: str | None = None) -> PricingRecord | None:
        candidates = [r for r in self._load_provider(provider) if r.model == model]
        if as_of is not None:
            candidates = [r for r in candidates if r.effective_date <= as_of]
        if not candidates:
            return None
        return max(candidates, key=lambda r: r.effective_date)

    def invalidate_cache(self) -> None:
        """Call after editing a config file mid-process (tests only in
        practice - a real deployment loads once per process)."""
        self._cache.clear()


def _record_from_dict(entry: dict) -> PricingRecord:
    provider = entry["provider"]
    input_price = PriceComponent(**entry["input_price"])
    output_price = PriceComponent(**entry["output_price"])
    categories = {
        name: PriceComponent(**value) for name, value in entry.get("categories", {}).items()
    }
    return PricingRecord(
        provider=provider,
        model=entry["model"],
        version=entry["version"],
        effective_date=entry["effective_date"],
        currency=entry["currency"],
        input_price=input_price,
        output_price=output_price,
        categories=categories,
        pricing_id=compute_pricing_id(provider, entry["model"], entry["version"], entry["effective_date"]),
    )
