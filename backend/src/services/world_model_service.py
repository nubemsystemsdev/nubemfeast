"""Service for building and managing the world model graph."""

import json
from uuid import UUID

import networkx as nx

from src.models.analysis import Barrier
from src.models.image import Image
from src.schemas.enums import (
    BarrierSeverity,
    Difficulty,
    DistanceEstimate,
    SpaceType,
)
from src.schemas.navigation import (
    BarrierSummary,
    NodeFeatures,
    WorldModelEdge,
    WorldModelNode,
    WorldModelResponse,
)


class WorldModelService:
    """Service for building and managing the world model graph."""

    def __init__(self) -> None:
        self.graph: nx.DiGraph = nx.DiGraph()

    def build_world_model(
        self,
        images: list[Image],
        analysis_results: dict[UUID, dict],
    ) -> nx.DiGraph:
        """Build a world model graph from analyzed images."""
        self.graph = nx.DiGraph()

        # Create nodes for each image
        for image in images:
            analysis = analysis_results.get(image.id, {})
            node_id = f"node_{image.sequence_order}"

            self.graph.add_node(
                node_id,
                image_id=str(image.id),
                label=f"Location {image.sequence_order + 1}",
                space_type=analysis.get("space_type", "other"),
                features=analysis.get("features", {}),
                barriers=[self._barrier_to_dict(b) for b in image.barriers],
                accessibility_score=analysis.get("accessibility_score", 50),
            )

        # Create edges between consecutive nodes
        node_ids = [f"node_{img.sequence_order}" for img in images]
        for i in range(len(node_ids) - 1):
            source = node_ids[i]
            target = node_ids[i + 1]

            # Calculate traversability based on barriers
            source_data = self.graph.nodes[source]
            target_data = self.graph.nodes[target]

            difficulty = self._calculate_difficulty(
                source_data.get("barriers", []),
                target_data.get("barriers", []),
            )

            barrier_ids = [
                b["id"]
                for b in source_data.get("barriers", []) + target_data.get("barriers", [])
                if "id" in b
            ]

            self.graph.add_edge(
                source,
                target,
                traversable=difficulty != Difficulty.IMPASSABLE,
                difficulty=difficulty.value,
                barriers_in_path=barrier_ids,
                distance_estimate=DistanceEstimate.SHORT.value,
                notes=None,
            )

            # Add reverse edge for bidirectional navigation
            self.graph.add_edge(
                target,
                source,
                traversable=difficulty != Difficulty.IMPASSABLE,
                difficulty=difficulty.value,
                barriers_in_path=barrier_ids,
                distance_estimate=DistanceEstimate.SHORT.value,
                notes=None,
            )

        return self.graph

    def _calculate_difficulty(
        self, source_barriers: list[dict], target_barriers: list[dict]
    ) -> Difficulty:
        """Calculate traversal difficulty based on barriers."""
        all_barriers = source_barriers + target_barriers

        if not all_barriers:
            return Difficulty.EASY

        max_severity = BarrierSeverity.LOW
        for barrier in all_barriers:
            severity_str = barrier.get("severity", "low")
            try:
                severity = BarrierSeverity(severity_str)
                if self._severity_rank(severity) > self._severity_rank(max_severity):
                    max_severity = severity
            except ValueError:
                pass

        severity_to_difficulty = {
            BarrierSeverity.LOW: Difficulty.EASY,
            BarrierSeverity.MEDIUM: Difficulty.MODERATE,
            BarrierSeverity.HIGH: Difficulty.DIFFICULT,
            BarrierSeverity.CRITICAL: Difficulty.IMPASSABLE,
        }

        return severity_to_difficulty.get(max_severity, Difficulty.MODERATE)

    def _severity_rank(self, severity: BarrierSeverity) -> int:
        """Get numeric rank for severity comparison."""
        ranks = {
            BarrierSeverity.LOW: 1,
            BarrierSeverity.MEDIUM: 2,
            BarrierSeverity.HIGH: 3,
            BarrierSeverity.CRITICAL: 4,
        }
        return ranks.get(severity, 0)

    def _barrier_to_dict(self, barrier: Barrier) -> dict:
        """Convert Barrier model to dictionary."""
        return {
            "id": str(barrier.id),
            "barrier_type": barrier.barrier_type.value,
            "severity": barrier.severity.value,
            "description": barrier.description,
            "recommendation": barrier.recommendation,
        }

    def find_recommended_path(
        self, start_node: str | None = None, end_node: str | None = None
    ) -> list[str] | None:
        """Find the recommended path through the space."""
        if not self.graph.nodes:
            return None

        nodes = list(self.graph.nodes)
        start = start_node or nodes[0]
        end = end_node or nodes[-1]

        try:
            # Use accessibility score as weight (inverted - lower score = higher weight)
            def weight_func(u: str, v: str, d: dict) -> float:
                if not d.get("traversable", True):
                    return float("inf")

                difficulty_weights = {
                    "easy": 1,
                    "moderate": 2,
                    "difficult": 4,
                    "impassable": float("inf"),
                }
                return difficulty_weights.get(d.get("difficulty", "moderate"), 2)

            path = nx.dijkstra_path(self.graph, start, end, weight=weight_func)
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            # Return sequential path if no weighted path found
            return nodes

    def to_json(self) -> str:
        """Serialize graph to JSON."""
        data = nx.node_link_data(self.graph)
        return json.dumps(data)

    def from_json(self, json_str: str) -> nx.DiGraph:
        """Deserialize graph from JSON."""
        data = json.loads(json_str)
        self.graph = nx.node_link_graph(data)
        return self.graph

    def to_response(self, scan_id: UUID, base_url: str = "") -> WorldModelResponse:
        """Convert graph to API response schema."""
        nodes = []
        for node_id, data in self.graph.nodes(data=True):
            barriers = [
                BarrierSummary(
                    id=UUID(b["id"]) if "id" in b else UUID(int=0),
                    barrier_type=b.get("barrier_type", "other"),
                    severity=b.get("severity", "medium"),
                    description=b.get("description", ""),
                    recommendation=b.get("recommendation"),
                )
                for b in data.get("barriers", [])
            ]

            features_data = data.get("features", {})
            features = NodeFeatures(
                has_ramp=features_data.get("has_ramp", False),
                has_handrails=features_data.get("has_handrails", False),
                has_elevator=features_data.get("has_elevator", False),
                lighting=features_data.get("lighting", "adequate"),
                floor_type=features_data.get("floor_type", "unknown"),
            )

            space_type_str = data.get("space_type", "other")
            try:
                space_type = SpaceType(space_type_str)
            except ValueError:
                space_type = SpaceType.OTHER

            node = WorldModelNode(
                id=node_id,
                image_id=UUID(data["image_id"]),
                image_url=f"{base_url}/api/scans/{scan_id}/images/{data['image_id']}/file",
                label=data.get("label", node_id),
                space_type=space_type,
                barriers=barriers,
                accessibility_score=data.get("accessibility_score", 50),
                features=features,
            )
            nodes.append(node)

        edges = []
        for source, target, data in self.graph.edges(data=True):
            edge = WorldModelEdge(
                source=source,
                target=target,
                traversable=data.get("traversable", True),
                difficulty=Difficulty(data.get("difficulty", "moderate")),
                barriers_in_path=[
                    UUID(b) for b in data.get("barriers_in_path", []) if b
                ],
                distance_estimate=DistanceEstimate(
                    data.get("distance_estimate", "short")
                ),
                notes=data.get("notes"),
            )
            edges.append(edge)

        recommended_path = self.find_recommended_path()

        return WorldModelResponse(
            scan_id=scan_id,
            nodes=nodes,
            edges=edges,
            recommended_path=recommended_path,
        )
