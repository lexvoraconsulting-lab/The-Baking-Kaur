# EAL — Naming Convention

## Rule

Every canonical path segment, namespace, group name, and attribute name is **lowercase
`snake_case`**, ASCII only, starting with a letter. No hyphens, no camelCase, no spaces.
Identifiers (`EAL-...`, `TBK-...`) are the one exception — they're opaque tokens, not names, and
their casing is fixed by their generation function (see
[Identifier_Strategy.md](Identifier_Strategy.md)).

## Reserved words

`core` is reserved as the platform-level namespace (see
[Namespace_Model.md](Namespace_Model.md)) — no domain may name itself `core`. `eal` is reserved as
the path prefix and may not appear as a namespace, group, or attribute name.

## Enforced by

`ai/eal/models_pydantic.py`'s `CANONICAL_PATH_PATTERN` regex rejects any path violating this
convention at validation time — see [Attribute_Path_Syntax.md](Attribute_Path_Syntax.md) for the
full grammar and [`ai/eal/test_eal.py::test_canonical_path_grammar`](../../ai/eal/test_eal.py) for
the runnable check (including a case-violation rejection test).

## Related Standards

[Attribute_Path_Syntax.md](Attribute_Path_Syntax.md), [Namespace_Model.md](Namespace_Model.md).
