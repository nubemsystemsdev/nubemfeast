"""API routers."""

from fastapi import APIRouter

from .scans import router as scans_router
from .analysis import router as analysis_router
from .navigation import router as navigation_router

api_router = APIRouter()

api_router.include_router(scans_router, prefix="/scans", tags=["Scans"])
api_router.include_router(analysis_router, tags=["Analysis"])
api_router.include_router(navigation_router, tags=["Navigation"])

__all__ = ["api_router"]
