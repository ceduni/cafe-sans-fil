"""
Main application initialization for Café Sans Fil.
Sets up FastAPI application, CORS middleware, and initializes the database connection.
"""

# FastAPI and middleware imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database and Beanie initialization
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Application settings and router
from app.core.config import settings
from app.api.api_v1.router import router
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.models.order_model import Order

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=True  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_init():
    """
    Initialize crucial application services including database connection and Beanie ORM.
    
    Establishes a connection to MongoDB, initializes Beanie with the database 
    and the defined models (User, Cafe, Order).
    """
    
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).cafesansfil 

    await init_beanie(
        database=db_client,
        document_models=[
            User,
            Cafe,
            Order
        ]
    )
    
app.include_router(router, prefix=settings.API_V1_STR)