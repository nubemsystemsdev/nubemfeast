"""Integration tests for Scans API."""

import pytest
from httpx import AsyncClient

from src.schemas.enums import ScanStatus


@pytest.mark.asyncio
class TestScansAPI:
    """Integration tests for Scans API endpoints."""

    async def test_create_scan(self, client: AsyncClient):
        """Test creating a new scan."""
        response = await client.post(
            "/api/scans",
            json={
                "name": "Test Museum",
                "description": "A test scan",
                "location": "Madrid, Spain",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Museum"
        assert data["description"] == "A test scan"
        assert data["location"] == "Madrid, Spain"
        assert data["status"] == ScanStatus.PENDING.value
        assert data["image_count"] == 0
        assert "id" in data

    async def test_create_scan_minimal(self, client: AsyncClient):
        """Test creating a scan with minimal data."""
        response = await client.post(
            "/api/scans",
            json={"name": "Minimal Scan"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Minimal Scan"
        assert data["description"] is None
        assert data["location"] is None

    async def test_create_scan_validation_error(self, client: AsyncClient):
        """Test creating a scan with invalid data."""
        response = await client.post(
            "/api/scans",
            json={"name": ""},  # Empty name should fail
        )

        assert response.status_code == 422

    async def test_list_scans_empty(self, client: AsyncClient):
        """Test listing scans when empty."""
        response = await client.get("/api/scans")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    async def test_list_scans(self, client: AsyncClient):
        """Test listing scans."""
        # Create some scans
        for i in range(3):
            await client.post(
                "/api/scans",
                json={"name": f"Scan {i}"},
            )

        response = await client.get("/api/scans")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3

    async def test_list_scans_pagination(self, client: AsyncClient):
        """Test scan listing pagination."""
        for i in range(5):
            await client.post(
                "/api/scans",
                json={"name": f"Scan {i}"},
            )

        response = await client.get("/api/scans?limit=2&offset=0")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["limit"] == 2
        assert data["offset"] == 0

        response = await client.get("/api/scans?limit=2&offset=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["offset"] == 2

    async def test_get_scan(self, client: AsyncClient):
        """Test getting a specific scan."""
        # Create scan
        create_response = await client.post(
            "/api/scans",
            json={"name": "Test Scan"},
        )
        scan_id = create_response.json()["id"]

        # Get scan
        response = await client.get(f"/api/scans/{scan_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == scan_id
        assert data["name"] == "Test Scan"
        assert "images" in data
        assert "analysis_result" in data
        assert "has_guide" in data

    async def test_get_scan_not_found(self, client: AsyncClient):
        """Test getting a non-existent scan."""
        response = await client.get(
            "/api/scans/00000000-0000-0000-0000-000000000000"
        )

        assert response.status_code == 404

    async def test_update_scan(self, client: AsyncClient):
        """Test updating a scan."""
        # Create scan
        create_response = await client.post(
            "/api/scans",
            json={"name": "Original Name"},
        )
        scan_id = create_response.json()["id"]

        # Update scan
        response = await client.patch(
            f"/api/scans/{scan_id}",
            json={"name": "Updated Name", "description": "New description"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "New description"

    async def test_delete_scan(self, client: AsyncClient):
        """Test deleting a scan."""
        # Create scan
        create_response = await client.post(
            "/api/scans",
            json={"name": "To Delete"},
        )
        scan_id = create_response.json()["id"]

        # Delete scan
        response = await client.delete(f"/api/scans/{scan_id}")
        assert response.status_code == 204

        # Verify deleted
        response = await client.get(f"/api/scans/{scan_id}")
        assert response.status_code == 404

    async def test_delete_scan_not_found(self, client: AsyncClient):
        """Test deleting a non-existent scan."""
        response = await client.delete(
            "/api/scans/00000000-0000-0000-0000-000000000000"
        )

        assert response.status_code == 404
