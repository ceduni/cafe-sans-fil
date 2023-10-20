from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

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
    "http://localhost:3000",  
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
    Initialize crucial application services.
    """
    # Establish a connection to MongoDB
    # db_client = AsyncIOMotorClient('mongodb://localhost:27017/').cafesansfil
    db_client = AsyncIOMotorClient("mongodb+srv://cafesansfil:cafesansfil@cluster0.lhfxwrd.mongodb.net/?retryWrites=true&w=majority").cafesansfil
    
    # Initialize Beanie with database and models
    await init_beanie(
        database=db_client,
        document_models=[
            User,
            Cafe,
            Order
        ]
    )
    
app.include_router(router, prefix="/api")
