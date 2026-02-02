"""Service for scan operations."""

import os
import shutil
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

import aiofiles
from fastapi import UploadFile
from PIL import Image as PILImage
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings
from src.models.image import Image
from src.models.scan import Scan
from src.repositories.image_repository import ImageRepository
from src.repositories.scan_repository import ScanRepository
from src.schemas.enums import ScanStatus
from src.schemas.scan import (
    ImageResponse,
    ImageUploadResponse,
    ScanCreate,
    ScanUpdate,
)


class ScanService:
    """Service for scan-related business logic."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.scan_repo = ScanRepository(session)
        self.image_repo = ImageRepository(session)

    async def create_scan(self, data: ScanCreate) -> Scan:
        """Create a new scan."""
        scan = Scan(
            name=data.name,
            description=data.description,
            location=data.location,
        )
        return await self.scan_repo.create(scan)

    async def get_scan(self, scan_id: UUID) -> Scan | None:
        """Get a scan by ID."""
        return await self.scan_repo.get_by_id(scan_id)

    async def list_scans(
        self,
        status: ScanStatus | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Scan], int]:
        """List scans with optional filtering."""
        return await self.scan_repo.get_all(status=status, limit=limit, offset=offset)

    async def update_scan(self, scan_id: UUID, data: ScanUpdate) -> Scan | None:
        """Update a scan."""
        scan = await self.scan_repo.get_by_id(scan_id)
        if not scan:
            return None

        if data.name is not None:
            scan.name = data.name
        if data.description is not None:
            scan.description = data.description
        if data.location is not None:
            scan.location = data.location

        scan.updated_at = datetime.utcnow()
        return await self.scan_repo.update(scan)

    async def delete_scan(self, scan_id: UUID) -> bool:
        """Delete a scan and its associated files."""
        scan = await self.scan_repo.get_by_id(scan_id)
        if not scan:
            return False

        # Delete uploaded files
        scan_upload_dir = settings.upload_dir / str(scan_id)
        if scan_upload_dir.exists():
            shutil.rmtree(scan_upload_dir)

        await self.scan_repo.delete(scan)
        return True

    async def upload_images(
        self, scan_id: UUID, files: list[UploadFile]
    ) -> ImageUploadResponse:
        """Upload images to a scan."""
        scan = await self.scan_repo.get_by_id(scan_id)
        if not scan:
            raise ValueError(f"Scan {scan_id} not found")

        # Check image limit
        current_count = len(scan.images) if scan.images else 0
        remaining_slots = settings.max_images_per_scan - current_count
        if remaining_slots <= 0:
            raise ValueError(
                f"Scan already has {current_count} images "
                f"(max: {settings.max_images_per_scan})"
            )

        # Update status
        if scan.status == ScanStatus.PENDING:
            scan.status = ScanStatus.UPLOADING
            await self.scan_repo.update(scan)

        # Create upload directory
        upload_dir = settings.upload_dir / str(scan_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        uploaded_images: list[Image] = []
        errors: list[str] = []
        start_order = await self.image_repo.get_max_sequence_order(scan_id) + 1

        for i, file in enumerate(files[: remaining_slots]):
            try:
                image = await self._process_upload(
                    scan_id, file, upload_dir, start_order + i
                )
                uploaded_images.append(image)
            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")

        # Save images to database
        if uploaded_images:
            await self.image_repo.create_many(uploaded_images)

            # Update scan status
            scan.status = ScanStatus.READY
            scan.updated_at = datetime.utcnow()
            await self.scan_repo.update(scan)

        return ImageUploadResponse(
            uploaded=len(uploaded_images),
            failed=len(errors),
            images=[self._image_to_response(img, scan_id) for img in uploaded_images],
            errors=errors,
        )

    async def _process_upload(
        self, scan_id: UUID, file: UploadFile, upload_dir: Path, sequence_order: int
    ) -> Image:
        """Process a single file upload."""
        if file.content_type not in settings.allowed_image_types:
            raise ValueError(f"Invalid file type: {file.content_type}")

        # Read file content
        content = await file.read()
        if len(content) > settings.max_upload_size_bytes:
            raise ValueError(
                f"File too large: {len(content)} bytes "
                f"(max: {settings.max_upload_size_bytes})"
            )

        # Generate unique filename
        ext = Path(file.filename or "image").suffix or ".jpg"
        filename = f"{uuid4()}{ext}"
        file_path = upload_dir / filename

        # Save file
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        # Get image dimensions
        width, height = None, None
        try:
            with PILImage.open(file_path) as img:
                width, height = img.size
        except Exception:
            pass

        return Image(
            scan_id=scan_id,
            filename=filename,
            original_filename=file.filename or "unknown",
            file_path=str(file_path),
            file_size=len(content),
            mime_type=file.content_type or "image/jpeg",
            width=width,
            height=height,
            sequence_order=sequence_order,
        )

    async def get_images(self, scan_id: UUID) -> list[Image]:
        """Get all images for a scan."""
        return await self.image_repo.get_by_scan_id(scan_id)

    async def delete_image(self, scan_id: UUID, image_id: UUID) -> bool:
        """Delete an image from a scan."""
        image = await self.image_repo.get_by_id(image_id)
        if not image or image.scan_id != scan_id:
            return False

        # Delete file
        if os.path.exists(image.file_path):
            os.remove(image.file_path)

        await self.image_repo.delete(image)
        return True

    async def reorder_images(
        self, scan_id: UUID, image_ids: list[UUID]
    ) -> list[Image]:
        """Reorder images in a scan."""
        return await self.image_repo.reorder(scan_id, image_ids)

    def _image_to_response(self, image: Image, scan_id: UUID) -> ImageResponse:
        """Convert Image model to response schema."""
        return ImageResponse(
            id=image.id,
            filename=image.filename,
            original_filename=image.original_filename,
            file_size=image.file_size,
            mime_type=image.mime_type,
            width=image.width,
            height=image.height,
            sequence_order=image.sequence_order,
            user_description=image.user_description,
            created_at=image.created_at,
            barrier_count=image.barrier_count,
            url=f"/api/scans/{scan_id}/images/{image.id}/file",
        )
