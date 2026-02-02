"""Service for generating navigation guides."""

import json
from uuid import UUID

from src.models.analysis import Barrier
from src.models.guide import Guide, WheelchairProfile
from src.models.image import Image
from src.schemas.enums import AccessibilityRating, BarrierSeverity
from src.schemas.navigation import (
    BarrierSummary,
    GuideResponse,
    NavigationStep,
    WheelchairProfileResponse,
)


class GuideService:
    """Service for generating accessibility guides."""

    DEFAULT_PROFILES = [
        {
            "name": "Manual Estándar",
            "description": "Silla de ruedas manual estándar para adultos",
            "width_cm": 65,
            "length_cm": 105,
            "min_door_width_cm": 75,
            "max_step_height_cm": 2,
            "max_slope_percent": 8,
            "can_handle_gravel": False,
            "can_handle_grass": False,
            "wheelchair_type": "manual",
            "is_default": True,
        },
        {
            "name": "Eléctrica Estándar",
            "description": "Silla de ruedas eléctrica estándar",
            "width_cm": 70,
            "length_cm": 120,
            "min_door_width_cm": 80,
            "max_step_height_cm": 5,
            "max_slope_percent": 12,
            "can_handle_gravel": False,
            "can_handle_grass": False,
            "wheelchair_type": "electric",
            "is_default": False,
        },
        {
            "name": "Deportiva",
            "description": "Silla de ruedas deportiva de alto rendimiento",
            "width_cm": 60,
            "length_cm": 90,
            "min_door_width_cm": 70,
            "max_step_height_cm": 2,
            "max_slope_percent": 10,
            "can_handle_gravel": False,
            "can_handle_grass": False,
            "wheelchair_type": "sport",
            "is_default": False,
        },
        {
            "name": "Pediátrica",
            "description": "Silla de ruedas para niños",
            "width_cm": 55,
            "length_cm": 85,
            "min_door_width_cm": 65,
            "max_step_height_cm": 2,
            "max_slope_percent": 8,
            "can_handle_gravel": False,
            "can_handle_grass": False,
            "wheelchair_type": "pediatric",
            "is_default": False,
        },
        {
            "name": "Bariátrica",
            "description": "Silla de ruedas bariátrica de alta capacidad",
            "width_cm": 80,
            "length_cm": 130,
            "min_door_width_cm": 90,
            "max_step_height_cm": 3,
            "max_slope_percent": 6,
            "can_handle_gravel": False,
            "can_handle_grass": False,
            "wheelchair_type": "bariatric",
            "is_default": False,
        },
    ]

    def generate_guide(
        self,
        scan_id: UUID,
        images: list[Image],
        analysis_results: dict[UUID, dict],
        wheelchair_profile: WheelchairProfile | None = None,
    ) -> Guide:
        """Generate a navigation guide for a scan."""
        # Build navigation steps
        steps = []
        critical_alerts = []

        for image in sorted(images, key=lambda x: x.sequence_order):
            analysis = analysis_results.get(image.id, {})
            step = self._create_navigation_step(
                image, analysis, wheelchair_profile, len(steps) + 1
            )
            steps.append(step)

            # Collect critical alerts
            for barrier in image.barriers:
                if barrier.severity == BarrierSeverity.CRITICAL:
                    critical_alerts.append(
                        f"Paso {len(steps)}: {barrier.description}"
                    )

        # Calculate overall accessibility score
        scores = [
            analysis_results.get(img.id, {}).get("accessibility_score", 50)
            for img in images
        ]
        avg_score = sum(scores) / len(scores) if scores else 50

        # Generate title and summary
        title = self._generate_title(images, avg_score)
        summary = self._generate_summary(images, critical_alerts, avg_score)

        # Create guide
        guide = Guide(
            scan_id=scan_id,
            wheelchair_profile_id=wheelchair_profile.id if wheelchair_profile else None,
            title=title,
            summary=summary,
            navigation_steps_json=json.dumps([s.model_dump() for s in steps], default=str),
            alerts_json=json.dumps(critical_alerts),
            recommended_path_json=None,
        )

        return guide

    def _create_navigation_step(
        self,
        image: Image,
        analysis: dict,
        profile: WheelchairProfile | None,
        step_number: int,
    ) -> NavigationStep:
        """Create a navigation step for an image."""
        barriers = [
            BarrierSummary(
                id=b.id,
                barrier_type=b.barrier_type,
                severity=b.severity,
                description=b.description,
                recommendation=b.recommendation,
            )
            for b in image.barriers
        ]

        alerts = []
        recommendations = []

        # Generate alerts and recommendations based on barriers and profile
        for barrier in image.barriers:
            if barrier.severity in [BarrierSeverity.HIGH, BarrierSeverity.CRITICAL]:
                alerts.append(barrier.description)

            if barrier.recommendation:
                recommendations.append(barrier.recommendation)

            # Profile-specific checks
            if profile and barrier.barrier_type.value == "narrow_door":
                if barrier.estimated_width_cm:
                    if barrier.estimated_width_cm < profile.min_door_width_cm:
                        alerts.append(
                            f"Puerta de {barrier.estimated_width_cm}cm - "
                            f"su silla necesita {profile.min_door_width_cm}cm"
                        )

        # Determine accessibility rating
        rating = self._calculate_rating(image.barriers)

        return NavigationStep(
            step_number=step_number,
            image_id=image.id,
            image_url=f"/api/scans/{image.scan_id}/images/{image.id}/file",
            title=f"Paso {step_number}: {analysis.get('space_type', 'Ubicación').title()}",
            description=analysis.get("overall_description", ""),
            barriers=barriers,
            alerts=alerts,
            recommendations=recommendations,
            accessibility_rating=rating,
        )

    def _calculate_rating(self, barriers: list[Barrier]) -> AccessibilityRating:
        """Calculate accessibility rating based on barriers."""
        if not barriers:
            return AccessibilityRating.ACCESSIBLE

        severities = [b.severity for b in barriers]

        if BarrierSeverity.CRITICAL in severities:
            return AccessibilityRating.INACCESSIBLE
        elif BarrierSeverity.HIGH in severities:
            return AccessibilityRating.DIFFICULT
        elif BarrierSeverity.MEDIUM in severities:
            return AccessibilityRating.CAUTION
        else:
            return AccessibilityRating.ACCESSIBLE

    def _generate_title(self, images: list[Image], score: float) -> str:
        """Generate guide title."""
        if score >= 80:
            accessibility = "Alta Accesibilidad"
        elif score >= 60:
            accessibility = "Accesibilidad Moderada"
        elif score >= 40:
            accessibility = "Accesibilidad Limitada"
        else:
            accessibility = "Accesibilidad Restringida"

        return f"Guía de Navegación - {accessibility}"

    def _generate_summary(
        self, images: list[Image], critical_alerts: list[str], score: float
    ) -> str:
        """Generate guide summary."""
        total_barriers = sum(len(img.barriers) for img in images)

        summary_parts = [
            f"Este recorrido consta de {len(images)} pasos.",
            f"Puntuación de accesibilidad: {score:.0f}/100.",
        ]

        if total_barriers > 0:
            summary_parts.append(
                f"Se han detectado {total_barriers} barreras de accesibilidad."
            )

        if critical_alerts:
            summary_parts.append(
                f"ATENCIÓN: Hay {len(critical_alerts)} alertas críticas."
            )

        return " ".join(summary_parts)

    def guide_to_response(
        self,
        guide: Guide,
        wheelchair_profile: WheelchairProfile | None,
        accessibility_score: float | None,
    ) -> GuideResponse:
        """Convert Guide model to response schema."""
        steps = json.loads(guide.navigation_steps_json)
        navigation_steps = [
            NavigationStep(**step) for step in steps
        ]

        alerts = json.loads(guide.alerts_json)

        profile_response = None
        if wheelchair_profile:
            profile_response = WheelchairProfileResponse(
                id=wheelchair_profile.id,
                name=wheelchair_profile.name,
                description=wheelchair_profile.description,
                width_cm=wheelchair_profile.width_cm,
                length_cm=wheelchair_profile.length_cm,
                min_door_width_cm=wheelchair_profile.min_door_width_cm,
                max_step_height_cm=wheelchair_profile.max_step_height_cm,
                max_slope_percent=wheelchair_profile.max_slope_percent,
                can_handle_gravel=wheelchair_profile.can_handle_gravel,
                can_handle_grass=wheelchair_profile.can_handle_grass,
                wheelchair_type=wheelchair_profile.wheelchair_type,
                is_default=wheelchair_profile.is_default,
            )

        return GuideResponse(
            id=guide.id,
            scan_id=guide.scan_id,
            title=guide.title,
            summary=guide.summary,
            accessibility_score=accessibility_score,
            navigation_steps=navigation_steps,
            critical_alerts=alerts,
            wheelchair_profile=profile_response,
            created_at=guide.created_at,
        )
