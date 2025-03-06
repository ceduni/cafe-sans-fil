"""
Module for routing endpoints.
"""

from fastapi import APIRouter

from app.auth.endpoints import auth_router
from app.cafe.announcement.endpoints import announcement_router
from app.cafe.endpoints import cafe_router
from app.cafe.event.endpoints import event_router
from app.cafe.menu.category.endpoints import category_router
from app.cafe.menu.item.endpoints import item_router
from app.cafe.order.endpoints import order_router
from app.cafe.staff.endpoints import staff_router
from app.interaction.endpoints import interaction_router
from app.search.endpoints import search_router
from app.user.endpoints import user_router

router = APIRouter()
router.include_router(cafe_router, tags=["cafes"])
router.include_router(category_router, tags=["categories"])
router.include_router(item_router, tags=["items"])
router.include_router(staff_router, tags=["staff"])
router.include_router(announcement_router, tags=["announcements"])
router.include_router(event_router, tags=["events"])
router.include_router(order_router, tags=["orders"])
router.include_router(interaction_router, tags=["interactions"])
router.include_router(user_router, tags=["users"])
router.include_router(auth_router, tags=["auth"])
router.include_router(search_router, tags=["search"])


@router.get("/health", include_in_schema=False)
def health():
    """Health check."""
    return {"status": "ok"}
