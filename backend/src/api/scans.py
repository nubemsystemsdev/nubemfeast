"""Scan API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.database import get_session
from src.schemas.enums import ScanStatus
from src.schemas.scan import (
    ImageResponse,
    ImageUploadResponse,
    ScanCreate,
    ScanDetailResponse,
    ScanResponse,
    ScanUpdate,
)
from src.services.scan_service import ScanService

router = APIRouter()


@router.post("", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
async def create_scan(
    data: ScanCreate,
    session: AsyncSession = Depends(get_session),
) -> ScanResponse:
    """Create a new scan."""
    service = ScanService(session)
    scan = await service.create_scan(data)
    return ScanResponse(
        id=scan.id,
        name=scan.name,
        description=scan.description,
        location=scan.location,
        status=scan.status,
        image_count=0,
        created_at=scan.created_at,
        updated_at=scan.updated_at,
    )


@router.get("", response_model=dict)
async def list_scans(
    status: ScanStatus | None = None,
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """List all scans."""
    service = ScanService(session)
    scans, total = await service.list_scans(status=status, limit=limit, offset=offset)

    return {
        "items": [
            ScanResponse(
                id=s.id,
                name=s.name,
                description=s.description,
                location=s.location,
                status=s.status,
                image_count=s.image_count,
                created_at=s.created_at,
                updated_at=s.updated_at,
            )
            for s in scans
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{scan_id}", response_model=ScanDetailResponse)
async def get_scan(
    scan_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> ScanDetailResponse:
    """Get a scan by ID."""
    service = ScanService(session)
    scan = await service.get_scan(scan_id)

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} not found",
        )

    images = [
        ImageResponse(
            id=img.id,
            filename=img.filename,
            original_filename=img.original_filename,
            file_size=img.file_size,
            mime_type=img.mime_type,
            width=img.width,
            height=img.height,
            sequence_order=img.sequence_order,
            user_description=img.user_description,
            created_at=img.created_at,
            barrier_count=img.barrier_count,
            url=f"/api/scans/{scan_id}/images/{img.id}/file",
        )
        for img in sorted(scan.images, key=lambda x: x.sequence_order)
    ]

    analysis_result = None
    if scan.analysis_result:
        from src.schemas.scan import AnalysisResultSummary

        analysis_result = AnalysisResultSummary(
            status=scan.analysis_result.status,
            total_barriers_found=scan.analysis_result.total_barriers_found,
            accessibility_score=scan.analysis_result.accessibility_score,
        )

    return ScanDetailResponse(
        id=scan.id,
        name=scan.name,
        description=scan.description,
        location=scan.location,
        status=scan.status,
        image_count=scan.image_count,
        created_at=scan.created_at,
        updated_at=scan.updated_at,
        images=images,
        analysis_result=analysis_result,
        has_guide=scan.has_guide,
    )


@router.patch("/{scan_id}", response_model=ScanResponse)
async def update_scan(
    scan_id: UUID,
    data: ScanUpdate,
    session: AsyncSession = Depends(get_session),
) -> ScanResponse:
    """Update a scan."""
    service = ScanService(session)
    scan = await service.update_scan(scan_id, data)

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} not found",
        )

    return ScanResponse(
        id=scan.id,
        name=scan.name,
        description=scan.description,
        location=scan.location,
        status=scan.status,
        image_count=scan.image_count,
        created_at=scan.created_at,
        updated_at=scan.updated_at,
    )


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scan(
    scan_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a scan."""
    service = ScanService(session)
    deleted = await service.delete_scan(scan_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} not found",
        )


@router.get("/{scan_id}/images", response_model=list[ImageResponse])
async def list_images(
    scan_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> list[ImageResponse]:
    """List images for a scan."""
    service = ScanService(session)
    scan = await service.get_scan(scan_id)

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} not found",
        )

    images = await service.get_images(scan_id)
    return [
        ImageResponse(
            id=img.id,
            filename=img.filename,
            original_filename=img.original_filename,
            file_size=img.file_size,
            mime_type=img.mime_type,
            width=img.width,
            height=img.height,
            sequence_order=img.sequence_order,
            user_description=img.user_description,
            created_at=img.created_at,
            barrier_count=img.barrier_count,
            url=f"/api/scans/{scan_id}/images/{img.id}/file",
        )
        for img in images
    ]


@router.post(
    "/{scan_id}/images",
    response_model=ImageUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_images(
    scan_id: UUID,
    files: list[UploadFile],
    session: AsyncSession = Depends(get_session),
) -> ImageUploadResponse:
    """Upload images to a scan."""
    service = ScanService(session)

    try:
        result = await service.upload_images(scan_id, files)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{scan_id}/images/{image_id}/file")
async def get_image_file(
    scan_id: UUID,
    image_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> FileResponse:
    """Get image file."""
    service = ScanService(session)
    images = await service.get_images(scan_id)

    image = next((img for img in images if img.id == image_id), None)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image {image_id} not found",
        )

    return FileResponse(
        image.file_path,
        media_type=image.mime_type,
        filename=image.original_filename,
    )


@router.delete(
    "/{scan_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_image(
    scan_id: UUID,
    image_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete an image."""
    service = ScanService(session)
    deleted = await service.delete_image(scan_id, image_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image {image_id} not found",
        )


@router.post("/{scan_id}/images/reorder", response_model=list[ImageResponse])
async def reorder_images(
    scan_id: UUID,
    image_ids: list[UUID],
    session: AsyncSession = Depends(get_session),
) -> list[ImageResponse]:
    """Reorder images in a scan."""
    service = ScanService(session)
    images = await service.reorder_images(scan_id, image_ids)

    return [
        ImageResponse(
            id=img.id,
            filename=img.filename,
            original_filename=img.original_filename,
            file_size=img.file_size,
            mime_type=img.mime_type,
            width=img.width,
            height=img.height,
            sequence_order=img.sequence_order,
            user_description=img.user_description,
            created_at=img.created_at,
            barrier_count=img.barrier_count,
            url=f"/api/scans/{scan_id}/images/{img.id}/file",
        )
        for img in images
    ]
