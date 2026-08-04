"""
Enterprise Product Knowledge Graph (Build-302) - the in-memory graph store.

WHY IN-MEMORY, NOT A DATABASE
  See models.py's module docstring and ADR
  docs/adr/2026-08-02-product-knowledge-graph.md: no storage-technology
  decision has been made for the Knowledge Graph (VIG-003 reserves that for
  a future ADR). KnowledgeGraph is a plain, rebuild-on-demand in-memory
  index over nodes/edges resolved live by ai.knowledge.resolvers - the same
  "assembled fresh, never independently persisted" discipline
  ai.product_intelligence.ProductAggregate already established.

WHY add_edge NEVER REJECTS A DANGLING EDGE
  A resolver may legitimately add an edge before both endpoint nodes exist
  yet (e.g. resolvers run in an order where Category nodes haven't been
  added when a Product->Category edge is emitted). Silently rejecting or
  raising would make resolver ordering a hidden coupling. Instead, dangling
  edges are allowed and then SURFACED by health-checking (observability.py)
  - "broken relationships" is one of the health signals Build-302 explicitly
  asked to track, which only means something if the graph itself stays
  permissive and the health check does the flagging.
"""
from collections import defaultdict

from ai.knowledge.models import KnowledgeEdge, KnowledgeNode, NodeType


class KnowledgeGraph:
    def __init__(self):
        self._nodes: dict[str, KnowledgeNode] = {}
        self._edges: dict[str, KnowledgeEdge] = {}
        self._edges_by_subject: dict[str, list[str]] = defaultdict(list)
        self._edges_by_object: dict[str, list[str]] = defaultdict(list)

    def add_node(self, node: KnowledgeNode) -> None:
        self._nodes[node.node_id] = node

    def add_edge(self, edge: KnowledgeEdge) -> None:
        self._edges[edge.edge_id] = edge
        self._edges_by_subject[edge.subject_id].append(edge.edge_id)
        self._edges_by_object[edge.object_id].append(edge.edge_id)

    def get_node(self, node_id: str) -> KnowledgeNode | None:
        return self._nodes.get(node_id)

    def get_edge(self, edge_id: str) -> KnowledgeEdge | None:
        return self._edges.get(edge_id)

    def nodes_by_type(self, node_type: NodeType) -> list[KnowledgeNode]:
        return [n for n in self._nodes.values() if n.node_type == node_type]

    def edges_from(self, node_id: str) -> list[KnowledgeEdge]:
        return [self._edges[eid] for eid in self._edges_by_subject.get(node_id, [])]

    def edges_to(self, node_id: str) -> list[KnowledgeEdge]:
        return [self._edges[eid] for eid in self._edges_by_object.get(node_id, [])]

    def edges_incident_to(self, node_id: str) -> list[KnowledgeEdge]:
        return self.edges_from(node_id) + self.edges_to(node_id)

    @property
    def nodes(self) -> list[KnowledgeNode]:
        return list(self._nodes.values())

    @property
    def edges(self) -> list[KnowledgeEdge]:
        return list(self._edges.values())

    def __len__(self) -> int:
        return len(self._nodes)
