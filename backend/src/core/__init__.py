"""Core module - Configuration and dependencies."""

from .config import settings
from .database import get_session, init_db

__all__ = ["settings", "get_session", "init_db"]
