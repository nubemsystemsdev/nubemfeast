"""Analysis API endpoints."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.database import get_session
from src.models.analysis import AnalysisResult, Barrier
from src.models.scan import Scan
from src.schemas.analysis import (
    AnalysisDetailResponse,
    AnalysisRequest,
    AnalysisResponse,
    BarrierResponse,
    BarriersBySeverity,
    ImageAnalysisSummary,
)
from src.schemas.enums import AnalysisStatus, BarrierSeverity, BarrierType, ScanStatus
from src.services.scan_service import ScanService
from src.services.vision_service import VisionService
from src.services.world_model_service import WorldModelService

router = APIRouter()


@router.post(
    "/scans/{scan_id}/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_analysis(
    scan_id: UUID,
    request: AnalysisRequest | None = None,
    session: AsyncSession = Depends(get_session),
) -> AnalysisResponse:
    """Start accessibility analysis for a scan."""
    # Get scan
    scan_service = ScanService(session)
    scan = await scan_service.get_scan(scan_id)

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} not found",
        )

    if not scan.images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No images to analyze",
        )

    # Check existing analysis
    if scan.analysis_result:
        if scan.analysis_result.status == AnalysisStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Analysis already in progress",
            )
        if scan.analysis_result.status == AnalysisStatus.COMPLETED and not (
            request and request.force
        ):
            return AnalysisResponse(
                id=scan.analysis_result.id,
                scan_id=scan_id,
                status=scan.analysis_result.status,
                started_at=scan.analysis_result.started_at,
                completed_at=scan.analysis_result.completed_at,
                error_message=scan.analysis_result.error_message,
                total_images_analyzed=scan.analysis_result.total_images_analyzed,
                total_barriers_found=scan.analysis_result.total_barriers_found,
                accessibility_score=scan.analysis_result.accessibility_score,
            )

    # Create or update analysis result
    if scan.analysis_result:
        analysis = scan.analysis_result
        analysis.status = AnalysisStatus.IN_PROGRESS
        analysis.started_at = datetime.utcnow()
        analysis.completed_at = None
        analysis.error_message = None
    else:
        analysis = AnalysisResult(
            scan_id=scan_id,
            status=AnalysisStatus.IN_PROGRESS,
            started_at=datetime.utcnow(),
        )
        session.add(analysis)

    # Update scan status
    scan.status = ScanStatus.ANALYZING
    await session.flush()

    # Perform analysis (synchronously for now, could be async task in production)
    try:
        vision_service = VisionService()
        world_model_service = WorldModelService()

        analysis_results: dict[UUID, dict] = {}
        total_barriers = 0

        for image in scan.images:
            try:
                result = await vision_service.analyze_image(image.file_path, image.id)
                analysis_results[image.id] = result

                # Create barrier records
                barriers = vision_service.parse_barriers(result, image.id)
                for barrier in barriers:
                    session.add(barrier)
                total_barriers += len(barriers)

            except Exception as e:
                analysis_results[image.id] = {
                    "error": str(e),
                    "accessibility_score": 0,
                }

        # Build world model
        await session.flush()  # Ensure barriers are saved
        # Reload images with barriers
        images = await scan_service.get_images(scan_id)
        world_model_service.build_world_model(images, analysis_results)

        # Calculate overall score
        scores = [
            r.get("accessibility_score", 50)
            for r in analysis_results.values()
            if "error" not in r
        ]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Update analysis result
        analysis.status = AnalysisStatus.COMPLETED
        analysis.completed_at = datetime.utcnow()
        analysis.total_images_analyzed = len(scan.images)
        analysis.total_barriers_found = total_barriers
        analysis.accessibility_score = avg_score
        analysis.world_model_json = world_model_service.to_json()

        # Update scan status
        scan.status = ScanStatus.COMPLETED

    except Exception as e:
        analysis.status = AnalysisStatus.FAILED
        analysis.error_message = str(e)
        analysis.completed_at = datetime.utcnow()
        scan.status = ScanStatus.FAILED

    await session.flush()
    await session.refresh(analysis)

    return AnalysisResponse(
        id=analysis.id,
        scan_id=scan_id,
        status=analysis.status,
        started_at=analysis.started_at,
        completed_at=analysis.completed_at,
        error_message=analysis.error_message,
        total_images_analyzed=analysis.total_images_analyzed,
        total_barriers_found=analysis.total_barriers_found,
        accessibility_score=analysis.accessibility_score,
    )


@router.get("/scans/{scan_id}/analysis", response_model=AnalysisDetailResponse)
async def get_analysis(
    scan_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> AnalysisDetailResponse:
    """Get analysis result for a scan."""
    # Get analysis
    statement = select(AnalysisResult).where(AnalysisResult.scan_id == scan_id)
    result = await session.execute(statement)
    analysis = result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis for scan {scan_id} not found",
        )

    # Get scan with images
    scan_service = ScanService(session)
    scan = await scan_service.get_scan(scan_id)
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} not found",
        )

    # Calculate barrier statistics
    barriers_by_severity = BarriersBySeverity()
    barriers_by_type: dict[str, int] = {}
    images_with_barriers: list[ImageAnalysisSummary] = []

    for image in sorted(scan.images, key=lambda x: x.sequence_order):
        max_severity = None
        for barrier in image.barriers:
            # Count by severity
            if barrier.severity == BarrierSeverity.LOW:
                barriers_by_severity.low += 1
            elif barrier.severity == BarrierSeverity.MEDIUM:
                barriers_by_severity.medium += 1
            elif barrier.severity == BarrierSeverity.HIGH:
                barriers_by_severity.high += 1
            elif barrier.severity == BarrierSeverity.CRITICAL:
                barriers_by_severity.critical += 1

            # Count by type
            type_key = barrier.barrier_type.value
            barriers_by_type[type_key] = barriers_by_type.get(type_key, 0) + 1

            # Track max severity
            if max_severity is None or self._severity_rank(
                barrier.severity
            ) > self._severity_rank(max_severity):
                max_severity = barrier.severity

        if image.barriers:
            images_with_barriers.append(
                ImageAnalysisSummary(
                    image_id=image.id,
                    image_url=f"/api/scans/{scan_id}/images/{image.id}/file",
                    sequence_order=image.sequence_order,
                    barrier_count=len(image.barriers),
                    max_severity=max_severity,
                )
            )

    return AnalysisDetailResponse(
        id=analysis.id,
        scan_id=scan_id,
        status=analysis.status,
        started_at=analysis.started_at,
        completed_at=analysis.completed_at,
        error_message=analysis.error_message,
        total_images_analyzed=analysis.total_images_analyzed,
        total_barriers_found=analysis.total_barriers_found,
        accessibility_score=analysis.accessibility_score,
        barriers_by_severity=barriers_by_severity,
        barriers_by_type=barriers_by_type,
        images_with_barriers=images_with_barriers,
    )


def _severity_rank(severity: BarrierSeverity) -> int:
    """Get numeric rank for severity comparison."""
    ranks = {
        BarrierSeverity.LOW: 1,
        BarrierSeverity.MEDIUM: 2,
        BarrierSeverity.HIGH: 3,
        BarrierSeverity.CRITICAL: 4,
    }
    return ranks.get(severity, 0)


@router.get("/scans/{scan_id}/analysis/barriers", response_model=list[BarrierResponse])
async def list_barriers(
    scan_id: UUID,
    severity: BarrierSeverity | None = None,
    type: BarrierType | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[BarrierResponse]:
    """List all barriers for a scan."""
    scan_service = ScanService(session)
    scan = await scan_service.get_scan(scan_id)

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} not found",
        )

    barriers = []
    for image in scan.images:
        for barrier in image.barriers:
            if severity and barrier.severity != severity:
                continue
            if type and barrier.barrier_type != type:
                continue

            barriers.append(
                BarrierResponse(
                    id=barrier.id,
                    image_id=barrier.image_id,
                    barrier_type=barrier.barrier_type,
                    severity=barrier.severity,
                    description=barrier.description,
                    bbox_x=barrier.bbox_x,
                    bbox_y=barrier.bbox_y,
                    bbox_width=barrier.bbox_width,
                    bbox_height=barrier.bbox_height,
                    estimated_width_cm=barrier.estimated_width_cm,
                    estimated_height_cm=barrier.estimated_height_cm,
                    estimated_depth_cm=barrier.estimated_depth_cm,
                    recommendation=barrier.recommendation,
                    confidence=barrier.confidence,
                )
            )

    return barriers


@router.get("/images/{image_id}/barriers", response_model=list[BarrierResponse])
async def get_image_barriers(
    image_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> list[BarrierResponse]:
    """Get barriers for a specific image."""
    statement = select(Barrier).where(Barrier.image_id == image_id)
    result = await session.execute(statement)
    barriers = result.scalars().all()

    return [
        BarrierResponse(
            id=b.id,
            image_id=b.image_id,
            barrier_type=b.barrier_type,
            severity=b.severity,
            description=b.description,
            bbox_x=b.bbox_x,
            bbox_y=b.bbox_y,
            bbox_width=b.bbox_width,
            bbox_height=b.bbox_height,
            estimated_width_cm=b.estimated_width_cm,
            estimated_height_cm=b.estimated_height_cm,
            estimated_depth_cm=b.estimated_depth_cm,
            recommendation=b.recommendation,
            confidence=b.confidence,
        )
        for b in barriers
    ]
