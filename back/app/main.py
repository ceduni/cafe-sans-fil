"""
Main module for the FastAPI application.
"""

from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.announcement.models import Announcement
from app.cafe.models import Cafe, CafeView
from app.config import settings
from app.event.models import Event
from app.menu.models import MenuItem
from app.order.models import Order
from app.router import router
from app.user.models import User

description = """
# API Documentation

This project is currently in development and is hosted on [Render](https://cafesansfil.onrender.com), utilizing a free MongoDB Atlas cluster for its database. The source code is available on [GitHub](https://github.com/ceduni/cafe-sans-fil).

- Explore and test the API endpoints using the [**Swagger UI**](https://cafesansfil-api.onrender.com/docs).
- Use the [**ReDoc**](https://cafesansfil-api.onrender.com/redoc) interface for an alternative view of the API documentation.

## Testing Protected Endpoints
To test protected endpoints, you can use the following structure: [role].[cafe_name]@umontreal.ca

Examples:
- admin.tore.et.fraction@umontreal.ca
- benevole.tore.et.fraction@umontreal.ca

You can also create your own user or utilize any pre-generated users with different roles via the `/api/users` endpoint. All pre-generated users share the same password: `Cafepass1`.

## Role in Endpoint Summaries
In the endpoint summaries, different roles are indicated using color codes for easy identification and include the permissions of the roles below them:
- 🔴 **Administrators** < Café Managers/Admins includes all features.
- 🟢 **Volunteers** < Includes features accessible to UdeM Members.
- 🔵 **Members** < Basic user access features.
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
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    summary="The project is a web application designed to improve café services and ordering processes for UdeM members.",
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


@app.get("/api/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    try:
        result = await db_client.admin.command("serverStatus")
        if result["ok"] == 1.0:
            return {"status": "available"}
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB serverStatus not ok",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )


# --------------------------------------
#           Scheduler
# --------------------------------------

import asyncio
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.order.models import Order, OrderStatus


async def cancel_old_orders():
    """Cancel orders older than 1 hour."""
    now = datetime.utcnow()
    async for order in Order.find(
        {
            "$or": [{"status": OrderStatus.PLACED}, {"status": OrderStatus.READY}],
            "created_at": {"$lt": now - timedelta(hours=1)},
        }
    ):
        order.status = OrderStatus.CANCELLED
        order.updated_at = order.created_at + timedelta(hours=1)
        await order.save()


scheduler = AsyncIOScheduler()
scheduler.add_job(cancel_old_orders, "interval", seconds=30)
scheduler.start()

loop = asyncio.get_event_loop()
if not loop.is_running():
    loop.run_forever()
