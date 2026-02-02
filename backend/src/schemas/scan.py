"""Scan-related Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import AnalysisStatus, ScanStatus


class ScanCreate(BaseModel):
    """Schema for creating a new scan."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    location: str | None = Field(default=None, max_length=500)


class ScanUpdate(BaseModel):
    """Schema for updating a scan."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    location: str | None = Field(default=None, max_length=500)


class ScanResponse(BaseModel):
    """Schema for scan response."""

    id: UUID
    name: str
    description: str | None
    location: str | None
    status: ScanStatus
    image_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ImageResponse(BaseModel):
    """Schema for image response."""

    id: UUID
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    width: int | None
    height: int | None
    sequence_order: int
    user_description: str | None
    created_at: datetime
    barrier_count: int = 0
    url: str

    model_config = {"from_attributes": True}


class AnalysisResultSummary(BaseModel):
    """Summary of analysis result for scan detail."""

    status: AnalysisStatus
    total_barriers_found: int
    accessibility_score: float | None

    model_config = {"from_attributes": True}


class ScanDetailResponse(ScanResponse):
    """Schema for detailed scan response."""

    images: list[ImageResponse]
    analysis_result: AnalysisResultSummary | None
    has_guide: bool


class ImageUploadResponse(BaseModel):
    """Schema for image upload response."""

    uploaded: int
    failed: int
    images: list[ImageResponse]
    errors: list[str]
