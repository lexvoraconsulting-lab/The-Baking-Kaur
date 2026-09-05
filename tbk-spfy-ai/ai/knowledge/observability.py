"""
Enterprise Product Knowledge Graph (Build-302) - observability.

WHY A HEALTH REPORT, NOT JUST AN OBSERVER
  Build-302 Phase 8 asks for graph-level signals (missing nodes, duplicate
  nodes, broken relationships, coverage, density) that no single event hook
  can express - those are properties of the whole graph at a point in time,
  not of one resolve() call. compute_health_report is a pure function of a
  KnowledgeGraph (+ any resolver failures the caller collected), callable on
  demand; KnowledgeGraphObserver (mirroring ai.pricing/ai.product_intelligence's
  Observer shape exactly) is for the per-call hooks a metrics/tracing
  consumer would want.
"""
import logging
from abc import ABC
from collections import Counter

from ai.knowledge.graph import KnowledgeGraph
from ai.knowledge.models import GraphHealthReport, GraphIssue

_logger = logging.getLogger("ai.knowledge")


class KnowledgeGraphObserver(ABC):
    def on_resolver_completed(self, resolver_name: str, node_count: int, edge_count: int) -> None:
        pass

    def on_resolver_failed(self, resolver_name: str, error: Exception) -> None:
        pass

    def on_health_report(self, report: GraphHealthReport) -> None:
        pass


class NullObserver(KnowledgeGraphObserver):
    """The default - see ai.pricing.observability.NullObserver's rationale."""


class LoggingObserver(KnowledgeGraphObserver):
    def on_resolver_completed(self, resolver_name: str, node_count: int, edge_count: int) -> None:
        _logger.info("knowledge.resolver_completed resolver=%s nodes=%d edges=%d", resolver_name, node_count, edge_count)

    def on_resolver_failed(self, resolver_name: str, error: Exception) -> None:
        _logger.warning("knowledge.resolver_failed resolver=%s error=%s", resolver_name, error)

    def on_health_report(self, report: GraphHealthReport) -> None:
        level = logging.INFO if report.is_healthy else logging.WARNING
        _logger.log(
            level, "knowledge.health nodes=%d edges=%d density=%.3f issues=%d",
            report.node_count, report.edge_count, report.relationship_density, len(report.issues),
        )


def compute_health_report(
    graph: KnowledgeGraph, generated_at: str, resolver_failures: list[str] | None = None,
) -> GraphHealthReport:
    issues: list[GraphIssue] = []

    node_ids = {n.node_id for n in graph.nodes}
    for edge in graph.edges:
        if edge.subject_id not in node_ids:
            issues.append(GraphIssue(
                code="dangling_edge_subject", severity="error",
                message=f"edge {edge.edge_id} references missing subject node {edge.subject_id!r}",
                edge_id=edge.edge_id,
            ))
        if edge.object_id not in node_ids:
            issues.append(GraphIssue(
                code="dangling_edge_object", severity="error",
                message=f"edge {edge.edge_id} references missing object node {edge.object_id!r}",
                edge_id=edge.edge_id,
            ))

    seen_by_type_and_label: dict[tuple[str, str], list[str]] = {}
    for node in graph.nodes:
        key = (node.node_type, node.label)
        seen_by_type_and_label.setdefault(key, []).append(node.node_id)
    for (node_type, label), node_ids_for_label in seen_by_type_and_label.items():
        if len(node_ids_for_label) > 1:
            issues.append(GraphIssue(
                code="possible_duplicate_node", severity="warning",
                message=f"{len(node_ids_for_label)} distinct {node_type} nodes share label {label!r}: {node_ids_for_label}",
            ))

    for failure in resolver_failures or []:
        issues.append(GraphIssue(code="resolver_failed", severity="error", message=failure))

    node_count_by_type = dict(Counter(n.node_type for n in graph.nodes))
    edge_count_by_predicate = dict(Counter(e.predicate for e in graph.edges))
    node_count = len(graph.nodes)
    edge_count = len(graph.edges)

    return GraphHealthReport(
        generated_at=generated_at,
        node_count=node_count,
        edge_count=edge_count,
        node_count_by_type=node_count_by_type,
        edge_count_by_predicate=edge_count_by_predicate,
        relationship_density=(edge_count / node_count) if node_count else 0.0,
        issues=tuple(issues),
    )
