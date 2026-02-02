"""Guide and wheelchair profile database models."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.schemas.enums import WheelchairType

if TYPE_CHECKING:
    from .scan import Scan


class WheelchairProfile(SQLModel, table=True):
    """Wheelchair profile for personalizing guides."""

    __tablename__ = "wheelchair_profiles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)

    # Dimensions (cm)
    width_cm: float
    length_cm: float
    min_door_width_cm: float

    # Capabilities
    max_step_height_cm: float = Field(default=2.0)
    max_slope_percent: float = Field(default=8.0)
    can_handle_gravel: bool = Field(default=False)
    can_handle_grass: bool = Field(default=False)

    wheelchair_type: WheelchairType = Field(default=WheelchairType.MANUAL)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_default: bool = Field(default=False)


class Guide(SQLModel, table=True):
    """Navigation guide generated for a scan."""

    __tablename__ = "guides"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    scan_id: UUID = Field(foreign_key="scans.id", unique=True, index=True)
    wheelchair_profile_id: UUID | None = Field(
        default=None, foreign_key="wheelchair_profiles.id"
    )

    title: str = Field(max_length=255)
    summary: str = Field(max_length=2000)

    navigation_steps_json: str
    alerts_json: str
    recommended_path_json: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    scan: "Scan" = Relationship(back_populates="guide")
    wheelchair_profile: WheelchairProfile | None = Relationship()
