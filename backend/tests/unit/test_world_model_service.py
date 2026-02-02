"""Tests for WorldModelService."""

import pytest
from uuid import uuid4

from src.models.image import Image
from src.schemas.enums import BarrierSeverity, Difficulty
from src.services.world_model_service import WorldModelService


class TestWorldModelService:
    """Tests for WorldModelService."""

    def test_build_empty_world_model(self):
        """Test building world model with no images."""
        service = WorldModelService()
        graph = service.build_world_model([], {})

        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0

    def test_build_world_model_single_image(self):
        """Test building world model with single image."""
        service = WorldModelService()

        image = Image(
            id=uuid4(),
            scan_id=uuid4(),
            filename="test.jpg",
            original_filename="test.jpg",
            file_path="/path/test.jpg",
            file_size=1000,
            mime_type="image/jpeg",
            sequence_order=0,
        )
        image.barriers = []

        analysis_results = {
            image.id: {
                "space_type": "entrance",
                "features": {"has_ramp": True},
                "accessibility_score": 85,
            }
        }

        graph = service.build_world_model([image], analysis_results)

        assert len(graph.nodes) == 1
        assert len(graph.edges) == 0

        node = graph.nodes["node_0"]
        assert node["space_type"] == "entrance"
        assert node["accessibility_score"] == 85

    def test_build_world_model_multiple_images(self):
        """Test building world model with multiple images."""
        service = WorldModelService()
        scan_id = uuid4()

        images = [
            Image(
                id=uuid4(),
                scan_id=scan_id,
                filename=f"test_{i}.jpg",
                original_filename=f"test_{i}.jpg",
                file_path=f"/path/test_{i}.jpg",
                file_size=1000,
                mime_type="image/jpeg",
                sequence_order=i,
            )
            for i in range(3)
        ]
        for img in images:
            img.barriers = []

        analysis_results = {
            img.id: {"accessibility_score": 80} for img in images
        }

        graph = service.build_world_model(images, analysis_results)

        assert len(graph.nodes) == 3
        # Bidirectional edges: 2 pairs * 2 = 4
        assert len(graph.edges) == 4

    def test_calculate_difficulty_no_barriers(self):
        """Test difficulty calculation with no barriers."""
        service = WorldModelService()

        difficulty = service._calculate_difficulty([], [])
        assert difficulty == Difficulty.EASY

    def test_calculate_difficulty_with_barriers(self):
        """Test difficulty calculation with barriers of different severities."""
        service = WorldModelService()

        low_barriers = [{"severity": "low"}]
        assert service._calculate_difficulty(low_barriers, []) == Difficulty.EASY

        medium_barriers = [{"severity": "medium"}]
        assert service._calculate_difficulty(medium_barriers, []) == Difficulty.MODERATE

        high_barriers = [{"severity": "high"}]
        assert service._calculate_difficulty(high_barriers, []) == Difficulty.DIFFICULT

        critical_barriers = [{"severity": "critical"}]
        assert service._calculate_difficulty(critical_barriers, []) == Difficulty.IMPASSABLE

    def test_find_recommended_path_empty(self):
        """Test finding path in empty graph."""
        service = WorldModelService()

        path = service.find_recommended_path()
        assert path is None

    def test_find_recommended_path(self):
        """Test finding recommended path."""
        service = WorldModelService()
        scan_id = uuid4()

        images = [
            Image(
                id=uuid4(),
                scan_id=scan_id,
                filename=f"test_{i}.jpg",
                original_filename=f"test_{i}.jpg",
                file_path=f"/path/test_{i}.jpg",
                file_size=1000,
                mime_type="image/jpeg",
                sequence_order=i,
            )
            for i in range(3)
        ]
        for img in images:
            img.barriers = []

        service.build_world_model(images, {})

        path = service.find_recommended_path()
        assert path == ["node_0", "node_1", "node_2"]

    def test_json_serialization(self):
        """Test graph JSON serialization/deserialization."""
        service = WorldModelService()
        scan_id = uuid4()

        images = [
            Image(
                id=uuid4(),
                scan_id=scan_id,
                filename="test.jpg",
                original_filename="test.jpg",
                file_path="/path/test.jpg",
                file_size=1000,
                mime_type="image/jpeg",
                sequence_order=0,
            )
        ]
        images[0].barriers = []

        service.build_world_model(images, {})

        json_str = service.to_json()
        assert json_str is not None

        # Create new service and load
        new_service = WorldModelService()
        new_service.from_json(json_str)

        assert len(new_service.graph.nodes) == 1
