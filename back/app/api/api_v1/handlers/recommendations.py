from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
)
from app.schemas.recommendation_schema import ItemRecommendationOut, ItemRecommendationUpdate, CafeRecommendationOut, CafeRecommendationUpdate
from app.models.user_model import User
from app.services.recommendation_service import RecommendationService
from app.api.deps.user_deps import get_current_user


"""
This module defines the API routes related to recommendations in the application.
"""

recs_router = APIRouter()

# --------------------------------------
#               User
# --------------------------------------

@recs_router.get(
    "/recommendations/user/{cafe_slug}",
    response_model=ItemRecommendationOut,
    summary="🔴 Items recommended",
    description="Retrive a list of all user's recommendations in this cafe."
)
async def get_user_recommendations(cafe_slug: str,
    current_user: User = Depends(get_current_user)):
    
    print(current_user)
    return await RecommendationService.get_recommendations_by_id(current_user.user_id, cafe_slug)

@recs_router.put(
    "/recommendations/user/{cafe_slug}",
    response_model=ItemRecommendationUpdate,
    summary="🔵 Update user recommendation",
    description="Modify an existing user recommendation"
)
async def update_user_recommendations(
        data: ItemRecommendationUpdate,
        cafe_slug: str,
        current_user: User = Depends(get_current_user)
):
    return await RecommendationService.update_user_recommendations(current_user.user_id, cafe_slug, data)

# --------------------------------------
#              Public
# --------------------------------------

@recs_router.get(
    "/recommendations/public/{cafe_slug}",
    response_model=ItemRecommendationOut,
    summary="🔵 Public recommendations",
    description="Retrive a list of all public recommendations"
)
async def get_public_recommendations(cafe_slug: str):
    return await RecommendationService.get_public_recommendations(cafe_slug)

@recs_router.put(
    "/recommendations/public/{cafe_slug}",
    response_model=ItemRecommendationUpdate,
    summary="🔵 Update public recommendation",
    description="Update an existing public recommendation"
)
async def update_public_recommendations(
        data: ItemRecommendationUpdate,
        cafe_slug: str
):
    return await RecommendationService.update_public_recommendations(cafe_slug, data)


# --------------------------------------
#               Bot
# --------------------------------------

@recs_router.get(
    "/recommendations/bot/{cafe_slug}",
    response_model=ItemRecommendationOut,
    summary="🔵 Bot recommendations",
    description="Retrive a list of all bot recommendations"
)
async def get_bot_recommendations(cafe_slug: str):
    recs = await RecommendationService.get_bot_recommendations(cafe_slug)
    if not recs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recommendation not found"
        )
    return recs

@recs_router.put(
    "/recommendations/bot/{cafe_slug}",
    response_model=ItemRecommendationUpdate,
    summary="🔵 Update bot recommendation",
    description="Update an existing bot recommendation"
)
async def update_bot_recommendations(
        data: ItemRecommendationUpdate,
        cafe_slug: str
):
    return await RecommendationService.update_bot_recommendations(cafe_slug, data)


# --------------------------------------
#               Cafe
# --------------------------------------

@recs_router.get(
    "/recommendations/cafe/{user_id}",
    response_model=CafeRecommendationOut,
    summary="🔵 Get cafe recommendation",
    description="Get an existing cafe recommendation"
)
async def get_user_cafe_recommendations(user_id: str):
    recs = await RecommendationService.get_user_cafe_recommendations(user_id)
    if not recs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recommendation not found"
        )
    return recs

@recs_router.put(
    "/recommendations/cafe/{user_id}",
    response_model=CafeRecommendationUpdate,
    summary="🔵 Update cafe recommendation",
    description="Update an existing cafe recommendation"
)
async def update_user_cafe_recommendations(
        data: CafeRecommendationUpdate,
        user_id: str
):
    try:
        return await RecommendationService.update_user_cafe_recommendations(user_id, data)
    except ValueError as e:
        error_message = str(e)
        if error_message == "Recommendation not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=error_message
            )