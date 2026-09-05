"""
Enterprise Product Knowledge Graph (Build-302) - plain dataclass models.

WHY THIS PACKAGE LIVES AT ai/knowledge/, NOT A NEW DIRECTORY
  ai/knowledge/ has existed, empty, since this repo's early scaffolding -
  ECP-100 recorded it as "Build-007 Knowledge Graph, not started, no
  storage-tech ADR yet". This IS that build (renumbered/scoped as Build-302
  by the current sprint), not a second, competing package.

WHY THIS IS NOT A DATABASE
  docs/00_Governance/VIG-003-Data-Principles.md already defines "Knowledge
  Graph" as a persistent system of record with per-attribute lineage back to
  observations - a real storage-technology decision this sprint deliberately
  does NOT make (VIG-003's own "Future Compatibility" section reserves that
  for a future ADR; ECP-100 confirmed none exists). What this package builds
  instead is the semantic RELATIONSHIP layer: typed nodes and edges,
  resolved live from existing systems, held in memory, queryable - Phase 1
  of VIG-003's Knowledge Graph vision, not the whole thing. See
  docs/adr/2026-08-02-product-knowledge-graph.md for the full scoping
  decision and the honest gap this leaves (no persistence, no lineage yet).

WHY NodeType/EdgeType ARE A SUPERSET OF EXISTING VOCABULARIES, NOT A REPLACEMENT
  docs/10_Taxonomy/Entity_Model.md and Relationship_Model.md already defined
  half of this schema (the image side: Image/Region/Object/Attribute/Genome
  Attribute/.../Business Entity, with typed, confidence+provenance-carrying
  edges) in Sprint 2.1 - never implemented in code until now. This module
  implements that existing logical schema rather than inventing a new one,
  and extends it with the commerce-side entities Entity_Model.md explicitly
  declined to model ("The taxonomy does not model Business Entities'
  internal structure"). EdgeType additionally reuses every string value
  ai.taxonomy.models.RelationshipType already defines (BELONGS_TO,
  RELATED_TO, IS_A, PART_OF, ...) verbatim - see test_knowledge_graph.py's
  test_edge_type_is_superset_of_taxonomy_relationship_type for the guard
  against drift. ai.taxonomy's own Relationship model is frozen (Build-005)
  and untouched.
"""
from dataclasses import dataclass, field
from typing import Any, Literal

from ai.knowledge.ids import compute_edge_id, compute_node_id

KNOWLEDGE_GRAPH_VERSION = "1.0"

NodeType = Literal[
    # Image side - already defined by docs/10_Taxonomy/Entity_Model.md (Sprint 2.1),
    # implemented in code here for the first time.
    "IMAGE", "REGION", "OBJECT", "DECORATION", "WRITING", "ATTRIBUTE",
    "GENOME_ATTRIBUTE", "AI_OBSERVATION", "HUMAN_REVIEW",
    "CATEGORY", "ATTRIBUTE_GROUP", "VOCABULARY", "VOCABULARY_TERM", "BUSINESS_ENTITY",
    # Commerce side - Business Entity's internal structure, Build-302's own scope.
    "PRODUCT", "VARIANT", "COLLECTION", "OCCASION", "THEME", "RECIPIENT",
    "FLAVOR", "INGREDIENT", "RECIPE", "PACKAGING", "DELIVERY", "PRICING",
    "INVENTORY", "MERCHANT", "SEO", "SCHEMA", "VIDEO", "REVIEW",
    "CUSTOMER_INTENT", "RECOMMENDATION", "AI_GENOME", "EMBEDDING",
    "AUTOMATION", "ANALYTICS",
]

# Every ai.taxonomy.models.RelationshipType value, verbatim (not redefined) -
# plus Relationship_Model.md's Object-to-Object types (ON, NEAR, MATCHES) and
# the Build-302-requested commerce predicates. See module docstring.
EdgeType = Literal[
    "IS_A", "PART_OF", "BELONGS_TO", "USES", "RELATED_TO",
    "PAIRS_WITH", "CONTRASTS_WITH", "COMPLEMENTS", "AVAILABLE_IN", "SUITABLE_FOR",
    "ON", "NEAR", "MATCHES",
    "HAS_CATEGORY", "HAS_COLLECTION", "HAS_OCCASION", "HAS_THEME", "HAS_STYLE",
    "HAS_COLOR", "HAS_FLAVOR", "HAS_INGREDIENT", "HAS_RECIPE", "HAS_PRICE",
    "HAS_VARIANT", "HAS_SCHEMA", "HAS_IMAGE", "HAS_VIDEO", "HAS_EMBEDDING",
    "HAS_GENOME", "SIMILAR_TO", "RECOMMENDED_WITH", "DELIVERED_BY",
    "OPTIMIZED_FOR", "INDEXED_BY", "GENERATED_BY", "VALIDATED_BY",
]

LifecycleStatus = Literal["active", "deprecated", "retired"]


@dataclass(frozen=True)
class KnowledgeNode:
    """node_id is a namespaced wrapper of the entity's own real identifier
    (a Shopify GID, a TAX-CAT-NNNNNN, an EAR-NNNNNN, ...) - never a new,
    competing identity (VIG-003 Principle 2, VIG-006 Principle 5: identifiers
    are opaque, and this package invents none where a canonical one already
    exists elsewhere)."""
    node_type: NodeType
    native_id: str
    label: str
    source_system: str
    node_id: str = ""
    confidence: float | None = None
    version: str = KNOWLEDGE_GRAPH_VERSION
    status: LifecycleStatus = "active"
    attributes: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.native_id:
            raise ValueError("native_id is required")
        if not self.node_id:
            object.__setattr__(self, "node_id", compute_node_id(self.node_type, self.native_id))


@dataclass(frozen=True)
class KnowledgeEdge:
    """A typed, directional edge - Relationship_Model.md's own requirement
    ("typed edges, not a generic graph") applied across the full node
    vocabulary, not just Image-side entities. confidence/source are
    optional: a deterministic join (e.g. Product -> its own resolved
    Category) has no meaningful confidence score and is not evidence to
    verify; an AI-derived edge (a future similarity/recommendation edge)
    would carry one, per VIG-007 Principles 1-2."""
    subject_id: str
    predicate: EdgeType
    object_id: str
    source_system: str
    edge_id: str = ""
    confidence: float | None = None
    version: str = KNOWLEDGE_GRAPH_VERSION
    status: LifecycleStatus = "active"

    def __post_init__(self):
        if not self.edge_id:
            object.__setattr__(
                self, "edge_id",
                compute_edge_id(self.subject_id, self.predicate, self.object_id),
            )


@dataclass(frozen=True)
class GraphIssue:
    code: str
    severity: Literal["error", "warning"]
    message: str
    node_id: str | None = None
    edge_id: str | None = None


@dataclass(frozen=True)
class GraphHealthReport:
    generated_at: str
    node_count: int
    edge_count: int
    node_count_by_type: dict[str, int]
    edge_count_by_predicate: dict[str, int]
    relationship_density: float
    issues: tuple[GraphIssue, ...] = ()

    @property
    def is_healthy(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)
