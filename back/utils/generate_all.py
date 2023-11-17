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
from utils.generate_users import create_users
from utils.generate_cafes import create_cafes
from utils.generate_orders import create_orders

async def main():
    # Initialize Beanie
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[settings.MONGO_DB_NAME + "test"]
    await init_beanie(database=db_client, document_models=[User, Cafe, Order])

    # Generate all 
    user_ids = await create_users(26) # Must have minimum 26 Users to always have enough Staff
    cafe_menu_items_ids_dict = await create_cafes(user_ids)
    await create_orders(user_ids, cafe_menu_items_ids_dict)

if __name__ == "__main__":
    asyncio.run(main())
