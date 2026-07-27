# VIG-007: Quality Standard

Status: Active
Version: 1.0

## Purpose

Defines the quality bar an observation or piece of logic must clear before it is trusted: confidence
and provenance for AI-derived data, verification before promotion to the Knowledge Graph, and a
minimum testing bar for non-trivial logic.

## Scope

Applies to every AI-derived observation before it reaches the Knowledge Graph, and to every piece of
non-trivial platform logic (branching, parsing, identifier generation) regardless of which module it
lives in.

## Definitions

- **Confidence Score**: a value expressing how certain an observation is, attached at the time the
  observation is produced.
- **Provenance**: see VIG-000. The record of what produced an observation.
- **Verification Gate**: the checkpoint (automatic, human, or both) an observation must pass before
  it is promoted from "observation" to a trusted Knowledge Graph entry.
- **Fabricated Attribute**: any claim presented as fact that the platform cannot trace to a
  verified source — a rating, certification, or delivery promise with no verifiable origin.

## Principles

1. No AI-derived observation is promoted to the Knowledge Graph without a confidence score.
2. No AI-derived observation is promoted to the Knowledge Graph without provenance sufficient to
   answer "what produced this, and when."
3. Nothing is ever fabricated to fill a gap. If a fact (a rating, a certification, a count) cannot be
   verified, the platform states nothing rather than inventing something plausible. This is
   absolute — it applies to every module, not only customer-facing surfaces.
4. Every unit of non-trivial logic (a branch, a parser, an identifier generator, a scoring function)
   ships with a runnable check that fails if the logic breaks. The check is proportional to the
   logic's complexity — an assert-based self-check is sufficient for simple branching; more complex
   logic warrants more thorough testing.
5. A verification gate may be automatic (a rule-based check), human (manual review), or both,
   depending on the risk of the claim — customer-facing claims warrant a higher bar than internal
   Knowledge Graph attributes used only for search relevance.

## Rules

- No observation record may omit a confidence field once structured-output parsing exists for it.
- No observation record may omit a provenance field (provider, model, prompt version, schema
  version, timestamp).
- No module may present a rating, count, certification, or delivery promise the platform cannot
  independently verify, regardless of how plausible an AI provider's suggestion is.
- Any function containing a conditional branch, a parser, or a non-trivial calculation must have at
  least one runnable check exercising that logic before it is considered complete.

## Examples

- A vision observation about a cake's decoration is recorded with `confidence: 0.82`,
  `provider: ollama`, `model: qwen2.5vl:3b`, `prompt_version: v1`, and a timestamp. Correct.
- A storefront section that previously showed an unverified "★ 4.9 Rated" badge is removed rather
  than replaced with a different unverified number, because no verified source exists yet. Correct
  application of Principle 3 (this is a live precedent already followed in this platform's storefront
  work).

## Non-examples

- An observation is written to the Knowledge Graph with a raw text blob and no confidence or
  provenance fields. Violates Principles 1 and 2.
- A module fabricates a "4.8-star" rating because the real rating isn't available yet and "something
  needs to go there." Violates Principle 3 without exception, regardless of module or urgency.
- A new `get_provider`-style dispatch function ships with no test of any kind covering its
  branches. Violates Principle 4.

## Implementation Guidance

When a new observation type is introduced, its schema (VIG-005) should include confidence and
provenance fields from the start — retrofitting them after data already exists without them is far
more expensive than including them from the first record.

## Future Compatibility

This standard does not fix a specific confidence scale (0–1, 0–100, categorical) or a specific
testing framework — those are ADR-level or module-level choices. The requirement that confidence,
provenance, and a minimum verification bar exist is permanent regardless of the specific scale or
tooling chosen.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. |

## Related Standards

VIG-000 (Constitution — Principles 3, 7, 8), VIG-003 (Data Principles — the verification gate data
must pass before Knowledge Graph promotion), VIG-004 (AI Principles — AI output as evidence, not
fact).

## References

- `CLAUDE.md` "Golden rules" — the existing, already-enforced repo rule against inventing GTINs,
  MPNs, barcodes, reviews/ratings, or unfulfillable delivery promises; Principle 3 of this document
  generalizes that rule from the storefront to the entire platform.
- `ai/vision/python/test_config_providers.py` — the existing self-check convention Principle 4
  generalizes into a platform-wide minimum testing bar.
