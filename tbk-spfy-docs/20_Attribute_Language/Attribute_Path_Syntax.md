# EAL — Attribute Path Syntax

## Grammar

```
eal.<namespace>.<group>.<attribute>

namespace  ::= "core" | "domain." NAME
group      ::= NAME
attribute  ::= NAME
NAME       ::= [a-z][a-z0-9_]*
```

Enforced exactly by `CANONICAL_PATH_PATTERN` in
[`ai/eal/models_pydantic.py`](../../ai/eal/models_pydantic.py):

```python
CANONICAL_PATH_PATTERN = re.compile(
    r"^eal\.(core|domain\.[a-z][a-z0-9_]*)\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$"
)
```

## Examples

| Path | Valid? | Why |
|---|---|---|
| `eal.core.confidence.score` | Yes | Platform-level namespace, real group, real attribute. |
| `eal.domain.bakery.colour.primary` | Yes | Domain namespace, real group, real attribute. |
| `eal.core.confidence` | No | Missing attribute segment. |
| `EAL.core.confidence.score` | No | Uppercase prefix — see [Naming_Convention.md](Naming_Convention.md). |
| `eal.bakery.colour.primary` | No | Domain namespace must be `domain.<name>`, not the bare name. |

Every case above is a runnable assertion in
[`test_canonical_path_grammar`](../../ai/eal/test_eal.py).

## Why exactly 4 segments, no more, no less

Fewer would collapse namespace/group distinctions Sprint 2.1 already needs
([Attribute_Group_Architecture.md](../10_Taxonomy/Attribute_Group_Architecture.md)). More would let
paths encode meaning beyond what `namespace`/`group`/`attribute` already carry as structured
fields — violating [Identifier_Strategy.md](Identifier_Strategy.md)'s "paths are readable, not a
second encoding of the record's other fields" principle.

## Related Standards

[Namespace_Model.md](Namespace_Model.md), [Naming_Convention.md](Naming_Convention.md).
