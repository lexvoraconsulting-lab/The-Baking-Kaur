"""
Enterprise Product Knowledge Graph (Build-302) - inference-ready architecture.

WHY THIS IS RULE-BASED TRAVERSAL, NOT ML
  Build-302 Phase 6 is explicit: "Do NOT implement ML. Implement
  inference-ready architecture only." An InferenceChain is a declared,
  ordered sequence of predicates (e.g. HAS_OCCASION -> HAS_THEME ->
  HAS_COLOR -> DELIVERED_BY) that GraphQueryEngine.find_related walks one
  hop at a time - exactly the shape of Phase 6's own worked example
  (Birthday Cake -> Kids -> Spider Theme -> Blue Theme -> ... -> Same Day
  Delivery -> Meerut). Every step is real graph traversal over whatever
  edges the resolvers actually produced; a future ML-ranked recommendation
  step plugs in at RECOMMENDED_WITH via RecommendationResolverPort
  (extensions.py) without changing this runner's shape.

WHY A BROKEN CHAIN RETURNS A PARTIAL PATH, NOT AN ERROR
  Matches this engine's system-wide Pending-not-failing discipline (see
  ai.pricing, ai.product_intelligence). A chain step with no matching edge
  today (e.g. no DELIVERED_BY edges exist because no live delivery-zone
  resolver is wired) is an honest, partial result - InferenceResult.reached
  tells the caller exactly how far the chain got.
"""
from dataclasses import dataclass

from ai.knowledge.graph import KnowledgeGraph
from ai.knowledge.models import EdgeType, KnowledgeNode


@dataclass(frozen=True)
class InferenceChain:
    """A named, declared sequence of predicates to walk in order - the
    controlled-vocabulary equivalent for inference paths that
    Relationship_Model.md already requires for relationship types
    themselves. New chains are added additively, never invented ad hoc."""
    name: str
    steps: tuple[EdgeType, ...]


@dataclass(frozen=True)
class InferenceResult:
    chain_name: str
    path: tuple[KnowledgeNode, ...]

    @property
    def reached_full_chain(self) -> bool:
        return len(self.path) >= 1


class InferenceChainRunner:
    def __init__(self, graph: KnowledgeGraph):
        self._graph = graph

    def run(self, chain: InferenceChain, start_node_id: str) -> InferenceResult:
        path: list[KnowledgeNode] = []
        current_id = start_node_id
        for predicate in chain.steps:
            edges = [e for e in self._graph.edges_from(current_id) if e.predicate == predicate]
            if not edges:
                break
            next_node = self._graph.get_node(edges[0].object_id)
            if next_node is None:
                break
            path.append(next_node)
            current_id = next_node.node_id
        return InferenceResult(chain_name=chain.name, path=tuple(path))
