# VIG-002: Architecture Principles

Status: Active
Version: 1.0

## Purpose

States the structural rules every module's internal architecture must satisfy, independent of what
the module does. These generalize lessons already proven in the Vision Engine's implementation
(see References) into requirements that apply before any future module's first commit.

## Scope

Applies to the internal structure of every module: folder layout, dependency direction,
configuration strategy, and how a module exposes itself to be called by other modules.

## Definitions

- **Mechanism**: how a capability is performed (e.g. which AI vendor's API is called).
- **Content**: what a capability is asked to do or produce (e.g. a prompt, a schema, a taxonomy).
- **Interchangeable Provider**: an implementation of a capability that can be swapped for another
  implementation of the same capability without changing any code that calls it.

## Principles

1. Mechanism and content are separated. A module's code must not need to change when its prompt,
   taxonomy, or schema content changes, and vice versa.
2. Every capability with more than one plausible implementation (a vision model, a storage backend,
   a search index) is accessed through an interface, with concrete implementations swappable behind
   it, chosen by configuration — not hardcoded at call sites.
3. Configuration is external to code. Model names, endpoints, file paths, and credentials are never
   literal values inside application logic.
4. A module's internal structure is created in proportion to its actual responsibilities.
   Sub-packages, service layers, and abstraction points are added when a second real
   implementation, caller, or use case exists — not preemptively for a first, and only, one.
5. Every module must be callable by every other module without workarounds. A module's internal
   layout must not assume it is only ever run as a standalone script.
6. Dependency direction within and across modules is acyclic. A lower-level module (e.g. a provider
   abstraction) never depends on a higher-level one (e.g. a business application built on it).

## Rules

- Any function or class implementing "call an external AI/data provider" must sit behind an
  interface with at least the method signature needed for a second implementation to exist without
  changing callers.
- No credential, endpoint, or model identifier may be a literal value in application code.
- A module is not split into sub-packages until it has at least two siblings of the same kind (e.g.
  a second provider implementation) needing the split.
- A module intended to be called by any other module must be structured so that call can happen via
  a normal import, not a `sys.path` modification or copy-pasted logic.

## Examples

- A `VisionProvider` interface with one concrete `OllamaProvider` today, and a factory function
  choosing the implementation from configuration. Adding a second provider requires one new class
  and one new configuration value — no change to any calling code. Correct.
- A module ships as a proper importable package (with `__init__.py` at every level) from its first
  commit, so a future module elsewhere in the repository can import it directly. Correct.

## Non-examples

- A vision-calling function hardcodes a specific vendor's URL and model name inline, with no
  interface separating "call a vision model" from "call this particular vendor's model." Violates
  Principle 2 and 3.
- A module's internal code assumes it is always invoked as `python script.py` from its own
  directory, making it unusable as a library by any other module. Violates Principle 5.
- Five near-identical service classes are created for a capability that, in production, has exactly
  one implementation and no near-term second one. Violates Principle 4.

## Implementation Guidance

Before adding an interface or abstraction, an implementer should be able to name the second
concrete case it exists to accommodate — either one that already exists, or one explicitly required
by an approved roadmap. An abstraction justified only by "we might need this later" does not yet
satisfy Principle 4 and should wait.

## Future Compatibility

This document intentionally does not mandate a specific dependency-injection framework, plugin
system, or package manager — it states the shape (interchangeable mechanism, external
configuration, acyclic dependencies) that any implementation, in any language or framework, must
have. The specific tools used to satisfy it are ADR-level decisions (VIG-009).

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. |

## Related Standards

VIG-000 (Constitution — Principle 11, provider interchangeability), VIG-001 (Platform Principles —
Principle 4, additive growth), VIG-004 (AI Principles), VIG-006 (Identifier Standard).

## References

- `docs/adr/2026-07-27-vision-provider-abstraction.md` — first concrete application of Principles
  1–3 (VisionProvider interface, JSON config, no hardcoded model/URL/paths).
- `docs/adr/2026-07-27-vision-identity-and-packaging.md` — first concrete application of Principle
  5 (making `ai.vision.python` importable) and Principle 6.
- `docs/AI/FolderStructure.md` — the Vision Engine's application of Principle 4 ("no `providers/`
  package until a second provider exists").
