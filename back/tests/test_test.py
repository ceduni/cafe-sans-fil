"""
Tests
"""

# FastAPI and middleware imports
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

# Database and Beanie initialization
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Application settings and router
from app.core.config import settings
from app.api.api_v1.router import router
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.models.order_model import Order
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize crucial application services including database connection and Beanie ORM.
    
    Establishes a connection to MongoDB, initializes Beanie with the database 
    and the defined models (User, Cafe, Order).
    """
    
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[settings.MONGO_DB_NAME+"test"] 

    await init_beanie(
        database=db_client,
        document_models=[
            User,
            Cafe,
            Order
        ]
    )
    yield
    
app = FastAPI(lifespan=lifespan)    
app.include_router(router, prefix=settings.API_V1_STR)


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

def test_list_cafes(test_client):
    response = test_client.get("/api/cafes")
    assert response.status_code == 200