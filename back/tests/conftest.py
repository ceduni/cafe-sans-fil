from fastapi import FastAPI
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import pytest

# Application settings and router
from app.core.config import settings
from app.api.api_v1.router import router
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.models.order_model import Order

"""
Conftest file for pytest.
"""
MONGO_DB_NAME = settings.MONGO_DB_NAME + "test"

@asynccontextmanager
async def lifespan(app: FastAPI):    
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[MONGO_DB_NAME] 
    await init_beanie(database=db_client, document_models=[User, Cafe, Order])
    yield
    
app = FastAPI(lifespan=lifespan)    
app.include_router(router, prefix=settings.API_V1_STR)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def auth_login(client):
    login_data = {
        "username": "cafesansfil",
        "password": "cafesansfil",
    }
    response = client.post("/api/auth/login", data=login_data)
    return response.json()

@pytest.fixture(scope="module")
def list_cafes(client):
    response = client.get("/api/cafes")
    return response.json()

@pytest.fixture(scope="module")
def list_orders(client, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.get("/api/orders", headers=headers)
    return response.json()

@pytest.fixture(scope="module")
def list_users(client, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.get("/api/users", headers=headers)
    return response.json()