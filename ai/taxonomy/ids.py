"""
Enterprise Master Taxonomy (Build-005) - identifier strategy.

WHY SEQUENTIAL, PREFIXED IDS FOR ALL FOUR ENTITY TYPES
  Same rationale as ai.ear.ids: taxonomy content is a single, centrally
  authored catalog with exactly one allocator (this package), not many
  uncoordinated producers - so sequential, human-readable IDs are safe here,
  the same way EAR-NNNNNN is safe for EAR. See
  docs/40_Enterprise_Attribute_Registry/EAR_SPECIFICATION.md's own note on
  when sequential IDs are appropriate.

WHY STABLE, NOT LABEL-DERIVED
  docs/10_Taxonomy/Hierarchy.md and Controlled_Vocabulary.md both require an
  identifier that survives relabeling/reparenting - a content-hash of the
  (mutable) label or tree position would break that guarantee. Allocation is
  the only scheme that satisfies it.
"""
import re

CATEGORY_ID_PATTERN = re.compile(r"^TAX-CAT-\d{6}$")
GROUP_ID_PATTERN = re.compile(r"^TAX-GRP-\d{6}$")
VOCABULARY_ID_PATTERN = re.compile(r"^TAX-VOC-\d{6}$")
TERM_ID_PATTERN = re.compile(r"^TAX-TERM-\d{6}$")
ATTRIBUTE_ID_PATTERN = re.compile(r"^TAX-ATTR-\d{6}$")
RELATIONSHIP_ID_PATTERN = re.compile(r"^TAX-REL-\d{6}$")

_PATTERNS = {
    "TAX-CAT": CATEGORY_ID_PATTERN,
    "TAX-GRP": GROUP_ID_PATTERN,
    "TAX-VOC": VOCABULARY_ID_PATTERN,
    "TAX-TERM": TERM_ID_PATTERN,
    "TAX-ATTR": ATTRIBUTE_ID_PATTERN,
    "TAX-REL": RELATIONSHIP_ID_PATTERN,
}

# subject_type/object_type -> the ID pattern an entity of that type must match
ENTITY_TYPE_ID_PATTERNS = {
    "category": CATEGORY_ID_PATTERN,
    "attribute_group": GROUP_ID_PATTERN,
    "attribute": ATTRIBUTE_ID_PATTERN,
    "vocabulary": VOCABULARY_ID_PATTERN,
    "term": TERM_ID_PATTERN,
}


def is_valid_category_id(value: str) -> bool:
    return bool(CATEGORY_ID_PATTERN.match(value))


def is_valid_group_id(value: str) -> bool:
    return bool(GROUP_ID_PATTERN.match(value))


def is_valid_vocabulary_id(value: str) -> bool:
    return bool(VOCABULARY_ID_PATTERN.match(value))


def is_valid_term_id(value: str) -> bool:
    return bool(TERM_ID_PATTERN.match(value))


def is_valid_attribute_id(value: str) -> bool:
    return bool(ATTRIBUTE_ID_PATTERN.match(value))


def is_valid_relationship_id(value: str) -> bool:
    return bool(RELATIONSHIP_ID_PATTERN.match(value))


def _allocate(prefix: str, existing_ids: list[str]) -> str:
    pattern = _PATTERNS[prefix]
    max_seq = 0
    for existing in existing_ids:
        if pattern.match(existing):
            max_seq = max(max_seq, int(existing.rsplit("-", 1)[1]))
    return f"{prefix}-{max_seq + 1:06d}"


def allocate_category_id(existing_ids: list[str]) -> str:
    return _allocate("TAX-CAT", existing_ids)


def allocate_group_id(existing_ids: list[str]) -> str:
    return _allocate("TAX-GRP", existing_ids)


def allocate_vocabulary_id(existing_ids: list[str]) -> str:
    return _allocate("TAX-VOC", existing_ids)


def allocate_term_id(existing_ids: list[str]) -> str:
    return _allocate("TAX-TERM", existing_ids)


def allocate_attribute_id(existing_ids: list[str]) -> str:
    return _allocate("TAX-ATTR", existing_ids)


def allocate_relationship_id(existing_ids: list[str]) -> str:
    return _allocate("TAX-REL", existing_ids)
