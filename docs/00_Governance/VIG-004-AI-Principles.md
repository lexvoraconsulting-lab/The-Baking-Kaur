# VIG-004: AI Principles

Status: Active
Version: 1.0

## Purpose

States how the platform must relate to AI providers and AI-generated output, so that no module,
prompt, or vendor integration ever becomes a single point of failure or a hidden decision-maker.

## Scope

Applies to every use of an AI provider anywhere in the platform: vision models, language models,
embedding models, and any future model type, regardless of vendor or deployment (local or hosted).

## Definitions

- **AI Provider**: any local or hosted model invoked to produce an observation (see VIG-000) —
  e.g. Ollama, Google Gemini, OpenAI, Claude, Azure OpenAI, or a future provider.
- **Prompt**: the instruction given to an AI provider describing what to observe.
- **Business Logic**: any rule that determines an outcome affecting the business (pricing,
  merchandising, customer-facing claims) independent of what a specific image or input contains.

## Principles

1. AI providers are interchangeable. No module's correctness may depend on a specific vendor's
   behavior, output format, or availability.
2. AI output is evidence, not verified fact, until it passes the verification gate in VIG-007.
3. Business logic never lives inside a prompt. A prompt asks a model what it observes; it does not
   instruct the model to apply a business rule the platform could not independently audit.
4. No module may assume permanent availability, pricing, or behavior of any one AI vendor. A
   provider outage or deprecation must be recoverable by configuration change, not code rewrite.
5. Local and hosted providers are treated identically by the interface a module calls through — the
   distinction between "runs on our hardware" and "runs on a vendor's hardware" is a configuration
   detail, not an architectural one.

## Rules

- Every AI provider call happens through the interface defined for its capability (VIG-002
  Principle 2), never as a direct, ad hoc call from application logic.
- No prompt may contain a business rule that determines a customer-facing outcome (price, claimed
  certification, delivery promise) without that rule also existing, auditable, outside the prompt.
- No module may hardcode assumptions about a specific provider's output format into logic shared
  by other providers; provider-specific parsing stays inside that provider's implementation.

## Examples

- A prompt instructs a vision model to describe visible decorations, colors, and shape. It does not
  instruct the model to decide which occasion the product should be marketed for — that mapping
  happens afterward, in code, auditable and testable. Correct.
- Switching from a local Ollama model to a hosted Gemini model for the same capability requires a
  new provider class and a configuration change, with zero changes to any consuming module. Correct.

## Non-examples

- A prompt says "if the cake looks expensive, describe it as premium" and that description flows
  directly into a price tier decision. Violates Principle 3.
- A downstream module parses a specific vendor's exact response envelope (e.g. a particular JSON
  field only that vendor returns) directly, instead of through a provider-specific adapter. Violates
  Principle 1 and VIG-002 Principle 2.

## Implementation Guidance

When a new AI capability is introduced, its interface should be designed by asking: "if this vendor
disappeared tomorrow, what would have to change?" The answer should be limited to one new class and
one configuration value (VIG-002), never a rewrite of any consuming module's logic.

## Future Compatibility

This document names specific vendors (Ollama, Gemini, OpenAI, Claude, Azure OpenAI) only as
examples of the category "AI Provider" it governs — it does not depend on any of them remaining in
use, and applies unchanged to providers not yet invented.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. |

## Related Standards

VIG-000 (Constitution — Principles 3, 4, 11), VIG-002 (Architecture Principles — provider
interface requirement), VIG-007 (Quality Standard — the verification gate AI output must pass).

## References

- `docs/adr/2026-07-27-vision-provider-abstraction.md` — the `VisionProvider` interface this
  document's Principle 1 and Rule 1 generalize from a single module's decision into platform law.
