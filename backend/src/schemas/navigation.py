"""Navigation-related Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import (
    AccessibilityRating,
    BarrierSeverity,
    BarrierType,
    Difficulty,
    DistanceEstimate,
    SpaceType,
    WheelchairType,
)


class BarrierSummary(BaseModel):
    """Summary of a barrier for navigation."""

    id: UUID
    barrier_type: BarrierType
    severity: BarrierSeverity
    description: str
    recommendation: str | None = None

    model_config = {"from_attributes": True}


class NavigationStep(BaseModel):
    """A step in the navigation guide."""

    step_number: int
    image_id: UUID
    image_url: str
    title: str
    description: str
    barriers: list[BarrierSummary]
    alerts: list[str]
    recommendations: list[str]
    accessibility_rating: AccessibilityRating


class GuideRequest(BaseModel):
    """Schema for generating a guide."""

    wheelchair_profile_id: UUID | None = None


class WheelchairProfileCreate(BaseModel):
    """Schema for creating a wheelchair profile."""

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    width_cm: float = Field(gt=0)
    length_cm: float = Field(gt=0)
    min_door_width_cm: float = Field(gt=0)
    max_step_height_cm: float = Field(default=2.0, ge=0)
    max_slope_percent: float = Field(default=8.0, ge=0)
    can_handle_gravel: bool = False
    can_handle_grass: bool = False
    wheelchair_type: WheelchairType = WheelchairType.MANUAL


class WheelchairProfileResponse(BaseModel):
    """Schema for wheelchair profile response."""

    id: UUID
    name: str
    description: str | None
    width_cm: float
    length_cm: float
    min_door_width_cm: float
    max_step_height_cm: float
    max_slope_percent: float
    can_handle_gravel: bool
    can_handle_grass: bool
    wheelchair_type: WheelchairType
    is_default: bool

    model_config = {"from_attributes": True}


class GuideResponse(BaseModel):
    """Schema for guide response."""

    id: UUID
    scan_id: UUID
    title: str
    summary: str
    accessibility_score: float | None = Field(default=None, ge=0, le=100)
    navigation_steps: list[NavigationStep]
    critical_alerts: list[str]
    wheelchair_profile: WheelchairProfileResponse | None
    created_at: datetime

    model_config = {"from_attributes": True}


class NodeFeatures(BaseModel):
    """Features of a node in the world model."""

    has_ramp: bool = False
    has_handrails: bool = False
    has_elevator: bool = False
    lighting: str = "adequate"
    floor_type: str = "unknown"


class WorldModelNode(BaseModel):
    """A node in the world model graph."""

    id: str
    image_id: UUID
    image_url: str
    label: str
    space_type: SpaceType
    barriers: list[BarrierSummary]
    accessibility_score: float = Field(ge=0, le=100)
    features: NodeFeatures


class WorldModelEdge(BaseModel):
    """An edge in the world model graph."""

    source: str
    target: str
    traversable: bool
    difficulty: Difficulty
    barriers_in_path: list[UUID]
    distance_estimate: DistanceEstimate
    notes: str | None = None


class WorldModelResponse(BaseModel):
    """Schema for world model response."""

    scan_id: UUID
    nodes: list[WorldModelNode]
    edges: list[WorldModelEdge]
    recommended_path: list[str] | None = None
