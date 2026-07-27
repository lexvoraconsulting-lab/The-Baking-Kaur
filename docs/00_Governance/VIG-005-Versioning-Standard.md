# VIG-005: Versioning Standard

Status: Active
Version: 1.0

## Purpose

Defines how schemas, taxonomies, prompts, and any other versionable platform artifact are versioned,
so that data produced under one version remains interpretable forever, even after the artifact
changes.

## Scope

Applies to every artifact whose meaning affects how observations or Knowledge Graph data are
interpreted: extraction schemas, taxonomies, prompts, and any future artifact class with the same
property (a config format, an embedding model version, an API contract).

This standard does not govern the versioning of governance documents themselves (VIG documents,
ADRs). Those follow VIG-000's amendment process and VIG-009's ADR supersession model respectively —
a different lifecycle from data/content artifacts, since a governance document is incrementally
revised prose, not a machine-consumed contract that must remain byte-for-byte reproducible.

## Definitions

- **Artifact**: a versionable thing — a schema, a taxonomy, a prompt.
- **Version**: an explicit, immutable identifier (e.g. `v1`, `v2`) attached to a specific state of
  an artifact.
- **Published Version**: a version that has been used to produce at least one observation or
  Knowledge Graph entry. Once published, a version is permanently immutable.

## Principles

1. Every artifact carries an explicit version identifier. No artifact is versioned implicitly by
   file modification time or git history alone.
2. Published versions are immutable. A change to an artifact's meaning always produces a new
   version; it never silently edits a version already in use.
3. Every observation and Knowledge Graph entry records which version of which artifact(s) produced
   it, for as long as that data exists.
4. Deprecating a version requires a documented migration path for data produced under it — data is
   never orphaned by a version's retirement.
5. Version identifiers are simple and ordered (`v1`, `v2`, ...) — the goal is unambiguous
   traceability, not semantic-versioning complexity for artifacts that are content, not code.

## Rules

- A change to a schema, taxonomy, or prompt's meaning is a new version, named distinctly from the
  version it supersedes; the old file/version remains readable.
- Every configuration or data structure referencing a versionable artifact must name the specific
  version, not "latest" or "current," so that reprocessing or lineage lookups are deterministic.
- A version may not be deprecated without a stated plan for what happens to data already produced
  under it (reprocess, retain as-is with a documented caveat, or migrate).

## Examples

- `taxonomy_v1.json` exists; a future taxonomy correction is published as `taxonomy_v2.json` rather
  than editing `taxonomy_v1.json` in place. `vision.json`'s `taxonomy_version` field names exactly
  which one a given run used. Correct.
- A Knowledge Graph entry records `schema_version: v1` alongside its data, so a later schema change
  doesn't silently reinterpret old entries incorrectly.

## Non-examples

- `extractor_v1.md`'s content is edited in place after it has already been used to produce
  observations, with no new version created. Violates Principle 2 — data produced under the old
  wording becomes indistinguishable from data produced under the new one.
- A config references a schema as `"latest"` rather than a specific version. Violates Rule 2 —
  the same config produces different, non-reproducible behavior over time.

## Implementation Guidance

Any config or data structure with a field like `schema_file` or `taxonomy_file` should have a
companion explicit version field (`schema_version`, `taxonomy_version`) rather than relying on the
filename alone to convey version — this keeps the version machine-readable and independent of any
future rename.

## Future Compatibility

This standard does not mandate semantic versioning (major.minor.patch) — content artifacts (prompts,
taxonomies, schemas) are not code and don't carry the same compatibility contract implications;
simple sequential versions are sufficient and were chosen deliberately over more complex schemes.

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-07-27 | Initial adoption. |

## Related Standards

VIG-000 (Constitution — Principle 9), VIG-003 (Data Principles — lineage requires version
tracking), VIG-006 (Identifier Standard — the companion permanent-identity standard).

## References

- `ai/vision/config/vision.json` and `docs/AI/Configuration.md` — first concrete application:
  explicit `schema_version`/`taxonomy_version` fields, matching the `_v1` suffix convention already
  used in `ai/vision/schemas/` and `ai/vision/prompts/` filenames.
- `docs/adr/2026-07-27-vision-identity-and-packaging.md` — the decision that introduced these
  fields into the Vision Engine.
