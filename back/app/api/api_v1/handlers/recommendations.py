from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
)
from app.schemas.recommendation_schema import (
    ItemOut, 
    ItemUpdate,
    CafeUpdate, 
    CafeOut,
    UserRecommendationUpdate, 
    UserRecommendationOut,
) 
from app.services.recommendation_service import RecommendationService
from app.api.deps.user_deps import get_current_user
from typing import List, Dict
from recommender_systems.routines.run_bot_recommendations import run_bot_recommendations
from recommender_systems.routines.missing_items import main
"""
This module defines the API routes related to recommendations in the application.
"""

recs_router = APIRouter()

# --------------------------------------
#            Cafe & Item
# --------------------------------------

@recs_router.get(
    "/recommendations/item/{item_id}",
    response_model=ItemOut,
    summary="Get item",
    description="Retrive an item"
)
async def get_item(item_id: str):
    item = await RecommendationService.get_item(item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item

@recs_router.put(
    "/recommendations/item/{item_id}",
    response_model=ItemOut,
    summary="🔵 Update item",
    description="Modify an existing item"
)
async def update_item(
    data: ItemUpdate,
    item_id: str
):
    return await RecommendationService.update_item(item_id=item_id, data=data)

@recs_router.get(
    "/recommendations/cafe_for_recommendation/{cafe_slug}",
    response_model=CafeOut,
    summary="Get cafe",
    description="Retrive a cafe."
)
async def get_cafe(cafe_slug: str):
    cafe = await RecommendationService.get_cafe(cafe_slug=cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )
    return cafe

@recs_router.put(
    "/recommendations/cafe/health_score/{cafe_slug}",
    response_model=CafeOut,
    summary="🔵 Update cafe health_score",
    description="Modify an existing cafe"
)
async def update_cafe_health_score(
    data: CafeUpdate,
    cafe_slug: str
):
    return await RecommendationService.update_cafe(cafe_slug=cafe_slug, data=data)

# --------------------------------------
#               User
# --------------------------------------

@recs_router.get(
    "/recommendations/user/{user_id}",
    response_model=UserRecommendationOut,
    summary="Get user",
    description="Retrive an user",
)
async def get_user(user_id: str):
    user = await RecommendationService.get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

@recs_router.get(
    "/recommendations/user/{user_id}/{cafe_slug}",
    response_model=List[str],
    summary="Get user personnal recommendation",
    description="Retrive a list of all user's recommendations in this cafe."
)
async def get_user_personnal_recommendations(
    user_id: str,
    cafe_slug: str):
    try:
        return await RecommendationService.get_user_personnal_recommendations_by_id(user_id=user_id, cafe_slug=cafe_slug)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@recs_router.put(
    "/recommendations/user/{user_id}",
    response_model=UserRecommendationOut,
    summary="🔴 Update user personnal recommendations for a specific cafe",
    description="Modify an existing user recommendation"
)
async def update_user_personnal_recommendations(
        data: UserRecommendationUpdate,
        user_id: str
):
    return await RecommendationService.update_user(user_id=user_id, data=data)

@recs_router.get(
        "/recommendations/cafes_recommendations/{user_id}",
        response_model=List[str],
        summary="Get user cafe recommendations",
        description="Retrive a list of all cafes recommended to the user."
)
async def get_user_cafe_recommendations(user_id: str):
    try:
        return await RecommendationService.get_user_cafe_recommendations(user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@recs_router.put(
        "/recommendations/cafes_recommendations/{user_id}",
        response_model=UserRecommendationOut,
        summary="🔴 Update user cafe recommendations",
        description="Modify an existing user recommendation"
)
async def update_user_cafe_recommendations(
        data: UserRecommendationUpdate,
        user_id: str
):
    return await RecommendationService.update_user(user_id=user_id, data=data)

@recs_router.get(
    "/recommendations/missing_items",
    response_model=List[Dict[str, str | int]],
    summary="🔵 Get Missing Items",
    description="Retrieve a list of missing items.",
)
async def get_missing_items():
    result = await main()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No missing items"
        )
    return result

# --------------------------------------
#              Public
# --------------------------------------

@recs_router.get(
    "/recommendations/public/{cafe_slug}",
    response_model=List[str],
    summary="🔵 Get public recommendations",
    description="Retrive a list of all public recommendations"
)
async def get_public_recommendations(cafe_slug: str):
    recs = await RecommendationService.get_public_recommendations(cafe_slug)
    if not recs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recommendation not found"
        )
    return recs

@recs_router.put(
    "/recommendations/public/{cafe_slug}",
    response_model=CafeOut,
    summary="🔵 Update public recommendation",
    description="Update an existing public recommendation"
)
async def update_public_recommendations(
        data: CafeUpdate,
        cafe_slug: str
):
    return await RecommendationService.update_cafe(cafe_slug, data)

# --------------------------------------
#               Bot
# --------------------------------------

@recs_router.get(
    "/recommendations/bot/{cafe_slug}",
    response_model=List[str],
    summary="🔵 Get bot recommendations",
    description="Retrive a list of all items recommended by the bot"
)
async def get_bot_recommendations(cafe_slug: str):
    recommendations = await run_bot_recommendations(cafe_slug)
    if not recommendations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recommendation not found"
        )
    return recommendations


