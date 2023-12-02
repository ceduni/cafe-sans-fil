# FastAPI and middleware imports
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Database and Beanie initialization
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Application settings and router
from app.core.config import settings
from app.api.api_v1.router import router
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.models.order_model import Order

"""
Main application initialization for Café Sans Fil.
Sets up FastAPI application, CORS middleware, and initializes the database connection.
"""

description = """
This project is in development and is hosted on [Render](https://cafesansfil.onrender.com) using a free MongoDB Atlas cluster for the database. You can find the source code on [GitHub](https://github.com/ceduni/udem-cafe)

\nYou can use the [**Swagger UI**](https://cafesansfil-api.onrender.com/docs) to explore the API and test the endpoints.  
You can also use the [**ReDoc**](https://cafesansfil-api.onrender.com/redoc) interface to explore the API.

To test protected endpoints, you can use the following credentials:
- Username: `cafesansfil`
- Password: `Cafepass1`

Alternatively, you can create your own user or you can use any users with different roles using the `/api/users` endpoint.  
All pre-generated users have the same password: `Cafepass1`.
"""

db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db_client[settings.MONGO_DB_NAME],
        document_models=[
            User,
            Cafe,
            Order
        ]
    )
    yield
    
app = FastAPI(
    title=settings.PROJECT_NAME,
    summary="Café sans-fil API for managing cafes, users, and orders.", 
    description=description,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
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
    try:
        result = await db_client.admin.command("serverStatus")
        if result['ok'] == 1.0:
            return {"status": "available"}
        else:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="MongoDB serverStatus not ok")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=str(e))

# --------------------------------------
#           Scheduler
# --------------------------------------

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from app.models.order_model import Order, OrderStatus
import asyncio

async def cancel_old_orders():
    now = datetime.utcnow()
    async for order in Order.find({"$or": [{"status": OrderStatus.PLACED}, {"status": OrderStatus.READY}], "created_at": {"$lt": now - timedelta(hours=1)}}):
        order.status = OrderStatus.CANCELLED
        order.updated_at = order.created_at + timedelta(hours=1)
        await order.save()

scheduler = AsyncIOScheduler()
scheduler.add_job(cancel_old_orders, 'interval', seconds=30)
scheduler.start()

loop = asyncio.get_event_loop()
if not loop.is_running():
    loop.run_forever()