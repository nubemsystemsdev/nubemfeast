"""Repository for Scan operations."""

from uuid import UUID

from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.scan import Scan
from src.schemas.enums import ScanStatus


class ScanRepository:
    """Repository for Scan CRUD operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, scan: Scan) -> Scan:
        """Create a new scan."""
        self.session.add(scan)
        await self.session.flush()
        await self.session.refresh(scan)
        return scan

    async def get_by_id(self, scan_id: UUID) -> Scan | None:
        """Get a scan by ID."""
        statement = select(Scan).where(Scan.id == scan_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        status: ScanStatus | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Scan], int]:
        """Get all scans with optional filtering."""
        statement = select(Scan)

        if status:
            statement = statement.where(Scan.status == status)

        # Get total count
        count_statement = select(func.count()).select_from(statement.subquery())
        total_result = await self.session.execute(count_statement)
        total = total_result.scalar() or 0

        # Apply pagination and ordering
        statement = statement.order_by(Scan.created_at.desc())
        statement = statement.offset(offset).limit(limit)

        result = await self.session.execute(statement)
        scans = list(result.scalars().all())

        return scans, total

    async def update(self, scan: Scan) -> Scan:
        """Update a scan."""
        self.session.add(scan)
        await self.session.flush()
        await self.session.refresh(scan)
        return scan

    async def delete(self, scan: Scan) -> None:
        """Delete a scan."""
        await self.session.delete(scan)
        await self.session.flush()

    async def update_status(self, scan_id: UUID, status: ScanStatus) -> Scan | None:
        """Update scan status."""
        scan = await self.get_by_id(scan_id)
        if scan:
            scan.status = status
            return await self.update(scan)
        return None
