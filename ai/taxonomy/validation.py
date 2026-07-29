"""
Enterprise Master Taxonomy (Build-005) - whole-catalog validation.

WHY
  Per-entry shape (ID format, status/superseded_by consistency, scope/domain
  consistency) is already enforced by each entity's own Pydantic validators
  at construction time - a single bad entry never reaches here. This module
  only checks invariants that require seeing the whole catalog at once:
  duplicate IDs, and every cross-entity reference (Category.parent_id,
  Category.attribute_group_ids, Term.vocabulary_id, Term.parent_term_id)
  resolving to a real entry.

WHAT IS NOT VALIDATED HERE (deliberately deferred)
  Whether a Category's attribute_group_ids satisfy Inheritance.md's
  additive-only rule against its ancestors, and whether an
  AttributeGroup.ear_namespace resolves against a live EAR registry, are
  content-authoring-time (BL-1+) concerns, not this skeleton's job - BL-0
  ships no real content to check either invariant against yet.
"""
from ai.taxonomy.models_pydantic import (
    AttributeGroupModel,
    CategoryModel,
    RelationshipModel,
    TaxonomyAttributeModel,
    TermModel,
    VocabularyModel,
)

# Hierarchical/transitive relationship types - the only ones a cycle is meaningful for.
# Associative types (PAIRS_WITH, RELATED_TO, ...) legitimately allow A<->B both directions.
_HIERARCHICAL_RELATIONSHIP_TYPES = {"IS_A", "PART_OF", "BELONGS_TO"}


def _check_no_duplicate_ids(entries: list, id_field: str, label: str) -> None:
    seen: set[str] = set()
    for entry in entries:
        entry_id = getattr(entry, id_field)
        if entry_id in seen:
            raise ValueError(f"duplicate {label} {entry_id!r}")
        seen.add(entry_id)


def _check_relationships(
    relationships: list[RelationshipModel],
    entity_ids_by_type: dict[str, set[str]],
) -> None:
    _check_no_duplicate_ids(relationships, "relationship_id", "relationship_id")

    seen_triples: set[tuple] = set()
    hierarchical_edges: list[tuple[str, str]] = []  # (subject_key, object_key)

    for rel in relationships:
        if rel.subject_id not in entity_ids_by_type.get(rel.subject_type, set()):
            raise ValueError(
                f"relationship {rel.relationship_id!r} has subject_id {rel.subject_id!r} "
                f"which does not resolve to any {rel.subject_type!r} in this catalog"
            )
        if rel.object_id not in entity_ids_by_type.get(rel.object_type, set()):
            raise ValueError(
                f"relationship {rel.relationship_id!r} has object_id {rel.object_id!r} "
                f"which does not resolve to any {rel.object_type!r} in this catalog"
            )

        triple = (rel.subject_type, rel.subject_id, rel.relationship_type, rel.object_type, rel.object_id)
        if triple in seen_triples:
            raise ValueError(f"duplicate relationship triple {triple!r} (relationship_id {rel.relationship_id!r})")
        seen_triples.add(triple)

        if rel.relationship_type in _HIERARCHICAL_RELATIONSHIP_TYPES:
            subject_key = f"{rel.subject_type}:{rel.subject_id}"
            object_key = f"{rel.object_type}:{rel.object_id}"
            hierarchical_edges.append((subject_key, object_key))

    _check_no_cycles(hierarchical_edges)


def _check_no_cycles(edges: list[tuple[str, str]]) -> None:
    graph: dict[str, list[str]] = {}
    for src, dst in edges:
        graph.setdefault(src, []).append(dst)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def visit(node: str, path: list[str]) -> None:
        color[node] = GRAY
        for neighbour in graph.get(node, []):
            if color.get(neighbour, WHITE) == GRAY:
                raise ValueError(f"circular relationship detected: {' -> '.join(path + [neighbour])}")
            if color.get(neighbour, WHITE) == WHITE:
                visit(neighbour, path + [neighbour])
        color[node] = BLACK

    for node in list(graph):
        if color[node] == WHITE:
            visit(node, [node])


def validate_catalog(
    categories: list[CategoryModel],
    attribute_groups: list[AttributeGroupModel],
    vocabularies: list[VocabularyModel],
    terms: list[TermModel],
    attributes: list[TaxonomyAttributeModel] | None = None,
    relationships: list[RelationshipModel] | None = None,
) -> None:
    attributes = attributes or []
    relationships = relationships or []

    _check_no_duplicate_ids(categories, "category_id", "category_id")
    _check_no_duplicate_ids(attribute_groups, "group_id", "group_id")
    _check_no_duplicate_ids(vocabularies, "vocabulary_id", "vocabulary_id")
    _check_no_duplicate_ids(terms, "term_id", "term_id")
    _check_no_duplicate_ids(attributes, "attribute_id", "attribute_id")

    category_ids = {c.category_id for c in categories}
    group_ids = {g.group_id for g in attribute_groups}
    vocabulary_ids = {v.vocabulary_id for v in vocabularies}
    term_ids = {t.term_id for t in terms}

    for attribute in attributes:
        if attribute.group_id not in group_ids:
            raise ValueError(
                f"attribute {attribute.attribute_id!r} has group_id {attribute.group_id!r} "
                f"which does not resolve to any group in this catalog"
            )
        if attribute.vocabulary_id is not None and attribute.vocabulary_id not in vocabulary_ids:
            raise ValueError(
                f"attribute {attribute.attribute_id!r} has vocabulary_id "
                f"{attribute.vocabulary_id!r} which does not resolve to any vocabulary in this catalog"
            )

    for category in categories:
        if category.parent_id is not None and category.parent_id not in category_ids:
            raise ValueError(
                f"category {category.category_id!r} has parent_id {category.parent_id!r} "
                f"which does not resolve to any category in this catalog"
            )
        for gid in category.attribute_group_ids:
            if gid not in group_ids:
                raise ValueError(
                    f"category {category.category_id!r} references attribute_group_id "
                    f"{gid!r} which does not resolve to any group in this catalog"
                )

    for term in terms:
        if term.vocabulary_id not in vocabulary_ids:
            raise ValueError(
                f"term {term.term_id!r} has vocabulary_id {term.vocabulary_id!r} which "
                f"does not resolve to any vocabulary in this catalog"
            )
        if term.parent_term_id is not None and term.parent_term_id not in term_ids:
            raise ValueError(
                f"term {term.term_id!r} has parent_term_id {term.parent_term_id!r} "
                f"which does not resolve to any term in this catalog"
            )
        if term.superseded_by is not None and term.superseded_by not in term_ids:
            raise ValueError(
                f"term {term.term_id!r} has superseded_by {term.superseded_by!r} "
                f"which does not resolve to any term in this catalog"
            )

    entity_ids_by_type = {
        "category": category_ids,
        "attribute_group": group_ids,
        "attribute": {a.attribute_id for a in attributes},
        "vocabulary": vocabulary_ids,
        "term": term_ids,
    }
    _check_relationships(relationships, entity_ids_by_type)
