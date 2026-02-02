"""Analysis-related Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import AnalysisStatus, BarrierSeverity, BarrierType


class AnalysisRequest(BaseModel):
    """Schema for starting an analysis."""

    wheelchair_profile_id: UUID | None = None
    force: bool = False


class AnalysisResponse(BaseModel):
    """Schema for analysis response."""

    id: UUID
    scan_id: UUID
    status: AnalysisStatus
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None
    total_images_analyzed: int
    total_barriers_found: int
    accessibility_score: float | None = Field(ge=0, le=100)

    model_config = {"from_attributes": True}


class BarrierResponse(BaseModel):
    """Schema for barrier response."""

    id: UUID
    image_id: UUID
    barrier_type: BarrierType
    severity: BarrierSeverity
    description: str
    bbox_x: float | None = Field(default=None, ge=0, le=1)
    bbox_y: float | None = Field(default=None, ge=0, le=1)
    bbox_width: float | None = Field(default=None, ge=0, le=1)
    bbox_height: float | None = Field(default=None, ge=0, le=1)
    estimated_width_cm: float | None = None
    estimated_height_cm: float | None = None
    estimated_depth_cm: float | None = None
    recommendation: str | None = None
    confidence: float = Field(ge=0, le=1)

    model_config = {"from_attributes": True}


class ImageAnalysisSummary(BaseModel):
    """Summary of analysis for a single image."""

    image_id: UUID
    image_url: str
    sequence_order: int
    barrier_count: int
    max_severity: BarrierSeverity | None

    model_config = {"from_attributes": True}


class BarriersByType(BaseModel):
    """Barrier counts grouped by type."""

    step: int = 0
    stairs: int = 0
    narrow_door: int = 0
    narrow_passage: int = 0
    steep_ramp: int = 0
    uneven_surface: int = 0
    obstacle: int = 0
    heavy_door: int = 0
    revolving_door: int = 0
    threshold: int = 0
    gravel: int = 0
    grass: int = 0
    slope: int = 0
    other: int = 0


class BarriersBySeverity(BaseModel):
    """Barrier counts grouped by severity."""

    low: int = 0
    medium: int = 0
    high: int = 0
    critical: int = 0


class AnalysisDetailResponse(AnalysisResponse):
    """Schema for detailed analysis response."""

    barriers_by_severity: BarriersBySeverity
    barriers_by_type: dict[str, int]
    images_with_barriers: list[ImageAnalysisSummary]
