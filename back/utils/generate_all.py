# Database and Beanie initialization
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import asyncio

# Application settings and router
from app.core.config import settings
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.models.order_model import Order

# Utils
from utils.generate_user import create_users
from utils.generate_cafe import create_cafes
from utils.generate_order import create_orders

"""
Script to generate data for the Test DB.
It can also be used to generate data for other DB.
"""
MONGO_DB_NAME = settings.MONGO_DB_NAME + "test"

async def main():
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db_client.drop_database(MONGO_DB_NAME)

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[MONGO_DB_NAME]
    await init_beanie(database=db_client, document_models=[User, Cafe, Order])

    # Generate all 
    user_ids = await create_users(26) # Must have minimum 26 Users to always have enough Staff
    cafe_menu_items_ids_dict = await create_cafes(user_ids)
    await create_orders(user_ids, cafe_menu_items_ids_dict)

if __name__ == "__main__":
    asyncio.run(main())