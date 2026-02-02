"""Repository for Image operations."""

from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.image import Image


class ImageRepository:
    """Repository for Image CRUD operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, image: Image) -> Image:
        """Create a new image."""
        self.session.add(image)
        await self.session.flush()
        await self.session.refresh(image)
        return image

    async def create_many(self, images: list[Image]) -> list[Image]:
        """Create multiple images."""
        for image in images:
            self.session.add(image)
        await self.session.flush()
        for image in images:
            await self.session.refresh(image)
        return images

    async def get_by_id(self, image_id: UUID) -> Image | None:
        """Get an image by ID."""
        statement = select(Image).where(Image.id == image_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_scan_id(self, scan_id: UUID) -> list[Image]:
        """Get all images for a scan."""
        statement = (
            select(Image)
            .where(Image.scan_id == scan_id)
            .order_by(Image.sequence_order)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def update(self, image: Image) -> Image:
        """Update an image."""
        self.session.add(image)
        await self.session.flush()
        await self.session.refresh(image)
        return image

    async def delete(self, image: Image) -> None:
        """Delete an image."""
        await self.session.delete(image)
        await self.session.flush()

    async def get_max_sequence_order(self, scan_id: UUID) -> int:
        """Get the maximum sequence order for a scan."""
        statement = (
            select(Image.sequence_order)
            .where(Image.scan_id == scan_id)
            .order_by(Image.sequence_order.desc())
            .limit(1)
        )
        result = await self.session.execute(statement)
        max_order = result.scalar_one_or_none()
        return max_order if max_order is not None else -1

    async def reorder(self, scan_id: UUID, image_ids: list[UUID]) -> list[Image]:
        """Reorder images in a scan."""
        images = await self.get_by_scan_id(scan_id)
        image_map = {img.id: img for img in images}

        for order, image_id in enumerate(image_ids):
            if image_id in image_map:
                image_map[image_id].sequence_order = order

        await self.session.flush()
        return await self.get_by_scan_id(scan_id)
