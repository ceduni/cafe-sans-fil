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

# Models and routers
from app.api.router import router
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.models.order_model import Order

app = FastAPI(
    title="Café Sans Fil",
    # openapi_url="/api/openapi.json",
    debug=True  
)

origins = [
    # "http://localhost:3000",
    "http://localhost:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

    # Using local MongoDB instance
    # db_client = AsyncIOMotorClient('mongodb://localhost:27017/').cafesansfil

    # Using cloud-based MongoDB cluster
    db_client = AsyncIOMotorClient("mongodb+srv://cafesansfil:cafesansfil@cluster0.lhfxwrd.mongodb.net/?retryWrites=true&w=majority").cafesansfil #
    
    await init_beanie(
        database=db_client,
        document_models=[
            User,
            Cafe,
            Order
        ]
    )
    
app.include_router(router, prefix="/api")
