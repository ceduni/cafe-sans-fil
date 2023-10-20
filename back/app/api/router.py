from fastapi import APIRouter
from app.api.handlers.cafe import cafe_router
from app.api.handlers.user import user_router
from app.api.handlers.order import order_router

router = APIRouter()

router.include_router(cafe_router, tags=["cafes"])
router.include_router(user_router, tags=["users"])
router.include_router(order_router, tags=["orders"])
