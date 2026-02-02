"""Enum definitions for the application."""

from enum import Enum


class ScanStatus(str, Enum):
    """Status of a scan."""

    PENDING = "pending"
    UPLOADING = "uploading"
    READY = "ready"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisStatus(str, Enum):
    """Status of an analysis."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class BarrierType(str, Enum):
    """Type of accessibility barrier."""

    STEP = "step"
    STAIRS = "stairs"
    NARROW_DOOR = "narrow_door"
    NARROW_PASSAGE = "narrow_passage"
    STEEP_RAMP = "steep_ramp"
    UNEVEN_SURFACE = "uneven_surface"
    OBSTACLE = "obstacle"
    HEAVY_DOOR = "heavy_door"
    REVOLVING_DOOR = "revolving_door"
    THRESHOLD = "threshold"
    GRAVEL = "gravel"
    GRASS = "grass"
    SLOPE = "slope"
    OTHER = "other"


class BarrierSeverity(str, Enum):
    """Severity level of a barrier."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WheelchairType(str, Enum):
    """Type of wheelchair."""

    MANUAL = "manual"
    ELECTRIC = "electric"
    SPORT = "sport"
    PEDIATRIC = "pediatric"
    BARIATRIC = "bariatric"


class SpaceType(str, Enum):
    """Type of space in the world model."""

    ENTRANCE = "entrance"
    CORRIDOR = "corridor"
    ROOM = "room"
    STAIRWAY = "stairway"
    ELEVATOR = "elevator"
    BATHROOM = "bathroom"
    OUTDOOR = "outdoor"
    PARKING = "parking"
    OTHER = "other"


class AccessibilityRating(str, Enum):
    """Accessibility rating for a navigation step."""

    ACCESSIBLE = "accessible"
    CAUTION = "caution"
    DIFFICULT = "difficult"
    INACCESSIBLE = "inaccessible"


class Difficulty(str, Enum):
    """Difficulty level for traversing an edge."""

    EASY = "easy"
    MODERATE = "moderate"
    DIFFICULT = "difficult"
    IMPASSABLE = "impassable"


class DistanceEstimate(str, Enum):
    """Estimated distance between nodes."""

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
