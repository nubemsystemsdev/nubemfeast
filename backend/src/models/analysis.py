"""Analysis-related database models."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.schemas.enums import AnalysisStatus, BarrierSeverity, BarrierType

if TYPE_CHECKING:
    from .image import Image
    from .scan import Scan


class AnalysisResult(SQLModel, table=True):
    """Consolidated analysis result for a scan."""

    __tablename__ = "analysis_results"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    scan_id: UUID = Field(foreign_key="scans.id", unique=True, index=True)

    status: AnalysisStatus = Field(default=AnalysisStatus.PENDING, index=True)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None

    total_images_analyzed: int = Field(default=0)
    total_barriers_found: int = Field(default=0)
    accessibility_score: float | None = None

    world_model_json: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    scan: "Scan" = Relationship(back_populates="analysis_result")


class Barrier(SQLModel, table=True):
    """Accessibility barrier detected in an image."""

    __tablename__ = "barriers"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    image_id: UUID = Field(foreign_key="images.id", index=True)

    barrier_type: BarrierType = Field(index=True)
    severity: BarrierSeverity = Field(index=True)

    description: str = Field(max_length=1000)

    # Bounding box (normalized 0-1 coordinates)
    bbox_x: float | None = None
    bbox_y: float | None = None
    bbox_width: float | None = None
    bbox_height: float | None = None

    # Estimated dimensions (cm)
    estimated_width_cm: float | None = None
    estimated_height_cm: float | None = None
    estimated_depth_cm: float | None = None

    recommendation: str | None = Field(default=None, max_length=500)
    confidence: float = Field(default=0.0)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    image: "Image" = Relationship(back_populates="barriers")
