"""Repository layer for data access."""

from .scan_repository import ScanRepository
from .image_repository import ImageRepository

__all__ = ["ScanRepository", "ImageRepository"]
