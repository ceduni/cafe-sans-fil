from fastapi import APIRouter
from app.api.api_v1.handlers.cafe import cafe_router
from app.api.api_v1.handlers.menu import menu_router
from app.api.api_v1.handlers.user import user_router
from app.api.api_v1.handlers.order import order_router
from app.api.api_v1.handlers.search import search_router
from app.api.api_v1.handlers.announcement import announcement_router
from app.api.api_v1.handlers.event import event_router
from app.api.auth.jwt import auth_router

"""
This module centralizes and aggregates the API routes into a single unified router.
"""

router = APIRouter()
router.include_router(cafe_router, tags=["cafes"])
router.include_router(menu_router, tags=["menus"])
router.include_router(announcement_router, tags=["announcements"])
router.include_router(event_router, tags=["events"])
router.include_router(user_router, tags=["users"])
router.include_router(order_router, tags=["orders"])
router.include_router(auth_router, tags=["auth"])
router.include_router(search_router, tags=["search"])
