# Enterprise Pricing Service — Overview

`ai/pricing/` records AI-provider token usage and calculates its cost, provider-agnostically and
config-driven by default. It exists because `ai/vision/python/providers.py`'s own docstring already
commits to adding paid providers (Google, OpenAI, Claude) later — this is the module that means
that addition never has to answer "and how do we track what it costs" from scratch.

## The four hard requirements this design is built around

1. **Token usage is always recorded**, even when nothing is known about pricing. `TokenUsage` is
   independently constructible from `CostResult` for exactly this reason.
2. **Cost calculation is separated from token collection.** Capturing usage
   (`ai.pricing.models.TokenUsage`) and pricing it (`ai.pricing.service.PricingService`) are two
   classes with two different reasons to change.
3. **A pricing failure never fails the calling code.** `PricingService.calculate_cost()` cannot
   raise — a missing rate card, an unknown model, or a corrupt config file all collapse to
   `CostResult.pending(reason)`, never an exception.
4. **The Audit Engine never depends on pricing configuration.** `ai/pricing/audit.py` imports only
   plain data types (`TokenUsage`, `CostResult`) — never `repository.py`, `strategy.py`, or
   `service.py`. `test_pricing.py` enforces this by parsing `audit.py`'s own AST, not by trusting a
   docstring promise.

## Package layout

```
ai/pricing/
  models.py             plain dataclasses (TokenUsage, PricingRecord, CostResult, ExecutionAuditRecord, ...)
  models_pydantic.py     validated mirror, used to check ai/pricing/config/*.json at test time
  ids.py                  compute_pricing_id() / compute_audit_id() — deterministic uuid5, no coordination needed
  repository.py           Repository pattern: PricingRepositoryBase (ABC) + FileConfigPricingRepository
  strategy.py              Strategy pattern: CostCalculationStrategy (ABC) + StandardTokenCostStrategy
  service.py                PricingService — the one class most callers should import
  audit.py                   AuditEngine — appends ExecutionAuditRecord entries to ai/logs/pricing_audit.jsonl
  config/                     one JSON file per provider, each a dated, versioned rate-card history
  schemas/                     regenerated from models_pydantic.py by test_pricing.py, not hand-edited
  test_pricing.py                self-check: python -m ai.pricing.test_pricing
```

## How the pieces compose

```
provider response
      │
      ▼
TokenUsage  ────────────────►  AuditEngine.record(usage, cost)  ──► ai/logs/pricing_audit.jsonl
      │                                    ▲
      ▼                                    │
PricingService.calculate_cost(usage)  ─────┘
      │
      ├─► FileConfigPricingRepository.get_pricing(provider, model, as_of)
      │        reads ai/pricing/config/<provider>.json, resolves the record whose
      │        effective_date is the most recent one on-or-before `as_of`
      │
      └─► StandardTokenCostStrategy.calculate(usage, pricing)
               sum(unit_price × token_count) per category present in both
               usage and the resolved PricingRecord
```

`calculate_cost()` always returns a `CostResult` — `status="calculated"` with a real `total_cost`
and `pricing_version`, or `status="pending_calculation"` with a `reason` and no cost. Either way,
`AuditEngine.record(usage, cost)` is the correct next call — usage is preserved regardless.

## Adding a real, paid provider later (the extensibility point this was built for)

1. Add a `VisionProvider` subclass in `ai/vision/python/providers.py` (or an equivalent client
   elsewhere) that returns real `input_tokens`/`output_tokens`/etc. from that provider's response —
   `OllamaProvider` already does this for the one live provider today (see `ProviderResponse` in
   `providers.py`).
2. Add or update `ai/pricing/config/<provider>.json` with a real, verified rate card — every
   config file this module ships marks its `source_note` as illustrative and unverified
   specifically so nobody mistakes a placeholder number for a confirmed one; replace the note once
   real rates are entered.
3. Nothing else changes. `PricingService`, `StandardTokenCostStrategy`, and `AuditEngine` are
   already provider-agnostic — no business logic depends on which provider a `TokenUsage` came from.

## Future integration with a live provider pricing API

`PricingRepositoryBase` is the seam: `FileConfigPricingRepository` is today's only implementation,
but any class satisfying `get_pricing(provider, model, as_of) -> PricingRecord | None` can replace
it — e.g. a `LivePricingRepository` calling a provider's pricing endpoint, or a caching wrapper
around either. `PricingService(repository=...)` accepts any of them; nothing downstream changes.

## Currency, units, and precision

Every rate is expressed as an explicit `(unit_price, unit)` pair
(`per_token` / `per_1k_tokens` / `per_1m_tokens`) rather than a bare float — real provider rate
cards are published per-1M-tokens, and doing float arithmetic on numbers like `0.0000006` both
loses precision and is unreadable in a config file. `PriceComponent.cost_for(token_count)` divides
by the correct denominator before multiplying, so config authors write the number exactly as the
provider publishes it.

## Related

[VisionPipeline.md](VisionPipeline.md), [FolderStructure.md](FolderStructure.md) (the `providers.py`
"no `providers/` package yet" precedent this module's own flat-file layout follows),
[../20_Attribute_Language/EAL_SPECIFICATION.md](../20_Attribute_Language/EAL_SPECIFICATION.md) (the
dataclass+Pydantic dual-model convention this module reuses).
