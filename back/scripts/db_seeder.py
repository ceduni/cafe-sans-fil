# scripts/db_seeder.py

# Database and Beanie initialization
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import asyncio

# Application settings and router
from app.core.config import settings
from app.models.cafe_model import Cafe
from app.models.menu_model import MenuItem
from app.models.announcement_model import Announcement
from app.models.event_model import Event
from app.models.user_model import User
from app.models.order_model import Order

from scripts.db_seed import UserSeeder, CafeSeeder, StaffSeeder, MenuSeeder 

MONGO_DB_NAME = settings.MONGO_DB_NAME
print (f"Seeding data for {MONGO_DB_NAME}")

async def main():
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db_client.drop_database(MONGO_DB_NAME)

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[MONGO_DB_NAME]
    await init_beanie(database=db_client, document_models=[Cafe, MenuItem, Announcement, Event, User, Order])

    user_seeder = UserSeeder()
    cafe_seeder = CafeSeeder()
    staff_seeder = StaffSeeder()
    menu_seeder = MenuSeeder()

    # Seed users
    await user_seeder.seed_users(num_users=27)

    # Seed cafes
    await cafe_seeder.seed_cafes(num_cafes=20)

    # Seed staff for cafes
    await staff_seeder.seed_staff_for_cafes(
        cafe_ids=cafe_seeder.get_cafe_ids(),
        usernames=user_seeder.get_usernames()
    )

    # Seed menu items for cafes
    await menu_seeder.seed_menu_items(
        cafe_ids=cafe_seeder.get_cafe_ids(),
        num_items=20
    )

if __name__ == "__main__":
    asyncio.run(main())