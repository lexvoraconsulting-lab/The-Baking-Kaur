"""
Vision extraction - taxonomy digest and prompt rendering (Build-008).

WHY THIS EXISTS
  docs/AI/VisionExtractionContract.md section 4 requires the extraction prompt
  to be a TEMPLATE rendered against the live taxonomy, never a hand-copied
  vocabulary list: "Never hand-copied; a hand-copy would silently drift the
  moment a Term is added." This module is that renderer.

WHY THE DIGEST IS A GENERATED ARTIFACT
  ai/vision/schemas/taxonomy_v1.json is regenerated from
  ai/taxonomy/content/bakery_v1.json, the single canonical Bakery vocabulary
  per ADR 0011. It is never edited by hand - the same discipline
  ai/eal/schemas/*.json and ai/ear/schemas/ear.schema.json already follow.

WHY prompt_version IS A CONTENT HASH
  ai.eal.models.Provenance carries prompt_version, and a record whose prompt
  cannot be identified is not reproducible. Hashing the RENDERED prompt (not
  the template) means adding one Term changes prompt_version, which is
  correct: the same photograph extracted before and after a vocabulary grows
  is genuinely two different extractions.
"""
import hashlib
import json
from pathlib import Path

from ai.taxonomy.catalog import TaxonomyCatalog
from ai.taxonomy.loader import load_catalog

_DEFAULT_TAXONOMY = Path(__file__).resolve().parent.parent.parent / "taxonomy" / "content" / "bakery_v1.json"
CANONICAL_TAXONOMY_PATH = str(_DEFAULT_TAXONOMY) if _DEFAULT_TAXONOMY.exists() else "ai/taxonomy/content/bakery_v1.json"

# Groups whose attributes are platform-level bookkeeping rather than things a
# camera can see. Nothing in bakery_v1.json is currently tier="platform", but
# the filter is applied rather than assumed - see build_digest().
_NON_VISUAL_TIERS = {"platform"}


def load_canonical_catalog(path: str | Path | None = None) -> TaxonomyCatalog:
    """The one canonical Bakery vocabulary (ADR 0011: Python owns taxonomy
    content). Read-only - nothing in the extraction path writes to it."""
    target_path = Path(path) if path is not None else Path(CANONICAL_TAXONOMY_PATH)
    if not target_path.exists() and _DEFAULT_TAXONOMY.exists():
        target_path = _DEFAULT_TAXONOMY
    return load_catalog(target_path)


def build_digest(catalog: TaxonomyCatalog) -> dict:
    """The machine-readable view of the taxonomy handed to the model: every
    domain-tier group, its attributes, and each attribute's vocabulary terms
    (labels + synonyms, so the model can name things the way the taxonomy
    already does).

    Groups with no attributes are included deliberately, marked empty. Seven
    of the thirty are empty today (Classification, Material, Business, Topper,
    Size, Flavour, Allergens) - telling the model the group exists but has no
    attribute is what lets it report a topper as unmatched-against-a-known-gap
    rather than as an unrelated observation.
    """
    vocab_by_id = {v.vocabulary_id: v for v in catalog.vocabularies}
    groups = []
    for group in catalog.attribute_groups:
        if group.tier in _NON_VISUAL_TIERS or group.status != "active":
            continue
        attributes = []
        for attr in catalog.attributes_in_group(group.group_id):
            if attr.status != "active":
                continue
            entry = {"name": attr.name, "data_type": attr.data_type}
            if attr.vocabulary_id:
                vocab = vocab_by_id.get(attr.vocabulary_id)
                terms = [
                    {"label": t.label, "synonyms": list(t.synonyms)}
                    for t in catalog.terms_in_vocabulary(attr.vocabulary_id)
                    if t.status == "active"
                ]
                entry["vocabulary"] = vocab.name if vocab else attr.vocabulary_id
                entry["terms"] = terms
            attributes.append(entry)
        groups.append({"group": group.name, "attributes": attributes})

    return {
        "taxonomy_version": _taxonomy_version(catalog),
        "domain": "bakery",
        "source": CANONICAL_TAXONOMY_PATH,
        "categories": [c.name for c in catalog.categories if c.status == "active"],
        "groups": groups,
        "relationship_types": sorted(_relationship_types()),
    }


def _taxonomy_version(catalog: TaxonomyCatalog) -> str:
    """Every entity carries taxonomy_version; they are expected to agree. Take
    the first rather than assume - a disagreement is a real defect and is
    surfaced by returning the set, not silently picking one."""
    versions = {g.taxonomy_version for g in catalog.attribute_groups}
    if len(versions) != 1:
        raise ValueError(f"Taxonomy carries mixed taxonomy_version values: {sorted(versions)}")
    return versions.pop()


def _relationship_types() -> set[str]:
    """ai.taxonomy's 10 types plus Relationship_Model.md's Object-to-Object
    spatial types. Imported rather than restated where possible."""
    from typing import get_args

    from ai.taxonomy.models import RelationshipType

    return set(get_args(RelationshipType)) | {"ON", "NEAR", "MATCHES"}


def render_prompt(template: str, digest: dict) -> str:
    """Substitute the rendered taxonomy digest into the prompt template.

    ponytail: str.replace on one marker, not a template engine - there is
    exactly one substitution and no conditionals. Swap for Jinja only if a
    second marker or any logic ever appears.
    """
    marker = "{{TAXONOMY_DIGEST}}"
    if marker not in template:
        raise ValueError(f"Prompt template is missing the {marker} marker")
    return template.replace(marker, _digest_as_text(digest))


def _digest_as_text(digest: dict) -> str:
    """Human/model-readable rendering. Plain text, not JSON - the JSON form
    already goes to the model as the output schema, and repeating the whole
    vocabulary as JSON burns input tokens for no gain in fidelity."""
    lines = [f"Domain: {digest['domain']}    Taxonomy version: {digest['taxonomy_version']}"]
    lines.append(f"Categories: {', '.join(digest['categories'])}")
    lines.append("")
    for group in digest["groups"]:
        if not group["attributes"]:
            lines.append(f"- {group['group']}: (group exists, no attribute defined yet)")
            continue
        lines.append(f"- {group['group']}:")
        for attr in group["attributes"]:
            if "terms" in attr:
                terms = ", ".join(
                    t["label"] + (f" ({'/'.join(t['synonyms'])})" if t["synonyms"] else "")
                    for t in attr["terms"]
                )
                lines.append(f"    {attr['name']} [{attr['vocabulary']}]: {terms}")
            else:
                lines.append(f"    {attr['name']} [{attr['data_type']}, free value]")
    lines.append("")
    lines.append(f"Relationship types: {', '.join(digest['relationship_types'])}")
    return "\n".join(lines)


def compute_prompt_version(rendered_prompt: str) -> str:
    """Identity of the exact prompt a record was produced under. Content hash
    of the RENDERED text, so a taxonomy change is visible in provenance."""
    return "extractor_v1-" + hashlib.sha256(rendered_prompt.encode("utf-8")).hexdigest()[:12]


def regenerate_digest_file(
    catalog: TaxonomyCatalog, path: str | Path = "ai/vision/schemas/taxonomy_v1.json",
) -> dict:
    """Write the generated digest. Called by the test/self-check the same way
    ai.eal.test_eal regenerates its JSON Schema - the file on disk is an
    artifact of this function, never hand-edited."""
    digest = build_digest(catalog)
    Path(path).write_text(json.dumps(digest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return digest
