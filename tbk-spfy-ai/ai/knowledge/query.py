"""
Enterprise Product Knowledge Graph (Build-302) - the query engine.

WHY THESE QUERIES AND NOT MORE
  Every method here is real graph traversal over whatever KnowledgeGraph
  already holds - no ranking model, no ML, no fabricated scoring. similar_to
  is a plain Jaccard-style overlap count over shared outgoing edges (shared
  categories/collections/occasions/etc.), which is honest about what it is:
  a coverage heuristic, not a recommendation engine (that stays
  RecommendationResolverPort's job, unbuilt this sprint - see extensions.py).
  This satisfies Build-302 Phase 5's query list without pretending any of
  it is ML-backed, which Phase 6 explicitly forbids anyway.
"""
from dataclasses import dataclass

from ai.knowledge.graph import KnowledgeGraph
from ai.knowledge.models import EdgeType, KnowledgeEdge, KnowledgeNode, NodeType


@dataclass(frozen=True)
class SimilarityResult:
    node: KnowledgeNode
    shared_edge_count: int
    shared_predicates: tuple[EdgeType, ...]


class GraphQueryEngine:
    def __init__(self, graph: KnowledgeGraph):
        self._graph = graph

    def find_by_type(self, node_type: NodeType) -> list[KnowledgeNode]:
        return self._graph.nodes_by_type(node_type)

    def find_related(self, node_id: str, predicate: EdgeType | None = None) -> list[KnowledgeNode]:
        """Every node reachable by one hop, in either direction. Filters to
        a single predicate (e.g. "Find Products by Theme" is
        find_related(theme_node_id, predicate='HAS_THEME')) when given."""
        related_ids: list[str] = []
        for edge in self._graph.edges_incident_to(node_id):
            if predicate is not None and edge.predicate != predicate:
                continue
            other_id = edge.object_id if edge.subject_id == node_id else edge.subject_id
            related_ids.append(other_id)
        return [n for n in (self._graph.get_node(nid) for nid in related_ids) if n is not None]

    def find_by_relationship(
        self, subject_type: NodeType | None, predicate: EdgeType, object_type: NodeType | None = None,
    ) -> list[KnowledgeEdge]:
        results = []
        for edge in self._graph.edges:
            if edge.predicate != predicate:
                continue
            subject = self._graph.get_node(edge.subject_id)
            obj = self._graph.get_node(edge.object_id)
            if subject_type is not None and (subject is None or subject.node_type != subject_type):
                continue
            if object_type is not None and (obj is None or obj.node_type != object_type):
                continue
            results.append(edge)
        return results

    def find_similar(self, node_id: str, node_type: NodeType, limit: int = 10) -> list[SimilarityResult]:
        """Same node_type peers ranked by count of shared one-hop
        neighbours - a real, cheap, non-ML "similar cakes" proxy."""
        this_neighbours = {e.object_id for e in self._graph.edges_from(node_id)}
        results = []
        for candidate in self._graph.nodes_by_type(node_type):
            if candidate.node_id == node_id:
                continue
            candidate_neighbours = {e.object_id for e in self._graph.edges_from(candidate.node_id)}
            shared = this_neighbours & candidate_neighbours
            if not shared:
                continue
            shared_predicates = tuple(sorted({
                e.predicate for e in self._graph.edges_from(candidate.node_id) if e.object_id in shared
            }))
            results.append(SimilarityResult(candidate, len(shared), shared_predicates))
        results.sort(key=lambda r: r.shared_edge_count, reverse=True)
        return results[:limit]

    def traverse(self, start_node_id: str, max_depth: int = 3) -> list[KnowledgeEdge]:
        """Breadth-first edge traversal outward from start_node_id, up to
        max_depth hops - the mechanism Build-302 Phase 6's inference-chain
        example (Birthday Cake -> Kids -> Spider Theme -> ...) runs on. See
        inference.py for the rule-based chain built on top of this."""
        visited_nodes = {start_node_id}
        frontier = [start_node_id]
        collected: list[KnowledgeEdge] = []
        for _ in range(max_depth):
            next_frontier = []
            for node_id in frontier:
                for edge in self._graph.edges_from(node_id):
                    collected.append(edge)
                    if edge.object_id not in visited_nodes:
                        visited_nodes.add(edge.object_id)
                        next_frontier.append(edge.object_id)
            frontier = next_frontier
            if not frontier:
                break
        return collected
