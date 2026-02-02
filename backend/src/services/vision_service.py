"""Service for Vision AI analysis using OpenAI GPT-4o."""

import base64
import json
from pathlib import Path
from uuid import UUID

from openai import AsyncOpenAI

from src.core.config import settings
from src.models.analysis import Barrier
from src.schemas.enums import BarrierSeverity, BarrierType


class VisionService:
    """Service for analyzing images with Vision AI."""

    ANALYSIS_PROMPT = """Analyze this image for wheelchair accessibility. Identify any barriers or obstacles that could affect wheelchair users.

For each barrier found, provide:
1. barrier_type: One of: step, stairs, narrow_door, narrow_passage, steep_ramp, uneven_surface, obstacle, heavy_door, revolving_door, threshold, gravel, grass, slope, other
2. severity: One of: low (manageable with care), medium (difficult, may need help), high (very difficult, needs alternative), critical (impassable)
3. description: Brief description of the barrier
4. estimated_dimensions: If possible, estimate width/height/depth in centimeters
5. recommendation: Suggestion for navigating or avoiding the barrier
6. confidence: Your confidence level (0.0-1.0) in this assessment
7. bbox: If you can identify the location, provide normalized coordinates (0-1) as {x, y, width, height}

Also analyze:
- Space type (entrance, corridor, room, stairway, elevator, bathroom, outdoor, parking, other)
- Overall accessibility features (ramps, handrails, elevators, lighting quality, floor type)

Respond ONLY with valid JSON in this format:
{
    "space_type": "corridor",
    "features": {
        "has_ramp": false,
        "has_handrails": true,
        "has_elevator": false,
        "lighting": "good",
        "floor_type": "tile"
    },
    "barriers": [
        {
            "barrier_type": "narrow_door",
            "severity": "medium",
            "description": "Door appears to be approximately 70cm wide",
            "estimated_width_cm": 70,
            "estimated_height_cm": null,
            "estimated_depth_cm": null,
            "recommendation": "May be tight for standard wheelchairs. Consider using side approach.",
            "confidence": 0.8,
            "bbox": {"x": 0.3, "y": 0.2, "width": 0.15, "height": 0.6}
        }
    ],
    "overall_description": "Indoor corridor with moderate accessibility. Main concern is door width.",
    "accessibility_score": 65
}

If no barriers are found, return an empty barriers array and a high accessibility_score (90-100)."""

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def analyze_image(self, image_path: str, image_id: UUID) -> dict:
        """Analyze a single image for accessibility barriers."""
        # Read and encode image
        image_data = self._encode_image(image_path)

        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.ANALYSIS_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}",
                                    "detail": "high",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=settings.openai_max_tokens,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from Vision AI")

            result = json.loads(content)
            result["image_id"] = str(image_id)
            return result

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Vision AI response: {e}")

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def parse_barriers(self, analysis_result: dict, image_id: UUID) -> list[Barrier]:
        """Parse analysis result into Barrier models."""
        barriers = []
        for barrier_data in analysis_result.get("barriers", []):
            barrier_type = self._parse_barrier_type(barrier_data.get("barrier_type"))
            severity = self._parse_severity(barrier_data.get("severity"))

            bbox = barrier_data.get("bbox", {})

            barrier = Barrier(
                image_id=image_id,
                barrier_type=barrier_type,
                severity=severity,
                description=barrier_data.get("description", "Unknown barrier"),
                bbox_x=bbox.get("x"),
                bbox_y=bbox.get("y"),
                bbox_width=bbox.get("width"),
                bbox_height=bbox.get("height"),
                estimated_width_cm=barrier_data.get("estimated_width_cm"),
                estimated_height_cm=barrier_data.get("estimated_height_cm"),
                estimated_depth_cm=barrier_data.get("estimated_depth_cm"),
                recommendation=barrier_data.get("recommendation"),
                confidence=barrier_data.get("confidence", 0.5),
            )
            barriers.append(barrier)

        return barriers

    def _parse_barrier_type(self, type_str: str | None) -> BarrierType:
        """Parse barrier type string to enum."""
        if not type_str:
            return BarrierType.OTHER

        type_map = {t.value: t for t in BarrierType}
        return type_map.get(type_str.lower(), BarrierType.OTHER)

    def _parse_severity(self, severity_str: str | None) -> BarrierSeverity:
        """Parse severity string to enum."""
        if not severity_str:
            return BarrierSeverity.MEDIUM

        severity_map = {s.value: s for s in BarrierSeverity}
        return severity_map.get(severity_str.lower(), BarrierSeverity.MEDIUM)
