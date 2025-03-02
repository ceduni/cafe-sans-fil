from contextlib import asynccontextmanager

import pytest
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.cafe.models import Cafe
from app.cafe.order.models import Order

# Application settings and router
from app.config import settings
from app.router import router
from app.user.models import User

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
        "username": "7802085",
        "password": "Cafepass1",
    }
    response = client.post("/api/auth/login", data=login_data)
    return response.json()


@pytest.fixture(scope="module")
def list_cafes(client):
    response = client.get("/api/cafes?sort_by=_id")
    return response.json()


@pytest.fixture(scope="module")
def list_orders(client, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.get("/api/orders?sort_by=_id", headers=headers)
    return response.json()


@pytest.fixture(scope="module")
def list_users(client, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.get("/api/users?sort_by=_id", headers=headers)
    return response.json()
