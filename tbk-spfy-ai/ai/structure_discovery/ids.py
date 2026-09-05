"""
Dynamic Visual Structure Discovery - identifiers.

WHY uuid5 WITH ITS OWN NAMESPACE, NOT A CONTENT HASH LIKE ai.eal
  VIG-006 permits both philosophies and this repository uses each
  deliberately: content-hash where multiple producers must agree without
  coordination (ai.eal, TBK_IMAGE_ID), sequential where one allocator owns
  the space (ai.ear, ai.taxonomy). A proposal is neither - it is produced by
  one engine but must be stable across runs so the same unmatched observation
  seen in two images deduplicates to one proposal. Deterministic uuid5 over
  (kind, canonical_name) gives exactly that, and the distinct namespace UUID
  keeps it from ever colliding with ai.product_intelligence's or
  ai.attribute_intelligence's uuid5 spaces.
"""
import re
import uuid

# Distinct from every other module's namespace UUID - see module docstring.
_NAMESPACE = uuid.UUID("6f3d9c21-7b4e-5a8f-9c2d-1e4b7a0f5d83")


def slugify(text: str) -> str:
    """The dedupe key. Lowercase, non-alphanumerics to underscore, collapsed.

    ponytail: regex, not a slug library. Two lines, ASCII-only inputs, and a
    dependency here would be the first in this package.
    """
    slug = re.sub(r"[^a-z0-9]+", "_", (text or "").strip().lower())
    return slug.strip("_") or "unnamed"


def compute_proposal_id(kind: str, canonical_name: str) -> str:
    return "PROP-" + str(uuid.uuid5(_NAMESPACE, f"{kind}|{canonical_name}"))[:18]


def compute_observation_id(image_id: str, extracted_at: str) -> str:
    """Identity of one AI Observation (Entity_Model.md) - one provider call.
    Keyed on the image and the call timestamp, so re-running the same image
    later is a genuinely distinct observation while the image_id stays fixed."""
    return "OBS-" + str(uuid.uuid5(_NAMESPACE, f"{image_id}|{extracted_at}"))[:18]
