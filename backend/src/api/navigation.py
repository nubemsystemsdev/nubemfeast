"""Navigation API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.database import get_session
from src.models.analysis import AnalysisResult
from src.models.guide import Guide, WheelchairProfile
from src.schemas.enums import AnalysisStatus, WheelchairType
from src.schemas.navigation import (
    GuideRequest,
    GuideResponse,
    WheelchairProfileCreate,
    WheelchairProfileResponse,
    WorldModelResponse,
)
from src.services.guide_service import GuideService
from src.services.scan_service import ScanService
from src.services.world_model_service import WorldModelService

router = APIRouter()


@router.get("/scans/{scan_id}/guide", response_model=GuideResponse)
async def get_guide(
    scan_id: UUID,
    wheelchair_profile_id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
) -> GuideResponse:
    """Get navigation guide for a scan."""
    # Get existing guide
    statement = select(Guide).where(Guide.scan_id == scan_id)
    result = await session.execute(statement)
    guide = result.scalar_one_or_none()

    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guide for scan {scan_id} not found. Run analysis first.",
        )

    # Get wheelchair profile
    profile = None
    if guide.wheelchair_profile_id:
        statement = select(WheelchairProfile).where(
            WheelchairProfile.id == guide.wheelchair_profile_id
        )
        result = await session.execute(statement)
        profile = result.scalar_one_or_none()

    # Get analysis for accessibility score
    statement = select(AnalysisResult).where(AnalysisResult.scan_id == scan_id)
    result = await session.execute(statement)
    analysis = result.scalar_one_or_none()

    guide_service = GuideService()
    return guide_service.guide_to_response(
        guide,
        profile,
        analysis.accessibility_score if analysis else None,
    )


@router.post(
    "/scans/{scan_id}/guide",
    response_model=GuideResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_guide(
    scan_id: UUID,
    request: GuideRequest | None = None,
    session: AsyncSession = Depends(get_session),
) -> GuideResponse:
    """Generate or regenerate navigation guide."""
    # Get scan
    scan_service = ScanService(session)
    scan = await scan_service.get_scan(scan_id)

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} not found",
        )

    # Check analysis is complete
    statement = select(AnalysisResult).where(AnalysisResult.scan_id == scan_id)
    result = await session.execute(statement)
    analysis = result.scalar_one_or_none()

    if not analysis or analysis.status != AnalysisStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Analysis not completed. Run analysis first.",
        )

    # Get wheelchair profile
    profile = None
    if request and request.wheelchair_profile_id:
        statement = select(WheelchairProfile).where(
            WheelchairProfile.id == request.wheelchair_profile_id
        )
        result = await session.execute(statement)
        profile = result.scalar_one_or_none()
    else:
        # Get default profile
        statement = select(WheelchairProfile).where(WheelchairProfile.is_default == True)
        result = await session.execute(statement)
        profile = result.scalar_one_or_none()

    # Build analysis results dict
    images = await scan_service.get_images(scan_id)

    # Load world model to get analysis data
    world_model_service = WorldModelService()
    if analysis.world_model_json:
        world_model_service.from_json(analysis.world_model_json)

    analysis_results: dict[UUID, dict] = {}
    for node_id, data in world_model_service.graph.nodes(data=True):
        image_id = UUID(data.get("image_id", ""))
        analysis_results[image_id] = {
            "space_type": data.get("space_type", "other"),
            "features": data.get("features", {}),
            "accessibility_score": data.get("accessibility_score", 50),
            "overall_description": "",
        }

    # Generate guide
    guide_service = GuideService()
    guide = guide_service.generate_guide(scan_id, images, analysis_results, profile)

    # Delete existing guide
    statement = select(Guide).where(Guide.scan_id == scan_id)
    result = await session.execute(statement)
    existing_guide = result.scalar_one_or_none()
    if existing_guide:
        await session.delete(existing_guide)

    session.add(guide)
    await session.flush()
    await session.refresh(guide)

    return guide_service.guide_to_response(
        guide,
        profile,
        analysis.accessibility_score,
    )


@router.get("/scans/{scan_id}/world-model", response_model=WorldModelResponse)
async def get_world_model(
    scan_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> WorldModelResponse:
    """Get world model graph for a scan."""
    # Get analysis
    statement = select(AnalysisResult).where(AnalysisResult.scan_id == scan_id)
    result = await session.execute(statement)
    analysis = result.scalar_one_or_none()

    if not analysis or not analysis.world_model_json:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"World model for scan {scan_id} not found",
        )

    # Load world model
    world_model_service = WorldModelService()
    world_model_service.from_json(analysis.world_model_json)

    return world_model_service.to_response(scan_id)


@router.get("/wheelchair-profiles", response_model=list[WheelchairProfileResponse])
async def list_wheelchair_profiles(
    session: AsyncSession = Depends(get_session),
) -> list[WheelchairProfileResponse]:
    """List all wheelchair profiles."""
    statement = select(WheelchairProfile).order_by(
        WheelchairProfile.is_default.desc(), WheelchairProfile.name
    )
    result = await session.execute(statement)
    profiles = result.scalars().all()

    # If no profiles, create defaults
    if not profiles:
        guide_service = GuideService()
        for profile_data in guide_service.DEFAULT_PROFILES:
            profile = WheelchairProfile(
                name=profile_data["name"],
                description=profile_data["description"],
                width_cm=profile_data["width_cm"],
                length_cm=profile_data["length_cm"],
                min_door_width_cm=profile_data["min_door_width_cm"],
                max_step_height_cm=profile_data["max_step_height_cm"],
                max_slope_percent=profile_data["max_slope_percent"],
                can_handle_gravel=profile_data["can_handle_gravel"],
                can_handle_grass=profile_data["can_handle_grass"],
                wheelchair_type=WheelchairType(profile_data["wheelchair_type"]),
                is_default=profile_data["is_default"],
            )
            session.add(profile)
        await session.flush()

        result = await session.execute(statement)
        profiles = result.scalars().all()

    return [
        WheelchairProfileResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            width_cm=p.width_cm,
            length_cm=p.length_cm,
            min_door_width_cm=p.min_door_width_cm,
            max_step_height_cm=p.max_step_height_cm,
            max_slope_percent=p.max_slope_percent,
            can_handle_gravel=p.can_handle_gravel,
            can_handle_grass=p.can_handle_grass,
            wheelchair_type=p.wheelchair_type,
            is_default=p.is_default,
        )
        for p in profiles
    ]


@router.post(
    "/wheelchair-profiles",
    response_model=WheelchairProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_wheelchair_profile(
    data: WheelchairProfileCreate,
    session: AsyncSession = Depends(get_session),
) -> WheelchairProfileResponse:
    """Create a custom wheelchair profile."""
    profile = WheelchairProfile(
        name=data.name,
        description=data.description,
        width_cm=data.width_cm,
        length_cm=data.length_cm,
        min_door_width_cm=data.min_door_width_cm,
        max_step_height_cm=data.max_step_height_cm,
        max_slope_percent=data.max_slope_percent,
        can_handle_gravel=data.can_handle_gravel,
        can_handle_grass=data.can_handle_grass,
        wheelchair_type=data.wheelchair_type,
        is_default=False,
    )
    session.add(profile)
    await session.flush()
    await session.refresh(profile)

    return WheelchairProfileResponse(
        id=profile.id,
        name=profile.name,
        description=profile.description,
        width_cm=profile.width_cm,
        length_cm=profile.length_cm,
        min_door_width_cm=profile.min_door_width_cm,
        max_step_height_cm=profile.max_step_height_cm,
        max_slope_percent=profile.max_slope_percent,
        can_handle_gravel=profile.can_handle_gravel,
        can_handle_grass=profile.can_handle_grass,
        wheelchair_type=profile.wheelchair_type,
        is_default=profile.is_default,
    )


@router.get("/wheelchair-profiles/{profile_id}", response_model=WheelchairProfileResponse)
async def get_wheelchair_profile(
    profile_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> WheelchairProfileResponse:
    """Get a wheelchair profile by ID."""
    statement = select(WheelchairProfile).where(WheelchairProfile.id == profile_id)
    result = await session.execute(statement)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wheelchair profile {profile_id} not found",
        )

    return WheelchairProfileResponse(
        id=profile.id,
        name=profile.name,
        description=profile.description,
        width_cm=profile.width_cm,
        length_cm=profile.length_cm,
        min_door_width_cm=profile.min_door_width_cm,
        max_step_height_cm=profile.max_step_height_cm,
        max_slope_percent=profile.max_slope_percent,
        can_handle_gravel=profile.can_handle_gravel,
        can_handle_grass=profile.can_handle_grass,
        wheelchair_type=profile.wheelchair_type,
        is_default=profile.is_default,
    )


@router.delete(
    "/wheelchair-profiles/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_wheelchair_profile(
    profile_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a wheelchair profile."""
    statement = select(WheelchairProfile).where(WheelchairProfile.id == profile_id)
    result = await session.execute(statement)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wheelchair profile {profile_id} not found",
        )

    if profile.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete default profile",
        )

    await session.delete(profile)
