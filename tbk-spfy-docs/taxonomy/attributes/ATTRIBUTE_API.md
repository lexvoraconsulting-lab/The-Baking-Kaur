# Attribute Intelligence Engine — Future API (Build-303)

No HTTP/GraphQL API is built this sprint — same reasoning as
[GRAPH_API.md](GRAPH_API.md) (Build-302): `ai/api/` is a confirmed-empty scaffold, and no concrete
consumer exists yet to design a real contract against.

## The seam that already exists

`export_profile(profile) -> dict` (exporter.py) already produces the plain, JSON-safe shape a
future API endpoint would return — `ai.product_intelligence.extensions.ProductIntelligenceAPIPort`
remains the port a real API layer implements against, reused rather than redefined
(`ai.knowledge` already made this same call in Build-302).

```python
from ai.attribute_intelligence.exporter import export_profile

payload = export_profile(profile)
# {"subject_id": ..., "resolved_at": ..., "attributes": {"EAR-000001": {"value": ..., ...}}, ...}
```

## What a real implementation would need to decide (not decided here)

- Whether attribute resolution happens synchronously per-request or is pre-computed and cached —
  `AttributeIntelligenceService.resolve()` is currently a pure, in-memory call with no caching
  layer; a real API would need to decide the freshness/latency trade-off.
- Whether `ConflictRecord`s and `ValidationIssue`s are exposed to API consumers directly, or
  summarized (Build-303's `export_profile()` already summarizes: `has_conflict: bool`, not the full
  competing-observations list — a real API might need the full detail for a moderation UI).

## Why not built now

Same reasoning as `GRAPH_API.md`: building an API against zero real consumers would be speculative.
The export function stays ready; a transport layer waits for a concrete need.
