"""Scan database model."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.schemas.enums import ScanStatus

if TYPE_CHECKING:
    from .analysis import AnalysisResult
    from .guide import Guide
    from .image import Image


class Scan(SQLModel, table=True):
    """Represents a scan/tour of a space."""

    __tablename__ = "scans"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=255, index=True)
    description: str | None = Field(default=None, max_length=1000)
    location: str | None = Field(default=None, max_length=500)
    status: ScanStatus = Field(default=ScanStatus.PENDING, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    images: list["Image"] = Relationship(
        back_populates="scan",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    analysis_result: "AnalysisResult | None" = Relationship(
        back_populates="scan",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "uselist": False},
    )
    guide: "Guide | None" = Relationship(
        back_populates="scan",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "uselist": False},
    )

    @property
    def image_count(self) -> int:
        """Get the number of images in this scan."""
        return len(self.images) if self.images else 0

    @property
    def has_guide(self) -> bool:
        """Check if this scan has a guide."""
        return self.guide is not None
