"""
Module for routing endpoints.
"""

from fastapi import APIRouter

from app.announcement.endpoints import announcement_router
from app.auth.endpoints import auth_router
from app.cafe.endpoints import cafe_router
from app.cafe_menu.endpoints import menu_router
from app.event.endpoints import event_router
from app.order.endpoints import order_router
from app.search.endpoints import search_router
from app.user.endpoints import user_router

router = APIRouter()
router.include_router(cafe_router, tags=["cafes"])
router.include_router(menu_router, tags=["menus"])
router.include_router(announcement_router, tags=["announcements"])
router.include_router(event_router, tags=["events"])
router.include_router(user_router, tags=["users"])
router.include_router(order_router, tags=["orders"])
router.include_router(auth_router, tags=["auth"])
router.include_router(search_router, tags=["search"])
