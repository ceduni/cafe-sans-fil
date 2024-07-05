from fastapi import APIRouter
from app.api.api_v1.handlers.cafe import cafe_router
from app.api.api_v1.handlers.user import user_router
from app.api.api_v1.handlers.order import order_router
from app.api.api_v1.handlers.recommendations import recs_router
from app.api.auth.jwt import auth_router

"""
This module centralizes and aggregates the API routes into a single unified router.
"""

router = APIRouter()
router.include_router(cafe_router, tags=["cafes"])
router.include_router(user_router, tags=["users"])
router.include_router(order_router, tags=["orders"])
router.include_router(auth_router, tags=["auth"])
router.include_router(recs_router, tags=["recommendations"])
