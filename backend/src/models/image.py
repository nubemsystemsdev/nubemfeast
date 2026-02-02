"""Image database model."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .analysis import Barrier
    from .scan import Scan


class Image(SQLModel, table=True):
    """Represents an image within a scan."""

    __tablename__ = "images"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    scan_id: UUID = Field(foreign_key="scans.id", index=True)

    filename: str = Field(max_length=255)
    original_filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int
    mime_type: str = Field(max_length=50)

    width: int | None = None
    height: int | None = None

    sequence_order: int = Field(default=0)
    user_description: str | None = Field(default=None, max_length=500)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    scan: "Scan" = Relationship(back_populates="images")
    barriers: list["Barrier"] = Relationship(
        back_populates="image",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    @property
    def barrier_count(self) -> int:
        """Get the number of barriers in this image."""
        return len(self.barriers) if self.barriers else 0
