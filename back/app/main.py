"""
Main module for the FastAPI application.
"""

from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient

from app.announcement.models import Announcement
from app.cafe.menu.item.models import MenuItem
from app.cafe.models import Cafe, CafeView
from app.config import settings
from app.event.models import Event
from app.order.models import Order
from app.order.scheduler import order_scheduler
from app.router import router
from app.user.models import User

description = """
# API Documentation

You can also create your own user or utilize any pre-generated users with different roles via the `/api/users` endpoint. All pre-generated users share the same password: `Cafepass1`.

## Permissions
`MEMBER` < `VOLUNTEER` < `ADMIN` < `OWNER`
"""

db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan for the application."""
    await init_beanie(
        database=db_client[settings.MONGO_DB_NAME],
        document_models=[Cafe, CafeView, MenuItem, User, Order, Announcement, Event],
        recreate_views=True,
    )
    await order_scheduler.start()
    yield
    await order_scheduler.shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_STR)
add_pagination(app)
