from fastapi import APIRouter, HTTPException, Path, Query, status, Request, Depends
from typing import List
from app.schemas.recommendation_schema import RecommendationOut, RecommendationUpdate
from app.models.user_model import User
from app.services.recommendation_service import RecommendationService
from app.services.user_service import UserService
from app.api.deps.user_deps import get_current_user
from uuid import uuid4


"""
This module defines the API routes related to recommendations in the application.
"""

recs_router = APIRouter()

# --------------------------------------
#               User
# --------------------------------------

recs_router.get(
    "/recommendations/{cafe_slug}",
    response_model=RecommendationOut,
    summary="🔴 Items recommended",
    description="Retrive a list of all user's recommendations in this cafe."
)
async def get_user_recommendations(cafe_slug: str):
    current_user: User = Depends(get_current_user)
    return await RecommendationService.get_recommendations_by_id(current_user.user_id, cafe_slug)

recs_router.put(
    "/recommendations/{cafe_slug}",
    response_model=RecommendationUpdate,
    summary="🔵 Update user recommendation",
    description="Modify an existing user recommendation"
)
async def update_user_recommendations(
        data: RecommendationUpdate,
        cafe_slug: str,
        current_user: User = Depends(get_current_user)
):
    return await RecommendationService.update_user_recommendations(current_user.user_id, cafe_slug, data)

# --------------------------------------
#              Public
# --------------------------------------

recs_router.get(
    "/recommendations/{cafe_slug}",
    response_model=RecommendationOut,
    summary="🔵 Public recommendations",
    description="Retrive a list of all public recommendations"
)
async def get_public_recommendations(cafe_slug: str):
    return await RecommendationService.get_public_recommendations(cafe_slug)

recs_router.put(
    "/recommendations/{cafe_slug}",
    response_model=RecommendationUpdate,
    summary="🔵 Update public recommendation",
    description="Update an existing public recommendation"
)
async def update_public_recommendations(
        data: RecommendationUpdate,
        cafe_slug: str
):
    return await RecommendationService.update_public_recommendations(cafe_slug, data)


# --------------------------------------
#               Bot
# --------------------------------------

recs_router.get(
    "/recommendations/{cafe_slug}",
    response_model=RecommendationOut,
    summary="🔵 Bot recommendations",
    description="Retrive a list of all bot recommendations"
)
async def get_bot_recommendations(cafe_slug: str):
    return await RecommendationService.get_bot_recommendations(cafe_slug)

recs_router.put(
    "/recommendations/{cafe_slug}",
    response_model=RecommendationUpdate,
    summary="🔵 Update bot recommendation",
    description="Update an existing bot recommendation"
)
async def update_bot_recommendations(
        data: RecommendationUpdate,
        cafe_slug: str
):
    return await RecommendationService.update_bot_recommendations(cafe_slug, data)