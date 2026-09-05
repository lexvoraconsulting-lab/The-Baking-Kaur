# Enterprise Pricing Intelligence Engine — Overview

`ai/pricing/` is two layers: a complete, live-wired **AI-usage pricing engine** (records AI-provider
token usage and calculates its cost, provider-agnostically and config-driven by default), and a
**domain extension layer** (`ai/pricing/domains/`) generalizing the same Repository+Strategy shape
to every other pricing concern a cake business has — delivery, discounts, corporate rates,
packaging, and more. The AI-usage engine exists because `ai/vision/python/providers.py`'s own
docstring already commits to adding paid providers (Google, OpenAI, Claude) later; the domain layer
exists so the *next* pricing need this business has doesn't start from zero either. Neither layer is
wired into any production Shopify system — see "Scope: no production integration" below.

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
  models.py                  plain dataclasses (TokenUsage, PricingRecord, CostResult, ExecutionAuditRecord, ...)
  models_pydantic.py          validated mirror, used to check ai/pricing/config/*.json at test time
  ids.py                       compute_pricing_id() / compute_audit_id() — deterministic uuid5, no coordination needed
  repository.py                Repository pattern: PricingRepositoryBase (ABC) + FileConfigPricingRepository
  strategy.py                   Strategy pattern: CostCalculationStrategy (ABC) + StandardTokenCostStrategy
  service.py                     PricingService — the one class most AI-usage callers should import
  audit.py                        AuditEngine — appends ExecutionAuditRecord entries to ai/logs/pricing_audit.jsonl
  observability.py                 PricingObserver (ABC) + NullObserver + LoggingObserver — see "Observability" below
  config/                            one JSON file per AI provider, each a dated, versioned rate-card history
  schemas/                            regenerated from models_pydantic.py by test_pricing.py, not hand-edited
  test_pricing.py                     self-check: python -m ai.pricing.test_pricing
  test_observability.py                self-check: python -m ai.pricing.test_observability
  domains/                               extension points for every other pricing concern — see "Domain layer" below
    discounts_promotions.py                real: percentage/flat/tiered-volume/BOGO strategies
    corporate_pricing.py                     real: negotiated flat-rate volume tiers
    delivery.py                               real: distance-band + minimum-order strategy
    recipe_costing.py                          interface-only: no real ingredient cost data exists yet
    packaging.py                                interface-only: no real packaging cost data exists yet
    customization.py                             interface-only: no real customization cost data exists yet
    erp_integration.py                            port-only: no real ERP system to integrate with
    ai_quote_generation.py                          port-only: no real quote specification exists yet
    test_domains.py                                  self-check: python -m ai.pricing.domains.test_domains
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

## Architecture diagram — the full engine

All three parts below share one currency: every strategy, in either layer, takes a plain dataclass
in and returns `ai.pricing.models.CostResult` out. A caller that already knows how to handle
`CostResult.status in {"calculated", "pending_calculation"}` from the AI-usage engine already knows
how to handle a discount, a delivery fee, or a corporate rate quote — that's the concrete meaning of
"provider-agnostic, reusable service" extended to "domain-agnostic."

**1. The AI-usage engine (live-wired into `ai/vision`):**

```
TokenUsage
    |
    v
PricingService --------> PricingRepositoryBase (ABC)
    |                         `-- FileConfigPricingRepository (today)
    |                         `-- a future live-API repository (unwritten)
    |
    `--------------------> CostCalculationStrategy (ABC)
    |                         `-- StandardTokenCostStrategy (linear, today's only one)
    v
CostResult ----> AuditEngine.record(usage, cost) ----> ai/logs/pricing_audit.jsonl
```

**2. The domain extension layer (`ai/pricing/domains/`, zero live callers today):**

```
DiscountStrategy (ABC)              CorporatePricingStrategy (ABC)     DeliveryPricingStrategy (ABC)
  |-- PercentageDiscountStrategy      `-- TieredCorporateRateStrategy    `-- TieredDistanceDeliveryStrategy
  |-- FlatAmountDiscountStrategy         (real, generic, tested)            (real, generic, tested)
  |-- TieredVolumeDiscountStrategy
  `-- BuyXGetYFreeStrategy
     (real, generic, tested)

RecipeCostStrategy (ABC)            PackagingCostStrategy (ABC)        CustomizationCostStrategy (ABC)
  `-- UnconfiguredRecipeCostStrategy  `-- UnconfiguredPackagingCostStrategy `-- UnconfiguredCustomizationCostStrategy
     (interface-only: always Pending,     (interface-only: always Pending,     (interface-only: always Pending,
      no real ingredient cost data)        no real packaging cost data)         no real customization cost data)

ERPPriceSyncPort (ABC)              QuoteGenerationPort (ABC)
  `-- NotConnectedERPPort             `-- NotImplementedQuoteGenerator
     (port only: raises              (port only: raises NotImplementedError -
      NotImplementedError -            no real quote specification exists yet)
      no real ERP system exists)
```

**3. Observability (optional, injected into both PricingService and AuditEngine):**

```
PricingObserver (ABC)
  |-- on_cost_calculated(usage, cost)
  |-- on_cost_pending(usage, cost)
  `-- on_usage_recorded(usage, cost)
        |
        |-- NullObserver        (default - every existing caller is unaffected)
        `-- LoggingObserver     (reference implementation, stdlib logging)
```

## Domain layer — what's real vs. an extension point, and why

Three domains ship a **real, generic, fully tested** strategy because the underlying math needs no
business-specific facts to be correct — the caller always supplies the actual numbers:

- **`discounts_promotions.py`** — percentage, flat-amount, tiered-volume, and buy-X-get-Y-free
  discounts. Universal retail arithmetic, correct for any currency or catalogue.
- **`corporate_pricing.py`** — tiered, negotiated flat-rate pricing keyed by account and volume.
  Returns `CostResult.pending(...)` for an account/quantity with no rate on file, not a guess.
- **`delivery.py`** — distance-banded delivery fees with an optional minimum-order gate. Encodes
  the *shape* of this store's real delivery policy (distance-based, minimum-order-gated, per
  `CLAUDE.md`) without hardcoding any of its actual current rupee figures — those are caller-supplied
  configuration, exactly like the AI-usage engine's own `config/*.json` rate cards.

Five domains are **interface-only extension points** — a real, working, tested `*Strategy`/`*Port`
class exists and is safely callable today, but it always returns `Pending` (or, for the two ports,
raises `NotImplementedError` with a clear message) because completing it would require inventing a
fact nobody has supplied:

| Domain | What's missing | Where it's documented |
|---|---|---|
| `recipe_costing.py` | Real per-ingredient unit costs | module docstring |
| `packaging.py` | Real per-material packaging costs | module docstring |
| `customization.py` | Real per-customization-type rates | module docstring |
| `erp_integration.py` | A real ERP system to connect to (same blocker as `ai/attribute_distribution`'s own ERP stub) | module docstring |
| `ai_quote_generation.py` | A real quote specification and generation approach | module docstring |

This mirrors the exact discipline `CLAUDE.md` already enforces for the storefront itself — no
fabricated GTINs, ratings, or delivery promises — applied to pricing figures instead. An
`Unconfigured*Strategy` is a real class with a real, tested contract; swapping in a real
implementation later changes zero calling code, because the `*Strategy`/`*Port` interface is what
callers actually depend on.

### Adding a tenth domain (the extension point this layer was built for)

1. Define an `Input`/`Context` dataclass with `__post_init__` validation (see any existing domain
   for the pattern).
2. Define a `*Strategy(ABC)` with one `calculate(context) -> CostResult` abstract method, reusing
   `ai.pricing.models.CostResult` — never a new parallel result type.
3. Either implement the real math (if it needs no unverified business fact — see `delivery.py` for
   the bar to clear) or ship an `Unconfigured*Strategy` that returns `CostResult.pending(...)`
   honestly (see `recipe_costing.py`).
4. Add the module to `ai/pricing/domains/` and a test file entry — no change to `models.py`,
   `service.py`, `repository.py`, `strategy.py`, or `audit.py` is ever required for a new domain.

## Observability

`PricingObserver` (`observability.py`) defines three hooks — `on_cost_calculated`,
`on_cost_pending`, `on_usage_recorded` — each a no-op by default, so a concrete observer only
overrides what it needs (the same shape as `logging.Handler`). `PricingService` and `AuditEngine`
both accept an optional `observer=` constructor argument, defaulting to `NullObserver()` — every
existing caller (`ai/vision/python/pipeline.py` calls `PricingService()`/`AuditEngine()` with no
arguments) is unaffected. `LoggingObserver` is the shipped reference implementation (stdlib
`logging`, no new dependency); a future `MetricsObserver` or `TracingObserver` satisfies the same
contract without touching `PricingService`/`AuditEngine` internals.

## Ready for future API exposure

Nothing in this engine is wired to a web server today (see "Scope" below), but the design already
satisfies what an API layer would need without a redesign:

- `PricingService.calculate_cost()` and every domain strategy's `calculate()`/`apply()` take a
  plain dataclass in and return a plain dataclass out — no hidden global state, no side effects
  beyond the optional observer hooks and `AuditEngine`'s explicit, opt-in file write.
- `models_pydantic.py` already defines validated, JSON-Schema-exportable request/response shapes
  for the AI-usage engine (`TokenUsageModel`, `CostResultModel`) — a REST/GraphQL layer wrapping
  `PricingService` would validate incoming requests against these models directly, not redefine them.
- The domain-layer dataclasses (`DiscountContext`, `DeliveryContext`, `CorporatePricingContext`, ...)
  follow the identical shape and would extend the same pattern with their own Pydantic mirrors
  if/when API exposure is actually built.

## Scope: no production integration

This engine is not called from any Shopify theme file, `seo-ops/` script, or live storefront code
path. Its one live caller is `ai/vision/python/pipeline.py` (a local, offline vision-pipeline
smoke-test tool), and even that integration only records AI-token usage/cost for that pipeline's own
Ollama calls — it does not touch product pricing, checkout, or any customer-facing price anywhere in
the store. The domain layer (delivery, discounts, corporate, ...) has **zero live callers** as of
this document — it exists as tested, documented, ready-to-wire-in architecture, per the explicit
instruction that created it.

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
dataclass+Pydantic dual-model convention this module reuses), `ai/attribute_distribution/` (the
sibling package whose own ERP-integration stub shares `erp_integration.py`'s "no real system to
connect to yet" blocker).
