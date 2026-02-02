"""FastAPI dependencies."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .database import get_session

# Type alias for database session dependency
DBSession = Annotated[AsyncSession, Depends(get_session)]


async def get_vision_service() -> AsyncGenerator["VisionService", None]:
    """Get vision service dependency."""
    from src.services.vision_service import VisionService

    service = VisionService()
    yield service


async def get_world_model_service() -> AsyncGenerator["WorldModelService", None]:
    """Get world model service dependency."""
    from src.services.world_model_service import WorldModelService

    service = WorldModelService()
    yield service


async def get_guide_service() -> AsyncGenerator["GuideService", None]:
    """Get guide service dependency."""
    from src.services.guide_service import GuideService

    service = GuideService()
    yield service
